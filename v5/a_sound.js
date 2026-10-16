/* ===================== ИТП 6.4.6 — звуки в стиле Discord и Telegram =====================
   Ни одного звукового файла, сэмпла или модели: всё синтезируется кодом (Web Audio) в этом модуле.
   Образ: чистые синусы без «стуков» и шума, ноты от соль малой до до третьей октавы, простые интервалы (квинта, кварта, октава),
   двух-трёхнотные фразы. Вверх — включить, верно, награда; вниз — выключить, ошибка. Основа — замеры настоящих звуков
   Discord и Telegram (частоты, интервалы, обертоны), но мелодии и ноты свои; записи не используются. Звуки выбраны по оценкам
   владельца из двух наборов (A Discord, B Telegram); где понравились оба, они ЧЕРЕДУЮТСЯ (случайно, но не один и тот же дважды подряд).
   Все ноты берутся из одного строя: до-мажорная пентатоника (до, ре, ми, соль, ля), поэтому любые два звука подряд не диссонируют.
   Переходы между экранами без звука. Одна «нижняя панель» для всех разделов.

   Как это устроено:
     SXD   — таблица звуков-вариантов (tap_1, tap_2, correct_1, …). У записи: fn — рецепт (времена в секундах, частоты в герцах),
             p — приоритет (0 касания, 1 обратная связь, 2 награды: младшие звуки приглушаются старшими), j — разброс высоты
             (0,035 = ±3,5 %), min — пауза между такими звуками (мс), dur — сколько секунд голос занят, w — доля комнаты (0…1),
             pk — ЦЕЛЕВОЙ пик в дБ от полной шкалы, lv — поправка уровня в дБ (её подбирает tests/sound_wav.py --calibrate).
     SXM   — события приложения (tap, ok, bad, …) → список вариантов (чередуются) и флаги: ui — только при включённых «Звуках интерфейса»,
             win — не накладывать на недавние награды. Вызов snd('ok') сам выбирает вариант (sxPick).
   КАК ИЗМЕНИТЬ ЗВУК: правьте рецепт fn нужного варианта (ноты из SXN_), потом запустите tests/sound_wav.py --calibrate (меняет только lv),
   tests/mk_preview.py и откройте sounds-preview.html. Какие события какие варианты играют — таблица SXM.

   Правила: AudioContext создаётся только после первого касания; без Web Audio, при выключенном звуке и до первого
   касания все вызовы тихо ничего не делают. Звуки вызываются из тех же событий, что и анимации, и не зависят от
   содержания тем: новая тема и островок получают их автоматически. */
var SX={c:null,x:null,dead:false,ln:'',lt:0,la:0,lf:0,cs:'',per:{},pv:{},vol:1,pend:null,hid:false};

/*==== ENGINE:BEGIN (без зависимостей от приложения; sounds-preview.html копирует этот кусок) ====*/
/* ноты строя (до-мажорная пентатоника), Гц */
var SXN_={G3:196,C4:261.63,D4:293.66,E4:329.63,G4:392,A4:440,C5:523.25,D5:587.33,E5:659.25,G5:783.99,A5:880,C6:1046.5,D6:1174.7,E6:1318.5,G6:1568};
function sxDb(d){return Math.pow(10,d/20)}
/* громкость 0–100 % → усиление. 70 % — опорная точка, на ней пики таблицы SXD совпадают с заданными (pk) */
function sxGain(v){return v<=0?0:Math.min(1.8,Math.pow(v/70,1.5))}
/* детерминированный ГСЧ для шума и комнаты: звук в проверках и в приложении одинаковый */
function sxRng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var t=Math.imul(s^s>>>15,1|s);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}

/* общая шина: фильтры → громкость → ограничитель; крошечная комната (45 мс) отдельной веткой */
function sxBuild(c,det){
  var sr=c.sampleRate,R=sxRng(20261014),bus=c.createGain(),hp=c.createBiquadFilter(),lp=c.createBiquadFilter(),mst=c.createGain(),
      lim=c.createWaveShaper(),conv=c.createConvolver(),rl=c.createBiquadFilter();
  hp.type='highpass';hp.frequency.value=70;hp.Q.value=.5;           /* убираем гул, телефон его всё равно не воспроизводит */
  lp.type='lowpass';lp.frequency.value=6000;lp.Q.value=.5;          /* страховка: выше 6 кГц ничего не звучит */
  /* ограничитель пиков: статическая мягкая кривая. До −6 дБ от полной шкалы сигнал не меняется (в штатной работе пики −16 дБ и ниже),
     выше плавно сжимается к потолку −1 дБ, клиппинга нет. DynamicsCompressorNode пробовал и убрал: его усиление зависит от истории
     сигнала (замер: один и тот же звук на 11 дБ тише в первые 100 мс жизни контекста) и он добавляет ~6 мс задержки */
  var cv=new Float32Array(2049);for(var j=0;j<2049;j++){var u=j/1024-1,m=Math.abs(u);cv[j]=m<=.5?u:(u<0?-1:1)*(.5+.5*Math.tanh((m-.5)/.5))}lim.curve=cv;
  var n=Math.round(sr*.045),ir=c.createBuffer(1,n,sr),d=ir.getChannelData(0),p=0;
  for(var i=0;i<n;i++){p=p*.5+(R()*2-1)*.5;d[i]=p*Math.pow(1-i/n,2.5)}d[n-1]=0;
  conv.buffer=ir;rl.type='lowpass';rl.frequency.value=3700;rl.Q.value=.4;
  var nz=c.createBuffer(1,sr,sr),nd=nz.getChannelData(0);for(var k=0;k<sr;k++)nd[k]=R()*2-1;
  bus.connect(hp);hp.connect(lp);lp.connect(mst);mst.connect(lim);lim.connect(c.destination);
  conv.connect(rl);rl.connect(bus);
  return{c:c,bus:bus,mst:mst,lim:lim,conv:conv,nz:nz,det:!!det,voices:[],last:{}}}

/* огибающая: 0 → пик за att (линейно, 1–3 мс: без щелчка) → экспоненциальный спад → линейное затухание до ТОЧНОГО нуля в момент T+d */
function sxEnv(g,T,pk,att,d){
  var fz=Math.min(.008,d*.25),e=Math.max(att+.001,d-fz),p=g.gain;
  p.setValueAtTime(0,T);p.linearRampToValueAtTime(pk,T+att);
  p.exponentialRampToValueAtTime(Math.max(pk*.002,1e-5),T+e);p.linearRampToValueAtTime(0,T+d)}
function sxSrc(v,s,T,E,off){if(off===undefined)s.start(T);else s.start(T,off);s.stop(E);v.srcs.push(s)}
/* тон из затухающих частичных. o: f (Гц), d (с), amp, att (с), parts=[[кратность,сила,доля длины]…], lpm — срез как кратность f */
function sxTone(v,t,o){
  var c=v.c,T=v.t0+t,F=o.f*v.pit,lp=c.createBiquadFilter(),parts=o.parts||[[1,1,1]],att=o.att||.002,amp=o.amp===undefined?1:o.amp;
  lp.type='lowpass';lp.frequency.value=o.lp||Math.min(5200,F*(o.lpm||6));lp.Q.value=o.q||.5;lp.connect(v.mix);
  parts.forEach(function(q){
    var fr=F*q[0];if(fr>5600)return;
    var os=c.createOscillator(),g=c.createGain();os.type='sine';os.frequency.value=fr;
    sxEnv(g,T,amp*q[1],att,o.d*q[2]);os.connect(g);g.connect(lp);sxSrc(v,os,T,T+o.d*q[2]+.01)})}
/* чистая нота: синус */
function sxSn(v,t,f,d,amp,att){sxTone(v,t,{f:f,d:d,amp:amp===undefined?1:amp,att:att||.006,parts:[[1,1,1]],lpm:6})}
/* нота с октавой: «глухие» низкие ноты и короткие блипы (слышны и на телефоне); атака 3 мс (Discord) и 6 мс (Telegram) */
function sxBk(v,t,f,d,amp,att){sxTone(v,t,{f:f,d:d,amp:amp===undefined?1:amp,att:att||.003,parts:[[1,1,1],[2,.5,.6]],lpm:6})}
function sxBt(v,t,f,d,amp,att){sxTone(v,t,{f:f,d:d,amp:amp===undefined?1:amp,att:att||.006,parts:[[1,1,1],[2,.45,.6]],lpm:6})}
/* ступени «опыта»: тик поднимается по строю до ми6 и дальше не растёт (не станет пронзительным) */
var SXXP=[SXN_.E5,SXN_.G5,SXN_.A5,SXN_.C6,SXN_.D6,SXN_.E6];
var N_=SXN_;

/* ---- словарь звуков-вариантов ---- */
var SXD={
  tap_1:{p:0,j:.035,min:55,dur:.07,w:.04,pk:-23.8,lv:-23.58,fn:function(v){sxSn(v,0,N_.G5,.045,1,.003)}},
  tap_2:{p:0,j:.035,min:55,dur:.07,w:.03,pk:-23.8,lv:-23.9,fn:function(v){sxBk(v,0,N_.G3,.05,1)}},
  nav_1:{p:0,j:.035,min:55,dur:.15,w:.06,pk:-25.7,lv:-25.67,fn:function(v){sxSn(v,0,N_.E5,.08,.9);sxSn(v,.06,N_.D5,.085,1)}},
  toggle_on_1:{p:0,j:.035,min:90,dur:.15,w:.05,pk:-25.7,lv:-25.92,fn:function(v){sxSn(v,0,N_.C5,.08,.9);sxSn(v,.055,N_.G5,.09,1)}},
  toggle_off_1:{p:0,j:.035,min:90,dur:.15,w:.05,pk:-25.7,lv:-25.46,fn:function(v){sxSn(v,0,N_.C5,.08,.9);sxSn(v,.055,N_.G4,.09,1)}},
  sheet_open_1:{p:0,j:.035,min:160,dur:.18,w:.08,pk:-31,lv:-30.26,fn:function(v){sxSn(v,0,N_.A5,.14,.9)}},
  sheet_close_1:{p:0,j:.035,min:160,dur:.2,w:.08,pk:-30.4,lv:-32.03,fn:function(v){sxSn(v,0,N_.D4,.08,.9);sxBk(v,.07,N_.G3,.11,.9)}},
  correct_1:{p:1,j:.03,min:90,dur:.34,w:.12,pk:-23,lv:-23.26,fn:function(v){sxSn(v,0,N_.G4,.14,.95);sxSn(v,.1,N_.G5,.26,1)}},
  correct_2:{p:1,j:.03,min:90,dur:.34,w:.14,pk:-24.5,lv:-24.77,fn:function(v){sxSn(v,0,N_.G5,.28,.9,.008);sxSn(v,.07,N_.C6,.26,.9,.008)}},
  wrong_1:{p:1,j:.035,min:120,dur:.3,w:0,pk:-22.4,lv:-25.45,fn:function(v){sxBk(v,0,N_.C4,.12,1);sxBk(v,.1,N_.G3,.2,.9)}},
  wrong_2:{p:1,j:.035,min:120,dur:.3,w:0,pk:-22,lv:-22.72,fn:function(v){sxBt(v,0,N_.C4,.07,1);sxBt(v,.11,N_.C4,.1,.9)}},
  wrong_3:{p:1,j:.035,min:120,dur:.3,w:0,pk:-23.3,lv:-25.27,fn:function(v){sxBt(v,0,N_.C4,.1,1);sxBt(v,.1,N_.G3,.18,.9)}},
  hint_1:{p:1,j:.03,min:220,dur:.32,w:.12,pk:-24.5,lv:-24.61,fn:function(v){sxSn(v,0,N_.C5,.28,1)}},
  hint_2:{p:1,j:.03,min:220,dur:.3,w:.12,pk:-24.5,lv:-24.69,fn:function(v){sxSn(v,0,N_.A5,.26,1)}},
  xp_1:{p:0,j:.035,min:40,dur:.07,w:0,pk:-29.1,lv:-27.76,fn:function(v,a){sxSn(v,0,SXXP[Math.min(5,a.k||0)],.04,.9,.003)}},
  xp_2:{p:0,j:.035,min:40,dur:.07,w:0,pk:-30.6,lv:-29.42,fn:function(v,a){sxSn(v,0,SXXP[Math.min(5,a.k||0)],.05,.9,.006)}},
  complete_1:{p:2,j:.03,min:400,dur:.6,w:.14,pk:-22,lv:-22.39,fn:function(v){sxSn(v,0,N_.C4,.14,.9);sxSn(v,.09,N_.G4,.16,1);sxSn(v,.18,N_.G5,.4,1)}},
  streak_1:{p:2,j:.03,min:450,dur:.48,w:.12,pk:-22.5,lv:-22.63,fn:function(v){sxSn(v,0,N_.G4,.2,1);sxSn(v,.11,N_.C5,.34,1)}},
  streak_2:{p:2,j:.03,min:450,dur:.48,w:.14,pk:-23.5,lv:-23.85,fn:function(v){sxSn(v,0,N_.A5,.16,1);sxSn(v,.1,N_.C6,.34,1)}},
  achievement_1:{p:2,j:.03,min:450,dur:.92,w:.18,pk:-18.3,lv:-24.15,fn:function(v){
      [N_.C5,N_.D5,N_.G5,N_.C6,N_.D6].forEach(function(f,i){sxSn(v,i*.07,f,.3,.85)});
      sxSn(v,.38,N_.C5,.5,.75);sxSn(v,.38,N_.G5,.5,.75);sxSn(v,.38,N_.C6,.46,.6);sxSn(v,.45,N_.E6,.3,.18)}},
  run_1:{p:0,j:.035,min:120,dur:.06,w:0,pk:-22.3,lv:-23.54,fn:function(v){sxBk(v,0,N_.G5,.035,.9)}},
  run_2:{p:0,j:.035,min:120,dur:.06,w:0,pk:-22.4,lv:-21.63,fn:function(v){sxSn(v,0,N_.C6,.03,.9,.003)}},
  key_1:{p:0,j:.035,min:28,dur:.04,w:0,pk:-40.4,lv:-38.45,fn:function(v){sxSn(v,0,N_.C6,.02,.8,.003)}},
  del_1:{p:0,j:.035,min:28,dur:.04,w:0,pk:-40,lv:-37.87,fn:function(v){sxSn(v,0,N_.G5,.02,.8,.003)}},
  error_1:{p:1,j:.035,min:300,dur:.2,w:0,pk:-28,lv:-28.19,fn:function(v){sxSn(v,0,N_.D5,.08,1,.008);sxSn(v,.07,N_.A4,.13,.95,.008)}},
  error_2:{p:1,j:.035,min:300,dur:.2,w:0,pk:-24.6,lv:-25.92,fn:function(v){sxBt(v,0,N_.A4,.06,1);sxBt(v,.1,N_.A4,.08,.9)}}
};
/* события приложения → варианты (чередуются) */
var SXM={
  tap:{v:['tap_1','tap_2'],ui:1},tick:{v:['tap_1','tap_2'],ui:1},
  on:{v:['toggle_on_1'],ui:1},off:{v:['toggle_off_1'],ui:1},
  lock:{v:['tap_2'],ui:1},                                  /* закрытый островок: глухая низкая нота */
  run:{v:['run_1','run_2'],ui:1},err:{v:['error_1','error_2']},key:{v:['key_1']},   /* key: ввод key_1, стирание del_1 */
  open:{v:['sheet_open_1'],ui:1,win:1},close:{v:['sheet_close_1'],ui:1,win:1},
  unlock:{v:['correct_2'],ui:1},disk:{v:['toggle_on_1'],ui:1},
  ok:{v:['correct_1','correct_2']},solve:{v:['correct_1','correct_2']},theory:{v:['correct_1','correct_2']},
  bad:{v:['wrong_1','wrong_2','wrong_3']},hint:{v:['hint_1','hint_2']},xpt:{v:['xp_1','xp_2']},
  done:{v:['complete_1']},level:{v:['complete_1']},fanfare:{v:['complete_1']},
  streak:{v:['streak_1','streak_2']},freeze:{v:['toggle_off_1']},ach:{v:['achievement_1']},pet:{v:['toggle_on_1']}};
/* какой вариант играть: нижняя панель — один звук; печать и стирание — разные; иначе случайный, но не тот же, что в прошлый раз */
function sxPick(n,a){
  var m=SXM[n];if(!m)return null;
  if(n==='tap'&&a&&a.nav>=0)return 'nav_1';
  if(n==='key')return a&&a.k===1?'del_1':'key_1';
  if(n==='xpt'&&a&&SXD[a.v])return a.v;
  var l=m.v;if(l.length===1)return l[0];
  var p=SX.pv[n],c,k=0;do{c=l[Math.floor(Math.random()*l.length)]}while(c===p&&++k<8);
  return c}

/* запуск одного звука на аудио-часах (без задержки): гуманизация, приглушение старых голосов, не более 6 голосов */
function sxFire(x,n,a){
  var d=SXD[n];if(!d)return null;
  var c=x.c,now=c.currentTime,pit=1,gdb=0,jit=0;
  if(!x.det){
    var L=x.last[n]||(x.last[n]={p:1,t:-1e9}),tm=performance.now();
    for(var k=0;k<8;k++){pit=1+d.j*(Math.random()*2-1);if(Math.abs(pit-L.p)>=.008)break}  /* два подряд никогда не звучат на одной высоте */
    L.p=pit;gdb=(Math.random()*2-1)*1.5;                       /* ±1,5 дБ */
    if(tm-L.t<1500)jit=Math.random()*.004;                     /* дрожание времени у повторов */
    L.t=tm}
  var T0=now+.003+jit,vs=x.voices=x.voices.filter(function(w){return w.end>now});
  vs.forEach(function(w){if(w.p<=d.p)w.duck.gain.setTargetAtTime(.35,T0,.012)});            /* новые звуки приглушают старые */
  if(vs.length>=6){                                                                           /* не больше 6 одновременно */
    var o=vs.slice().sort(function(p,q){return p.p-q.p||p.end-q.end})[0];
    o.duck.gain.setTargetAtTime(0,T0,.004);o.srcs.forEach(function(s){try{s.stop(T0+.03)}catch(e){}});o.end=T0+.03;vs.splice(vs.indexOf(o),1)}
  var v={c:c,x:x,mix:c.createGain(),duck:c.createGain(),srcs:[],pit:pit,t0:T0,end:T0+d.dur,p:d.p};
  v.mix.gain.value=sxDb(d.lv+gdb);v.mix.connect(v.duck);v.duck.connect(x.bus);
  if(d.w>0){var sn=c.createGain();sn.gain.value=d.w;v.duck.connect(sn);sn.connect(x.conv)}
  d.fn(v,a||{});
  vs.push(v);
  if(!x.det)setTimeout(function(){try{v.duck.disconnect()}catch(e){}},(d.dur+.5)*1e3);
  return v}
function sxKill(x){
  var now=x.c.currentTime;
  x.voices.forEach(function(w){w.duck.gain.cancelScheduledValues(now);w.duck.gain.setTargetAtTime(0,now,.004);w.srcs.forEach(function(s){try{s.stop(now+.03)}catch(e){}});w.end=now});
  x.voices=[]}
/* отрисовка звука без динамиков: Float32Array. Для проверок и страницы sounds-preview.html */
function sxRender(n,a,sr){
  var OC=window.OfflineAudioContext||window.webkitOfflineAudioContext;sr=sr||44100;
  if(!OC||!SXD[n])return Promise.resolve(null);
  var c=new OC(1,Math.ceil(sr*(SXD[n].dur+.35)),sr),x=sxBuild(c,true);x.mst.gain.value=1;sxFire(x,n,a);
  return c.startRendering().then(function(b){return b.getChannelData(0)})}

/* AudioContext — только по касанию. Возвращает true, если контекст есть */
function sxEnsure(){
  if(SX.dead)return false;
  try{
    if(!SX.c){
      var AC0=window.AudioContext||window.webkitAudioContext;if(!AC0){SX.dead=true;return false}
      /* беззвучный режим телефона: «ambient» подчиняется переключателю звонка и не прерывает музыку (Safari 16.4+) */
      try{if(navigator.audioSession)navigator.audioSession.type='ambient'}catch(e){}
      SX.c=new AC0({latencyHint:'interactive'});SX.x=sxBuild(SX.c,false);SX.x.mst.gain.value=SX.vol}
    if(SX.c.state!=='running')sxResume();
    return true
  }catch(e){SX.dead=true;return false}}
function sxResume(){
  try{var p=SX.c.resume();if(p&&p.then)p.then(function(){
    var q=SX.pend;SX.pend=null;if(q&&performance.now()-q.t<400&&SX.c.state==='running'&&!document.hidden)sxFire(SX.x,q.n,q.a)},function(){SX.pend=null})}catch(e){}}
function sxVol(g){if(g!==undefined)SX.vol=g;if(SX.x)SX.x.mst.gain.setTargetAtTime(SX.vol,SX.c.currentTime,.015)}
/* играть сейчас. Если браузер ещё не разрешил звук (контекст не running), звук не копится: максимум один, и только свежий */
function sxPlay(n,a){
  if(!SX.x||SX.dead)return;
  if(SX.c.state!=='running'){SX.pend={n:n,a:a,t:performance.now()};sxResume();return}
  sxFire(SX.x,n,a)}
/* вкладка скрыта: гасим и обрываем всё, контекст спит; вернулись — просыпаемся */
function sxHide(){
  SX.hid=true;if(!SX.c)return;
  try{sxKill(SX.x);SX.x.mst.gain.setTargetAtTime(0,SX.c.currentTime,.005);
    setTimeout(function(){try{if(document.hidden&&SX.c.state==='running')SX.c.suspend()}catch(e){}},60)}catch(e){}}
function sxShow(){
  SX.hid=false;if(!SX.c)return;
  try{SX.x.mst.gain.setTargetAtTime(SX.vol,SX.c.currentTime+.02,.015);if(SX.c.state!=='running')sxResume()}catch(e){}}
/*==== ENGINE:END ====*/

/* ===== интеграция с приложением ===== */
/* прежние названия звуков → новые */
var SXNM={click:'tap',chord:'solve',xp:'xpt'};
function VOLK(){return sxGain(ST('vol'))}

['pointerup','touchend','click','keydown'].forEach(function(ev){document.addEventListener(ev,function(){sxEnsure()},{capture:true,passive:true})});
document.addEventListener('visibilitychange',function(){if(document.hidden)sxHide();else sxShow()});
window.addEventListener('pagehide',sxHide);
window.addEventListener('pageshow',function(){if(!document.hidden)sxShow()});

function sndRecent(n,ms){return SX.ln===n&&performance.now()-SX.lt<ms}
function snd(x,a){
  if(typeof S==='undefined'||!S||S.mute||document.hidden)return;
  var n;
  if(typeof x==='string')n=SXNM[x]||x;
  else if(Array.isArray(x)){
    /* старые вызовы с нотами: известные сочетания получают свой звук */
    var l=x.length;
    if(l===1&&x[0]===200)n='lock';
    else if(l>=5){n=SX.cs||'fanfare';SX.cs=''}
    else if(l===2&&x[0]===659&&x[1]===784)n='pet';
    else if(l===3&&x[0]===784){n='xpt';a={k:3}}
    else n='ok'}
  else return;
  var m=SXM[n];if(!m)return;                              /* переходы между экранами (go, back) без звука */
  if(m.ui&&!ST('sfx'))return;
  if(n==='key'&&!ST('ks'))return;
  var v=sxPick(n,a),d=SXD[v];if(!d)return;
  var now=performance.now();
  if(n!=='tap'&&n!=='key')SX.la=now;
  if(!m.ui)SX.lf=now;
  /* звуки окон не накладываются на награды, сыгравшие только что */
  if(m.win&&now-SX.lf<260)return;
  if(SX.per[n]&&now-SX.per[n]<d.min)return;
  SX.per[n]=now;SX.ln=n;SX.lt=now;SX.pv[n]=v;
  if(!SX.c||SX.dead)return;                              /* до первого касания звука нет */
  try{sxVol(VOLK());sxPlay(v,a)}catch(e){}}

/* касание любой кнопки: короткий чистый звук (вариант чередуется). Другие звуки того же события (ответ, окно, переход, переключатель) его заменяют:
   проверка отложена на конец события. «Запустить» играет свой тик. */
document.addEventListener('click',function(e){
  var b=e.target&&e.target.closest&&e.target.closest('button,[role=button],a[href],summary');
  if(!b||b.disabled||b.getAttribute('aria-disabled')==='true')return;
  var t=performance.now(),nv=b.closest&&b.closest('.nav'),run=b.id==='run'&&!b.classList.contains('stp');
  setTimeout(function(){
    if(SX.la>=t)return;
    var a=null;if(nv){var bs=[].slice.call(nv.querySelectorAll('button'));a={nav:bs.indexOf(b)}}
    snd(run?'run':'tap',a)},0)},true);

/* печать в редакторе: ввод — один звук, стирание — другой, очень тихие; только если включено «Звуки набора кода» (по умолчанию выключено) */
document.addEventListener('beforeinput',function(e){
  var t=e.target;if(!t||t.tagName!=='TEXTAREA'||!t.closest||!t.closest('.ed')||!ST('ks'))return;
  var ty=e.inputType||'';
  if(/^deleteContent/.test(ty))snd('key',{k:1});
  else if(ty==='insertText'||ty==='insertLineBreak'||ty==='insertParagraph')snd('key',{k:0})},true);

/* счёт опыта: каждый засчитанный пункт даёт тик, высота растёт по ступеням до верхнего предела. Вариант тика выбирается на весь счёт
   (иначе ступени вверх звучали бы рвано). Вызывать с текущим числом */
function xpTick(){var n=0,last=0,lt=0,w=sxPick('xpt');return function(v){if(v<=last)return;last=v;var t=performance.now();if(t-lt<48)return;lt=t;snd('xpt',{k:n++,v:w})}}

/* для проверок: отрисовать звук без динамиков и вернуть сэмплы (tests/sound_wav.py, tests/sound6.py) */
function sndRender(n,a){return sxRender(n,a,44100).then(function(b){return b&&Array.from(b)})}
