# -*- coding: utf-8 -*-
# Патчи v4.1.5. Выполняется после p414.py внутри build.py (доступны s, rep, re).

# ---------- CSS: убираем старый календарь, ставим минималистичный ----------
_n0 = len(s)
s, _c = re.subn(r"\.cal\{display:flex;gap:6px;align-items:flex-start\}.*?\.cnote\{[^}]*\}\n", "", s, count=1, flags=re.S)
assert _c == 1
s, _c = re.subn(r"\.cal\{display:flex;gap:6px\}\n.*?\.cleg i\{[^}]*\}\n", "", s, count=1, flags=re.S)
assert _c == 1
CSS415 = r"""
/* ===== v4.1.5 ===== */
.cal{--cs:14px;--cgp:3px}
.csc{overflow-x:auto;padding-bottom:6px;scrollbar-width:thin;-webkit-overflow-scrolling:touch;overscroll-behavior-x:contain}
.cmo{display:grid;grid-template-columns:repeat(var(--n,371),var(--cs));column-gap:var(--cgp);height:14px;margin-bottom:3px;font-size:10px;line-height:14px;color:var(--muted);width:max-content}
.cmo span{white-space:nowrap}
.cg{display:grid;grid-auto-flow:column;grid-template-rows:var(--cs);grid-auto-columns:var(--cs);gap:var(--cgp);width:max-content}
.cg i{display:block;border-radius:3px}
.cg .fu{display:none}
.cinfo{font-size:13px;color:var(--muted);text-align:center;margin-top:2px}
.cinfo:empty{display:none}
.cft{display:flex;justify-content:center;align-items:center;margin-top:6px;font-size:12px;color:var(--muted)}
.cleg i{display:inline-block;width:12px;height:12px;border-radius:3px;margin:0 2px;vertical-align:-2px}
.top h1{cursor:default;-webkit-tap-highlight-color:transparent;-webkit-user-select:none;user-select:none}
#fs{background:var(--accent);border-color:var(--accent);color:var(--on)}
#fo,#fnw{background:var(--soft);border-color:transparent;color:var(--muted);font-weight:700}
.pet.mp{cursor:pointer;-webkit-tap-highlight-color:transparent}
.bk h3{font-size:16px;margin:10px 0 4px}
"""
_i = s.index('</style>')
s = s[:_i] + CSS415 + s[_i:]

# ---------- версия ----------
s = s.replace("v4.1.4", "v4.1.5")

# ---------- календарь ----------
rep("function lvC(h){if(!h)return 0;var l=h.les|0;if(!l)return h.xp>0?1:0;return l>=6?4:l>=4?3:l>=2?2:1}",
    "function lvC(h){if(!h)return 0;var l=h.les|0;return l>=6?4:l>=4?3:l>=2?2:l>=1?1:0}")
_a = s.index('function regDay()')
_b = s.index('function profile()')
CAL = r"""function regDay(){if(S.reg)return S.reg;var m='';for(var k in S.hist)if(!m||k<m)m=k;return m||day(new Date())}
function calText(k){
  var p=k.split('-'),h=S.hist[k],cy=String(new Date().getFullYear()),t=(+p[2])+' '+MON[+p[1]-1]+(p[0]!==cy?' '+p[0]:''),n=h&&h.les?h.les:0;
  return t+': '+(n?n+' '+pl(n,['островок','островка','островков']):'без занятий');
}
function calHtml(){
  var t=new Date();t.setHours(12,0,0,0);var N=371,st=new Date(t);st.setDate(t.getDate()-(N-1));
  var g='',lb='',act=0,pm=-1;
  for(var n=0;n<N;n++){
    var c=new Date(st);c.setDate(st.getDate()+n);var mo=c.getMonth();
    if(mo!==pm&&(c.getDate()===1||n===0&&c.getDate()<=8))lb+='<span style="grid-column:'+(n+1)+'">'+MS3[mo]+'</span>';
    pm=mo;
    var k=day(c),l=lvC(S.hist[k]);if(l)act++;
    g+='<i class="l'+l+'" data-d="'+k+'" title="'+calText(k)+'"></i>';
  }
  return'<div class="cal" role="img" aria-label="Календарь активности. Дней с занятиями: '+act+'"><div class="csc"><div class="cmo" style="--n:'+N+'" aria-hidden="true">'+lb+'</div><div class="cg" id="cg">'+g+'</div></div></div><div class="cinfo" id="ci"></div><div class="cft"><span class="cleg" aria-hidden="true">меньше<i class="l0"></i><i class="l1"></i><i class="l2"></i><i class="l3"></i><i class="l4"></i>больше</span></div>';
}
function calBind(){
  var cg=$('cg'),sc=app.querySelector('.csc');if(!cg||!sc)return;
  var w=sc.clientWidth;if(w<100)w=300;var cs=Math.max(10,Math.min(26,Math.floor((w-20*3)/21)));$('cg').parentNode.parentNode.style.setProperty('--cs',cs+'px');sc.scrollLeft=sc.scrollWidth;
  function sh(e){var d=e.target.closest&&e.target.closest('[data-d]');if(d)$('ci').textContent=calText(d.dataset.d)}
  cg.addEventListener('click',sh);
  sc.addEventListener('wheel',function(e){if(e.shiftKey||Math.abs(e.deltaX)>Math.abs(e.deltaY))return;var mx=sc.scrollWidth-sc.clientWidth,n=sc.scrollLeft+e.deltaY;if((e.deltaY<0&&sc.scrollLeft>0)||(e.deltaY>0&&sc.scrollLeft<mx)){e.preventDefault();sc.scrollLeft=Math.max(0,Math.min(mx,n))}},{passive:false});
}
"""
s = s[:_a] + CAL + s[_b:]

# карточка «Поделиться»: те же недели, что и в профиле, не 26, а 13 для читаемости
rep("g.fillText('Активность за последние 26 недель',540,1096);", "g.fillText('Активность за последние 13 недель',540,1090);")
_a = s.index("var t=new Date();t.setHours(12,0,0,0);var s0=new Date(t);s0.setDate(t.getDate()-((t.getDay()+6)%7)-25*7)")
_b = s.index("g.fill()}\n", _a) + len("g.fill()}\n")
s = s[:_a] + """var t=new Date();t.setHours(12,0,0,0);var WK=13,s0=new Date(t);s0.setDate(t.getDate()-((t.getDay()+6)%7)-(WK-1)*7);var gx=540-(WK*24-4)/2;
    for(var w2=0;w2<WK;w2++)for(var d=0;d<7;d++){var c=new Date(s0);c.setDate(s0.getDate()+w2*7+d);if(c>t)continue;g.fillStyle=V('--c'+lvC(S.hist[day(c)]));rr(g,gx+w2*24,1106+d*24,20,20,5);g.fill()}
""" + s[_b:]

# ---------- считаем только первое прохождение ----------
rep("function bump(k){S.d[k]=1;", "function bump(k){var nw=!S.d[k];S.d[k]=1;")
rep("delete S.dr[k];hit(0,1);save()}", "delete S.dr[k];if(nw)hit(0,1);save()}")

# ---------- флажок над введением ----------
rep("(c?'<div class=\"flag\">🚩 Ты остановился здесь</div>':'')", "(c&&!TOPICS[i].intro?'<div class=\"flag\">🚩 Ты остановился здесь</div>':'')")

# ---------- вода почти до верха экрана, капля в центр ----------
rep("P=Math.round(surf/vh*1000)/10;", "P=8;")

# ---------- настройки по нажатию на «ИТП» ----------
rep("<div class=\"top\"><h1>ИТП <small", "<div class=\"top\"><h1 id=\"ttl\">ИТП <small")
rep("  var kb=$('kb');if(kb)kb.onclick=keys;\n}", "  var kb=$('kb');if(kb)kb.onclick=keys;\n  var tt=$('ttl');if(tt)tt.onclick=backup;\n}")
rep('<button class="btn g" id="bk">💾 Резервная копия</button><div class="row">', '<div class="row">')
rep("$('sh').onclick=share;$('bk').onclick=backup;", "$('sh').onclick=share;")
rep('<h2 style="font-size:20px">Резервная копия</h2><p>Прогресс хранится на этом устройстве. ',
    '<h2 style="font-size:20px">Настройки</h2><h3>Резервная копия</h3><p>Прогресс и сохранённые коды из компилятора хранятся на этом устройстве. ')
rep("Загрузка заменит текущий прогресс на сохранённый.", "Загрузка заменит текущий прогресс и сохранённые коды на те, что в файле. Файл подписан приложением: если его изменить вручную, он не загрузится.")

# ---------- пропущенные темы: после теории открыты следующие островки ----------
rep("if(i<S.start)return IT(i,j).t==='theory'||theoryOk(i);return cur()===k}",
    "if(i<S.start){if(IT(i,j).t==='theory')return 1;for(var x=0;x<j;x++)if(IT(i,x).t==='theory'&&!S.d[i+'-'+x])return 0;return 1}return cur()===k}")
_a = s.index("function nxI(i,j){")
_b = s.index("\n", _a)
s = s[:_a] + "function nxI(i,j){if(!(i<S.start)||TOPICS[i].intro)return false;var hi=-1,x,f=-1;for(x=0;x<ni(i);x++)if(S.d[i+'-'+x])hi=x;for(x=hi+1;x<ni(i);x++)if(!S.d[i+'-'+x]&&isOpen(i,x)){f=x;break}if(f<0)for(x=0;x<=hi;x++)if(!S.d[i+'-'+x]&&isOpen(i,x)){f=x;break}return f===j}" + s[_b:]

# ---------- мелочи ----------
rep("<pre>'+hl(sol)+'</pre>", "<pre class=\"cmp\">'+hl(sol)+'</pre>")
rep("%;background:var(--bad)\"></i></div><b>'+r.c+'</b>", "%\"></i></div><b>'+r.c+'</b>")
rep('<button id="fs">💾 Сохранить</button>', '<button id="fs" class="pri">💾 Сохранить</button>')
rep("var c=app.querySelector('.cur');if(c&&!REV)c.scrollIntoView({block:'center'});\n}",
    "var c=app.querySelector('.cur');if(c&&!REV)c.scrollIntoView({block:'center'});\n  var mp=app.querySelector('.pet');if(mp){mp.classList.add('mp');mp.onclick=function(){var t=app.querySelector('.isl.cur')||app.querySelector('.isl.nx');if(t)t.scrollIntoView({block:'center',behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth'})}}\n}")

# кролик: тени, внутренность ушей, блик в глазу, нос, усы
rep('<ellipse cx="68" cy="72" rx="34" ry="21" fill="var(--rab)"/>',
    '<ellipse cx="68" cy="72" rx="34" ry="21" fill="var(--rab)"/><ellipse cx="68" cy="85" rx="28" ry="8" fill="#000" opacity=".07"/><ellipse cx="76" cy="77" rx="19" ry="10" fill="#fff" opacity=".35"/>')
rep('<circle cx="101" cy="70" r="8" fill="var(--rab)"/>', '<circle cx="101" cy="70" r="8" fill="var(--rab)"/><circle cx="103" cy="68" r="4.5" fill="#fff" opacity=".55"/>')
rep('<ellipse cx="60" cy="22" rx="7" ry="19" fill="var(--rab)"/>',
    '<ellipse cx="60" cy="22" rx="7" ry="19" fill="var(--rab)"/><ellipse cx="44" cy="25" rx="3.3" ry="12" fill="#F3B6BD" opacity=".9"/><ellipse cx="60" cy="23" rx="3.3" ry="12" fill="#F3B6BD" opacity=".9"/>')
rep('<circle cx="45" cy="49" r="2.8" fill="var(--ink)"/>',
    '<ellipse cx="45" cy="49" rx="3.3" ry="4" fill="var(--ink)"/><circle cx="46.3" cy="47.5" r="1.3" fill="#fff"/><ellipse cx="33.5" cy="54" rx="2.3" ry="1.8" fill="#E9697A"/><path d="M33.5 55.5 Q36 59.5 41 57" fill="none" stroke="var(--ink)" stroke-width="1.3" stroke-linecap="round"/><path d="M31 53 L22 50 M31 56 L22 59" stroke="var(--ink)" stroke-width="1" opacity=".45" stroke-linecap="round"/>')

# ---------- защита данных: проверка, подпись, транзакционный импорт ----------
_a = s.index("function clean(r){")
_b = s.index("/* Хранилище.")
CLEAN = r"""function clean(r){if(!r||typeof r!=='object'||Array.isArray(r))r={};
  var TM=day(ago(-1)),CUT=day(ago(370)),XC=TOPICS.reduce(function(a,t){return a+(t.items||[]).length},0)*80+500;
  var N=function(x,mx){return typeof x==='number'&&Number.isFinite(x)&&x>=0?Math.min(mx,Math.floor(x)):0},
  dt=function(x){if(typeof x!=='string'||!/^\d{4}-\d\d-\d\d$/.test(x))return'';var y=+x.slice(0,4),mo=+x.slice(5,7),d=+x.slice(8,10);if(y<2020||y>2100||mo<1||mo>12||d<1||d>31)return'';var t=new Date(y,mo-1,d,12);return t.getFullYear()===y&&t.getMonth()===mo-1&&t.getDate()===d?x:''},
  dtn=function(x){x=dt(x);return x&&x<=TM?x:''},
  vi=function(k){var m=/^(\d{1,3})-(\d{1,3})$/.exec(k);return!!m&&+m[1]<TOPICS.length&&+m[2]<ni(+m[1])},
  vt=function(k){var m=/^(\d{1,3})-(\d{1,3})-(\d{1,3})$/.exec(k);if(!m||+m[1]>=TOPICS.length||+m[2]>=ni(+m[1]))return false;var it=IT(+m[1],+m[2]);return!!(it.tasks&&+m[3]<it.tasks.length)},
  mk=function(x,ok,vk){var a={},c=0;if(x&&typeof x==='object'&&!Array.isArray(x))for(var k in x)if(Object.prototype.hasOwnProperty.call(x,k)&&vk(k)&&ok(x[k])&&c++<600)a[k]=x[k];return a};
  var nt=Object.create(null),c=0;if(r.nt&&typeof r.nt==='object')for(var k in r.nt){if(c<300&&k.length<=40&&typeof r.nt[k]==='string'){nt[k]=r.nt[k].slice(0,1000);c++}}
  var hs={},hn=0;if(r.hist&&typeof r.hist==='object'&&!Array.isArray(r.hist))for(var hk in r.hist){var hv=r.hist[hk];if(hn<400&&dtn(hk)&&hk>=CUT&&hv&&typeof hv==='object'){hs[hk]={xp:N(hv.xp,3000),les:N(hv.les,200)};hn++}}
  var sv=[],ids=Object.create(null);if(Array.isArray(r.sv))r.sv.slice(0,200).forEach(function(x){if(sv.length<30&&x&&typeof x==='object'&&typeof x.id==='string'&&/^[A-Za-z0-9]{1,24}$/.test(x.id)&&!ids[x.id]&&typeof x.c==='string'&&typeof x.n==='string'){ids[x.id]=1;sv.push({id:x.id,n:Array.from(x.n).slice(0,40).join('')||'Без названия',c:x.c.slice(0,4000),t:N(x.t,4102444800000)})}});
  var cu=typeof r.cur==='string'&&ids[r.cur]?r.cur:'';
  var dr=cd(r.dr),dr2={};for(var dk in dr)if(vi(dk))dr2[dk]=dr[dk];
  var streak=N(r.streak,3660),mx=Math.max(N(r.max,3660),streak);
  return{d:mk(r.d,function(v){return v===1},vi),tk:mk(r.tk,function(v){return v===1},vt),at:mk(r.at,function(v){return v==='low'||v==='full'||v==='rep'||v==='skip'},vi),es:mk(r.es,function(v){return Number.isInteger(v)&&v>=0&&v<100},vi),nt:nt,nick:typeof r.nick==='string'?Array.from(r.nick.trim()).slice(0,16).join(''):'',start:Number.isInteger(r.start)&&r.start>=-1&&r.start<TOPICS.length?r.start:-1,xp:N(r.xp,XC),streak:streak,last:dtn(r.last),seen:dtn(r.seen),theme:r.theme==='light'||r.theme==='dark'?r.theme:'',mute:r.mute===1||r.mute===true?1:0,max:mx,ec:typeof r.ec==='string'?r.ec.slice(0,4000):'',dr:dr2,dsort:r.dsort?1:0,hc:r.hc?1:0,hist:hs,sv:sv,cur:cu,reg:dtn(r.reg)}}
"""
s = s[:_a] + CLEAN + s[_b:]
rep("er:Math.max(0,v.er|0)", "er:Math.min(999,Math.max(0,v.er|0))")
rep("err:Math.max(0,v.err|0)", "err:Math.min(999,Math.max(0,v.err|0))")
rep("set:function(v){mem=v;", "set:function(v){if(typeof v!=='string'||v.length>2000000)return false;mem=v;")

_a = s.index("function exportData()")
_b = s.index("function backup()")
EXP = r"""var SECRET='ИТП·k7Qx2mVz9Lr4Ns8Jd3Wp·2026';
function sig(str,sec){var a=0x811c9dc5,b=0x9747b28c,t=sec+'|'+str+'|'+sec;for(var i=0;i<t.length;i++){var c=t.charCodeAt(i);a^=c;a=Math.imul(a,0x01000193);b^=(c+i)&0xffff;b=Math.imul(b,0x01000193)}a^=a>>>15;b^=b>>>13;return(a>>>0).toString(16).padStart(8,'0')+(b>>>0).toString(16).padStart(8,'0')}
function exportData(){var p=JSON.stringify({v:'4.1.5',t:new Date().toISOString(),data:clean(S)});return JSON.stringify({app:'ITP',f:2,p:p,s:sig(p,SECRET)})}
function importData(txt){
  if(typeof txt!=='string')return'Это не файл ИТП';
  if(txt.length>2000000)return'Файл слишком большой (максимум 2 МБ)';
  var o;try{o=JSON.parse(txt)}catch(e){return'Это не похоже на сохранение ИТП'}
  if(!o||typeof o!=='object')return'Это не файл ИТП';
  if(typeof o.p!=='string'||typeof o.s!=='string')return o.data?'Копия сделана старой версией и не имеет подписи, загрузить её нельзя':'Файл повреждён или подделан';
  if(o.s!==sig(o.p,SECRET))return'Файл повреждён или подделан';
  var d;try{d=JSON.parse(o.p)}catch(e){return'Файл повреждён или подделан'}
  if(!d||typeof d!=='object'||!d.data||typeof d.data!=='object')return'В файле нет данных ИТП';
  var r=clean(d.data);if(!r.nick)return'В сохранении нет ника, это не файл ИТП';
  if(['xp','streak','max'].some(function(k){return typeof d.data[k]==='number'&&d.data[k]!==r[k]}))return'Файл повреждён или подделан';
  var bak=JSON.stringify(S);
  try{S=r;seedLit();save();var chk=JSON.parse(Store.get()||'null');if(!chk||chk.nick!==r.nick)throw 1}
  catch(e){try{S=clean(JSON.parse(bak));seedLit();save()}catch(e2){}return'Не получилось сохранить данные, прогресс оставлен прежним'}
  return''}
"""
s = s[:_a] + EXP + s[_b:]
