/* ===================== карточка для шеринга v5 ===================== */
function emoLoadImg(g){return new Promise(function(res){var s=emoSrc(g);if(!s)return res(null);var i=new Image();i.onload=function(){res(i)};i.onerror=function(){res(null)};i.src=s})}
function drawCard(cb){
  var CW=1080,CH=1500,cv=document.createElement('canvas');cv.width=CW;cv.height=CH;
  var g=cv.getContext('2d'),cs=getComputedStyle(document.documentElement),V=function(n){return cs.getPropertyValue(n).trim()||'#888'};
  var F='Nunito,system-ui,-apple-system,"Segoe UI",sans-serif',gl=['🥕','⭐','🏆','📚'];
  var earned=ACH.filter(function(a){return S.ach[a.id]});
  Promise.all(gl.map(emoLoadImg).concat(earned.slice(0,8).map(function(a){return emoLoadImg(a.e)}))).then(function(em){
    var src=IMG[rabKey()]||IMG.eat,im=new Image();
    function body(rb){
      g.fillStyle=V('--bg');g.fillRect(0,0,CW,CH);
      g.fillStyle=V('--card');rr(g,50,50,980,1400,56);g.fill();g.lineWidth=3;g.strokeStyle=V('--line');g.stroke();
      g.textBaseline='alphabetic';g.fillStyle=V('--accent');g.font='900 64px '+F;g.textAlign='left';g.fillText('ИТП',110,150);
      g.fillStyle=V('--muted');g.font='700 32px '+F;g.textAlign='right';g.fillText('И так, программирование',970,148);
      if(rb&&rb.width){var bs=380,sc=Math.min(bs/rb.width,bs/rb.height),w=rb.width*sc,h=rb.height*sc,lt=!isDark();
        /* светлая тема: тонкий контур по силуэту и контактная тень под лапами (без круга за кроликом) */
        var bx=540-w/2,by=190+(bs-h)/2;
        if(lt){var cy=by+h-4,gr=g.createRadialGradient(540,cy,2,540,cy,w*.3);gr.addColorStop(0,'rgba(110,70,50,.34)');gr.addColorStop(1,'rgba(110,70,50,0)');
          g.save();g.translate(540,cy);g.scale(1,.2);g.translate(-540,-cy);g.fillStyle=gr;g.beginPath();g.arc(540,cy,w*.3,0,6.283);g.fill();g.restore();
          [[2,0],[-2,0],[0,2],[0,-2]].forEach(function(o){g.save();g.shadowColor=V('--fur-edge');g.shadowBlur=0;g.shadowOffsetX=o[0];g.shadowOffsetY=o[1];g.drawImage(rb,bx,by,w,h);g.restore()})}
        g.drawImage(rb,bx,by,w,h)}
      var nm=String(S.nick);g.font='900 80px '+F;
      if(isRb(nm)){var A=Array.from(nm),ws=A.map(function(ch){return g.measureText(ch).width}),tot=ws.reduce(function(a,b){return a+b},0),x0=540-tot/2;g.textAlign='left';A.forEach(function(ch,k){g.fillStyle='hsl('+(k*47%360)+',85%,58%)';g.fillText(ch,x0,650);x0+=ws[k]})}
      else{g.textAlign='center';g.fillStyle=V('--ink');g.fillText(nm,540,650)}
      var L=lvlInfo(S.xp),lt='Уровень '+L.l;g.font='900 34px '+F;g.textAlign='center';var pw=g.measureText(lt).width+64;
      g.fillStyle=V('--accent');rr(g,540-pw/2,690,pw,60,30);g.fill();g.fillStyle=V('--on');g.fillText(lt,540,732);
      var n=ND(),st=[[0,S.xp,'опыта',1],[1,streakNow(),'дней подряд',0],[2,Math.max(S.max,streakNow()),'рекорд серии',2],[3,n+' из '+NT(),'тем пройдено',3]];
      st=[[1,S.xp,'опыта'],[0,streakNow(),'дней подряд'],[2,Math.max(S.max,streakNow()),'рекорд серии'],[3,n+' из '+NT(),'тем пройдено']];
      st.forEach(function(t,k){var x=100+(k%2)*460,y=790+Math.floor(k/2)*140;g.fillStyle=V('--card2');rr(g,x,y,440,120,32);g.fill();
        var ic=em[t[0]];if(ic)g.drawImage(ic,x+26,y+26,52,52);else{g.font='48px '+F;g.textAlign='left';g.fillStyle=V('--ink');g.fillText(gl[t[0]],x+26,y+66)}
        g.textAlign='left';g.font='900 48px '+F;g.fillStyle=V('--ink');g.fillText(String(t[1]),x+94,y+66);g.font='700 26px '+F;g.fillStyle=V('--muted');g.fillText(t[2],x+28,y+104)});
      g.textAlign='center';g.font='700 26px '+F;g.fillStyle=V('--muted');g.fillText('Активность за последние 13 недель',540,1090);
      var t=new Date();t.setHours(12,0,0,0);var WK=13,s0=new Date(t);s0.setDate(t.getDate()-((t.getDay()+6)%7)-(WK-1)*7);var gx=540-(WK*24-4)/2;
      for(var w2=0;w2<WK;w2++)for(var d=0;d<7;d++){var c=new Date(s0);c.setDate(s0.getDate()+w2*7+d);if(c>t)continue;g.fillStyle=V('--c'+lvC(S.hist[day(c)]));rr(g,gx+w2*24,1106+d*24,20,20,5);g.fill()}
      if(earned.length){g.fillStyle=V('--muted');g.font='700 26px '+F;g.textAlign='center';g.fillText('Достижения: '+earned.length,540,1318);
        var m=Math.min(8,earned.length),x1=540-(m*54-8)/2;
        earned.slice(0,8).forEach(function(a,k){g.fillStyle=a.c;rr(g,x1+k*54,1334,46,50,7);g.fill();g.fillStyle='rgba(255,255,255,.85)';rr(g,x1+k*54+6,1360,34,20,3);g.fill();g.fillStyle='rgba(255,255,255,.55)';rr(g,x1+k*54+10,1334,24,16,3);g.fill();var ei=em[4+k];if(ei)g.drawImage(ei,x1+k*54+14,1362,18,18)})}
      g.fillStyle=V('--muted');g.font='700 26px '+F;g.textAlign='center';g.fillText('Попробуй и ты! ИТП '+ITPV,540,(earned.length?1432:1330));
      cb(cv)}
    if(src){im.onload=function(){body(im)};im.onerror=function(){body(null)};im.src=src}else body(null)})}
