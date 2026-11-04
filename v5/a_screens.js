/* ===================== ИТП 6 — экраны уроков, редактор, словарь, окна =====================
   Переопределяет экраны из базы (orig.html): логика (опыт, подсказки, черновики, проверка тестами)
   перенесена без изменений, поменялась только раскладка. Ничего о конкретных темах здесь не записано. */

/* --- переходы между экранами: направление объясняет, куда ты попал --- */
var SDEP={home:0,practice:0,editor:0,profile:0,greet:0,nick:0,place:0,settings:1,dict:1,codes:1,hole:1,theory:1,quiz:1,task:1,project:1,askq:1,rcode:1,skills:1,done:2,goal:2},PSKEY='';
function show(h,tab){
  cancelAnimationFrame(TYR);HRE=null;tocKill();CERR=0;
  document.removeEventListener('click',popOut,true);if(JIO){JIO.disconnect();JIO=null}
  var k=SKEY,d='';SKEY='';
  if(k&&PSKEY){
    if(k===PSKEY)d=/^(quiz|task|askq|rcode)$/.test(k)?'nx':'same';
    else{var a=SDEP[PSKEY],b=SDEP[k];if(a!==undefined&&b!==undefined)d=a===0&&b===0?'tab':b<a?'back':'fwd'}}
  /* переходы между экранами без звука (решение владельца) */
  PSKEY=k;
  document.querySelectorAll('body>.dock,body>.jump').forEach(function(x){x.remove()});
  app.innerHTML=h;app.className='';void app.offsetWidth;
  app.className='in'+(d?' '+d:'')+(app.querySelector('.dock')?' dk':'');
  /* док и кнопка «к текущему» живут прямо в body: #app анимируется через transform,
     а fixed внутри элемента с transform привязался бы к нему и прыгал при переходах */
  app.querySelectorAll('.dock,.jump').forEach(function(x){document.body.appendChild(x)});
  setNav(tab||null)}
function setNav(t){CURTAB=t||null;NAV.classList.toggle('on',!!t);NAV.inert=!t;NAV.querySelectorAll('button').forEach(function(b){var on=b.dataset.t===t;b.classList.toggle('act',on);if(on)b.setAttribute('aria-current','page');else b.removeAttribute('aria-current')})}
/* нижняя панель: те же четыре раздела, значки нарисованы кодом */
NAV.innerHTML=[['home','🗺️','Путь'],['pr','🎯','Практика'],['ed','💻','Код'],['prof','🐰','Профиль']].map(function(t){return'<button data-t="'+t[0]+'"><span class="ni" aria-hidden="true">'+t[1]+'</span>'+t[2]+'</button>'}).join('');
/* нажатие на вкладку уводит из кроличьей норы: «Путь» открывает сам Путь */
NAV.addEventListener('click',function(e){if(e.target.closest('button'))HOLE=-1},true);

/* --- окна: лист снизу на телефоне, карточка по центру на компьютере --- */
var MSIL=0;
function modal(h,btns){
  var prev=document.activeElement,o=document.createElement('div');o.className='modal';if(!MSIL)snd('open');MSIL=0;
  o.innerHTML='<div class="mc" role="dialog" aria-modal="true" tabindex="-1">'+h+'<div class="mb"></div></div>';
  var mc=o.querySelector('.mc'),r=o.querySelector('.mb'),t=mc.querySelector('h2');
  if(t){t.id=t.id||'mh'+Date.now();mc.setAttribute('aria-labelledby',t.id)}
  (btns||[]).forEach(function(b){var e=document.createElement('button');e.className='btn'+(b[2]?' g':'')+(b[3]?' dg':'');e.textContent=b[0];e.onclick=function(){if(b[1]&&b[1](o)===false)return;o.remove()};r.appendChild(e)});
  if(!r.children.length)r.remove();
  var gone=false;
  /* закрытие с анимацией: и кнопкой, и Esc, и «назад» на Android (они вызывают .remove()) */
  o.remove=function(){if(gone)return;gone=true;snd('close');o.classList.replace('modal','sheet-out');if(prev&&prev.focus&&document.body.contains(prev))try{prev.focus({preventScroll:true})}catch(e){}
    setTimeout(function(){Element.prototype.remove.call(o)},RM()?0:190)};
  o.onclick=function(e){if(e.target===o)o.remove()};
  o.addEventListener('keydown',function(e){if(e.key==='Enter'&&e.target.tagName==='INPUT'){e.preventDefault();var f=r.querySelector('button');if(f)f.click()}
    if(e.key==='Tab'){var f2=[].slice.call(mc.querySelectorAll('button:not([disabled]),input,textarea,[tabindex="0"]')).filter(function(x){return x.offsetParent});if(!f2.length)return;var a=f2[0],z=f2[f2.length-1];if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus()}}});
  /* лист можно смахнуть вниз */
  var y0=null,dy=0;
  mc.addEventListener('touchstart',function(e){y0=mc.scrollTop<=0?e.touches[0].clientY:null;dy=0},{passive:true});
  mc.addEventListener('touchmove',function(e){if(y0===null)return;dy=e.touches[0].clientY-y0;if(dy>0){mc.style.transition='none';mc.style.transform='translateY('+dy+'px)'}},{passive:true});
  mc.addEventListener('touchend',function(){if(y0===null)return;mc.style.transition='transform .22s cubic-bezier(.2,.8,.2,1)';if(dy>90)o.remove();else mc.style.transform='';y0=null});
  document.body.appendChild(o);
  setTimeout(function(){if(!mc.contains(document.activeElement))mc.focus({preventScroll:true})},30);
  return o}
/* меню действий: строки с значками вместо россыпи кнопок */
function actionSheet(title,items){
  var o=modal('<h2>'+esc(title)+'</h2><div class="lst acts">'+items.map(function(x,k){return'<button class="li'+(x[3]?' dg':'')+'" data-k="'+k+'"><span class="lic" aria-hidden="true">'+x[0]+'</span><span class="lt">'+esc(x[1])+(x[4]?'<small>'+esc(x[4])+'</small>':'')+'</span></button>'}).join('')+'</div>',[['Отмена',null,1]]);
  o.classList.add('as');o.querySelectorAll('.acts .li').forEach(function(b){b.onclick=function(){o.remove();items[+b.dataset.k][2]()}});return o}
/* окно термина: обычный текст абзацами, «Пример:» — кодом с отступами и кнопкой копирования, «Вывод:» — блоком вывода */
function termHtml(d){
  var L=String(d).split('\n'),h='',buf=[],i=0;
  function flush(){var t=buf.join('\n').replace(/^\n+|\n+$/g,'');buf=[];if(t)h+='<p style="font-weight:500">'+esc(t).replace(/\n/g,'<br>')+'</p>'}
  function code(a){if(a.length)h+='<div class="cpw"><button type="button" class="cp" aria-label="Копировать код"></button><pre>'+hl(a.join('\n'))+'</pre></div>'}
  function out(a){if(a.length)h+='<pre class="out">'+esc(a.join('\n'))+'</pre>'}
  while(i<L.length){
    var t=L[i].trim(),a=[];
    if(/^Пример:?$/.test(t)){
      flush();i++;
      while(i<L.length&&L[i].trim()!==''&&!/^Вывод:?($|\s)/.test(L[i].trim())){a.push(L[i]);i++}
      code(a);continue}
    if(/^Вывод:?($|\s)/.test(t)){
      flush();var one=t.replace(/^Вывод:?\s*/,'');i++;
      if(one)a.push(one);else while(i<L.length&&L[i].trim()!==''){a.push(L[i]);i++}
      h+='<div class="tvo">Вывод</div>';out(a);continue}
    buf.push(L[i]);i++}
  flush();return h}
function sheet(n,d){var c=fcol(n);modal('<h2><code'+(c?' style="color:'+c+'"':'')+'>'+esc(n)+'</code></h2>'+termHtml(d),[['Понятно']])}
/* эталон; why — строки «на чём держится решение» (у проекта это его подсказки), note — своя строка про опыт */
function solModal(sol,why,note){modal('<h2>Как это можно сделать</h2><pre class="cmp">'+hl(sol)+'</pre>'+(why&&why.length?'<p><b>На чём держится решение</b><br>'+why.map(esc).join('<br>')+'</p>':'')+'<p>Это один из вариантов. Если тесты прошли, твоё решение тоже верное.</p><p class="mu">'+(note||'Эталон не влияет на опыт.')+'</p>',[['Закрыть']])}
function askName(title,val,cb,max){
  modal('<h2>'+esc(title)+'</h2><input class="f n" id="mi" maxlength="'+(max||40)+'" value="'+esc(val)+'" autocomplete="off" aria-label="'+esc(title)+'">',[['Сохранить',function(o){var i=o.querySelector('#mi'),v=i.value.trim();if(!v){i.focus();return false}if(cb(v.slice(0,max||40))===false){i.focus();i.select();return false}}],['Отмена',null,1]]);
  setTimeout(function(){var i=$('mi');if(i){i.focus();i.select()}},40)}
function popup(t){var d=document.createElement('div');d.className='pop';d.setAttribute('aria-hidden','true');d.innerHTML='<span>⭐</span><b>'+esc(t)+'</b>';document.body.appendChild(d);snd([784,988,1175]);setTimeout(function(){d.remove()},1250)}

/* --- знакомство: ник, обращение, с чего начать --- */
function nick(){
  scr('nick','<div class="onb">'+rabbit('eat')+'<h1>Привет! Это ИТП</h1><p class="lead">«И так, программирование»: учим Python шаг за шагом, по островку в день.</p><label class="fld"><span>Как тебя зовут?</span><input class="f n" id="nk" maxlength="20" placeholder="Никнейм" autocomplete="off" autocapitalize="words" enterkeyhint="next"><small>Кролик будет приветствовать тебя по нику.</small></label><div class="fld" role="group" aria-labelledby="gq"><span id="gq">Как к тебе обращаться?</span><div class="seg2 gs"><button class="gb" data-g="m">Парень</button><button class="gb" data-g="f">Девушка</button><button class="gb" data-g="">Не указывать</button></div><small>Чтобы окончания в тексте были правильными.</small></div><button class="btn" id="go" disabled>Дальше</button></div>');
  var i=$('nk'),g=$('go'),gv=S.g||'';
  function gsel(){app.querySelectorAll('.gb').forEach(function(b){var on=b.dataset.g===gv;b.classList.toggle('on',on);b.setAttribute('aria-pressed',on)})}
  app.querySelectorAll('.gb').forEach(function(b){b.onclick=function(){gv=b.dataset.g;gsel();snd('click')}});gsel();
  i.oninput=function(){g.disabled=!i.value.trim()};
  i.onkeydown=function(e){if(e.key==='Enter'&&!g.disabled)g.click()};
  g.onclick=function(){S.nick=i.value.trim();S.g=gv;if(!S.reg)S.reg=day(new Date());save();place()};
  setTimeout(function(){if(!('ontouchstart' in window))i.focus()},300)}
function place(){
  var f=TOPICS[0]&&TOPICS[0].intro?1:0,h='<div class="onb" style="padding-top:6px"><h1>С чего начнём?</h1><p class="lead">Выбери первую тему, которую ещё не знаешь. Пропущенные можно пройти потом.</p></div>',n=0;
  TOPICS.forEach(function(t,i){if(t.intro||t.opt)return;n++;var z=i===f;h+='<button class="plc'+(z?' rec':'')+'" data-i="'+i+'"><span class="pn" aria-hidden="true">'+n+'</span><span class="pt">'+(z?'С нуля: ':'')+esc(t.n)+'<small>'+esc(t.s)+'</small></span>'+ico('chev','ch')+'</button>'});
  scr('place',h);
  app.querySelectorAll('.plc').forEach(function(b){b.onclick=function(){S.start=(+b.dataset.i===f?0:+b.dataset.i);save();greet()}})}

/* --- общие части урока --- */
function lessonTop(mid,right){return'<div class="top ls"><button class="icon" id="x" aria-label="Выйти из урока">'+ico('x')+'</button><div class="grow">'+(mid||'')+'</div>'+(right||'')+'</div>'}
/* главная кнопка урока живёт внизу, в зоне большого пальца */
function dockHtml(btns,inFlow,fb){return'<div class="dock" id="dock" role="region" aria-label="Действия"><div class="dki">'+(fb?'<div id="fb" class="fbx" aria-live="polite"></div>':'')+'<div class="dkb">'+btns+'</div></div></div>'}
function dockSet(btns){var b=document.querySelector('#dock .dkb');if(b){b.innerHTML=btns;var f=b.querySelector('button');if(f)setTimeout(function(){f.focus({preventScroll:true})},50)}}
function dockState(ok,title,html,mood){var d=$('dock'),f=$('fb');if(!d||!f)return;d.classList.remove('ok','bad');d.classList.add(ok?'ok':'bad');f.innerHTML='<div class="fh">'+(!ok&&mood?moodBox(mood):'<i aria-hidden="true">'+(ok?ico('check'):ico('x'))+'</i>')+title+'</div>'+(html?'<p>'+html+'</p>':'')+(!ok&&mood?'<p class="mq">'+moodLine(mood)+'</p>':'')}
/* нижняя панель урока не закрывает то, к чему прокручиваем (вывод, итог проверки, подсказку): её высота уходит в scroll-padding страницы */
var dockPad=function(){};
(function(){var R=document.documentElement,cur=null,ro=window.ResizeObserver?new ResizeObserver(sp):null;dockPad=sp;
  function sp(){var d=$('dock');if(d&&d.isConnected&&d.offsetHeight)R.style.setProperty('--dkh',d.offsetHeight+'px');else R.style.removeProperty('--dkh')}
  new MutationObserver(function(){var d=$('dock');if(d===cur)return;if(cur&&ro)ro.unobserve(cur);cur=d;if(d&&ro)ro.observe(d);sp()}).observe(app,{childList:true})})();
function fbSet(h){var f=$('fb');if(!f)return;f.innerHTML=h;if(h)requestAnimationFrame(function(){dockPad();var d=$('dock'),r=f.getBoundingClientRect(),lim=d&&!f.closest('#dock')?d.getBoundingClientRect().top-12:innerHeight-110;if(r.top>lim-60||r.bottom>lim)f.scrollIntoView({block:'nearest',behavior:RM()?'auto':'smooth'})})}
var OL='1234';
function optsHtml(q,ord){return'<div class="opts" role="group" aria-label="Варианты ответа">'+ord.map(function(k,n){return'<button class="opt" data-k="'+k+'" aria-pressed="false"><span class="ol" aria-hidden="true">'+(OL[n]||'')+'</span><span class="ot">'+esc(q.o[k])+'</span></button>'}).join('')+'</div>'}
/* выбор варианта: нажатием или цифрой на клавиатуре; Enter жмёт главную кнопку */
var OPTK=null;
function optKeys(os,sel){os.forEach(function(b){b.onclick=function(){sel(b)}});OPTK=function(n){var b=os[n];if(b&&!b.disabled&&b.isConnected){snd('tap');sel(b)}}}
document.addEventListener('keydown',function(e){
  if(e.ctrlKey||e.metaKey||e.altKey||document.querySelector('.modal'))return;
  var ty=/^(INPUT|TEXTAREA)$/.test((e.target&&e.target.tagName)||'');if(ty)return;
  if(/^[1-4]$/.test(e.key)&&OPTK&&app.querySelector('.opts')){e.preventDefault();OPTK(+e.key-1);return}
  if(e.key==='Enter'&&e.target===document.body){var g=document.querySelector('#dock .dkb .btn:not([disabled])');if(g&&app.querySelector('.opts')){e.preventDefault();g.click()}}});
/* v6.10.1: длинные условия (большие проекты) удобно читать с телефона: пункты разбираются на заголовки, которые можно
   сворачивать и разворачивать, примеры с кодом показываются блоками, а не текстом в строку */
var QLONG=700;
function qTitle(t){var k=t.indexOf(':');if(k>2&&k<=70)return[t.slice(0,k),t.slice(k+1).trim()||t];
  var d=t.search(/[.!?](\s|$)/);if(d>0&&d<=90&&t.slice(d+1).trim())return[t.slice(0,d+1),t.slice(d+1).trim()];
  return[t.slice(0,56).replace(/\s+\S*$/,'')+'…',t]}
/* 7.0: значения в «ёлочках» в условиях — точный текст вывода; показываем их моноширинным шрифтом на подложке */
function qfmt(t){return esc(t).replace(/«([^«»\n]{1,80})»/g,'«<span class="qv">$1</span>»')}
function condHtml(text,long){
  var L=String(text||'').split('\n').filter(function(x){return x.trim()});
  if(!long)return L.map(function(l){return'<p>'+qfmt(l)+'</p>'}).join('');
  var h='';
  L.forEach(function(l){
    var m=/^\s*(—\s*|\d+\)\s*)(.*)$/.exec(l);
    if(!m){h+='<p'+(/:\s*$/.test(l)?' class="qh"':'')+'>'+qfmt(l)+'</p>';return}
    var pre=m[1].indexOf(')')>0?m[1].trim()+' ':'',body=m[2];
    if(body.length<=110){h+='<p class="qi">'+qfmt(l)+'</p>';return}
    var t=qTitle(body);
    h+='<details class="qd"><summary>'+esc(pre+t[0])+'</summary><div class="qdb">'+qfmt(t[1])+'</div></details>'});
  return h}
/* 7.0: ввод и вывод примера — рядом, если обе колонки помещаются по самой длинной строке (ширина в знаках
   моноширинного шрифта), иначе друг под другом; решает сетка, а не JS, поэтому работает при любой ширине экрана */
function exIO(inp,out){var w=Math.max.apply(null,(inp==null?'':inp).split('\n').concat(out.split('\n')).map(function(l){return l.length}));
  return'<div class="exio" style="--exw:'+(Math.min(w,60)+3)+'ch">'+(inp!=null?'<div><p class="qlab">Ввод</p><pre class="cmp">'+esc(inp)+'</pre></div>':'')+'<div><p class="qlab">Вывод</p><pre class="cmp">'+esc(out)+'</pre></div></div>'}
function exHtml(ex,strict){
  var m=/^Проверка запустит:\n([\s\S]*?)\nВывод:\n([\s\S]*)$/.exec(String(ex||''));
  if(m)return'<p class="qlab">Проверка запустит такой код</p><pre class="cmp">'+esc(m[1])+'</pre><p class="qlab">и ждёт такой вывод</p><pre class="cmp">'+esc(m[2])+'</pre>';
  /* вход/вывод в несколько строк (таблицы, матрицы): блоками с равной шириной знаков, иначе пробелы схлопываются */
  var e2=/^(?:Вход:\n([\s\S]*?)\n)?Вывод:\n([\s\S]*)$/.exec(String(ex||''));
  if(e2&&!strict)return exIO(e2[1],e2[2]);
  return strict?'<pre class="cmp">'+esc(ex)+'</pre>':'<p>'+esc(ex).replace(/\n/g,'<br>')+'</p>'}
function qSec(title,body,open){return'<details class="qsec"'+(open?' open':'')+'><summary>'+title+'</summary><div class="qsb">'+body+'</div></details>'}
/* 7.0: кнопок «Развернуть всё / Свернуть всё» больше нет (владелец: лишнее) — каждый пункт раскрывается сам */
var QTB='';
function qBind(root){(root||document).querySelectorAll('.qtb button').forEach(function(b){b.onclick=function(){
  var on=b.dataset.q==='1',card=b.closest('.card,.tcard')||root;card.querySelectorAll('details').forEach(function(d){d.open=on});snd('click')}})}
/* 7.0: файлы рядом с программой (поле f задачи или проекта) — показываем ученику их содержимое */
function filesHtml(f){var fs=typeof fsOf==='function'?fsOf(f):(f&&typeof f==='object'?f:null);if(!fs)return'';var ks=Object.keys(fs).filter(function(n){return n.indexOf('_itp')!==0});if(!ks.length)return'';/* _itp_servers.json — служебный файл учебных серверов */return qSec('Файлы рядом с программой: '+ks.map(esc).join(', '),ks.map(function(n){return'<p class="qlab">'+esc(n)+'</p><pre class="cmp">'+esc(fs[n])+'</pre>'}).join(''),false)}
function taskCard(q,lab){
  var lg=String(q.q||'').length>QLONG||(String(q.q||'').length>330&&/\n/.test(q.q));
  var big=String(q.q||'').length>260;
  if(!big)return'<section class="tcard"><span class="ov">'+(lab||'Задание')+'</span><h2>'+qfmt(q.q)+'</h2>'+(q.ex?'<div class="pyex"><span>Пример</span>'+exHtml(q.ex,q.strict)+'</div>':'')+filesHtml(q.f)+'</section>';
  return'<section class="tcard lq"><span class="ov">'+(lab||'Задание')+'</span>'+(lg?QTB:'')+'<div class="tqt" role="heading" aria-level="2">'+condHtml(q.q,lg)+'</div>'+(q.ex?qSec('Пример',exHtml(q.ex,q.strict),true):'')+filesHtml(q.f)+'</section>'}
function edHtml(dc){return'<div class="ed"><div class="gt" aria-hidden="true"></div><div class="ew"><pre id="hl" aria-hidden="true"></pre><textarea id="code" wrap="off" spellcheck="false" autocapitalize="off" autocorrect="off" autocomplete="off" aria-label="Код"'+(KBD?' aria-describedby="edk"':'')+'>'+esc(dc)+'</textarea></div></div>'}
function runBtn(pri){return'<button class="btn s'+(pri?'':' g')+'" id="run" aria-keyshortcuts="Control+Enter">'+ico('play')+'Запустить</button>'}
IC.undo='<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>';
/* tpl — начальный код задания: рядом с «Запустить» кнопка вернуть его (7.0) */
function edCard(lab,dc,headL,tpl){return'<div class="edc"><div class="edh">'+(headL||'<span class="ov">'+lab+'</span>')+(tpl!==undefined?'<button class="icon rsb" type="button" data-tpl="'+esc(tpl)+'" aria-label="Вернуть начальный код" title="Вернуть начальный код">'+ico('undo')+'</button>':'')+runBtn()+'</div>'+edHtml(dc)+'</div>'+(KBD?'<p class="mu hint0" id="edk">Ctrl + Enter запускает код.</p>':'')}
function conHtml(){return'<section class="cons" id="cons" hidden aria-label="Вывод программы"><div class="csh"><span class="ov">Вывод</span><p class="mu rst" id="rst" hidden aria-live="polite"></p></div><pre class="out" id="o"></pre><div class="cmq" id="cmq" hidden></div>'+'<form class="inrow" id="ir" autocomplete="off"><input class="f" id="ii" placeholder="Ответ программе" aria-label="Ввод для программы" autocomplete="off" enterkeyhint="send"><button class="btn" id="ib" type="submit">Ввод</button></form></section>'}
var IOHTML=conHtml();
/* консоль показывается при первом запуске, пока её нет — не занимает место */
(function(){var lr=liveRun;liveRun=function(code){var c=$('cons');if(c)c.hidden=false;var q=$('cmq');if(q)q.hidden=true;var r=lr(code);consWatch();return r}})();
function runBind(c){
  $('run').onclick=function(){var o=$('o'),cs=$('cons');if(cs)cs.hidden=false;if(!SKOK){o.textContent='Загружаю среду Python…'}needSk().then(function(ok){if(ok)liveRun(c.value)});
    /* 7.0: вывод сразу в поле зрения — на телефоне он начинается ниже края экрана */
    if(cs)requestAnimationFrame(function(){try{cs.scrollIntoView({block:'nearest',behavior:RM()?'auto':'smooth'})}catch(e){}})}}
/* редактор растёт вместе с кодом: внутри нет второй прокрутки, только у страницы */
function initEd(c,cb){
  var ed=c.closest('.ed'),gt=ed.querySelector('.gt'),hh=c.previousElementSibling,pr={'(':')','[':']','{':'}','"':'"'},AP=String.fromCharCode(39);pr[AP]=AP;if(!ST('ac'))pr={};
  var sm={'«':'"','»':'"','“':'"','”':'"','„':'"','‘':AP,'’':AP},lastN=-1;
  function fit(){c.style.height='0px';var h=Math.max(ed.dataset.min?+ed.dataset.min:220,c.scrollHeight);c.style.height=h+'px'}
  function sync(){hh.innerHTML=hl(c.value)+'\n';var n=c.value.split('\n').length;if(n!==lastN){var g='';for(var z=1;z<=n;z++)g+=z+'\n';gt.textContent=g;lastN=n}fit();hh.scrollLeft=c.scrollLeft}
  function fire(){sync();if(cb)cb()}
  c.onscroll=function(){hh.scrollLeft=c.scrollLeft;c.scrollTop=0};
  c.onkeydown=function(e){if(e.key==='Tab'&&!e.shiftKey&&!e.ctrlKey&&!e.altKey){e.preventDefault();c.setRangeText('    ',c.selectionStart,c.selectionEnd,'end');fire()}};
  c.addEventListener('beforeinput',function(e){
    var p=c.selectionStart,q=c.selectionEnd,v=c.value,t=e.inputType,d=e.data;
    if(t==='insertLineBreak'||t==='insertParagraph'){e.preventDefault();var ls=v.lastIndexOf('\n',p-1)+1,ln=v.slice(ls,p),ind=ln.match(/^ */)[0];if(/:\s*$/.test(ln.split('#')[0]))ind+='    ';c.setRangeText('\n'+ind,p,q,'end');return fire()}
    if(t==='insertText'&&d&&d.length===1){
      if(ST('ac')&&p===q&&v[p]===d&&(d===')'||d===']'||d==='}'||d==='"'||d===AP)){e.preventDefault();c.selectionStart=c.selectionEnd=p+1;return}
      if(pr[d]&&!((d==='"'||d===AP)&&!qo(v,p))){e.preventDefault();c.setRangeText(d+v.slice(p,q)+pr[d],p,q,'end');c.selectionStart=c.selectionEnd=p+1+(q-p);return fire()}
    }
  });
  c.addEventListener('input',function(e){
    var p=c.selectionStart,ch=c.value[p-1];
    if(sm[ch]){c.setRangeText(sm[ch],p-1,p,'end');ch=sm[ch]}
    if(/^insert/.test(e.inputType||'')&&e.inputType!=='insertFromPaste'&&pr[ch]&&c.value[p]!==pr[ch]&&!((ch==='"'||ch===AP)&&!qo(c.value,p-1)))c.setRangeText(pr[ch],p,p,'start');
    fire();
  });
  window.addEventListener('resize',function rs(){if(!c.isConnected){window.removeEventListener('resize',rs);return}fit()});
  /* 7.0: вернуть начальный код — с вопросом, ведь черновик пропадёт */
  var rb=ed.parentNode.querySelector('.rsb');
  if(rb)rb.onclick=function(){if(c.value===rb.dataset.tpl)return;modal('<h2>Вернуть начальный код?</h2><p>Всё, что написано в редакторе, пропадёт.</p>',[['Вернуть',function(){c.value=rb.dataset.tpl;c.setSelectionRange(c.value.length,c.value.length);fire()},0,1],['Отмена',null,1]])};
  /* 7.0: полоска символов над клавиатурой телефона */
  function ins(k){
    var p=c.selectionStart,q=c.selectionEnd,v=c.value;
    if(k==='←'||k==='→'){var n=p!==q?(k==='←'?p:q):k==='←'?Math.max(0,p-1):Math.min(v.length,p+1);c.setSelectionRange(n,n);return kbCaret()}
    if(k==='⇥'){c.setRangeText('    ',p,q,'end');return fire()}
    if(k==='⇤'){var ls=v.lastIndexOf('\n',p-1)+1,m=v.slice(ls,ls+4).match(/^ */)[0].length;if(m){c.setRangeText('',ls,ls+m);c.setSelectionRange(Math.max(ls,p-m),Math.max(ls,q-m));fire()}return}
    if(ST('ac')&&p===q&&v[p]===k&&/^[)\]}"']$/.test(k)){c.setSelectionRange(p+1,p+1);return kbCaret()}
    if(pr[k]&&!((k==='"'||k===AP)&&!qo(v,p))){c.setRangeText(k+v.slice(p,q)+pr[k],p,q,'end');c.setSelectionRange(q+1,q+1);return fire()}
    c.setRangeText(k,p,q,'end');fire()}
  c.addEventListener('focus',function(){if(KBD)return;KB.c=c;KB.ins=ins;kbBar();kbPlace();setTimeout(kbPlace,400)});
  c.addEventListener('blur',function(){setTimeout(kbPlace,150)});
  c.addEventListener('input',function(){if(KB.c===c)requestAnimationFrame(kbCaret)});
  return sync}

/* Полоска одна на всё приложение и цепляется к редактору в фокусе. Высоту клавиатуры даёт visualViewport:
   всё, что ниже его края, закрыто. Пока пишешь, нижняя панель с «Проверить» прячется, полоска встаёт
   прямо над клавиатурой, а строка с курсором прокручивается так, чтобы оставаться над полоской. */
var KB={el:null,c:null,ins:null,q:false};
function kbBar(){
  if(KB.el)return KB.el;
  var nm={'⇥':'Отступ','⇤':'Убрать отступ','←':'Курсор влево','→':'Курсор вправо'};
  var b=document.createElement('div');b.className='kbar';b.hidden=true;
  /* над строкой символов — условие задачи: раскрывается кнопкой «Условие», клавиатура при этом не закрывается */
  b.innerHTML='<div class="kbq" id="kbq" hidden role="region" aria-label="Условие задачи"></div><div class="kbr" role="toolbar" aria-label="Символы для кода"><button type="button" tabindex="-1" data-k="cond" class="kx kq" aria-expanded="false" aria-controls="kbq">Условие</button>'+
   /* размер кода прямо отсюда (владелец): те же шаги, что в настройках «Размер кода» */
   '<button type="button" tabindex="-1" data-k="fz-" class="kx kz" aria-label="Код мельче">A−</button><button type="button" tabindex="-1" data-k="fz+" class="kx kz" aria-label="Код крупнее">A+</button>'+
   ['⇥','⇤','←','→','(',')',':','"',"'",'=','[',']','{','}','+','-','*','/','\\','%','<','>','#','_',',','.'].map(function(k){return'<button type="button" tabindex="-1" data-k="'+esc(k)+'"'+(nm[k]?' class="kx" aria-label="'+nm[k]+'"':'')+'>'+esc(k)+'</button>'}).join('')+'</div>';
  /* нажатие не должно забирать фокус у поля, иначе клавиатура закроется */
  b.addEventListener('pointerdown',function(e){e.preventDefault()});
  b.addEventListener('mousedown',function(e){e.preventDefault()});
  b.addEventListener('click',function(e){var t=e.target.closest('button');if(!t||!KB.ins||!KB.c)return;
    if(document.activeElement!==KB.c)KB.c.focus({preventScroll:true});
    if(t.closest('.kbq'))return;
    if(t.dataset.k==='cond'){kbCond(!KB.q);return}
    if(t.dataset.k==='fz-'||t.dataset.k==='fz+'){kbFz(t.dataset.k==='fz+'?1:-1);return}
    KB.ins(t.dataset.k);if(ST('vib')&&navigator.vibrate)navigator.vibrate(5)});
  document.body.appendChild(b);KB.el=b;
  if(window.visualViewport){visualViewport.addEventListener('resize',kbPlace);visualViewport.addEventListener('scroll',kbPlace)}
  return b}
var CFS=[11,13,15,17,19];
function kbFz(d){var i=CFS.indexOf(+ST('cf'));if(i<0)i=2;var n=Math.max(0,Math.min(CFS.length-1,i+d));
  if(n===i){toast(d>0?'Это самый крупный код':'Это самый мелкий код');return}
  S.set=S.set||{};S.set.cf=CFS[n];save();applyPrefs();if(KB.c)KB.c.dispatchEvent(new Event('input'));kbPlace()}
function kbPlace(){
  var b=KB.el,c=KB.c;if(!b)return;
  var on=!KBD&&!!ST('kbb')&&!!c&&c.isConnected&&document.activeElement===c,vv=window.visualViewport;
  b.hidden=!on;document.documentElement.classList.toggle('kbo',on);
  if(!on){kbCond(false);return}
  b.querySelector('.kq').hidden=!kbSrc();
  var kb=vv?Math.max(0,innerHeight-vv.height-vv.offsetTop):0;
  b.style.transform=kb?'translateY('+(-kb)+'px)':'';
  b.style.setProperty('--kbqh',Math.round((vv?vv.height:innerHeight)*.45)+'px');
  kbCaret()}
/* карточка условия на текущем экране: задание или цель проекта */
function kbSrc(){return app.querySelector('.tcard')||app.querySelector('.pj .card')}
function kbCond(open){
  var b=KB.el;if(!b)return;var p=b.querySelector('.kbq'),t=b.querySelector('.kq'),s=kbSrc();
  if(open&&!s)open=false;
  KB.q=!!open;p.hidden=!open;t.setAttribute('aria-expanded',open?'true':'false');t.classList.toggle('on',!!open);
  if(!open){p.innerHTML='';return}
  var k=s.cloneNode(true);k.querySelectorAll('[id]').forEach(function(x){x.removeAttribute('id')});
  p.innerHTML='';p.appendChild(k);qBind(p);p.scrollTop=0;kbCaret()}
function kbCaret(){
  var c=KB.c,b=KB.el;if(!c||!b||b.hidden)return;
  var vv=window.visualViewport,cs=getComputedStyle(c),lh=parseFloat(cs.lineHeight)||24,pt=parseFloat(cs.paddingTop)||12;
  var ln=c.value.slice(0,c.selectionEnd).split('\n').length-1,y=c.getBoundingClientRect().top+pt+ln*lh;
  var top=(vv?vv.offsetTop:0)+76,bot=(vv?vv.offsetTop+vv.height:innerHeight)-b.offsetHeight-14;
  if(y+lh>bot)scrollBy(0,y+lh-bot);else if(y<top)scrollBy(0,y-top)}

/* --- итог островка: что получил, сколько опыта, куда дальше --- */
/* U1-10: время прохождения островка — с первого захода в него (в памяти; после перезагрузки страницы отсчёт начнётся заново) */
var ISLT={k:'',t:0};
function islStart(k){if(ISLT.k!==k)ISLT={k:k,t:Date.now()}}
function islTime(k){var r=ISLT.k===k?Math.round((Date.now()-ISLT.t)/1000):-1;ISLT={k:'',t:0};return r}
function fmtTm(s){var m=Math.floor(s/60),h=Math.floor(m/60);return h?h+':'+pad2(m%60)+':'+pad2(s%60):m+':'+pad2(s%60)}
/* точность: доля верных попыток (n заданий или вопросов, err ошибок) */
function accOf(n,err){return n>0?Math.round(n/(n+(err||0))*100):-1}
function doneScreen(o){
  var many=o.err>=ROLL_AT,acc=o.acc>=0?o.acc:-1,tm=o.tm>=0?o.tm:-1;
  /* плитки как в Duolingo: опыт, точность, время — появляются по очереди */
  var tl='<div class="xpt x dt" id="xpt"><small>Опыт</small><b>⭐ <span id="xpn">+0</span></b></div>'+
   (acc>=0?'<div class="xpt ac dt"><small>Точность</small><b>🎯 <span class="cnt" data-v="'+acc+'" data-f="p">'+acc+'%</span></b></div>':o.err!==undefined?'<div class="xpt dt"><small>Ошибок</small><b>'+o.err+'</b></div>':'')+
   (tm>=0?'<div class="xpt tmr dt"><small>Время</small><b>⏰ <span class="cnt" data-v="'+tm+'" data-f="t">'+fmtTm(tm)+'</span></b></div>':'');
  var h='<div class="fin">'+rabbit(many?'rolled':(o.mood||(o.err===0?'cool':'happy')))+'<h1>'+o.title+'</h1>'+(many?'<p class="lead">Непростой островок: ошибок было много. Но он пройден, а ошибки разобраны.</p>':o.lead?'<p class="lead">'+o.lead+'</p>':'')+
   '<div class="xpr">'+tl+'</div>'+
   (o.bonus?'<p class="note2">'+o.bonus+'</p>':'')+(o.note?'<p class="note2">'+esc(o.note)+'</p>':'')+
   (o.tj?'<div class="tj">🎉 Тема «'+esc(o.tj)+'» пройдена!</div>':'')+(o.lv?'<div><span class="lvup">⬆️ Новый уровень: '+o.lv+'</span></div>':'')+
   xpStrip(o.x)+'</div>';
  scr('done',h+dockHtml(o.btns,1));
  /* звук в такт анимации: «пройдено» в момент появления экрана, искорка опыта в момент, когда число начинает расти;
     тема пройдена или новый уровень звучат через конфетти (там нужный звук выбирает SX.cs) */
  SX.cs=o.tj?'fanfare':(o.lv?'level':'');setTimeout(function(){SX.cs=''},1500);
  if(!o.tj&&!o.lv&&!sndRecent('fanfare',600))snd('done');
  var n=$('xpn'),t=$('xpt'),x=o.x||0,ts=app.querySelectorAll('.xpr .dt');
  if(RM()){ts.forEach(function(e){e.classList.add('in')});n.textContent='+'+x;if(x>0)setTimeout(function(){snd('xpt',{k:0})},260)}
  else ts.forEach(function(e,k){setTimeout(function(){if(!e.isConnected)return;e.classList.add('in');
    if(k===0){if(!x){n.textContent='+0';return}
      /* опыт «набегает» числом */
      var t0=0,xt=xpTick();t.classList.add('pp');requestAnimationFrame(function st(q){if(!t0)t0=q;var kk=Math.min(1,(q-t0)/650),vv=Math.round(x*(1-Math.pow(1-kk,3)));n.textContent='+'+vv;xt(vv);if(kk<1&&n.isConnected)requestAnimationFrame(st)});sparks(t)}
    else{snd('pet');
      /* точность и время тоже «набегают» числом, как опыт */
      var c=e.querySelector('.cnt');if(c){var v=+c.dataset.v,f=c.dataset.f,t1=0,fm=function(z){return f==='t'?fmtTm(z):z+'%'};c.textContent=fm(0);
        requestAnimationFrame(function st2(q){if(!t1)t1=q;var kk=Math.min(1,(q-t1)/600),vv=Math.round(v*(1-Math.pow(1-kk,3)));c.textContent=fm(vv);if(kk<1&&c.isConnected)requestAnimationFrame(st2)})}}},300+k*520)});
  /* потом заполняется полоса уровня */
  xpStripRun();
  /* U1-8, U1-9: после итога — экран цели дня и (один раз) выбор цели серии; главная кнопка сначала ведёт туда.
     Свой onclick кнопка получает сразу после doneScreen, поэтому оборачиваем его на следующем шаге */
  setTimeout(function(){var gb=$('go');if(!gb)return;var f=gb.onclick;gb.onclick=function(e){if(GOALP||sgAsk())postDone(function(){if(f)f.call(gb,e)});else if(f)f.call(gb,e)}},0);
  var b=document.querySelector('#dock .btn');if(b)setTimeout(function(){b.focus({preventScroll:true})},60)}
/* очередь после итога островка: выбор цели серии → цель дня (уже с полосой выбранной цели) → куда шёл ученик */
function postDone(then){
  if(sgAsk())return sgChooser(function(){postDone(then)});
  if(GOALP){GOALP=0;return goalScreen(function(){postDone(then)})}
  if(skNew())return skPop(then);
  then()}
/* выбор цели серии спрашиваем после 2-го пройденного островка (вступление не считается) и после каждой достигнутой цели */
function islN(){var n=0;for(var k in S.d){var i=+k.split('-')[0];if(TOPICS[i]&&!TOPICS[i].intro&&/^\d+-\d+$/.test(k))n++}return n}
function sgAsk(){return!!S.sg&&!S.sg.a&&!S.sg.n&&islN()>=2}
/* как в Duolingo: строки со сроком и словом про него, выбранная — с рамкой акцента; опыт — тихой подписью справа */
var SGW={7:'Хорошее начало',14:'Уже привычка',30:'Месяц подряд',50:'Железная воля'};
function sgChooser(then){
  S.sg.a=1;save();
  var nx=SGN.filter(function(n){return n>(S.sg.ok||0)})[0]||SGN[SGN.length-1],cur=S.sg.n||nx,gl=S.goal,re=S.sg.ok&&!S.sg.n;
  var m=modal('<div class="sgc"><h2>'+(re?'Новая цель серии':'Цель серии')+'</h2><p class="mu">'+(re?'Ты '+G('продержался','продержалась','продержался')+' '+S.sg.ok+' '+pl(S.sg.ok,['день','дня','дней'])+' подряд. Сколько дальше?':'Сколько дней подряд будешь заниматься? Дойдёшь — получишь опыт, и чем дольше серия, тем больше.')+'</p>'+
   '<div class="sgo" role="radiogroup" aria-label="Цель серии">'+SGN.map(function(n){return'<button role="radio" class="sgr" data-n="'+n+'" aria-checked="'+(n===cur)+'"><b>'+n+' '+pl(n,['день','дня','дней'])+'</b><span>'+SGW[n]+'</span><small>+'+SGX[n]+' опыта</small></button>'}).join('')+'</div>'+
   '<p class="sgl">Островков в день</p>'+SG('goal',[[1,'1'],[2,'2'],[3,'3']],gl)+'</div>',
   [['Готово',function(){S.sg.n=cur;S.goal=gl;save()}],['Позже',null,1]]);
  segInit(m);
  m.querySelectorAll('.sgr').forEach(function(b){b.onclick=function(){cur=+b.dataset.n;m.querySelectorAll('.sgr').forEach(function(x){x.setAttribute('aria-checked',x===b?'true':'false')});snd('click')}});
  m.querySelectorAll('.segc button').forEach(function(b){b.onclick=function(){var g=b.parentNode;g.querySelectorAll('button').forEach(function(x){var on=x===b;x.classList.toggle('on',on);x.setAttribute('aria-checked',on?'true':'false')});gl=+b.dataset.v;snd('click');segPos(g,true)}});
  /* окно закрыли любым способом — идём дальше */
  var rm=m.remove;m.remove=function(){rm.call(m);if(then){var f=then;then=null;setTimeout(f,RM()?0:200)}};
  return m}
/* U1-8: цель дня выполнена — морковка вместо огонька, сколько дней подряд, неделя с отметками */
function goalScreen(then){
  var s=streakNow(),sg=S.sg&&S.sg.n;
  var h='<div class="gday">'+rbSay(G('Ты справился','Ты справилась','Цель дня выполнена')+'. Встретимся завтра')+
   '<div class="gst"><b class="gnum">'+s+'</b><span class="gcar" aria-hidden="true">🥕</span></div><p class="glab">'+pl(s,['день','дня','дней'])+' подряд</p>'+
   weekRow('a')+
   (sg?'<div class="gsg"><div class="bar" role="progressbar" aria-valuemin="0" aria-valuemax="'+sg+'" aria-valuenow="'+Math.min(s,sg)+'" aria-label="Цель серии"><i style="width:'+Math.min(100,Math.round(s/sg*100))+'%"></i></div><span class="mu">Цель серии: '+Math.min(s,sg)+' из '+sg+', за неё +'+SGX[sg]+' опыта</span></div>':'')+
   '</div>';
  scr('goal',h+dockHtml('<button class="btn" id="gz">Закрыть</button><button class="btn t" id="gsh">'+phi('share-network')+'Поделиться</button>',1));
  snd('streak');vib([20,30,20]);
  $('gz').onclick=function(){then()};$('gsh').onclick=share}
function sparks(el){
  var r=el.getBoundingClientRect(),cols=['var(--gold)','var(--carrot)','var(--accent)','#fff'];
  for(var k=0;k<14;k++){var s=document.createElement('i');s.style.cssText='position:fixed;z-index:31;left:'+(r.left+r.width/2)+'px;top:'+(r.top+r.height/2)+'px;width:7px;height:7px;margin:-3.5px;border-radius:2px;pointer-events:none;background:'+cols[k%4];document.body.appendChild(s);
    var a=k/14*6.283+Math.random()*.4,d=50+Math.random()*50;
    (function(s){s.animate([{transform:'translate(0,0) rotate(0) scale(1)',opacity:1},{transform:'translate('+Math.cos(a)*d+'px,'+(Math.sin(a)*d-20)+'px) rotate('+(Math.random()*360)+'deg) scale(.4)',opacity:0}],{duration:700+Math.random()*300,easing:'cubic-bezier(.2,.8,.3,1)'}).onfinish=function(){s.remove()}})(s)}}

/* --- теория --- */
function theory(i,j){if(window.pyWarm)setTimeout(pyWarm,1200);
  var it=IT(i,j),T={},fresh=!S.d[i+'-'+j],rm=RM();(it.terms||[]).forEach(function(x){T[x.n]=x});
  var h=it.html.split(/(<pre[^>]*>[\s\S]*?<\/pre>)/).map(function(p){return /^<pre /.test(p)?p:/^<pre>/.test(p)?'<div class="cpw"><button type="button" class="cp" aria-label="Копировать код"></button><pre>'+hl(p.slice(5,-6))+'</pre></div>':p.replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,function(m,n,l){return T[n]?'<button class="term'+(fcol(n)?' fn':'')+'"'+(fcol(n)?' style="color:'+fcol(n)+'"':'')+' data-n="'+esc(n)+'" aria-haspopup="dialog">'+(l||esc(n))+'</button>':(l||esc(n))})}).join('');
  scr('theory',lessonTop('<div class="rprog" role="progressbar" aria-label="Прочитано" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><i id="rpb"></i></div>','<span class="lstep">≈ '+readMin(it)+' мин</span>')+'<article class="th"><p class="ov tov">'+esc(TOPICS[i].n)+'</p><h1 class="tt">'+esc(it.n)+'</h1><div id="tb">'+h+'</div><p class="mu tm" id="tm">'+(fresh&&!rm&&ST('ty')?TMSK:TMT)+'</p></article><button class="btn" id="go">'+(S.d[i+'-'+j]?'Готово':G('Я прочитал','Я прочитала','Прочитано')+', открыть дальше')+'</button>');
  $('x').onclick=goBack;qBind(app);
  app.querySelectorAll('.term').forEach(function(b){b.onclick=function(){var x=T[b.dataset.n];sheet(x.n,x.d)}});
  $('go').onclick=function(){var w=tdone(i);if(!S.d[i+'-'+j]){snd('theory');bump(i+'-'+j)}if(TOPICS[i].intro&&!w&&tdone(i)&&S.start===0){reveal();return}if(TOPICS[i].intro&&(S.start>0||w)){goBack();if(!w)toast('Готово. Эта кнопка больше не нужна и пропала из профиля');return}
    /* U1-8: цель дня выполнена теорией — сначала её экран */
    postDone(function(){home();if(!w&&tdone(i)){toast('🎉 Тема «'+TOPICS[i].n+'» пройдена!');confetti(allDone()?2:1)}})};
  if(window.TW)TW.scan(app);
  tocBuild();if(fresh&&!rm&&ST('ty'))typeIn($('tb'),$('tm'));
  readProg()}
/* полоска в шапке теории: сколько уже прочитано. Короткий урок (страница не прокручивается) считается прочитанным
   целиком, но только когда текст допечатан: во время печати страница короткая лишь потому, что текста ещё нет
   (typeIn вешает на #tb класс noemo, пока печатает) */
var RPS=null;
function readProg(){
  if(RPS)window.removeEventListener('scroll',RPS);
  var b=$('rpb');if(!b)return;var bar=b.parentNode,lp=-1,fin=0,tb=$('tb');
  RPS=function(){if(!b.isConnected){window.removeEventListener('scroll',RPS);RPS=null;return}var ty=tb&&tb.classList.contains('noemo'),mx=document.documentElement.scrollHeight-innerHeight,p=mx>8?Math.min(100,Math.round(window.scrollY/mx*100)):(fin&&!ty?100:0);if(p!==lp){lp=p;b.style.width=p+'%';bar.setAttribute('aria-valuenow',p)}};
  window.addEventListener('scroll',RPS,{passive:true});if(window.ResizeObserver){var ro=new ResizeObserver(function(){if(!b.isConnected||!RPS){ro.disconnect();return}RPS()});ro.observe(document.body)}
  /* печать закончилась (или её допечатали касанием) — пересчитать */
  if(tb&&window.MutationObserver){var mo=new MutationObserver(function(){if(!b.isConnected||!RPS){mo.disconnect();return}if(!tb.classList.contains('noemo')){mo.disconnect();RPS()}});mo.observe(tb,{attributes:true,attributeFilter:['class']})}
  setTimeout(function(){if(RPS)RPS()},60);setTimeout(function(){fin=1;if(RPS)RPS()},700)}

/* --- вопросы --- */
function quiz(i,j){
  var key=i+'-'+j,Ql=IT(i,j).q,tot=Ql.length,D=S.dr[key],first=!S.at[key];islStart(key);
  var idx=[],st=Ql.map(function(){return 0}),ph=0,er=0,nx=0,cb=0,bon=0;
  if(D&&D.kind==='q'&&D.st&&D.st.length===tot){idx=D.qs.filter(function(x){return x<tot});st=D.st.split('').map(Number);ph=D.ph;er=D.er;nx=D.nx}
  if(!idx.length){idx=Ql.map(function(x,n){return n});st=st.map(function(){return 0});ph=0;er=0;nx=0}
  function save2(){S.dr[key]={kind:'q',qs:idx.slice(),st:st.join(''),ph:ph,er:er,nx:nx};save()}
  function segs(){return st.map(function(v,n){return'<i class="'+(v===1?'ok':v===2?'bad':n===idx[0]&&!ph?'cu':'')+'"></i>'}).join('')}
  function finish(){
    var tj0=tdone(i);rec(key,er);bump(key);
    var a=award(key,20,nx?99:er,first&&!nx?bon:0,1);
    if(nx&&a.x)a.note='Повторная ошибка, поэтому только +2. Опыт за островок даётся один раз, а тренироваться можно сколько угодно.';
    var tj=!tj0&&tdone(i);
    doneScreen({title:'Островок пройден',lead:er?'Ошибки разобраны, двигаемся дальше.':'Без единой ошибки!',err:er,acc:accOf(tot,er),tm:islTime(key),x:a.x,bonus:!nx&&first&&bon&&er<=3?'Бонус за серию верных ответов: +'+bon+' ⭐':'',note:a.note,tj:tj?TOPICS[i].n:'',lv:a.lv,btns:'<button class="btn" id="go">Дальше</button>'+(nx?'<button class="btn t" id="rp">Пройти заново</button>':'')});
    $('go').onclick=goBack;if(nx)$('rp').onclick=function(){quiz(i,j)};
    if(tj||a.lv)confetti(tj&&allDone()?2:1)}
  function nextq(){
    if(!idx.length){
      var bad=[];st.forEach(function(v,n){if(v===2)bad.push(n)});
      if(!ph&&bad.length){ph=1;idx=bad;save2();return nextq()}
      return finish()}
    save2();
    var q=Ql[idx[0]],qi=idx[0],sel=-1,ch=false,right=false,ord=q.o.map(function(x,n){return n});
    if(ph)ord.sort(function(){return Math.random()-.5});
    var h=lessonTop('<div class="sbar" id="sb" role="img" aria-label="Отвечено '+st.filter(Boolean).length+' из '+tot+'">'+segs()+'</div>')+'<h1 class="sr-only">'+esc(IT(i,j).n||'Вопросы')+'</h1>'+(ph?'<div class="qph">🔁 Работа над ошибками</div>':'')+'<h2 class="q">'+qfmt(q.q)+'</h2>'+(q.v||'')+(q.c?'<pre>'+hl(q.c)+'</pre>':'')+optsHtml(q,ord);
    scr('quiz',h+dockHtml('<button class="btn" id="go" disabled>Проверить</button>',0,1));if(q.v)imgZoom(app);
    $('x').onclick=goBack;
    var g=$('go'),os=app.querySelectorAll('.opt');
    optKeys(os,function(b){if(ch)return;sel=+b.dataset.k;os.forEach(function(o){o.classList.remove('sel');o.setAttribute('aria-pressed','false')});b.classList.add('sel');b.setAttribute('aria-pressed','true');g.disabled=false});
    g.onclick=function(){
      if(ch){idx.shift();return nextq()}
      ch=true;right=sel===q.a;
      if(right){st[qi]=1;cb++}else{st[qi]=2;er++;cb=0;if(ph)nx=1}
      fx(right);$('sb').innerHTML=segs();
      os.forEach(function(o){var k=+o.dataset.k;o.disabled=true;if(right&&k===q.a)o.classList.add('ok');else if(k===sel&&!right)o.classList.add('no');else if(!right&&k===q.a)o.classList.add('ok')});
      if(right)dockState(true,'Верно!',esc(q.e||'')+xm(q));
      else if(ph)dockState(false,'Снова неверно',esc(q.e||'')+xm(q)+'<br><span class="mu">За этот островок будет только +2 опыта. Потренироваться можно и позже, но опыт даётся один раз.</span>');
      else dockState(false,'Неверно',esc(q.e||'')+xm(q)+'<br><span class="mu">Этот вопрос вернётся в конце островка.</span>',errMood(er));
      if(right&&cb>=5){if(first&&!nx)bon+=2;popup(first&&!nx?'+2 ⭐ опыта':'Серия ×'+cb)}
      g.textContent='Дальше';g.focus({preventScroll:true})}}
  nextq()}

/* --- телефон боком (владелец): в заданиях с кодом и проектах условие слева, код справа, границу между ними можно двигать.
   Разметка одна на все положения: условие и подсказка — в .spa, редактор, вывод и ответ проверки — в .spb. Стоймя и на
   широком экране обёртки «прозрачные» (display:contents), и экран такой же, как был; телефон боком (низкий экран в
   горизонтальной ориентации, CSS) — две колонки, каждая прокручивается сама. Граница — палец/мышь или стрелки, ширина
   левой колонки запоминается (itp-app spl, в процентах) */
var SPLQ=matchMedia('(orientation:landscape) and (max-height:540px) and (min-width:600px)');
function splitOn(){return SPLQ.matches&&!!app.querySelector('.spl')}
/* телефон боком весь экран — две колонки (владелец: верхняя лента и широкая «Проверить» съедали почти всё): шапка урока
   (крестик, полоска заданий, подсказка) переезжает тонкой строкой в верх левой колонки, панель с «Проверить» — компактной
   строкой под редактор в правую. Стоймя — всё обратно на свои места. Высоту колонок задаёт CSS (экран — колонка flex) */
function splitFit(){var sp=app.querySelector('.spl');if(!sp)return;var a=sp.querySelector('.spa'),b=sp.querySelector('.spb'),d=$('dock'),t=app.querySelector('.top.ls')||sp.querySelector('.top.ls');
  if(SPLQ.matches){window.scrollTo(0,0);if(d&&d.parentNode!==b)b.appendChild(d);if(t&&t.parentNode!==a)a.insertBefore(t,a.firstChild)}
  else{if(d&&d.parentNode===b)app.appendChild(d);if(t&&t.parentNode===a)app.insertBefore(t,app.firstChild)}}
function splitSet(sp,v){v=Math.max(25,Math.min(75,Math.round(v)));sp.style.setProperty('--spl',v+'%');var h=sp.querySelector('.sph');if(h)h.setAttribute('aria-valuenow',v);return v}
function splitWrap(){
  var l=app.querySelector('.tcard,.pj'),e=app.querySelector('.edc');if(!l||!e)return;
  var sp=document.createElement('div'),a=document.createElement('div'),b=document.createElement('div'),h=document.createElement('div');
  sp.className='spl';a.className='spa';b.className='spb';h.className='sph';
  h.setAttribute('role','separator');h.setAttribute('aria-orientation','vertical');h.setAttribute('aria-label','Граница между условием и кодом');h.setAttribute('aria-valuemin','25');h.setAttribute('aria-valuemax','75');h.tabIndex=0;
  l.parentNode.insertBefore(sp,l);
  [$('tip0'),l,$('hint')].forEach(function(x){if(x)a.appendChild(x)});
  [e,$('cons'),app.querySelector('div#fb')].forEach(function(x){if(x&&x.parentNode!==b&&!x.closest('.dock'))b.appendChild(x)});
  sp.appendChild(a);sp.appendChild(h);sp.appendChild(b);app.classList.add('spw');
  var v=+appGet().spl||45;v=splitSet(sp,v);
  function save(){appSet({spl:v})}
  h.addEventListener('pointerdown',function(ev){if(!splitOn())return;ev.preventDefault();h.setPointerCapture(ev.pointerId);h.classList.add('drag');
    var r=sp.getBoundingClientRect();
    function mv(m){v=splitSet(sp,(m.clientX-r.left)/r.width*100)}
    function up(){h.classList.remove('drag');h.removeEventListener('pointermove',mv);h.removeEventListener('pointerup',up);h.removeEventListener('pointercancel',up);save()}
    h.addEventListener('pointermove',mv);h.addEventListener('pointerup',up);h.addEventListener('pointercancel',up)});
  h.addEventListener('keydown',function(ev){var d=ev.key==='ArrowLeft'?-5:ev.key==='ArrowRight'?5:0;if(!d)return;ev.preventDefault();v=splitSet(sp,v+d);save()});
  requestAnimationFrame(splitFit)}
window.addEventListener('resize',function(){if(app.querySelector('.spl'))splitFit()});
try{SPLQ.addEventListener('change',function(){if(app.querySelector('.spl'))setTimeout(splitFit,60)})}catch(e){}

/* --- задания с кодом --- */
function task(i,j,k){
  var it=IT(i,j),T=it.tasks,q=T[k],key=i+'-'+j,tk=key+'-'+k;islStart(key);
  var dc=((S.dr[key]||{}).codes||{})[k]||(S.tk[tk]?'':'# Пиши код здесь\n'+(q.starter||''));
  /* полоска заданий: на решённое задание (и на первое нерешённое) можно перейти — взять прошлый код или ещё раз
     посмотреть, как задумано */
  var fu=T.findIndex(function(x,n){return!S.tk[key+'-'+n]});if(fu<0)fu=T.length-1;
  var dots='<div class="sbar" role="group" aria-label="Задание '+(k+1)+' из '+T.length+'">'+T.map(function(x,n){var ok=S.tk[key+'-'+n],go=n!==k&&(ok||n===fu);
    return'<button type="button" class="'+(ok?'ok':'')+(n===k?' cu':'')+'" data-n="'+n+'"'+(go?' title="Задание '+(n+1)+'"':' disabled')+' aria-label="Задание '+(n+1)+(ok?', решено':'')+'"'+(n===k?' aria-current="step"':'')+'></button>'}).join('')+'</div>';
  scr('task',lessonTop(dots,'<span class="lstep" aria-hidden="true">'+(k+1)+' / '+T.length+'</span>'+(q.h?'<button class="icon hbe" id="hb" aria-label="Подсказка (опыт будет вдвое меньше)" aria-keyshortcuts="Control+H">'+phi('lightbulb','hbl')+'</button>':''))+'<h1 class="sr-only">'+esc(it.n||'Задания с кодом')+', задание '+(k+1)+' из '+T.length+'</h1>'+(k>0&&!S.tp&&S.tk[key+'-'+(k-1)]?'<div class="tip0" id="tip0" role="note"><span>Решённое задание можно открыть снова: нажми на его полоску сверху. Там твой код и «как задумано».</span><button class="btn t" id="tip0b">Понятно</button></div>':'')+taskCard(q)+'<div id="hint"></div>'+edCard('Решение',dc,0,'# Пиши код здесь\n'+(q.starter||''))+conHtml()+'<div id="fb" aria-live="polite"></div>'+dockHtml('<button class="btn" id="chk">Проверить</button>'));
  splitWrap();$('x').onclick=goBack;
  if($('tip0')){S.tp=1;save();$('tip0b').onclick=function(){var t=$('tip0');if(t)t.remove()}}
  app.querySelectorAll('.top .sbar button[data-n]').forEach(function(b){b.onclick=function(){if(!b.disabled)task(i,j,+b.dataset.n)}});
  var c=$('code'),sync=initEd(c,function(){drc(i,j,k).codes[k]=c.value.slice(0,3000);lazySave()});sync();
  /* вернулись к уже решённому заданию: сразу «дальше» и эталон; «Проверить» появляется, только когда код изменили (U1-1) */
  if(S.tk[tk]){var nl=k+1>=T.length,c0=c.value;dockSet('<button class="btn g" id="chk" hidden>Проверить</button><button class="btn" id="nx">'+(fu>k&&fu!==k?'К заданию '+(fu+1):nl?'Завершить':'Следующее задание')+'</button>'+(q.sol?'<button class="btn t" id="sl">Посмотреть, как задумано</button>':''));
    c.addEventListener('input',function(){var b=$('chk');if(b&&b.classList.contains('g'))b.hidden=c.value===c0});
    $('nx').onclick=function(){fu>k?task(i,j,fu):nl?end(i,j):task(i,j,k+1)};if(q.sol)$('sl').onclick=function(){solModal(q.sol)}}
  function showHint(){var hb=$('hb');if(hb)hb.classList.add('on');$('hint').innerHTML='<div class="fb"><b>Подсказка</b>'+hintTx(q.h)+'<br><span class="mu">Опыт за это задание: 50% от максимума.</span></div>'}
  if(q.h){
    if(HINT)showHint();
    $('hb').onclick=function(){
      if(HINT){showHint();$('hint').scrollIntoView({block:'nearest',behavior:RM()?'auto':'smooth'});return}
      var use=function(){S.hc=1;S.hu[i]=1;HINT=1;snd('hint');drc(i,j,k);save();showHint();$('hint').scrollIntoView({block:'nearest',behavior:RM()?'auto':'smooth'})};
      if(S.hc)use();else modal('<h2>Взять подсказку?</h2><p>С подсказкой опыт за это задание будет вдвое меньше.</p><p class="mu">Больше спрашивать не будем. Вернуть вопрос можно в настройках.</p>',[['Взять подсказку',use],['Отмена',null,1]])}}
  skReady();chkPulse();runBind(c);
  $('chk').onclick=async function(){
    if(!SKOK)fbSet('<div class="fb"><b>Загружаю среду Python…</b></div>');
    if(!(await needSk()))return;
    var b=$('chk');b.disabled=true;
    var v=await judge(q,c.value);
    if(!v.ok){ERR++;drc(i,j,k);save();fx(false);b.disabled=false;fbSet(badFb(v.h,errMood(ERR)));return}
    fx(true,'test');
    if(!S.tk[tk]){S.tk[tk]=1;save()}
    var last=k+1>=T.length;
    var self=!ERR&&!HINT;
    fbSet('<div class="fb">'+(self?moodBox('wowhead','fl'):'')+'<b>Все тесты пройдены!</b>'+(self?'Сам, с первой попытки и без подсказки.':'Кролик получил корм 🥕')+'</div>');
    var sb=app.querySelector('.top .sbar [data-n="'+k+'"]');if(sb){sb.className='ok cu';sb.setAttribute('aria-label','Задание '+(k+1)+', решено')}
    dockSet('<button class="btn" id="nx">'+(last?'Завершить':'Следующее задание')+'</button>'+(q.sol?'<button class="btn t" id="sl">Посмотреть, как задумано</button>':''));
    $('nx').onclick=function(){last?end(i,j):task(i,j,k+1)};
    if(q.sol)$('sl').onclick=function(){solModal(q.sol)}}}
function end(i,j){
  var key=i+'-'+j,tj0=tdone(i);rec(key,ERR);bump(key);var a=award(key,60,ERR,0,HINT?.5:1),all=allDone(),tj=!tj0&&tdone(i),e=ERR,hn=HINT;
  HINT=0;
  doneScreen({title:all?'Обучение завершено!':'Задания решены',lead:all?'Кролик научился программировать и построил автоматическую кормушку 🤖':'Кролик сыт и доволен.',err:e,acc:accOf(IT(i,j).tasks.length,e),tm:islTime(key),x:a.x,bonus:hn?'С подсказкой: 50% опыта':'',note:a.note,tj:tj?TOPICS[i].n:'',lv:a.lv,btns:'<button class="btn" id="go">К темам</button>'});
  $('go').onclick=goBack;
  if(tj||a.lv)confetti(tj&&all?2:1)}

/* --- мини-проект --- */
function project(i,j){
  var PF=0;
  /* at: skip — пропущен; seen — пропущен и эталон открыт: решить можно, но уже без опыта */
  var it=IT(i,j),key=i+'-'+j,done=S.d[key];islStart(key);var seen=S.at[key]==='seen',sk=S.at[key]==='skip'||seen,bonus=it.bonus>0?it.bonus|0:40;
  var dc=((S.dr[key]||{}).codes||{})[0]||'# Пиши код здесь\n'+(it.starter||''),hs=String(it.h||'').split('\n').filter(Boolean);
  scr('project',lessonTop('<span class="lstep">🚀 Мини-проект · по желанию</span>',done?'':'<button class="btn t" id="sk" style="margin:0">Пропустить</button>')+'<div class="pj"><h1>'+esc(it.n)+'</h1>'+(String(it.q||'').length>QLONG?'<div class="card pjl">'+QTB+qSec('Цель',condHtml(it.q,true),true)+(hs.length?qSec('Что пригодится',hs.map(function(l){return'<p class="qi">'+hintTx(l)+'</p>'}).join(''),false):'')+(it.ex?qSec('Пример',exHtml(it.ex,it.strict),true):'')+filesHtml(it.f)+'</div>':'<div class="card"><b>Цель</b><p>'+qfmt(it.q).replace(/\n/g,'</p><p>')+'</p>'+(hs.length?'<b>Что пригодится</b><p>'+hs.map(function(l){return hintTx(l)}).join('<br>')+'</p>':'')+(it.ex?'<b>Пример</b>'+(it.strict?'<pre class="cmp">'+esc(it.ex)+'</pre>':exHtml(it.ex,false)):'')+filesHtml(it.f)+'</div>')+'<p class="mu" style="margin:0 4px 14px">'+(seen?'Эталон открыт, поэтому опыт за проект не начисляется. Решить его всё равно можно.':sk?'Этот проект пропущен. Сделай его сейчас и получи бонус +'+bonus+' ⭐. Или посмотри эталон, но тогда уже без опыта.':done?'Проект уже выполнен, бонус за него получен.':'Проект можно пропустить, тема всё равно засчитается. За выполнение бонус +'+bonus+' ⭐.')+'</p></div>'+edCard('Решение',dc,0,'# Пиши код здесь\n'+(it.starter||''))+conHtml()+'<div id="fb" aria-live="polite"></div>'+dockHtml('<button class="btn" id="chk">Проверить</button>'+(sk&&it.sol?'<button class="btn t" id="pjs">Посмотреть эталон</button>':'')));
  splitWrap();$('x').onclick=home;qBind(app);
  var c=$('code'),ed=c.closest('.ed');ed.dataset.min=300;var sync=initEd(c,function(){drc(i,j,0).codes[0]=c.value.slice(0,3000);lazySave()});sync();
  skReady();chkPulse();runBind(c);
  $('chk').onclick=async function(){
    if(!SKOK)fbSet('<div class="fb"><b>Загружаю среду Python…</b></div>');
    if(!(await needSk()))return;
    var b=$('chk');b.disabled=true;
    var v=await judge(it,c.value);
    if(!v.ok){fx(false);b.disabled=false;PF++;fbSet(badFb(v.h,errMood(PF)));return}
    fx(true,'none');projEnd(i,j)};
  if($('sk'))$('sk').onclick=function(){projSkip(i,j)};
  if($('pjs'))$('pjs').onclick=function(){
    var why=String(it.h||'').split('\n').filter(Boolean);
    function show(){solModal(it.sol,why,'Эталон открыт: опыт за этот проект больше не начисляется.')}
    if(S.at[key]==='seen')return show();
    modal('<h2>Открыть эталон?</h2><p>После этого опыт за проект не начислится, даже если решишь его сам. Решить проект всё равно можно.</p>',[['Открыть эталон',function(){S.at[key]='seen';save();setTimeout(function(){project(i,j);show()},200)}],['Отмена',null,1]])}}
function projEnd(i,j){
  var key=i+'-'+j,it=IT(i,j),tj0=tdone(i),x=0,lv=0,at=S.at[key];
  if(!at||at==='skip'){x=it.bonus>0?it.bonus|0:40;S.at[key]='full';lv=addXp(x)}
  else if(at==='seen')S.at[key]='full';
  bump(key);ach('proj');snd('fanfare');
  var tj=!tj0&&tdone(i),all=allDone();
  doneScreen({mood:'wow',title:all?'Обучение завершено!':'Проект готов!',lead:all?'Кролик научился программировать и построил автоматическую кормушку 🤖':'Кролик в восторге 🚀',tm:islTime(key),x:x,note:x?'':at==='seen'?'Эталон был открыт, поэтому опыт не начислен.':'Бонус за этот проект уже получен.',tj:tj?TOPICS[i].n:'',lv:lv,btns:'<button class="btn" id="go">К темам</button>'+(it.sol?'<button class="btn t" id="sl">Посмотреть, как задумано</button>':'')});
  $('go').onclick=home;if(it.sol)$('sl').onclick=function(){solModal(it.sol)};
  if(tj||lv)confetti(tj&&all?2:1)}

/* --- раздел «Код»: песочница. Главное действие — «Запустить», остальное в меню файла --- */
function fbar(){var s=curSv(),n=$('fnt');if(!n)return;n.textContent=s?s.n:'Без названия';$('fd').hidden=!dirty()}
function fileMenu(){
  var s=curSv(),n=S.sv.length;
  actionSheet(s?s.n:'Код без названия',[
   ['💾','Сохранить',function(){saveCode()},0,KBD?'Ctrl + S':''],
   ['✏️',s?'Переименовать':'Сохранить как…',function(){if(s)askName('Название кода',s.n,function(v){s.n=v;save();fbar();toast('Название изменено')});else saveCode()}],
   ['📂','Мои коды'+(n?' ('+n+')':''),codes],
   ['📄','Новый код',function(){guard(function(){S.cur='';S.ec=NEWC;save();editor()})}],
   ['⬇️','Скачать .py',function(){dlPy({n:s?s.n:'code',c:$('code')?$('code').value:S.ec})}]])}
function editor(){
  scr('editor',head()+'<h1 class="sr-only">Код</h1><div class="edc ec"><div class="edh"><button class="fname" id="fn" aria-label="Меню файла"><svg class="fic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+IC.file+'</svg><span id="fnt"></span><i class="dot" id="fd" hidden title="Есть несохранённые изменения"></i>'+ico('down')+'</button>'+runBtn(1)+'</div>'+edHtml(S.ec||DEFC)+'</div>'+conHtml()+'<p class="mu hint0">Поле ввода появится, когда программа вызовет input().'+(KBD?' Ctrl + Enter запускает код.':'')+'</p>','ed');
  bindHead(editor);
  var c=$('code'),ed=c.closest('.ed');ed.dataset.min=Math.max(260,Math.round(innerHeight*.42));
  var sync=initEd(c,function(){S.ec=c.value.slice(0,4000);lazySave();fbar()});sync();fbar();
  $('fn').onclick=fileMenu;
  $('run').onclick=function(){var o=$('o');$('cons').hidden=false;if(!SKOK){o.textContent='Загружаю среду Python…'}skReady().then(function(ok){if(!ok){o.textContent='Среда Python не загрузилась. Нажми «Запустить» ещё раз.';return}liveRun(c.value)})}}
var EMPTY='<svg viewBox="0 0 120 96" aria-hidden="true"><ellipse cx="60" cy="88" rx="44" ry="5" fill="var(--line)"/><rect x="30" y="14" width="60" height="70" rx="10" fill="var(--card)" stroke="var(--line2)" stroke-width="3"/><path d="M42 34h36M42 46h26M42 58h32" stroke="var(--line2)" stroke-width="5" stroke-linecap="round"/><path d="M76 66l10 10" stroke="var(--accent)" stroke-width="5" stroke-linecap="round"/><circle cx="70" cy="60" r="10" fill="none" stroke="var(--accent)" stroke-width="5"/></svg>';
function codes(){
  var L=S.sv.slice().sort(function(a,b){return b.t-a.t});
  var h=subTop('Мои коды','💾',L.length?L.length+' '+pl(L.length,['программа','программы','программ']):'');
  if(!L.length)h+='<div class="empty">'+EMPTY+'<p>Пока пусто. Открой меню файла в разделе «Код» и нажми «Сохранить».</p></div>';
  L.forEach(function(s){
    var ln=s.c.replace(/\s+$/,'').split('\n').length;
    h+='<div class="sr'+(s.id===S.cur?' cur':'')+'" data-id="'+s.id+'"><button class="so" data-a="o"><b>'+esc(s.n)+(s.id===S.cur?' <span class="pill a">открыт</span>':'')+'</b><small>'+fdt(s.t)+(s.t?', ':'')+ln+' '+pl(ln,['строка','строки','строк'])+'</small></button><button class="icon" data-a="m" aria-label="Действия с «'+esc(s.n)+'»">'+ico('more')+'</button></div>'});
  scr('codes',h+(L.length?'<p class="mu" style="font-size:.8125rem;margin:12px 6px 0">Сохранено '+L.length+' из 30. Коды хранятся только на этом устройстве.</p>':''),'ed');
  $('x').onclick=editor;
  app.querySelectorAll('.sr').forEach(function(r){
    var s=S.sv.filter(function(z){return z.id===r.dataset.id})[0];
    function open(){if(s.id===S.cur){editor();return}guard(function(){S.cur=s.id;S.ec=s.c;save();editor()})}
    r.onclick=function(e){
      var b=e.target.closest('button');if(!b||!s)return;
      if(b.dataset.a==='o'){open();return}
      actionSheet(s.n,[
       ['📂','Открыть',open],
       ['✏️','Переименовать',function(){askName('Название кода',s.n,function(v){s.n=v;save();codes();toast('Название изменено')})}],
       ['⧉','Дублировать',function(){if(S.sv.length>=30){toast('Можно хранить до 30 кодов');return}S.sv.unshift({id:uid(),n:(s.n+' (копия)').slice(0,40),c:s.c,t:Date.now()});save();codes();toast('Копия создана')}],
       ['⬇️','Скачать .py',function(){dlPy(s)}],
       ['🗑️','Удалить',function(){modal('<h2>Удалить «'+esc(s.n)+'»?</h2><p>Отменить это нельзя.</p>',[['Удалить',function(){S.sv=S.sv.filter(function(z){return z.id!==s.id});if(S.cur===s.id)S.cur='';save();codes();toast('Удалено')},0,1],['Отмена',null,1]])},1]])}})}

/* --- словарь изученных функций --- */
var DOPEN=Object.create(null),DNOTE=0;
function dict(){
  var L=learned();L.sort(S.dsort?function(a,b){return a.ti-b.ti}:function(a,b){return a.n.localeCompare(b.n,'ru')});
  var h=subTop('Изученные функции','📚',L.length?L.length+' '+pl(L.length,['функция','функции','функций']):'');
  if(!L.length){scr('dict',h+'<div class="empty">'+EMPTY+'<p>Пока пусто. Прочитай теорию, и функции из неё появятся здесь.</p></div>','prof');$('x').onclick=profile;return}
  h+='<div class="srch">'+ico('search')+'<input class="f dq" id="dq" type="search" placeholder="Найти функцию или заметку" autocomplete="off" aria-label="Поиск по функциям"></div><div class="dtools">'+SG('ds',[[0,'А–Я'],[1,'По темам']],S.dsort?1:0)+'<button class="chip tgl" id="sf" aria-pressed="'+(DNOTE?'true':'false')+'">📝 Заметки</button></div><div class="dm" id="dm" aria-live="polite"></div>';
  var lt=-1,open=false;
  function closeG(){if(open){h+='</div></div>';open=false}}
  L.forEach(function(x){
    if(!open||(S.dsort&&x.ti!==lt)){closeG();lt=x.ti;h+='<div class="dg">'+(S.dsort?'<div class="dt">'+esc(x.tn)+'</div>':'')+'<div class="dl">';open=true}
    var nt=S.nt[x.n]||'',op=!!DOPEN[x.n],c=fcol(x.n);
    h+='<div class="de'+(op?' op':'')+(nt.trim()?' hn':'')+'" data-n="'+esc(x.n)+'" data-s="'+esc((x.n+' '+x.d).toLowerCase())+'"><button class="dh" aria-expanded="'+(op?'true':'false')+'"><code'+(c?' style="color:'+c+'"':'')+'>'+esc(x.n)+'</code><span class="dn" role="img" aria-label="Есть заметка">📝</span>'+ico('chev','dc')+'</button><div class="dp"><div class="di"><div class="dx">'+termHtml(x.d)+'<textarea class="note" rows="1" maxlength="1000" placeholder="Моя заметка" aria-label="Заметка к '+esc(x.n)+'">'+esc(nt)+'</textarea></div></div></div></div>'});
  closeG();
  scr('dict',h,'prof');
  $('x').onclick=profile;
  app.querySelectorAll('.dtools .segc button').forEach(function(b){b.onclick=function(){S.dsort=+b.dataset.v;save();KEEPSCR=1;SKEY='dict';dict()}});
  var ds=app.querySelectorAll('.de');
  function grow(t){t.style.height='auto';t.style.height=Math.min(t.scrollHeight+4,164)+'px';t.style.overflowY=t.scrollHeight>160?'auto':'hidden'}
  function apply(keep){
    var q=$('dq').value.trim().toLowerCase(),v=0,nc=0;
    ds.forEach(function(d){
      var tx=d.querySelector('textarea').value,hn=d.classList.contains('hn'),ok=(!q||(d.dataset.s+' '+tx.toLowerCase()).indexOf(q)>=0)&&(!DNOTE||hn);
      if(hn)nc++;if(ok)v++;if(!keep)d.hidden=!ok});
    if(!keep)app.querySelectorAll('.dg').forEach(function(g){g.hidden=!g.querySelector('.de:not([hidden])')});
    $('dm').textContent=(q||DNOTE)?(v?'Найдено: '+v:'Ничего не найдено'):ds.length+' '+pl(ds.length,['функция','функции','функций'])+(nc?', заметок: '+nc:'')}
  ds.forEach(function(d){
    var n=d.dataset.n,b=d.querySelector('.dh'),t=d.querySelector('textarea');
    b.onclick=function(){var o=!d.classList.contains('op');d.classList.toggle('op',o);b.setAttribute('aria-expanded',o?'true':'false');if(o){DOPEN[n]=1;requestAnimationFrame(function(){grow(t)})}else delete DOPEN[n]};
    if(DOPEN[n])requestAnimationFrame(function(){grow(t)});
    t.oninput=function(){var v=t.value;if(n.length<=40){if(v.trim())S.nt[n]=v.slice(0,1000);else delete S.nt[n];lazySave()}d.classList.toggle('hn',!!v.trim());grow(t);apply(true)}});
  $('sf').onclick=function(){DNOTE=DNOTE?0:1;this.setAttribute('aria-pressed',DNOTE?'true':'false');apply()};
  $('dq').oninput=function(){apply()};
  apply()}

/* --- телефон: пока открыта клавиатура, док и нижняя панель уходят и не закрывают код --- */
(function(){
  if(!matchMedia('(pointer:coarse)').matches)return;
  var R=document.documentElement;
  function typing(t){return t&&(t.tagName==='TEXTAREA'||(t.tagName==='INPUT'&&!/^(range|checkbox|radio|button|submit)$/.test(t.type)))}
  document.addEventListener('focusin',function(e){if(typing(e.target)&&!e.target.closest('.modal'))R.classList.add('kbo')});
  document.addEventListener('focusout',function(){setTimeout(function(){if(!typing(document.activeElement))R.classList.remove('kbo')},80)});
})();

/* --- резервная копия: те же действия, что и раньше, но списком, а не стопкой из пяти кнопок --- */
function backup(){
  var fl=location.protocol==='file:';
  var o=modal('<div class="bk"><h2>Резервная копия</h2><p>Прогресс и коды из раздела «Код» хранятся только на этом устройстве. Если очистить данные браузера, переустановить приложение или открыть ИТП на другом телефоне, они пропадут. Сохрани копию, чтобы потом загрузить её обратно.</p><p class="mu">Так же переносится прогресс между устройствами: сохрани копию на телефоне и загрузи её на компьютере, или наоборот. Файл и код подходят для приложения, программы для ПК и браузера.</p>'+(fl?'<p class="mu">ИТП открыт как файл. На некоторых устройствах прогресс привязан к месту, где лежит файл: если его переместить или переименовать, прогресс может не найтись. Копия от этого защитит.</p>':'')+(Store.ok()?'':'<p class="mu" style="color:var(--bad)">Браузер не разрешает сохранять данные. Прогресс исчезнет при закрытии страницы, поэтому обязательно сделай копию.</p>')+
    '<div class="lst acts"><button class="li" data-a="s"><span class="lic" aria-hidden="true">💾</span><span class="lt">Сохранить в файл<small>'+(typeof NATIVE!=='undefined'&&NATIVE==='android'?'Файл .json — отправь его в мессенджер, на диск или себе на почту':typeof NATIVE!=='undefined'&&NATIVE==='win'?'Файл .json — выберешь, куда сохранить':'Файл .json в загрузках')+'</small></span></button><button class="li" data-a="l"><span class="lic" aria-hidden="true">📂</span><span class="lt">Загрузить из файла<small>Заменит текущий прогресс</small></span></button><button class="li" data-a="c"><span class="lic" aria-hidden="true">📋</span><span class="lt">Скопировать код сохранения<small>Если с файлами неудобно</small></span></button><button class="li" data-a="p"><span class="lic" aria-hidden="true">📥</span><span class="lt">Вставить код сохранения</span></button></div>'+
    '<textarea id="bkt" hidden placeholder="Вставь сюда код сохранения" aria-label="Код сохранения"></textarea><button class="btn" id="bkg" hidden>Загрузить код</button><p class="mu" style="margin-top:10px;font-size:.84375rem">Файл подписан приложением: если изменить его вручную, он не загрузится.</p></div>',[['Закрыть',null,1]]);
  o.classList.add('as');
  var t=o.querySelector('#bkt'),g=o.querySelector('#bkg');
  function load(txt){var e=importData(txt);if(e){toast(e);return}o.remove();toast('Прогресс загружен');home()}
  o.querySelector('[data-a="s"]').onclick=function(){saveFile('itp-backup-'+day(new Date())+'.json',new Blob([exportData()],{type:'application/json'}));toast('Копия сохранена')};
  o.querySelector('[data-a="l"]').onclick=function(){var f=document.createElement('input');f.type='file';f.accept=typeof NATIVE!=='undefined'&&NATIVE==='android'?'':'.json,application/json,text/plain';f.onchange=function(){var fi=f.files&&f.files[0];if(!fi)return;var r=new FileReader();r.onload=function(){load(String(r.result))};r.readAsText(fi)};f.click()};
  o.querySelector('[data-a="c"]').onclick=function(){copyTxt(exportData())};
  o.querySelector('[data-a="p"]').onclick=function(){t.hidden=false;g.hidden=false;t.focus()};
  g.onclick=function(){load(t.value.trim())}}
/* --- горячие клавиши (на компьютере) --- */
function keys(){
  var ex=document.querySelector('.modal');if(ex){if(ex.classList.contains('kbm'))ex.remove();return}
  var km=modal('<h2>Горячие клавиши</h2><table class="kt">'+[['Ctrl + Enter','Запустить код'],['Ctrl + S','Сохранить код в разделе «Код»'],['1…4','Выбрать вариант ответа'],['Enter','Проверить ответ или идти дальше'],['Esc','Назад или закрыть окно'],['Ctrl + H','Подсказка в задании'],['Ctrl или Alt + 1…4','Путь, Практика, Код, Профиль'],['Ctrl + D','Светлая или тёмная тема'],['Ctrl + M','Звук вкл/выкл'],['F1 или ?','Это окно']].map(function(r){return'<tr><td><kbd>'+r[0]+'</kbd></td><td>'+r[1]+'</td></tr>'}).join('')+'</table><p class="mu" style="margin:10px 0 0;font-size:.875rem">Если браузер занимает Ctrl + цифры под вкладки, используй Alt + цифры. Сочетания работают на любой раскладке.</p>',[['Закрыть']]);km.classList.add('kbm')}

/* --- цвет каждой функции: оттенок прежний (у каждой функции свой, одинаковый в теории и в редакторе),
       светлота подбирается по оттенку так, чтобы текст читался на фоне кода не хуже 4,5:1 в обеих темах.
       Синие, фиолетовые, красные оттенки не меняются, темнеют только светлые жёлто-зелёные. --- */
var FADJ=Object.create(null);
function fadj(h){
  if(FADJ[h])return FADJ[h];
  function rgb(H,s,l){s/=100;l/=100;var k=function(n){return(n+H/30)%12},a=s*Math.min(l,1-l),f=function(n){return l-a*Math.max(-1,Math.min(k(n)-3,Math.min(9-k(n),1)))};return[f(0),f(8),f(4)]}
  function lu(c){var g=function(x){return x<=.03928?x/12.92:Math.pow((x+.055)/1.055,2.4)};return .2126*g(c[0])+.7152*g(c[1])+.0722*g(c[2])}
  function hx(n){return[(n>>16&255)/255,(n>>8&255)/255,(n&255)/255]}
  function mix(a,b,t){return[a[0]*t+b[0]*(1-t),a[1]*t+b[1]*(1-t),a[2]*t+b[2]*(1-t)]}
  function cr(a,b){var x=lu(a),y=lu(b);return(Math.max(x,y)+.05)/(Math.min(x,y)+.05)}
  function okL(c,bgs){return bgs.every(function(b){return cr(c,b)>=4.5&&cr(c,mix(c,b,.13))>=4.5})}
  var BL=[0xF7F4EE,0xFFFFFF,0xF1EDE5].map(hx),BD=[0x191715,0x1E1C1A,0x272421].map(hx),a=34,b=68;
  while(a>18&&!okL(rgb(h,72,a),BL))a--;
  while(b<88&&!okL(rgb(h,68,b),BD))b++;
  return FADJ[h]=[a-34,b-68]}
function fcol(n){if(n==='print')return'var(--bi)';var h=FH[n];if(h===undefined){if(!(BI[n]||MS[n]||ML[n]||MD[n]||MT[n]||MF[n]||TB[n]))return'';h=0;for(var i=0;i<n.length;i++)h=(h*31+n.charCodeAt(i))%360}
  var d=fadj(h);return'hsl('+h+' var(--fsat) calc(var(--flit) + '+d[0]+'% * var(--fl1) + '+d[1]+'% * var(--fd1)))'}

/* --- доступность: основная область страницы для экранных чтецов --- */
app.setAttribute('role','main');


/* ===== настроения кролика =====
   Спрайты показываются только в настоящих событиях, без реакций на нажатия и без фонового движения:
   • grumphead (хмурая голова): первая ошибка в серии (неверный ответ, непрошедший тест, ошибка в программе), статичный;
   • rolled (закатил глаза): один раз, на итоге островка, где ошибок было ROLL_AT и больше;
   • happy (ликующий): итог островка, проекта, уровня, курса; eat (с морковкой): знакомство и приветствие при идущей серии.
   Не больше одного спрайта на момент. Если файла rolled нет в сборке, на его месте стоит grump (хмурый целиком). */
var PRW=0,CERR=0;
var MOODL={grumphead:['Хм. Не совсем.','Кролик приподнял бровь.','Почти, но нет.','Бывает. Кролик не в обиде.'],
 rolled:['Кролик закатил глаза, но верит в тебя.','Ну вот опять. Зато теперь запомнишь.','Глубокий вдох. Ещё раз.','Кролик вздохнул. Ты справишься.']};
var MOODI={grumphead:Math.floor(Math.random()*4),rolled:Math.floor(Math.random()*4)};
function moodLine(k){var a=MOODL[k]||MOODL.grumphead;return a[MOODI[k]++%a.length]}
/* закатил глаза: только на итоге островка, если на нём ошибок ROLL_AT и больше; хмурый: только первая ошибка в серии */
var ROLL_AT=4;
function errMood(n){return n===1?'grumphead':''}
function moodBox(k,sz){var s=IMG[k]||IMG.grumphead;return s?'<span class="mood '+k+(sz?' '+sz:'')+'" aria-hidden="true"><img src="'+s+'" alt="" draggable="false"></span>':''}
function badFb(h,k){return k?h.replace('<div class="fb bad">','<div class="fb bad">'+moodBox(k,'fl')).replace(/<\/div>\s*$/,'<p class="mq">'+moodLine(k)+'</p></div>'):h}
/* консоль: следим за строкой состояния, не трогая движок запуска */
function consWatch(){
  var r=$('rst');if(!r||r._w)return;r._w=1;r._s='';
  new MutationObserver(function(){
    var t=r.textContent;
    if(/выполняется|ждёт ввод/.test(t)){r._s='';return}
    if(/ошибк|не запущена/.test(t)&&r._s!=='e'){
      r._s='e';CERR++;var k=errMood(CERR),q=$('cmq');
      if(q&&k){q.innerHTML=moodBox(k,'sm')+'<span>'+moodLine(k)+' '+(k==='grumphead'?'Прочитай последнюю строку сообщения: там сказано, что не так.':'Проверь номер строки из сообщения.')+'</span>';q.hidden=false}
      else if(q)q.hidden=true}
    else if(/завершена/.test(t)){CERR=0;r._s='';var q2=$('cmq');if(q2)q2.hidden=true}
  }).observe(r,{childList:true,characterData:true,subtree:true,attributes:true})}
