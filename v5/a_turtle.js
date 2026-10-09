/* v5.4.0: окно «Черепаха». Python считает фигуру (модуль turtle), здесь она рисуется на координатной плоскости. */
(function(){
var TW={last:null,el:null,st:null,raf:0};
var ex0=exec;
exec=function(code,src){
  return ex0(code,src).then(function(r){
    if(r&&r.turtle&&src&&src.live){try{TW.last=JSON.parse(r.turtle)}catch(e){TW.last=null}TW.code=code;if(TW.last)TW.open(TW.last)}
    return r})};
TW.run=function(code,done){
  var o=null;
  return exec(code,{live:function(){}}).then(function(r){
    if(r&&r.err&&done)done(r.err);
    else if(r&&!r.turtle&&done)done('Программа ничего не нарисовала: в ней нет команд turtle.');
    return r})};
function esc2(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function nice(x){var e=Math.pow(10,Math.floor(Math.log(x)/Math.LN10)),m=x/e;return(m<=1?1:m<=2?2:m<=5?5:10)*e}
function fmt(v){var r=Math.round(v*100)/100;return String(r).replace('-','−')}
function bbox(D){
  var a=[0,0,0,0],f=0;
  function add(x,y,r){r=r||0;if(!f){a=[x-r,y-r,x+r,y+r];f=1;return}a[0]=Math.min(a[0],x-r);a[1]=Math.min(a[1],y-r);a[2]=Math.max(a[2],x+r);a[3]=Math.max(a[3],y+r)}
  add(0,0,0);
  D.ops.forEach(function(o){
    if(o[0]===0){add(o[1],o[2]);add(o[3],o[4])}
    else if(o[0]===3){o[1].forEach(function(p){add(p[0],p[1])})}
    else add(o[1],o[2])});
  D.tur.forEach(function(t){add(t[0],t[1])});
  return a}
TW.open=function(D){
  TW.close(true);
  var old=document.activeElement;
  var el=document.createElement('div');el.className='tuw';el.setAttribute('role','dialog');el.setAttribute('aria-label','Окно черепахи');
  el.innerHTML='<div class="tuc"><div class="tuh"><b>🐢 Черепаха</b><span class="tun" id="tun"></span><button class="tux" id="tux" aria-label="Закрыть окно черепахи">✕</button></div>'+
  '<div class="tucv"><canvas id="tucv" role="img" aria-label="Рисунок черепахи на координатной плоскости"></canvas><div class="tuz"><button id="tuzi" aria-label="Приблизить">＋</button><button id="tuzo" aria-label="Отдалить">−</button><button id="tuzf" aria-label="Показать весь рисунок">⌖</button></div></div>'+
  '<div class="tuinfo" id="tuinfo" aria-live="polite"></div>'+
  '<div class="turow"><button class="tub" id="tupl">↻ Заново</button><button class="tub on" id="tugr" aria-pressed="true">Сетка</button><button class="tub" id="tupt" aria-pressed="false">Точки</button><button class="tub" id="tumk" aria-pressed="false">Отмечать</button></div>'+
  '<div class="tumark" id="tumark" hidden><span id="tumn"></span><button class="tub" id="tumc">Сбросить отметки</button></div></div>';
  document.body.appendChild(el);document.body.classList.add('tuopen');TW.el=el;
  var cv=el.querySelector('#tucv'),ctx=cv.getContext('2d'),info=el.querySelector('#tuinfo');
  var S={D:D,vx:0,vy:0,sc:1,grid:true,pts:false,mk:false,marks:{},p:1,anim:0,sel:null};TW.st=S;
  var N=D.ops.length;
  el.querySelector('#tun').textContent=N+' '+(N%10===1&&N%100!==11?'действие':(N%10>=2&&N%10<=4&&(N%100<10||N%100>=20))?'действия':'действий');
  function fit(){
    var b=bbox(D),W=cv.clientWidth||300,H=cv.clientHeight||300;
    if(D.w){b=[D.w[0],D.w[1],D.w[2],D.w[3]]}
    var w=Math.max(b[2]-b[0],1e-6),h=Math.max(b[3]-b[1],1e-6),pad=D.w?0:.14;
    var sc=Math.min(W/(w*(1+2*pad)),H/(h*(1+2*pad)));
    if(!isFinite(sc)||sc<=0)sc=1;
    if(!D.w){ // красивый масштаб: целое число пикселей на единицу, если фигура небольшая
      if(sc>6)sc=Math.floor(sc/ (sc>20?5:1))*(sc>20?5:1)||sc}
    S.sc=sc;S.vx=(b[0]+b[2])/2;S.vy=(b[1]+b[3])/2}
  function size(){
    var dpr=window.devicePixelRatio||1,W=cv.clientWidth,H=cv.clientHeight;
    if(!W)return;cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);S.dpr=dpr;draw()}
  function X(x){return(cv.width/2)+(x-S.vx)*S.sc*S.dpr}
  function Y(y){return(cv.height/2)-(y-S.vy)*S.sc*S.dpr}
  function inv(px,py){return[(px*S.dpr-cv.width/2)/(S.sc*S.dpr)+S.vx,-(py*S.dpr-cv.height/2)/(S.sc*S.dpr)+S.vy]}
  function cs(n){return getComputedStyle(document.documentElement).getPropertyValue(n).trim()}
  function paper(){var b=(D.bg||'#ffffff').toLowerCase();return(b==='#ffffff'||b==='#fff')?'#fbfaf6':b}
  function ink(){var p=paper();var m=/^#([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/.exec(p);if(m){var l=(parseInt(m[1],16)*299+parseInt(m[2],16)*587+parseInt(m[3],16)*114)/1000;return l<110?'255,255,255':'30,35,45'}return'30,35,45'}
  function drawGrid(){
    var d=S.dpr,W=cv.width,H=cv.height,ic=ink(),step=nice(48/(S.sc)),tl=inv(0,0),br=inv(W/d,H/d);
    var x0=Math.floor(tl[0]/step)*step,x1=br[0],y0=Math.floor(br[1]/step)*step,y1=tl[1],i;
    ctx.save();ctx.lineWidth=1*d;ctx.font=(10*d)+'px system-ui,sans-serif';
    if(S.grid){
      ctx.strokeStyle='rgba('+ic+',.10)';ctx.beginPath();
      for(i=x0;i<=x1+step;i+=step){var gx=Math.round(X(i))+.5*d;ctx.moveTo(gx,0);ctx.lineTo(gx,H)}
      for(i=y0;i<=y1+step;i+=step){var gy=Math.round(Y(i))+.5*d;ctx.moveTo(0,gy);ctx.lineTo(W,gy)}
      ctx.stroke();
      // более мелкая сетка по 1, если помещается
      if(S.sc>=14){
        var s1=1;ctx.strokeStyle='rgba('+ic+',.05)';ctx.beginPath();
        for(i=Math.floor(tl[0]);i<=br[0];i+=s1){var hx=Math.round(X(i))+.5*d;ctx.moveTo(hx,0);ctx.lineTo(hx,H)}
        for(i=Math.floor(br[1]);i<=tl[1];i+=s1){var hy=Math.round(Y(i))+.5*d;ctx.moveTo(0,hy);ctx.lineTo(W,hy)}
        ctx.stroke()}}
    // оси
    ctx.strokeStyle='rgba('+ic+',.45)';ctx.fillStyle='rgba('+ic+',.62)';ctx.lineWidth=1.4*d;
    var ox=X(0),oy=Y(0);
    if(ox>=0&&ox<=W){ctx.beginPath();ctx.moveTo(ox,0);ctx.lineTo(ox,H);ctx.stroke()}
    if(oy>=0&&oy<=H){ctx.beginPath();ctx.moveTo(0,oy);ctx.lineTo(W,oy);ctx.stroke()}
    var lx=Math.min(Math.max(oy,12*d),H-4*d);
    ctx.textAlign='center';ctx.textBaseline='top';
    for(i=Math.ceil(x0/step)*step;i<=x1;i+=step){if(Math.abs(i)<step/1e3)continue;var tx=X(i);if(tx>14*d&&tx<W-14*d){var yy=oy>=0&&oy<=H-16*d?oy+3*d:H-14*d;ctx.fillText(fmt(i),tx,yy)}}
    ctx.textAlign='left';ctx.textBaseline='middle';
    for(i=Math.ceil(y0/step)*step;i<=y1;i+=step){if(Math.abs(i)<step/1e3)continue;var ty=Y(i);if(ty>10*d&&ty<H-10*d){var xx=ox>=0&&ox<=W-30*d?ox+4*d:4*d;ctx.fillText(fmt(i),xx,ty)}}
    if(ox>=0&&ox<=W&&oy>=0&&oy<=H){ctx.textAlign='left';ctx.textBaseline='top';ctx.fillText('0',ox+3*d,oy+3*d)}
    ctx.restore()}
  function drawPts(){
    if(!S.pts&&!Object.keys(S.marks).length)return;
    var d=S.dpr,W=cv.width,H=cv.height,tl=inv(0,0),br=inv(W/d,H/d),ic=ink();
    if(S.pts&&S.sc>=7){
      ctx.fillStyle='rgba('+ic+',.28)';
      var xa=Math.ceil(tl[0]),xb=Math.floor(br[0]),ya=Math.ceil(br[1]),yb=Math.floor(tl[1]);
      if((xb-xa+1)*(yb-ya+1)<9000)for(var x=xa;x<=xb;x++)for(var y=ya;y<=yb;y++){ctx.beginPath();ctx.arc(X(x),Y(y),Math.min(2.2,S.sc/7)*d,0,6.3);ctx.fill()}}
    ctx.fillStyle='#2E9E4F';ctx.strokeStyle='#fff';ctx.lineWidth=1.5*d;
    Object.keys(S.marks).forEach(function(k){var p=k.split(',');var cx=X(+p[0]),cy=Y(+p[1]);ctx.beginPath();ctx.arc(cx,cy,Math.max(4,Math.min(7,S.sc/3))*d,0,6.3);ctx.fill();ctx.stroke()})}
  function tri(x,y,h,c,fc){
    var d=S.dpr,a=-h*Math.PI/180,px=X(x),py=Y(y),L=11*d;
    ctx.save();ctx.translate(px,py);ctx.rotate(a);ctx.beginPath();ctx.moveTo(L,0);ctx.lineTo(-L*.7,L*.62);ctx.lineTo(-L*.35,0);ctx.lineTo(-L*.7,-L*.62);ctx.closePath();
    ctx.fillStyle=fc||'#2E9E4F';ctx.globalAlpha=.88;ctx.fill();ctx.globalAlpha=1;ctx.lineWidth=1.4*d;ctx.strokeStyle=c||'#1b5e2f';ctx.stroke();ctx.restore()}
  function drawOps(p){
    var d=S.dpr,end=Math.floor(p),fr=p-end,head=null;
    ctx.lineCap='round';ctx.lineJoin='round';
    for(var i=0;i<N&&i<=end;i++){
      var o=D.ops[i],part=(i===end&&p<N)?fr:1;
      if(o[0]===3){
        if(o[1].length>2){ctx.beginPath();o[1].forEach(function(q,k){k?ctx.lineTo(X(q[0]),Y(q[1])):ctx.moveTo(X(q[0]),Y(q[1]))});ctx.closePath();ctx.fillStyle=o[2];ctx.fill()}}
      else if(o[0]===0){
        var ex=o[1]+(o[3]-o[1])*part,ey=o[2]+(o[4]-o[2])*part;
        if(o[5]){ctx.beginPath();ctx.moveTo(X(o[1]),Y(o[2]));ctx.lineTo(X(ex),Y(ey));ctx.strokeStyle=o[6];ctx.lineWidth=Math.max(1.4,o[7]||1)*d;ctx.stroke()}
        if(i===end||p>=N)head=[ex,ey,Math.atan2(o[4]-o[2],o[3]-o[1])*180/Math.PI]}
      else if(o[0]===1){if(part>0){ctx.beginPath();ctx.arc(X(o[1]),Y(o[2]),Math.max(1.5*d,(o[3]||4)/2*(S.dot||1)*d),0,6.3);ctx.fillStyle=o[4];ctx.fill()}}
      else if(o[0]===2){ctx.fillStyle=o[4];ctx.font=((o[5]||8)*1.4*d)+'px system-ui,sans-serif';ctx.textAlign=o[6]==='center'?'center':o[6]==='right'?'right':'left';ctx.textBaseline='alphabetic';ctx.fillText(o[3],X(o[1]),Y(o[2]))}
      else if(o[0]===4){tri(o[1],o[2],o[3],o[4],o[5])}}
    return head}
  function draw(){
    var W=cv.width,H=cv.height;if(!W)return;
    ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle=paper();ctx.fillRect(0,0,W,H);
    drawGrid();drawPts();
    var head=drawOps(S.p*N);
    if(S.p>=1){D.tur.forEach(function(t){if(t[3])tri(t[0],t[1],t[2],'#1b5e2f','#3bb55f')})}
    else if(head){tri(head[0],head[1],head[2],'#1b5e2f','#3bb55f')}
    if(S.sel){var d=S.dpr,sx=X(S.sel[0]),sy=Y(S.sel[1]);ctx.strokeStyle='#E5484D';ctx.lineWidth=2*d;ctx.beginPath();ctx.arc(sx,sy,6*d,0,6.3);ctx.stroke()}}
  function report(){
    var t=D.tur[0],s='';
    if(t)s='Черепаха остановилась в точке ('+fmt(t[0])+'; '+fmt(t[1])+'), смотрит на '+fmt(t[2])+'° от оси X. ';
    if(D.cut)s+='Рисунок обрезан: слишком много действий. ';
    if(S.sel)s='Точка ('+fmt(S.sel[0])+'; '+fmt(S.sel[1])+'). '+s;
    info.textContent=s||'Черепаха ничего не нарисовала.'}
  function marks(){var n=Object.keys(S.marks).length,b=el.querySelector('#tumark');b.hidden=!(S.mk||n);el.querySelector('#tumn').textContent='Отмечено точек: '+n}
  function play(){
    cancelAnimationFrame(TW.raf);
    if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches||N<2){S.p=1;draw();return}
    var dur=Math.min(6500,Math.max(900,N*45)),t0=null;S.p=0;
    function fr(ts){if(!TW.el)return;if(t0===null)t0=ts;S.p=Math.min(1,(ts-t0)/dur);draw();if(S.p<1)TW.raf=requestAnimationFrame(fr)}
    TW.raf=requestAnimationFrame(fr)}
  function zoom(f,cx,cy){
    var W=cv.clientWidth,H=cv.clientHeight;cx=cx==null?W/2:cx;cy=cy==null?H/2:cy;
    var a=inv(cx,cy);S.sc=Math.min(Math.max(S.sc*f,1e-3),4000);var b=inv(cx,cy);S.vx+=a[0]-b[0];S.vy+=a[1]-b[1];draw()}
  el.querySelector('#tux').onclick=function(){TW.close();try{old&&old.focus&&old.focus()}catch(e){}};
  el.addEventListener('pointerdown',function(e){if(e.target===el){TW.close()}});
  document.addEventListener('keydown',TW.key=function(e){if(e.key==='Escape'&&TW.el){TW.close();e.stopPropagation()}},true);
  el.querySelector('#tuzi').onclick=function(){zoom(1.5)};
  el.querySelector('#tuzo').onclick=function(){zoom(1/1.5)};
  el.querySelector('#tuzf').onclick=function(){fit();draw()};
  el.querySelector('#tupl').onclick=function(){snd('click');play()};
  function tog(id,k,f){var b=el.querySelector(id);b.onclick=function(){S[k]=!S[k];b.classList.toggle('on',S[k]);b.setAttribute('aria-pressed',S[k]);if(f)f();draw()}}
  tog('#tugr','grid');tog('#tupt','pts',function(){if(S.pts&&S.sc<7)info.textContent='Приблизь рисунок (＋), чтобы увидеть целые точки.'});tog('#tumk','mk',marks);
  el.querySelector('#tumc').onclick=function(){S.marks={};marks();draw()};
  cv.addEventListener('wheel',function(e){e.preventDefault();var r=cv.getBoundingClientRect();zoom(e.deltaY<0?1.15:1/1.15,e.clientX-r.left,e.clientY-r.top)},{passive:false});
  var P={},drag=null,pinch=null;
  cv.addEventListener('pointerdown',function(e){try{cv.setPointerCapture(e.pointerId)}catch(x){}P[e.pointerId]=[e.clientX,e.clientY];
    var ks=Object.keys(P);if(ks.length===2){var a=P[ks[0]],b=P[ks[1]];pinch={d:Math.hypot(a[0]-b[0],a[1]-b[1]),sc:S.sc};drag=null}
    else drag={x:e.clientX,y:e.clientY,vx:S.vx,vy:S.vy,mv:0,id:e.pointerId}});
  cv.addEventListener('pointermove',function(e){
    if(!P[e.pointerId])return;P[e.pointerId]=[e.clientX,e.clientY];
    var ks=Object.keys(P);
    if(pinch&&ks.length===2){var a=P[ks[0]],b=P[ks[1]],d=Math.hypot(a[0]-b[0],a[1]-b[1]);if(pinch.d>0){var r=cv.getBoundingClientRect();S.sc=Math.min(Math.max(pinch.sc*d/pinch.d,1e-3),4000);draw()}return}
    if(drag){var dx=e.clientX-drag.x,dy=e.clientY-drag.y;drag.mv=Math.max(drag.mv,Math.hypot(dx,dy));
      if(drag.mv>5){S.vx=drag.vx-dx/S.sc;S.vy=drag.vy+dy/S.sc;draw()}}});
  function up(e){
    var had=P[e.pointerId];delete P[e.pointerId];if(Object.keys(P).length<2)pinch=null;
    if(drag&&drag.id===e.pointerId&&had&&e.type==='pointerup'&&drag.mv<=5){
      var r=cv.getBoundingClientRect(),w=inv(e.clientX-r.left,e.clientY-r.top),sn=[Math.round(w[0]),Math.round(w[1])];
      var near=S.sc>=7&&Math.hypot((w[0]-sn[0])*S.sc,(w[1]-sn[1])*S.sc)<18;
      if(S.mk&&near){var k=sn[0]+','+sn[1];if(S.marks[k])delete S.marks[k];else S.marks[k]=1;S.sel=null;marks();snd('click')}
      else S.sel=near?sn:[Math.round(w[0]*100)/100,Math.round(w[1]*100)/100];
      report();draw()}
    if(drag&&drag.id===e.pointerId)drag=null}
  cv.addEventListener('pointerup',up);cv.addEventListener('pointercancel',up);
  if(window.ResizeObserver)new ResizeObserver(function(){if(!S.dpr||Math.abs(cv.width/(S.dpr||1)-cv.clientWidth)>1){var first=!S.dpr;size();if(first){fit();draw()}}}).observe(cv);
  S.dpr=window.devicePixelRatio||1;
  requestAnimationFrame(function(){size();fit();report();marks();play();el.querySelector('#tux').focus({preventScroll:true})});
  TW.api={S:S,fit:fit,draw:draw,zoom:zoom,play:play};
};
TW.close=function(quiet){
  cancelAnimationFrame(TW.raf);
  if(TW.key){document.removeEventListener('keydown',TW.key,true);TW.key=null}
  if(TW.el){TW.el.remove();TW.el=null;document.body.classList.remove('tuopen')}
  TW.api=null};
/* кнопки «Показать рисунок» в уроках и «🐢 Окно» под выводом */
document.addEventListener('click',function(e){
  var b=e.target.closest&&e.target.closest('[data-tu]');
  if(b){
    e.preventDefault();snd('click');var code=b.getAttribute('data-tu');
    var msg=b.parentNode.querySelector('.tumsg');
    TW.run(code,function(m){if(msg){msg.textContent=m}});
    return}
  var r=e.target.closest&&e.target.closest('#tureopen');
  if(r&&TW.last){TW.open(TW.last)}
});
/* после запуска программы в компиляторе предложить вернуться к окну */
var lr=liveRun;
liveRun=function(code){
  lr(code);
  var chk=setInterval(function(){
    var o=document.getElementById('o');if(!o){clearInterval(chk);return}
    var rs=document.getElementById('rst');
    if(rs&&/Программа (завершена|завершилась)/.test(rs.textContent||'')){
      clearInterval(chk);
      var old=document.getElementById('tureopen');if(old)old.remove();
      if(TW.last&&TW.code===code){var bt=document.createElement('button');bt.className='btn g tureopen';bt.id='tureopen';bt.type='button';bt.textContent='🐢 Показать окно черепахи';o.parentNode.insertBefore(bt,o.nextSibling)}}
  },200);
  setTimeout(function(){clearInterval(chk)},30000)};
window.TW=TW;
})();
