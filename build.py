import re, sys, importlib
sys.path.insert(0, '.')
import dsl

VER = '4.3.0'
s = open('orig.html', encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, ('якорь найден %d раз(а), нужно %d' % (c, n), a[:90])
    s = s.replace(a, b)


rep('4.0.1', VER, s.count('4.0.1'))

# ---------- CSS ----------
rep('@media (hover:hover) and (pointer:fine){.kb{display:grid}}', 'html.kbd .kb{display:grid}')
CSS = r"""
/* ===== v4.1.3 ===== */
.ty-t{--ti:#3B82F6}.ty-f{--ti:var(--accent)}.ty-c{--ti:#E8842A}.ty-p{--ti:#D6457A}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .ty-t{--ti:#6FA8FF}:root:not([data-theme="light"]) .ty-c{--ti:#F2A154}:root:not([data-theme="light"]) .ty-p{--ti:#F27AA6}}
:root[data-theme="dark"] .ty-t{--ti:#6FA8FF}:root[data-theme="dark"] .ty-c{--ti:#F2A154}:root[data-theme="dark"] .ty-p{--ti:#F27AA6}
.isl.op path{fill:var(--soft);stroke:var(--soft)}
@supports (background:color-mix(in srgb,red 50%,blue)){.isl.op path{fill:color-mix(in srgb,var(--ti) 26%,var(--card));stroke:color-mix(in srgb,var(--ti) 26%,var(--card))}}
.isl.dn path,.isl.cur path,.isl path.gl{fill:var(--ti);stroke:var(--ti)}
.isl.cur path.gl{animation-name:glow2}
@keyframes glow2{from{filter:drop-shadow(0 0 2px var(--ti))}to{filter:drop-shadow(0 0 9px var(--ti))}}
.isl .bd{position:absolute;right:6px;top:-2px;width:26px;height:26px;border-radius:50%;background:var(--card);border:2px solid var(--line);display:grid;place-items:center;font-size:13px;font-style:normal;font-weight:800;line-height:1}
.isl .bd.ok{background:var(--ok);border-color:var(--ok);color:#fff}
.isl.lk .ic{opacity:.4}
.ilw.wait .isl .bd{opacity:.4}
:root{--b0:var(--bi);--b1:#0369A1;--b2:#15803D;--b3:#BE185D;--ka:#5E7F00}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--b1:#7DD3FC;--b2:#86EFAC;--b3:#F9A8D4;--ka:#B5D63D}}
:root[data-theme="dark"]{--b1:#7DD3FC;--b2:#86EFAC;--b3:#F9A8D4;--ka:#B5D63D}
:root[data-theme="light"]{--b1:#0369A1;--b2:#15803D;--b3:#BE185D;--ka:#5E7F00}
.b0{color:var(--b0)}.b1{color:var(--b1)}.b2{color:var(--b2)}.b3{color:var(--b3)}.bx{color:var(--bad);text-decoration:underline wavy}
.ka{color:var(--ka);font-weight:700}.fe{color:var(--fs)}.es{color:var(--nm);font-weight:800}
.th h3{font-size:18px;margin:20px 0 8px;font-weight:800}
.th ul,.th ol{margin:0 0 12px;padding-left:22px}.th li{margin:0 0 6px}
.th table{border-collapse:collapse;margin:0 0 14px;font-size:15px;width:100%}
.th td,.th th{border:1px solid var(--line);padding:6px 10px;text-align:left}.th th{background:var(--soft)}
.th pre.out,.th pre.pin{position:relative;margin-top:-6px;padding-top:30px;background:transparent;border:2px dashed var(--line)}
.th pre.out::before,.th pre.pin::before{position:absolute;left:16px;top:8px;font:800 11px/1 Nunito,system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.th pre.out::before{content:'Вывод'}.th pre.pin::before{content:'Ввод'}.th pre.con::before{content:'Консоль'}
.ty{color:var(--accent);font-weight:800}
.rst{margin:8px 0 0;font-size:14px}.rst.ok{color:var(--accent)}.rst.bad{color:var(--bad)}
.cmp{white-space:pre;overflow-x:auto;margin:4px 0 8px;font-size:14px}
.elist{display:flex;flex-direction:column;gap:6px;margin:0 0 10px}
.elink{display:flex;justify-content:space-between;align-items:center;gap:10px;width:100%;text-align:left;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:10px 14px;font:inherit;font-size:15px;font-weight:700;color:var(--ink);cursor:pointer}
.elink span{color:var(--accent);font-size:14px;white-space:nowrap}
.rv{opacity:0;pointer-events:none}
#sea{position:fixed;inset:0;z-index:60;overflow:hidden}
#sea .sw{position:absolute;left:0;right:0;top:0;height:100%;transform:translateY(100%)}
#sea .wv{position:absolute;left:0;top:-39px;width:200%;height:40px;fill:rgba(56,152,236,.66)}
#sea .wf{position:absolute;left:0;right:0;top:0;bottom:-240px;background:linear-gradient(rgba(56,152,236,.66),rgba(22,92,176,.86))}
#sea .dr{position:absolute;left:50%;top:-34px;width:20px;height:28px;margin-left:-10px;opacity:0}
#sea .rg{position:absolute;left:50%;width:44px;height:14px;margin:-7px 0 0 -22px;border:3px solid rgba(255,255,255,.9);border-radius:50%;opacity:0}
#sea .sp{position:absolute;left:50%;width:9px;height:9px;margin:-4px 0 0 -4px;border-radius:50%;background:#cfe9ff;opacity:0}
"""
i = s.index('</style>')
s = s[:i] + CSS + s[i:]

# ---------- состояние, введение, подсчёты ----------
rep("function allDone(){return TOPICS.every(function(t,i){return tdone(i)})}", r"""var REV=0,BACK=null;
function allDone(){return TOPICS.every(function(t,i){return t.intro||tdone(i)})}
function NT(){return TOPICS.filter(function(t){return!t.intro}).length}
function ND(){return TOPICS.filter(function(t,i){return!t.intro&&tdone(i)}).length}
function vis(i){var t=TOPICS[i],f=TOPICS[0]&&TOPICS[0].intro;
  if(t.intro)return S.start>0?false:(REV?true:!tdone(i));
  return REV||!(f&&S.start===0&&!tdone(0))}
function goBack(){var f=BACK||home;BACK=home;f()}
function reveal(){
  var rm=matchMedia('(prefers-reduced-motion:reduce)').matches;
  REV=1;home();REV=0;
  var intro=app.querySelector('.topic.intro'),rest=[].slice.call(app.querySelectorAll('.topic.rv'));
  window.scrollTo(0,0);
  var ov=null,anims=[],tms=[],ended=false;
  function T(f,ms){tms.push(setTimeout(f,ms))}
  function A(el,kf,op){var a=el.animate(kf,op);anims.push(a);return a}
  function end(){
    if(ended)return;ended=true;tms.forEach(clearTimeout);anims.forEach(function(a){try{a.cancel()}catch(e){}});
    if(ov){ov.remove();ov=null}
    if(intro&&intro.parentNode)intro.remove();
    rest.forEach(function(e){e.classList.remove('rv')});
    window.scrollTo(0,0);var c=app.querySelector('.cur');if(c)c.scrollIntoView({block:'center'});
    links();
  }
  if(!intro||!rest.length){end();return}
  if(rm){
    A(intro,[{opacity:1},{opacity:0}],{duration:500,fill:'forwards'});
    rest.forEach(function(e,k){A(e,[{opacity:0},{opacity:1}],{duration:600,delay:500+k*150,fill:'both'})});
    T(end,1500);return}
  var vh=innerHeight,surf=Math.round(vh*.3);
  ov=document.createElement('div');ov.id='sea';
  ov.innerHTML='<div class="sw"><svg class="wv" viewBox="0 0 1200 40" preserveAspectRatio="none"><path d="M0 20 C150 0 450 40 600 20 C750 0 1050 40 1200 20 V40 H0 Z"/></svg><div class="wf"></div></div><svg class="dr" viewBox="0 0 20 28"><path d="M10 0 C10 0 0 13 0 19 a10 9 0 0 0 20 0 C20 13 10 0 10 0Z" fill="#9fd3ff" stroke="#fff" stroke-width="1.5"/></svg><i class="rg"></i><i class="rg"></i><i class="rg"></i>';
  document.body.appendChild(ov);ov.onclick=end;
  var sw=ov.querySelector('.sw'),wv=ov.querySelector('.wv'),dr=ov.querySelector('.dr'),rg=[].slice.call(ov.querySelectorAll('.rg'));
  rg.forEach(function(r){r.style.top=surf+'px'});
  snd([330,262,196]);
  A(wv,[{transform:'translateX(0)'},{transform:'translateX(-50%)'}],{duration:2400,iterations:Infinity});
  A(sw,[{transform:'translateY(100%)'},{transform:'translateY(30%)'}],{duration:1900,easing:'ease-in-out',fill:'forwards'});
  A(intro,[{transform:'none',opacity:1,filter:'blur(0)'},{transform:'translateY(170px) scale(.8) rotate(3deg)',opacity:0,filter:'blur(3px)'}],{duration:2000,easing:'ease-in',fill:'forwards'});
  T(function(){if(intro)intro.style.display='none';window.scrollTo(0,0)},2100);
  T(function(){
    A(dr,[{opacity:1,transform:'translateY(0)'},{opacity:1,transform:'translateY('+(surf+34)+'px)'}],{duration:650,easing:'cubic-bezier(.5,0,1,.6)',fill:'forwards'});
  },2200);
  T(function(){
    dr.style.display='none';snd([880,660]);
    rg.forEach(function(r,k){A(r,[{opacity:.95,transform:'scale(.2)'},{opacity:0,transform:'scale(14)'}],{duration:1700,delay:k*260,easing:'ease-out',fill:'both'})});
    A(sw,[{transform:'translateY(30%)'},{transform:'translateY(26%)'},{transform:'translateY(31.5%)'},{transform:'translateY(30%)'}],{duration:1000});
    for(var n=0;n<9;n++){var d=document.createElement('i');d.className='sp';d.style.top=surf+'px';ov.appendChild(d);
      var dx=(Math.random()-.5)*190,up=50+Math.random()*80;
      A(d,[{opacity:1,transform:'translate(0,0)'},{opacity:1,transform:'translate('+dx/2+'px,'+(-up)+'px)',offset:.45},{opacity:0,transform:'translate('+dx+'px,8px)'}],{duration:900,easing:'ease-out',fill:'both'})}
  },2850);
  T(function(){
    snd([523,659,784]);
    rest.forEach(function(e,k){A(e,[{opacity:0,transform:'translateY(90px) scale(.94)',filter:'blur(10px)'},{opacity:1,transform:'none',filter:'blur(0)'}],{duration:1000,delay:k*260,easing:'cubic-bezier(.2,.8,.2,1)',fill:'both'})});
    A(sw,[{transform:'translateY(30%)'},{transform:'translateY(105%)'}],{duration:2300,delay:1000,easing:'ease-in-out',fill:'forwards'});
  },3500);
  T(end,3500+1000+2300+400+rest.length*80);
}""")

# ---------- главная ----------
rep("function home(){\n", "function home(){BACK=home;\n")
rep("""TOPICS.forEach(function(t,i){h+='<section class="topic"><h2>'""",
    """TOPICS.forEach(function(t,i){if(!vis(i))return;h+='<section class="topic'+(t.intro?' intro':'')+(REV&&!t.intro?' rv':'')+'"><h2>'""")
rep("var c=app.querySelector('.cur');if(c)c.scrollIntoView({block:'center'});\n}\nfunction go(i,j){",
    "var c=app.querySelector('.cur');if(c&&!REV)c.scrollIntoView({block:'center'});\n}\nfunction go(i,j){")
# выбор стартовой темы
rep("TOPICS.forEach(function(t,i){h+='<button class=\"lesson\"", "TOPICS.forEach(function(t,i){if(t.intro)return;h+='<button class=\"lesson\"")
rep("(i?'Начать с темы «':'С нуля: «')", "(i>(TOPICS[0].intro?1:0)?'Начать с темы «':'С нуля: «')")
rep("S.start=+b.dataset.i;save();greet()", "S.start=(+b.dataset.i===(TOPICS[0].intro?1:0)?0:+b.dataset.i);save();greet()")

# ---------- островки: тип, значок остаётся ----------
a = s.index('function island(i,j){')
b = s.index('function home(){')
ISL = r"""function island(i,j){
  var k=i+'-'+j,it=IT(i,j),d=S.d[k],op=isOpen(i,j),c=cur()===k,wt=j>0&&S.d[i+'-'+(j-1)]&&!LIT[i+'-'+(j-1)];
  var ty={theory:['t','📖','Теория'],flash:['f','✏️','Вопросы'],test:['c','💻','Код'],project:['p','🚀','Мини-проект']}[it.t],lb=it.n||'',off=[0,46,0,-46][j%4];
  return '<div class="ilw'+(wt?' wait':'')+'" style="transform:translateX('+off+'px)">'+(c?'<div class="flag">🚩 Ты остановился здесь</div>':'')+'<button class="isl ty-'+ty[0]+' '+(d?'dn':(op?'op':'lk'))+(c?' cur':'')+'" data-i="'+i+'" data-j="'+j+'" aria-label="'+esc(ty[2]+': '+lb)+(d?' (пройдено)':(op?'':' (закрыто)'))+'">'+PEN+'<span class="ic">'+ty[1]+'</span>'+(d?'<i class="bd ok">✓</i>':(op?'':'<i class="bd">🔒</i>'))+'</button><div class="mu">'+esc(lb)+(it.t==='project'?'<br><small>'+(S.at[k]==='skip'?'пропущен':'по желанию')+'</small>':'')+'</div></div>';
}
"""
s = s[:a] + ISL + s[b:]

# ---------- теория ----------
rep("<div class=\"th\"><h2>'+esc(TOPICS[i].n)+'</h2><div id=\"tb\">", "<div class=\"th\"><p class=\"mu\" style=\"margin:0 0 2px\">'+esc(TOPICS[i].n)+'</p><h2>'+esc(it.n)+'</h2><div id=\"tb\">")
rep("$('go').onclick=function(){var w=tdone(i);if(!S.d[i+'-'+j])bump(i+'-'+j);home();",
    "$('go').onclick=function(){var w=tdone(i);if(!S.d[i+'-'+j])bump(i+'-'+j);if(TOPICS[i].intro&&!w&&tdone(i)&&S.start===0){reveal();return}home();")
# печать: скорость по объёму, таблицы
rep("BL={P:1,PRE:1,UL:1,OL:1,DIV:1,H3:1,H4:1,BLOCKQUOTE:1}", "BL={P:1,PRE:1,UL:1,OL:1,DIV:1,H3:1,H4:1,BLOCKQUOTE:1,TABLE:1}")
rep("var u=0,last=0,bud=0,done=false;", "var u=0,last=0,bud=0,done=false,TOT=0;U.forEach(function(x){TOT+=x.e?1:x.t.length*(x.f?.3:1)});var SPD=Math.max(60,Math.min(900,TOT/4));")
rep("bud+=dt/1000*45", "bud+=dt/1000*SPD")

# ---------- подсветка ----------
a = s.index('function hl(c){')
b = s.index("return o+esc(c.slice(p))}", a) + len("return o+esc(c.slice(p))}")
HL = r"""function hs(t,f){
  var o='',i=0,n=t.length,sg='';
  function esq(x){return x.split(/(\\.)/).map(function(p,q){return q%2?'<span class="es">'+esc(p)+'</span>':esc(p)}).join('')}
  function fl(){if(sg){o+='<span class="st">'+esq(sg)+'</span>';sg=''}}
  while(i<n){var ch=t[i];
    if(f&&ch==='{'){
      if(t[i+1]==='{'){sg+='{{';i+=2;continue}
      var j=i+1,d=1;while(j<n&&d>0){if(t[j]==='{')d++;else if(t[j]==='}')d--;j++}
      fl();o+='<span class="fs">{</span><span class="fe">'+esc(t.slice(i+1,d===0?j-1:j))+'</span>'+(d===0?'<span class="fs">}</span>':'');i=j;continue}
    if(f&&ch==='}'&&t[i+1]==='}'){sg+='}}';i+=2;continue}
    sg+=ch;i++}
  fl();return o}
function hl(c){var re=/(#[^\n]*)|("(?:[^"\\\n]|\\.)*"?|'(?:[^'\\\n]|\\.)*'?)|(\b\d+(?:\.\d+)?\b)|(\b(?:[fF][rR]?|[rR][fF])(?=["']))|([A-Za-z_]\w*)|([()\[\]{}])/g,o='',p=0,m,stk=[],PR={')':'(',']':'[','}':'{'},fe=-1;
  while(m=re.exec(c)){o+=esc(c.slice(p,m.index));var t=m[0],k;
    if(m[2]){o+=hs(t,fe===m.index);fe=-1;p=re.lastIndex;continue}
    if(m[4]){fe=re.lastIndex}
    if(m[6]){if(PR[t]){if(stk.length&&stk[stk.length-1].c===PR[t])k='b'+(stk.pop().d%4);else k='bx'}else{k='b'+(stk.length%4);stk.push({c:t,d:stk.length})}}
    else if(m[1])k='cm';else if(m[3])k='nm';else if(m[4])k='fs';
    else if(c.charAt(m.index-1)==='.')k=MS[t]?'ms':ML[t]?'ml':MD[t]?'md':MT[t]?'mt':MF[t]?'mf':'';
    else if((t==='match'||t==='case')&&/^[ \t]*$/.test(c.slice(c.lastIndexOf('\n',m.index-1)+1,m.index))&&/^[^\n]*:[ \t]*(#[^\n]*)?(\n|$)/.test(c.slice(re.lastIndex)))k='kw';
    else if((t==='sep'||t==='end')&&stk.length&&/[,(]$/.test(c.slice(0,m.index).replace(/\s+$/,''))&&/^[ \t]*=(?!=)/.test(c.slice(re.lastIndex)))k='ka';
    else k=KW[t]?'kw':BI[t]?'bi':'';
    o+=k?'<span class="'+k+'">'+esc(t)+'</span>':esc(t);p=re.lastIndex}
  return o+esc(c.slice(p))}"""
s = s[:a] + HL + s[b:]

# ---------- редактор: кавычки после f/r/b/u ----------
rep("function initEd(c,cb){", "function qo(v,p){var b=v.slice(0,p),m=b.match(/[A-Za-z]*$/)[0];if(!m)return!/\\w/.test(b.slice(-1)||'');if(/\\w/.test(b.charAt(b.length-m.length-1)||''))return false;return/^(?:[fFrRbBuU]|[fF][rR]|[rR][fF]|[bB][rR]|[rR][bB])$/.test(m)}\nfunction initEd(c,cb){")
rep("if(pr[d]&&!((d==='\"'||d===AP)&&/\\w/.test(v[p-1]||''))){", "if(pr[d]&&!((d==='\"'||d===AP)&&!qo(v,p))){")
rep("&&!((ch==='\"'||ch===AP)&&/\\w/.test(c.value[p-2]||'')))c.setRangeText(pr[ch],p,p,'start');", "&&!((ch==='\"'||ch===AP)&&!qo(c.value,p-1)))c.setRangeText(pr[ch],p,p,'start');")

# ---------- запуск кода и ввод ----------
a = s.index('function liveRun(code){')
b = s.index("var NAV=document.createElement('nav')")
LR = r"""function liveRun(code){
  var o=$('o'),ir=$('ir'),ii=$('ii'),rs=$('rst');o.style.display='block';o.textContent='';ir.classList.remove('on');
  function st(t,c){if(rs){rs.hidden=!t;rs.textContent=t||'';rs.className='mu rst'+(c?' '+c:'')}}
  var le=lint(code);if(le){o.textContent='SyntaxError: '+le;st('✗ Программа не запущена: исправь ошибку в коде','bad');return}
  st('⏳ Программа выполняется…');
  exec(code,{live:function(t){o.textContent=t},ask:function(){return new Promise(function(r){
    ir.classList.add('on');ii.value='';st('⌨️ Программа ждёт ввод: напиши ответ в поле ниже и нажми «Ввод»');ii.focus();
    try{ir.scrollIntoView({block:'nearest'})}catch(e){}
    ir.onsubmit=function(e){e.preventDefault();if(!ir.classList.contains('on'))return;ir.classList.remove('on');st('⏳ Программа выполняется…');r(ii.value)};
  })}}).then(function(r){ir.classList.remove('on');o.textContent=(r.raw+(r.err?'\n'+fixErr(r.err,code):'')).trim()||'(программа ничего не вывела)';st(r.err?'✗ Программа завершилась с ошибкой':'✓ Программа завершена',r.err?'bad':'ok');try{o.scrollIntoView({block:'nearest'})}catch(e){}})
}
"""
s = s[:a] + LR + s[b:]
rep("""enterkeyhint="send"><button class="btn" id="ib" type="submit">Ввод</button></form>';""",
    """enterkeyhint="send"><button class="btn" id="ib" type="submit">Ввод</button></form><p class="mu rst" id="rst" hidden></p>';""")

# ---------- строгая проверка ----------
rep("function norm(s){return s.replace(/\\r/g,'').split('\\n').map(function(l){return l.trim().replace(/\\s+/g,' ')}).join('\\n').trim()}",
    "function norm(s,st){s=s.replace(/\\r/g,'').split('\\n');return st?s.map(function(l){return l.replace(/\\s+$/,'')}).join('\\n').replace(/^\\n+|\\n+$/g,''):s.map(function(l){return l.trim().replace(/\\s+/g,' ')}).join('\\n').trim()}")
rep("if(r.err||norm(r.out)!==norm(q.tests[n][1])){", "if(r.err||norm(r.out,q.strict)!==norm(q.tests[n][1],q.strict)){")
OLDF = "return{ok:false,h:'<div class=\"fb bad\"><b>Не прошёл тест '+(n+1)+' из '+q.tests.length+'</b>Вход: '+esc(q.tests[n][0]).replace(/\\n/g,' ↵ ')+'<br>Ожидалось: '+esc(q.tests[n][1]).replace(/\\n/g,' ↵ ')+'<br>Получилось: '+esc((fixErr(r.err,code)||norm(r.out))||'(пусто)').replace(/\\n/g,' ↵ ')+hint+'</div>'}"
NEWF = "var got=(fixErr(r.err,code)||norm(r.out,q.strict))||'(пусто)';return{ok:false,h:'<div class=\"fb bad\"><b>Не прошёл тест '+(n+1)+' из '+q.tests.length+'</b>Вход: '+esc(q.tests[n][0]||'(нет)').replace(/\\n/g,' ↵ ')+(q.strict?'<br>Здесь важны и пробелы: ширина и выравнивание проверяются точно.<br>Ожидалось:<pre class=\"cmp\">'+esc(q.tests[n][1])+'</pre>Получилось:<pre class=\"cmp\">'+esc(got)+'</pre>'+hint:'<br>Ожидалось: '+esc(q.tests[n][1]).replace(/\\n/g,' ↵ ')+'<br>Получилось: '+esc(got).replace(/\\n/g,' ↵ ')+hint)+'</div>'}"
rep(OLDF, NEWF)
rep("<p class=\"mu\" style=\"margin:0 0 12px\">'+esc(q.ex||'').replace(/\\n/g,'<br>')+'</p>",
    "'+(q.strict?'<pre class=\"cmp\">'+esc(q.ex||'')+'</pre>':'<p class=\"mu\" style=\"margin:0 0 12px\">'+esc(q.ex||'').replace(/\\n/g,'<br>')+'</p>')+'")
rep("(it.ex?'<b>Пример</b><p style=\"margin-bottom:0\">'+esc(it.ex).replace(/\\n/g,'<br>')+'</p>':'')",
    "(it.ex?'<b>Пример</b>'+(it.strict?'<pre class=\"cmp\">'+esc(it.ex)+'</pre>':'<p style=\"margin-bottom:0\">'+esc(it.ex).replace(/\\n/g,'<br>')+'</p>'):'')")

# ---------- «назад» после отработки из профиля ----------
rep("$('go').onclick=home;if(nx)$('rp').onclick=function(){quiz(i,j)};", "$('go').onclick=goBack;if(nx)$('rp').onclick=function(){quiz(i,j)};")
rep("    $('x').onclick=home;\n    var g=$('go'),os=", "    $('x').onclick=goBack;\n    var g=$('go'),os=")
rep("  $('x').onclick=home;\n  var c=$('code'),sync=initEd(c,function(){drc(i,j,k)", "  $('x').onclick=goBack;\n  var c=$('code'),sync=initEd(c,function(){drc(i,j,k)")
rep("HINT=0;$('go').onclick=home;", "HINT=0;$('go').onclick=goBack;")

# ---------- профиль ----------
rep("var n=TOPICS.filter(function(t,i){return tdone(i)}).length,pct=Math.round(n/TOPICS.length*100);", "var n=ND(),pct=Math.round(n/NT()*100);")
rep("var rows=TOPICS.map(function(t,i){var c=0;(t.items||[]).forEach(function(x,j){c+=S.es[i+'-'+j]||0});return{n:t.n,c:c}})",
    "var rows=TOPICS.map(function(t,i){var c=0,l=[];(t.items||[]).forEach(function(x,j){var e=S.es[i+'-'+j]||0;c+=e;if(e>0)l.push({j:j,n:x.n,e:e,ic:x.t==='flash'?'✏️':x.t==='test'?'💻':'🚀'})});return{i:i,n:t.n,c:c,l:l}})")
rep("<b>Пройдено тем: '+n+' из '+TOPICS.length+' · '+pct+'%</b>", "<b>Пройдено тем: '+n+' из '+NT()+' · '+pct+'%</b>")
rep("""'<div class="erow"><span>'+esc(r.n)+'</span><div class="bar"><i style="width:'+Math.round(r.c/mx*100)+'%;background:var(--bad)"></i></div><b>'+r.c+'</b></div>'}).join('')""",
    """'<div class="erow"><span>'+esc(r.n)+'</span><div class="bar"><i style="width:'+Math.round(r.c/mx*100)+'%;background:var(--bad)"></i></div><b>'+r.c+'</b></div><div class="elist">'+r.l.map(function(x){return'<button class="elink" data-i="'+r.i+'" data-j="'+x.j+'"><span style="color:var(--ink);font-size:15px">'+x.ic+' '+esc(x.n)+' · ошибок: '+x.e+'</span><span>Отработать →</span></button>'}).join('')+'</div>'}).join('')+'<p class="mu" style="margin:6px 0 0;font-size:14px">Нажми на островок, чтобы отработать ошибки. Пройдёшь без ошибок, и он пропадёт из списка.</p>'""")
rep("""<button class="btn g" id="dc">📖 Изученные функции</button>""", """<button class="btn g" id="dc">📖 Изученные функции</button>'+(TOPICS[0]&&TOPICS[0].intro?'<button class="btn g" id="intr">🏝 Знакомство с ИТП</button>':'')+'""")
rep("$('dc').onclick=dict;$('sh').onclick=share;", "$('dc').onclick=dict;$('sh').onclick=share;if($('intr'))$('intr').onclick=function(){theory(0,0)};app.querySelectorAll('.elink').forEach(function(b){b.onclick=function(){BACK=profile;go(+b.dataset.i,+b.dataset.j)}});")

# ---------- шаринг ----------
rep("function shareTxt(){var n=TOPICS.filter(function(t,i){return tdone(i)}).length;", "function shareTxt(){var n=ND();")
rep("var n=TOPICS.filter(function(t,i){return tdone(i)}).length,st=[", "var n=ND(),st=[")
rep("n+' из '+TOPICS.length,'тем пройдено'", "n+' из '+NT(),'тем пройдено'")

# ---------- клавиатура и горячие клавиши ----------
rep("var DESK=matchMedia('(hover:hover) and (pointer:fine)').matches;",
    r"""var KBD=matchMedia('(hover:hover) and (pointer:fine)').matches&&!(navigator.maxTouchPoints>0);
if(KBD)document.documentElement.classList.add('kbd');
function setKbd(){KBD=true;document.documentElement.classList.add('kbd')}
function physKey(e){return e.isTrusted&&e.key&&e.key!=='Unidentified'&&e.keyCode!==229&&!e.isComposing&&(/^(Tab|Escape|F\d+|Arrow\w+|Home|End|PageUp|PageDown|Control|Alt|Meta|Insert|Delete)$/.test(e.key)||e.ctrlKey||e.metaKey||e.altKey)}""")
rep("function keys(){\n  modal(", "function keys(){\n  var ex=document.querySelector('.modal');if(ex){if(ex.classList.contains('kbm'))ex.remove();return}\n  var km=modal(")
rep("Сочетания работают на любой раскладке.</p>',[['Закрыть']]);\n}", "Сочетания работают на любой раскладке.</p>',[['Закрыть']]);km.classList.add('kbm');\n}")
rep("var m=document.querySelector('.modal');if(m){e.preventDefault();m.remove();return}\n    if(!DESK)return;",
    "var ms=document.querySelectorAll('.modal'),m=ms[ms.length-1];if(m){e.preventDefault();m.remove();return}\n    if(!KBD){if(physKey(e))setKbd();else return}")
rep("  if(!DESK)return;\n  var ctl=", "  if(!KBD){if(physKey(e))setKbd();else return}\n  var ctl=")
rep("if(ctl&&!e.altKey&&c==='Enter'){var r=$('run');", "if(ctl&&!e.altKey&&c==='Enter'){if(e.target&&e.target.id==='ii'){e.preventDefault();var fm=$('ir');if(fm&&fm.requestSubmit)fm.requestSubmit();return}var r=$('run');")


# ---------- у каждой функции свой цвет ----------
rep(".ka{color:var(--ka);font-weight:700}", """:root{--fsat:72%;--flit:34%}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--fsat:68%;--flit:68%}}
:root[data-theme="dark"]{--fsat:68%;--flit:68%}
.th .term.fn{background:none;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.95em}
.ka{color:var(--ka);font-weight:700}""")
rep("function hs(t,f){", r"""var FH={input:185,int:335,float:160,str:50,round:300,len:255,max:355,min:200,ord:85,chr:70,bin:15,oct:110,hex:270,abs:235,sum:140,range:30,type:325,bool:175,pow:215,divmod:45,format:95,sorted:350,list:205,dict:120,set:20,join:280,lower:190,upper:340,strip:150,split:60,replace:310,find:10,count:240,startswith:100,endswith:130,capitalize:75,title:225};
function fcol(n){if(n==='print')return 'var(--bi)';var h=FH[n];if(h===undefined){if(!(BI[n]||MS[n]||ML[n]||MD[n]||MT[n]||MF[n]))return '';h=0;for(var i=0;i<n.length;i++)h=(h*31+n.charCodeAt(i))%360}return 'hsl('+h+' var(--fsat) var(--flit))'}
function hs(t,f){""")
rep("o+=k?'<span class=\"'+k+'\">'+esc(t)+'</span>':esc(t);p=re.lastIndex}\n  return o+esc(c.slice(p))}",
    "var fc=(k==='bi'||k==='ms'||k==='ml'||k==='md'||k==='mt'||k==='mf')?fcol(t):'';o+=k?'<span class=\"'+k+'\"'+(fc?' style=\"color:'+fc+'\"':'')+'>'+esc(t)+'</span>':esc(t);p=re.lastIndex}\n  return o+esc(c.slice(p))}")
rep("return T[n]?'<button class=\"term\" data-n=\"'+esc(n)+'\">'",
    "return T[n]?'<button class=\"term'+(fcol(n)?' fn':'')+'\"'+(fcol(n)?' style=\"color:'+fcol(n)+'\"':'')+' data-n=\"'+esc(n)+'\">'")


# ---------- приглашение input("...") не должно попадать в проверяемый вывод ----------
# Skulpt сам печатает приглашение через output() и сразу вызывает inputfun с пустой строкой,
# поэтому запоминаем последний выведенный кусок и вырезаем его при вызове input.
rep("var out='',n=0,marks=[],my=++TK,cut=false,ov=false;", "var out='',n=0,marks=[],my=++TK,cut=false,ov=false,LS=0,LL=0;")
rep("output:function(x){if(my!==TK||cut)return;", "output:function(x){if(my!==TK||cut)return;LS=out.length;LL=x.length;")
rep("if(p&&out.slice(-p.length)===p)marks.push([out.length-p.length,p.length]);", "if(LL)marks.push([LS,LL]);LL=0;")

# ---------- проверка данных ----------
rep("!(x.a>=0&&x.a<x.o.length)", "!(typeof x.a==='number'&&x.a>=0&&x.a<x.o.length)")
rep("if(!t.n)e.push(p+'нет поля n');", "if(!t.n)e.push(p+'нет поля n');if(!t.s)e.push(p+'нет поля s (подзаголовок)');")

exec(open('p414.py',encoding='utf-8').read())
exec(open('p415.py',encoding='utf-8').read())
exec(open('p420.py',encoding='utf-8').read())
exec(open('p430.py',encoding='utf-8').read())

# ---------- темы ----------
m = re.search(r'var TOPICS=\[.*?\n\];\n', s, re.S)
assert m
import content
import json
_T = content.build()
# данные тем для tests/coverage_check.py (что где введено и где используется)
json.dump(dict(topics=_T, filesets=dsl.FILESETS), open('topics.json', 'w', encoding='utf-8'), ensure_ascii=False)
tj = dsl.topics_js(_T)
s = s[:m.start()] + tj + '\n' + s[m.end():]
rep("/* Островки темы (items), порядок и количество любые:",
    "/* Тема с intro:1 показывается только при «С нуля», стоит первой. Поле s у темы обязательно. strict:1 у задания или проекта: сравнение вывода с учётом пробелов в начале и середине строк. */\n/* Островки темы (items), порядок и количество любые:")
open('out.html', 'w', encoding='utf-8').write(s)
import json
json.dump(dict(EX=dsl.EX, FL=dsl.FL, TK=dsl.TK, ER=dsl.ER), open('checks.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('ok', len(s), 'ex', len(dsl.EX), 'fl', len(dsl.FL), 'tk', len(dsl.TK))
