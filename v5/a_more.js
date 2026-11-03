/* ===================== карточка для шеринга v5 ===================== */
/* достижения на карточке: помещается 8, а их куча — ученик сам выбирает, какие показать (владелец). Выбор — в itp-app (shA),
   по порядку выбора; ничего не выбрано — первые 8 полученных */
var SHMAX=8;
function shSel(){var a=appGet().shA;return Array.isArray(a)?a.filter(function(x){return typeof x==='string'}):[]}
function shShown(earned){var p=shSel(),x=p.map(function(id){return earned.filter(function(a){return a.id===id})[0]}).filter(Boolean);return(x.length?x:earned).slice(0,SHMAX)}
function emoLoadImg(g){return new Promise(function(res){var s=emoSrc(g);if(!s)return res(null);var i=new Image();i.onload=function(){res(i)};i.onerror=function(){res(null)};i.src=s})}
function drawCard(cb){
  var CW=1080,CH=1500,cv=document.createElement('canvas');cv.width=CW;cv.height=CH;
  var g=cv.getContext('2d'),cs=getComputedStyle(document.documentElement),V=function(n){return cs.getPropertyValue(n).trim()||'#888'};
  var F='Nunito,system-ui,-apple-system,"Segoe UI",sans-serif',gl=['🥕','⭐','🏆','📚','🐰'];
  var earned=ACH.filter(function(a){return S.ach[a.id]}),shown=shShown(earned);
  Promise.all(gl.map(emoLoadImg).concat(shown.map(function(a){return emoLoadImg(a.e)}))).then(function(em){
    var src=IMG[rabKey()]||IMG.eat,im=new Image();
    function body(rb){
      g.fillStyle=V('--bg');g.fillRect(0,0,CW,CH);
      g.fillStyle=V('--card');rr(g,50,50,980,1400,56);g.fill();g.lineWidth=3;g.strokeStyle=V('--line');g.stroke();
      g.textBaseline='alphabetic';g.fillStyle=V('--accent');g.font='900 64px '+F;g.textAlign='left';g.fillText('ИТП',110,150);
      g.fillStyle=V('--muted');g.font='700 32px '+F;g.textAlign='right';g.fillText('И так, программирование',970,148);
      if(rb&&rb.width){var bs=380,sc=Math.min(bs/rb.width,bs/rb.height),w=rb.width*sc,h=rb.height*sc,lt=!isDark();
        /* светлая тема: контактная тень под лапами (без круга и обводки); спрайт «морковка» сдвинут на 5 %, чтобы тело стояло по центру */
        var eat=rb.src===IMG.eat,bx=540-w/2+(eat?w*.05:0),by=190+(bs-h)/2;
        /* тень ровно под лапами: место лап посчитано по пикселям спрайта (feetOf в a_ui.js) */
        var ft=FEET[rb.src],fr=ft?(ft.r-ft.l)/2*1.15:.3;
        if(lt){var cy=by+h*(ft?ft.y:1)-4,sx=bx+w*(ft?(ft.l+ft.r)/2:(eat?.37:.5)),gr=g.createRadialGradient(sx,cy,2,sx,cy,w*fr);gr.addColorStop(0,'rgba(110,70,50,.34)');gr.addColorStop(1,'rgba(110,70,50,0)');
          g.save();g.translate(sx,cy);g.scale(1,.2);g.translate(-sx,-cy);g.fillStyle=gr;g.beginPath();g.arc(sx,cy,w*fr,0,6.283);g.fill();g.restore()}
        g.drawImage(rb,bx,by,w,h)}
      var nm=nkv(S.nick);g.font='900 80px '+F;
      if(isRb(nm)){var A=Array.from(nm),ws=A.map(function(ch){return g.measureText(ch).width}),tot=ws.reduce(function(a,b){return a+b},0),x0=540-tot/2;g.textAlign='left';A.forEach(function(ch,k){g.fillStyle='hsl('+(k*47%360)+',85%,58%)';g.fillText(ch,x0,650);x0+=ws[k]})}
      else{g.textAlign='center';g.fillStyle=V('--ink');g.fillText(nm,540,650)}
      var L=lvlInfo(S.xp),lt='Уровень '+L.l;g.font='900 34px '+F;g.textAlign='center';var pw=g.measureText(lt).width+64;
      g.fillStyle=V('--accent');rr(g,540-pw/2,690,pw,60,30);g.fill();g.fillStyle=V('--on');g.fillText(lt,540,732);
      var n=ND(),st=[[0,S.xp,'опыта',1],[1,streakNow(),'дней подряд',0],[2,Math.max(S.max,streakNow()),'рекорд серии',2],[3,n+' из '+NT(),'тем пройдено',3]];
      st=[[1,S.xp,'опыта'],[0,streakNow(),'дней подряд'],[2,Math.max(S.max,streakNow()),'рекорд серии'],[3,n+' из '+NT(),'тем пройдено']];
      /* U1-13: пройденные норы — пятой плиткой, только когда пройдена хотя бы одна; тогда плитки в три колонки */
      var hd=typeof HD==='function'?HD():0;if(hd)st.push([4,hd+' из '+HN(),'нор пройдено']);var nc=hd?3:2,tw=hd?286:440,tg=hd?307:460;
      st.forEach(function(t,k){var x=100+(k%nc)*tg+(hd&&k>=3?tg/2:0),y=790+Math.floor(k/nc)*140;g.fillStyle=V('--card2');rr(g,x,y,tw,120,32);g.fill();
        var ic=em[t[0]];if(ic)g.drawImage(ic,x+26,y+26,52,52);else{g.font='48px '+F;g.textAlign='left';g.fillStyle=V('--ink');g.fillText(gl[t[0]],x+26,y+66)}
        g.textAlign='left';g.font=(hd?'900 40px ':'900 48px ')+F;g.fillStyle=V('--ink');g.fillText(String(t[1]),x+94,y+66);g.font='700 26px '+F;g.fillStyle=V('--muted');g.fillText(t[2],x+28,y+104)});
      g.textAlign='center';g.font='700 26px '+F;g.fillStyle=V('--muted');g.fillText('Активность за последние 13 недель',540,1090);
      var t=new Date();t.setHours(12,0,0,0);var WK=13,s0=new Date(t);s0.setDate(t.getDate()-((t.getDay()+6)%7)-(WK-1)*7);var gx=540-(WK*24-4)/2;
      for(var w2=0;w2<WK;w2++)for(var d=0;d<7;d++){var c=new Date(s0);c.setDate(s0.getDate()+w2*7+d);if(c>t)continue;g.fillStyle=V('--c'+lvC(S.hist[day(c)]));rr(g,gx+w2*24,1106+d*24,20,20,5);g.fill()}
      if(earned.length){g.fillStyle=V('--muted');g.font='700 26px '+F;g.textAlign='center';g.fillText('Достижения: '+earned.length,540,1318);
        var m=shown.length,x1=540-(m*54-8)/2;
        shown.forEach(function(a,k){g.fillStyle=a.c;rr(g,x1+k*54,1334,46,50,7);g.fill();g.fillStyle='rgba(255,255,255,.85)';rr(g,x1+k*54+6,1360,34,20,3);g.fill();g.fillStyle='rgba(255,255,255,.55)';rr(g,x1+k*54+10,1334,24,16,3);g.fill();var ei=em[gl.length+k];if(ei)g.drawImage(ei,x1+k*54+14,1362,18,18)})}
      g.fillStyle=V('--muted');g.font='700 26px '+F;g.textAlign='center';g.fillText('Попробуй и ты! ИТП '+ITPV,540,(earned.length?1432:1330));
      cb(cv)}
    if(src){im.onload=function(){body(im)};im.onerror=function(){body(null)};im.src=src}else body(null)})}

/* «Поделиться прогрессом» — то же окно, что раньше, плюс выбор достижений для картинки: значки полученных, нажатием —
   на картинку и обратно (до 8), картинка тут же перерисовывается */
share=function(){
  var tx=shareTxt(),BLOB=null,earned=ACH.filter(function(a){return S.ach[a.id]});
  var btns=[['Скачать картинку',function(){if(!BLOB){toast('Картинка ещё рисуется');return false}saveFile('itp-progress.png',BLOB);toast('Картинка сохранена');return false}]];
  if(navigator.share)btns.push(['Отправить…',function(){if(!BLOB){toast('Картинка ещё рисуется');return false}
    var d={text:tx},f;try{f=new File([BLOB],'itp-progress.png',{type:'image/png'})}catch(e){}if(f&&navigator.canShare&&navigator.canShare({files:[f]}))d.files=[f];
    navigator.share(d).then(function(){ach('share')}).catch(function(){});return false}]);
  btns.push(['Копировать текст',function(){copyTxt(tx);return false},1],['Закрыть',null,1]);
  modal('<h2 style="font-size:20px">Поделиться прогрессом</h2><div id="shw" style="min-height:120px"><p class="mu">Рисую картинку…</p></div>'+
    (earned.length>SHMAX?'<button type="button" class="btn t shpkb" id="shpk" aria-expanded="false" aria-controls="shpl">'+'🏅 Какие достижения показать</button>'+
      '<div class="shpl" id="shpl" hidden><p class="mu shpn" id="shpn"></p><div class="shpg" role="group" aria-label="Достижения на картинке">'+
      earned.map(function(a){return'<button type="button" class="shch" data-id="'+a.id+'" aria-pressed="false" title="'+esc(a.n)+'"><span class="shce" style="--c:'+a.c+'">'+a.e+'</span><span class="shcn">'+esc(a.n)+'</span></button>'}).join('')+'</div></div>':'')+
    '<p class="mu" style="margin:10px 0 0;font-size:14px">'+esc(tx)+'</p>',btns);
  function redraw(){BLOB=null;drawCard(function(cv){var h=$('shw');if(!h)return;h.innerHTML='';
    cv.style.cssText='width:100%;max-height:46vh;object-fit:contain;border-radius:16px;display:block';cv.setAttribute('role','img');cv.setAttribute('aria-label','Картинка с твоим прогрессом');
    h.appendChild(cv);cv.toBlob(function(b){BLOB=b},'image/png')})}
  function marks(){var on=shShown(earned).map(function(a){return a.id});
    [].forEach.call(document.querySelectorAll('.shch'),function(b){var k=on.indexOf(b.dataset.id);b.setAttribute('aria-pressed',k>=0?'true':'false');b.dataset.n=k>=0?k+1:''});
    var n=$('shpn');if(n)n.textContent='На картинке '+on.length+' из '+SHMAX+'. Нажми на достижение, чтобы добавить его или убрать'}
  redraw();
  var pk=$('shpk');if(pk){marks();pk.onclick=function(){var l=$('shpl'),o=l.hidden;l.hidden=!o;pk.setAttribute('aria-expanded',o?'true':'false');snd(o?'open':'close')};
    [].forEach.call(document.querySelectorAll('.shch'),function(b){b.onclick=function(){
      var cur=shShown(earned).map(function(a){return a.id}),id=b.dataset.id,k=cur.indexOf(id);
      if(k>=0){if(cur.length===1){toast('Хотя бы одно достижение');return}cur.splice(k,1)}
      else{if(cur.length>=SHMAX){toast('На картинку помещается '+SHMAX+' — сначала убери какое-нибудь');snd('bad');return}cur.push(id)}
      appSet({shA:cur});snd('tap');marks();redraw()}})}};
