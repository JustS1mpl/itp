/* «Что обновилось в курсе» (владелец, 7.0.0): у каждой теории, карточек и задач есть отпечаток содержимого. Отпечатки
   с прошлого захода лежат в настройках устройства (appGet().ch). Если в темах, которые ученик уже начал, что-то
   поменялось или появилось новое — при заходе окно Windows 98 на чёрном экране с падающими символами (как условия
   использования) со списком «где именно»; «OK» — вспышка и обычный экран. Первый заход на устройстве — отпечатки
   запоминаются молча. Темы, до которых ученик не дошёл, не перечисляются: там всё и так будет новым */
var UPK={theory:'Теория',flash:'Карточки',test:'Задачи',project:'Проект',quiz:'Вопросы'};
function upHash(x){var h=2166136261;for(var i=0;i<x.length;i++){h^=x.charCodeAt(i);h=Math.imul(h,16777619)}return(h>>>0).toString(36)}
function upPrint(it){
  var o={t:it.t,html:it.html,q:it.q};
  if(it.tasks)o.tasks=it.tasks.map(function(k){return[k.q,k.ex,k.h,k.tests,k.starter,k.fix]});
  return upHash(JSON.stringify(o))}
/* отпечатки всего курса: ключ — отпечаток «тема|вид|название|который по счёту» (у теории, карточек и задач урока
   название общее), чтобы перестановка тем не считалась изменением */
function upKeys(t){var c={};return(t.items||[]).map(function(it){var b=t.n+'|'+it.t+'|'+it.n;c[b]=(c[b]||0)+1;return upHash(b+'|'+c[b])})}
function upMap(){var m={};TOPICS.forEach(function(t){var ks=upKeys(t);(t.items||[]).forEach(function(it,j){m[ks[j]]=upPrint(it)})});return m}
function upStarted(i){var t=TOPICS[i];return(t.items||[]).some(function(x,j){return S.d&&S.d[i+'-'+j]||S.tk&&S.tk[i+'-'+j+'-0']})}
function upDiff(old){var r=[];
  TOPICS.forEach(function(t,i){if(t.intro||!upStarted(i))return;var ch=[];
    var ks=upKeys(t);(t.items||[]).forEach(function(it,j){var k=ks[j];if(old[k]===undefined)ch.push([it,'новое']);else if(old[k]!==upPrint(it))ch.push([it,'обновлено'])});
    if(ch.length)r.push({i:i,t:t,ch:ch})});
  return r}
function upList(r){
  return r.map(function(g){return'<div class="upg"><b>'+esc(g.t.n)+'</b><ul>'+g.ch.map(function(c){
    return'<li>'+(UPK[c[0].t]||'Урок')+(c[0].n?' «'+esc(c[0].n)+'»':'')+' — <span class="upw">'+c[1]+'</span></li>'}).join('')+'</ul></div>'}).join('')}
function upView(r){
  var prev=document.activeElement,o,V=null,R=null,gone=false;
  function kd(e){if(e.key==='Escape'||e.key==='Enter'){e.preventDefault();e.stopPropagation();close()}}
  function close(){if(gone)return;gone=true;document.removeEventListener('keydown',kd,true);snd('ok');
    agFlash(function(){if(V)V.stop();if(R)R.stop();o.remove();document.documentElement.classList.remove('crt-on');if(prev&&prev.focus)try{prev.focus({preventScroll:true})}catch(e){}})}
  o=document.createElement('div');o.className='crt on live agvw upvw'+(RM()?' rm':'');
  o.innerHTML='<div class="sc"><div class="sci"><canvas class="rain" aria-hidden="true"></canvas></div><i class="fx" aria-hidden="true"></i><canvas class="grn" aria-hidden="true"></canvas><i class="trk" aria-hidden="true"></i></div>'
    +'<div class="w98 w98top"><div class="w98w w98big" role="dialog" aria-modal="true" aria-labelledby="upvt"><div class="w98h"><span class="w98ic" aria-hidden="true"></span><b id="upvt">Обновление курса</b><button type="button" class="w98x w98cl" aria-label="Закрыть">×</button></div>'
    +'<div class="w98c"><div class="w98m"><span class="w98i" aria-hidden="true">i</span><p>С твоего прошлого захода в курсе кое-что поменялось. Вот где:</p></div>'
    +'<div class="w98txt" tabindex="0">'+upList(r)+'</div><div class="w98b"><button type="button" class="w98btn w98cl">OK</button></div></div></div></div>';
  document.body.appendChild(o);document.documentElement.classList.add('crt-on');snd('open');
  if(!RM()){V=vhsStart(o);R=rainStart(o.querySelector('.rain'))}
  o.querySelectorAll('.w98cl').forEach(function(b){b.onclick=close});
  document.addEventListener('keydown',kd,true);
  o.querySelector('.w98btn').focus({preventScroll:true})}
/* при заходе: ждём, пока уйдут вступление, соглашение, «долго не заходил» и прочие окна, затем сравниваем */
function upCheck(n){
  if(typeof DVPV!=='undefined'&&DVPV)return;
  if(document.querySelector('#crt,body>.w98,body>.bkt,.agvw,body>.modal')||!S.nick||!agOk()){if((n||0)<120)setTimeout(function(){upCheck((n||0)+1)},800);return}
  var m=upMap(),old=appGet().ch;appSet({ch:m});
  if(!old||typeof old!=='object')return;
  var r=upDiff(old);if(r.length)upView(r)}
(function(){var g0=greet;greet=function(){var r=g0.apply(this,arguments);setTimeout(upCheck,900);return r}})();
