/* ===================== v5.1.3: ЕГЭ ===================== */
var EXK='ege';
/* пересчёт «обычных» функций так, чтобы экзаменационные темы не мешали обучению Python */
NT=function(){return TOPICS.filter(function(t){return!t.intro&&!t.ex}).length};
ND=function(){return TOPICS.filter(function(t,i){return!t.intro&&!t.ex&&(tdone(i)||i<S.start)}).length};
allDone=function(){return TOPICS.every(function(t,i){return t.intro||t.ex||tdone(i)})};
cur=function(){var ex=S.mode==='ex';for(var i=ex?0:Math.max(S.start,0);i<TOPICS.length;i++){if(!!TOPICS[i].ex!==ex)continue;for(var j=0;j<ni(i);j++)if(!S.d[i+'-'+j])return i+'-'+j}return''};
passed=function(type){var a=[];TOPICS.forEach(function(t,i){if(t.ex)return;(t.items||[]).forEach(function(x,j){if(x.t===type&&S.d[i+'-'+j])a.push([i,j])})});return a};
(function(){
  var io0=isOpen;isOpen=function(i,j){if(!TOPICS[i].ex)return io0(i,j);if(typeof DEV==='function'&&DEV())return 1;return!!S.d[i+'-'+j]||j===0||!!S.d[i+'-'+(j-1)]};
  var v0=vis;vis=function(i){return TOPICS[i].ex?true:v0(i)};
  var sn0=setNav;setNav=function(t){navMode();return sn0(t)};
  var th0=theory;theory=function(i,j){th0(i,j);exImgs(app)};
})();
function navMode(){
  var b=NAV.querySelector('[data-t="mx"]');if(!b)return;
  var ex=S.mode==='ex';b.innerHTML=ex?'<span>🐍</span>Python':'<span>🎓</span>ЕГЭ';document.documentElement.dataset.mode=ex?'ex':'py';
  b.setAttribute('aria-label',ex?'Вернуться к обучению Python':'Подготовка к ЕГЭ по информатике');
}
function modeSwap(){S.mode=S.mode==='ex'?'py':'ex';EXOPEN=-1;save();snd('click');home()}
function exImgs(root){
  ex2Fill(root||app);
  (root||app).querySelectorAll('img[data-x]').forEach(function(im){
    var s=(typeof EXIMG!=='undefined')&&EXIMG[im.dataset.x];if(s&&!im.src)im.src=s;
    im.onclick=function(){modal('<div class="exz"><img src="'+im.src+'" alt="'+esc(im.alt||'')+'"></div><p class="mu" style="margin:8px 0 0;font-size:13px">Рисунок можно прокручивать пальцем.</p>',[['Закрыть',null,1]])};
    im.setAttribute('role','button');im.setAttribute('tabindex','0');
    im.onkeydown=function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();im.click()}};
  });
  (root||app).querySelectorAll('.exf svg').forEach(function(sv){
    sv.style.cursor='zoom-in';sv.onclick=function(){modal('<div class="exz">'+sv.outerHTML+'</div><p class="mu" style="margin:8px 0 0;font-size:13px">Рисунок можно прокручивать пальцем.</p>',[['Закрыть',null,1]])}})}
function exFig(q){if(q.tb)return'<figure class="exf exfw">'+exTb(q.tb)+'</figure>';if(q.db&&window.exDb)return'<figure class="exf exfw exfdb">'+exDb(q.db)+'</figure>';if(q.ct&&window.exTb4)return'<figure class="exf exfw">'+exTb4(q.ct)+'</figure>';if(!q.svg&&!q.img)return'';return q.svg?'<figure class="exf">'+q.svg+'</figure>':'<figure class="exf"><img class="exi" data-x="'+esc(q.img)+'" alt="Схема дорог и таблица к заданию"></figure>'}
var EXOPEN=-1,EXDASH=0;
function exIdx(){var a=[];TOPICS.forEach(function(t,i){if(t.ex===EXK)a.push(i)});return a}
function exCount(i){var c=0;(TOPICS[i].items||[]).forEach(function(x,j){if(S.d[i+'-'+j])c++});return c}
function exShort(n){return String(n).replace(/^Задание\s*\d+\.\s*/,'')}
function exHome(){BACK=exHome;EXOPEN=-1;fzApply();
  var ids=exIdx(),tot=0,dn=0;ids.forEach(function(i){tot+=ni(i);dn+=exCount(i)});
  var p=tot?Math.round(dn/tot*100):0,cu=cur();
  var h=head()+'<section class="exh"><div class="exk">ЕГЭ · информатика</div><h2>Подготовка к экзамену</h2><p>Теория, разбор и тренировки по каждому заданию. Когда разберёшься, задания можно решать бесконечно.</p><div class="bar" aria-label="Пройдено уроков"><i style="width:'+p+'%"></i></div><div class="exhs"><span>Пройдено уроков: <b>'+dn+'</b> из '+tot+'</span></div>'+(cu?'<button class="btn" id="exgo">'+(dn?'Продолжить':'Начать с первого задания')+'</button>':'')+'</section>';
  h+='<button class="extr" id="exm"><span class="lic">🎲</span><span class="lt">Бесконечный тренажёр<small>Новые задания каждый раз, опыт не начисляется</small></span><span class="ch">›</span></button>';
  h+='<h3 class="exh3">Задания</h3><div class="exl">';
  ids.forEach(function(i){var t=TOPICS[i],n=ni(i),c=exCount(i),m=String(t.n).match(/^Задание\s*(\d+)/),done=c>=n;
    h+='<button class="ext'+(done?' ok':'')+'" data-i="'+i+'"><span class="exn">'+(m?m[1]:'•')+'</span><span class="lt">'+esc(exShort(t.n))+'<small>'+esc(t.s||'')+'</small><span class="bar"><i style="width:'+Math.round(c/n*100)+'%"></i></span></span><span class="lv">'+(done?'✓':c+'/'+n)+'</span></button>'});
  h+='</div><p class="mu exnote">Новые задания добавляются по мере готовности.</p>';
  show(h,'home');bindHead(exHome);
  var g=$('exgo');if(g)g.onclick=function(){var k=cur();if(!k)return;var q=k.split('-');EXOPEN=+q[0];BACK=function(){exTopic(EXOPEN)};go(+q[0],+q[1])};
  $('exm').onclick=function(){EXDASH=1;exMenu()};
  app.querySelectorAll('.ext').forEach(function(b){b.onclick=function(){exTopic(+b.dataset.i)}});
}
function exTopic(i){EXOPEN=i;BACK=function(){exTopic(EXOPEN)};fzApply();
  var t=TOPICS[i],n=ni(i),c=exCount(i),m=String(t.n).match(/^Задание\s*(\d+)/),cu='';for(var u=0;u<n;u++)if(!S.d[i+'-'+u]){cu=i+'-'+u;break}
  var h=head()+'<button class="exbk" id="exbk">‹ Все задания</button><section class="exh sm"><div class="exk">Задание '+(m?m[1]:'')+'</div><h2>'+esc(exShort(t.n))+'</h2><div class="bar"><i style="width:'+Math.round(c/n*100)+'%"></i></div><div class="exhs"><span>Пройдено: <b>'+c+'</b> из '+n+'</span></div></section>';
  var gs=[],gm={};
  for(var j=0;j<n;j++){var it=IT(i,j),g=it.g||'Уроки';if(!(g in gm)){gm[g]=gs.length;gs.push({n:g,a:[]})}gs[gm[g]].a.push(j)}
  var ic={theory:'📖',flash:'✏️',ans:'🎓',test:'💻'},lbl={theory:'Теория',flash:'Вопросы',ans:'Тренировка',test:'Код'};
  gs.forEach(function(G){
    var d=G.a.filter(function(j){return S.d[i+'-'+j]}).length;
    h+='<h3 class="exh3">'+esc(G.n)+'<span>'+d+'/'+G.a.length+'</span></h3><div class="exl">';
    G.a.forEach(function(j){var it=IT(i,j),k=i+'-'+j,dn=S.d[k],op=isOpen(i,j);
      h+='<button class="exlt '+(dn?'dn':(op?(cu===k?'cur':'op'):'lk'))+'" data-j="'+j+'"'+(op||dn?'':' aria-disabled="true"')+'><span class="exic">'+(dn?'✓':ic[it.t]||'•')+'</span><span class="lt">'+esc(it.n||'')+'<small>'+(lbl[it.t]||'')+(dn?' · пройдено':(op?'':' · закрыто'))+'</small></span><span class="ch">'+(op||dn?'›':'🔒')+'</span></button>'});
    h+='</div>'});
  show(h,'home');bindHead(function(){exTopic(EXOPEN)});
  $('exbk').onclick=exHome;
  app.querySelectorAll('.exlt').forEach(function(b){b.onclick=function(){go(i,+b.dataset.j)}});
  var c0=app.querySelector('.exlt.cur');if(c0&&!RM())try{c0.scrollIntoView({block:'center'})}catch(e){}
}
(function(){var h0=home;home=function(){if(S.mode!=='ex'||PE.length)return h0();EXOPEN>=0?exTopic(EXOPEN):exHome()}})();
function exBind(){}
/* нормализация ответа: регистр, пробелы, похожие русские и латинские буквы */
var EXL={'А':'A','В':'B','Е':'E','К':'K','М':'M','Н':'H','О':'O','Р':'P','С':'C','Т':'T','У':'Y','Х':'X'};
function normAns(s){return String(s||'').toUpperCase().replace(/[\s,.;:]+/g,'').replace(/[А-ЯЁ]/g,function(c){return EXL[c]||c})}
var EXDIFF={'1.1':3,'1.2':4,'1.3':2,'1.4':3,'1.5':4,'1.6':2,'2.1':2,'2.2':2,'2.3':3,'2.4':4,'2.5':4,'2.6':1,'3.1':3,'3.2':3,'3.3':3,'3.4':2,'3.5':3,'3.6':3,'4.1':2,'4.2':3,'4.3':3,'4.4':3,'4.5':1,'4.6':3,'4.7':4,'5.1':2,'5.2':2,'5.3':3,'5.4':3,'5.5':4,'5.6':3,'5.7':4,'6.1':2,'6.2':2,'6.3':4,'6.4':3,'6.5':3,'6.6':3},EXDN=['','очень лёгкое','лёгкое','среднее','сложное','очень сложное'];
function exDf(q){var d=q.d||EXDIFF[q.type]||0;if(!d)return'';var s='';for(var i=1;i<=5;i++)s+='<i'+(i<=d?' class="on"':'')+'></i>';return'<span class="exdf" title="Сложность: '+EXDN[d]+'" aria-label="Сложность: '+EXDN[d]+'">'+s+'<em>'+EXDN[d]+'</em></span>'}
function exStmt(q,label){
  var h='<section class="exst"><div class="exlab">'+esc(label)+exDf(q)+'</div>';
  if(q.expr){h+='<div class="exfx"><span>F</span> = '+esc(q.expr)+'</div><p class="exlead">'+(q.tb?'Определи, какому столбцу соответствует каждая переменная.':'Построй таблицу истинности и запиши значения F.')+'</p><details class="exdt"><summary>Полное условие</summary><p>'+esc(q.q)+'</p></details>'}
  else if(q.pr)h+=(q.q?'<details class="exdt"><summary>Условие исполнителя</summary><p>'+esc(q.q)+'</p></details>':'')+'<pre class="expr'+(q.pl?' pro':'')+'">'+esc(q.pr)+'</pre><h2 class="exq">'+esc(q.qq)+'</h2>';
  else h+='<h2 class="exq">'+esc(q.q)+'</h2>';
  return h+'</section>'}
function exAsk(q,hint){
  return'<div class="exfmt">'+esc(q.f)+'</div><form class="exin" id="af" autocomplete="off"><input class="f" id="ai" placeholder="Твой ответ" autocomplete="off" autocapitalize="characters" spellcheck="false" '+(/^\d+$/.test(q.a)&&q.a.length<5?'inputmode="numeric"':'')+' aria-label="Ответ"><button class="btn" type="submit" id="ac">Проверить</button></form>'+hint+'<div id="hint"></div><div id="fb"></div>'}
function exStart(q){return'# Пиши код здесь\n'+(q.expr?'# F = '+q.expr+'\n':'')+(q.starter||'')}
function exProg(k,n){var h='<div class="exprog" aria-label="Задание '+(k+1)+' из '+n+'">';for(var u=0;u<n;u++)h+='<i class="'+(u<k?'d':u===k?'c':'')+'"></i>';return h+'</div>'}
function exSol(q){
  return'<section class="exsol"><h3>Как решать</h3><ol class="exs">'+q.s.map(function(x){return'<li>'+esc(x)+'</li>'}).join('')+'</ol></section>'+(q.m?'<div class="exwarn"><b>Частая ошибка</b><p>'+esc(q.m)+'</p></div>':'')+(q.alt?'<div class="exalt"><b>Другой способ</b><p>'+esc(q.alt)+'</p></div>':'')}
function exRes(q,ok,btn){
  return'<div class="exres '+(ok?'ok':'no')+'"><div class="exv">'+(ok?'✓ Верно!':'Разбор задания')+'</div><div class="exan"><span>Ответ</span><b>'+esc(q.a)+'</b></div><button class="btn pulse" id="nx">'+btn+'</button></div>'+exSol(q)}

/* ---------- рисование поверх условия и свой код ---------- */
var EXDR={},EXCD={};
function exDraw(q,label){
  return'<div class="exdraw" id="exd">'+exStmt(q,label)+exFig(q)+'</div><div class="extl" role="group" aria-label="Инструменты"><button id="exbd" aria-pressed="false"><span>✏️</span>Рисовать</button>'+(q.db?'<button id="exbs" aria-pressed="false"><span>📊</span>Таблица</button>':'<button id="exbc" aria-pressed="false"><span>💻</span>Код</button>')+(q.tu?'<button id="exbt"><span>🐢</span>Черепаха</button>':'')+'</div><div class="expal" id="expal" hidden></div>'+(q.db?'<div class="exsh" id="exsh" hidden></div>':'')+'<div class="excode" id="excode" hidden>'+edHtml('')+'<div class="row"><button class="btn g" id="run">Запустить</button></div><pre class="out" id="o" style="margin-top:10px;display:none"></pre>'+IOHTML+'</div>'}
function exTools(key,starter,q){
  var d=$('exd'),cv=document.createElement('canvas'),dpr=window.devicePixelRatio||1;cv.className='exc';cv.setAttribute('aria-hidden','true');d.appendChild(cv);
  var ctx=cv.getContext('2d'),st=EXDR[key]=EXDR[key]||[],col='#E5484D',wd=3,er=false,on=false,cur=null;
  function size(){var r=d.getBoundingClientRect();if(!r.width)return;cv.width=Math.round(r.width*dpr);cv.height=Math.round(r.height*dpr);cv.style.width=r.width+'px';cv.style.height=r.height+'px';redraw()}
  function seg(s,a,b){ctx.save();ctx.lineCap='round';ctx.lineJoin='round';ctx.lineWidth=s.w*dpr*(s.e?4:1);ctx.strokeStyle=s.c;ctx.globalCompositeOperation=s.e?'destination-out':'source-over';
    ctx.beginPath();ctx.moveTo(a[0]*cv.width,a[1]*cv.height);ctx.lineTo(b[0]*cv.width+.01,b[1]*cv.height);ctx.stroke();ctx.restore()}
  function redraw(){ctx.clearRect(0,0,cv.width,cv.height);st.forEach(function(s){for(var i=0;i<s.p.length;i++)seg(s,s.p[Math.max(0,i-1)],s.p[i])})}
  function pt(e){var r=cv.getBoundingClientRect();return[(e.clientX-r.left)/r.width,(e.clientY-r.top)/r.height]}
  cv.onpointerdown=function(e){if(!on)return;e.preventDefault();try{cv.setPointerCapture(e.pointerId)}catch(x){}cur={c:col,w:wd,e:er,p:[pt(e)]};st.push(cur);seg(cur,cur.p[0],cur.p[0])};
  cv.onpointermove=function(e){if(!cur)return;e.preventDefault();var p=pt(e),l=cur.p[cur.p.length-1];cur.p.push(p);seg(cur,l,p)};
  cv.onpointerup=cv.onpointercancel=function(){cur=null};
  if(window.ResizeObserver)new ResizeObserver(size).observe(d);else window.addEventListener('resize',size);
  size();
  var pal=$('expal'),bd=$('exbd'),bc=$('exbc');
  var sw=['#E5484D','#2F7BEF','#2E9E4F','#F5A623'];
  pal.innerHTML=sw.map(function(c,n){return'<button class="exsw'+(n?'':' on')+'" data-c="'+c+'" style="--c:'+c+'" aria-label="Цвет '+(n+1)+'"></button>'}).join('')+'<button data-a="e" aria-label="Ластик" aria-pressed="false">🧽</button><button data-a="w" aria-label="Толщина линии">━</button><button data-a="u" aria-label="Отменить штрих">↶</button><button data-a="x" aria-label="Стереть всё">🗑</button>';
  pal.onclick=function(e){var b=e.target.closest('button');if(!b)return;
    if(b.dataset.c){col=b.dataset.c;er=false;pal.querySelectorAll('.exsw,[data-a=e]').forEach(function(x){x.classList.remove('on')});b.classList.add('on');pal.querySelector('[data-a=e]').setAttribute('aria-pressed','false')}
    else if(b.dataset.a==='e'){er=!er;b.classList.toggle('on',er);b.setAttribute('aria-pressed',er);pal.querySelectorAll('.exsw').forEach(function(x){x.classList.toggle('dim',er)})}
    else if(b.dataset.a==='w'){wd=wd===3?6:3;b.style.fontSize=wd===3?'':'1.5em'}
    else if(b.dataset.a==='u'){st.pop();redraw()}
    else if(b.dataset.a==='x'){st.length=0;redraw()}};
  function setDraw(v){on=v;bd.classList.toggle('on',v);bd.setAttribute('aria-pressed',v);pal.hidden=!v;d.classList.toggle('drawing',v);cv.style.pointerEvents=v?'auto':'none';cv.style.touchAction=v?'none':'auto';setTimeout(size,0)}
  bd.onclick=function(){setDraw(!on)};
  setDraw(false);
  /* код */
  var box=$('excode'),c=$('code'),sync=null,sv=EXCD[key];
  c.value=sv!==undefined?sv:starter;
  sync=initEd(c,function(){EXCD[key]=c.value.slice(0,4000)});
  if(bc)bc.onclick=function(){var v=box.hidden;box.hidden=!v;bc.classList.toggle('on',v);bc.setAttribute('aria-pressed',v);if(v){sync();if(!/Mobi|Android/i.test(navigator.userAgent))c.focus()}};
  var bt=$('exbt');if(bt&&q&&q.tu)bt.onclick=function(){snd('click');if(window.TW)TW.run(q.tu,function(m){toast(m)})};
  if(window.exSheetInit&&q)exSheetInit(key,q);
  $('run').onclick=function(){var o=$('o');if(!SKOK){o.style.display='block';o.textContent='Загружаю среду Python…'}needSk().then(function(ok){if(ok)liveRun(c.value)})};
  skReady();
}
function ansTask(i,j,k){
  var it=IT(i,j),T=it.tasks,q=T[k],key=i+'-'+j,tk=key+'-'+k,tries=0,hn=0,fin=!!S.tk[tk];if(q.expr&&!q.s)exFill2(q);if(q.query&&q.no===6&&window.exFill6)exFill6(q);else if(q.query&&q.no===5&&window.exFill5)exFill5(q);else if(q.query&&q.db&&window.exFill3)exFill3(q);else if(q.query&&window.exFill4)exFill4(q);
  DVC={t:'ans',i:i,j:j,k:k};
  var hasH=q.h&&q.h.length;
  show('<div class="top"><button class="icon" id="x" aria-label="Назад">✕</button>'+(T.length<=12?exProg(k,T.length):'<span class="chip">Задание '+(k+1)+' из '+T.length+'</span>')+'</div>'+exDraw(q,'Тренировка · задание '+(k+1)+' из '+T.length)+exAsk(q,(hasH?'<button class="btn g exhb" id="hb">💡 Подсказка</button>':'')));
  exImgs(app);exTools('a'+key+'-'+k,exStart(q),q);
  $('x').onclick=goBack;
  var ai=$('ai'),fb=$('fb'),ac=$('ac');
  function showHints(){
    var h='';for(var n=0;n<hn;n++)h+='<div class="exh1"><b>Подсказка '+(n+1)+' из '+q.h.length+'</b>'+esc(q.h[n])+'</div>';
    if(hn)h+='<p class="mu exnoteh">Опыт за эту тренировку: 50% от максимума.</p>';
    $('hint').innerHTML=h;var b=$('hb');if(b){if(hn>=q.h.length){b.disabled=true;b.textContent='💡 Подсказки закончились'}else b.textContent='💡 Ещё подсказка ('+(hn+1)+'/'+q.h.length+')'}}
  if(hasH){
    if(HINT){hn=1;showHints()}
    $('hb').onclick=function(){
      var use=function(){S.hc=1;S.hu[i]=1;HINT=1;drc(i,j,k);save();hn=Math.min(q.h.length,hn+1);showHints()};
      if(HINT||S.hc)use();else modal('<h2 style="font-size:20px">Использовать подсказку?</h2><p>Вы уверены, что хотите использовать подсказку? Учтите, вам дадут лишь 50% от максимального опыта.</p><p class="mu">Учтите, в последующие разы подтверждения не будет.</p>',[['Использовать подсказку',use],['Отмена',null,1]])}}
  function solution(){return''}
  function next(ok){
    fin=true;S.tk[tk]=1;save();ai.disabled=true;ac.disabled=true;
    var last=k===T.length-1;
    fb.innerHTML=exRes(q,ok,last?'Закончить':'Дальше');
    $('nx').onclick=function(){if(last)ansEnd(i,j);else ansTask(i,j,k+1)};
    try{fb.scrollIntoView({block:'start',behavior:'smooth'})}catch(e){}}
  if(fin){next(false);return}
  $('af').onsubmit=function(e){
    e.preventDefault();if(fin)return;var v=normAns(ai.value);if(!v)return;
    if(v===normAns(q.a)){fx(true);next(true);return}
    ERR++;tries++;drc(i,j,k);fx(false);
    var msg=tries===1?'Проверь формат ответа: '+q.f:(tries===2&&q.m?'Частая ошибка в этом типе: '+q.m:'Попробуй ещё раз или возьми подсказку.');
    fb.innerHTML='<div class="exwr"><b>Не совпало</b>'+esc(msg)+'</div>'+(tries>=3?'<button class="btn g" id="gv">Показать разбор и пойти дальше</button>':'');
    if(tries>=3)$('gv').onclick=function(){next(false)};
    ai.focus();ai.select()};
  if(!/Mobi|Android/i.test(navigator.userAgent))ai.focus();
}
function ansEnd(i,j){
  var key=i+'-'+j,tj0=tdone(i);rec(key,ERR);bump(key);var a=award(key,60,ERR,0,HINT?.5:1),tj=!tj0&&tdone(i);
  show('<div class="center">'+rabbit('happy')+'<h2>Тренировка пройдена</h2><p>Ошибок: '+ERR+' · Опыт: +'+a.x+' ⭐'+(HINT?' (с подсказкой: 50%)':'')+'</p><p>'+esc(a.note)+'</p>'+(tj?'<p><b>🎉 «'+esc(TOPICS[i].n)+'» пройдено!</b></p>':'')+(a.lv?'<p><b>⬆️ Новый уровень: '+a.lv+'</b></p>':'')+xpStrip()+'<button class="btn pulse" id="go">Дальше</button></div>');
  HINT=0;$('go').onclick=goBack;
  if(tj||a.lv)confetti(1);
}

/* ---------- бесконечный тренажёр ---------- */
var EXST={ok:0,all:0};
function exMenu(){BACK=exMenu;document.documentElement.dataset.tr=EXDASH?'1':'';
  var h=head('Тренажёр')+'<section class="exh sm"><div class="exk">ЕГЭ · бесконечные задания</div><p style="margin:6px 0 0">Задания создаются заново каждый раз, поэтому их можно решать сколько угодно. Опыт не начисляется, прогресс и серия не меняются.</p></section>';
  Object.keys(EXGEN).forEach(function(no){var g=EXGEN[no];
    h+='<h3 class="exh3">Задание №'+g.no+'. '+esc(g.name)+'</h3><div class="exl"><button class="ext" data-a="t:'+no+':any"><span class="exn">🎲</span><span class="lt">Любой тип<small>Случайные задания всех типов</small></span><span class="ch">›</span></button>'+g.types.map(function(t){return'<button class="ext" data-a="t:'+no+':'+t.id+'"><span class="exn s">'+esc(t.id.split('.')[1])+'</span><span class="lt">'+esc(t.n)+'<small>'+esc(t.d)+'</small></span><span class="ch">›</span></button>'}).join('')+'</div>'});
  h+='<p class="mu exnote">Остальные задания ЕГЭ появятся здесь по мере добавления в приложение.</p>';
  show(h,EXDASH?'home':'pr');bindHead(exMenu);
  app.querySelectorAll('.ext').forEach(function(b){b.onclick=function(){var p=b.dataset.a.split(':');EXST={ok:0,all:0};exTrain(+p[1],p[2])}})}
function exTrain(no,type){
  var g=EXGEN[no],q=null;
  for(var n=0;n<5&&!q;n++)q=g.make(type);
  if(!q){toast('Не удалось создать задание, попробуй ещё раз');return exMenu()}
  var tries=0,hn=0,fin=false;
  show('<div class="top"><button class="icon" id="x" aria-label="К выбору типа">✕</button><span class="chip s">🎲 '+EXST.ok+' из '+EXST.all+'</span></div>'+exDraw(q,'Тренажёр · задание №'+no+(q.type?' · тип '+q.type:''))+exAsk(q,'<div class="row"><button class="btn g" id="hb">💡 Подсказка</button><button class="btn g" id="sk">Пропустить</button></div>'));
  exImgs(app);exTools('t'+Date.now(),exStart(q),q);
  $('x').onclick=exMenu;
  var ai=$('ai'),fb=$('fb');
  function chip(){var c=app.querySelector('.chip.s');if(c)c.textContent='🎲 '+EXST.ok+' из '+EXST.all}
  function solution(){return''}
  function end(ok){fin=true;EXST.all++;if(ok){EXST.ok++;rcInc()}chip();ai.disabled=true;$('ac').disabled=true;$('hb').disabled=true;$('sk').disabled=true;
    fb.innerHTML=exRes(q,ok,'Следующее задание');
    $('nx').onclick=function(){exTrain(no,type)};try{fb.scrollIntoView({block:'start',behavior:'smooth'})}catch(e){}}
  $('hb').onclick=function(){hn=Math.min(q.h.length,hn+1);var h='';for(var i=0;i<hn;i++)h+='<div class="exh1"><b>Подсказка '+(i+1)+' из '+q.h.length+'</b>'+esc(q.h[i])+'</div>';$('hint').innerHTML=h;if(hn>=q.h.length){$('hb').disabled=true;$('hb').textContent='💡 Подсказки закончились'}else $('hb').textContent='💡 Ещё подсказка ('+(hn+1)+'/'+q.h.length+')'};
  $('sk').onclick=function(){if(!fin)end(false)};
  $('af').onsubmit=function(e){e.preventDefault();if(fin)return;var v=normAns(ai.value);if(!v)return;
    if(v===normAns(q.a)){fx(true);end(true);return}
    tries++;fx(false);fb.innerHTML='<div class="exwr"><b>Не совпало</b>'+esc(tries===1?'Проверь формат ответа: '+q.f:(tries===2&&q.m?'Частая ошибка в этом типе: '+q.m:'Попробуй ещё раз, возьми подсказку или нажми «Пропустить», чтобы увидеть разбор.'))+'</div>';ai.focus();ai.select()};
  if(!/Mobi|Android/i.test(navigator.userAgent))ai.focus();
}
