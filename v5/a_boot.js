/* ===================== ИТП 6.6 — вступление: заставка, терминал, «синий экран» =====================
   Первый запуск: заставка со светящимся растровым кроликом и подписью IT'S THE PROGRAMMING (как логотип студии перед
   игрой) → терминал во весь экран с лёгким налётом старой видеокассеты (зерно, редкая полоса трекинга и подёргивание),
   за текстом еле заметно стекают символы → кролик спрашивает ник, обращение и первую тему → сбой, экран гаснет в точку,
   чёрный экран → «синий экран» на ~7 секунд → трещины → медленное осыпание осколками, под ними уже Путь.
   Если ник есть, а тема не выбрана, терминал открывается сразу с вопросом о теме, без заставки.
   Кролик — та же картинка, что у иконки профиля (--pi-o и --pi-f из build5.py): из неё кодом делаются растр заставки
   и контур для терминала. Всё рисуется и звучит кодом (canvas, CSS, SVG, Web Audio). При «меньше движения» нет дождя,
   зерна, печати и осколков. Переопределяет nick() и place() из a_screens.js, поэтому сброс прогресса тоже приводит сюда. */

var CRT=null,RBIMG=null;
/* значок «ввод» для кнопки у поля ника: corner-down-left из набора Lucide (лицензия ISC), тот же стиль контура, что у IC */
IC.enter='<path d="M20 4v7a4 4 0 0 1-4 4H4"/><path d="m9 10-5 5 5 5"/>';
var CRTG='01{}[]()<>=+-*/%#:;._$&|λabcdefghijklmnopqrstuvwxyzабвгдежзиклмнопрстуфхцчшэюя';
function nick(){crtOpen()}
function place(){crtOpen()}

/* --- ник: убрать «я», «меня зовут»… в начале; распознать мат, оскорбления, оскорбительные прозвища и пошлость
   (по-русски, по-английски и транслитом), в том числе замаскированные: латиница вместо кириллицы (xуй), цифры
   вместо букв (пи3да), растянутые буквы (хууууй), точки и пробелы между буквами (х.у.й). Обычные имена (Глеб,
   Хуан, Амандина, Педро, Лохматов, Сосискин, Аналитик…) под проверку не попадают: опасные корни ищутся с учётом
   начала слова или целиком */
function nkClean(s){
  var v=String(s||'').trim(),re=/^(?:я|ну\s+я|меня\s+зовут|зови\s+меня|называй\s+меня|обращайся\s+ко\s+мне|мо[её]\s+имя|мой\s+ник|ник|это|i\s+am|i'?m|my\s+name\s+is|call\s+me)[\s,:—-]+/i,k=0;
  while(re.test(v)&&k++<3){var w=v.replace(re,'').trim();if(!w)break;v=w}
  return v.replace(/^[\s«"'„“]+|[\s»"'”.!?,;:]+$/g,'')||String(s||'').trim()}
var NKG={a:'а',b:'в',c:'с',e:'е',h:'н',k:'к',m:'м',o:'о',p:'р',t:'т',x:'х',y:'у',u:'и',3:'з',0:'о',6:'б',4:'ч','@':'а'};
/* где угодно в слове (и в строке без пробелов — так ловится «х у й») */
var NKA=/ху[йеяю]|хуи|пизд|пезд|бляд|блят|пид[оа]р|пидр|педик|педераст|педрил|залуп|г[ао]ндон|шлюх|шалав|проститут|мудак|мудил|мудач|долб[оа]е?б|[её]бан|[её]бал|[её]бат|[её]буч|[её]бну|[её]бл[аоияу]|[её]бис|[её]баш|[её]бет|[её]беш|[её]быр|(?:^|за|на|вы|въ|отъ|подъ|съ|разъ|до|про|при|пере|по|у)[её]б(?!е)|говн|гавн|жоп|срак|засран|обосра|ссыкл|дерьм|минет|отсос|сосат|соси(?!с)|пенис|писюн|письк|сиськ|сисяр|трах(?!т)|секс(?!т)|порн|анал(?!и|ог|оги)|оргазм|вагин|дроч|дебил|идиот|дурак|придур|кретин|имбецил|олигофрен|дегенерат|тупиц|тупорыл|урод|ублюд|выродок|мраз|тварь|скотин|сволоч|падл|гнид|шмар|быдл|чмо|чушпан|лошар|лошок|лошпед|нигер|черномаз|пиндос|хохол|хохл|кацап|москал/;
/* только целым словом или его началом: у этих корней слишком много честных совпадений внутри имён */
/* (прозвища для национальностей и «козёл» — только в этих формах: Жидков, Хачатурян, Чуркин, Козлов, Дауни — честные фамилии) */
var NKW=/^(?:бля|сук[аиуеой]?$|сучк|сучар|сучок|лох$|хер$|херн|херов|херас|дура$|член$|манда$|тупой$|тупая$|тупые$|кончи|[её]б|жид(?!к)|негр(?:$|ы|а$|у$|ов$|ит|ил)|хач(?:$|и$|ик|ей$|у$|а$)|чурк(?:а|и|е|у|ой)?$|коз[её]л$|козл(?:ы|а|у|ом|ина|ище)$|даун(?:$|ы|а$|у$|ом|[её]н|иц))/;
var NKE=/fuck|fuk|fck|shit|bitch|cunt|dick|cock|puss|ashole|bastard|whore|slut|nig+[ae]|fag+ot|retard|porn|sex|penis|vagin|boob|tits|dildo|wank|twat|moron|idiot|stupid|dumb|loser|huy|hui|huj|xyu|xyi|xuy|xui|pizd|pezd|blyad|blyat|bljad|bljat|eban|ebal|ebat|eblan|yeban|suka|suki|pidor|pidar|pidr|mudak|zalup|gandon|gondon|shly?uh|dolbo|dolba|debil|durak|chmo|lokh|govno|gavno|zhop|jopa|ueban|uebok|nahu[iyj]/;
function nkBad(s){
  var low=String(s||'').toLowerCase().replace(/ё/g,'е').replace(/(.)\1+/g,'$1');
  if(NKE.test(low.replace(/[^a-z]/g,'')))return true;
  var tk=low.split(/[^a-zа-я0-9@]+/).filter(Boolean).map(function(t){
    /* в слове есть кириллица: латиницу и цифры читаем как похожие русские буквы (xуй, пи3да) */
    return /[а-я]/.test(t)?t.replace(/[a-z0-9@]/g,function(c){return NKG[c]||c}).replace(/[^а-я]/g,'').replace(/(.)\1+/g,'$1'):t});
  if(tk.some(function(t){return/[а-я]/.test(t)&&(NKA.test(t)||NKW.test(t))}))return true;
  /* буквы, разделённые точками и пробелами: «х у й», «п.и.з.д.а», «С у к а». Склеиваем только если слово и правда
     разбито на буквы (иначе «Сукачёв Ан…» склеилось бы в «сука…»); латиница в таких буквах читается как кириллица */
  var one=tk.filter(function(t){return t.length<=2}).length;
  if(tk.length>=3&&one>=tk.length-1){var j=tk.map(function(t){return t.replace(/[a-z0-9@]/g,function(c){return NKG[c]||c})}).join('').replace(/[^а-я]/g,'').replace(/(.)+/g,'$1');if(NKA.test(j)||NKW.test(j))return true}
  var jj=tk.filter(function(t){return/[а-я]/.test(t)}).join('');
  return /ху[йея]|пизд|пезд|бляд|блят|пид[оа]р|залуп|[её]бан|[её]бал|[её]блан|долб[оа]е?б|мудак|г[ао]ндон|шлюх|уебан|нахуй/.test(jj)}
var NKBAD=0;   /* сколько раз за этот запуск ник оказался неприличным: первый — перезагрузка, второй — «Морковка» */

/* --- звуки вступления. Свой набор (шум, «железо», стекло, гул), а не короткие ноты интерфейса, но идут через общую шину
   a_sound.js: та же громкость, «без звука» и тишина в скрытой вкладке. До первого касания звука нет (поэтому включатель). --- */
var BXG=.25,BXK=0;
function bxC(){if(typeof S==='undefined'||!S||S.mute||document.hidden||!SX.c||SX.dead||SX.c.state!=='running')return null;try{sxVol(VOLK())}catch(e){}return SX.c}
function bxEnv(g,T,a,att,d){g.gain.setValueAtTime(0,T);g.gain.linearRampToValueAtTime(a,T+att);g.gain.exponentialRampToValueAtTime(Math.max(a*.001,1e-5),T+Math.max(att+.002,d));g.gain.linearRampToValueAtTime(0,T+d+.01)}
/* тон: частота f (скольжение до f2), длина d, сила a, форма ty, атака att, срез lp */
function bxT(c,o,t,f,d,a,ty,f2,att,lp){
  var T=c.currentTime+t,s=c.createOscillator(),g=c.createGain();s.type=ty||'sine';s.frequency.setValueAtTime(f,T);if(f2)s.frequency.exponentialRampToValueAtTime(f2,T+d);
  bxEnv(g,T,a,att||.004,d);s.connect(g);
  if(lp){var l=c.createBiquadFilter();l.type='lowpass';l.frequency.value=lp;g.connect(l);l.connect(o)}else g.connect(o);
  s.start(T);s.stop(T+d+.05)}
/* шум через фильтр: тип ty, частота f (до f2), добротность q */
function bxN(c,o,t,d,a,ty,f,f2,q,att){
  var T=c.currentTime+t,s=c.createBufferSource(),fl=c.createBiquadFilter(),g=c.createGain();s.buffer=SX.x.nz;s.loop=true;
  fl.type=ty||'bandpass';fl.frequency.setValueAtTime(f,T);if(f2)fl.frequency.exponentialRampToValueAtTime(f2,T+d);fl.Q.value=q||.8;
  bxEnv(g,T,a,att||.003,d);s.connect(fl);fl.connect(g);g.connect(o);s.start(T,Math.random()*.9);s.stop(T+d+.05)}
function bxR(a,b){return a+Math.random()*(b-a)}
var BX={
  /* включение: глухой удар, треск помех, тонкий писк кинескопа */
  power:function(c,o){bxT(c,o,0,96,.4,.9,'sine',36);bxN(c,o,0,.6,.55,'bandpass',2600,1500,.7);bxN(c,o,.01,.3,.3,'highpass',4200);bxT(c,o,.06,5200,1.1,.02,'sine',5350,.06)},
  /* заставка: неоновое потрескивание в такт мерцанию, низкий удар с подъёмом, тёплый гул, колокольчик к подписи, уход */
  logo:function(c,o){
    [.73,.92,1.14,1.3].forEach(function(t,k){bxT(c,o,t,118,k===2?.11:.06,.16,'sawtooth',0,.003,900);bxN(c,o,t,.06,.1,'bandpass',1900,0,2)});
    bxN(c,o,.45,.95,.22,'lowpass',160,2600,.7,.85);
    bxT(c,o,1.34,64,3,.9,'sine',46,.01);bxT(c,o,1.34,128,2.2,.35,'sine',96,.01);bxN(c,o,1.34,.6,.4,'lowpass',420,120,.7,.004);
    [130.81,196,261.63,392].forEach(function(f,k){bxT(c,o,1.4+k*.08,f,5.2,k<2?.07:.045,'triangle',0,1.3,1500)});
    [[1046.5,.11],[1568,.06],[2093,.03]].forEach(function(p){bxT(c,o,2.6,p[0],2.4,p[1],'sine',0,.004)});
    bxN(c,o,6.7,1.1,.22,'bandpass',2600,260,.9,.5)},
  /* звук разрешили посреди заставки: удар и гул без потрескивания, колокольчик сразу */
  late:function(c,o){bxT(c,o,0,64,2.6,.8,'sine',46,.01);bxT(c,o,0,128,2,.3,'sine',96,.01);
    [130.81,196,261.63,392].forEach(function(f,k){bxT(c,o,.05+k*.08,f,4.2,k<2?.07:.045,'triangle',0,1,1500)});
    [[1046.5,.11],[1568,.06],[2093,.03]].forEach(function(p){bxT(c,o,.4,p[0],2.4,p[1],'sine',0,.004)})},
  out:function(c,o){bxN(c,o,0,.8,.22,'bandpass',2600,260,.9,.12)},
  /* печать: сухой щелчок клавиши; у системных строк тише */
  key:function(c,o,a){bxN(c,o,0,.012,a?.06:.15,'highpass',3600);bxT(c,o,0,bxR(1900,2400),.012,a?.02:.045)},
  /* кролик заговорил: два коротких «бипа» старого компьютера */
  beep:function(c,o){bxT(c,o,0,880,.07,.07,'square',0,.003,2400);bxT(c,o,.085,1318.5,.06,.06,'square',0,.003,2400)},
  mv:function(c,o){bxT(c,o,0,1400,.025,.05,'square',0,.002,3000)},
  ok:function(c,o){bxT(c,o,0,659.3,.07,.08,'square',0,.003,2600);bxT(c,o,.075,987.8,.1,.08,'square',0,.003,2600)},
  prog:function(c,o,a){bxT(c,o,0,440+(a||0)*25,.025,.04,'square',0,.002,2200)},
  fatal:function(c,o){bxT(c,o,0,110,.55,.2,'sawtooth',0,.004,1400);bxT(c,o,0,116.5,.55,.2,'sawtooth',0,.004,1400);bxN(c,o,0,.5,.12,'bandpass',900,0,1.2)},
  /* сбой: рваные всплески шума и цифровое заикание, в конце экран схлопывается со свистом вниз */
  glitch:function(c,o){
    for(var k=0;k<11;k++){var t=k*.055+bxR(0,.02);bxN(c,o,t,bxR(.03,.07),bxR(.2,.4),'bandpass',bxR(400,5000),0,bxR(.8,3));if(k%2)bxT(c,o,t,bxR(200,2200),.03,.06,'square',0,.002,3500)}
    bxT(c,o,.5,2600,.45,.28,'sine',55,.004);bxN(c,o,.92,.25,.35,'lowpass',320,90,.7)},
  /* синий экран: щелчок реле и низкий гудок */
  bsod:function(c,o){bxN(c,o,0,.05,.45,'lowpass',900,0,.7,.001);bxT(c,o,.02,98,.9,.45,'sine',0,.006);bxT(c,o,.02,196,.7,.18,'sine',0,.006)},
  /* удар по стеклу: хлопок, низкий «бум», звон и россыпь мелких тресков */
  impact:function(c,o){
    bxN(c,o,0,.06,.95,'highpass',1300,0,.7,.001);bxT(c,o,0,72,.5,.85,'sine',38,.002);bxN(c,o,0,.7,.22,'bandpass',3200,2400,6);
    for(var k=0;k<16;k++)bxN(c,o,bxR(.04,.85),bxR(.006,.014),bxR(.25,.6),'bandpass',bxR(2500,6000),0,3,.001)},
  /* осыпание: шорох крошки и сотни мелких «дзыньков», больше в начале */
  shatter:function(c,o){
    bxN(c,o,0,.7,.45,'bandpass',3600,2200,.9,.006);bxN(c,o,.1,1.6,.12,'highpass',5000,0,.7,.3);
    for(var k=0;k<46;k++){var t=Math.pow(Math.random(),1.7)*2.4,hi=Math.random()<.75;bxT(c,o,t,hi?bxR(2200,5600):bxR(900,2000),bxR(.06,.32),bxR(.05,.17),'sine',0,.002)}}
};
/* играть звук; вернуть его выход (чтобы оборвать, если заставку пропустили) */
function bx(n,a){var c=bxC();if(!c||!BX[n])return null;
  if(n==='key'){var t=performance.now();if(t-BXK<34)return null;BXK=t}
  /* SX.la: общий звук касания кнопки (a_sound.js) не накладывается на этот */
  try{SX.la=performance.now();var o=c.createGain();o.gain.value=BXG;o.connect(SX.x.bus);BX[n](c,o,a);return o}catch(e){return null}}
function bxStop(o){if(!o||!SX.c)return;try{o.gain.setTargetAtTime(0,SX.c.currentTime,.06)}catch(e){}}
/* шипение плёнки: очень тихое, пока виден VHS-экран */
function bxHiss(){var c=bxC();if(!c)return null;
  try{var s=c.createBufferSource(),f=c.createBiquadFilter(),g=c.createGain();s.buffer=SX.x.nz;s.loop=true;f.type='bandpass';f.frequency.value=3000;f.Q.value=.5;
    g.gain.setValueAtTime(0,c.currentTime);g.gain.linearRampToValueAtTime(.012,c.currentTime+1.5);s.connect(f);f.connect(g);g.connect(SX.x.bus);s.start();
    return function(){try{g.gain.setTargetAtTime(0,c.currentTime,.1);s.stop(c.currentTime+.6)}catch(e){}}}catch(e){return null}}
/* браузер включает звук не сразу после касания: ждём (не дольше 350 мс) */
function bxReady(cb){var d=0;function go(){if(!d){d=1;cb()}}
  try{if(typeof sxEnsure==='function')sxEnsure();if(!SX.c||SX.c.state==='running')return go();SX.c.resume().then(go,go)}catch(e){go()}setTimeout(go,350)}

/* --- картинка кролика: контур (для терминала) и карта «контур / заливка / пусто» (для растра заставки) --- */
function rbLoad(cb){
  if(RBIMG)return cb(RBIMG);
  var cs=getComputedStyle(document.documentElement);
  function src(v){var m=/url\(["']?([^"')]+)/.exec(cs.getPropertyValue(v));return m?m[1]:''}
  var a=new Image(),b=new Image(),n=0,so=src('--pi-o'),sf=src('--pi-f');
  if(!so)return cb(null);
  function one(){if(++n<2)return;try{
    var w=a.naturalWidth,h=a.naturalHeight,c=document.createElement('canvas');c.width=w;c.height=h;
    var x=c.getContext('2d');x.drawImage(a,0,0);var d=x.getImageData(0,0,w,h).data;
    x.clearRect(0,0,w,h);if(b.naturalWidth)x.drawImage(b,0,0,w,h);var f=x.getImageData(0,0,w,h).data;
    var o=x.createImageData(w,h),v=new Float32Array(w*h);
    for(var i=0;i<w*h;i++){
      var al=d[i*4+3]/255,l=(d[i*4]+d[i*4+1]+d[i*4+2])/765,ln=Math.min(1,al*(1-l)*1.4);
      o.data[i*4+3]=Math.round(255*ln);
      /* 1 — линия, .5 — внутри кролика (заливка профиля или белое внутри контура), 0 — снаружи */
      v[i]=ln>.5?1:(f[i*4+3]>128||(al>.5&&l>.5))?.5:0}
    x.putImageData(o,0,0);RBIMG={ol:c.toDataURL(),v:v,w:w,h:h}}catch(e){RBIMG=null}cb(RBIMG)}
  a.onload=a.onerror=one;b.onload=b.onerror=one;a.src=so;if(sf)b.src=sf;else one()}

/* растр как на старом люминофоре: линии — крупные точки, тело — мелкие и неровные, вокруг редкая пыль */
function rbHalftone(cv){
  var R=RBIMG;if(!R||!cv.isConnected)return;
  var dpr=Math.min(2,window.devicePixelRatio||1),W=cv.clientWidth||220,H=W*R.h/R.w,N=44,st=W/N,x=cv.getContext('2d');
  cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);x.scale(dpr,dpr);x.fillStyle='#ffb347';
  for(var gy=0;gy<H/st;gy++)for(var gx=0;gx<N;gx++){
    var x0=Math.floor(gx*st/W*R.w),x1=Math.floor((gx+1)*st/W*R.w),y0=Math.floor(gy*st/H*R.h),y1=Math.min(R.h,Math.floor((gy+1)*st/H*R.h)),s=0,c=0,ol=0;
    for(var yy=y0;yy<y1;yy++)for(var xx=x0;xx<x1;xx++){var q=R.v[yy*R.w+xx];s+=q;c++;if(q===1)ol++}
    if(!c)continue;var val=s/c,cx=(gx+.5)*st,cy=(gy+.5)*st;
    if(ol/c>.25)val=.75+.25*ol/c;
    else if(val>.2)val=.16+.3*(.5+.25*Math.sin(gx*.55+gy*.21)+.25*Math.sin(gx*.13-gy*.47)+(Math.random()-.5)*.5);
    else if(Math.random()<.035)val=.05+Math.random()*.08;else continue;
    if(val<=0)continue;
    x.globalAlpha=Math.min(1,.35+val);x.beginPath();x.arc(cx,cy,st*.52*Math.sqrt(Math.min(1,val)),0,6.2832);x.fill()}}

/* --- дождь символов за текстом терминала: еле заметный, 20 кадров в секунду --- */
function rainStart(cv){
  if(RM())return null;
  var x=cv.getContext('2d'),R={on:1,raf:0,last:0,cols:[]},fs=14,dpr=1,W=0,H=0;
  function rc(){return CRTG[Math.floor(Math.random()*CRTG.length)]}
  function col(init){var n=8+Math.floor(Math.random()*18),ch=[];for(var k=0;k<n;k++)ch.push(rc());
    return{y:init?Math.random()*(H/fs+n)-n:-Math.random()*30,sp:.12+Math.random()*.32,n:n,ch:ch,a:.04+Math.random()*.07}}
  function fit(){dpr=Math.min(2,window.devicePixelRatio||1);W=cv.clientWidth;H=cv.clientHeight;cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);
    fs=W<600?13:15;R.cols=[];for(var i=0,m=Math.ceil(W/fs);i<m;i++)R.cols.push(col(true))}
  function fr(t){
    if(!R.on)return;R.raf=requestAnimationFrame(fr);if(t-R.last<50)return;R.last=t;
    x.setTransform(dpr,0,0,dpr,0,0);x.clearRect(0,0,W,H);x.font=fs+'px '+getComputedStyle(cv).fontFamily;x.textBaseline='top';
    for(var i=0;i<R.cols.length;i++){var c=R.cols[i];c.y+=c.sp;if(Math.random()<.05)c.ch[Math.floor(Math.random()*c.n)]=rc();
      var hy=Math.floor(c.y);if((hy-c.n)*fs>H){R.cols[i]=col(false);continue}
      for(var k=0;k<c.n;k++){var yy=hy-k;if(yy<0||yy*fs>H)continue;
        x.fillStyle='rgba(120,255,160,'+(k?c.a*(1-k/c.n):Math.min(.3,c.a*2.8)).toFixed(3)+')';x.fillText(c.ch[yy%c.n],i*fs,yy*fs)}}}
  fit();R.fit=fit;window.addEventListener('resize',fit);R.raf=requestAnimationFrame(fr);
  R.stop=function(){R.on=0;cancelAnimationFrame(R.raf);window.removeEventListener('resize',fit)};
  return R}

/* --- плёнка, без перебора: слабое мелкое зерно (небольшой canvas, растянутый на экран) и редкое лёгкое подёргивание кадра --- */
function vhsStart(o){
  var cv=o.querySelector('.grn'),sci=o.querySelector('.sci'),x=cv.getContext('2d'),W=0,H=0,im=null,V={on:1,raf:0,last:0,jt:0};
  /* размер зерна — по пропорциям экрана: точки квадратные (~4 px), а не вытянутые полосы на высоком экране телефона */
  function fit(){var s=Math.max(3,Math.round(Math.max(innerWidth,innerHeight)/320));W=Math.ceil(innerWidth/s);H=Math.ceil(innerHeight/s);cv.width=W;cv.height=H;im=x.createImageData(W,H)}
  fit();window.addEventListener('resize',fit);
  function grain(){for(var i=0;i<W*H;i++){var g=Math.random()*255|0;im.data[i*4]=im.data[i*4+1]=im.data[i*4+2]=g;im.data[i*4+3]=255}x.putImageData(im,0,0)}
  grain();
  if(!RM()){(function fr(t){if(!V.on)return;V.raf=requestAnimationFrame(fr);if(t-V.last<80)return;V.last=t;grain()})(0);
    (function jit(){V.jt=setTimeout(function(){if(!V.on)return;sci.classList.add('jt');setTimeout(function(){sci.classList.remove('jt')},80+Math.random()*60);jit()},7000+Math.random()*8000)})()}
  V.stop=function(){V.on=0;cancelAnimationFrame(V.raf);clearTimeout(V.jt);window.removeEventListener('resize',fit)};
  return V}

/* --- экран --- */
function crtT(f,ms){var t=setTimeout(f,ms);if(CRT)CRT.tms.push(t);return t}
function crtW(ms){return new Promise(function(r){crtT(r,CRT&&(CRT.fast||CRT.rm)?0:ms)})}
function crtClose(keep){
  if(!CRT)return;var c=CRT;CRT=null;
  c.tms.forEach(clearTimeout);c.off.forEach(function(f){f()});if(c.rain)c.rain.stop();if(c.vhs)c.vhs.stop();if(c.hiss)c.hiss();bxStop(c.lgs);
  c.el.remove();if(!keep)document.documentElement.classList.remove('crt-on')}
/* op.reboot — перезагрузка за неприличный ник: без заставки, сразу BIOS со строкой FAIL */
function crtOpen(op){
  op=op||{};crtClose();
  /* неприличный ник, сохранённый до появления проверки (или в обход неё), не принимаем: спросим заново */
  if(S.nick&&nkBad(S.nick)){S.nick='';save()}var bx0=document.getElementById('shards');if(bx0)bx0.remove();bx0=document.getElementById('bsod');if(bx0)bx0.remove();
  scr('nick','');window.scrollTo(0,0);
  var full=!S.nick&&!op.reboot,rm=RM(),o=document.createElement('div');o.id='crt';o.className='crt on'+(rm?' rm':'');
  o.innerHTML='<div class="sc"><div class="sci"><canvas class="rain" aria-hidden="true"></canvas>'
    +(full?'<div class="spl" aria-hidden="true"><canvas class="lg"></canvas><i class="sg">▮</i><div class="bl">IT&#39;S THE PROGRAMMING</div></div>':'')
    +'<div class="tm" role="log" aria-live="polite" aria-label="Знакомство с ИТП"><div class="tmi"></div></div></div>'
    +'<i class="fx" aria-hidden="true"></i><canvas class="grn" aria-hidden="true"></canvas><i class="trk" aria-hidden="true"></i></div>';
  document.body.appendChild(o);document.documentElement.classList.add('crt-on');
  CRT={el:o,tm:o.querySelector('.tm'),log:o.querySelector('.tmi'),tms:[],off:[],fast:0,rm:rm,rain:null,spl:null,touch:'ontouchstart' in window};
  CRT.vhs=vhsStart(o);
  /* касание или клавиша: пропустить заставку, допечатать текущую реплику */
  function hurry(e){if(!CRT)return;if(CRT.spl){if(e.type!=='keydown'||!(e.ctrlKey||e.metaKey||e.altKey||e.key==='Tab'))CRT.spl();return}
    var t=e.target;if(t&&t.closest&&t.closest('input,button'))return;if(e.type==='keydown'&&(e.ctrlKey||e.metaKey||e.altKey||e.key==='Tab'))return;CRT.fast=1}
  o.addEventListener('pointerdown',hurry);document.addEventListener('keydown',hurry,true);
  CRT.off.push(function(){document.removeEventListener('keydown',hurry,true)});
  rbLoad(function(R){if(!CRT||CRT.el!==o)return;if(R)o.style.setProperty('--rb','url('+R.ol+')');var lg=o.querySelector('.lg');if(lg)rbHalftone(lg)});
  if(op.reboot){bx('power');CRT.hiss=bxHiss();crtDialog(true,1);return}
  if(!full){CRT.hiss=bxHiss();crtDialog(false);return}
  /* звук пробуем включить сразу: браузер разрешает это не всегда (обычно нужен первый жест), тогда заставка начинается тихо */
  try{if(typeof sxEnsure==='function')sxEnsure()}catch(e){}
  bx('power');CRT.hiss=bxHiss();
  crtSplash().then(function(){if(CRT&&CRT.el===o)crtDialog(true)})}

/* заставка (~7 с): кролик разгорается с мерцанием, как неоновая лампа, «дышит», появляется подпись, всё гаснет вспышкой.
   Если звук ещё не разрешён, первое касание не пропускает заставку, а включает звук прямо на ней; пропускает второе */
function crtSplash(){return new Promise(function(res){
  var sp=CRT.el.querySelector('.spl'),ok=0,late=0;sp.classList.add('on');CRT.lgs=bx('logo');
  function go(e){if(ok||!CRT)return;ok=1;CRT.spl=null;if(e||late){bxStop(CRT.lgs);bx('out')}sp.classList.add('out');crtT(function(){sp.remove();res()},CRT.rm?0:900)}
  CRT.spl=function(){
    if(!CRT.lgs&&!late&&!S.mute){late=1;bxReady(function(){if(!CRT||ok)return;CRT.lgs=bx('late');if(!CRT.hiss)CRT.hiss=bxHiss()});return}
    go(1)};
  crtT(function(){go(0)},CRT.rm?2600:6800)})}

function crtScroll(el){var t=CRT&&CRT.tm;if(!t)return;
  if(el&&el.offsetHeight>t.clientHeight*.6)t.scrollTop=Math.max(0,el.offsetTop-t.clientHeight*.25);else t.scrollTop=t.scrollHeight}
function crtRow(h,cls,tag){var e=document.createElement(tag||'div');e.className=cls;e.innerHTML=h;CRT.log.appendChild(e);crtScroll(e);return e}
/* печать по буквам со щелчками клавиш; на точках и запятых пауза */
function crtType(el,s,ms,soft){return new Promise(function(res){
  if(!CRT)return;if(CRT.rm){el.textContent=s;crtScroll();return res()}
  var i=0;el.classList.add('typ');
  (function st(){if(!CRT)return;i=CRT.fast?s.length:i+1;el.textContent=s.slice(0,i);crtScroll();
    if(i>=s.length){el.classList.remove('typ');return res()}
    var c=s[i-1];if(c!==' ')bx('key',soft);crtT(st,(ms||28)*(/[.?!]/.test(c)?8:c===','?4:1)*(.6+Math.random()*.8))})()})}
/* служебные строки; строка-массив [текст,'err'] печатается красным */
function crtSys(lines){var p=Promise.resolve();
  lines.forEach(function(s){p=p.then(function(){if(!CRT)return;var er=Array.isArray(s),e=crtRow('','tl '+(er?'err':'sys'));if(er)bx('fatal');return crtType(e,er?s[0]:s,7,1).then(function(){return crtW(er?600:110)})})});
  return p}
/* реплика кролика; bad — кролик сердится: красный, с гудком вместо «бипа» */
function crtSay(lines,bad){
  var r=crtRow('<i class="rb" aria-hidden="true"></i><span class="ds" aria-hidden="true">—</span><div class="tx"></div>','tr'+(bad?' bad':'')),tx=r.querySelector('.tx'),p=crtW(260);bx(bad?'fatal':'beep');
  lines.forEach(function(s,k){p=p.then(function(){if(!CRT)return;var e=document.createElement('p');tx.appendChild(e);return crtType(e,s).then(function(){return crtW(k<lines.length-1?380:220)})})});
  return p.then(function(){if(CRT)CRT.fast=0})}
function crtYou(s){if(!CRT)return;var e=crtRow('','tl you');e.textContent=s}

/* поле ввода: рамка, «…» и мигающий блок-курсор; само поле настоящее (клавиатура телефона, вставка) */
function crtAsk(max){return new Promise(function(res){
  var f=crtRow('<label class="tbx"><span class="sr-only">Как тебя зовут?</span><span class="tvw" aria-hidden="true"><span class="tv"></span></span><span class="ph" aria-hidden="true">…</span><i class="cu" aria-hidden="true"></i><input id="nk" maxlength="'+max+'" autocomplete="off" autocapitalize="words" autocorrect="off" spellcheck="false" enterkeyhint="done"></label><button class="tgo" id="go" type="submit" disabled aria-label="Дальше">'+ico('enter')+'</button>','tin','form');
  var i=f.querySelector('input'),tv=f.querySelector('.tv'),g=f.querySelector('#go');
  f.setAttribute('autocomplete','off');
  i.oninput=function(){tv.textContent=i.value;f.classList.toggle('has',!!i.value);g.disabled=!i.value.trim();bx('key')};
  f.onsubmit=function(e){e.preventDefault();var v=i.value.trim();if(!v){i.focus();return}bx('ok');i.blur();f.remove();crtYou('> '+v);res(v.slice(0,max))};
  if(!CRT.touch)setTimeout(function(){i.focus({preventScroll:true})},60)})}

/* меню: стрелки, цифры (если пунктов меньше десяти), Enter или касание */
function crtMenu(items,lab){return new Promise(function(res){
  var m=crtRow(items.map(function(it,k){return'<button type="button" class="tmo'+(it.c?' '+it.c:'')+'"'+(it.a||'')+' data-k="'+k+'"><span class="mk" aria-hidden="true">▸</span>'+it.h+'</button>'}).join(''),'tmn');
  m.setAttribute('role','group');m.setAttribute('aria-label',lab);
  var bs=[].slice.call(m.querySelectorAll('button')),sel=0,done=0;
  function hi(n,q){var p=sel;sel=(n+bs.length)%bs.length;bs.forEach(function(b,k){b.classList.toggle('hi',k===sel)});if(!q&&p!==sel)bx('mv')}
  function pick(k){if(done)return;done=1;bx('ok');bs.forEach(function(b){b.disabled=true});bs[k].classList.add('pk');crtT(function(){res(k)},CRT.rm?0:280)}
  function kd(e){if(done||!CRT||e.ctrlKey||e.metaKey||e.altKey)return;
    if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();hi(sel+(e.key==='ArrowDown'?1:-1));bs[sel].focus();bs[sel].scrollIntoView({block:'nearest'})}
    else if(bs.length<10&&/^[1-9]$/.test(e.key)&&+e.key<=bs.length){e.preventDefault();pick(+e.key-1)}}
  bs.forEach(function(b,k){b.onclick=function(){pick(k)};b.onfocus=b.onpointerenter=function(){if(!done)hi(k)}});
  document.addEventListener('keydown',kd,true);CRT.off.push(function(){document.removeEventListener('keydown',kd,true)});
  hi(0,1);if(!CRT.touch)bs[0].focus({preventScroll:true})})}

/* --- ник: спросить; неприличный в первый раз — перезагрузка, во второй — кролик сам называет ученика Морковкой.
   Неприличный ник нигде не сохраняется; промис перезагрузки не разрешается, поэтому прежний разговор дальше не идёт --- */
function crtName(){return crtAsk(20).then(function(v){
  v=nkClean(v);if(!nkBad(v))return v;
  if(++NKBAD<2)return crtSay(['Ну всё. Перезагружаю.'],1).then(function(){if(!CRT)return;CRT.el.classList.add('gl','snow');bx('glitch');crtT(function(){crtClose(1);crtOpen({reboot:1})},1050);return new Promise(function(){})});
  return crtSay(['Всё, решено: будешь Морковкой.','Поменять ник можно в настройках.'],1).then(function(){return'Морковка'})})}

/* --- разговор --- */
function crtDialog(full,reboot){
  CRT.el.classList.add('live');CRT.rain=rainStart(CRT.el.querySelector('.rain'));
  var bios=['ITP BIOS v'+ITPV,'(c) It\'s The Programming','Проверка памяти ......... 640K OK','Интерпретатор Python .... найден'];
  if(reboot)bios.push(['Проверка воспитанности .. FAIL']);
  bios.push('Кролик .................. на связи');
  var p=full?crtSys(bios):Promise.resolve(),NK='';
  /* ник и обращение сохраняются вместе, после ответа про обращение: иначе, уйдя со страницы между вопросами (приложение
     сохраняет прогресс при уходе), ученик возвращался «с ником», и вопрос про обращение пропускался */
  if(!S.nick)p=p.then(function(){return crtSay(reboot?['Привет ещё раз.','Как я могу к тебе обращаться? Только нормально.']:['Привет.','Как я могу к тебе обращаться?'])}).then(crtName).then(function(v){
    NK=v;return crtSay((v==='Морковка'&&NKBAD>1?[]:['Приятно познакомиться, '+v+'.']).concat(['Ты парень или девушка? Это нужно, чтобы окончания в тексте были правильными.']))}).then(function(){
    return crtMenu([['m','Парень'],['f','Девушка'],['','Не указывать']].map(function(x,k){return{c:'tgd',a:' data-g="'+x[0]+'"',h:'<span class="tno">['+(k+1)+']</span>'+x[1]}}),'Как к тебе обращаться')}).then(function(k){
    S.nick=NK;S.g=['m','f',''][k];if(!S.reg)S.reg=day(new Date());save();crtYou('> '+['Парень','Девушка','Не указывать'][k])});
  else p=p.then(function(){return crtSay(['С возвращением, '+S.nick+'.'])});
  p.then(function(){if(CRT)return crtSay(['С чего начнём?','Выбери первую тему, которую ещё не знаешь. Пропущенные можно пройти потом.'])}).then(function(){
    if(!CRT)return;
    var f=TOPICS[0]&&TOPICS[0].intro?1:0,ix=[],n=0;
    var it=[];TOPICS.forEach(function(t,i){if(t.intro||t.opt)return;n++;ix.push(i);var z=i===f;
      it.push({c:'tpc'+(z?' rec':''),a:' data-i="'+i+'"',h:'<span class="tno">'+(n<10?'0':'')+n+'</span><span class="ct">'+(z?'С нуля: ':'')+esc(t.n)+'<small>'+esc(t.s||'')+'</small></span>'})});
    return crtMenu(it,'Первая тема').then(function(k){var i=ix[k];S.start=i===f?0:i;save();crtYou('> '+TOPICS[i].n);return crtLaunch()})})}

/* «загрузка» с полоской, потом сбой */
function crtLaunch(){
  var e=crtRow('','tl sys'),n=0;
  return new Promise(function(res){(function st(){if(!CRT)return;
    e.textContent='Запуск ИТП ['+'#'.repeat(n)+'.'.repeat(20-n)+'] '+n*5+'%';crtScroll();bx('prog',n);
    if(n>=20)return crtT(res,CRT.rm?0:420);n=Math.min(20,n+1+Math.floor(Math.random()*3));crtT(st,CRT.rm?0:80+Math.random()*110)})()}).then(function(){
    if(!CRT)return;var w=crtRow('','tl err');w.textContent='FATAL 0x0000C0DE: вступление закончилось';bx('fatal');return crtW(900)}).then(crtCrash)}

/* --- сбой: помехи → экран гаснет в точку → чёрный экран → синий экран ~7 с → трещины → осколки, под ними Путь --- */
function crtCrash(){
  if(!CRT)return;
  fzApply();S.seen=day(new Date());save();
  home();window.scrollTo(0,0);
  if(CRT.rm){var c=CRT.el;c.classList.add('fade');crtT(function(){crtClose()},450);return}
  CRT.el.classList.add('gl','snow');bx('glitch');
  crtT(function(){crtClose(1);bsod()},1050)}

/* пасхалка: настоящий QR-код с текстом «Привет из ИТП!» (UTF-8 с пометкой ECI, версия 2, 25×25, коррекция M). Сетка посчитана заранее
   библиотекой segno (кодировка задана явно: без этого она выбирает Shift_JIS) и записана построчно: каждое число — строка из 25 клеток, старший бит слева, 1 — тёмная клетка.
   Рисуется тёмным по белому квадрату с полем в 2 клетки, как на синем экране Windows: так его читают камеры телефонов */
var BSQR=[33348991,17103425,24417373,24396893,24397917,17134913,33379711,49408,19780512,8041198,30718345,33168294,32999258,9022336,22458798,12289112,30903801,96028,33334103,17131295,24400374,24502820,24397289,17046731,33390023];
function bsQr(){
  var d='',N=25;
  for(var y=0;y<N;y++)for(var x=0;x<N;x++)if((BSQR[y]>>(N-1-x))&1)d+='M'+x+' '+y+'h1v1h-1z';
  return'<svg viewBox="-2 -2 29 29" shape-rendering="crispEdges" aria-hidden="true" focusable="false"><rect x="-2" y="-2" width="29" height="29" fill="#fff"/><path fill="#0b63ce" d="'+d+'"/></svg>'}
function bsod(){
  var b=document.createElement('div'),tms=[],gone=0,nm=S.nick||'';b.id='bsod';b.className='blk';b.setAttribute('role','alert');
  b.innerHTML='<div class="bsv"><div class="bsi"><div class="sad" aria-hidden="true">:(</div><p class="bm">В ИТП возникла проблема, и его нужно перезапустить. Мы лишь подготовим островки'+(nm?', '+esc(nm)+',':'')+' и всё заработает.</p><p class="bp"><b>0</b>% выполнено</p><div class="bq">'+bsQr()+'<div><p>Это не настоящая ошибка, а начало курса.</p><p>Код остановки: HELLO_WORLD</p></div></div></div></div>';
  document.body.appendChild(b);
  function T(f,ms){tms.push(setTimeout(f,ms))}
  /* касание — сразу к Пути */
  function end(){if(gone)return;gone=1;tms.forEach(clearTimeout);b.remove();var x=document.getElementById('shards');if(x)x.remove();document.documentElement.classList.remove('crt-on')}
  b.onclick=end;
  /* 1,4 с темноты (в центре гаснет точка кинескопа), потом синий экран; проценты ползут неровно ~6,5 с */
  var pc=b.querySelector('.bp b'),steps=[0,0,2,5,5,9,14,14,20,27,33,33,41,48,55,55,62,70,76,83,88,88,94,100],B=1400,ST=270;
  T(function(){b.classList.remove('blk');bx('bsod')},B);
  steps.forEach(function(v,k){T(function(){pc.textContent=v},B+ST*k)});
  T(function(){bsCrack(b,T,end)},B+ST*steps.length+700)}

/* разбиение экрана на осколки как у настоящего стекла: ячейки Вороного вокруг случайных точек, у места удара точки гуще
   (там мелкая крошка), к краям реже (крупные куски). Каждая ячейка — пересечение полуплоскостей «ближе к своей точке» */
function bsClip(pl,nx,ny,c){var o=[];for(var i=0;i<pl.length;i++){var a=pl[i],b=pl[(i+1)%pl.length],da=nx*a[0]+ny*a[1]-c,db=nx*b[0]+ny*b[1]-c;
  if(da<=0)o.push(a);if((da<0&&db>0)||(da>0&&db<0)){var t=da/(da-db);o.push([a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t])}}return o}
function bsCells(w,h,cx,cy){
  /* большинство точек лежит вдоль неровных лучей от удара: осколки вытягиваются к краям, как у разбитого экрана */
  var D=Math.hypot(w,h),n=w<600?36:56,pts=[[cx,cy]],k=0,R=[],nr=7+Math.floor(Math.random()*4),i;
  for(i=0;i<nr;i++)R.push((i+(Math.random()-.5)*.7)/nr*6.2832);
  while(pts.length<n&&k++<4000){var r=D*.6*Math.pow(Math.random(),1.6),a=Math.random()<.72?R[Math.floor(Math.random()*nr)]+(Math.random()-.5)*(.5/nr)*6.2832*Math.min(1,40/(r+1)+.25):Math.random()*6.2832,x=cx+Math.cos(a)*r,y=cy+Math.sin(a)*r;
    if(x<2||y<2||x>w-2||y>h-2)continue;
    if(pts.some(function(p){return Math.hypot(p[0]-x,p[1]-y)<10+r*.16}))continue;
    pts.push([x,y])}
  return pts.map(function(p,i){var pl=[[0,0],[w,0],[w,h],[0,h]];
    pts.forEach(function(q,j){if(i===j||pl.length<3)return;var nx=q[0]-p[0],ny=q[1]-p[1];pl=bsClip(pl,nx,ny,(nx*(p[0]+q[0])+ny*(p[1]+q[1]))/2)});
    return pl}).filter(function(pl){return pl.length>2})}

/* удар в три приёма, как будто по стеклу бьют несколько раз: звёздочка у места удара → трещины до середины → до краёв.
   Каждый удар — со звуком и встряской; внутри этапа трещины прорисовываются по очереди от центра (WAAPI, а не CSS:
   до своей очереди каждая трещина гарантированно скрыта, и вся сетка не вспыхивает разом) */
function bsCrack(b,T,end){
  var w=innerWidth,h=innerHeight,cx=w*(.44+Math.random()*.12),cy=h*(.4+Math.random()*.1),D=Math.hypot(w,h),cells=bsCells(w,h,cx,cy),seen={},ed=[],e=.5;
  function bd(a,b2){return(Math.abs(a[0])<e&&Math.abs(b2[0])<e)||(Math.abs(a[0]-w)<e&&Math.abs(b2[0]-w)<e)||(Math.abs(a[1])<e&&Math.abs(b2[1])<e)||(Math.abs(a[1]-h)<e&&Math.abs(b2[1]-h)<e)}
  cells.forEach(function(pl){for(var i=0;i<pl.length;i++){var a=pl[i],c=pl[(i+1)%pl.length];if(bd(a,c))continue;
    var ka=Math.round(a[0])+','+Math.round(a[1]),kc=Math.round(c[0])+','+Math.round(c[1]),key=ka<kc?ka+'|'+kc:kc+'|'+ka;if(seen[key])continue;seen[key]=1;
    var d0=Math.hypot(a[0]-cx,a[1]-cy),d1=Math.hypot(c[0]-cx,c[1]-cy);if(d1<d0){var t=a;a=c;c=t;t=d0;d0=d1;d1=t}
    ed.push({a:a,c:c,d:d0/D,L:Math.ceil(Math.hypot(c[0]-a[0],c[1]-a[1]))})}});
  var ST=[[0,.09,0],[.09,.26,1150],[.26,9,2300]],sv='';
  ed.forEach(function(q,k){var p=' d="M'+q.a[0].toFixed(1)+' '+q.a[1].toFixed(1)+'L'+q.c[0].toFixed(1)+' '+q.c[1].toFixed(1)+'" data-k="'+k+'" style="stroke-dasharray:'+q.L+';stroke-dashoffset:'+q.L+'"/>';sv+='<path class="cu2"'+p+'<path class="cl"'+p});
  var bv=b.querySelector('.bsv');
  bv.insertAdjacentHTML('beforeend','<svg class="ck" viewBox="0 0 '+w+' '+h+'" preserveAspectRatio="none" aria-hidden="true">'+sv+'</svg>');
  var svg=bv.querySelector('.ck'),ps=svg.querySelectorAll('path');
  [].forEach.call(ps,function(pe){var q=ed[+pe.getAttribute('data-k')],sg=ST[q.d<ST[0][1]?0:q.d<ST[1][1]?1:2],span=Math.min(sg[1],.6)-sg[0];
    pe.animate([{strokeDashoffset:q.L},{strokeDashoffset:0}],{duration:90+q.L*1.4,delay:sg[2]+70+Math.max(0,q.d-sg[0])/span*650+Math.random()*90,easing:'ease-out',fill:'both'})});
  ST.forEach(function(sg,k){T(function(){
    var fl=document.createElementNS('http://www.w3.org/2000/svg','circle');fl.setAttribute('class','imp');fl.setAttribute('cx',cx.toFixed(1));fl.setAttribute('cy',cy.toFixed(1));fl.setAttribute('r',10+k*4);svg.insertBefore(fl,svg.firstChild);
    bx('impact');bv.animate([{transform:'translate('+(-4-k*2)+'px,'+(2+k)+'px)'},{transform:'translate('+(3+k*2)+'px,'+(-2-k)+'px)'},{transform:'none'}],{duration:220+k*40,easing:'steps(3)'})},sg[2])});
  T(function(){bsShatter(b,cells,cx,cy,w,h,D,T,end)},ST[2][2]+1700)}

/* осыпание: стекло вываливается из рамки на зрителя. Кусок чуть проседает, отклоняется вперёд вокруг своего верхнего края
   (низ идёт к зрителю, кусок немного растёт) и падает вниз с ускорением; куски срываются почти одновременно с небольшим
   разбросом, нижние и ближние к удару — раньше. Ничего не тает: каждый кусок уходит за нижний край */
function bsShatter(b,cells,cx,cy,w,h,D,T,end){
  var v=b.querySelector('.bsv'),box=document.createElement('div'),last=0,G=4200,an=[];box.id='shards';box.onclick=end;
  cells.forEach(function(pl){
    var xs=pl.map(function(p){return p[0]}),ys=pl.map(function(p){return p[1]});
    var x0=Math.max(0,Math.floor(Math.min.apply(0,xs))),y0=Math.max(0,Math.floor(Math.min.apply(0,ys))),x1=Math.min(w,Math.ceil(Math.max.apply(0,xs))),y1=Math.min(h,Math.ceil(Math.max.apply(0,ys)));
    if(x1-x0<2||y1-y0<2)return;
    var d=document.createElement('div'),inn=document.createElement('div'),pp=pl.map(function(p){return(p[0]-x0).toFixed(1)+' '+(p[1]-y0).toFixed(1)});
    d.className='shd';inn.className='shi';
    d.style.cssText='left:'+x0+'px;top:'+y0+'px;width:'+(x1-x0)+'px;height:'+(y1-y0)+'px;clip-path:polygon('+pp.map(function(q){return q.replace(' ','px ')+'px'}).join(',')+')';
    inn.style.cssText='left:'+(-x0)+'px;top:'+(-y0)+'px;width:'+w+'px;height:'+h+'px';
    inn.appendChild(v.cloneNode(true));d.appendChild(inn);
    /* тонкая светлая кромка скола */
    d.insertAdjacentHTML('beforeend','<svg class="she" viewBox="0 0 '+(x1-x0)+' '+(y1-y0)+'" aria-hidden="true"><polygon points="'+pp.join(' ')+'"/></svg>');
    box.appendChild(d);
    var mx=0,my=0;pl.forEach(function(p){mx+=p[0];my+=p[1]});mx=mx/pl.length;my=my/pl.length;
    var ar=(x1-x0)*(y1-y0)/(w*h),ds=Math.hypot(mx-cx,my-cy)/D,sm=Math.max(.25,1-ar*6);
    var dy=h-y0+120,du=Math.round(Math.sqrt(2*dy/G)*1000*(1+Math.random()*.15)),dl=Math.round(Math.random()*420+(1-my/h)*380+ds*260);
    var dx=((mx-cx)/w)*60+(Math.random()-.5)*30,rz=(Math.random()-.5)*30*sm,rx=-(25+Math.random()*45)*sm,tz=60+Math.random()*160,sg=1.5+Math.random()*3,SG=200,tot=SG+du;
    last=Math.max(last,dl+tot);
    d.style.transformOrigin='50% 0';
    /* одна анимация на общих часах: проседание → отклонение вперёд → падение; отстать от расписания она не может */
    an.push(d.animate([{transform:'translate3d(0,0,0) rotateX(0deg) rotateZ(0deg)',easing:'ease-out'},
      {transform:'translate3d(0,'+sg.toFixed(1)+'px,0) rotateX('+(rx*.08).toFixed(1)+'deg) rotateZ('+(rz*.05).toFixed(1)+'deg)',offset:SG/tot,easing:'cubic-bezier(.45,0,.9,.55)'},
      {transform:'translate3d('+(dx*.3).toFixed(1)+'px,'+(dy*.22).toFixed(1)+'px,'+(tz*.6).toFixed(0)+'px) rotateX('+(rx*.75).toFixed(1)+'deg) rotateZ('+(rz*.45).toFixed(1)+'deg)',offset:(SG+du*.45)/tot,easing:'cubic-bezier(.3,0,1,.7)'},
      {transform:'translate3d('+dx.toFixed(1)+'px,'+(dy+sg).toFixed(1)+'px,'+tz.toFixed(0)+'px) rotateX('+rx.toFixed(1)+'deg) rotateZ('+rz.toFixed(1)+'deg)'}],
      {duration:tot,delay:dl,fill:'both'}))});
  document.body.appendChild(box);b.remove();bx('shatter');document.documentElement.classList.remove('crt-on');
  app.animate([{filter:'brightness(.45)'},{filter:'brightness(.45)',offset:.25},{filter:'brightness(1)'}],{duration:Math.min(3000,last),easing:'ease-out'});
  T(function(){snd('level')},Math.min(2200,last*.7));
  /* сцена заканчивается, когда упал последний кусок; таймер — только запасной */
  Promise.all(an.map(function(a){return a.finished})).then(end,end);
  T(end,last+1500)}
