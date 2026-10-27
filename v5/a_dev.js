/* ===================== Режим разработчика ===================== */
var DVN='TheCreatorOfNothing',DVC=null;
function DEV(){return S&&S.nick===DVN}
(function(){
  var _t=task,_q=quiz,_p=project,_th=theory,_h=home;
  task=function(i,j,k){DVC={t:'task',i:i,j:j,k:k};return _t.apply(this,arguments)};
  quiz=function(i,j){DVC={t:'quiz',i:i,j:j};return _q.apply(this,arguments)};
  project=function(i,j){DVC={t:'project',i:i,j:j};return _p.apply(this,arguments)};
  theory=function(i,j){DVC={t:'theory',i:i,j:j};return _th.apply(this,arguments)};
  home=function(){DVC=null;return _h.apply(this,arguments)};
})();
function dvEsc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;')}
function dvClose(){var o=document.getElementById('dvp');if(o)o.remove()}
function dvDone(i,j){var k=i+'-'+j,it=IT(i,j);if(!it)return;S.d[k]=1;if(it.t==='flash'||it.t==='test'){if(S.es[k]===undefined)S.es[k]=0}save()}
/* значки панели: контурные Lucide (ISC), рисуются так же, как IC в a_ui.js */
var DVI={
 tool:'<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
 pin:'<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
 star:'<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>',
 flame:'<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.07-2.14-.22-4.05 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.15.43-2.29 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
 image:'<rect width="18" height="18" x="3" y="3" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.09-3.09a2 2 0 0 0-2.82 0L6 21"/>',
 vol:'<path d="M11 5 6 9H2v6h4l5 4V5z"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07M19.07 4.93a10 10 0 0 1 0 14.14"/>',
 flag:'<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><path d="M4 22v-7"/>',
 film:'<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M7 3v18M17 3v18M3 7.5h4M3 12h18M3 16.5h4M17 7.5h4M17 16.5h4"/>',
 cup:'<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6M18 9h1.5a2.5 2.5 0 0 0 0-5H18M4 22h16M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>'
};
function dvIco(n){return'<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'+DVI[n]+'</svg>'}
/* «▶» в кнопках — простой символ, а не синяя картинка-эмодзи: noemo отключает замену из a_core.js, \uFE0E и шрифт символов (.dvpl) не дают системе нарисовать цветной глиф */
/* группа панели: заголовок со значком, необязательная подсказка, содержимое; cls: w — во всю ширину (на компьютере две колонки), cur — текущий островок */
function dvSec(ic,t,hint,body,cls){return'<section class="dvg'+(cls?' '+cls:'')+'"><h3 class="dvs">'+dvIco(ic)+'<span>'+t+'</span></h3>'+(hint?'<p class="dvn">'+hint+'</p>':'')+body+'</section>'}
function dvPanel(){
  /* при перерисовке (выдали достижение) окно не прыгает: без анимации появления и на той же прокрутке */
  var old=document.getElementById('dvp'),top=old?old.querySelector('.dvbd').scrollTop:0,fid=old&&document.activeElement&&document.activeElement.dataset.id;
  dvClose();
  var o=document.createElement('div');o.id='dvp';o.className='dvp'+(old?' re':'');
  var h='<div class="dvc" role="dialog" aria-modal="true" aria-labelledby="dvt"><div class="dvh"><span class="dvhi">'+dvIco('tool')+'</span><div class="dvht"><b id="dvt">Режим разработчика</b><small>ник «'+DVN+'»</small></div><button class="icon" id="dvx" aria-label="Закрыть">'+ico('x')+'</button></div><div class="dvbd">';
  if(DVC){
    var it=IT(DVC.i,DVC.j),lab=dvEsc(TOPICS[DVC.i].n)+' · '+dvEsc(it.n||''),b='';
    if(DVC.t==='task'){var T=it.tasks;
      b+='<div class="dvr dvst"><button data-a="tp"'+(DVC.k<1?' disabled':'')+'>◀ Задание</button><span>'+(DVC.k+1)+' из '+T.length+'</span><button data-a="tn"'+(DVC.k>=T.length-1?' disabled':'')+'>Задание <span class="dvpl noemo">▶\uFE0E</span></button></div>'}
    b+='<div class="dvr">';
    if(DVC.t==='task'||DVC.t==='project')b+='<button data-a="sol">Вставить решение</button><button class="pr" data-a="solc">Решение и проверить</button>';
    if(DVC.t==='quiz')b+='<button class="pr" data-a="ans">Показать верный ответ</button>';
    b+='</div><div class="dvr"><button data-a="cur">Отметить островок пройденным</button></div>';
    h+=dvSec('pin','Сейчас',lab,b,'w cur');
  }
  h+=dvSec('star','Опыт и уровень','','<div class="dvr"><button data-a="xp50">+50 ⭐</button><button data-a="xp500">+500 ⭐</button><button data-a="lv">+1 уровень</button></div>');
  h+=dvSec('flame','Серия и заморозки','','<div class="dvr"><button data-a="st">Серия +1</button><button data-a="st0">Серия = 0</button><button data-a="fz">Заморозка +1</button><button data-a="fzm">Заморозка −1</button><button data-a="fz0">Заморозки = 0</button></div>');
  h+=dvSec('flag','Прогресс','','<div class="dvr"><button data-a="all">Все островки пройдены</button><button data-a="gl">Цель дня выполнена</button><button class="bad" data-a="none">Сбросить прогресс островков</button></div>');
  h+=dvSec('film','Вступление','Идёт целиком (заставка, знакомство, выбор темы, сбой, синий экран) на копии данных: прогресс, ник и настройки не меняются. Выйти можно кнопкой «✕ Выйти из просмотра».','<div class="dvr"><button data-a="intro"><span class="dvpl noemo">▶\uFE0E</span> Посмотреть вступление</button></div>');
  var sp='<div class="dvim">';
  Object.keys(IMG).forEach(function(k){sp+='<figure class="dvsp"><img src="'+IMG[k]+'" alt="'+k+'" loading="lazy"><figcaption>'+k+'</figcaption></figure>'});
  h+=dvSec('image','Спрайты кролика','',sp+'</div>','w');
  var sn='<div class="dvr dvsn">';
  Object.keys(SXD).forEach(function(k){sn+='<button data-s="'+k+'"><span class="dvpl noemo">▶\uFE0E</span> '+k+'</button>'});
  h+=dvSec('vol','Звуки','Нажми, чтобы послушать.',sn+'</div>','w');
  var n=0,ac='<div class="dvr"><button data-a="aa">Выдать все</button><button data-a="an">Забрать все</button></div><div class="dva">';
  ACH.forEach(function(a){var on=!!S.ach[a.id];if(on)n++;ac+='<button class="dvk'+(on?' on':'')+'" aria-pressed="'+on+'" data-id="'+a.id+'" title="'+dvEsc(a.d)+'"><span class="e">'+a.e+'</span><span>'+dvEsc(a.n)+'</span></button>'});
  h+=dvSec('cup','Достижения','Нажми, чтобы выдать или забрать. Выдано '+n+' из '+ACH.length+'.',ac+'</div>','w');
  h+='<p class="dvf">Режим включён ником «'+DVN+'». Все островки открыты, прогресс и достижения можно менять вручную. Чтобы выключить, смени ник в профиле.</p></div></div>';
  o.innerHTML=h;document.body.appendChild(o);
  var c=o.querySelector('.dvbd');if(old){c.scrollTop=top;var fb=fid&&o.querySelector('.dvk[data-id="'+fid+'"]');if(fb)fb.focus({preventScroll:true})}else document.getElementById('dvx').focus({preventScroll:true});
  o.onclick=function(e){if(e.target===o)dvClose()};
  document.getElementById('dvx').onclick=dvClose;
  o.querySelectorAll('.dvk').forEach(function(b){b.onclick=function(){var id=b.dataset.id;if(S.ach[id]){delete S.ach[id];save()}else ach(id);dvPanel()}});
  o.querySelectorAll('[data-s]').forEach(function(b){b.onclick=function(){
    try{if(typeof sxShow==='function')sxShow();sxVol(VOLK());sxPlay(b.dataset.s,{k:3})}catch(e){toast('Звук недоступен: коснись экрана и попробуй снова')}}});
  o.querySelectorAll('[data-a]').forEach(function(b){b.onclick=function(){dvAct(b.dataset.a)}});
}
function dvAct(a){
  var c=DVC;
  if(a==='tp'||a==='tn'){dvClose();return task(c.i,c.j,c.k+(a==='tn'?1:-1))}
  if(a==='sol'||a==='solc'){
    var it=IT(c.i,c.j),sol=c.t==='task'?it.tasks[c.k].sol:it.sol,ed=document.getElementById('code');
    if(!sol||!ed)return toast('Решения нет или редактор не открыт');
    ed.value=sol;ed.dispatchEvent(new Event('input',{bubbles:true}));
    dvClose();if(a==='solc'){var b=document.getElementById('chk')||document.getElementById('pchk');if(b)b.click()}return}
  if(a==='ans'){
    var qq=document.querySelector('h2'),Ql=IT(c.i,c.j).q,tx=qq?qq.textContent.trim():'',hit=null;
    Ql.forEach(function(x){if(x.q.trim()===tx&&!hit)hit=x});
    if(!hit)return toast('Вопрос не найден на экране');
    document.querySelectorAll('.opt').forEach(function(b){if(b.textContent.trim()===String(hit.o[hit.a]).trim())b.classList.add('sel')});
    return toast('Верно: '+hit.o[hit.a])}
  if(a==='cur'){dvDone(c.i,c.j);dvClose();return home()}
  if(a==='xp50'){addXp(50);save();toast('+50 ⭐');return}
  if(a==='xp500'){addXp(500);save();toast('+500 ⭐');return}
  if(a==='lv'){var l=lvlInfo(S.xp).l,n=0;while(lvlInfo(S.xp).l===l&&n++<400)addXp(10);save();toast('Уровень: '+lvlInfo(S.xp).l);return}
  if(a==='st'){var t=day(new Date());if(S.last!==t){S.last=t;S.streak=(S.streak||0)+1}else S.streak++;if(S.streak>S.max)S.max=S.streak;save();toast('Серия: '+S.streak);return}
  if(a==='st0'){S.streak=0;save();toast('Серия сброшена');return}
  if(a==='fz'){S.fz.n=Math.min(2,S.fz.n+1);save();toast('Заморозок: '+S.fz.n);return}
  if(a==='fzm'){S.fz.n=Math.max(0,S.fz.n-1);save();toast('Заморозок: '+S.fz.n);return}
  if(a==='fz0'){S.fz.n=0;S.fz.p=0;save();toast('Заморозок: 0');return}
  if(a==='all'){TOPICS.forEach(function(t,i){t.items.forEach(function(x,j){dvDone(i,j)})});toast('Все островки пройдены');dvClose();return home()}
  if(a==='none'){S.d={};S.es={};S.at={};S.dr={};S.tk={};S.hu={};save();toast('Прогресс островков сброшен');dvClose();return home()}
  if(a==='intro')return dvIntro();
  if(a==='gl'){var t2=day(new Date());S.hist[t2]=S.hist[t2]||{les:0};S.hist[t2].les=Math.max(S.hist[t2].les||0,S.goal);goalCheck();save();toast('Цель дня засчитана');return}
  if(a==='aa'){ACH.forEach(function(x){if(x.id!=='all'&&!S.ach[x.id])ach(x.id)});return dvPanel()}
  if(a==='an'){S.ach={};save();return dvPanel()}
}
(function(){
  function sync(){var b=document.getElementById('dvb');if(DEV()){if(!b){b=document.createElement('button');b.id='dvb';b.className='dvb';b.setAttribute('aria-label','Режим разработчика');b.innerHTML=dvIco('tool');b.onclick=dvPanel;document.body.appendChild(b)}}else{if(b)b.remove();dvClose()}}
  setInterval(sync,700);
})();

/* Просмотр вступления для разработчика: настоящее вступление, но на копии данных. Хранилище не пишется (save заглушен),
   в конце или по кнопке выхода S возвращается из снимка. Прогресс, ник и настройки остаются как были. */
var DVPV=null;
function dvIntro(){
  dvClose();if(DVPV||typeof crtOpen!=='function')return;
  DVPV={bk:JSON.stringify(S),sv:save,fa:fzApply,cc:crtCrash};
  save=function(){};S.nick='';
  crtCrash=function(){
    var P=DVPV;if(!P)return;
    S=JSON.parse(P.bk);var seen=S.seen;fzApply=function(){};
    try{P.cc()}finally{fzApply=P.fa;S.seen=seen}
    dvIntroEnd(1)};
  var b=document.createElement('button');b.id='dvpx';b.className='dvpx';b.textContent='✕ Выйти из просмотра';b.onclick=function(){dvIntroEnd()};document.body.appendChild(b);
  crtOpen()}
function dvIntroEnd(soft){
  var P=DVPV;if(!P)return;DVPV=null;
  save=P.sv;fzApply=P.fa;crtCrash=P.cc;if(!soft)S=JSON.parse(P.bk);
  var x=document.getElementById('dvpx');if(x)x.remove();
  if(!soft){crtClose();['shards','bsod'].forEach(function(id){var e=document.getElementById(id);if(e)e.remove()});document.documentElement.classList.remove('crt-on');home();window.scrollTo(0,0)}}
