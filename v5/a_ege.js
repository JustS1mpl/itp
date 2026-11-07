/* ===================== 7.3.0: ЕГЭ по информатике =====================
   Три норы (course/c_h_ege1..3.py): каждый номер — глава из двух островков теории. Первый островок любой главы открыт
   сразу, как в основном пути можно начать любую тему. Прочитал первую теорию номера — его задачи появляются в «Практике»
   в ЕГЭ-тренажёре: бесконечный режим, ввод ответа, ссылка на условие и разбор на КомпЕГЭ. Опыт не начисляется.
   Задачи главы лежат в поле pr её первого островка; у островков главы есть ch (номер), у первого — cht (название). */

/* mv:7 — норы «Черепаха» (тема 10) и «IP-адреса» (40) заменены тремя норами ЕГЭ: прогресс в убранных норах
   выбрасывается, остальные темы переезжают на новые номера. Таблица: старый номер → новый (−1 — норы больше нет).
   Функция, а не var: clean() зовёт её при загрузке раньше, чем выполняются var */
function migr7(r){
  if(!r||typeof r!=='object'||Array.isArray(r)||!(r.mv>=5)||r.mv>=7)return r;
  var M=[0,1,2,3,4,5,6,7,8,9,-1,10,11,12,13,14,15,16,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,34,36,37,38,39,40,41,-1,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61];
  var m=function(i){return i<M.length?M[i]:-1},o={},xd=0;
  /* опыт за островки убранных нор остаётся, а отметки уходят — запоминаем, сколько его могло быть (с запасом: проект до 200) */
  if(r.at&&typeof r.at==='object')for(var ak in r.at){var ap=ak.split('-');if(/^\d+$/.test(ap[0])&&m(+ap[0])<0)xd+=r.at[ak]==='full'?200:r.at[ak]==='low'?2:0}
  if(xd)o.xd=(Number.isInteger(r.xd)?r.xd:0)+xd;
  for(var k in r)if(Object.prototype.hasOwnProperty.call(r,k))o[k]=r[k];
  ['d','tk','at','es','dr','hu'].forEach(function(f){var x=r[f];if(!x||typeof x!=='object'||Array.isArray(x))return;var y={};
    Object.keys(x).forEach(function(key){var p=key.split('-');if(!/^\d+$/.test(p[0]))return;var n=m(+p[0]);if(n<0)return;p[0]=String(n);y[p.join('-')]=x[key]});o[f]=y});
  if(Number.isInteger(r.start)&&r.start>=0){var s=m(r.start);o.start=s<0?0:s}
  o.mv=7;return o}

/* глава ЕГЭ: первый островок открыт всегда, следующие — по порядку внутри главы */
(function(){var _o=isOpen;isOpen=function(i,j){
  var t=TOPICS[i],it=t&&t.items&&t.items[j];
  if(t&&t.opt&&it&&it.ch){
    if(S.d[i+'-'+j]||(typeof DEV==='function'&&DEV())||TCH())return 1;
    var p=t.items[j-1];if(!p||p.ch!==it.ch)return 1;
    return S.d[i+'-'+(j-1)]?1:0}
  return _o(i,j)}})();

/* заголовок главы над её первым островком */
(function(){var _is=island;island=function(i,j,n,dx){
  var h=_is(i,j,n,dx),it=IT(i,j);
  return it&&it.cht&&TOPICS[i].opt?'<h3 class="ech"><small>Задание №'+it.ch+'</small>'+esc(it.cht)+'</h3>'+h:h}})();

/* открытые главы: прочитан первый островок (или учительский ник) */
function egeOpen(){
  var a=[];TOPICS.forEach(function(t,i){if(!t.opt)return;(t.items||[]).forEach(function(x,j){if(x.pr&&(S.d[i+'-'+j]||TCH()))a.push({n:x.ch,t:x.cht,pr:x.pr})})});
  return a.sort(function(p,q){return p.n-q.n})}

(function(){var _p=practice;practice=function(){
  _p();var a=egeOpen(),pc=app.querySelector('.prc');if(!pc)return;
  var b=document.createElement('button');b.className='pcard ege';
  b.innerHTML='<span class="pic" aria-hidden="true">🎓</span><b>ЕГЭ-тренажёр</b><small>'+(a.length?'Задания '+a.map(function(x){return'№'+x.n}).join(', ')+' — без конца, из открытых глав':'Прочитай первую теорию любого задания в норах «ЕГЭ» — и его задачи появятся здесь')+'</small><span class="go">'+(a.length?'Решать'+ico('chev'):ico('lock')+'Пока нет открытых глав')+'</span>';
  if(!a.length){b.disabled=true;b.setAttribute('aria-disabled','true')}
  b.onclick=function(){if(!b.disabled)egeHome()};
  pc.appendChild(b)}})();

var EGE={r:0,t:0,seen:[],nums:null,code:{}};
function egeHome(){BACK=egeHome;
  var a=egeOpen();if(!a.length)return practice();
  var h='<div class="top ls"><button class="icon" id="x" aria-label="Назад">'+ico('x')+'</button><div class="grow"></div></div>'+ttl('ЕГЭ-тренажёр','Задачи с экзаменов и сборника КомпЕГЭ. Реши у себя (в «Коде» или своём редакторе) и впиши ответ. Опыт не начисляется.')+
   '<div class="lst egl0"><button class="li" data-n="all"><span class="lic" aria-hidden="true">🎲</span><span class="lt">Все открытые вперемешку<small>'+a.length+' '+pl(a.length,['номер','номера','номеров'])+'</small></span>'+ico('chev','ch')+'</button>'+
   a.map(function(x){return'<button class="li" data-n="'+x.n+'"><span class="lic egn" aria-hidden="true">'+x.n+'</span><span class="lt">'+esc(x.t)+'<small>Задание №'+x.n+' · '+x.pr.length+' '+pl(x.pr.length,['задача','задачи','задач'])+'</small></span>'+ico('chev','ch')+'</button>'}).join('')+'</div>';
  scr('egeh',h,'pr');
  $('x').onclick=practice;
  app.querySelectorAll('.egl0 .li').forEach(function(b){b.onclick=function(){var n=b.dataset.n;EGE.nums=n==='all'?null:[+n];EGE.r=0;EGE.t=0;rndWarn(egeNext)}})}
function egeNorm(s){return String(s).toLowerCase().replace(/ё/g,'е').split(/[\s;,]+/).filter(Boolean).join(' ')}
function egeNext(){
  var a=egeOpen().filter(function(x){return!EGE.nums||EGE.nums.indexOf(x.n)>=0}),P=[];
  a.forEach(function(x){x.pr.forEach(function(p){P.push({n:x.n,p:p})})});
  if(!P.length)return egeHome();
  var fresh=P.filter(function(x){return EGE.seen.indexOf(x.p.id)<0});if(!fresh.length){EGE.seen=[];fresh=P}
  var x=fresh[Math.floor(Math.random()*fresh.length)],p=x.p;EGE.seen.push(p.id);if(EGE.seen.length>Math.max(1,P.length-1))EGE.seen.shift();
  var h='<div class="top ls"><button class="icon" id="x" aria-label="Выйти">'+ico('x')+'</button><div class="grow"><span class="lstep">🎓 Верно '+EGE.r+' из '+EGE.t+'</span></div></div>'+
   '<h1 class="egh">Задание №'+x.n+'<small>'+esc(p.src)+(p.st?' · '+esc(p.st):'')+'</small></h1>'+
   '<div class="th egt">'+p.h+'</div>'+
   (p.f?'<div class="egf">'+p.f.map(function(f){return'<a class="btn t sm" href="'+esc(f[1])+'" data-ext="1">📎 '+esc(f[0])+'</a>'}).join('')+'<p class="mu">Файл скачивается с сайта КомпЕГЭ — нужен интернет.</p></div>':'')+
   '<p class="egs">Источник: <a href="'+esc(p.u)+'" data-ext="1">КомпЕГЭ, задача '+esc(p.u.split('id=')[1]||'')+'</a></p>'+
   /* компилятор прямо под условием: тот же редактор и консоль, что в разделе «Код»; код задачи помнится, пока открыт тренажёр */
   '<div class="egcode"><div class="edc ec"><div class="edh"><span class="egct">💻 Реши здесь</span>'+runBtn(1)+'</div>'+edHtml(EGE.code[p.id]||'# Пиши решение здесь\n')+'</div>'+conHtml()+'</div>'+
   '<label class="egin"><span>Ответ</span><input id="ega" class="inp" autocomplete="off" autocapitalize="off" spellcheck="false" inputmode="text" placeholder="Например: 516"></label>';
  scr('eget',h+dockHtml('<button class="btn" id="go" disabled>Проверить</button>',0,1),'pr');
  if(typeof imgZoom==='function')imgZoom(app);
  /* длинное условие — свёрнуто до нескольких строк, раскрывается по кнопке */
  var et=app.querySelector('.egt');
  if(et&&et.scrollHeight>230){et.classList.add('cl');var mb=document.createElement('button');mb.className='egmore';mb.type='button';mb.textContent='Показать условие целиком';
    mb.onclick=function(){var c=et.classList.toggle('cl');mb.textContent=c?'Показать условие целиком':'Свернуть условие'};et.after(mb)}
  var cd=$('code'),ced=cd.closest('.ed');if(ced)ced.dataset.min=180;
  initEd(cd,function(){EGE.code[p.id]=cd.value.slice(0,4000)})();
  $('run').onclick=function(){var o=$('o');$('cons').hidden=false;if(!SKOK){o.textContent='Загружаю среду Python…'}skReady().then(function(ok){if(!ok){o.textContent='Среда Python не загрузилась. Нажми «Запустить» ещё раз.';return}liveRun(cd.value)})};
  app.querySelectorAll('a[data-ext],a.egl').forEach(function(l){l.onclick=function(e){e.preventDefault();openExt(l.getAttribute('href'))}});
  $('x').onclick=egeHome;
  var g=$('go'),inp=$('ega'),ch=false;
  inp.oninput=function(){g.disabled=!inp.value.trim()};
  inp.onkeydown=function(e){if(e.key==='Enter'&&!g.disabled){e.preventDefault();g.click()}};
  g.onclick=function(){
    if(ch){egeNext();return}
    ch=true;var ok=egeNorm(inp.value)===egeNorm(p.a);fx(ok);EGE.t++;if(ok){EGE.r++;rcInc()}inp.disabled=true;
    dockState(ok,ok?'Верно!':'Неверно','Ответ: <b>'+esc(p.a)+'</b>. <a href="'+esc(p.tu)+'" data-ext="1">Разбор с кодом — у ИИ-тьютора КомпЕГЭ</a>',ok?'':errMood(1));
    var d=$('fb');if(d)d.querySelectorAll('a[data-ext]').forEach(function(l){l.onclick=function(e){e.preventDefault();openExt(l.getAttribute('href'))}});
    g.textContent='Дальше';g.focus()};
  setTimeout(function(){try{inp.focus({preventScroll:true})}catch(e){}},50)}
/* у нор ЕГЭ короткое имя — целиком («ЕГЭ: код решает»), иначе все три подписаны просто «ЕГЭ» */
(function(){var _hn=holeName;holeName=function(t){return /^ЕГЭ:/.test(String(t&&t.n||''))?String(t.n):_hn(t)}})();
