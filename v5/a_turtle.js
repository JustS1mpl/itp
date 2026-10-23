/* v6.5.0: рисунок черепахи. Python (модуль turtle) считает фигуру, здесь она рисуется на холсте прямо в странице:
   в теории (готовый рисунок из сборки, data-td) и под выводом в компиляторе. Окон и лишних кнопок нет, только «заново». */
(function(){
var TW={};
function fmt(v){var r=Math.round(v*100)/100;return String(r).replace('-','−').replace('.',',')}
function bbox(D){var m=0;
  D.ops.forEach(function(o){if(o[0]===3)o[1].forEach(function(p){m=Math.max(m,Math.abs(p[0]),Math.abs(p[1]))});else{m=Math.max(m,Math.abs(o[1]),Math.abs(o[2]));if(o[0]===0)m=Math.max(m,Math.abs(o[3]),Math.abs(o[4]))}});
  D.tur.forEach(function(t){m=Math.max(m,Math.abs(t[0]),Math.abs(t[1]))});return m}
function view(D){
  if(D.w&&D.w.length===4)return{x0:D.w[0],y0:D.w[1],x1:D.w[2],y1:D.w[3]};
  var R=Math.max(200,Math.ceil(bbox(D)*1.12/50)*50);return{x0:-R,y0:-R,x1:R,y1:R}}
function tshape(c,x,y,h,pc,fc,name,u){
  c.save();c.translate(x,y);c.rotate(-h*Math.PI/180);c.lineWidth=1.3*u;c.lineJoin='round';c.strokeStyle=pc;c.fillStyle=fc;
  if(name==='turtle'){
    /* миленькая черепашка: панцирь, 4 лапки, голова с глазом, хвостик */
    var s=u*1.5;c.lineWidth=1.1*u;
    [[1,1,-.8],[1,-1,.8],[-1,1,-2.35],[-1,-1,2.35]].forEach(function(d){
      c.save();c.translate(d[0]*4.3*s,d[1]*4.3*s);c.rotate(d[2]);
      c.beginPath();c.ellipse(0,0,3.3*s,2.1*s,0,0,6.3);c.fill();c.stroke();c.restore()});
    c.beginPath();c.moveTo(-5.6*s,1.6*s);c.quadraticCurveTo(-9.4*s,0,-5.6*s,-1.6*s);c.closePath();c.fill();c.stroke();
    c.beginPath();c.ellipse(7.3*s,0,3.2*s,2.7*s,0,0,6.3);c.fill();c.stroke();
    c.beginPath();c.ellipse(0,0,6.7*s,6*s,0,0,6.3);c.fill();c.stroke();
    c.save();c.strokeStyle='rgba(255,255,255,.62)';c.lineWidth=1.2*u;
    c.beginPath();c.ellipse(0,0,3.2*s,2.8*s,0,0,6.3);c.stroke();
    [0,1.26,2.51,3.77,5.03].forEach(function(an){c.beginPath();c.moveTo(Math.cos(an)*3.2*s,Math.sin(an)*2.8*s);c.lineTo(Math.cos(an)*6.5*s,Math.sin(an)*5.8*s);c.stroke()});c.restore();
    c.beginPath();c.arc(8.3*s,-1.2*s,.62*s,0,6.3);c.fillStyle='#fff';c.fill()}
  else if(name==='circle'){c.beginPath();c.arc(0,0,7.5*u,0,6.3);c.fill();c.stroke()}
  else if(name==='square'){c.beginPath();c.rect(-7*u,-7*u,14*u,14*u);c.fill();c.stroke()}
  else if(name==='triangle'){c.beginPath();c.moveTo(10*u,0);c.lineTo(-7*u,7.5*u);c.lineTo(-7*u,-7.5*u);c.closePath();c.fill();c.stroke()}
  else{var L=1.25*u;c.beginPath();c.moveTo(10*L,0);c.lineTo(-7*L,6.5*L);c.lineTo(-3.5*L,0);c.lineTo(-7*L,-6.5*L);c.closePath();c.fill();c.stroke()}
  c.restore()}
TW.mount=function(host,D,opt){
  opt=opt||{};host.textContent='';
  var cv=document.createElement('canvas');cv.setAttribute('role','img');
  var last=D.tur&&D.tur.filter(function(t){return t[3]})[0]||(D.tur&&D.tur[0]);
  cv.setAttribute('aria-label','Рисунок черепахи, действий: '+D.ops.length+(last?'. Черепаха остановилась в точке ('+fmt(last[0])+'; '+fmt(last[1])+')':''));
  host.appendChild(cv);
  var bt=document.createElement('button');bt.type='button';bt.className='tuplay';bt.setAttribute('aria-label','Нарисовать заново');bt.textContent='↻';host.appendChild(bt);
  var cap=document.createElement('div');cap.className='tucap';
  cap.textContent=last?'Черепаха остановилась в точке ('+fmt(last[0])+'; '+fmt(last[1])+')':'Рисунок готов';
  if(D.cut)cap.textContent+=' · рисунок обрезан: слишком много действий';
  host.appendChild(cap);
  var V=view(D),ctx=cv.getContext('2d'),N=D.ops.length,raf=0,p=1,dpr=1,W=0;
  function X(x){return(x-V.x0)/(V.x1-V.x0)*W}
  function Y(y){return W-(y-V.y0)/(V.y1-V.y0)*W}
  function grid(){
    var span=V.x1-V.x0,st=span<=120?20:span<=300?50:span<=600?100:200,u=dpr;
    ctx.save();ctx.lineWidth=1*u;ctx.font=(10*u)+'px system-ui,sans-serif';ctx.fillStyle='rgba(30,35,45,.5)';ctx.strokeStyle='rgba(30,35,45,.09)';
    var x,y;ctx.beginPath();
    for(x=Math.ceil(V.x0/st)*st;x<=V.x1;x+=st){var gx=Math.round(X(x))+.5*u;ctx.moveTo(gx,0);ctx.lineTo(gx,W)}
    for(y=Math.ceil(V.y0/st)*st;y<=V.y1;y+=st){var gy=Math.round(Y(y))+.5*u;ctx.moveTo(0,gy);ctx.lineTo(W,gy)}
    ctx.stroke();ctx.strokeStyle='rgba(30,35,45,.28)';ctx.beginPath();
    if(V.x0<=0&&V.x1>=0){ctx.moveTo(X(0),0);ctx.lineTo(X(0),W)}if(V.y0<=0&&V.y1>=0){ctx.moveTo(0,Y(0));ctx.lineTo(W,Y(0))}ctx.stroke();
    ctx.textAlign='center';ctx.textBaseline='bottom';
    for(x=Math.ceil(V.x0/st)*st;x<=V.x1;x+=st){if(x===0)continue;var tx=X(x);if(tx>16*u&&tx<W-16*u)ctx.fillText(String(x).replace('-','−'),tx,W-3*u)}
    ctx.textAlign='left';ctx.textBaseline='middle';
    for(y=Math.ceil(V.y0/st)*st;y<=V.y1;y+=st){if(y===0)continue;var ty=Y(y);if(ty>10*u&&ty<W-10*u)ctx.fillText(String(y).replace('-','−'),3*u,ty)}
    ctx.restore()}
  function draw(){
    if(!W)return;ctx.setTransform(1,0,0,1,0,0);
    var bg=(D.bg||'#ffffff');ctx.fillStyle=bg;ctx.fillRect(0,0,W,W);grid();
    var u=dpr,end=Math.floor(p*N),fr=p*N-end,sc=W/(V.x1-V.x0),head=null;
    ctx.lineCap='round';ctx.lineJoin='round';
    for(var i=0;i<N&&i<=end;i++){
      var o=D.ops[i],part=(i===end&&p<1)?fr:1;
      if(o[0]===3){if(o[1].length>2&&(i<end||p>=1)){ctx.beginPath();o[1].forEach(function(q,k){k?ctx.lineTo(X(q[0]),Y(q[1])):ctx.moveTo(X(q[0]),Y(q[1]))});ctx.closePath();ctx.fillStyle=o[2];ctx.fill()}}
      else if(o[0]===0){
        var ex=o[1]+(o[3]-o[1])*part,ey=o[2]+(o[4]-o[2])*part;
        if(o[5]){ctx.beginPath();ctx.moveTo(X(o[1]),Y(o[2]));ctx.lineTo(X(ex),Y(ey));ctx.strokeStyle=o[6];ctx.lineWidth=Math.max(1,(o[7]||1)*sc)*u*(sc>=1?1:1);ctx.stroke()}
        head=[ex,ey,Math.atan2(o[4]-o[2],o[3]-o[1])*180/Math.PI]}
      else if(o[0]===1){ctx.beginPath();ctx.arc(X(o[1]),Y(o[2]),Math.max(1.5,(o[3]||4)/2*sc)*u,0,6.3);ctx.fillStyle=o[4];ctx.fill()}
      else if(o[0]===2){ctx.fillStyle=o[4];ctx.font=((o[5]||8)*1.4*u)+'px system-ui,sans-serif';ctx.textAlign=o[6]==='center'?'center':o[6]==='right'?'right':'left';ctx.textBaseline='alphabetic';ctx.fillText(o[3],X(o[1]),Y(o[2]))}
      else if(o[0]===4){tshape(ctx,X(o[1]),Y(o[2]),o[3],o[4],o[5],'classic',u)}}
    if(p>=1){D.tur.forEach(function(t){if(t[3])tshape(ctx,X(t[0]),Y(t[1]),t[2],t[4],t[5],t[6]||'classic',u)})}
    else if(head){var t0=D.tur.filter(function(t){return t[3]})[0];tshape(ctx,X(head[0]),Y(head[1]),head[2],t0?t0[4]:'#000',t0?t0[5]:'#000',t0?t0[6]||'classic':'classic',u)}}
  function size(){
    var w=host.clientWidth;if(!w||w===W/dpr)return;
    dpr=Math.min(window.devicePixelRatio||1,3);W=Math.round(w*dpr);cv.width=W;cv.height=W;draw()}
  function play(){
    cancelAnimationFrame(raf);
    if(RM()||!N){p=1;draw();return}
    var dur=Math.min(4500,Math.max(760,N*30)),t0=null;p=0;
    function fr(ts){if(!cv.isConnected)return;if(t0===null)t0=ts;p=Math.min(1,(ts-t0)/dur);draw();if(p<1)raf=requestAnimationFrame(fr)}
    raf=requestAnimationFrame(fr)}
  bt.onclick=function(){snd('click');play()};
  if(window.ResizeObserver)new ResizeObserver(function(){if(!cv.isConnected)return;size()}).observe(host);
  requestAnimationFrame(function(){size();if(opt.play)play()});
  return{play:play}};
/* готовые рисунки в теории: <div class="tuf" data-td="json"> */
TW.scan=function(root){
  (root||document).querySelectorAll('.tuf[data-td]').forEach(function(h){
    if(h.dataset.on)return;h.dataset.on='1';var D;try{D=JSON.parse(h.getAttribute('data-td'))}catch(e){return}
    TW.mount(h,D,{play:false})})};
/* рисунок после запуска программы в компиляторе */
var ex0=exec;
exec=function(code,src){
  var live=src&&src.live;
  if(live){var old=document.getElementById('tur');if(old)old.remove()}
  return ex0(code,src).then(function(r){
    if(live&&r&&r.turtle){
      var o=document.getElementById('o');
      if(o&&o.isConnected){var D=null;try{D=JSON.parse(r.turtle)}catch(e){}
        if(D){var h=document.createElement('div');h.className='tuf run';h.id='tur';o.parentNode.insertBefore(h,o.nextSibling);TW.mount(h,D,{play:true})}}}
    return r})};
window.TW=TW;
})();
