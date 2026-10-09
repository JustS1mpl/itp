# -*- coding: utf-8 -*-
# Патчи v4.1.4. Выполняется внутри build.py (доступны s, rep, re).
import re as _re

# ---------- CSS ----------
CSS414 = r"""
/* ===== v4.1.4 ===== */
.topic.intro{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;min-height:calc(100vh - 330px);min-height:calc(100dvh - 330px)}
.seg.lit{stroke:var(--ti,var(--accent))}
.isl.nx path{fill:var(--ti);stroke:var(--ti)}
.isl.nx path.gl{opacity:1}
.elink{box-sizing:border-box;max-width:100%;overflow:hidden}
.elink .et{flex:1;min-width:0;color:var(--ink);font-size:15px;white-space:normal;overflow-wrap:anywhere;line-height:1.3}
.elink .et small{display:block;color:var(--muted);font-weight:600;font-size:13px;margin-top:2px}
.elink .eg{flex:none;background:var(--soft);border-radius:999px;padding:6px 12px;font-size:13px}
.erow span{min-width:0;overflow-wrap:anywhere}
.cal{display:flex;gap:6px;align-items:flex-start}
.cwd{display:grid;grid-template-rows:repeat(7,30px);gap:4px;margin-top:22px;font-size:11px;line-height:30px;color:var(--muted)}
.csc{flex:1;min-width:0;overflow-x:auto;padding-bottom:8px;scrollbar-width:thin;-webkit-overflow-scrolling:touch}
.cmo{display:grid;grid-template-columns:repeat(var(--n,3),var(--cw,100px));gap:4px;height:18px;margin-bottom:4px;font-size:11px;line-height:18px;color:var(--muted);white-space:nowrap;width:max-content}
.cg{display:grid;grid-auto-flow:column;grid-template-rows:repeat(7,30px);grid-auto-columns:var(--cw,100px);gap:4px;width:max-content}
.cg i{border-radius:9px;position:relative;display:flex;align-items:center;justify-content:center;font-style:normal;font-size:12px;font-weight:700;color:var(--muted)}
.cg i.l3,.cg i.l4{color:#fff}
.cg i.pre{background:none;border:1.5px dashed var(--line);color:transparent}
.cg i.rg::after{content:'🚩';position:absolute;right:6px;top:50%;transform:translateY(-50%);font-size:12px}
.cnote{font-size:13px;color:var(--muted);margin:2px 0 0}
.bk textarea{min-height:90px;margin:8px 0 0}
"""
_i = s.index('</style>')
s = s[:_i] + CSS414 + s[_i:]

# ---------- введение: по центру, капля в центр ----------
rep("var vh=innerHeight,surf=Math.round(vh*.3);",
    "var vh=innerHeight,ib=intro.querySelector('.isl'),ir=ib?ib.getBoundingClientRect():null,surf=ir?Math.round(ir.top+ir.height/2):Math.round(vh*.5),P=Math.round(surf/vh*1000)/10;")
rep("{transform:'translateY(30%)'}],{duration:1900", "{transform:'translateY('+P+'%)'}],{duration:1900")
rep("[{transform:'translateY(30%)'},{transform:'translateY(26%)'},{transform:'translateY(31.5%)'},{transform:'translateY(30%)'}]",
    "[{transform:'translateY('+P+'%)'},{transform:'translateY('+(P-4)+'%)'},{transform:'translateY('+(P+1.5)+'%)'},{transform:'translateY('+P+'%)'}]")
rep("A(sw,[{transform:'translateY(30%)'},{transform:'translateY(105%)'}]", "A(sw,[{transform:'translateY('+P+'%)'},{transform:'translateY(105%)'}]")

# ---------- кнопка «Знакомство с ИТП» только до прочтения ----------
rep("(TOPICS[0]&&TOPICS[0].intro?'<button class=\"btn g\" id=\"intr\">", "(TOPICS[0]&&TOPICS[0].intro&&!S.d['0-0']?'<button class=\"btn g\" id=\"intr\">")
rep("if($('intr'))$('intr').onclick=function(){theory(0,0)};", "if($('intr'))$('intr').onclick=function(){BACK=profile;theory(0,0)};")
rep("$('x').onclick=home;\n  app.querySelectorAll('.term')", "$('x').onclick=goBack;\n  app.querySelectorAll('.term')")
rep("reveal();return}home();if(!w&&tdone(i))", "reveal();return}if(TOPICS[i].intro&&S.start>0){goBack();toast('Готово. Эта кнопка больше не нужна и пропала из профиля');return}home();if(!w&&tdone(i))")

# ---------- пропущенные темы считаются пройденными, словарь ----------
rep("function ND(){return TOPICS.filter(function(t,i){return!t.intro&&tdone(i)}).length}",
    "function ND(){return TOPICS.filter(function(t,i){return!t.intro&&(tdone(i)||i<S.start)}).length}")
rep("if(it.t==='theory'&&S.d[i+'-'+j])(it.terms||[])", "if(it.t==='theory'&&(S.d[i+'-'+j]||(i<S.start&&!t.intro)))(it.terms||[])")

# ---------- серия верных ответов с 5 ----------
rep("if(right&&cb>=3){", "if(right&&cb>=5){")

# ---------- пустой ввод в тесте ----------
rep("var r=await exec(code,{lines:q.tests[n][0].split('\\n')});", "var r=await exec(code,{lines:q.tests[n][0]===''?[]:q.tests[n][0].split('\\n')});")

# ---------- отработка ошибок: вёрстка ----------
rep("""<span style="color:var(--ink);font-size:15px">'+x.ic+' '+esc(x.n)+' · ошибок: '+x.e+'</span><span>Отработать →</span>""",
    """<span class="et">'+x.ic+' '+esc(x.n)+'<small>ошибок: '+x.e+'</small></span><span class="eg">Отработать →</span>""")

# ---------- линии цвета острова, к которому ведут ----------
rep("lp.setAttribute('class','seg lit');", "var tc=(it[j+1].querySelector('.isl').className.match(/ty-\\w/)||[''])[0];lp.setAttribute('class','seg lit '+tc);")

rep("if(S.d[key]){var lp=","if(S.d[key]&&isOpen(i,j+1)){var lp=")

# ---------- подсветка следующего острова в пропущенной теме ----------
rep("c=cur()===k,wt=", "c=cur()===k,nx=!c&&!d&&nxI(i,j),wt=")
rep("+(c?' cur':'')+'\" data-i=\"'", "+(c?' cur':'')+(nx?' nx':'')+'\" data-i=\"'")
rep("function island(i,j){", "function nxI(i,j){if(!(i<S.start)||TOPICS[i].intro)return false;var f=-1;for(var x=0;x<ni(i);x++)if(!S.d[i+'-'+x]&&isOpen(i,x)){f=x;break}return f===j}\nfunction island(i,j){")

# ---------- календарь ----------
_a = s.index('function lvC(h)')
_b = s.index('function profile()')
CAL = r"""function lvC(h){if(!h)return 0;var l=h.les|0;if(!l)return h.xp>0?1:0;return l>=6?4:l>=4?3:l>=2?2:1}
function regDay(){if(S.reg)return S.reg;var m='';for(var k in S.hist)if(!m||k<m)m=k;return m||day(new Date())}
function calText(k){
  var p=k.split('-'),h=S.hist[k],cy=String(new Date().getFullYear()),t=(+p[2])+' '+MON[+p[1]-1]+(p[0]!==cy?' '+p[0]:''),rg=regDay();
  if(k<rg)return t+': ты ещё не занимался в ИТП';
  var a=h&&(h.xp||h.les)?h.xp+' ⭐, пройдено '+h.les+' '+pl(h.les,['островок','островка','островков']):'без занятий';
  return k===rg?t+': здесь ты начал заниматься в ИТП 🚩'+(a==='без занятий'?'':' ('+a+')'):t+': '+a;
}
function calHtml(){
  var t=new Date();t.setHours(12,0,0,0);var tk=day(t),rg=regDay();
  var m0=new Date(t);m0.setDate(t.getDate()-((t.getDay()+6)%7));
  var rp=rg.split('-'),rd=new Date(+rp[0],+rp[1]-1,+rp[2],12),rm=new Date(rd);rm.setDate(rd.getDate()-((rd.getDay()+6)%7));
  var wk=Math.max(3,Math.min(53,Math.round((m0-rm)/604800000)+1)),st=new Date(m0);st.setDate(m0.getDate()-(wk-1)*7);
  var g='',lb='',act=0;
  for(var w=0;w<wk;w++){
    var ws=new Date(st);ws.setDate(st.getDate()+w*7);lb+='<span>'+ws.getDate()+' '+MS3[ws.getMonth()]+'</span>';
    for(var d=0;d<7;d++){
      var c=new Date(ws);c.setDate(ws.getDate()+d);
      if(c>t){g+='<i class="fu"></i>';continue}
      var k=day(c);
      if(k<rg){g+='<i class="pre" data-d="'+k+'"></i>';continue}
      var l=lvC(S.hist[k]);if(l)act++;
      g+='<i class="l'+l+(k===tk?' td':'')+(k===rg?' rg':'')+'" data-d="'+k+'">'+c.getDate()+'</i>';
    }
  }
  return'<div class="cal" role="img" aria-label="Календарь активности. Дней с занятиями: '+act+'"><div class="cwd" aria-hidden="true"><span>Пн</span><span>Вт</span><span>Ср</span><span>Чт</span><span>Пт</span><span>Сб</span><span>Вс</span></div><div class="csc" style="--n:'+wk+'"><div class="cmo" aria-hidden="true">'+lb+'</div><div class="cg" id="cg">'+g+'</div></div></div><div class="cinfo" id="ci">'+calText(tk)+'</div><div class="cft"><span>Дней с занятиями: '+act+'</span><span class="cleg" aria-hidden="true">меньше<i class="l0"></i><i class="l1"></i><i class="l2"></i><i class="l3"></i><i class="l4"></i>больше</span></div><p class="cnote">Оттенок зависит от числа пройденных островков за день: 1, 2–3, 4–5, 6 и больше.'+(wk>3?' Листай влево, чтобы увидеть прошлые недели.':'')+'</p>';
}
function calBind(){
  var cg=$('cg'),sc=app.querySelector('.csc');if(!cg||!sc)return;
  var w=sc.clientWidth;if(w<60)w=300;sc.style.setProperty('--cw',Math.floor((w-8)/3)+'px');sc.scrollLeft=sc.scrollWidth;
  function sh(e){var d=e.target.closest&&e.target.closest('[data-d]');if(d)$('ci').textContent=calText(d.dataset.d)}
  cg.addEventListener('mouseover',sh);cg.addEventListener('click',sh);
}
"""
s = s[:_a] + CAL + s[_b:]
rep("hist:hs,sv:sv,cur:cu}}", "hist:hs,sv:sv,cur:cu,reg:dt(r.reg)}}")
rep("g.onclick=function(){S.nick=i.value.trim();save();place()};", "g.onclick=function(){S.nick=i.value.trim();if(!S.reg)S.reg=day(new Date());save();place()};")

# ---------- хранилище ----------
rep("try{S=clean(JSON.parse(localStorage.getItem('pyshag2')||'{}'))}catch(e){S=clean({})}\nfunction save(){try{localStorage.setItem('pyshag2',JSON.stringify(S))}catch(e){}}",
r"""/* Хранилище. Всё обращение к данным идёт через Store: при переносе в apk меняется только этот блок.
   Основное место: localStorage. Копия: IndexedDB (если localStorage очистили, прогресс вернётся). */
var Store=(function(){
  var KEY='pyshag2',mem=null,ok=true,db=null;
  try{localStorage.setItem('__t','1');localStorage.removeItem('__t')}catch(e){ok=false}
  function open(cb){if(db)return cb(db);try{var r=indexedDB.open('itp-store',1);r.onupgradeneeded=function(){r.result.createObjectStore('kv')};r.onsuccess=function(){db=r.result;cb(db)};r.onerror=function(){cb(null)}}catch(e){cb(null)}}
  function idbPut(v){open(function(d){if(!d)return;try{d.transaction('kv','readwrite').objectStore('kv').put(v,KEY)}catch(e){}})}
  function idbGet(cb){open(function(d){if(!d)return cb(null);try{var r=d.transaction('kv').objectStore('kv').get(KEY);r.onsuccess=function(){cb(r.result||null)};r.onerror=function(){cb(null)}}catch(e){cb(null)}})}
  try{navigator.storage&&navigator.storage.persist&&navigator.storage.persist()}catch(e){}
  return{ok:function(){return ok},
    get:function(){try{return ok?localStorage.getItem(KEY):mem}catch(e){return mem}},
    set:function(v){mem=v;if(ok){try{localStorage.setItem(KEY,v)}catch(e){ok=false}}idbPut(v)},
    idbGet:idbGet}
})();
try{S=clean(JSON.parse(Store.get()||'{}'))}catch(e){S=clean({})}
function save(){try{Store.set(JSON.stringify(S))}catch(e){}}""")

HELP = r"""
/* ===== платформа: вибрация, файлы, кнопка «назад», резервная копия ===== */
function vib(p){var C=window.Capacitor,H=C&&C.Plugins&&C.Plugins.Haptics;try{if(H&&H.vibrate)H.vibrate({duration:Array.isArray(p)?p.reduce(function(a,b){return a+b},0):p});else if(navigator.vibrate)navigator.vibrate(p)}catch(e){}}
function saveFile(name,blob){
  var C=window.Capacitor,P=C&&C.Plugins;
  if(P&&P.Filesystem&&P.Share&&C.isNativePlatform&&C.isNativePlatform()){
    var fr=new FileReader();fr.onload=function(){var b64=String(fr.result).split(',')[1];
      P.Filesystem.writeFile({path:name,data:b64,directory:'CACHE'}).then(function(r){return P.Share.share({title:name,url:r.uri})}).catch(function(){toast('Не получилось сохранить файл')})};
    fr.readAsDataURL(blob);return true}
  try{var u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(u)},2000);return true}
  catch(e){toast('Не получилось сохранить файл');return false}
}
function itpBack(){
  var ms=document.querySelectorAll('.modal');if(ms.length){ms[ms.length-1].remove();return true}
  var x=document.getElementById('x');if(x){x.click();return true}
  if(CURTAB&&CURTAB!=='home'){home();return true}return false}
(function(){var C=window.Capacitor,A=C&&C.Plugins&&C.Plugins.App;
  if(A&&A.addListener)A.addListener('backButton',function(){if(!itpBack()&&A.exitApp)A.exitApp()});
  document.addEventListener('backbutton',function(e){e.preventDefault();itpBack()})})();
function exportData(){return JSON.stringify({app:'ITP',v:'4.1.4',t:new Date().toISOString(),data:S})}
function importData(txt){
  var o;try{o=JSON.parse(txt)}catch(e){return'Это не похоже на сохранение ИТП'}
  var d=o&&o.data&&typeof o.data==='object'?o.data:o;
  if(!d||typeof d!=='object')return'В файле нет данных ИТП';
  var r=clean(d);if(!r.nick)return'В сохранении нет ника, это не файл ИТП';
  S=r;seedLit();save();return''}
function backup(){
  var fl=location.protocol==='file:';
  var o=modal('<div class="bk"><h2 style="font-size:20px">Резервная копия</h2><p>Прогресс хранится на этом устройстве. Если очистить данные браузера, переустановить приложение или открыть ИТП на другом телефоне, он пропадёт. Сохрани копию и при необходимости загрузи её обратно.</p>'+(fl?'<p class="mu">Сейчас ИТП открыт как файл. На некоторых устройствах прогресс привязан к расположению этого файла: если его переместить, переименовать или открыть из другого места, прогресс может не найтись. Копия защитит от этого.</p>':'')+(Store.ok()?'':'<p class="mu" style="color:var(--bad)">Браузер не разрешает сохранять данные. Прогресс исчезнет при закрытии страницы, поэтому обязательно сделай копию.</p>')+'<p class="mu">Загрузка заменит текущий прогресс на сохранённый.</p><textarea id="bkt" style="display:none" placeholder="Вставь сюда код сохранения" aria-label="Код сохранения"></textarea></div>',[
    ['Сохранить в файл',function(){saveFile('itp-backup-'+day(new Date())+'.json',new Blob([exportData()],{type:'application/json'}));toast('Копия сохранена');return false}],
    ['Загрузить из файла',function(){var f=document.createElement('input');f.type='file';f.accept='.json,application/json,text/plain';f.onchange=function(){var fi=f.files&&f.files[0];if(!fi)return;var r=new FileReader();r.onload=function(){var e=importData(String(r.result));if(e){toast(e);return}o.remove();toast('Прогресс загружен');home()};r.readAsText(fi)};f.click();return false},1],
    ['Скопировать код',function(){copyTxt(exportData());return false},1],
    ['Вставить код',function(){var t=o.querySelector('#bkt');if(t.style.display==='none'){t.style.display='block';t.focus();return false}var e=importData(t.value.trim());if(e){toast(e);return false}toast('Прогресс загружен');home()},1],
    ['Закрыть',null,1]]);
}
"""
rep("function copyTxt(t){", HELP + "function copyTxt(t){")
rep("try{navigator.vibrate&&navigator.vibrate([60,40,60])}catch(e){}", "vib([60,40,60])")
rep("try{navigator.vibrate&&navigator.vibrate(big>1?[40,40,40,40,80]:[40,40,40])}catch(e){}", "vib(big>1?[40,40,40,40,80]:[40,40,40])")
rep("var u=URL.createObjectURL(BLOB),a=document.createElement('a');a.href=u;a.download='itp-progress.png';document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(u)},2000);toast('Картинка сохранена');return false",
    "saveFile('itp-progress.png',BLOB);toast('Картинка сохранена');return false")
rep("$('dc').onclick=dict;$('sh').onclick=share;", "$('dc').onclick=dict;$('sh').onclick=share;$('bk').onclick=backup;")
rep('<div class="row"><button class="btn g" id="sh">', '<button class="btn g" id="bk">💾 Резервная копия</button><div class="row"><button class="btn g" id="sh">')

# ---------- запуск: восстановление из резервного хранилища ----------
rep("if(!S.nick)nick();else if(S.start<0)place();else greet();",
r"""(function(){
  function go(){if(S.nick&&!S.reg){S.reg=regDay();save()}if(!S.nick)nick();else if(S.start<0)place();else greet()}
  if(S.nick){go();return}
  var fin=0;
  Store.idbGet(function(v){if(fin)return;fin=1;if(v){try{var r=clean(JSON.parse(v));if(r.nick){S=r;seedLit();Store.set(v);setTimeout(function(){toast('Прогресс восстановлен из резервного хранилища')},400)}}catch(e){}}go()});
  setTimeout(function(){if(!fin){fin=1;go()}},1500);
})();""")

# ---------- Skulpt внутри файла: работает без интернета ----------
_a = s.index("function skReady(){")
_b = s.index("\n", _a)
s = s[:_a] + r"""function skReady(){if(SKOK)return Promise.resolve(true);if(!SKP)SKP=new Promise(function(res){try{['sk-lib','sk-std'].forEach(function(id){var e=document.createElement('script');e.text=document.getElementById(id).textContent;document.head.appendChild(e)});SKOK=true;res(true)}catch(err){SKP=null;res(false)}});return SKP}""" + s[_b:]
_lib = open('sk/skulpt.min.js', encoding='utf-8').read()
_std = open('sk/skulpt-stdlib.js', encoding='utf-8').read()
assert '</script' not in _lib.lower() and '</script' not in _std.lower()
s = s.replace('</body>', '<script type="text/plain" id="sk-lib">' + _lib + '</script>\n<script type="text/plain" id="sk-std">' + _std + '</script>\n</body>', 1)
