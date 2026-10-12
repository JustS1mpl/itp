/* ===================== ИТП 6 — звуковой дизайн =====================
   Ни одного звукового файла и ни одного сэмпла: всё синтезируется Web Audio (осцилляторы, шум, огибающие, фильтры).
   Семейство одного инструмента: «мягкая калимба». Основа каждого звука — синусный щипок с очень коротким нарастанием
   (4 мс) и плавным затуханием, к нему добавлены тихий октавный обертон и едва слышный «колокольный» призвук. Весь звук
   идёт через общую шину: фильтр низких частот (срез 5,6 кГц, поэтому нет ничего резкого), крошечная комнатная
   реверберация, генерируемая кодом, и ограничитель громкости. Ноты берутся только из пентатоники до-мажора, поэтому
   любые два звука, сыгранные подряд или вместе, не конфликтуют.
   Звуки вызываются из тех же событий, что и анимации (ответ, опыт, достижение, окно, переход), и не зависят от
   содержания тем: новая тема или островок получают их автоматически.
   Правила: контекст создаётся только после первого касания; без Web Audio, при выключенном звуке и до первого касания
   все вызовы тихо ничего не делают. */
var SX={c:null,x:null,ln:'',lt:0,la:0,lf:0,act:0,cs:'',per:{},dead:false};
/* звуки интерфейса (касания, переходы, окна) подчиняются переключателю «Звуки интерфейса», остальные — только общему «Звук» */
var SXUI={tap:1,tick:1,lock:1,go:1,back:1,open:1,close:1,disk:1,unlock:1};
/* минимальная пауза между одинаковыми звуками, мс: так двойное нажатие не превращается в «пулемёт» */
var SXMIN={tap:90,tick:60,lock:160,go:160,back:160,open:160,close:160,disk:160,unlock:200,ok:90,solve:120,bad:120,xp:150,done:400,level:500,fanfare:700,streak:450,ach:450,hint:220,theory:300,freeze:450,pet:220};
var SXN={click:'tap',chord:'solve'};
/* C5 D5 E5 G5 A5 C6 D6 E6 G6 C7 */
var NC5=523.25,ND5=587.33,NE5=659.25,NG5=783.99,NA5=880,NC6=1046.5,ND6=1174.7,NE6=1318.5,NG6=1568,NC7=2093;
function VOLK(){return Math.min(1.4,ST('vol')/70)}

/* общая шина: фильтр → (сухой + реверберация) → ограничитель → громкость */
function sxBuild(c){
  var bus=c.createGain(),lp=c.createBiquadFilter(),comp=c.createDynamicsCompressor(),master=c.createGain(),send=c.createGain(),conv=c.createConvolver();
  lp.type='lowpass';lp.frequency.value=5600;lp.Q.value=.4;
  comp.threshold.value=-16;comp.knee.value=12;comp.ratio.value=8;comp.attack.value=.004;comp.release.value=.14;
  /* комната 0,4 с: затухающий шум, смягчённый скользящим средним */
  var sr=c.sampleRate,n=Math.round(sr*.4),ir=c.createBuffer(2,n,sr);
  for(var ch=0;ch<2;ch++){var d=ir.getChannelData(ch),p=0;for(var i=0;i<n;i++){p=p*.55+(Math.random()*2-1)*.45;d[i]=p*Math.pow(1-i/n,3.2)}}
  conv.buffer=ir;send.gain.value=.15;
  var nz=c.createBuffer(1,Math.round(sr*.6),sr),nd=nz.getChannelData(0);for(var k=0;k<nd.length;k++)nd[k]=Math.random()*2-1;
  bus.connect(lp);lp.connect(comp);lp.connect(send);send.connect(conv);conv.connect(comp);comp.connect(master);master.connect(c.destination);
  return{c:c,bus:bus,master:master,nz:nz,t0:0}}

/* щипок: основной тон + октава + тихий «колокольчик»; dull — приглушённый вариант для ошибки и замка */
function sxP(x,t,f,d,v,o){
  o=o||{};var c=x.c,T=x.t0+t,g=c.createGain(),lp=c.createBiquadFilter();
  lp.type='lowpass';lp.frequency.value=o.dull?Math.min(1500,f*3):Math.min(5200,f*5);
  g.gain.setValueAtTime(.0001,T);g.gain.linearRampToValueAtTime(v,T+.004);g.gain.exponentialRampToValueAtTime(.0001,T+d);
  lp.connect(g);g.connect(x.bus);
  var parts=o.dull?[[1,1,1]]:[[1,1,1],[2,.2,.55],[2.76,.06,.22]];
  parts.forEach(function(p){
    var os=c.createOscillator(),pg=c.createGain();os.type='sine';os.frequency.setValueAtTime(f*p[0],T);
    if(o.to)os.frequency.exponentialRampToValueAtTime(o.to*p[0],T+d*.8);
    pg.gain.setValueAtTime(p[1],T);if(p[2]<1)pg.gain.exponentialRampToValueAtTime(.0001,T+d*p[2]);
    os.connect(pg);pg.connect(lp);SX.act++;os.onended=function(){SX.act--};os.start(T);os.stop(T+d+.05)})}
/* «шух»: шум через полосовой фильтр, частота скользит вверх или вниз */
function sxS(x,t,d,v,f0,f1){
  var c=x.c,T=x.t0+t,s=c.createBufferSource(),bp=c.createBiquadFilter(),g=c.createGain();
  s.buffer=x.nz;s.loop=true;bp.type='bandpass';bp.Q.value=1.1;
  bp.frequency.setValueAtTime(f0,T);bp.frequency.exponentialRampToValueAtTime(f1,T+d);
  g.gain.setValueAtTime(.0001,T);g.gain.linearRampToValueAtTime(v,T+d*.35);g.gain.linearRampToValueAtTime(.0001,T+d);
  s.connect(bp);bp.connect(g);g.connect(x.bus);SX.act++;s.onended=function(){SX.act--};s.start(T,Math.random()*.3);s.stop(T+d+.02)}

/* словарь звуков. Громкости подобраны так, чтобы пик каждого был около −20…−13 дБ при громкости 70% */
var SXV={
  /* касание: «ток» с лёгким падением тона; в нижней панели у каждого раздела своя нота пентатоники */
  tap:function(x,a){var i=a&&a.nav!==undefined?a.nav:-1;if(i>=0)sxP(x,0,[NC5,NE5,NG5,NA5][i%4],.16,.2);else sxP(x,0,880,.07,.12,{to:700})},
  tick:function(x){sxP(x,0,NG6,.06,.08)},
  lock:function(x){sxP(x,0,220,.14,.14,{dull:1,to:196})},
  /* верный ответ: восходящая квинта */
  ok:function(x){sxP(x,0,NG5,.24,.13);sxP(x,.09,NC6,.28,.13)},
  /* все тесты пройдены или все вопросы верно: арпеджио */
  solve:function(x){sxP(x,0,NE5,.24,.12);sxP(x,.06,NG5,.24,.12);sxP(x,.12,NC6,.3,.13)},
  /* неверный ответ: два мягких приглушённых тона вниз, без резкости */
  bad:function(x){sxP(x,0,392,.2,.12,{dull:1});sxP(x,.12,311,.28,.11,{dull:1})},
  /* опыт: короткая искорка вверх */
  xp:function(x){[NC6,NE6,NG6,NC7].forEach(function(f,i){sxP(x,i*.05,f,.15,.065)})},
  /* островок пройден: арпеджио до-мажора */
  done:function(x){[NC5,NE5,NG5,NC6].forEach(function(f,i){sxP(x,i*.065,f,.22,.12)});sxP(x,0,261.63,.45,.06,{dull:1})},
  /* новый уровень: арпеджио подлиннее с подъёмом шума */
  level:function(x){[NC5,NE5,NG5,NC6,NE6].forEach(function(f,i){sxP(x,i*.075,f,.34,.115)});sxS(x,.05,.4,.05,500,3000)},
  /* тема пройдена, проект сделан: тема из трёх нот и аккорд */
  fanfare:function(x){sxP(x,0,NC5,.3,.065);sxP(x,.13,NG5,.3,.065);sxP(x,.26,NC6,.7,.065);sxP(x,.26,NE6,.6,.045);sxP(x,.26,NG6,.55,.035);sxP(x,.26,261.63,.7,.035,{dull:1})},
  /* серия продолжается: тёплый «динь-динь» вверх на квинту */
  streak:function(x){sxP(x,0,NG5,.26,.12);sxP(x,.11,ND6,.3,.12);sxP(x,.11,NG5/2,.3,.05,{dull:1})},
  /* достижение: богаче всех, арпеджио с октавным удвоением и мерцанием */
  ach:function(x){[NC5,NE5,NG5,NC6].forEach(function(f,i){sxP(x,i*.09,f,.4,.09);sxP(x,i*.09,f*2,.3,.03)});sxP(x,.36,NE6,.5,.07);sxP(x,.45,NG6,.5,.055);sxS(x,.3,.35,.04,2500,7000)},
  /* подсказка: «лампочка» из двух высоких нот */
  hint:function(x){sxP(x,0,NA5,.16,.1);sxP(x,.07,NE6,.22,.1)},
  /* теория прочитана: один колокольчик */
  theory:function(x){sxP(x,0,NC6,.45,.1);sxP(x,.07,NG5,.4,.07)},
  /* заморозка серии: «ледяные» ноты вниз */
  freeze:function(x){[NG6,ND6,NG5].forEach(function(f,i){sxP(x,i*.1,f,.35,.075)});sxS(x,0,.3,.03,5000,2500)},
  /* открытый островок */
  unlock:function(x){sxS(x,0,.12,.06,400,1800);sxP(x,.05,NC6,.2,.1)},
  /* окно открывается и закрывается */
  open:function(x){sxS(x,0,.13,.07,350,1800);sxP(x,.04,NE5,.15,.1)},
  close:function(x){sxS(x,0,.11,.06,1600,400);sxP(x,0,NC5,.1,.09)},
  /* переход на другой экран: еле слышный «шух» */
  go:function(x){sxS(x,0,.12,.09,300,1200)},
  back:function(x){sxS(x,0,.12,.08,1200,300)},
  /* дискета достижения: пластиковый щелчок и нота */
  disk:function(x){sxS(x,0,.04,.07,3000,1500);sxP(x,.03,NE5,.14,.08)},
  /* погладить кролика */
  pet:function(x){sxP(x,0,NA5,.2,.08);sxP(x,.09,NC6,.26,.08)}
};

/* создание контекста — только в ответ на касание или клавишу (правила автовоспроизведения) */
function sxGesture(){
  if(SX.dead)return;
  try{
    if(!SX.c){
      var AC0=window.AudioContext||window.webkitAudioContext;if(!AC0){SX.dead=true;return}
      SX.c=new AC0({latencyHint:'interactive'});SX.x=sxBuild(SX.c)}
    if(SX.c.state!=='running')SX.c.resume()
  }catch(e){SX.dead=true}}
['pointerup','touchend','click','keydown'].forEach(function(ev){document.addEventListener(ev,sxGesture,{capture:true,passive:true})});
/* экономим батарею: на скрытой вкладке звук спит, на видимой просыпается при следующем касании */
document.addEventListener('visibilitychange',function(){try{if(document.hidden&&SX.c&&SX.c.state==='running')SX.c.suspend()}catch(e){}});

function sndRecent(n,ms){return SX.ln===n&&performance.now()-SX.lt<ms}
function snd(x,a){
  if(typeof S==='undefined'||!S||S.mute)return;
  var n;
  if(typeof x==='string')n=SXN[x]||x;
  else if(Array.isArray(x)){
    /* старые вызовы с нотами: известные сочетания получают свой звук, остальные играются мягким щипком */
    var l=x.length;
    if(l===1&&x[0]===200)n='lock';
    else if(l>=5){n=SX.cs||'fanfare';SX.cs=''}
    else if(l===2&&x[0]===659&&x[1]===784)n='pet';
    else if(l===3&&x[0]===784)n='xp';
    else n='ok'}
  else return;
  if(!SXV[n])return;
  var ui=!!SXUI[n];if(ui&&!ST('sfx'))return;
  var now=performance.now();
  if(n!=='tap')SX.la=now;
  if(!ui)SX.lf=now;
  /* звуки окон и переходов не накладываются на награды, сыгравшие только что */
  if((n==='go'||n==='back'||n==='open'||n==='close')&&now-SX.lf<260)return;
  var mn=SXMIN[n]||80;if(SX.per[n]&&now-SX.per[n]<mn)return;
  SX.per[n]=now;SX.ln=n;SX.lt=now;
  if(!SX.c||SX.dead||SX.act>70)return;                /* до первого касания звука нет */
  try{
    if(SX.c.state!=='running'){SX.c.resume();return}
    var xs=SX.x;xs.t0=SX.c.currentTime+.004;xs.master.gain.value=VOLK();
    SXV[n](xs,a)
  }catch(e){}}
/* касание любой кнопки: тихое «ток». Другие звуки того же события (ответ, окно, переход) его заменяют:
   проверка отложена на конец текущего события, когда все обработчики уже отработали. */
document.addEventListener('click',function(e){
  var b=e.target&&e.target.closest&&e.target.closest('button,[role=button],a[href],summary');
  if(!b||b.disabled||b.getAttribute('aria-disabled')==='true')return;
  var t=performance.now(),nv=b.closest&&b.closest('.nav');
  setTimeout(function(){
    if(SX.la>=t)return;
    var a=null;if(nv){var bs=[].slice.call(nv.querySelectorAll('button'));a={nav:bs.indexOf(b)}}
    snd('tap',a)},0)},true);

/* для проверок: отрисовать звук без динамиков и вернуть сэмплы (используется в tests/sound6.py) */
function sndRender(n,a){
  var OC=window.OfflineAudioContext||window.webkitOfflineAudioContext,sr=44100;
  if(!OC||!SXV[n])return Promise.resolve(null);
  var c=new OC(1,sr*2,sr),x=sxBuild(c);x.t0=0;x.master.gain.value=1;SXV[n](x,a);
  return c.startRendering().then(function(b){return Array.from(b.getChannelData(0))})}
