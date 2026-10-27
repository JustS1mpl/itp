/* ===================== ИТП — ядро: настройки, сохранение, звук, серия, цели, достижения ===================== */
function defset(){return{acc:'',tz:100,anim:'full',vol:70,sfx:1,vib:1,emo:1,ty:1,toc:1,rep:1,ln:1,ac:1,cf:15,gc:1,bg:1,ks:0,ph:'card',sh:'v',fl:'tilt'}}
function ST(k){return S.set&&S.set[k]!==undefined?S.set[k]:defset()[k]}
function RM(){return ST('anim')==='off'||matchMedia('(prefers-reduced-motion:reduce)').matches}
function pad2(n){return(n<10?'0':'')+n}
function dnum(s){var p=s.split('-');return Math.round(Date.UTC(+p[0],p[1]-1,+p[2])/864e5)}
function dadd(s,n){var p=s.split('-'),d=new Date(Date.UTC(+p[0],p[1]-1,+p[2]+n));return d.getUTCFullYear()+'-'+pad2(d.getUTCMonth()+1)+'-'+pad2(d.getUTCDate())}
function vdate(x){if(typeof x!=='string'||!/^\d{4}-\d\d-\d\d$/.test(x))return'';var y=+x.slice(0,4),m=+x.slice(5,7),d=+x.slice(8,10);if(y<2020||y>2100)return'';var t=new Date(Date.UTC(y,m-1,d));return t.getUTCFullYear()===y&&t.getUTCMonth()===m-1&&t.getUTCDate()===d?x:''}
/* --- проверка новых полей сохранения --- */
function clean0_(r){return clean0(r)}
/* v5.7.0: раздел ЕГЭ удалён. В старых сохранениях номера тем 15-20 выбрасываются, 21 и выше сдвигаются на -6.
   Метка mv=2 (число, а не переменная: clean() вызывается при загрузке раньше, чем выполняются var) нужна, чтобы сдвиг не применился дважды. */
function migr(r){
  /* mv:2 — удалён раздел ЕГЭ (темы 15–20 выброшены, 21+ сдвинуты на −6); mv:3 — между темами 8 и 9 вставлена доп. глава «Черепаха» (9+ сдвинуты на +1);
     mv:4 — после темы «Строки, кортежи, списки» вставлена доп. глава «Системы счисления» (11+ сдвинуты на +1) */
  if(!r||typeof r!=='object'||Array.isArray(r)||r.mv>=4)return r;
  var m1=function(i){return i<15?i:(i>=21?i-6:-1)},m2=function(i){return i<9?i:i+1},m3=function(i){return i<11?i:i+1};
  var mp=r.mv>=3?m3:(r.mv===2?function(i){return m3(m2(i))}:function(i){var a=m1(i);return a<0?-1:m3(m2(a))}),o={};
  for(var k in r)if(Object.prototype.hasOwnProperty.call(r,k))o[k]=r[k];
  ['d','tk','at','es','dr','hu'].forEach(function(f){
    var x=r[f];if(!x||typeof x!=='object'||Array.isArray(x))return;
    var y={};
    Object.keys(x).forEach(function(key){
      var p=key.split('-'),n=mp(+p[0]);
      if(n<0||!/^\d+$/.test(p[0]))return;
      p[0]=String(n);y[p.join('-')]=x[key]});
    o[f]=y});
  if(Number.isInteger(r.start)&&r.start>=0){var s=r.start;
    if(r.mv>=3)o.start=m3(s);
    else{if(r.mv!==2)s=s<15?s:(s>=21?s-6:15);o.start=m3(m2(s))}}
  return o}
function clean(r){
  r=migr(r);
  var o=clean0(r);o.mv=4;r=(r&&typeof r==='object'&&!Array.isArray(r))?r:{};
  var s=(r.set&&typeof r.set==='object'&&!Array.isArray(r.set))?r.set:{},q={};
  var pick=function(k,list){q[k]=list.indexOf(s[k])>=0?s[k]:defset()[k]},bl=function(k){q[k]=s[k]===0||s[k]===false?0:(s[k]===1||s[k]===true?1:defset()[k])};
  pick('acc',['','carrot','pink','blue','violet']);pick('tz',[90,100,115,130]);pick('anim',['full','less','off']);pick('cf',[13,15,17,19]);pick('sh',['v','h']);pick('ph',['card','corner','pop']);pick('fl',['tilt','flat']);
  q.vol=typeof s.vol==='number'&&s.vol>=0&&s.vol<=100?Math.round(s.vol):defset().vol;
  ['sfx','vib','emo','ty','toc','rep','ln','ac','gc','bg','ks'].forEach(bl);
  /* «Минимализм» убран (6.9.0): у кого он был включён, узор на фоне возвращается таким, каким был до минимализма (mb) */
  if(s.mn===1||s.mn===true)q.bg=s.mb===0||s.mb===false?0:1;
  o.set=q;
  o.goal=[1,2,3].indexOf(r.goal)>=0?r.goal:1;
  var gm={},c=0,TM=day(ago(-1));if(r.gm&&typeof r.gm==='object'&&!Array.isArray(r.gm))Object.keys(r.gm).sort().reverse().forEach(function(k){if(c<70&&vdate(k)&&k<=TM&&r.gm[k]){gm[k]=1;c++}});o.gm=gm;
  o.wk=vdate(r.wk);
  var f=(r.fz&&typeof r.fz==='object')?r.fz:{},u=[];
  if(Array.isArray(f.u))f.u.forEach(function(x){if(vdate(x)&&u.indexOf(x)<0&&u.length<80)u.push(x)});
  o.fz={n:Number.isInteger(f.n)&&f.n>=0&&f.n<=2?f.n:0,p:Number.isInteger(f.p)&&f.p>=0&&f.p<=14?f.p:0,u:u.sort()};
  var a={};if(r.ach&&typeof r.ach==='object'&&!Array.isArray(r.ach))for(var k in r.ach)if(/^[a-z0-9]{2,12}$/.test(k)&&vdate(r.ach[k])&&Object.keys(a).length<60)a[k]=r.ach[k];o.ach=a;
  var cn=(r.cn&&typeof r.cn==='object')?r.cn:{};
  var cnum=function(k){return Number.isInteger(cn[k])&&cn[k]>=0?Math.min(cn[k],99999):0};
  o.cn={ne:cnum('ne'),nn:cnum('nn'),nd:vdate(cn.nd),gn:cnum('gn'),gd:vdate(cn.gd),pf:cnum('pf'),pj:cnum('pj'),rc:cnum('rc')};
  var hu={};if(r.hu&&typeof r.hu==='object'&&!Array.isArray(r.hu))for(var h in r.hu)if(/^\d{1,3}$/.test(h)&&+h<TOPICS.length&&r.hu[h])hu[h]=1;o.hu=hu;
  o.rp=vdate(r.rp);o.rnd=r.rnd?1:0;
  return o}
/* --- тема, акцент, размер текста --- */
function applyPrefs(){
  var r=document.documentElement,th=S.theme||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');
  r.setAttribute('data-theme',th);
  if(ST('acc'))r.setAttribute('data-acc',ST('acc'));else r.removeAttribute('data-acc');
  r.style.setProperty('--tz',ST('tz')/100);r.style.setProperty('--cf',ST('cf')+'px');
  r.setAttribute('data-anim',ST('anim'));r.setAttribute('data-fl',ST('fl'));r.classList.toggle('noln',!ST('ln'));r.setAttribute('data-ph',ST('ph'));r.classList.toggle('nobg',!ST('bg'));
  var m=document.querySelector('meta[name=theme-color]');if(!m){m=document.createElement('meta');m.name='theme-color';document.head.appendChild(m)}
  m.content=th==='dark'?'#171315':'#FBF7F5';
}
function applyTheme(){applyPrefs()}
try{matchMedia('(prefers-color-scheme:dark)').addEventListener('change',function(){if(!S.theme)themeSwap(applyPrefs)})}catch(e){}
/* смена темы: плавный наплыв всей страницы (View Transitions — один снимок «до» и «после»), а не переходы цвета у каждого
   элемента: их сотни, многие со стеклом и размытием, и на Ctrl+D смена шла рывками. Без поддержки — мгновенно */
function themeSwap(fn){if(document.startViewTransition&&!RM()&&!document.hidden){try{document.startViewTransition(fn);return}catch(e){}}fn()}
function toggleTheme(){themeSwap(function(){S.theme=isDark()?'light':'dark';applyPrefs();save();if(HRE)HRE()})}
function isDark(){return document.documentElement.getAttribute('data-theme')==='dark'||(!document.documentElement.getAttribute('data-theme')&&matchMedia('(prefers-color-scheme:dark)').matches)}
/* --- смайлики Windows 11 (Fluent Emoji, MIT) --- */
var EM={map:null,url:Object.create(null),obs:null};
var EMRX=/(?:[\u{1F000}-\u{1FAFF}←-⯿©®‼⁉™ℹⓂ〰〽㊗㊙])️?(?:‍[\u{1F000}-\u{1FAFF}♀♂⚕⚖✈❤]️?)*/gu,EMT=/[\u{1F000}-\u{1FAFF}←-⯿©®‼⁉™ℹⓂ〰〽㊗㊙]/u;
function emoKey(g){var a=[];for(var ch of g){var c=ch.codePointAt(0);if(c!==0xFE0F)a.push(c.toString(16))}return a.join('-')}
function emoSrc(g){var k=emoKey(g);if(!EM.map||!EM.map[k])return'';if(!EM.url[k])EM.url[k]='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(EM.map[k]);return EM.url[k]}
function emoImg(g){var s=emoSrc(g);if(!s)return null;var i=document.createElement('img');i.className='em';i.alt=g;i.onerror=function(){if(i.parentNode)i.replaceWith(document.createTextNode(g))};i.src=s;i.draggable=false;return i}
function emoNode(n){
  var t=n.nodeValue;if(!t||!EMT.test(t))return;
  var p=n.parentNode;if(!p||p.closest&&p.closest('pre,code,textarea,input,script,style,.noemo'))return;
  var out=document.createDocumentFragment(),last=0,m,any=false;EMRX.lastIndex=0;
  while((m=EMRX.exec(t))){var im=emoImg(m[0]);if(!im)continue;any=true;if(m.index>last)out.appendChild(document.createTextNode(t.slice(last,m.index)));out.appendChild(im);last=m.index+m[0].length}
  if(!any)return;if(last<t.length)out.appendChild(document.createTextNode(t.slice(last)));p.replaceChild(out,n)}
function emoScan(root){
  if(!EM.map||!ST('emo'))return;
  if(root.nodeType===3){emoNode(root);return}
  if(root.nodeType!==1)return;
  var w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,null),a=[],n;while(n=w.nextNode())a.push(n);a.forEach(emoNode)}
function emoOn(){
  if(!EM.map||!ST('emo'))return;
  emoScan(document.body);
  if(!EM.obs){EM.obs=new MutationObserver(function(ms){EM.obs.disconnect();try{ms.forEach(function(m){if(m.type==='characterData')emoNode(m.target);else m.addedNodes.forEach(function(x){emoScan(x)})})}finally{EM.obs.observe(document.body,{childList:true,subtree:true,characterData:true})}})}
  EM.obs.observe(document.body,{childList:true,subtree:true,characterData:true})}
function emoOff(){if(EM.obs)EM.obs.disconnect();document.querySelectorAll('img.em').forEach(function(i){i.replaceWith(document.createTextNode(i.alt))})}
function emoLoad(){
  var el=document.getElementById('emo-pack');if(!el||!window.DecompressionStream||EM.map){if(EM.map)emoOn();return}
  try{var b=atob(el.textContent.trim()),u=new Uint8Array(b.length);for(var i=0;i<b.length;i++)u[i]=b.charCodeAt(i);
    new Response(new Blob([u]).stream().pipeThrough(new DecompressionStream('gzip'))).json().then(function(m){EM.map=m;if(ST('emo'))emoOn()}).catch(function(){})}catch(e){}}
/* звуки: v5/a_sound.js (синтез Web Audio, без файлов) */
function vib(p){if(!ST('vib'))return;var C=window.Capacitor,H=C&&C.Plugins&&C.Plugins.Haptics;try{if(H&&H.vibrate)H.vibrate({duration:Array.isArray(p)?p.reduce(function(a,b){return a+b},0):p});else if(navigator.vibrate)navigator.vibrate(p)}catch(e){}}
function fx(ok,kind){
  if(ok){if(kind==='test')snd('solve');else if(kind!=='none')snd('ok')}else snd('bad');
  vg.className=ok?'ok':'no';
  if(!RM())vg.animate([{opacity:0},{opacity:.7},{opacity:0}],{duration:800});
  if(!ok){vib([60,40,60]);if(!RM())app.animate([{transform:'translateX(0)'},{transform:'translateX(-7px)'},{transform:'translateX(6px)'},{transform:'translateX(-4px)'},{transform:'translateX(0)'}],{duration:380})}
}
function toggleMute(){if(!S.mute)snd('off');S.mute=S.mute?0:1;save();if(HRE)HRE();toast(S.mute?'Звук выключен':'Звук включён');if(!S.mute)snd('on')}
/* --- очередь уведомлений --- */
var TQ=[],TB=false;
function toast(t,cls,a){TQ.push([t,cls,a]);if(!TB)tnext()}
/* достижение приходит карточкой с дискетой своего цвета, остальное — короткой строкой сверху */
function tnext(){var x=TQ.shift();if(!x){TB=false;return}TB=true;var o=document.querySelector('.toast');if(o)o.remove();var d=document.createElement('div');d.className='toast'+(x[1]?' '+x[1]:'');d.setAttribute('role','status');
  if(x[1]==='ach'&&x[2]){d.innerHTML='<span class="mfd" style="--fc:'+x[2].c+'" aria-hidden="true"><b>'+x[2].e+'</b></span><span><span class="tsm">Новое достижение</span>'+esc(x[2].n)+'</span>'}else d.textContent=x[0];
  document.body.appendChild(d);if(x[1]==='ach')snd('ach');setTimeout(function(){d.remove();setTimeout(tnext,80)},x[1]==='ach'?3100:2300)}
/* --- серия и заморозки --- */
function streakNow(){var y=day(ago(1));return(S.last===day(new Date())||S.last===y)?S.streak:0}
function fzApply(){
  if(!S.last||S.streak<1)return 0;var y=day(ago(1));if(S.last>=y)return 0;
  var miss=dnum(y)-dnum(S.last);if(miss<1||S.fz.n<miss)return 0;
  for(var k=1;k<=miss;k++)S.fz.u.push(dadd(S.last,k));
  S.fz.u=S.fz.u.slice(-80);S.fz.n-=miss;S.last=y;save();
  setTimeout(function(){snd('freeze');toast('Серия сохранена: заморозка потрачена ('+miss+')','');ach('ice2')},500);
  return miss}
function fzEarn(){
  if(S.fz.n>=2){S.fz.p=0;return}
  S.fz.p++;if(S.fz.p>=15){S.fz.p=0;S.fz.n++;toast('Новая заморозка серии! Теперь их: '+S.fz.n);snd('freeze');ach('ice')}}
/* --- цели --- */
function goalDone(){var h=S.hist[day(new Date())];return h?h.les:0}
function wkStart(){var d=new Date();d.setHours(12,0,0,0);d.setDate(d.getDate()-((d.getDay()+6)%7));return day(d)}
function wkCount(){var w=wkStart(),n=0;for(var i=0;i<7;i++)if(S.gm[dadd(w,i)])n++;return n}
function goalCheck(){
  var t=day(new Date());if(goalDone()<S.goal||S.gm[t])return;
  S.gm[t]=1;var ks=Object.keys(S.gm).sort();while(ks.length>70)delete S.gm[ks.shift()];
  S.cn.gn=(S.cn.gd===dadd(t,-1))?S.cn.gn+1:1;S.cn.gd=t;save();
  toast('Цель дня выполнена!');snd('done');
  if(S.cn.gn>=5)ach('g5');if(S.cn.gn>=14)ach('g14');if(S.cn.gn>=30)ach('g30');
  if(wkCount()>=5&&S.wk!==wkStart()){S.wk=wkStart();var lv=addXp(50);toast('Цель недели закрыта: +50 ⭐');ach('week');if(lv)toast('Новый уровень: '+lv)}
}
/* --- достижения --- */
var ACH=[
 {id:'intro',n:'Первые шаги',d:'Пройди вводный островок.',e:'🌱',c:'#6BBE49'},
 {id:'first',n:'Без единой ошибки',d:'Реши кодовое задание с первой попытки, не сделав ни одной ошибки.',e:'🎯',c:'#E8557A'},
 {id:'hat',n:'Тройная точность',d:'Пройди 3 островка подряд без ошибок.',e:'⚡',c:'#2F7BEF'},
 {id:'perfect',n:'Чистая тема',d:'Пройди тему целиком с первой попытки, без ошибок.',e:'💯',c:'#46A32F'},
 {id:'perf5',n:'Пять чистых тем',d:'Пройди пять тем без единой ошибки (по каждой отдельно).',e:'🌟',c:'#D6A100'},
 {id:'nohint',n:'Своим умом',d:'Пройди тему, ни разу не взяв подсказку.',e:'🧠',c:'#E85DA0'},
 {id:'t5',n:'Пятёрка',d:'Пройди 5 тем.',e:'🏅',c:'#3D8EF0'},
 {id:'t10',n:'Десятка',d:'Пройди 10 тем.',e:'🥇',c:'#E0A100'},
 {id:'tall',n:'Весь курс',d:'Пройди все темы курса.',e:'🎓',c:'#7B5CE6'},
 {id:'proj',n:'Первый проект',d:'Сделай свой первый мини-проект (пропуск не считается).',e:'🚀',c:'#7B5CE6'},
 {id:'pj3',n:'Проектировщик',d:'Сделай 3 мини-проекта (пропуск не считается).',e:'🛠️',c:'#B5651D'},
 {id:'pran',n:'Аналитик',d:'Сделай проект «Анализ качества образовательной программы».',e:'📊',c:'#16A39A'},
 {id:'papi',n:'Бэкендер',d:'Сделай итоговый проект «Обработка запроса с интерфейса».',e:'🖥️',c:'#2F6FD0'},
 {id:'pwsgi',n:'Архитектор сервера',d:'Сделай итоговый проект «Создание ASGI/WSGI-сервера».',e:'🏗️',c:'#6B4EE6'},
 {id:'pbank',n:'Банкир',d:'Сделай большой проект «Банк» целиком: все пять этапов.',e:'🏦',c:'#0F8B8D'},
 {id:'w1',n:'Неделя подряд',d:'Занимайся 7 дней подряд.',e:'🥕',c:'#F28A12'},
 {id:'m1',n:'Месяц подряд',d:'Занимайся 30 дней подряд.',e:'🏆',c:'#D6A100'},
 {id:'s100',n:'Сотня',d:'Занимайся 100 дней подряд.',e:'👑',c:'#C2410C'},
 {id:'g5',n:'Пять целей подряд',d:'Выполни цель дня 5 дней подряд.',e:'🔥',c:'#E8553A'},
 {id:'week',n:'Цель недели',d:'Выполни цель дня пять раз за одну неделю.',e:'🎖️',c:'#C4562B'},
 {id:'g14',n:'Две недели цели',d:'Выполни цель дня 14 дней подряд.',e:'💎',c:'#2AA5D8'},
 {id:'g30',n:'Цель месяца',d:'Выполни цель дня 30 дней подряд.',e:'🌠',c:'#6B4FD8'},
 {id:'ice',n:'Первая заморозка',d:'Получи свою первую заморозку серии.',e:'❄️',c:'#4AB3E8'},
 {id:'ice2',n:'Серия спасена',d:'Пусть заморозка спасёт твою серию после пропущенного дня.',e:'🧊',c:'#2A8BC4'},
 {id:'lv5',n:'Пятый уровень',d:'Достигни 5 уровня.',e:'⬆️',c:'#46A32F'},
 {id:'lv10',n:'Десятый уровень',d:'Достигни 10 уровня.',e:'🚀',c:'#E8557A'},
 {id:'rnd50',n:'Тренажёр',d:'Верно ответь на 50 заданий в режимах «Случайный вопрос» и «Случайный код».',e:'🎲',c:'#8B5CF6'},
 {id:'rep1',n:'Освежил память',d:'Ответь верно на все 3 вопроса повторения после перерыва.',e:'🔁',c:'#16A39A'},
 {id:'share',n:'Поделился',d:'Сохрани или отправь картинку со своим прогрессом.',e:'📤',c:'#3D8EF0'},
 {id:'back',n:'С возвращением!',d:'Вернись к занятиям после перерыва больше 3 дней.',e:'👋',c:'#16A39A'},
 {id:'night',n:'Ночная сова',d:'Пройди островок с 23:00 до 3:59.',e:'🦉',c:'#5B4BC4'},
 {id:'early',n:'Жаворонок',d:'Пройди островок с 4:00 до 8:00.',e:'🌅',c:'#F7931E'},
 {id:'owl5',n:'Полуночник',d:'Занимайся с 23:00 до 3:59 пять ночей подряд.',e:'🌙',c:'#34408F'},
 {id:'egg',n:'Секрет',d:'Найди секрет, спрятанный в приложении.',e:'🪄',c:'#C026D3'},
 {id:'all',n:'Коллекционер',d:'Собери все остальные достижения.',e:'🏆',c:'#B8860B'}
];
function achDef(id){for(var i=0;i<ACH.length;i++)if(ACH[i].id===id)return ACH[i]}
function ach(id){
  if(S.ach[id])return;var d=achDef(id);if(!d)return;
  S.ach[id]=day(new Date());save();
  toast('🏆 Достижение: '+d.n,'ach',d);
  vib([30,40,30]);
  if(id!=='all'&&ACH.every(function(a){return a.id==='all'||S.ach[a.id]}))ach('all');
}
function topicDone(i){
  var t=TOPICS[i];if(!t)return;
  if(t.intro){ach('intro');return}
  var clean_=true,hasTest=false;
  (t.items||[]).forEach(function(x,j){if(x.t==='flash'||x.t==='test'){if(S.es[i+'-'+j]===undefined||S.es[i+'-'+j]>0)clean_=false}if(x.t==='test')hasTest=true});
  if(clean_){ach('perfect');S.cn.pf=Math.min(99999,S.cn.pf+1);if(S.cn.pf>=5)ach('perf5');save()}
  if(hasTest&&!S.hu[i])ach('nohint');
  var n=0;TOPICS.forEach(function(x,k){if(!x.intro&&tdone(k)&&(x.items||[]).some(function(y,j){return(y.t==='flash'||y.t==='test')&&S.es[k+'-'+j]!==undefined}))n++});
  if(n>=5)ach('t5');if(n>=10)ach('t10');if(allDone()&&n>=NT())ach('tall');
}
function rec(k,e){
  var nw=!S.d[k];S.es[k]=Math.min(99,e);if(!nw)return;
  var m=/^(\d+)-(\d+)$/.exec(k),it=m?IT(+m[1],+m[2]):null;if(!it||(it.t!=='flash'&&it.t!=='test'))return;
  if(e===0){S.cn.ne++;if(it.t==='test')ach('first');if(S.cn.ne>=3)ach('hat')}else S.cn.ne=0;
  save()}
function bump(k){
  fzApply();
  var nw=!S.d[k];S.d[k]=1;var t=day(new Date()),prev=S.last;
  if(S.last!==t){S.streak=(S.last===day(ago(1)))?S.streak+1:1;S.last=t}
  if(S.streak>S.max)S.max=S.streak;delete S.dr[k];
  if(nw){
    hit(0,1);fzEarn();
    var hr=new Date().getHours();
    if(hr>=23||hr<4){ach('night');if(S.cn.nd!==t){S.cn.nn=(S.cn.nd===dadd(t,-1))?S.cn.nn+1:1;S.cn.nd=t}if(S.cn.nn>=5)ach('owl5')}
    if(hr>=4&&hr<8)ach('early');
    if(prev&&dnum(t)-dnum(prev)>3)ach('back');
    if(S.streak>=7)ach('w1');if(S.streak>=30)ach('m1');if(S.streak>=100)ach('s100');
    var m=/^(\d+)-\d+$/.exec(k);if(m&&tdone(+m[1]))topicDone(+m[1]);
    goalCheck();
  }
  save()}

/* уровни: достижения (оборачиваем addXp) */
var addXp0=addXp;
addXp=function(x){var r=addXp0(x),l=lvlInfo(S.xp).l;if(l>=5)ach('lv5');if(l>=10)ach('lv10');return r};
