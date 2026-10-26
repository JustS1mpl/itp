/* ===================== ИТП 6 — экраны уроков, редактор, словарь, окна =====================
   Переопределяет экраны из базы (orig.html): логика (опыт, подсказки, черновики, проверка тестами)
   перенесена без изменений, поменялась только раскладка. Ничего о конкретных темах здесь не записано. */

/* --- переходы между экранами: направление объясняет, куда ты попал --- */
var SDEP={home:0,practice:0,editor:0,profile:0,greet:0,nick:0,place:0,settings:1,dict:1,codes:1,theory:1,quiz:1,task:1,project:1,askq:1,rcode:1,done:2},PSKEY='';
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
function solModal(sol){modal('<h2>Как это можно сделать</h2><pre class="cmp">'+hl(sol)+'</pre><p>Это один из вариантов. Если тесты прошли, твоё решение тоже верное.</p><p class="mu">Эталон не влияет на опыт.</p>',[['Закрыть']])}
function askName(title,val,cb,max){
  modal('<h2>'+esc(title)+'</h2><input class="f n" id="mi" maxlength="'+(max||40)+'" value="'+esc(val)+'" autocomplete="off" aria-label="'+esc(title)+'">',[['Сохранить',function(o){var i=o.querySelector('#mi'),v=i.value.trim();if(!v){i.focus();return false}cb(v.slice(0,max||40))}],['Отмена',null,1]]);
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
function fbSet(h){var f=$('fb');if(!f)return;f.innerHTML=h;if(h)requestAnimationFrame(function(){var r=f.getBoundingClientRect(),lim=innerHeight-110;if(r.top>lim-60||r.bottom>lim)f.scrollIntoView({block:'nearest',behavior:RM()?'auto':'smooth'})})}
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
function taskCard(q,lab){return'<section class="tcard"><span class="ov">'+(lab||'Задание')+'</span><h2>'+esc(q.q)+'</h2>'+(q.ex?'<div class="pyex"><span>Пример</span>'+(q.strict?'<pre class="cmp">'+esc(q.ex)+'</pre>':'<p>'+esc(q.ex).replace(/\n/g,'<br>')+'</p>')+'</div>':'')+'</section>'}
function edHtml(dc){return'<div class="ed"><div class="gt" aria-hidden="true"></div><div class="ew"><pre id="hl" aria-hidden="true"></pre><textarea id="code" wrap="off" spellcheck="false" autocapitalize="off" autocorrect="off" autocomplete="off" aria-label="Код"'+(KBD?' aria-describedby="edk"':'')+'>'+esc(dc)+'</textarea></div></div>'}
function runBtn(pri){return'<button class="btn s'+(pri?'':' g')+'" id="run" aria-keyshortcuts="Control+Enter">'+ico('play')+'Запустить</button>'}
function edCard(lab,dc,headL){return'<div class="edc"><div class="edh">'+(headL||'<span class="ov">'+lab+'</span>')+runBtn()+'</div>'+edHtml(dc)+'</div>'+(KBD?'<p class="mu hint0" id="edk">Ctrl + Enter запускает код.</p>':'')}
function conHtml(){return'<section class="cons" id="cons" hidden aria-label="Вывод программы"><div class="csh"><span class="ov">Вывод</span><p class="mu rst" id="rst" hidden aria-live="polite"></p></div><pre class="out" id="o"></pre><div class="cmq" id="cmq" hidden></div>'+'<form class="inrow" id="ir" autocomplete="off"><input class="f" id="ii" placeholder="Ответ программе" aria-label="Ввод для программы" autocomplete="off" enterkeyhint="send"><button class="btn" id="ib" type="submit">Ввод</button></form></section>'}
var IOHTML=conHtml();
/* консоль показывается при первом запуске, пока её нет — не занимает место */
(function(){var lr=liveRun;liveRun=function(code){var c=$('cons');if(c)c.hidden=false;var q=$('cmq');if(q)q.hidden=true;var r=lr(code);consWatch();return r}})();
function runBind(c){
  $('run').onclick=function(){var o=$('o'),cs=$('cons');if(cs)cs.hidden=false;if(!SKOK){o.textContent='Загружаю среду Python…'}needSk().then(function(ok){if(ok)liveRun(c.value)})}}
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
  return sync}

/* --- итог островка: что получил, сколько опыта, куда дальше --- */
function doneScreen(o){
  var many=o.err>=ROLL_AT;
  var h='<div class="fin">'+rabbit(many?'rolled':(o.mood||(o.err===0?'cool':'happy')))+'<h1>'+o.title+'</h1>'+(many?'<p class="lead">Непростой островок: ошибок было много. Но он пройден, а ошибки разобраны.</p>':o.lead?'<p class="lead">'+o.lead+'</p>':'')+
   '<div class="xpr">'+(o.err!==undefined?'<div class="xpt"><small>Ошибок</small><b>'+o.err+'</b></div>':'')+'<div class="xpt x" id="xpt"><small>Опыт</small><b>⭐ <span id="xpn">+0</span></b></div></div>'+
   (o.bonus?'<p class="note2">'+o.bonus+'</p>':'')+(o.note?'<p class="note2">'+esc(o.note)+'</p>':'')+
   (o.tj?'<div class="tj">🎉 Тема «'+esc(o.tj)+'» пройдена!</div>':'')+(o.lv?'<div><span class="lvup">⬆️ Новый уровень: '+o.lv+'</span></div>':'')+
   xpStrip(o.x)+'</div>';
  scr('done',h+dockHtml(o.btns,1));
  /* звук в такт анимации: «пройдено» в момент появления экрана, искорка опыта в момент, когда число начинает расти;
     тема пройдена или новый уровень звучат через конфетти (там нужный звук выбирает SX.cs) */
  SX.cs=o.tj?'fanfare':(o.lv?'level':'');setTimeout(function(){SX.cs=''},1500);
  if(!o.tj&&!o.lv&&!sndRecent('fanfare',600))snd('done');
  if(RM()&&o.x>0)setTimeout(function(){snd('xpt',{k:0})},260);
  /* опыт «набегает» числом, потом заполняется полоса уровня */
  var n=$('xpn'),t=$('xpt'),x=o.x||0;
  if(RM()||!x){n.textContent='+'+x}else{var t0=0,xt=xpTick();setTimeout(function(){t.classList.add('pp');requestAnimationFrame(function st(ts){if(!t0)t0=ts;var k=Math.min(1,(ts-t0)/650),vv=Math.round(x*(1-Math.pow(1-k,3)));n.textContent='+'+vv;xt(vv);if(k<1&&n.isConnected)requestAnimationFrame(st)});sparks(t)},260)}
  xpStripRun();
  var b=document.querySelector('#dock .btn');if(b)setTimeout(function(){b.focus({preventScroll:true})},60)}
function sparks(el){
  var r=el.getBoundingClientRect(),cols=['var(--gold)','var(--carrot)','var(--accent)','#fff'];
  for(var k=0;k<14;k++){var s=document.createElement('i');s.style.cssText='position:fixed;z-index:31;left:'+(r.left+r.width/2)+'px;top:'+(r.top+r.height/2)+'px;width:7px;height:7px;margin:-3.5px;border-radius:2px;pointer-events:none;background:'+cols[k%4];document.body.appendChild(s);
    var a=k/14*6.283+Math.random()*.4,d=50+Math.random()*50;
    (function(s){s.animate([{transform:'translate(0,0) rotate(0) scale(1)',opacity:1},{transform:'translate('+Math.cos(a)*d+'px,'+(Math.sin(a)*d-20)+'px) rotate('+(Math.random()*360)+'deg) scale(.4)',opacity:0}],{duration:700+Math.random()*300,easing:'cubic-bezier(.2,.8,.3,1)'}).onfinish=function(){s.remove()}})(s)}}

/* --- теория --- */
function theory(i,j){
  var it=IT(i,j),T={},fresh=!S.d[i+'-'+j],rm=RM();(it.terms||[]).forEach(function(x){T[x.n]=x});
  var h=it.html.split(/(<pre[^>]*>[\s\S]*?<\/pre>)/).map(function(p){return /^<pre /.test(p)?p:/^<pre>/.test(p)?'<div class="cpw"><button type="button" class="cp" aria-label="Копировать код"></button><pre>'+hl(p.slice(5,-6))+'</pre></div>':p.replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,function(m,n,l){return T[n]?'<button class="term'+(fcol(n)?' fn':'')+'"'+(fcol(n)?' style="color:'+fcol(n)+'"':'')+' data-n="'+esc(n)+'" aria-haspopup="dialog">'+(l||esc(n))+'</button>':(l||esc(n))})}).join('');
  scr('theory',lessonTop('<div class="rprog" role="progressbar" aria-label="Прочитано" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><i id="rpb"></i></div>','<span class="lstep">≈ '+readMin(it)+' мин</span>')+'<article class="th"><p class="ov tov">'+esc(TOPICS[i].n)+'</p><h1 class="tt">'+esc(it.n)+'</h1><div id="tb">'+h+'</div><p class="mu tm" id="tm">'+(fresh&&!rm&&ST('ty')?TMSK:TMT)+'</p></article><button class="btn" id="go">'+(S.d[i+'-'+j]?'Готово':G('Я прочитал','Я прочитала','Прочитано')+', открыть дальше')+'</button>');
  $('x').onclick=goBack;
  app.querySelectorAll('.term').forEach(function(b){b.onclick=function(){var x=T[b.dataset.n];sheet(x.n,x.d)}});
  $('go').onclick=function(){var w=tdone(i);if(!S.d[i+'-'+j]){snd('theory');bump(i+'-'+j)}if(TOPICS[i].intro&&!w&&tdone(i)&&S.start===0){reveal();return}if(TOPICS[i].intro&&(S.start>0||w)){goBack();if(!w)toast('Готово. Эта кнопка больше не нужна и пропала из профиля');return}home();if(!w&&tdone(i)){toast('🎉 Тема «'+TOPICS[i].n+'» пройдена!');confetti(allDone()?2:1)}};
  if(window.TW)TW.scan(app);
  tocBuild();if(fresh&&!rm&&ST('ty'))typeIn($('tb'),$('tm'));
  readProg()}
/* полоска в шапке теории: сколько уже прочитано */
var RPS=null;
function readProg(){
  if(RPS)window.removeEventListener('scroll',RPS);
  var b=$('rpb');if(!b)return;var bar=b.parentNode,lp=-1,fin=0;
  RPS=function(){if(!b.isConnected){window.removeEventListener('scroll',RPS);RPS=null;return}var mx=document.documentElement.scrollHeight-innerHeight,p=mx>8?Math.min(100,Math.round(window.scrollY/mx*100)):(fin?100:0);if(p!==lp){lp=p;b.style.width=p+'%';bar.setAttribute('aria-valuenow',p)}};
  window.addEventListener('scroll',RPS,{passive:true});if(window.ResizeObserver){var ro=new ResizeObserver(function(){if(!b.isConnected||!RPS){ro.disconnect();return}RPS()});ro.observe(document.body)}setTimeout(function(){if(RPS)RPS()},60);setTimeout(function(){fin=1;if(RPS)RPS()},700)}

/* --- вопросы --- */
function quiz(i,j){
  var key=i+'-'+j,Ql=IT(i,j).q,tot=Ql.length,D=S.dr[key],first=!S.at[key];
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
    doneScreen({title:'Островок пройден',lead:er?'Ошибки разобраны, двигаемся дальше.':'Без единой ошибки!',err:er,x:a.x,bonus:!nx&&first&&bon&&er<=3?'Бонус за серию верных ответов: +'+bon+' ⭐':'',note:a.note,tj:tj?TOPICS[i].n:'',lv:a.lv,btns:'<button class="btn" id="go">Дальше</button>'+(nx?'<button class="btn t" id="rp">Пройти заново</button>':'')});
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
    var h=lessonTop('<div class="sbar" id="sb" role="img" aria-label="Отвечено '+st.filter(Boolean).length+' из '+tot+'">'+segs()+'</div>')+'<h1 class="sr-only">'+esc(IT(i,j).n||'Вопросы')+'</h1>'+(ph?'<div class="qph">🔁 Работа над ошибками</div>':'')+'<h2 class="q">'+esc(q.q)+'</h2>'+(q.v||'')+(q.c?'<pre>'+hl(q.c)+'</pre>':'')+optsHtml(q,ord);
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

/* --- задания с кодом --- */
function task(i,j,k){
  var it=IT(i,j),T=it.tasks,q=T[k],key=i+'-'+j,tk=key+'-'+k;
  var dc=((S.dr[key]||{}).codes||{})[k]||(S.tk[tk]?'':'# Пиши код здесь\n'+(q.starter||''));
  var dots='<div class="sbar" role="img" aria-label="Задание '+(k+1)+' из '+T.length+'">'+T.map(function(x,n){return'<i class="'+(S.tk[key+'-'+n]?'ok':n===k?'cu':'')+'"></i>'}).join('')+'</div>';
  scr('task',lessonTop(dots,'<span class="lstep" aria-hidden="true">'+(k+1)+' / '+T.length+'</span>'+(q.h?'<button class="icon" id="hb" aria-label="Подсказка (опыт будет вдвое меньше)" aria-keyshortcuts="Control+H">'+ico('bulb')+'</button>':''))+'<h1 class="sr-only">'+esc(it.n||'Задания с кодом')+', задание '+(k+1)+' из '+T.length+'</h1>'+taskCard(q)+'<div id="hint"></div>'+edCard('Решение',dc)+conHtml()+'<div id="fb" aria-live="polite"></div>'+dockHtml('<button class="btn" id="chk">Проверить</button>'));
  $('x').onclick=goBack;
  var c=$('code'),sync=initEd(c,function(){drc(i,j,k).codes[k]=c.value.slice(0,3000);lazySave()});sync();
  function showHint(){var hb=$('hb');if(hb)hb.classList.add('on');$('hint').innerHTML='<div class="fb"><b>Подсказка</b>'+esc(q.h).replace(/\n/g,'<br>')+'<br><span class="mu">Опыт за это задание: 50% от максимума.</span></div>'}
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
    var sb=app.querySelector('.top .sbar i:nth-child('+(k+1)+')');if(sb)sb.className='ok';
    dockSet('<button class="btn" id="nx">'+(last?'Завершить':'Следующее задание')+'</button>'+(q.sol?'<button class="btn t" id="sl">Посмотреть, как задумано</button>':''));
    $('nx').onclick=function(){last?end(i,j):task(i,j,k+1)};
    if(q.sol)$('sl').onclick=function(){solModal(q.sol)}}}
function end(i,j){
  var key=i+'-'+j,tj0=tdone(i);rec(key,ERR);bump(key);var a=award(key,60,ERR,0,HINT?.5:1),all=allDone(),tj=!tj0&&tdone(i),e=ERR,hn=HINT;
  HINT=0;
  doneScreen({title:all?'Обучение завершено!':'Задания решены',lead:all?'Кролик научился программировать и построил автоматическую кормушку 🤖':'Кролик сыт и доволен.',err:e,x:a.x,bonus:hn?'С подсказкой: 50% опыта':'',note:a.note,tj:tj?TOPICS[i].n:'',lv:a.lv,btns:'<button class="btn" id="go">К темам</button>'});
  $('go').onclick=goBack;
  if(tj||a.lv)confetti(tj&&all?2:1)}

/* --- мини-проект --- */
function project(i,j){
  var PF=0;
  var it=IT(i,j),key=i+'-'+j,done=S.d[key],sk=S.at[key]==='skip',bonus=it.bonus>0?it.bonus|0:40;
  var dc=((S.dr[key]||{}).codes||{})[0]||'# Пиши код здесь\n'+(it.starter||''),hs=String(it.h||'').split('\n').filter(Boolean);
  scr('project',lessonTop('<span class="lstep">🚀 Мини-проект · по желанию</span>',done?'':'<button class="btn t" id="sk" style="margin:0">Пропустить</button>')+'<div class="pj"><h1>'+esc(it.n)+'</h1><div class="card"><b>Цель</b><p>'+esc(it.q).replace(/\n/g,'</p><p>')+'</p>'+(hs.length?'<b>Что пригодится</b><p>'+hs.map(esc).join('<br>')+'</p>':'')+(it.ex?'<b>Пример</b>'+(it.strict?'<pre class="cmp">'+esc(it.ex)+'</pre>':'<p style="margin-bottom:0">'+esc(it.ex).replace(/\n/g,'<br>')+'</p>'):'')+'</div><p class="mu" style="margin:0 4px 14px">'+(sk?'Этот проект пропущен. Сделай его сейчас и получи бонус +'+bonus+' ⭐.':done?'Проект уже выполнен, бонус за него получен.':'Проект можно пропустить, тема всё равно засчитается. За выполнение бонус +'+bonus+' ⭐.')+'</p></div>'+edCard('Решение',dc)+conHtml()+'<div id="fb" aria-live="polite"></div>'+dockHtml('<button class="btn" id="chk">Проверить</button>'));
  $('x').onclick=home;
  var c=$('code'),ed=c.closest('.ed');ed.dataset.min=300;var sync=initEd(c,function(){drc(i,j,0).codes[0]=c.value.slice(0,3000);lazySave()});sync();
  skReady();chkPulse();runBind(c);
  $('chk').onclick=async function(){
    if(!SKOK)fbSet('<div class="fb"><b>Загружаю среду Python…</b></div>');
    if(!(await needSk()))return;
    var b=$('chk');b.disabled=true;
    var v=await judge(it,c.value);
    if(!v.ok){fx(false);b.disabled=false;PF++;fbSet(badFb(v.h,errMood(PF)));return}
    fx(true,'none');projEnd(i,j)};
  if($('sk'))$('sk').onclick=function(){projSkip(i,j)}}
function projEnd(i,j){
  var key=i+'-'+j,it=IT(i,j),tj0=tdone(i),x=0,lv=0,at=S.at[key];
  if(!at||at==='skip'){x=it.bonus>0?it.bonus|0:40;S.at[key]='full';lv=addXp(x)}
  bump(key);ach('proj');snd('fanfare');
  var tj=!tj0&&tdone(i),all=allDone();
  doneScreen({mood:'wow',title:all?'Обучение завершено!':'Проект готов!',lead:all?'Кролик научился программировать и построил автоматическую кормушку 🤖':'Кролик в восторге 🚀',x:x,note:x?'':'Бонус за этот проект уже получен.',tj:tj?TOPICS[i].n:'',lv:lv,btns:'<button class="btn" id="go">К темам</button>'+(it.sol?'<button class="btn t" id="sl">Посмотреть, как задумано</button>':'')});
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
  var h='<div class="top ls"><button class="icon" id="x" aria-label="Назад">'+ico('back')+'</button><h1>Мои коды</h1></div>';
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
  var h='<div class="top ls"><button class="icon" id="x" aria-label="Назад">'+ico('back')+'</button><h1>Изученные функции</h1></div>';
  if(!L.length){scr('dict',h+'<div class="empty">'+EMPTY+'<p>Пока пусто. Прочитай теорию, и функции из неё появятся здесь.</p></div>','prof');$('x').onclick=profile;return}
  h+='<div class="srch">'+ico('search')+'<input class="f dq" id="dq" type="search" placeholder="Найти функцию или заметку" autocomplete="off" aria-label="Поиск по функциям"></div><div class="dtools">'+SG('ds',[[0,'А–Я'],[1,'По темам']],S.dsort?1:0)+'<button class="chip tgl" id="sf" aria-pressed="'+(DNOTE?'true':'false')+'">📝 Заметки</button></div><div class="dm" id="dm" aria-live="polite"></div>';
  var lt=-1,open=false;
  function closeG(){if(open){h+='</div></div>';open=false}}
  L.forEach(function(x){
    if(!open||(S.dsort&&x.ti!==lt)){closeG();lt=x.ti;h+='<div class="dg">'+(S.dsort?'<div class="dt">'+esc(x.tn)+'</div>':'')+'<div class="dl">';open=true}
    var nt=S.nt[x.n]||'',op=!!DOPEN[x.n],c=fcol(x.n);
    h+='<div class="de'+(op?' op':'')+(nt.trim()?' hn':'')+'" data-n="'+esc(x.n)+'" data-s="'+esc((x.n+' '+x.d).toLowerCase())+'"><button class="dh" aria-expanded="'+(op?'true':'false')+'"><code'+(c?' style="color:'+c+'"':'')+'>'+esc(x.n)+'</code><span class="dn" role="img" aria-label="Есть заметка">📝</span>'+ico('chev','dc')+'</button><div class="dp"><div class="di"><div class="dx"><p>'+esc(x.d).replace(/\n/g,'<br>')+'</p><textarea class="note" rows="1" maxlength="1000" placeholder="Моя заметка" aria-label="Заметка к '+esc(x.n)+'">'+esc(nt)+'</textarea></div></div></div></div>'});
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
  var o=modal('<div class="bk"><h2>Резервная копия</h2><p>Прогресс и коды из раздела «Код» хранятся только на этом устройстве. Если очистить данные браузера, переустановить приложение или открыть ИТП на другом телефоне, они пропадут. Сохрани копию, чтобы потом загрузить её обратно.</p>'+(fl?'<p class="mu">ИТП открыт как файл. На некоторых устройствах прогресс привязан к месту, где лежит файл: если его переместить или переименовать, прогресс может не найтись. Копия от этого защитит.</p>':'')+(Store.ok()?'':'<p class="mu" style="color:var(--bad)">Браузер не разрешает сохранять данные. Прогресс исчезнет при закрытии страницы, поэтому обязательно сделай копию.</p>')+
    '<div class="lst acts"><button class="li" data-a="s"><span class="lic" aria-hidden="true">💾</span><span class="lt">Сохранить в файл<small>Файл .json в загрузках</small></span></button><button class="li" data-a="l"><span class="lic" aria-hidden="true">📂</span><span class="lt">Загрузить из файла<small>Заменит текущий прогресс</small></span></button><button class="li" data-a="c"><span class="lic" aria-hidden="true">📋</span><span class="lt">Скопировать код сохранения<small>Если с файлами неудобно</small></span></button><button class="li" data-a="p"><span class="lic" aria-hidden="true">📥</span><span class="lt">Вставить код сохранения</span></button></div>'+
    '<textarea id="bkt" hidden placeholder="Вставь сюда код сохранения" aria-label="Код сохранения"></textarea><button class="btn" id="bkg" hidden>Загрузить код</button><p class="mu" style="margin-top:10px;font-size:.84375rem">Файл подписан приложением: если изменить его вручную, он не загрузится.</p></div>',[['Закрыть',null,1]]);
  o.classList.add('as');
  var t=o.querySelector('#bkt'),g=o.querySelector('#bkg');
  function load(txt){var e=importData(txt);if(e){toast(e);return}o.remove();toast('Прогресс загружен');home()}
  o.querySelector('[data-a="s"]').onclick=function(){saveFile('itp-backup-'+day(new Date())+'.json',new Blob([exportData()],{type:'application/json'}));toast('Копия сохранена')};
  o.querySelector('[data-a="l"]').onclick=function(){var f=document.createElement('input');f.type='file';f.accept='.json,application/json,text/plain';f.onchange=function(){var fi=f.files&&f.files[0];if(!fi)return;var r=new FileReader();r.onload=function(){load(String(r.result))};r.readAsText(fi)};f.click()};
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
   • grump (хмурый): первая ошибка в серии (неверный ответ, непрошедший тест, ошибка в программе), статичный;
   • rolled (закатил глаза): один раз, на итоге островка, где ошибок было ROLL_AT и больше;
   • happy (ликующий): итог островка, проекта, уровня, курса; eat (с морковкой): знакомство и приветствие при идущей серии.
   Не больше одного спрайта на момент. Если файла rolled нет в сборке, на его месте стоит grump. */
var PRW=0,CERR=0;
var MOODL={grump:['Хм. Не совсем.','Кролик приподнял бровь.','Почти, но нет.','Бывает. Кролик не в обиде.'],
 rolled:['Кролик закатил глаза, но верит в тебя.','Ну вот опять. Зато теперь запомнишь.','Глубокий вдох. Ещё раз.','Кролик вздохнул. Ты справишься.']};
var MOODI={grump:Math.floor(Math.random()*4),rolled:Math.floor(Math.random()*4)};
function moodLine(k){var a=MOODL[k]||MOODL.grump;return a[MOODI[k]++%a.length]}
/* закатил глаза: только на итоге островка, если на нём ошибок ROLL_AT и больше; хмурый: только первая ошибка в серии */
var ROLL_AT=4;
function errMood(n){return n===1?'grump':''}
function moodBox(k,sz){var s=IMG[k]||IMG.grump;return s?'<span class="mood '+k+(sz?' '+sz:'')+'" aria-hidden="true"><img src="'+s+'" alt="" draggable="false"></span>':''}
function badFb(h,k){return k?h.replace('<div class="fb bad">','<div class="fb bad">'+moodBox(k,'fl')).replace(/<\/div>\s*$/,'<p class="mq">'+moodLine(k)+'</p></div>'):h}
/* консоль: следим за строкой состояния, не трогая движок запуска */
function consWatch(){
  var r=$('rst');if(!r||r._w)return;r._w=1;r._s='';
  new MutationObserver(function(){
    var t=r.textContent;
    if(/выполняется|ждёт ввод/.test(t)){r._s='';return}
    if(/ошибк|не запущена/.test(t)&&r._s!=='e'){
      r._s='e';CERR++;var k=errMood(CERR),q=$('cmq');
      if(q&&k){q.innerHTML=moodBox(k,'sm')+'<span>'+moodLine(k)+' '+(k==='grump'?'Прочитай последнюю строку сообщения: там сказано, что не так.':'Проверь номер строки из сообщения.')+'</span>';q.hidden=false}
      else if(q)q.hidden=true}
    else if(/завершена/.test(t)){CERR=0;r._s='';var q2=$('cmq');if(q2)q2.hidden=true}
  }).observe(r,{childList:true,characterData:true,subtree:true,attributes:true})}
