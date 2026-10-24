/* ===================== ИТП 6.6 — вступление: заставка, терминал на ЭЛТ-мониторе, «синий экран» =====================
   Первый запуск: заставка со светящимся растровым кроликом (как логотип студии перед игрой) → терминал на старом
   скруглённом мониторе, за текстом еле заметно стекают символы → кролик спрашивает ник, обращение и первую тему →
   «синий экран», который трескается и осыпается осколками, а под ним уже Путь. Если ник есть, а тема не выбрана,
   терминал открывается сразу с вопросом о теме, без заставки.
   Кролик — та же картинка, что у иконки профиля (--pi-o и --pi-f из build5.py): из неё кодом делаются растр заставки
   и контур для терминала. Всё рисуется кодом (canvas, CSS, SVG). При «меньше движения» нет дождя, печати и осколков.
   Переопределяет nick() и place() из a_screens.js, поэтому сброс прогресса тоже приводит сюда. */

var CRT=null,RBIMG=null;
var CRTG='01{}[]()<>=+-*/%#:;._$&|λabcdefghijklmnopqrstuvwxyzабвгдежзиклмнопрстуфхцчшэюя';
function nick(){crtOpen()}
function place(){crtOpen()}

/* --- картинка кролика: контур (для терминала) и карта «контур / заливка / пусто» (для растра заставки) --- */
function rbLoad(cb){
  if(RBIMG)return cb(RBIMG);
  var cs=getComputedStyle(document.documentElement);
  function src(v){var m=/url\(["']?([^"')]+)/.exec(cs.getPropertyValue(v));return m?m[1]:''}
  var a=new Image(),b=new Image(),n=0,so=src('--pi-o'),sf=src('--pi-f');
  if(!so)return cb(null);
  function one(){if(++n<2)return;try{
    var w=a.naturalWidth,h=a.naturalHeight,c=document.createElement('canvas');c.width=w;c.height=h;
    var x=c.getContext('2d');x.drawImage(a,0,0);var d=x.getImageData(0,0,w,h).data;
    x.clearRect(0,0,w,h);if(b.naturalWidth)x.drawImage(b,0,0,w,h);var f=x.getImageData(0,0,w,h).data;
    var o=x.createImageData(w,h),v=new Float32Array(w*h);
    for(var i=0;i<w*h;i++){
      var al=d[i*4+3]/255,l=(d[i*4]+d[i*4+1]+d[i*4+2])/765,ln=Math.min(1,al*(1-l)*1.4);
      o.data[i*4+3]=Math.round(255*ln);
      /* 1 — линия, .5 — внутри кролика (заливка профиля или белое внутри контура), 0 — снаружи */
      v[i]=ln>.5?1:(f[i*4+3]>128||(al>.5&&l>.5))?.5:0}
    x.putImageData(o,0,0);RBIMG={ol:c.toDataURL(),v:v,w:w,h:h}}catch(e){RBIMG=null}cb(RBIMG)}
  a.onload=a.onerror=one;b.onload=b.onerror=one;a.src=so;if(sf)b.src=sf;else one()}

/* растр как на старом люминофоре: линии — крупные точки, тело — мелкие и неровные, вокруг редкая пыль */
function rbHalftone(cv){
  var R=RBIMG;if(!R||!cv.isConnected)return;
  var dpr=Math.min(2,window.devicePixelRatio||1),W=cv.clientWidth||220,H=W*R.h/R.w,N=44,st=W/N,x=cv.getContext('2d');
  cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);x.scale(dpr,dpr);x.fillStyle='#ffb347';
  for(var gy=0;gy<H/st;gy++)for(var gx=0;gx<N;gx++){
    var x0=Math.floor(gx*st/W*R.w),x1=Math.floor((gx+1)*st/W*R.w),y0=Math.floor(gy*st/H*R.h),y1=Math.min(R.h,Math.floor((gy+1)*st/H*R.h)),s=0,c=0,ol=0;
    for(var yy=y0;yy<y1;yy++)for(var xx=x0;xx<x1;xx++){var q=R.v[yy*R.w+xx];s+=q;c++;if(q===1)ol++}
    if(!c)continue;var val=s/c,cx=(gx+.5)*st,cy=(gy+.5)*st;
    if(ol/c>.25)val=.75+.25*ol/c;
    else if(val>.2)val=.16+.3*(.5+.25*Math.sin(gx*.55+gy*.21)+.25*Math.sin(gx*.13-gy*.47)+(Math.random()-.5)*.5);
    else if(Math.random()<.035)val=.05+Math.random()*.08;else continue;
    if(val<=0)continue;
    x.globalAlpha=Math.min(1,.35+val);x.beginPath();x.arc(cx,cy,st*.52*Math.sqrt(Math.min(1,val)),0,6.2832);x.fill()}}

/* --- дождь символов за текстом терминала: еле заметный, 20 кадров в секунду --- */
function rainStart(cv){
  if(RM())return null;
  var x=cv.getContext('2d'),R={on:1,raf:0,last:0,cols:[]},fs=14,dpr=1,W=0,H=0;
  function rc(){return CRTG[Math.floor(Math.random()*CRTG.length)]}
  function col(init){var n=8+Math.floor(Math.random()*18),ch=[];for(var k=0;k<n;k++)ch.push(rc());
    return{y:init?Math.random()*(H/fs+n)-n:-Math.random()*30,sp:.12+Math.random()*.32,n:n,ch:ch,a:.04+Math.random()*.07}}
  function fit(){dpr=Math.min(2,window.devicePixelRatio||1);W=cv.clientWidth;H=cv.clientHeight;cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);
    fs=W<600?13:15;R.cols=[];for(var i=0,m=Math.ceil(W/fs);i<m;i++)R.cols.push(col(true))}
  function fr(t){
    if(!R.on)return;R.raf=requestAnimationFrame(fr);if(t-R.last<50)return;R.last=t;
    x.setTransform(dpr,0,0,dpr,0,0);x.clearRect(0,0,W,H);x.font=fs+'px '+getComputedStyle(cv).fontFamily;x.textBaseline='top';
    for(var i=0;i<R.cols.length;i++){var c=R.cols[i];c.y+=c.sp;if(Math.random()<.05)c.ch[Math.floor(Math.random()*c.n)]=rc();
      var hy=Math.floor(c.y);if((hy-c.n)*fs>H){R.cols[i]=col(false);continue}
      for(var k=0;k<c.n;k++){var yy=hy-k;if(yy<0||yy*fs>H)continue;
        x.fillStyle='rgba(120,255,160,'+(k?c.a*(1-k/c.n):Math.min(.3,c.a*2.8)).toFixed(3)+')';x.fillText(c.ch[yy%c.n],i*fs,yy*fs)}}}
  fit();R.fit=fit;window.addEventListener('resize',fit);R.raf=requestAnimationFrame(fr);
  R.stop=function(){R.on=0;cancelAnimationFrame(R.raf);window.removeEventListener('resize',fit)};
  return R}

/* --- монитор --- */
function crtT(f,ms){var t=setTimeout(f,ms);if(CRT)CRT.tms.push(t);return t}
function crtW(ms){return new Promise(function(r){crtT(r,CRT&&(CRT.fast||CRT.rm)?0:ms)})}
function crtClose(keep){
  if(!CRT)return;var c=CRT;CRT=null;
  c.tms.forEach(clearTimeout);c.off.forEach(function(f){f()});if(c.rain)c.rain.stop();
  c.el.remove();if(!keep)document.documentElement.classList.remove('crt-on')}
function crtOpen(){
  crtClose();var bx=document.getElementById('shards');if(bx)bx.remove();bx=document.getElementById('bsod');if(bx)bx.remove();
  scr('nick','');window.scrollTo(0,0);
  var full=!S.nick,rm=RM(),o=document.createElement('div');o.id='crt';o.className='crt'+(rm?' rm':'');
  o.innerHTML='<div class="bz"><div class="sc"><div class="sci"><canvas class="rain" aria-hidden="true"></canvas>'+(full?'<div class="spl" aria-hidden="true"><canvas class="lg"></canvas><i class="sg">▮</i><div class="bl">IT&#39;S THE PROGRAMMING</div></div>':'')+'<div class="tm" role="log" aria-live="polite" aria-label="Знакомство с ИТП"><div class="tmi"></div></div></div><i class="fx" aria-hidden="true"></i></div></div>';
  document.body.appendChild(o);document.documentElement.classList.add('crt-on');
  CRT={el:o,tm:o.querySelector('.tm'),log:o.querySelector('.tmi'),tms:[],off:[],fast:0,rm:rm,rain:null,spl:null,touch:'ontouchstart' in window};
  /* касание или клавиша: пропустить заставку, допечатать текущую реплику */
  function hurry(e){if(!CRT)return;if(CRT.spl){CRT.spl();return}
    var t=e.target;if(t&&t.closest&&t.closest('input,button'))return;if(e.type==='keydown'&&(e.ctrlKey||e.metaKey||e.altKey||e.key==='Tab'))return;CRT.fast=1}
  o.addEventListener('pointerdown',hurry);document.addEventListener('keydown',hurry,true);
  CRT.off.push(function(){document.removeEventListener('keydown',hurry,true)});
  rbLoad(function(R){if(!CRT||CRT.el!==o)return;if(R)o.style.setProperty('--rb','url('+R.ol+')');var lg=o.querySelector('.lg');if(lg)rbHalftone(lg)});
  (full?crtSplash():Promise.resolve()).then(function(){if(CRT&&CRT.el===o)crtDialog(full)})}

/* заставка: кролик разгорается с мерцанием, как неоновая лампа, держится и гаснет вспышкой */
function crtSplash(){return new Promise(function(res){
  var sp=CRT.el.querySelector('.spl'),ok=0;sp.classList.add('on');
  function go(){if(ok||!CRT)return;ok=1;CRT.spl=null;sp.classList.add('out');crtT(function(){sp.remove();res()},CRT.rm?0:650)}
  CRT.spl=go;crtT(go,CRT.rm?1600:3900)})}

function crtScroll(el){var t=CRT&&CRT.tm;if(!t)return;
  if(el&&el.offsetHeight>t.clientHeight*.6)t.scrollTop=Math.max(0,el.offsetTop-t.clientHeight*.25);else t.scrollTop=t.scrollHeight}
function crtRow(h,cls,tag){var e=document.createElement(tag||'div');e.className=cls;e.innerHTML=h;CRT.log.appendChild(e);crtScroll(e);return e}
/* печать по буквам; на точках и запятых пауза */
function crtType(el,s,ms){return new Promise(function(res){
  if(!CRT)return;if(CRT.rm){el.textContent=s;crtScroll();return res()}
  var i=0;el.classList.add('typ');
  (function st(){if(!CRT)return;i=CRT.fast?s.length:i+1;el.textContent=s.slice(0,i);crtScroll();
    if(i>=s.length){el.classList.remove('typ');return res()}
    var c=s[i-1];crtT(st,(ms||28)*(/[.?!]/.test(c)?8:c===','?4:1)*(.6+Math.random()*.8))})()})}
function crtSys(lines){var p=Promise.resolve();
  lines.forEach(function(s){p=p.then(function(){if(!CRT)return;var e=crtRow('','tl sys');return crtType(e,s,7).then(function(){return crtW(110)})})});
  return p}
function crtSay(lines){
  var r=crtRow('<i class="rb" aria-hidden="true"></i><span class="ds" aria-hidden="true">—</span><div class="tx"></div>','tr'),tx=r.querySelector('.tx'),p=crtW(260);
  lines.forEach(function(s,k){p=p.then(function(){if(!CRT)return;var e=document.createElement('p');tx.appendChild(e);return crtType(e,s).then(function(){return crtW(k<lines.length-1?380:220)})})});
  return p.then(function(){if(CRT)CRT.fast=0})}
function crtYou(s){if(!CRT)return;var e=crtRow('','tl you');e.textContent=s}

/* поле ввода: рамка, «…» и мигающий блок-курсор; само поле настоящее (клавиатура телефона, вставка) */
function crtAsk(max){return new Promise(function(res){
  var f=crtRow('<label class="tbx"><span class="sr-only">Как тебя зовут?</span><span class="tvw" aria-hidden="true"><span class="tv"></span></span><span class="ph" aria-hidden="true">…</span><i class="cu" aria-hidden="true"></i><input id="nk" maxlength="'+max+'" autocomplete="off" autocapitalize="words" autocorrect="off" spellcheck="false" enterkeyhint="done"></label><button class="tgo" id="go" type="submit" disabled aria-label="Дальше">⏎</button>','tin','form');
  var i=f.querySelector('input'),tv=f.querySelector('.tv'),g=f.querySelector('#go');
  f.setAttribute('autocomplete','off');
  i.oninput=function(){tv.textContent=i.value;f.classList.toggle('has',!!i.value);g.disabled=!i.value.trim()};
  f.onsubmit=function(e){e.preventDefault();var v=i.value.trim();if(!v){i.focus();return}i.blur();f.remove();crtYou('> '+v);res(v.slice(0,max))};
  if(!CRT.touch)setTimeout(function(){i.focus({preventScroll:true})},60)})}

/* меню: стрелки, цифры (если пунктов меньше десяти), Enter или касание */
function crtMenu(items,lab){return new Promise(function(res){
  var m=crtRow(items.map(function(it,k){return'<button type="button" class="tmo'+(it.c?' '+it.c:'')+'"'+(it.a||'')+' data-k="'+k+'"><span class="mk" aria-hidden="true">▸</span>'+it.h+'</button>'}).join(''),'tmn');
  m.setAttribute('role','group');m.setAttribute('aria-label',lab);
  var bs=[].slice.call(m.querySelectorAll('button')),sel=0,done=0;
  function hi(n){sel=(n+bs.length)%bs.length;bs.forEach(function(b,k){b.classList.toggle('hi',k===sel)})}
  function pick(k){if(done)return;done=1;bs.forEach(function(b){b.disabled=true});bs[k].classList.add('pk');crtT(function(){res(k)},CRT.rm?0:280)}
  function kd(e){if(done||!CRT||e.ctrlKey||e.metaKey||e.altKey)return;
    if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();hi(sel+(e.key==='ArrowDown'?1:-1));bs[sel].focus();bs[sel].scrollIntoView({block:'nearest'})}
    else if(bs.length<10&&/^[1-9]$/.test(e.key)&&+e.key<=bs.length){e.preventDefault();snd('tap');pick(+e.key-1)}}
  bs.forEach(function(b,k){b.onclick=function(){pick(k)};b.onfocus=b.onpointerenter=function(){if(!done)hi(k)}});
  document.addEventListener('keydown',kd,true);CRT.off.push(function(){document.removeEventListener('keydown',kd,true)});
  hi(0);if(!CRT.touch)bs[0].focus({preventScroll:true})})}

/* --- разговор --- */
function crtDialog(full){
  CRT.el.classList.add('live');CRT.rain=rainStart(CRT.el.querySelector('.rain'));
  var p=full?crtSys(['ITP BIOS v'+ITPV,'(c) It\'s The Programming','Проверка памяти ......... 640K OK','Интерпретатор Python .... найден','Кролик .................. на связи']):Promise.resolve();
  if(!S.nick)p=p.then(function(){return crtSay(['Привет.','Как я могу к тебе обращаться?'])}).then(function(){return crtAsk(20)}).then(function(v){
    S.nick=v;return crtSay(['Приятно познакомиться, '+v+'.','Ты парень или девушка? Это нужно, чтобы окончания в тексте были правильными.'])}).then(function(){
    return crtMenu([['m','Парень'],['f','Девушка'],['','Не указывать']].map(function(x,k){return{c:'tgd',a:' data-g="'+x[0]+'"',h:'<span class="tno">['+(k+1)+']</span>'+x[1]}}),'Как к тебе обращаться')}).then(function(k){
    S.g=['m','f',''][k];if(!S.reg)S.reg=day(new Date());save();crtYou('> '+['Парень','Девушка','Не указывать'][k])});
  else p=p.then(function(){return crtSay(['С возвращением, '+S.nick+'.'])});
  p.then(function(){if(CRT)return crtSay(['С чего начнём?','Выбери первую тему, которую ещё не знаешь. Пропущенные можно пройти потом.'])}).then(function(){
    if(!CRT)return;
    var f=TOPICS[0]&&TOPICS[0].intro?1:0,ix=[],n=0;
    var it=[];TOPICS.forEach(function(t,i){if(t.intro||t.opt)return;n++;ix.push(i);var z=i===f;
      it.push({c:'tpc'+(z?' rec':''),a:' data-i="'+i+'"',h:'<span class="tno">'+(n<10?'0':'')+n+'</span><span class="ct">'+(z?'С нуля: ':'')+esc(t.n)+'<small>'+esc(t.s||'')+'</small></span>'})});
    return crtMenu(it,'Первая тема').then(function(k){var i=ix[k];S.start=i===f?0:i;save();crtYou('> '+TOPICS[i].n);return crtLaunch()})})}

/* «загрузка» с полоской, потом сбой */
function crtLaunch(){
  var e=crtRow('','tl sys'),n=0;
  return new Promise(function(res){(function st(){if(!CRT)return;
    e.textContent='Запуск ИТП ['+'#'.repeat(n)+'.'.repeat(20-n)+'] '+n*5+'%';crtScroll();
    if(n>=20)return crtT(res,CRT.rm?0:320);n=Math.min(20,n+1+Math.floor(Math.random()*3));crtT(st,CRT.rm?0:70+Math.random()*90)})()}).then(function(){
    if(!CRT)return;var w=crtRow('','tl err');w.textContent='FATAL 0x0000C0DE: вступление закончилось';return crtW(380)}).then(crtCrash)}

/* --- сбой: помехи → синий экран → трещины → осколки, под ними Путь --- */
function crtCrash(){
  if(!CRT)return;
  fzApply();S.seen=day(new Date());save();
  home();window.scrollTo(0,0);
  if(CRT.rm){var c=CRT.el;c.classList.add('fade');crtT(function(){crtClose()},450);return}
  CRT.el.classList.add('gl');snd('err');
  crtT(function(){crtClose(1);bsod()},720)}

/* картинка в духе QR-кода: три «глазка» по углам, остальное — случайные клетки */
function bsQr(){
  var d='',N=25,R=sxRng?sxRng(20261024):Math.random;
  function eye(x,y){d+='M'+x+' '+y+'h7v7h-7zM'+(x+1)+' '+(y+1)+'v5h5v-5zM'+(x+2)+' '+(y+2)+'h3v3h-3z'}
  for(var y=0;y<N;y++)for(var x=0;x<N;x++){if((x<8&&y<8)||(x>N-9&&y<8)||(x<8&&y>N-9))continue;if(R()<.47)d+='M'+x+' '+y+'h1v1h-1z'}
  eye(0,0);eye(N-7,0);eye(0,N-7);
  return'<svg viewBox="-1 -1 27 27" shape-rendering="crispEdges" aria-hidden="true" focusable="false"><path fill="currentColor" fill-rule="evenodd" d="'+d+'"/></svg>'}
function bsod(){
  var b=document.createElement('div'),tms=[],gone=0,nm=S.nick||'';b.id='bsod';b.setAttribute('role','alert');
  b.innerHTML='<div class="bsv"><div class="bsi"><div class="sad" aria-hidden="true">:(</div><p class="bm">В ИТП возникла проблема, и его нужно перезапустить. Мы лишь подготовим островки'+(nm?' для '+esc(nm):'')+', и всё заработает.</p><p class="bp"><b>0</b>% выполнено</p><div class="bq">'+bsQr()+'<div><p>Это не настоящая ошибка, а начало курса.</p><p>Код остановки: HELLO_WORLD</p></div></div></div></div>';
  document.body.appendChild(b);
  function T(f,ms){tms.push(setTimeout(f,ms))}
  /* касание — сразу к Пути */
  function end(){if(gone)return;gone=1;tms.forEach(clearTimeout);b.remove();var x=document.getElementById('shards');if(x)x.remove();document.documentElement.classList.remove('crt-on')}
  b.onclick=end;
  var pc=b.querySelector('.bp b'),steps=[0,3,3,11,24,24,41,67,88,100];
  steps.forEach(function(v,k){T(function(){pc.textContent=v},180*k)});
  T(function(){bsCrack(b,T,end)},180*steps.length+250)}

function bsCrack(b,T,end){
  var w=innerWidth,h=innerHeight,cx=w*.5,cy=h*.44,K=w<600?9:12,D=Math.hypot(w,h),RR=[0,.05,.13,.26,.45,1.05],P=[],ang=[],i,j;
  for(i=0;i<K;i++)ang.push((i+(Math.random()-.5)*.6)/K*6.2832);
  for(i=0;i<K;i++){P.push([]);for(j=0;j<RR.length;j++){var a=ang[i]+(Math.random()-.5)*.14,r=RR[j]*D*(j?.85+Math.random()*.3:0);P[i].push([cx+Math.cos(a)*r,cy+Math.sin(a)*r])}}
  var sv='<svg class="ck" viewBox="0 0 '+w+' '+h+'" preserveAspectRatio="none" aria-hidden="true"><circle class="imp" cx="'+cx+'" cy="'+cy+'" r="10"/>',ps=[];
  function seg(pts,dl){var d='M'+pts.map(function(p){return p[0].toFixed(1)+' '+p[1].toFixed(1)}).join('L'),L=0;
    for(var k=1;k<pts.length;k++)L+=Math.hypot(pts[k][0]-pts[k-1][0],pts[k][1]-pts[k-1][1]);
    ps.push([d,Math.ceil(L),dl])}
  for(i=0;i<K;i++)seg(P[i],Math.random()*60);
  for(j=1;j<RR.length-1;j++)for(i=0;i<K;i++)if(Math.random()<(j<3?.85:.55))seg([P[i][j],P[(i+1)%K][j]],160+j*70+Math.random()*60);
  /* у каждой трещины тёмная подложка (cu2) и светлый скол (cl), обе прорисовываются от точки удара */
  ps.forEach(function(p){var st=' d="'+p[0]+'" style="--l:'+p[1]+';animation-delay:'+p[2].toFixed(0)+'ms"/>';sv+='<path class="cu2"'+st+'<path class="cl"'+st});
  b.querySelector('.bsv').insertAdjacentHTML('beforeend',sv+'</svg>');
  b.classList.add('hit');
  T(function(){bsShatter(b,P,K,RR.length,cx,cy,w,h,D,T,end)},720)}

function bsShatter(b,P,K,J,cx,cy,w,h,D,T,end){
  var v=b.querySelector('.bsv'),box=document.createElement('div'),dmax=0;box.id='shards';box.onclick=end;
  for(var i=0;i<K;i++)for(var j=0;j<J-1;j++){
    var pts=[P[i][j],P[(i+1)%K][j],P[(i+1)%K][j+1],P[i][j+1]],xs=pts.map(function(p){return p[0]}),ys=pts.map(function(p){return p[1]});
    var x0=Math.max(0,Math.floor(Math.min.apply(0,xs))),y0=Math.max(0,Math.floor(Math.min.apply(0,ys))),x1=Math.min(w,Math.ceil(Math.max.apply(0,xs))),y1=Math.min(h,Math.ceil(Math.max.apply(0,ys)));
    if(x1-x0<2||y1-y0<2)continue;
    var d=document.createElement('div'),inn=document.createElement('div');d.className='shd';inn.className='shi';
    d.style.cssText='left:'+x0+'px;top:'+y0+'px;width:'+(x1-x0)+'px;height:'+(y1-y0)+'px;clip-path:polygon('+pts.map(function(p){return(p[0]-x0).toFixed(1)+'px '+(p[1]-y0).toFixed(1)+'px'}).join(',')+')';
    inn.style.cssText='left:'+(-x0)+'px;top:'+(-y0)+'px;width:'+w+'px;height:'+h+'px';
    inn.appendChild(v.cloneNode(true));d.appendChild(inn);box.appendChild(d);
    var mx=(xs[0]+xs[1]+xs[2]+xs[3])/4-cx,my=(ys[0]+ys[1]+ys[2]+ys[3])/4-cy,ds=Math.hypot(mx,my)/D;dmax=Math.max(dmax,ds);
    var dx=mx*.45+(Math.random()-.5)*160,dy=h*(.75+Math.random()*.55)+my*.25,du=1050+Math.random()*550,dl=ds*420;
    d.animate([{transform:'none',opacity:1},
      {transform:'translate('+(mx*.035).toFixed(1)+'px,'+(my*.035).toFixed(1)+'px)',opacity:1,offset:.1},
      {transform:'translate('+dx.toFixed(1)+'px,'+dy.toFixed(1)+'px) rotateX('+((Math.random()-.5)*120).toFixed(0)+'deg) rotateY('+((Math.random()-.5)*120).toFixed(0)+'deg) rotate('+((Math.random()-.5)*90).toFixed(0)+'deg) scale(.9)',opacity:0}],
      {duration:du,delay:dl,easing:'cubic-bezier(.42,0,.85,.6)',fill:'both'})}
  document.body.appendChild(box);b.remove();snd('level');
  app.animate([{filter:'brightness(.35) blur(6px)',transform:'scale(1.05)'},{filter:'brightness(1) blur(0)',transform:'none'}],{duration:1300,easing:'cubic-bezier(.2,.8,.2,1)'});
  T(end,1700+dmax*420)}
