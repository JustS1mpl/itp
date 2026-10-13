/* ===================== ИТП 6.4.2 — звуковой дизайн «тихая клавиатура» =====================
   Ни одного звукового файла, сэмпла или модели: всё синтезируется кодом (Web Audio) в этом модуле.
   Образ: тихая смазанная механическая клавиатура с глушащим корпусом. Короткий круглый «тхок» и совсем мягкий «тик»,
   без резкого щелчка и без дребезга.

   Три «кирпичика», из них собран каждый звук (раздел ENGINE ниже):
     sxThock  — клавишный щелчок: шумовой всплеск 5–15 мс (полоса 1–3 кГц, потом срез) + затухающий «корпус»
                (синус и немного треугольника 150–400 Гц, спад 30–80 мс, лёгкое падение тона);
     sxPluck  — мягкая мелодическая нота (глухая маримба / калимба): синус + тихие обертоны + крошечный «стук молоточка»
                из того же шума, чтобы мелодии были «из того же материала», что и клавиши;
     sxAir    — «воздух»: колоколообразный всплеск шума под 200 мс, еле слышный.
   Все ноты берутся из ОДНОГО строя: до-мажорная пентатоника (до, ре, ми, соль, ля), поэтому любые два звука,
   сыгранные подряд или вместе, не диссонируют.

   КАК ИЗМЕНИТЬ ЗВУК: все звуки лежат в таблице SXD ниже. У записи есть:
     fn  — рецепт (времена в секундах, частоты в герцах), ui — относится ли к «Звукам интерфейса», p — приоритет
     (0 касания, 1 обратная связь, 2 награды: младшие звуки приглушаются старшими), j — разброс высоты (доля, 0,035 = ±3,5 %),
     min — минимальная пауза между такими звуками (мс), dur — сколько секунд голос считается занятым,
     w — доля комнаты (0…1), pk — ЦЕЛЕВОЙ пик в дБ от полной шкалы, lv — поправка уровня в дБ.
   Поправки lv подбирает проверка: python3 tests/sound_wav.py --calibrate (меняет только числа lv). Править рецепт можно
   вручную, потом запустить проверку и страницу sounds-preview.html (она берёт код из этого файла: python3 tests/mk_preview.py).

   Правила: AudioContext создаётся только после первого касания; без Web Audio, при выключенном звуке и до первого
   касания все вызовы тихо ничего не делают. Звуки вызываются из тех же событий, что и анимации, и не зависят от
   содержания тем: новая тема и островок получают их автоматически. */
var SX={c:null,x:null,dead:false,ln:'',lt:0,la:0,lf:0,cs:'',per:{},vol:1,pend:null,hid:false};

/*==== ENGINE:BEGIN (без зависимостей от приложения; sounds-preview.html копирует этот кусок) ====*/
/* ноты строя (до-мажорная пентатоника), Гц */
var SXN_={C3:130.81,D3:146.83,E3:164.81,G3:196,A3:220,C4:261.63,D4:293.66,E4:329.63,G4:392,A4:440,
  C5:523.25,D5:587.33,E5:659.25,G5:783.99,A5:880,C6:1046.5,E6:1318.5,G6:1568};
function sxDb(d){return Math.pow(10,d/20)}
/* громкость 0–100 % → усиление. 70 % — опорная точка, на ней пики таблицы SXD совпадают с заданными (pk) */
function sxGain(v){return v<=0?0:Math.min(1.8,Math.pow(v/70,1.5))}
/* детерминированный ГСЧ для шума и комнаты: звук в проверках и в приложении одинаковый */
function sxRng(s){return function(){s|=0;s=s+0x6D2B79F5|0;var t=Math.imul(s^s>>>15,1|s);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
var SXHANN=(function(){var a=new Float32Array(48);for(var i=0;i<48;i++)a[i]=.5-.5*Math.cos(2*Math.PI*i/47);return a})();

/* общая шина: фильтры → громкость → ограничитель; крошечная комната (70 мс) отдельной веткой */
function sxBuild(c,det){
  var sr=c.sampleRate,R=sxRng(20261013),bus=c.createGain(),hp=c.createBiquadFilter(),lp=c.createBiquadFilter(),mst=c.createGain(),
      lim=c.createWaveShaper(),conv=c.createConvolver(),rl=c.createBiquadFilter();
  hp.type='highpass';hp.frequency.value=70;hp.Q.value=.5;           /* убираем гул, телефон его всё равно не воспроизводит */
  lp.type='lowpass';lp.frequency.value=6000;lp.Q.value=.5;          /* страховка: выше 6 кГц ничего не звучит */
  /* ограничитель пиков: статическая мягкая кривая. До −6 дБ от полной шкалы сигнал не меняется (в штатной работе пики −16 дБ и ниже),
     выше плавно сжимается к потолку −1 дБ, клиппинга нет. DynamicsCompressorNode пробовал и убрал: его усиление зависит от истории
     сигнала (замер: один и тот же звук на 11 дБ тише в первые 100 мс жизни контекста) и он добавляет ~6 мс задержки */
  var cv=new Float32Array(2049);for(var j=0;j<2049;j++){var u=j/1024-1,m=Math.abs(u);cv[j]=m<=.5?u:(u<0?-1:1)*(.5+.5*Math.tanh((m-.5)/.5))}lim.curve=cv;
  var n=Math.round(sr*.07),ir=c.createBuffer(1,n,sr),d=ir.getChannelData(0),p=0;
  for(var i=0;i<n;i++){p=p*.5+(R()*2-1)*.5;d[i]=p*Math.pow(1-i/n,2.5)}d[n-1]=0;
  conv.buffer=ir;rl.type='lowpass';rl.frequency.value=3000;rl.Q.value=.4;
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
/* шумовой всплеск: полоса fc (Q), срез lpf */
function sxNz(v,T,d,amp,fc,q,lpf){
  var c=v.c,s=c.createBufferSource(),bp=c.createBiquadFilter(),lp=c.createBiquadFilter(),g=c.createGain();
  s.buffer=v.x.nz;bp.type='bandpass';bp.frequency.value=fc*v.pit;bp.Q.value=q||.9;lp.type='lowpass';lp.frequency.value=lpf||3200;lp.Q.value=.5;
  sxEnv(g,T,amp,.0012,d);s.connect(bp);bp.connect(lp);lp.connect(g);g.connect(v.mix);
  sxSrc(v,s,T,T+d+.01,v.x.det?0:Math.random()*.8)}
/* «корпус» клавиши: затухающий синус (+ треугольник) с лёгким падением тона. dull — глухой вариант без щелчка */
function sxBody(v,T,f,d,amp,drop,dull){
  var c=v.c,F=f*v.pit,lp=c.createBiquadFilter(),parts=dull?[['sine',1,1],['sine',2,.5]]:[['sine',1,1],['triangle',1,.3]];
  lp.type='lowpass';lp.frequency.value=dull?Math.max(520,F*3.4):Math.min(1500,F*5);lp.Q.value=.5;lp.connect(v.mix);
  parts.forEach(function(q){
    var o=c.createOscillator(),g=c.createGain();o.type=q[0];
    o.frequency.setValueAtTime(F*q[1]*(1+drop),T);o.frequency.exponentialRampToValueAtTime(F*q[1],T+Math.min(.03,d*.5));
    sxEnv(g,T,amp*q[2],.0015,d);o.connect(g);g.connect(lp);sxSrc(v,o,T,T+d+.01)})}
/* клавишный щелчок. o: f — тон корпуса, d — длина (30–80 мс), amp — сила корпуса, nza — сила шума (0 = без щелчка),
   nzc — центр полосы шума, nzd — длина шума (5–15 мс), drop — падение тона (отрицательное: подъём), dull — глухой */
function sxThock(v,t,o){
  var T=v.t0+t;sxBody(v,T,o.f,o.d||.06,o.amp===undefined?1:o.amp,o.drop===undefined?.07:o.drop,o.dull);
  if(o.nza!==0)sxNz(v,T,o.nzd||.01,o.nza===undefined?.5:o.nza,o.nzc||1900,.9,3200)}
/* мягкая нота: синус + тихие обертоны (2f, 4f — «тонк» маримбы) + стук молоточка. sub — тёплый подтон на октаву ниже */
function sxPluck(v,t,f,d,amp,o){
  o=o||{};var c=v.c,T=v.t0+t,F=f*v.pit,lp=c.createBiquadFilter(),parts=[[1,1,1],[2,.16,.45]];
  if(F<1000)parts.push([4,.07,.22]);if(o.sub)parts.push([.5,o.sub,.9]);
  lp.type='lowpass';lp.frequency.value=Math.min(4200,F*5);lp.Q.value=.4;lp.connect(v.mix);
  parts.forEach(function(q){
    var os=c.createOscillator(),g=c.createGain();os.type='sine';os.frequency.value=F*q[0];
    sxEnv(g,T,amp*q[1],.003,d*q[2]);os.connect(g);g.connect(lp);sxSrc(v,os,T,T+d+.01)});
  sxNz(v,T,.007,amp*.16,1700,.9,2600)}
/* «воздух»: колоколообразный всплеск шума, полоса скользит f0 → f1 */
function sxAir(v,t,d,amp,f0,f1){
  var c=v.c,T=v.t0+t,s=c.createBufferSource(),bp=c.createBiquadFilter(),lp=c.createBiquadFilter(),lp2=c.createBiquadFilter(),g=c.createGain(),cv=new Float32Array(48);
  for(var i=0;i<48;i++)cv[i]=SXHANN[i]*amp;
  s.buffer=v.x.nz;bp.type='bandpass';bp.Q.value=.8;bp.frequency.setValueAtTime(f0,T);bp.frequency.exponentialRampToValueAtTime(f1,T+d);
  lp.type='lowpass';lp.frequency.value=2200;lp.Q.value=.5;lp2.type='lowpass';lp2.frequency.value=2200;lp2.Q.value=.5;g.gain.value=0;g.gain.setValueCurveAtTime(cv,T,d);
  s.connect(bp);bp.connect(lp);lp.connect(lp2);lp2.connect(g);g.connect(v.mix);sxSrc(v,s,T,T+d+.01,v.x.det?0:Math.random()*.8)}

/* ступени «опыта»: тик поднимается по строю до до6 и дальше не растёт (не станет пронзительным) */
var SXXP=[SXN_.C5,SXN_.D5,SXN_.E5,SXN_.G5,SXN_.A5,SXN_.C6];
var SXNAV=[SXN_.C4,SXN_.D4,SXN_.E4,SXN_.G4];   /* нижняя панель: у каждого раздела своя высота «тхока» */
var N_=SXN_;

/* ---- словарь звуков ---- */
var SXD={
  /* --- семейство «клавиша»: касания и переключатели --- */
  tap:{ui:1,p:0,j:.035,min:55,dur:.1,w:0,pk:-23,lv:-24.92,
    fn:function(v,a){sxThock(v,0,{f:a&&a.nav>=0?SXNAV[a.nav%4]:N_.A3,d:.075,nza:.35,nzc:1900})}},
  /* лёгкий «тик»: копирование, запрос ввода */
  tick:{ui:1,p:0,j:.035,min:60,dur:.07,w:0,pk:-24.1,lv:-22.08,
    fn:function(v){sxThock(v,0,{f:N_.E4,d:.04,nza:.7,nzc:2300,nzd:.008,amp:.6})}},
  /* выключатель вверх (включено) и вниз (выключено) */
  on:{ui:1,p:0,j:.035,min:90,dur:.09,w:0,pk:-23.6,lv:-24.92,
    fn:function(v){sxThock(v,0,{f:N_.D4,d:.05,drop:-.09,nza:.55,nzc:2500,nzd:.008})}},
  off:{ui:1,p:0,j:.035,min:90,dur:.1,w:0,pk:-23.6,lv:-25.16,
    fn:function(v){sxThock(v,0,{f:N_.G3,d:.07,drop:.1,nza:.45,nzc:1400})}},
  /* закрытый островок: один глухой стук */
  lock:{ui:1,p:0,j:.035,min:160,dur:.16,w:0,pk:-24.6,lv:-27.24,
    fn:function(v){sxThock(v,0,{f:N_.D3,d:.11,nza:0,dull:1,drop:.05})}},
  /* запуск кода: один мягкий тик, чуть светлее касания */
  run:{ui:1,p:0,j:.035,min:120,dur:.08,w:0,pk:-23.6,lv:-25.37,
    fn:function(v){sxThock(v,0,{f:N_.E4,d:.045,nza:.6,nzc:2600,nzd:.008})}},
  /* ошибка в коде: очень тихий низкий звук */
  err:{ui:0,p:1,j:.035,min:300,dur:.2,w:0,pk:-26.6,lv:-29.49,
    fn:function(v){sxThock(v,0,{f:N_.C3,d:.13,nza:0,dull:1,drop:.04})}},
  /* печать в редакторе (отдельный выключатель, по умолчанию выключен): a.k=1 — пробел, Enter, стирание */
  key:{ui:0,p:0,j:.035,min:28,dur:.05,w:0,pk:-40.6,lv:-39.46,
    fn:function(v,a){var lo=a&&a.k;sxThock(v,0,{f:lo?N_.G3:[N_.A3,N_.C4,N_.G3][Math.floor((v.x.det?0:Math.random())*3)],d:.03,nza:.8,nzc:2000,nzd:.006,amp:.6})}},

  /* --- окна и переходы: еле слышный «воздух» до 200 мс --- */
  go:{ui:1,p:0,j:.035,min:160,dur:.19,w:.08,win:1,pk:-34.6,lv:-29.14,fn:function(v){sxAir(v,0,.15,1,420,1500)}},
  back:{ui:1,p:0,j:.035,min:160,dur:.19,w:.08,win:1,pk:-34.6,lv:-28.34,fn:function(v){sxAir(v,0,.15,1,1400,420)}},
  open:{ui:1,p:0,j:.035,min:160,dur:.19,w:.08,win:1,pk:-34.6,lv:-30.92,fn:function(v){sxAir(v,0,.17,1,380,1700)}},
  close:{ui:1,p:0,j:.035,min:160,dur:.19,w:.08,win:1,pk:-34.6,lv:-28.09,fn:function(v){sxAir(v,0,.14,1,1600,380)}},
  /* новый островок открылся: «воздух» вверх и тихая нота */
  unlock:{ui:1,p:1,j:.025,min:200,dur:.3,w:.12,pk:-24.6,lv:-22.93,
    fn:function(v){sxAir(v,0,.12,.8,420,1700);sxPluck(v,.05,N_.E5,.17,.6)}},
  /* дискета достижения: клавиша и тихая нота */
  disk:{ui:1,p:1,j:.025,min:160,dur:.25,w:.1,pk:-23.6,lv:-25.57,
    fn:function(v){sxThock(v,0,{f:N_.C4,d:.06,nza:.45});sxPluck(v,.03,N_.E5,.16,.55)}},

  /* --- обратная связь по ответам --- */
  /* верно: две мягкие восходящие ноты, до 350 мс */
  ok:{ui:0,p:1,j:.025,min:90,dur:.34,w:.12,pk:-22.1,lv:-24.81,
    fn:function(v){sxThock(v,0,{f:N_.G3,d:.05,nza:.35,amp:.5});sxPluck(v,0,N_.G4,.2,1);sxPluck(v,.085,N_.C5,.22,1)}},
  /* все тесты/вопросы верно: чуть светлее и выше */
  solve:{ui:0,p:1,j:.025,min:120,dur:.36,w:.12,pk:-21.6,lv:-25.76,
    fn:function(v){sxThock(v,0,{f:N_.G3,d:.05,nza:.35,amp:.5});sxPluck(v,0,N_.C5,.2,1);sxPluck(v,.085,N_.G5,.22,.95)}},
  /* неверно: низкий мягкий приглушённый двойной стук, не наказание */
  bad:{ui:0,p:1,j:.035,min:120,dur:.3,w:0,pk:-22.6,lv:-24.95,
    fn:function(v){sxThock(v,0,{f:N_.D3,d:.1,nza:0,dull:1,drop:.05});sxThock(v,.095,{f:N_.C3,d:.12,nza:0,dull:1,drop:.05,amp:.85})}},
  /* подсказка: тик и одна нейтральная нота */
  hint:{ui:0,p:1,j:.025,min:220,dur:.3,w:.1,pk:-23.6,lv:-22.64,
    fn:function(v){sxThock(v,0,{f:N_.E4,d:.035,nza:.6,nzc:2400,amp:.5});sxPluck(v,.015,N_.D5,.25,.85)}},
  /* теория прочитана */
  theory:{ui:0,p:1,j:.025,min:300,dur:.3,w:.1,pk:-23.6,lv:-25.57,
    fn:function(v){sxThock(v,0,{f:N_.C4,d:.06,nza:.45});sxPluck(v,.02,N_.G4,.26,.8)}},
  /* опыт: крошечный тик; a.k — номер шага, высота растёт по строю до до6 и дальше не меняется */
  xpt:{ui:0,p:0,j:.035,min:40,dur:.07,w:0,pk:-28.6,lv:-26.51,
    fn:function(v,a){var k=Math.min(5,Math.max(0,a&&a.k||0));
      sxPluck(v,0,SXXP[k],.04,.8);}},

  /* --- моменты: мотивы --- */
  /* островок пройден: три ноты вверх, до 700 мс */
  done:{ui:0,p:2,j:.025,min:400,dur:.6,w:.14,pk:-20.6,lv:-25.26,
    fn:function(v){sxThock(v,0,{f:N_.C4,d:.07,nza:.4,amp:.7});
      sxPluck(v,0,N_.C5,.17,1);sxPluck(v,.105,N_.E5,.19,1);sxPluck(v,.21,N_.G5,.36,1,{sub:.22})}},
  /* новый уровень: те же три шага, но выше и к до6 */
  level:{ui:0,p:2,j:.025,min:500,dur:.64,w:.14,pk:-20.1,lv:-24.82,
    fn:function(v){sxThock(v,0,{f:N_.C4,d:.07,nza:.4,amp:.7});
      sxPluck(v,0,N_.E5,.17,1);sxPluck(v,.1,N_.G5,.19,1);sxPluck(v,.2,N_.C6,.38,.95,{sub:.2})}},
  /* тема пройдена, проект сделан: мотив из трёх нот с тихой квинтой внизу */
  fanfare:{ui:0,p:2,j:.025,min:700,dur:.66,w:.14,pk:-20.1,lv:-25.39,
    fn:function(v){sxThock(v,0,{f:N_.C4,d:.08,nza:.4,amp:.8});
      sxPluck(v,0,N_.C5,.17,1);sxPluck(v,.11,N_.G5,.2,1);sxPluck(v,.22,N_.C6,.4,.9,{sub:.25});sxPluck(v,.22,N_.E6,.3,.28)}},
  /* серия продолжается: тёплые две ноты (квинта вверх, с подтоном) */
  streak:{ui:0,p:2,j:.025,min:450,dur:.48,w:.12,pk:-21.1,lv:-23.12,
    fn:function(v){sxPluck(v,0,N_.G4,.26,1,{sub:.3});sxPluck(v,.115,N_.D5,.34,1,{sub:.2})}},
  /* заморозка серии: две мягкие ноты вниз */
  freeze:{ui:0,p:2,j:.025,min:450,dur:.4,w:.14,pk:-22.6,lv:-23.15,
    fn:function(v){sxPluck(v,0,N_.A5,.2,.8);sxPluck(v,.09,N_.E5,.3,1)}},
  /* достижение: самый богатый звук, но мягкий; меньше 1 с */
  ach:{ui:0,p:2,j:.025,min:450,dur:.92,w:.16,pk:-17.9,lv:-24.12,
    fn:function(v){sxThock(v,0,{f:N_.C4,d:.09,nza:.4,amp:.9});
      [N_.C5,N_.E5,N_.G5,N_.C6].forEach(function(f,i){sxPluck(v,i*.085,f,.3,.9);sxPluck(v,i*.085,f*2,.18,.18)});
      sxPluck(v,.34,N_.C5,.5,.7,{sub:.25});sxPluck(v,.34,N_.G5,.5,.7);sxPluck(v,.34,N_.E6,.46,.5);
      sxPluck(v,.47,N_.G6,.2,.18);sxPluck(v,.55,N_.E6,.22,.14)}},
  /* погладить кролика */
  pet:{ui:0,p:1,j:.025,min:220,dur:.35,w:.1,pk:-23.6,lv:-23.01,
    fn:function(v){sxPluck(v,0,N_.E5,.18,.9);sxPluck(v,.08,N_.G5,.24,.9)}}
};

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
  var d=SXD[n];if(!d)return;
  if(d.ui&&!ST('sfx'))return;
  if(n==='key'&&!ST('ks'))return;
  var now=performance.now();
  if(n!=='tap'&&n!=='key')SX.la=now;
  if(!d.ui)SX.lf=now;
  /* звуки окон и переходов не накладываются на награды, сыгравшие только что */
  if(d.win&&now-SX.lf<260)return;
  if(SX.per[n]&&now-SX.per[n]<d.min)return;
  SX.per[n]=now;SX.ln=n;SX.lt=now;
  if(!SX.c||SX.dead)return;                              /* до первого касания звука нет */
  try{sxVol(VOLK());sxPlay(n,a)}catch(e){}}

/* касание любой кнопки: тихое «тхок». Другие звуки того же события (ответ, окно, переход, переключатель) его заменяют:
   проверка отложена на конец события. «Запустить» играет свой тик. */
document.addEventListener('click',function(e){
  var b=e.target&&e.target.closest&&e.target.closest('button,[role=button],a[href],summary');
  if(!b||b.disabled||b.getAttribute('aria-disabled')==='true')return;
  var t=performance.now(),nv=b.closest&&b.closest('.nav'),run=b.id==='run'&&!b.classList.contains('stp');
  setTimeout(function(){
    if(SX.la>=t)return;
    var a=null;if(nv){var bs=[].slice.call(nv.querySelectorAll('button'));a={nav:bs.indexOf(b)}}
    snd(run?'run':'tap',a)},0)},true);

/* печать в редакторе: очень тихий щелчок, только если включено «Звуки набора кода» (по умолчанию выключено) */
document.addEventListener('beforeinput',function(e){
  var t=e.target;if(!t||t.tagName!=='TEXTAREA'||!t.closest||!t.closest('.ed')||!ST('ks'))return;
  var ty=e.inputType||'';
  if(ty==='insertText'&&e.data===' '||ty==='insertLineBreak'||ty==='insertParagraph'||/^deleteContent/.test(ty))snd('key',{k:1});
  else if(ty==='insertText')snd('key',{k:0})},true);

/* счёт опыта: каждый засчитанный пункт даёт тик, высота растёт по ступеням до верхнего предела. Вызывать с текущим числом */
function xpTick(){var n=0,last=0,lt=0;return function(v){if(v<=last)return;last=v;var t=performance.now();if(t-lt<48)return;lt=t;snd('xpt',{k:n++})}}

/* для проверок: отрисовать звук без динамиков и вернуть сэмплы (tests/sound_wav.py, tests/sound6.py) */
function sndRender(n,a){return sxRender(n,a,44100).then(function(b){return b&&Array.from(b)})}
