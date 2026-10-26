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
function dvPanel(){
  dvClose();
  var o=document.createElement('div');o.id='dvp';o.className='dvp';
  var h='<div class="dvc"><div class="dvh"><b>🛠 Режим разработчика</b><button class="icon" id="dvx" aria-label="Закрыть">✕</button></div>';
  if(DVC){
    var it=IT(DVC.i,DVC.j),lab=dvEsc(TOPICS[DVC.i].n)+' · '+dvEsc(it.n||'');
    h+='<div class="dvs">Сейчас: '+lab+'</div><div class="dvr">';
    if(DVC.t==='task'){var T=it.tasks;
      h+='<button data-a="tp"'+(DVC.k<1?' disabled':'')+'>◀ Задание</button><button data-a="tn"'+(DVC.k>=T.length-1?' disabled':'')+'>Задание ▶</button><button data-a="sol">Вставить решение</button><button data-a="solc">Решение и проверить</button>'}
    if(DVC.t==='project')h+='<button data-a="sol">Вставить решение</button><button data-a="solc">Решение и проверить</button>';
    if(DVC.t==='quiz')h+='<button data-a="ans">Показать верный ответ</button>';
    h+='<button data-a="cur">Отметить островок пройденным</button></div>';
  }
  h+='<div class="dvs">Опыт и уровень</div><div class="dvr"><button data-a="xp50">+50 ⭐</button><button data-a="xp500">+500 ⭐</button><button data-a="lv">+1 уровень</button></div>';
  h+='<div class="dvs">Серия и заморозки</div><div class="dvr"><button data-a="st">Серия +1</button><button data-a="st0">Серия = 0</button><button data-a="fz">Заморозка +1</button><button data-a="fzm">Заморозка −1</button><button data-a="fz0">Заморозки = 0</button></div>';
  h+='<div class="dvs">Спрайты кролика</div><div class="dvr dvim">';
  Object.keys(IMG).forEach(function(k){h+='<figure class="dvsp"><img src="'+IMG[k]+'" alt="'+k+'"><figcaption>'+k+'</figcaption></figure>'});
  h+='</div>';
  h+='<div class="dvs">Звуки (нажми, чтобы послушать)</div><div class="dvr">';
  Object.keys(SXD).forEach(function(k){h+='<button class="dvk" data-s="'+k+'">▶ '+k+'</button>'});
  h+='</div>';
  h+='<div class="dvs">Прогресс</div><div class="dvr"><button data-a="all">Все островки пройдены</button><button data-a="none">Сбросить прогресс островков</button><button data-a="gl">Цель дня выполнена</button></div>';
  h+='<div class="dvs">Достижения (нажми, чтобы выдать или забрать)</div><div class="dvr"><button data-a="aa">Выдать все</button><button data-a="an">Забрать все</button></div><div class="dva">';
  ACH.forEach(function(a){h+='<button class="dvk'+(S.ach[a.id]?' on':'')+'" data-id="'+a.id+'" title="'+dvEsc(a.d)+'">'+a.e+' '+dvEsc(a.n)+'</button>'});
  h+='</div><p class="mu" style="font-size:12px;margin-top:10px">Режим включён ником «'+DVN+'». Все островки открыты, прогресс и достижения можно менять вручную. Чтобы выключить, смени ник в профиле.</p></div>';
  o.innerHTML=h;document.body.appendChild(o);
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
  if(a==='gl'){var t2=day(new Date());S.hist[t2]=S.hist[t2]||{les:0};S.hist[t2].les=Math.max(S.hist[t2].les||0,S.goal);goalCheck();save();toast('Цель дня засчитана');return}
  if(a==='aa'){ACH.forEach(function(x){if(x.id!=='all'&&!S.ach[x.id])ach(x.id)});return dvPanel()}
  if(a==='an'){S.ach={};save();return dvPanel()}
}
(function(){
  function sync(){var b=document.getElementById('dvb');if(DEV()){if(!b){b=document.createElement('button');b.id='dvb';b.className='dvb';b.setAttribute('aria-label','Режим разработчика');b.textContent='🛠';b.onclick=dvPanel;document.body.appendChild(b)}}else{if(b)b.remove();dvClose()}}
  setInterval(sync,700);
})();
