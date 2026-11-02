/* ===================== ИТП 6 — интерфейс: оболочка, Путь, Практика, Профиль, Настройки =====================
   Экраны строятся только из данных TOPICS: число тем, число и порядок островков любые,
   новая тема появляется на Пути сама. Ничего о конкретных темах здесь не записано. */
var ITPV='__VER__';

/* --- значки интерфейса: рисуются кодом (SVG), цвет берут из currentColor --- */
var IC={
 path:'<path class="f" d="M3 6.5a3.5 3.5 0 1 0 7 0 3.5 3.5 0 0 0-7 0zM14 17.5a3.5 3.5 0 1 0 7 0 3.5 3.5 0 0 0-7 0z" fill="currentColor" stroke="none"/><circle cx="6.5" cy="6.5" r="2.6"/><circle cx="17.5" cy="17.5" r="2.6"/><path d="M9.1 6.5H15a3 3 0 0 1 0 6H9a3 3 0 0 0 0 6h5.9"/>',
 prac:'<circle class="f" cx="12" cy="12" r="9" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4" fill="currentColor"/>',
 code:'<rect class="f" x="2.5" y="4" width="19" height="16" rx="4" fill="currentColor" stroke="none"/><path d="M8.5 8.5 5 12l3.5 3.5M15.5 8.5 19 12l-3.5 3.5M13.2 6.8l-2.4 10.4"/>',
 bun:'<path class="f" d="M12 21c4 0 7-2.3 7-5.5S16 9.6 12 9.6 5 12.3 5 15.5 8 21 12 21z" fill="currentColor" stroke="none"/><path d="M12 21c4 0 7-2.3 7-5.5S16 9.6 12 9.6 5 12.3 5 15.5 8 21 12 21z"/><path d="M9.6 10C8.3 6.9 7.9 3.4 9.3 3s2.7 3.1 2.9 6.6M14.4 10c1.3-3.1 1.7-6.6.3-7s-2.7 3.1-2.9 6.6"/><circle cx="9.7" cy="15.2" r=".95" fill="currentColor" stroke="none"/><circle cx="14.3" cy="15.2" r=".95" fill="currentColor" stroke="none"/>',
 chev:'<path d="m9 6 6 6-6 6"/>',
 down:'<path d="m6 9 6 6 6-6"/>',
 back:'<path d="M15 5 8 12l7 7"/>',
 x:'<path d="M6 6l12 12M18 6 6 18"/>',
 play:'<path d="M7 5.2v13.6a1 1 0 0 0 1.5.86l11-6.8a1 1 0 0 0 0-1.72l-11-6.8A1 1 0 0 0 7 5.2z" fill="currentColor" stroke="none"/>',
 bulb:'<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.6 10.8c.7.5 1.1 1.3 1.1 2.2h5c0-.9.4-1.7 1.1-2.2A6 6 0 0 0 12 3z"/>',
 more:'<circle cx="5" cy="12" r="1.6" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="1.6" fill="currentColor" stroke="none"/><circle cx="19" cy="12" r="1.6" fill="currentColor" stroke="none"/>',
 file:'<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/>',
 check:'<path d="m5 12.5 4.5 4.5L19 7.5"/>',
 lock:'<rect x="5" y="11" width="14" height="10" rx="2.5"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
 arrow:'<path d="M12 5v14M6 13l6 6 6-6"/>',
 search:'<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
 share:'<path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="m16 6-4-4-4 4"/><path d="M12 2v13"/>',
 gear:'<circle cx="12" cy="12" r="3.2"/><path d="M12 2.8v2.4M12 18.8v2.4M2.8 12h2.4M18.8 12h2.4M5.5 5.5l1.7 1.7M16.8 16.8l1.7 1.7M5.5 18.5l1.7-1.7M16.8 7.2l1.7-1.7"/>'
};
function ico(n,cls){return'<svg class="'+(cls||'')+'" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'+IC[n]+'</svg>'}
/* знак приложения: тот же наклонный шестиугольник-остров, что и на Пути */

/* --- кролик (картинка встроена в файл) --- */
function rabbit(st){var s=IMG[st]||(st==='rolled'?IMG.grump||IMG.grumphead:IMG.eat);return'<div class="rw im '+st+'"><img src="'+s+'" alt="" draggable="false"></div>'}
/* тень под лапами: где стоят лапы, считается по пикселям каждого спрайта (нижние непрозрачные ряды), а не подгоняется
   на глаз — так тень всегда ровно под кроликом, и у нового спрайта тоже. FEET[src] = {l, r, y} в долях картинки */
var FEET={};
function feetOf(src,cb){
  if(FEET[src])return cb&&cb(FEET[src]);
  var im=new Image();im.onload=function(){try{
    var W=Math.min(240,im.naturalWidth),H=Math.round(W*im.naturalHeight/im.naturalWidth),c=document.createElement('canvas');c.width=W;c.height=H;
    var x=c.getContext('2d');x.drawImage(im,0,0,W,H);var d=x.getImageData(0,0,W,H).data,yb=-1,X,Y;
    for(Y=H-1;Y>=0&&yb<0;Y--)for(X=0;X<W;X++)if(d[(Y*W+X)*4+3]>140){yb=Y;break}
    if(yb<0)return;
    var l=W,r=0,band=Math.max(2,Math.round(H*.06));
    for(Y=yb;Y>yb-band&&Y>=0;Y--)for(X=0;X<W;X++)if(d[(Y*W+X)*4+3]>140){if(X<l)l=X;if(X>r)r=X}
    FEET[src]={l:l/W,r:(r+1)/W,y:(yb+1)/H};if(cb)cb(FEET[src])}catch(e){}};im.src=src}
function feetCss(){
  var css='';
  ['eat','happy','grump','rolled','wow','cool'].forEach(function(st){var s=IMG[st]||(st==='rolled'?IMG.grump||IMG.grumphead:null);if(!s)return;
    feetOf(s,function(f){var pad=(f.r-f.l)*.12,L=Math.max(0,f.l-pad),R=Math.max(0,1-f.r-pad);
      css+=':root:not([data-theme=dark]) .rw.im.'+st+'::after{left:'+(L*100).toFixed(1)+'%;right:'+(R*100).toFixed(1)+'%;bottom:'+((1-f.y)*100-4).toFixed(1)+'%}\n';
      var el=document.getElementById('feet');if(!el){el=document.createElement('style');el.id='feet';document.head.appendChild(el)}el.textContent=css})})}
feetCss();
/* окончания по выбранному обращению: m — парень, f — девушка, n — нейтрально (если не указано) */
function G(m,f,n){return S.g==='f'?f:S.g==='m'?m:(n===undefined?m:n)}
function tabFn(){return({home:home,pr:practice,ed:editor,prof:profile})[CURTAB]||home}
var SBACK=null,SKEY='';
/* show() с подсказкой, какой это экран: по ней выбирается направление перехода */
function scr(key,h,tab){SKEY=key;show(h,tab)}

/* --- шапка: «ИТП» слева открывает настройки, справа серия и опыт --- */
function head(){
  var f=S.fz.n,s=streakNow();
  return'<div class="top"><button class="logo" id="ttl" aria-label="ИТП. Открыть настройки">'+'<span class="lgw">ИТП</span>'+'</button><div class="chips"><button class="chip" id="hs" aria-label="Серия: '+s+' '+pl(s,['день','дня','дней'])+(f?', заморозок: '+f:'')+'">🥕 <span>'+s+'</span>'+(f?'<span class="fzm">❄️'+f+'</span>':'')+'</button><button class="chip" id="hx" aria-label="Опыт: '+S.xp+'">⭐ <span>'+S.xp+'</span></button></div></div>'}
function ttl(t,sub){return'<div class="ttl"><div><h1>'+esc(t)+'</h1>'+(sub?'<p class="mu">'+sub+'</p>':'')+'</div></div>'}
function bindHead(re){
  HRE=re;$('hs').onclick=streakSheet;$('hx').onclick=levelSheet;chipFx();
  $('ttl').onclick=function(){SBACK=tabFn();settings()}}
/* тонкая линия под шапкой появляется, когда страницу прокрутили */
(function(){var m=document.createElement('i');m.setAttribute('aria-hidden','true');m.style.cssText='position:absolute;top:0;left:0;width:1px;height:6px;pointer-events:none';document.body.prepend(m);
  if(window.IntersectionObserver)new IntersectionObserver(function(e){document.documentElement.classList.toggle('scr',!e[0].isIntersecting)}).observe(m)})();

/* --- серия, заморозки, уровень --- */
/* U1-12: галочка дня серии — своя, рисуется кодом: толстый скруглённый штрих, без символа ✓ из шрифта */
var WCHK='<svg class="wck" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M5.5 12.8l4.2 4.2L18.6 7.6"/></svg>';
function weekRow(mode){
  var w=wkStart(),t=day(new Date()),nm=['Пн','Вт','Ср','Чт','Пт','Сб','Вс'],h='<div class="wk" role="list" aria-label="Эта неделя">';
  for(var i=0;i<7;i++){
    var d=dadd(w,i),a=S.hist[d]&&S.hist[d].les>0,fz=S.fz.u.indexOf(d)>=0&&!a,g=!!S.gm[d],cl,ic,st;
    if(mode==='g'){cl=g?'on':(d>t?'fu':'');ic=g?WCHK:'';st=g?'цель выполнена':'нет'}
    else{cl=a?'on':fz?'fz':(d>t?'fu':'');ic=a?WCHK:fz?'❄️':'';st=a?'занимался':fz?'заморозка':'нет'}
    h+='<div class="wd '+cl+(d===t?' td':'')+'" role="listitem" aria-label="'+nm[i]+': '+st+'"><span aria-hidden="true">'+nm[i]+'</span><i aria-hidden="true">'+ic+'</i></div>'}
  return h+'</div>'}
function fzLeft(){return 15-S.fz.p}
function streakSheet(){
  var s=streakNow(),f=S.fz,l=fzLeft();
  modal('<div class="ssh"><h2 class="sr-only">Серия</h2><div class="big">🥕 <b>'+s+'</b></div><p class="mu" style="text-align:center;margin:0">'+(s?pl(s,['день','дня','дней'])+' подряд':'Пройди островок сегодня, и серия начнётся')+'</p>'+weekRow('a')+'<div class="fzr"><div class="fzi">'+[0,1].map(function(i){return'<span class="fzs'+(i<f.n?' on':'')+'" aria-hidden="true">❄️</span>'}).join('')+'</div><div class="fzt"><b>Заморозки: '+f.n+' из 2</b><span class="mu">'+(f.n>=2?'Максимум. Заморозка потратится сама, если пропустишь день.':'Новая через '+l+' '+pl(l,['островок','островка','островков'])+'. Тратится сама, если пропустишь день.')+'</span></div></div><p class="mu" style="text-align:center;margin:0">Рекорд серии: '+Math.max(S.max,s)+'</p></div>',[['Понятно']])}
function levelSheet(){
  var L=lvlInfo(S.xp);
  modal('<div class="ssh"><h2 class="sr-only">Опыт и уровень</h2><div class="big">⭐ <b>'+S.xp+'</b></div><p class="mu" style="text-align:center;margin:0">Уровень '+L.l+'</p><div class="bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="'+L.p+'" aria-label="Прогресс уровня"><i class="grow" style="width:'+L.p+'%"></i></div><p class="mu" style="text-align:center;margin:0">До уровня '+(L.l+1)+': ещё '+L.left+' ⭐</p></div>',[['Понятно']])}

/* --- переход «введение → курс» --- */
function reveal(){
  var rm=RM();REV=1;home();REV=0;
  var gc0=app.querySelector('.gcard');if(gc0)gc0.classList.add('rv');
  var intro=app.querySelector('.topic.intro'),rest=[].slice.call(app.querySelectorAll('.topic.rv,.gcard.rv'));
  window.scrollTo(0,0);
  var ov=null,anims=[],tms=[],ended=false;
  function T(f,ms){tms.push(setTimeout(f,ms))}
  function A(el,kf,op){var a=el.animate(kf,op);anims.push(a);return a}
  function end(){
    if(ended)return;ended=true;tms.forEach(clearTimeout);anims.forEach(function(a){try{a.cancel()}catch(e){}});
    if(ov){ov.remove();ov=null}
    if(intro&&intro.parentNode)intro.remove();
    rest.forEach(function(e){e.classList.remove('rv')});
    window.scrollTo(0,0);var c=app.querySelector('.isl.cur');if(c)c.scrollIntoView({block:'center'});
    links();jumpWatch();
  }
  if(!intro||!rest.length){end();return}
  if(rm){
    A(intro,[{opacity:1},{opacity:0}],{duration:400,fill:'forwards'});
    rest.forEach(function(e,k){A(e,[{opacity:0},{opacity:1}],{duration:500,delay:400+k*120,fill:'both'})});
    T(end,1300);return}
  var ib=intro.querySelector('.isl');
  /* центр считаем по раскладке (offset*), а не по getBoundingClientRect: при переходе экрана #app ещё едет (transform), и вспышка стартовала не из центра */
  var lx=0,ly=0,le=ib;while(le){lx+=le.offsetLeft;ly+=le.offsetTop;le=le.offsetParent}
  var cx=lx+ib.offsetWidth/2-window.pageXOffset,cy=ly+ib.offsetHeight/2-window.pageYOffset;
  var rc=getComputedStyle(ib).getPropertyValue('--ti').trim()||'#3D7FEA';
  var cols=[rc,rc,'var(--gold)','var(--carrot)','#fff'];
  ov=document.createElement('div');ov.id='rvfx';ov.style.setProperty('--rc',rc);
  var h='<i class="bl"></i><i class="rn"></i><i class="rn"></i><i class="rn"></i>';
  for(var n=0;n<18;n++)h+='<i class="pt"></i>';
  ov.innerHTML=h;document.body.appendChild(ov);ov.onclick=end;
  [].forEach.call(ov.children,function(e){e.style.left=cx+'px';e.style.top=cy+'px'});
  var X='translate(-50%,-50%) ';
  snd('ach');
  A(ov.querySelector('.bl'),[{opacity:0,transform:X+'scale(.3)'},{opacity:1,transform:X+'scale(1.4)',offset:.3},{opacity:0,transform:X+'scale(4.2)'}],{duration:1500,easing:'cubic-bezier(.2,.7,.2,1)',fill:'both'});
  [].forEach.call(ov.querySelectorAll('.rn'),function(r,k){A(r,[{opacity:.9,transform:X+'scale(.5)'},{opacity:0,transform:X+'scale(3.6)'}],{duration:1200,delay:k*170,easing:'cubic-bezier(.15,.7,.2,1)',fill:'both'})});
  [].forEach.call(ov.querySelectorAll('.pt'),function(p,k){
    var ang=Math.random()*6.283,d=70+Math.random()*120,sz=3+Math.random()*4;
    p.style.width=p.style.height=sz+'px';p.style.color=cols[k%cols.length];
    A(p,[{opacity:0,transform:X+'translate(0,0) scale(.4)'},{opacity:1,transform:X+'translate('+Math.cos(ang)*d*.55+'px,'+Math.sin(ang)*d*.55+'px) scale(1)',offset:.35},{opacity:0,transform:X+'translate('+Math.cos(ang)*d+'px,'+(Math.sin(ang)*d-26)+'px) scale(.2)'}],{duration:900+Math.random()*600,delay:120+k*22,easing:'cubic-bezier(.2,.7,.3,1)',fill:'both'})});
  A(ib,[{transform:'scale(1)',filter:'brightness(1)'},{transform:'scale(1.14)',filter:'brightness(1.18)',offset:.4},{transform:'scale(1)',filter:'brightness(1)'}],{duration:800,easing:'cubic-bezier(.3,1.3,.5,1)'});
  T(function(){A(intro,[{opacity:1,transform:'none',filter:'blur(0)'},{opacity:0,transform:'translateY(-16px) scale(.97)',filter:'blur(6px)'}],{duration:520,easing:'cubic-bezier(.5,0,.8,.5)',fill:'forwards'})},700);
  var k2=0;
  T(function(){
    intro.style.display='none';window.scrollTo(0,0);snd('level');
    rest.forEach(function(e,k){A(e,[{opacity:0,transform:'translateY(30px) scale(.97)',filter:'blur(8px)'},{opacity:1,transform:'none',filter:'blur(0)'}],{duration:800,delay:k*140,easing:'cubic-bezier(.2,.8,.2,1)',fill:'both'})});
    rest.forEach(function(e){[].forEach.call(e.querySelectorAll('.ilw'),function(il){if(k2>14)return;A(il,[{opacity:0,scale:'.55'},{opacity:1,scale:'1.06',offset:.7},{opacity:1,scale:'1'}],{duration:620,delay:520+(k2++)*95,easing:'cubic-bezier(.3,1.1,.5,1)',fill:'both'})})});
  },1230);
  T(end,1230+1500+Math.min(rest.length,4)*140+15*95);
}

/* --- линии между островами: считаются по раскладке (offset*), поэтому анимации их не сдвигают --- */
var LRO=null,LFT=0;
function lkX(el){var m=/translateX\((-?[\d.]+)px\)/.exec(el.style.transform||'');return m?+m[1]:0}
function links(){curOnce(links0)}
function links0(){
  var ns='http://www.w3.org/2000/svg';
  app.querySelectorAll('.path').forEach(function(pa){
    var old=pa.querySelector('.cn');if(old)old.remove();
    var it=pa.querySelectorAll('.ilw'),i=pa.dataset.i;
    if(it.length<2)return;
    var pw=pa.offsetWidth,ph=pa.offsetHeight;pa.dataset.lsz=pw+'x'+ph;
    /* тема с норой: три равных промежутка — край экрана, нора, островок, край; на широком экране промежуток между норой
       и островком не больше 56 px, а пара стоит по центру колонки (на телефоне это одно и то же).
       Отходит от норы только её островок: если двигать и соседей, сбивается зигзаг тропинки; считается до линий */
    var bu=pa.querySelector('.bur');
    if(bu){var aw=bu.parentNode,L=bu.classList.contains('l'),nw=bu.querySelector('.nwr'),g=parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--gut'))||16;
      var vb=nw.offsetWidth*80/92,G=Math.min(56,(pw+2*g-vb-106)/3),x0=(pw-vb-106-G)/2,c0=aw.offsetLeft+aw.offsetWidth/2+(+aw.dataset.b);
      var hd=Math.max(-90,Math.min(90,(L?x0+vb+G+53:pw-x0-vb-G-53)-c0));
      pa.querySelectorAll('.ilw[data-hw]').forEach(function(w){w.style.transform='translateX('+(+w.dataset.b+hd*w.dataset.hw)+'px)'});
      bu.style.right='auto';bu.style.left=(L?x0:pw-x0-vb)-nw.offsetLeft-nw.offsetWidth*6/92-aw.offsetLeft-lkX(aw)+'px'}
    var sv=document.createElementNS(ns,'svg');sv.setAttribute('class','cn');sv.setAttribute('width',pw);sv.setAttribute('height',ph);sv.setAttribute('aria-hidden','true');
    var fresh=[];
    for(var j=0;j<it.length-1;j++){
      var a=it[j],b=it[j+1],bi=b.querySelector('.isl');
      var x1=a.offsetLeft+lkX(a)+a.offsetWidth/2,y1=a.offsetTop+a.offsetHeight+2;
      var x2=b.offsetLeft+lkX(b)+bi.offsetLeft+bi.offsetWidth/2,y2=b.offsetTop+bi.offsetTop+10,ym=(y1+y2)/2;
      var d='M'+x1+' '+y1+' C'+x1+' '+ym+' '+x2+' '+ym+' '+x2+' '+y2,key=i+'-'+j;
      var base=document.createElementNS(ns,'path');base.setAttribute('d',d);base.setAttribute('class','seg');sv.appendChild(base);
      if(S.d[key]&&isOpen(i,j+1)){var lp=document.createElementNS(ns,'path');lp.setAttribute('d',d);var tc=(bi.className.match(/ty-\w/)||[''])[0];lp.setAttribute('class','seg lit '+tc);sv.appendChild(lp);if(!LIT[key]){LIT[key]=1;fresh.push([lp,b])}}
    }
    if(!pa.dataset.lk)pa.dataset.lk=Date.now();
    if(pa.classList.contains('stg')&&!RM()){var el=(Date.now()-pa.dataset.lk)/1000,dl=.2+Math.min(it.length,8)*.045;if(el<dl+.6)sv.style.animation='cnin .6s ease '+(dl-el)+'s both'}
    pa.insertBefore(sv,pa.firstChild);
    /* новый открытый островок: линия дорисовывается, потом остров «всплывает» с волной */
    fresh.forEach(function(f,n){
      var L=f[0].getTotalLength();f[0].style.strokeDasharray=L;f[0].style.strokeDashoffset=L;f[0].getBoundingClientRect();
      f[0].style.transition='stroke-dashoffset .9s cubic-bezier(.4,0,.2,1) '+(n*.9)+'s';f[0].style.strokeDashoffset=0;
      setTimeout(function(){f[1].classList.remove('wait');if(!RM()){var ic=f[1].querySelector('.isl');if(ic)f[1].style.setProperty('--ti',getComputedStyle(ic).getPropertyValue('--ti'));f[1].classList.add('unl');snd('unlock');setTimeout(function(){f[1].classList.remove('unl')},950)}},900*(n+1)+60);
    });
  });
  linksWatch();
}
/* перерисовка, если размер колонки изменился (подгрузился шрифт, перенеслась подпись) */
function linksWatch(){
  if(!LFT&&document.fonts&&document.fonts.ready){LFT=1;document.fonts.ready.then(function(){if(app.querySelector('.path'))links()})}
  if(!window.ResizeObserver)return;
  if(LRO)LRO.disconnect();
  var busy=0;
  LRO=new ResizeObserver(function(){
    if(busy)return;busy=1;
    requestAnimationFrame(function(){busy=0;var ch=false;app.querySelectorAll('.path').forEach(function(p){if(p.dataset.lsz&&p.dataset.lsz!==p.offsetWidth+'x'+p.offsetHeight)ch=true});if(ch)links()})});
  app.querySelectorAll('.path').forEach(function(p){LRO.observe(p)});
}

/* --- островки --- */
/* cur() (текущий островок) обходит весь курс; при отрисовке Пути его зовут для каждого острова,
   поэтому на время отрисовки ответ запоминается один раз */
var CUR1=null;
/* «где я остановился» — сразу за самым дальним пройденным островком на Пути;
   всё, что раньше этой точки и не пройдено, считается пропущенным, но остаётся открытым.
   Доп. главы (кроличьи норы) в расчёте не участвуют: нора — ответвление, флажок на Пути остаётся там, где ученик свернул */
var FRN1=null;
function FRN(){if(FRN1)return FRN1;var li=-1,lj=-1,i,j,r=null;
  for(i=0;i<TOPICS.length;i++)if(!TOPICS[i].opt)for(j=0;j<ni(i);j++)if(S.d[i+'-'+j]){li=i;lj=j}
  if(li<0)r=[Math.max(S.start,0),0];
  else{for(i=li,j=lj+1;i<TOPICS.length&&!r;i++,j=0)if(!TOPICS[i].opt)for(;j<ni(i);j++)if(!S.d[i+'-'+j]){r=[i,j];break}
    if(!r)r=[TOPICS.length,0]}
  if(CUR1!==null)FRN1=r;return r}
function bfr(i,j){var f=FRN();return i<f[0]||(i===f[0]&&j<f[1])}
/* ближайшая теория перед островком в его теме (-1, если её нет): без неё пропущенный островок не открывается */
function thPrev(i,j){for(var x=j-1;x>=0;x--)if(IT(i,x).t==='theory')return x;return -1}
function cur(){if(CUR1!==null)return CUR1;var f=FRN();if(f[0]<TOPICS.length)return f[0]+'-'+f[1];
  for(var i=Math.max(S.start,0);i<TOPICS.length;i++)if(!TOPICS[i].opt)for(var j=0;j<ni(i);j++)if(!S.d[i+'-'+j])return i+'-'+j;return''}
/* доп. главы (opt:1) необязательны: путь идёт мимо них, в счёт тем и завершение обучения они не входят */
/* --- кроличьи норы: доп. глава не стоит в ряду тем, а уходит ответвлением от последнего островка темы перед ней --- */
var HOLE=-1;
function holePar(i){for(var p=i-1;p>=0;p--)if(!TOPICS[p].opt)return p;return-1}
function holesOf(p){var a=[];for(var i=p+1;i<TOPICS.length&&TOPICS[i].opt;i++)a.push(i);return a}
/* внутри норы островки открываются по порядку; «ты здесь» — первый непройденный */
function ocur(i){for(var j=0;j<ni(i);j++)if(!S.d[i+'-'+j])return i+'-'+j;return''}
function ostarted(i){for(var j=0;j<ni(i);j++)if(S.d[i+'-'+j])return true;return false}
/* островок темы, рядом с которым нора и после которого глава открывается: after из данных главы, иначе последний */
function holeAt(i){var p=holePar(i),l=p<0?0:ni(p)-1,a=TOPICS[i].after;return a!=null?Math.min(a,l):l}
/* нора зелёная, когда пройден её островок, тема пропущена при выборе старта или глава уже начата; в режиме разработчика — всегда.
   То, что островок остался позади на карте (bfr), не в счёт: ученик мог уйти вперёд, не пройдя его, и нора зеленела зря */
function holeVis(i){var p=holePar(i),k=holeAt(i);return p<0||TOPICS[p].intro||(typeof DEV==='function'&&DEV())||!!S.d[p+'-'+k]||p<S.start||ostarted(i)}
function holeName(t){return String(t.n||'').split(':')[0]}
/* нора — «вывернутый островок»: тот же шестиугольник и ракурс (точки HEX, viewBox), только утопленный в землю.
   Сверху бортик с низкой боковой гранью, внутри видны три дальние стенки (опущенные на глубину верхние рёбра
   уменьшенного шестиугольника), ниже дно. Рядом, за дальним углом, — наклонённый знак со стрелкой вниз. Цвета — в CSS (--hlt, --hw, --hb, --sgn) */
var NHN=0;
/* знак — с внешней стороны, подальше от тропинки: у норы слева он левее ямы, у норы справа (r) — правее, наклон наружу */
function burrowSvg(r){var id='nh'+(++NHN),I='M18.6 34 L31.9 19.2 L60.1 19.2 L73.4 34 L60.1 48.8 L31.9 48.8 Z';
  return'<svg class="nsv" viewBox="0 8 92 74" aria-hidden="true" focusable="false"><defs><clipPath id="'+id+'"><path d="'+I+'"/></clipPath></defs><g class="npt"><path class="rs" d="M9 34 L27 54 L65 54 L83 34 L83 40 L65 60 L27 60 L9 40 Z"/><path class="rt" d="M9 34 L27 14 L65 14 L83 34 L65 54 L27 54 Z"/><g clip-path="url(#'+id+')"><path class="w" d="'+I+'"/><path class="w wl" d="M18.6 34 L31.9 19.2 L31.9 32.2 L18.6 47 Z"/><path class="w wr" d="M60.1 19.2 L73.4 34 L73.4 47 L60.1 32.2 Z"/><path class="b" d="M18.6 47 L31.9 32.2 L60.1 32.2 L73.4 47 L60.1 61.8 L31.9 61.8 Z"/></g></g><g class="sgw"><g class="sg" transform="'+(r?'translate(44 -5) rotate(9 24 24)':'translate(-16 -5) rotate(-9 24 24)')+'"><ellipse class="sf" cx="24.6" cy="25.2" rx="5" ry="2.7"/><rect class="sp" x="22.3" y="4" width="2.7" height="21.4" rx="1"/><rect class="sps" x="24.6" y="4" width="1.7" height="21.4" rx=".8"/><path class="sbk" d="M8 -6 L16 8 L32 8 L40 -6 L40 -2.5 L32 11.5 L16 11.5 L8 -2.5 Z"/><path class="sb" d="M8 -6 L16 -20 L32 -20 L40 -6 L32 8 L16 8 Z"/><path class="sa" d="M24 -13v12M18.5 -6.5l5.5 5.5 5.5-5.5"/></g></g></svg>'}
/* в нору можно зайти всегда; бледная (lk), пока не пройден её островок темы, потом зелёная */
/* норы, которые уже видели открытыми: только что открывшаяся нора один раз зеленеет и знак подпрыгивает */
var HOP=null;
function burrow(o,side){
  var t=TOPICS[o],m=ni(o),c=0,op=holeVis(o),fr=op&&!HOP[o];for(var j=0;j<m;j++)if(S.d[o+'-'+j])c++;
  if(op)HOP[o]=1;if(fr&&!RM())setTimeout(function(){snd('unlock')},1500);
  var dn=c===m,st=dn?'пройдена':c?c+' из '+m:'';
  return'<button class="bur '+side+(op?'':' lk')+(dn?' dn':'')+(fr&&!RM()?' fr':'')+'" data-o="'+o+'" aria-label="'+esc('Доп. глава: '+t.n+' ('+st+')')+'"><span class="nwr">'+burrowSvg(side.charAt(0)==='r')+(dn?'<i class="bd ok"></i>':'')+'</span><span class="ntx">'+esc(holeName(t))+(st?'<small>'+st+'</small>':'')+'</span></button>'}
function hole(i){HOLE=i;curOnce(function(){hole0(i)})}
function hole0(i){BACK=home;fzApply();
  var t=TOPICS[i],p=holePar(i),n=ni(i),c=0;for(var j=0;j<n;j++)if(S.d[i+'-'+j])c++;
  var h='<div class="top ls"><button class="icon" id="x" aria-label="Назад на Путь">'+ico('back')+'</button><h1>'+esc(holeName(t))+'</h1></div>'+
   '<section class="topic hole" aria-label="'+esc('Доп. глава: '+t.n)+'"><div class="hhd'+(c===n?' dn':'')+'"><span class="nwr">'+burrowSvg()+'</span><h2>'+esc(t.n)+'</h2><p class="mu">'+esc(t.s||'')+'</p><p class="hnt">Доп. глава по желанию: открыта всегда, заходи, когда интересно. В счёт тем не входит, опыт за островки начисляется как обычно.</p><div class="hpr"><div class="ring" style="--p:'+Math.round(c/Math.max(1,n)*100)+'" role="img" aria-label="Пройдено '+c+' из '+n+'"><span>'+c+'/'+n+'</span></div><span>'+(c===n?'Глава пройдена':c?'Пройдено '+c+' из '+n:'Ещё не начата')+'</span></div></div>'+
   '<div class="path'+(RM()?'':' stg')+'" data-i="'+i+'">';
  for(var j2=0;j2<n;j2++)h+=island(i,j2,j2);
  scr('hole',h+'</div></section>','home');links();
  $('x').onclick=function(){HOLE=-1;home();var b=app.querySelector('.bur[data-o="'+i+'"]');if(b)b.scrollIntoView({block:'center'})};
  app.querySelectorAll('.isl').forEach(function(b){b.onclick=function(e){e.stopPropagation();islandPop(b)}});
  var cu=app.querySelector('.isl.cur');if(cu&&c)cu.scrollIntoView({block:'center'});else window.scrollTo(0,0);
}
function allDone(){return TOPICS.every(function(t,i){return t.intro||t.opt||tdone(i)})}
function NT(){return TOPICS.filter(function(t){return!t.intro&&!t.opt}).length}
function ND(){return TOPICS.filter(function(t,i){return!t.intro&&!t.opt&&(tdone(i)||i<S.start)}).length}
function curOnce(f){var o=CUR1,of=FRN1;CUR1=null;FRN1=null;CUR1=cur();try{return f()}finally{CUR1=o;FRN1=of}}
/* объёмный наклонный шестиугольник: верх, бок, блик, свечение; тень на воде и галочка рисуются в CSS (меньше узлов на длинном Пути) */
var HEX='<svg class="hx" viewBox="0 8 92 74" width="118" height="92" aria-hidden="true" focusable="false"><path class="gl" d="M9 34 L27 14 L65 14 L83 34 L83 46 L65 66 L27 66 L9 46 Z"/><path class="sd" d="M9 34 L27 54 L65 54 L83 34 L83 46 L65 66 L27 66 L9 46 Z"/><path d="M9 34 L27 14 L65 14 L83 34 L65 54 L27 54 Z"/><path class="sh" d="M13 33 L29 17 L63 17 L57 23 L31 23 L19 33 Z"/></svg>';
var ITY={theory:['t','📖','Теория'],flash:['f','✏️','Вопросы'],test:['c','💻','Код'],project:['p','🚀','Мини-проект']};
function ity(it){return ITY[it.t]||['a','⭐','Островок']}
function island(i,j,n,dx){
  var o=TOPICS[i].opt,k=i+'-'+j,it=IT(i,j),d=S.d[k],op=isOpen(i,j),c=(o?ocur(i):cur())===k,nx=!c&&!d&&!o&&nxI(i,j),wt=j>0&&S.d[i+'-'+(j-1)]&&!LIT[i+'-'+(j-1)];
  var ty=ity(it),lb=it.n||'',off=[0,46,0,-46][j%4]+(dx||0),st=d?'пройдено':(op?(c?'ты здесь':'открыто'):'закрыто');
  return'<div class="ilw'+(wt?' wait':'')+(c?' cu':'')+'" style="--n:'+Math.min(n||0,9)+';transform:translateX('+off+'px)">'+(c?'<div class="flag" aria-hidden="true">'+(TOPICS[i].intro||o&&!ostarted(i)?'Начни здесь':'🚩 Ты остановился здесь')+'</div>':'')+'<button class="isl ty-'+ty[0]+' '+(d?'dn':(op?'op':'lk'))+(c?' cur':'')+(nx?' nx':'')+'" data-i="'+i+'" data-j="'+j+'" aria-label="'+esc(ty[2]+': '+lb+' ('+st+')')+'"'+(c?' aria-current="step"':'')+'>'+HEX+'<span class="ic">'+ty[1]+'</span>'+(d?'<i class="bd ok"></i>':(op?'':'<i class="bd">🔒</i>'))+'</button><div class="mu">'+esc(lb)+(it.t==='project'?'<br><small>'+(/^(skip|seen)$/.test(S.at[k])?'пропущен':'по желанию')+'</small>':'')+'</div></div>'}
/* сколько читать теорию: по объёму текста, примерно 160 слов в минуту */
function readMin(it){var t=String(it.html||'').replace(/<pre[\s\S]*?<\/pre>/g,' ').replace(/<[^>]+>/g,' '),w=t.split(/\s+/).filter(Boolean).length,c=(String(it.html||'').match(/<pre>/g)||[]).length;return Math.max(1,Math.round(w/160+c*.25))}
function goalCard(all){
  var d=goalDone(),g=S.goal,ok=d>=g,cu=cur(),nx=null;
  if(cu){var p=cu.split('-');nx=IT(+p[0],+p[1])}
  /* сверху приветствие во всю ширину (ник до 20 символов помещается целиком); в центре крупно — что дальше;
     кнопка во всю ширину; под ней тихая строка цели с маленьким кольцом */
  var ty=nx?ity(nx):null,mt=ty?ty[2]+(nx.t==='theory'?' · ≈ '+readMin(nx)+' мин':''):'';
  return'<section class="gcard" aria-label="Сегодня"><div class="gh">Привет, <b>'+nk(S.nick)+'</b>!</div>'+
   (all?'<p class="gall">Курс пройден. Кролик гордится тобой.</p>':cu?'<div class="gnx ty-'+ty[0]+'"><span class="gic" aria-hidden="true">'+ty[1]+'</span><span class="gnt"><small>'+esc(mt)+'</small><b>'+esc(nx.n||'')+'</b></span></div><button class="btn" id="gc">'+(d?'Продолжить':'Начать')+'</button>':'')+
   '<div class="gg'+(ok?' ok':'')+'"><span class="ring" role="img" aria-label="Цель дня: '+d+' из '+g+'"><svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="8"/><circle class="v" cx="10" cy="10" r="8" pathLength="100"'+(ok?'':' stroke-dasharray="'+Math.round(d/g*100)+' 100"')+'/></svg></span>'+(ok?'Цель дня выполнена':'Цель дня: '+d+' из '+g)+'</div></section>'}
function home(){if(HOLE>=0&&TOPICS[HOLE]&&TOPICS[HOLE].opt)return hole(HOLE);HOLE=-1;curOnce(home0)}
function home0(){BACK=home;fzApply();
  var all=allDone();
  if(PE.length){scr('home',head()+'<div class="fb bad"><b>Ошибка в данных тем</b>'+PE.map(esc).join('<br>')+'</div>','home');bindHead(home);return}
  var first=TOPICS[0]&&TOPICS[0].intro&&S.start===0&&!tdone(0)&&!REV;
  var h=head()+'<h1 class="sr-only">Путь</h1>'+(first?'':goalCard(all)),num=0,cu=cur(),ci=cu?+cu.split('-')[0]:-1;
  TOPICS.forEach(function(t,i){
    if(t.opt)return;if(!t.intro)num++;if(!vis(i))return;
    var c=0;(t.items||[]).forEach(function(x,j){if(S.d[i+'-'+j])c++});
    var pc=Math.round(c/Math.max(1,ni(i))*100),dn=tdone(i);
    h+='<section class="topic'+(t.intro?' intro':'')+(REV&&!t.intro?' rv':'')+'" aria-label="'+esc(t.intro?t.n:'Тема '+num+': '+t.n)+'">'+(t.intro?'<div class="ihead"><h2>'+esc(t.n)+'</h2><p class="mu">'+esc(t.s||'')+'</p></div>':'<div class="thead'+(dn?' done':'')+(i===ci?' now':'')+'"><div class="tn'+(dn?' ok':'')+'" aria-hidden="true">'+(dn?'':num)+'</div><div class="tt"><h2>'+esc(t.n)+'</h2><div class="mu">'+esc(t.s||'')+((i<S.start||i<FRN()[0])&&!dn?' · пропущено':'')+'</div></div><div class="ring" style="--p:'+pc+'" role="img" aria-label="Пройдено '+c+' из '+ni(i)+'"><span>'+c+'/'+ni(i)+'</span></div></div>')+'<div class="path'+(RM()?'':' stg')+'" data-i="'+i+'">';
    /* нора — примерно за пять островков до конца темы, у островка, сдвинутого вбок (нечётный), в свободном месте с другой стороны */
    if(!HOP){HOP={};TOPICS.forEach(function(x,o){if(x.opt&&holeVis(o))HOP[o]=1})}
    /* островок посередине тропинки (чётный) места сбоку не оставляет — тогда нора у следующего, сдвинутого вбок; открывается всё равно после своего */
    var hs=holesOf(i),l=ni(i)-1,an=hs.length?holeAt(hs[0]):-1;if(an>=0&&an%2===0&&an<l)an++;
    /* островок с норой отходит от неё (точный сдвиг считает links0; здесь — начальный, чтобы не прыгало) */
    var hd=hs.length?(an%4===1?1:-1)*34:0;
    for(var j=0;j<ni(i);j++){var dj=Math.abs(j-an),hw=hs.length&&!dj?1:0,w=island(i,j,j,hd*hw);
      if(hw)w=w.replace('<div class="ilw','<div data-b="'+[0,46,0,-46][j%4]+'" data-hw="'+hw+'" class="ilw');
      if(j===an&&hs.length)w=w.replace('class="ilw','class="ilw nhb').replace(/<\/div>$/,burrow(hs[0],an%4===1?'l':'r')+'</div>');
      h+=w}
    h+='</div></section>'});
  scr('home',h+'<aside class="jump" aria-label="Быстрый переход"><button id="jmp" aria-label="К текущему островку">'+ico('arrow')+'</button></aside>','home');bindHead(home);links();
  app.querySelectorAll('.isl').forEach(function(b){b.onclick=function(e){e.stopPropagation();islandPop(b)}});
  app.querySelectorAll('.bur').forEach(function(b){b.onclick=function(e){e.stopPropagation();popClose();hole(+b.dataset.o)}});
  var c=app.querySelector('.isl.cur');if(c&&!REV)c.scrollIntoView({block:'center'});
  var gc=$('gc');if(gc)gc.onclick=function(){var k=cur();if(!k)return;var p=k.split('-');BACK=home;go(+p[0],+p[1])};
  jumpWatch();
}
function toCur(){var t=app.querySelector('.isl.cur')||app.querySelector('.isl.nx');if(t)t.scrollIntoView({block:'center',behavior:RM()?'auto':'smooth'})}
/* кнопка «к текущему»: видна, только когда текущий островок ушёл за экран, стрелка показывает направление */
var JIO=null;
function jumpWatch(){
  if(JIO){JIO.disconnect();JIO=null}
  var j=$('jmp'),t=app.querySelector('.isl.cur')||app.querySelector('.isl.nx');
  if(!j)return;if(!t||!window.IntersectionObserver){j.remove();return}
  j.onclick=toCur;
  JIO=new IntersectionObserver(function(es){es.forEach(function(e){var off=!e.isIntersecting;j.classList.toggle('on',off);j.classList.toggle('up',off&&e.boundingClientRect.top<0);j.setAttribute('aria-hidden',off?'false':'true');j.tabIndex=off?0:-1})},{rootMargin:'-60px 0px -90px 0px'});
  JIO.observe(t);
}
/* карточка островка: что это, сколько займёт, сколько опыта, одна кнопка */
function popClose(){var o=app.querySelector('.ipop');if(!o)return;app.classList.remove('pk');var b=app.querySelector('.isl.sel');if(b)b.classList.remove('sel');document.removeEventListener('click',popOut,true);if(RM()){o.remove();return}o.classList.add('out');setTimeout(function(){o.remove()},180)}
function popOut(e){if(!e.target.closest('.ipop')&&!e.target.closest('.isl'))popClose()}
function islandPop(b){
  var i=+b.dataset.i,j=+b.dataset.j,was=b.classList.contains('sel');
  var o0=app.querySelector('.ipop');if(o0){o0.remove();app.classList.remove('pk');var s0=app.querySelector('.isl.sel');if(s0)s0.classList.remove('sel');document.removeEventListener('click',popOut,true)}
  if(was)return;
  var it=IT(i,j),k=i+'-'+j,ty=ity(it),d=S.d[k],op=isOpen(i,j),meta='',txt='',btn='',sk='';
  if(it.t==='theory')meta='≈ '+readMin(it)+' мин';
  else if(it.t==='flash')meta=it.q.length+' '+pl(it.q.length,['вопрос','вопроса','вопросов']);
  else if(it.t==='test')meta=it.tasks.length+' '+pl(it.tasks.length,['задание','задания','заданий']);
  else if(it.t==='project')meta='по желанию';
  var xp=it.t==='flash'?20:it.t==='test'?60:it.t==='project'?(it.bonus>0?it.bonus|0:40):0;
  var tp=!op&&!TOPICS[i].opt&&(i<S.start||bfr(i,j))?thPrev(i,j):-1;
  if(tp>=0){snd('lock');txt='Сначала прочитай теорию «'+esc(IT(i,tp).n||'')+'»: этот островок по ней.';btn='<button class="btn" id="ipt">Читать теорию</button>'}
  else if(!op){snd('lock');txt='Откроется, когда пройдёшь островки перед ним.';btn='<button class="btn g" id="ipc">К текущему островку</button>'}
  else if(d){
    txt=S.at[k]==='seen'?'Проект пропущен, эталон открыт. Решить можно, но уже без опыта.':S.at[k]==='skip'?'Этот проект пропущен. Сделай его сейчас и получи +'+xp+' ⭐.':(xp?'Пройдено. Опыт за этот островок уже получен, повторять можно сколько угодно.':'Пройдено. Можно перечитать в любой момент.');
    btn='<button class="btn" id="ipg">'+(/^(skip|seen)$/.test(S.at[k])?'Сделать проект':it.t==='theory'?'Перечитать':'Повторить')+'</button>'}
  else{
    txt=it.t==='theory'?'Прочитай и нажми «'+G('Я прочитал','Я прочитала','Прочитано')+'» в конце. Выделенные слова открывают описание.':it.t==='flash'?'Выбирай верный ответ. Ошибки вернутся в конце островка.':it.t==='test'?'Пиши программы, проверка запустит их на тестах.':'Задача покрупнее. Можно пропустить, тема всё равно засчитается.';
    if(xp)txt+=' Награда: до +'+xp+' ⭐.';
    btn='<button class="btn" id="ipg">'+(it.t==='project'?'Начать проект':'Начать')+'</button>';
    if(it.t==='project')sk='<button class="btn t" id="ips">Пропустить</button>'}
  var pa=b.closest('.path'),w=b.closest('.ilw'),br=b.getBoundingClientRect();
  var o=document.createElement('div');o.className='ipop ty-'+ty[0];o.setAttribute('role','dialog');o.setAttribute('aria-label',ty[2]+': '+(it.n||''));
  o.innerHTML='<div class="ipk"><span class="tg"><i></i>'+ty[2]+'</span><span class="mu">'+(d?'✓ пройдено':meta)+'</span></div><h3>'+esc(it.n||ty[2])+'</h3><p>'+txt+'</p><div class="row">'+btn+sk+'</div>';
  o.style.top=(w.offsetTop+w.offsetHeight+10)+'px';
  pa.appendChild(o);b.classList.add('sel');app.classList.add('pk');
  /* стрелка карточки смотрит точно на остров, даже если карточка уже ширины дорожки */
  /* считаем по раскладке, а не по getBoundingClientRect: карточка в момент замера ещё «въезжает» (scale/translate) и стрелка съезжала */
  var ix=w.offsetLeft+lkX(w)+b.offsetLeft+b.offsetWidth/2;
  o.style.setProperty('--ax',Math.max(24,Math.min(o.offsetWidth-24,ix-o.offsetLeft))+'px');
  var g=$('ipg');if(g)g.onclick=function(){BACK=home;popClose();go(i,j)};
  var s=$('ips');if(s)s.onclick=function(){popClose();projSkip(i,j)};
  var cc=$('ipc');if(cc)cc.onclick=function(){popClose();toCur()};
  var tt=$('ipt');if(tt)tt.onclick=function(){BACK=home;popClose();go(i,tp)};
  setTimeout(function(){document.addEventListener('click',popOut,true)},0);
  /* карточку должно быть видно целиком; пока она «въезжает» (scale), она ниже настоящей — после анимации докручиваем */
  function vis(){if(o.isConnected)o.scrollIntoView({block:'nearest',behavior:RM()?'auto':'smooth'})}
  requestAnimationFrame(function(){vis();var fb=g||cc||tt;if(fb)fb.focus({preventScroll:true})});o.addEventListener('animationend',vis,{once:true});
}
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&app.querySelector('.ipop')&&!document.querySelector('.modal')){e.stopImmediatePropagation();e.preventDefault();var b=app.querySelector('.isl.sel');popClose();if(b)b.focus()}},true);

/* --- приветствие и повторение после перерыва --- */
function greet(){
  var t=day(new Date());fzApply();
  if(S.seen===t)return home();
  var away=S.seen?dnum(t)-dnum(S.seen):0;S.seen=t;save();
  var s=streakNow(),lost=S.streak>=2&&s===0;
  scr('greet','<div class="onb center gr">'+rabbit('eat')+'<h1>Привет, '+nk(S.nick)+'!</h1><p class="lead">'+(lost?'Серия в '+S.streak+' '+pl(S.streak,['день','дня','дней'])+' прервалась'+(away>=3?', тебя не было '+away+' '+pl(away,['день','дня','дней']):'')+'. Не страшно: новая начнётся сегодня.':away>=3?'Тебя не было '+away+' '+pl(away,['день','дня','дней'])+'. Кролик скучал.':s?'Серия: '+s+' '+pl(s,['день','дня','дней'])+'. Не прерывай её сегодня.':'Кролик завтракает и ждёт тебя.')+'</p><button class="btn pulse" id="go">Начать</button></div>');
  $('go').onclick=function(){home();if(away>=3)setTimeout(function(){repeatAsk(away)},400)};
}
function passed(type){var a=[];TOPICS.forEach(function(t,i){(t.items||[]).forEach(function(x,j){if(x.t===type&&S.d[i+'-'+j])a.push([i,j])})});return a}
function repeatAsk(away){
  if(!ST('rep')||S.rp===day(new Date())||!passed('flash').length)return;
  modal('<h2>Давно не виделись</h2><p>Тебя не было '+away+' '+pl(away,['день','дня','дней'])+'. Повторим 3 вопроса из пройденного?</p><p class="mu">Это разминка: опыт за неё не начисляется.</p>',[['Давай',function(){S.rp=day(new Date());save();repeat3()}],['Позже',function(){S.rp=day(new Date());save()},1]])}

/* --- практика --- */
function row(ic,t,sub,a,dis,rt){return'<button class="li" data-a="'+a+'"'+(dis?' disabled':'')+'><span class="lic" aria-hidden="true">'+ic+'</span><span class="lt">'+t+(sub?'<small>'+sub+'</small>':'')+'</span>'+(rt?'<span class="lv">'+rt+'</span>':ico('chev','ch'))+'</button>'}
/* кубики-украшение: только контур, вектор (иконка dices из набора Lucide, лицензия ISC) */
var DICE='<svg class="pdeco" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect width="12" height="12" x="2" y="10" rx="2" ry="2"/><path d="m17.92 14 3.5-3.5a2.24 2.24 0 0 0 0-3l-5-4.92a2.24 2.24 0 0 0-3 0L10 6"/><path class="dpp" d="M6 18h.01M10 14h.01M15 6h.01M18 9h.01"/></svg>';
function practice(){BACK=practice;PRW=0;
  var nf=passed('flash').length,nt=passed('test').length;
  /* главный режим — крупная карточка с кубиками вместо значка; два других — тихие строки под ней */
  function pc(a,ic,t,s,dis,big,lab){return'<button class="pcard'+(big?' big':'')+'" data-a="'+a+'"'+(dis?' disabled aria-disabled="true"':'')+'>'+(big?DICE:'<span class="pic" aria-hidden="true">'+ic+'</span>')+'<b>'+t+'</b><small>'+s+'</small><span class="go">'+(dis?ico('lock')+'Сначала пройди островок':lab+ico('chev'))+'</span></button>'}
  scr('practice',head()+ttl('Практика','Без опыта: прогресс и серия не меняются')+'<div class="prc">'+
   pc('rf','🎲','Случайный вопрос','Вопросы из пройденных островков, пока не закроешь',!nf,1,'Начать')+
   '<div class="prl">'+pc('rc','💻','Случайный код','Задание из пройденных',!nt,0,'Решить')+
   pc('r3','🔁','Разминка','3 вопроса по пройденному',!nf,0,'Начать')+'</div></div>'+
   (S.cn.rc?'<p class="pnote">Верных ответов в тренировках: <b>'+S.cn.rc+'</b></p>':''),'pr');
  bindHead(practice);
  app.querySelectorAll('.pcard').forEach(function(b){b.onclick=function(){if(b.disabled)return;({rf:rndFlash,rc:rndCode,r3:repeat3})[b.dataset.a]()}})}
function oge(){practice()}
/* вопрос в тренировке: та же раскладка, что у островка с вопросами */
function askQ(q,o){
  var sel=-1,ch=false,right=false,ord=q.o.map(function(x,n){return n}).sort(function(){return Math.random()-.5});
  var h='<div class="top ls"><button class="icon" id="x" aria-label="Выйти">'+ico('x')+'</button><div class="grow">'+o.mid+'</div></div><h1 class="sr-only">Тренировка</h1><h2 class="q">'+(typeof qfmt==='function'?qfmt(q.q):esc(q.q))+'</h2>'+(q.v||'')+(q.c?'<pre>'+hl(q.c)+'</pre>':'')+optsHtml(q,ord);
  scr('askq',h+dockHtml('<button class="btn" id="go" disabled>Проверить</button>',0,1));if(q.v)imgZoom(app);
  $('x').onclick=o.exit;
  var g=$('go'),os=app.querySelectorAll('.opt');
  optKeys(os,function(b){if(ch)return;sel=+b.dataset.k;os.forEach(function(x){x.classList.remove('sel');x.setAttribute('aria-pressed','false')});b.classList.add('sel');b.setAttribute('aria-pressed','true');g.disabled=false});
  g.onclick=function(){
    if(ch){o.next();return}
    ch=true;right=sel===q.a;fx(right);
    os.forEach(function(x){var k=+x.dataset.k;x.disabled=true;if(k===q.a)x.classList.add('ok');else if(k===sel)x.classList.add('no')});
    if(right)PRW=0;else PRW++;
    dockState(right,right?'Верно!':'Неверно',esc(q.e||'')+xm(q),right?'':errMood(PRW));
    g.textContent=o.last&&o.last()?'Закончить':'Дальше';o.done(right);g.focus()}}
var RND={r:0,t:0,last:null};
function rndWarn(go){if(S.rnd)return go();modal('<h2>Бесконечный режим</h2><p>Задания идут одно за другим, пока не закроешь режим крестиком. Опыт не начисляется, прогресс не меняется.</p>',[['Понятно',function(){S.rnd=1;save();go()}],['Отмена',null,1]])}
function allFlashQ(){var a=[];passed('flash').forEach(function(p){IT(p[0],p[1]).q.forEach(function(q,n){a.push({q:q,k:p[0]+'-'+p[1]+'-'+n})})});return a}
function rndFlash(){
  if(!passed('flash').length){toast('Сначала пройди хотя бы один островок с вопросами');return}
  rndWarn(function(){RND.r=0;RND.t=0;RND.last=null;rfNext()})}
function rfNext(){
  var P=allFlashQ();if(!P.length){practice();return}
  var x;do{x=P[Math.floor(Math.random()*P.length)]}while(P.length>1&&x.k===RND.last);RND.last=x.k;
  askQ(x.q,{mid:'<span class="lstep">🎲 Верно '+RND.r+' из '+RND.t+'</span>',exit:practice,next:rfNext,done:function(r){RND.t++;if(r){RND.r++;rcInc()}}})}
function repeat3(){
  var P=allFlashQ();if(!P.length){toast('Сначала пройди хотя бы один островок с вопросами');return}
  P.sort(function(){return Math.random()-.5});var Q=P.slice(0,3),st=Q.map(function(){return 0}),n=0,ok=0;
  function bar(){return'<div class="sbar" role="img" aria-label="Вопрос '+(n+1)+' из '+Q.length+'">'+st.map(function(v,k){return'<i class="'+(v===1?'ok':v===2?'bad':k===n?'cu':'')+'"></i>'}).join('')+'</div>'}
  function step(){
    if(n>=Q.length){
      var all=ok===Q.length;
      scr('done','<div class="fin">'+(all?rabbit('happy'):'')+'<h1>Повторено: '+ok+' из '+Q.length+'</h1><p class="lead">'+(all?'Всё помнишь. Отлично.':'Ничего страшного, это просто разминка.')+'</p></div>'+dockHtml('<button class="btn" id="go">Готово</button><button class="btn t" id="rp">Ещё раз</button>',1));
      $('go').onclick=home;$('rp').onclick=repeat3;if(all){snd('solve');ach('rep1')}return}
    askQ(Q[n].q,{mid:bar(),exit:home,last:function(){return n===Q.length-1},next:function(){n++;step()},done:function(r){st[n]=r?1:2;if(r)ok++;var sb=app.querySelector('.sbar');if(sb)sb.outerHTML=bar()}})}
  step()}
function rndCode(){
  if(!passed('test').length){toast('Сначала пройди хотя бы один островок с кодом');return}
  rndWarn(function(){RND.last=null;rcNext()})}
function rcNext(){
  var P=passed('test'),T=[];P.forEach(function(p){IT(p[0],p[1]).tasks.forEach(function(q,n){T.push({q:q,k:p[0]+'-'+p[1]+'-'+n})})});
  if(!T.length){practice();return}
  var x;do{x=T[Math.floor(Math.random()*T.length)]}while(T.length>1&&x.k===RND.last);RND.last=x.k;var q=x.q;
  scr('rcode','<h1 class="sr-only">Случайный код</h1><div class="top ls"><button class="icon" id="x" aria-label="Выйти">'+ico('x')+'</button><span class="lstep grow">🎲 Случайный код</span>'+(q.h?'<button class="icon" id="hb" aria-label="Подсказка">'+ico('bulb')+'</button>':'')+'</div>'+taskCard(q)+'<div id="hint"></div>'+edCard('Решение','# Пиши код здесь\n'+(q.starter||''),0,'# Пиши код здесь\n'+(q.starter||''))+conHtml()+'<div id="fb"></div>'+dockHtml('<button class="btn" id="chk">Проверить</button>'));
  $('x').onclick=practice;
  var c=$('code'),sync=initEd(c,function(){});sync();
  if(q.h)$('hb').onclick=function(){snd('hint');$('hb').classList.add('on');$('hint').innerHTML='<div class="fb"><b>Подсказка</b>'+hintTx(q.h)+'</div>';$('hint').scrollIntoView({block:'nearest',behavior:RM()?'auto':'smooth'})};
  skReady();chkPulse();runBind(c);
  $('chk').onclick=async function(){
    var b=$('chk');if(!SKOK)fbSet('<div class="fb"><b>Загружаю среду Python…</b></div>');
    if(!(await needSk()))return;
    b.disabled=true;var v=await judge(q,c.value);
    if(!v.ok){fx(false);b.disabled=false;PRW++;fbSet(badFb(v.h,errMood(PRW)));return}
    PRW=0;fx(true,'test');rcInc();
    fbSet('<div class="fb"><b>Все тесты пройдены!</b>Опыт не начисляется, это тренировка.</div>');
    dockSet('<button class="btn" id="nx">Ещё задание</button>'+(q.sol?'<button class="btn t" id="sl">Посмотреть, как задумано</button>':''),1);
    $('nx').onclick=rcNext;if(q.sol)$('sl').onclick=function(){solModal(q.sol)}}}
function chkPulse(){var c=$('code'),b=$('chk');if(!c||!b)return;function u(){var v=c.value.trim();b.classList.toggle('pulse',v!==''&&v!=='# Пиши код здесь')}u();c.addEventListener('input',u)}
/* полоса уровня на экранах итога: заполняется от старого значения к новому */
function xpStrip(gain){
  var L=lvlInfo(S.xp),L0=lvlInfo(Math.max(0,S.xp-(gain||0))),p0=L0.l===L.l?L0.p:0;
  return'<div class="xps"><div class="xph"><b>Уровень '+L.l+'</b><span class="mu">до '+(L.l+1)+': ещё '+L.left+' ⭐</span></div><div class="bar" style="height:12px" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="'+L.p+'" aria-label="Прогресс уровня"><i class="xpb" style="width:'+p0+'%" data-p="'+L.p+'"></i></div></div>'}
function xpStripRun(){var b=app.querySelector('.xpb');if(!b)return;setTimeout(function(){b.style.width=b.dataset.p+'%'},RM()?0:450)}

/* --- достижения-дискеты --- */
function hsh(s){var h=0;for(var i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))|0;return Math.abs(h)}
function fdate(d){var p=d.split('-');return(+p[2])+' '+MON[+p[1]-1]+' '+p[0]}
function floppyFace(a){return'<div class="fface" style="--fc:'+a.c+'" aria-hidden="true"><div class="fsh"><i></i></div><div class="flb"><div class="fe">'+a.e+'</div><div class="fn">'+esc(a.n)+'</div></div></div>'}
function floppyBtn(a){return'<button class="fd" data-id="'+a.id+'" style="--fc:'+a.c+';--lean:'+((hsh(a.id)%5)-2)*1.4+'deg" aria-label="Достижение: '+esc(a.n)+'"><span class="fb3" aria-hidden="true"><span class="ff"><span class="fm"></span><span class="fl"><em>'+a.e+'</em></span></span><span class="fsx"><span class="fsn"></span><em>'+a.e+'</em></span><span class="fbk"></span></span><i class="fsd"></i></button>'}
function shelf(){
  /* общее число достижений не показываем: это тайна */
  var L=ACH.filter(function(a){return S.ach[a.id]}).sort(function(a,b){return S.ach[a.id]<S.ach[b.id]?-1:S.ach[a.id]>S.ach[b.id]?1:0}),hz=ST('sh')==='h',per=Math.max(4,Math.min(10,Math.floor((Math.min(innerWidth,640)-80)/(ST('fl')==='flat'?22:44))));
  var h='<div class="card shelfc"><div class="sh-h"><b>Достижения</b><span class="mu">Получено: '+L.length+'</span></div>';
  if(!L.length)return h+'<div class="shrow"></div><p class="mu" style="margin:10px 0 0">Здесь появятся дискеты за твои успехи. За что их дают, узнаешь сам.</p></div>';
  if(hz)h+='<div class="shrow hs" tabindex="0" aria-label="Полка с дискетами">'+L.map(floppyBtn).join('')+'</div>';
  else for(var r=0;r<L.length;r+=per){h+='<div class="shrow">'+L.slice(r,r+per).map(floppyBtn).join('')+'</div>'}
  return h+'</div>'}
function fdOpen(btn){
  var a=achDef(btn.dataset.id);if(!a||btn.dataset.busy)return;btn.dataset.busy=1;
  snd('disk');vib(12);MSIL=1;
  var an=RM()?null:btn.animate([{transform:'translateY(0)'},{transform:'translateY(-30px) rotate(-3deg)'}],{duration:260,easing:'cubic-bezier(.2,.9,.3,1.2)',fill:'forwards'});
  setTimeout(function(){
    var m=modal('<div class="fwin">'+floppyFace(a)+'<h2>'+esc(a.n)+'</h2><p class="fd2">'+esc(a.d)+'</p><p class="mu">Получено '+fdate(S.ach[a.id])+'</p></div>',[['Закрыть',null,1]]);
    new MutationObserver(function(x,o){if(!document.body.contains(m)){o.disconnect();if(an)an.cancel();delete btn.dataset.busy}}).observe(document.body,{childList:true});
  },RM()?0:230)}

/* --- профиль --- */
/* U1-13: кроличьи норы — сколько пройдено целиком (в профиле и в «Поделиться» — только когда пройдена хотя бы одна) */
function HN(){return TOPICS.filter(function(t){return t.opt}).length}
function HD(){return TOPICS.filter(function(t,i){if(!t.opt||!ni(i))return false;for(var j=0;j<ni(i);j++)if(!S.d[i+'-'+j])return false;return true}).length}
function shareTxt(){var n=ND(),h=HD(),s=streakNow();return'Я учу Python в ИТП! Уже '+G('прошёл','прошла','пройдено')+' '+n+' '+pl(n,['тему','темы','тем'])+(h?' и '+h+' '+pl(h,['кроличью нору','кроличьи норы','кроличьих нор'])+' из '+HN():'')+(s?', '+s+' '+pl(s,['день','дня','дней'])+' подряд':'')+', '+S.xp+' XP. Попробуй и ты!'}
/* --- U1-7: «Что ты уже умеешь» — шкала курса как в Duolingo. Очки — пройденные островки (и в норах тоже, вступление не в счёт);
   веха — конец темы: её порог равен числу островков основного курса до неё включительно --- */
/* значки вех — линейные, в духе набора Lucide (ISC), нарисованы здесь же; цвет — currentColor */
var SKI={sprout:'<path d="M7 20h10M12 20v-8"/><path d="M12 12C12 8 9.5 6 5 6c0 4 2.5 6 7 6zM12 10c0-3 2-5 6.5-5 0 3-2 5-6.5 5z"/>',
 msg:'<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
 kbd:'<rect x="2" y="6" width="20" height="12" rx="2"/><path d="M6 10h.01M10 10h.01M14 10h.01M18 10h.01M7 14h10"/>',
 calc:'<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M8 6h8M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15h.01M8 18h.01M12 18h4"/>',
 loop:'<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
 list:'<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
 fn:'<path d="M8 3H7a2 2 0 0 0-2 2v5a2 2 0 0 1-2 2 2 2 0 0 1 2 2v5a2 2 0 0 0 2 2h1M16 21h1a2 2 0 0 0 2-2v-5a2 2 0 0 1 2-2 2 2 0 0 1-2-2V5a2 2 0 0 0-2-2h-1"/>',
 file:'<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.7-.9l-.8-1.2A2 2 0 0 0 7.9 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2z"/>',
 sort:'<path d="m3 16 4 4 4-4M7 20V4M11 4h10M11 8h7M11 12h4"/>',
 box:'<path d="M21 8a2 2 0 0 0-1-1.7l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.7l7 4a2 2 0 0 0 2 0l7-4a2 2 0 0 0 1-1.7z"/><path d="m3.3 7 8.7 5 8.7-5M12 22V12"/>',
 chart:'<path d="M3 3v18h18"/><path d="M18 17V9M13 17V5M8 17v-3"/>',
 bot:'<rect x="3" y="8" width="18" height="12" rx="2"/><path d="M12 8V4H8M2 14h2M20 14h2M9 13v2M15 13v2"/>',
 cap:'<path d="M22 10 12 5 2 10l10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>'};
function ski(k){return'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'+SKI[k]+'</svg>'}
/* знак-остров: тот же наклонный шестиугольник, что на Пути, плоский, в цвет акцента */
var SKHX='<svg class="skx" viewBox="6 10 80 56" aria-hidden="true" focusable="false"><path class="s" d="M9 34 L27 54 L65 54 L83 34 L83 44 L65 64 L27 64 L9 44 Z"/><path d="M9 34 L27 14 L65 14 L83 34 L65 54 L27 54 Z"/></svg>';
/* вехи как в Duolingo: короткое действие из жизни, которое уже по силам; can — то же для реплики «Значит, ты уже можешь…» */
var SKL=[['','sprout','Начинаем',''],
 ['Начало знакомства','msg','Напиши первую программу','написать свою программу'],
 ['Переменные и ввод','kbd','Поговори с программой','научить программу задавать вопросы'],
 ['Условия','calc','Сделай калькулятор','сделать свой калькулятор'],
 ['Циклы в циклах','loop','Нарисуй узор','рисовать узоры кодом'],
 ['Словари и множества','list','Собери телефонную книгу','собрать свою телефонную книгу'],
 ['Гибкие функции','fn','Напиши мини-игру','написать мини-игру'],
 ['Файлы и форматы данных','file','Разбери файлы с данными','работать с файлами'],
 ['Поиск и сортировка','sort','Отсортируй рекорды','отсортировать таблицу рекордов'],
 ['Наследование','box','Опиши героя игры','описать героя игры классом'],
 ['Таблицы данных','chart','Найди закономерность в данных','разбирать таблицы с данными'],
 ['Запросы к серверам','bot','Сделай бота','сделать своего бота'],
 ['Итоговые проекты','cap','Курс пройден','сделать свой проект от идеи до программы']];
function skPts(){var n=0;TOPICS.forEach(function(t,i){if(t.intro)return;for(var j=0;j<ni(i);j++)if(S.d[i+'-'+j]||(!t.opt&&i<S.start))n++});return n}
function skList(){var c=0,th={};TOPICS.forEach(function(t,i){if(t.intro||t.opt)return;c+=ni(i);th[t.n]=c});
  return SKL.map(function(m){return{t:m[0]?th[m[0]]:0,e:m[1],n:m[2],c:m[3]}}).filter(function(m){return m.t!==undefined})}
function skNow(){var p=skPts(),L=skList(),k=0;L.forEach(function(m,i){if(p>=m.t)k=i});return{p:p,L:L,k:k}}
/* U1-7: новое умение — окно после итога островка (как в Duolingo «теперь ты можешь…») с переходом на страницу.
   S.skk — последнее показанное; -1 у старых сохранений: тогда запоминаем текущее молча, без окна за прошлое */
function skNew(){var k=skNow().k;if(S.skk<0){S.skk=k;save();return false}return k>S.skk}
function skPop(then){
  var s=skNow(),m=s.L[s.k];S.skk=s.k;save();
  var o=modal('<div class="skm"><span class="skd" aria-hidden="true">'+ski(m.e)+'</span><p class="skr">Новое умение</p><h2>'+esc(m.n)+'</h2>'+rbSay('Теперь ты можешь '+esc(m.c)+'!')+'</div>',
   [['Посмотреть прогресс',function(){var f=then;then=null;setTimeout(function(){skills(f)},RM()?0:200)}],['Дальше',null,1]]);
  var rm=o.remove;o.remove=function(){rm.call(o);if(then){var f=then;then=null;setTimeout(f,RM()?0:200)}};
  snd('ach');return o}
/* реплика кролика: голова без подложки и пузырь с хвостиком, как у персонажей Duolingo */
function rbSay(t){var hd=IMG.wowhead||IMG.eat;return'<div class="gsay">'+(hd?'<img class="gav" src="'+hd+'" alt="" draggable="false">':'')+'<p>'+t+'</p></div>'}
/* back — куда вернуться: в настройки (по умолчанию) или дальше по пути из окна нового умения */
function skills(back){
  var s=skNow(),L=s.L,m=L[s.k];
  var h='<div class="top ls"><button class="icon" id="x" aria-label="Назад">'+ico('back')+'</button><h1>Что ты уже умеешь</h1></div><div class="skp">'+
   '<div class="skh">'+SKHX+'<b>'+s.p+'</b></div><p class="mu skn">'+pl(s.p,['островок пройден','островка пройдено','островков пройдено'])+', норы тоже считаются</p>'+
   rbSay(s.k?'Значит, ты уже можешь '+esc(m.c)+'!':'Пройди первую тему, и здесь появится, что ты уже можешь')+
   '<h2 class="skov">Прогресс</h2><ol class="skl">'+L.map(function(x,i){var on=s.p>=x.t,nw=i===s.k;return'<li class="'+(on?'on':'')+(nw?' now':'')+(i+1<L.length&&s.p>=L[i+1].t?' fl':'')+'"><span class="skd">'+ski(x.e)+'</span><span class="sktx"><small>'+SKHX+x.t+'</small><b>'+esc(x.n)+'</b></span></li>'}).join('')+'</ol></div>';
  scr('skills',h);$('x').onclick=function(){if(typeof back==='function')back();else{SBACK=SBACK||profile;settings()}}}
/* U1-9: цель дня и цель серии выбираются в одном окне (sgChooser в a_screens.js) */
function goalSheet(){sgChooser(function(){if(CURTAB!=='prof')return;KEEPSCR=1;SKEY='profile';var y=window.scrollY;profile();window.scrollTo(0,y)})}
function profile(){BACK=profile;
  var n=ND(),LV=lvlInfo(S.xp),d=goalDone(),g=S.goal,gp=Math.min(100,Math.round(d/g*100)),f=S.fz,s=streakNow();
  var rows=TOPICS.map(function(t,i){var c=0,l=[];(t.items||[]).forEach(function(x,j){var e=S.es[i+'-'+j]||0;c+=e;if(e>0)l.push({j:j,n:x.n,e:e,ic:ity(x)[1]})});return{i:i,n:t.n,c:c,l:l}}).filter(function(r){return r.c>0}).sort(function(a,b){return b.c-a.c});
  var EM=3,more=rows.length>EM;
  function erow(r,k){return'<div class="eg2"'+(k>=EM?' hidden':'')+'><div class="erow"><span>'+esc(r.n)+'</span><b aria-label="ошибок: '+r.c+'">'+r.c+'</b></div><div class="elist">'+r.l.map(function(x){return'<button class="elink" data-i="'+r.i+'" data-j="'+x.j+'"><span class="et">'+x.ic+'&nbsp;'+esc(x.n)+'<small>ошибок: '+x.e+'</small></span><span class="eg">Отработать</span></button>'}).join('')+'</div></div>'}
  scr('profile',head()+'<h1 class="sr-only">Профиль</h1><div class="pf">'+
   '<div class="hero"><div class="pav" aria-hidden="true">'+rabbit('eat')+'</div><div class="hn"><b class="nmx">'+nk(S.nick)+'</b><div class="lvp"><span class="pill">Уровень '+LV.l+'</span><span class="mu">до '+(LV.l+1)+': ещё '+LV.left+' ⭐</span></div><div class="bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="'+LV.p+'" aria-label="Прогресс уровня"><i class="grow" style="width:'+LV.p+'%"></i></div></div></div>'+
   '<div class="tiles"><button class="tile tbig'+(s>=100?' d3':s>=10?' d2':'')+'" id="tst"><span aria-hidden="true">🥕</span><span><b>'+s+'</b><small>'+pl(s,['день','дня','дней'])+' подряд</small></span>'+(f.n?'<i class="fzm" aria-label="заморозок: '+f.n+'">❄️'+f.n+'</i>':'')+'</button><div class="tcol"><div class="tile"><span aria-hidden="true">🏆</span><span><b>'+Math.max(S.max,s)+'</b><small>рекорд серии</small></span></div><button class="tile" id="txp"><span aria-hidden="true">⭐</span><span><b>'+S.xp+'</b><small>опыта</small></span></button><div class="tile"><span aria-hidden="true">📚</span><span><b>'+n+' из '+NT()+'</b><small>тем пройдено</small></span></div>'+(HD()?'<div class="tile"><span aria-hidden="true">🐰</span><span><b>'+HD()+' из '+HN()+'</b><small>нор пройдено</small></span></div>':'')+'</div></div>'+
   '<section class="psec"><div class="ch2"><b>Цель дня</b><button class="btn t" id="gset">'+g+' '+pl(g,['островок','островка','островков'])+' ›</button></div><div class="psf"><div class="bar gbar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="'+gp+'" aria-label="Цель дня: '+d+' из '+g+'"><i class="grow" style="width:'+gp+'%"></i></div>'+weekRow('g')+(S.sg.n?'<p class="mu gnote">Цель серии: '+Math.min(s,S.sg.n)+' из '+S.sg.n+' '+pl(S.sg.n,['дня','дней','дней'])+' подряд, за неё +'+SGX[S.sg.n]+' ⭐.</p>':'<p class="mu gnote">Цель серии не выбрана. Нажми на цель дня, чтобы выбрать.</p>')+'</div></section>'+
   shelf()+
   '<section class="psec"><div class="ch2"><b>Активность</b></div><div class="psf">'+calHtml()+'</div></section>'+
   (rows.length?'<section class="psec"><div class="ch2"><b>Работа над ошибками</b></div><div class="psf">'+rows.map(erow).join('')+(more?'<button class="btn t emore" id="emr">Показать все темы ('+rows.length+')</button>':'')+'<p class="mu enote">Пройди островок без ошибок, и он исчезнет из списка.</p></div></section>':'')+
   '<div class="lst">'+row('📖','Изученные функции','Словарь с твоими заметками','dc')+(TOPICS[0]&&TOPICS[0].intro&&!S.d['0-0']?row('🏝️','Знакомство с ИТП','Как устроено приложение','intr'):'')+row('📤','Поделиться прогрессом','Картинка со статистикой','sh')+row('⚙️','Настройки','Вид, звук, обучение, резервная копия','st')+'</div>'+
   '<p class="pfoot"><button class="ver" id="vr" aria-label="ИТП '+ITPV+'. ИТП означает: И так, программирование"><u>ИТП '+ITPV+'</u><span class="vt" role="tooltip">ИТП — «И так, программирование»</span></button></p></div>','prof');
  /* подпись месяца стоит у его первого дня и часто уезжает влево за край — под лентой сразу сегодняшний день, потом тот, на который нажали */
  bindHead(profile);calBind();var ci0=$('ci');if(ci0&&!ci0.textContent)ci0.textContent=calText(day(new Date()));var csc=app.querySelector('.csc');if(csc){csc.tabIndex=0;csc.setAttribute('aria-label','Календарь активности, листается вбок')}
  var vr=$('vr'),vt;vr.onclick=function(){vr.classList.add('on');clearTimeout(vt);vt=setTimeout(function(){vr.classList.remove('on')},2500)};
  $('tst').onclick=streakSheet;$('txp').onclick=levelSheet;$('gset').onclick=goalSheet;
  if($('emr'))$('emr').onclick=function(){app.querySelectorAll('.eg2[hidden]').forEach(function(x){x.hidden=false});this.remove()};
  app.querySelectorAll('.fd').forEach(function(b){b.onclick=function(){fdOpen(b)}});
  app.querySelectorAll('.lst .li').forEach(function(b){b.onclick=function(){var a=b.dataset.a;if(a==='dc')dict();else if(a==='sh')share();else if(a==='intr'){BACK=profile;theory(0,0)}else if(a==='st'){SBACK=profile;settings()}}});
  app.querySelectorAll('.elink').forEach(function(b){b.onclick=function(){BACK=profile;go(+b.dataset.i,+b.dataset.j)}});
}

/* --- настройки (второй уровень: без нижней панели, назад — туда, откуда пришли) --- */
/* подсказка: строки, которые целиком код (print(...), a = int(input()), for ...), — моноширинным, как в теории */
function hintTx(h){return String(h||'').split('\n').map(function(l){return/^([A-Za-z_][\w.]*\s*(\(|\[|=|\+=|-=)|(for|if|elif|else|while|def|import|from|return)\b)/.test(l.trim())?'<code class="hcl">'+esc(l)+'</code>':esc(l)}).join('<br>')}
function SW(k,on,lab){return'<button class="sw" role="switch" aria-checked="'+(on?'true':'false')+'" data-k="'+k+'"'+(lab?' aria-label="'+esc(lab)+'"':'')+'></button>'}
function SG(k,opts,cur){return'<div class="segc" role="radiogroup">'+opts.map(function(o){var on=String(cur)===String(o[0]);return'<button role="radio" aria-checked="'+on+'" data-k="'+k+'" data-v="'+o[0]+'" class="'+(on?'on':'')+'">'+o[1]+'</button>'}).join('')+'</div>'}
function SR(ic,t,sub,ctl,a){var blk=ctl&&/segc|swa|type="range"/.test(ctl),sw=ctl&&/class="sw"/.test(ctl);if(sw)ctl=ctl.replace('class="sw"','class="sw" aria-label="'+esc(t)+'"');return(a?'<button class="li" data-a="'+a+'">':'<div class="li static'+(blk?' blk':'')+(sw?' tg':'')+'">')+'<span class="lic" aria-hidden="true">'+ic+'</span><span class="lt">'+t+(sub?'<small>'+sub+'</small>':'')+'</span>'+(ctl||ico('chev','ch'))+(a?'</button>':'</div>')}
function setSet(k,v){
  if(k==='theme'){themeSwap(function(){S.theme=v;save();applyPrefs()});return}
  if(k==='mute'){S.mute=v?0:1}else if(k==='goal'){S.goal=+v}else if(k==='g'){S.g=v}else if(k==='hc'){S.hc=v?0:1}
  else{S.set[k]=(typeof v==='number'||typeof v==='boolean')?v:(/^\d+$/.test(v)?+v:v)}
  save();applyPrefs();
  if(k==='emo'){if(ST('emo')){emoLoad();if(EM.map)emoOn()}else emoOff()}
  if(k==='goal')goalCheck()}
function settings(){
  var h='<div class="top ls"><button class="icon" id="x" aria-label="Назад">'+ico('back')+'</button><h1>Настройки</h1></div>';
  h+='<div class="sec">Внешний вид</div><div class="lst">'+
   SR('🎨','Тема','',SG('theme',[['','Авто'],['light','Светлая'],['dark','Тёмная']],S.theme))+
   SR('🖌️','Цвет акцента','Кнопки, полоски, выделение','<div class="swa" role="radiogroup" aria-label="Цвет акцента">'+[['','#2B8420','Зелёный'],['carrot','#F08C1A','Морковный'],['pink','#C73B63','Розовый'],['blue','#2563D0','Синий'],['violet','#6C4BD6','Фиолетовый']].map(function(c){var on=ST('acc')===c[0];return'<button role="radio" aria-checked="'+on+'" data-k="acc" data-v="'+c[0]+'" style="background:'+c[1]+';color:'+c[1]+'" class="'+(on?'on':'')+'" aria-label="'+c[2]+'"></button>'}).join('')+'</div>')+
   SR('🔤','Размер текста','',SG('tz',[[90,'Мелкий'],[100,'Обычный'],[115,'Крупный'],[130,'Огромный']],ST('tz')))+
   SR('✨','Анимации','«Выкл» подойдёт слабым устройствам и тем, кого они отвлекают',SG('anim',[['full','Все'],['less','Меньше'],['off','Выкл']],ST('anim')))+
   SR('😀','Смайлики Windows 11','Встроены и выглядят одинаково на всех устройствах',SW('emo',ST('emo')))+
   SR('🎉','Конфетти','Салют, когда тема пройдена',SW('gc',ST('gc')))+
   SR('🐰','Шапка профиля','Где стоит кролик',SG('ph',[['card','Карточка'],['corner','В углу'],['pop','Из плитки']],ST('ph')))+
   SR('🌊','Узор на фоне','Точки, как тропинка между островками, и мягкий свет цвета акцента. Выкл: ровный фон',SW('bg',ST('bg')))+'</div>';
  h+='<div class="sec">Полка достижений</div><div class="lst">'+
   SR('🗄️','Когда дискет много','',SG('sh',[['v','Вторая полка ниже'],['h','Листать вбок']],ST('sh')))+
   SR('💾','Вид дискет','',SG('fl',[['tilt','Объёмные'],['flat','Плоские']],ST('fl')))+'</div>';
  h+='<div class="sec">Звук и отклик</div><div class="lst">'+
   SR('🔊','Звук','Главный выключатель: выкл — полная тишина',SW('mute',!S.mute))+
   SR('🎚️','Громкость','','<input type="range" min="0" max="100" step="5" value="'+ST('vol')+'" id="vol" aria-label="Громкость">')+
   SR('👆','Звуки интерфейса','Касания, переходы и окна. Ответы, опыт и награды звучат всегда',SW('sfx',ST('sfx')))+
   SR('⌨️','Звуки набора кода','Очень тихий щелчок клавиш в редакторе',SW('ks',ST('ks')))+
   SR('📳','Вибрация','При ошибке и успехе',SW('vib',ST('vib')))+'</div>';
  h+='<div class="sec">Обучение</div><div class="lst">'+
   SR('🎯','Цель дня','Сколько островков в день',SG('goal',[[1,'1'],[2,'2'],[3,'3']],S.goal))+
   SR('⌨️','Печатать теорию по буквам','Выкл: текст появится сразу',SW('ty',ST('ty')))+
   SR('📑','Оглавление теории','Слева на широких экранах',SW('toc',ST('toc')))+
   SR('📐','Пример в задании','Компактно: ввод и вывод рядом, больше места для кода',SG('exl',[['c','Компактно'],['b','Крупно']],ST('exl')))+
   SR('🔁','Повторение после перерыва','3 вопроса, если не заходил 3 дня и больше',SW('rep',ST('rep')))+
   SR('💡','Спрашивать про подсказку','Напомнить, что опыт будет вдвое меньше',SW('hc',!S.hc))+'</div>';
  h+='<div class="sec">Редактор кода</div><div class="lst">'+
   SR('🔠','Размер кода','',SG('cf',[[13,'S'],[15,'M'],[17,'L'],[19,'XL']],ST('cf')))+
   SR('🔢','Номера строк','',SW('ln',ST('ln')))+
   SR('🧩','Закрывать скобки и кавычки','Сама допишет пару',SW('ac',ST('ac')))+'</div>';
  var skn=skNow();
  h+='<div class="sec">Профиль и данные</div><div class="lst">'+
   SR('🌱','Что ты уже умеешь',skn.k?esc(skn.L[skn.k].n)+', '+skn.p+' '+pl(skn.p,['островок','островка','островков']):'Шкала умений курса','','skl')+
   SR('🐰','Никнейм',nk(S.nick),'','nick')+
   SR('🙂','Обращение','Для правильных окончаний в тексте',SG('g',[['m','Парень'],['f','Девушка'],['','Не указывать']],S.g||''))+
   SR('💾','Резервная копия','Сохранить или загрузить прогресс','','bk')+
   SR('🧹','Сбросить оформление','Вернуть вид и звук как было','','rs1')+
   SR('🗑️','Сбросить прогресс','Удалит всё, кроме сохранённых кодов и звука','','rs2')+'</div>';
  h+='<div class="sec">О приложении</div><div class="lst">'+(KBD?SR('⌨️','Горячие клавиши','','','kb'):'')+SR('📖','Прочитать введение','Знакомство с ИТП ещё раз','','intro')+SR('🐇','ИТП','«И так, программирование»','<span class="lv" id="egv">'+ITPV+'</span>')+'</div><div style="height:24px"></div>';
  scr('settings',h,null);HRE=settings;
  $('x').onclick=function(){(SBACK||profile)()};
  function again(){var yy=window.scrollY;KEEPSCR=1;SKEY='settings';settings();window.scrollTo(0,yy)}
  app.querySelectorAll('.sw').forEach(function(b){b.onclick=function(e){e.stopPropagation();var on=b.getAttribute('aria-checked')!=='true';var k=b.dataset.k;b.setAttribute('aria-checked',on?'true':'false');if(!on)snd('off');setSet(k,on?1:0);if(on)snd('on')}});
  /* строку с выключателем можно нажать целиком: так проще попасть пальцем */
  app.querySelectorAll('.li.tg').forEach(function(r){r.onclick=function(e){if(e.target.closest('.sw'))return;var s=r.querySelector('.sw');if(s)s.click()}});
  app.querySelectorAll('.segc button,.swa button').forEach(function(b){b.onclick=function(){var g=b.parentNode;g.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b);x.setAttribute('aria-checked',x===b?'true':'false')});setSet(b.dataset.k,b.dataset.v);snd('click');if(g.classList.contains('segc'))segPos(g,true)}});
  eggBind();
  var v=$('vol');v.oninput=function(){S.set.vol=+v.value;save();sxVol(VOLK())};v.onchange=function(){snd('ok')};
  app.querySelectorAll('.lst button.li').forEach(function(b){b.onclick=function(){var a=b.dataset.a;
    if(a==='nick')askName('Никнейм',S.nick,function(n){n=Array.from(n).slice(0,20).join('');if(nkBad(n)){snd('bad');toast('🐰 Так ник назвать нельзя');return false}S.nick=n;save();again();toast('Никнейм изменён')},20);
    else if(a==='bk')backup();
    else if(a==='skl')skills();
    else if(a==='kb')keys();
    else if(a==='intro'){BACK=function(){settings()};theory(0,0)}
    else if(a==='rs1')modal('<h2>Сбросить оформление?</h2><p>Тема, цвет, размер текста, звук и другие настройки станут как в начале. Прогресс не изменится.</p>',[['Сбросить',function(){themeSwap(function(){S.set=clean({}).set;S.theme='';S.mute=0;save();applyPrefs();emoLoad();again()});toast('Настройки сброшены')},0,1],['Отмена',null,1]]);
    else if(a==='rs2')modal('<h2>Сбросить весь прогресс?</h2><p>Опыт, серия, пройденные островки, достижения и настройки оформления удалятся, знакомство начнётся заново. Сохранённые коды и звук останутся. Отменить это нельзя.</p>',[['Да, сбросить',function(){S=clean({mute:S.mute,sv:S.sv,ec:S.ec,cur:S.cur,nick:''});applyTheme();seedLit();save();nick()},0,1],['Отмена',null,1]])}});
}
/* --- оглавление теории (широкие экраны) --- */
var TOCS=null;
function tocKill(){var o=document.getElementById('toc');if(o)o.remove();if(TOCS){window.removeEventListener('scroll',TOCS);TOCS=null}}
function tocBuild(){
  tocKill();if(!ST('toc'))return;var tb=$('tb');if(!tb)return;
  var hs=[].slice.call(tb.querySelectorAll('h3'));if(hs.length<4)return;
  var a=document.createElement('nav');a.id='toc';a.setAttribute('aria-label','Оглавление');
  a.innerHTML='<div class="tct">Оглавление</div>'+hs.map(function(h,k){h.id='tcs'+k;return'<button data-k="'+k+'">'+esc(h.textContent)+'</button>'}).join('');
  document.body.appendChild(a);
  var bs=[].slice.call(a.querySelectorAll('button'));
  bs.forEach(function(b){b.onclick=function(){tb.click();hs[+b.dataset.k].scrollIntoView({behavior:RM()?'auto':'smooth',block:'start'})}});
  function spy(){var y=innerHeight*.32,c=-1;hs.forEach(function(h,k){if(h.offsetParent&&h.getBoundingClientRect().top<y)c=k});if(window.scrollY>0&&window.scrollY+innerHeight>=document.documentElement.scrollHeight-6){for(var q=hs.length-1;q>=0;q--)if(hs[q].offsetParent){c=q;break}}bs.forEach(function(b,k){b.classList.toggle('on',k===c)})}
  TOCS=spy;window.addEventListener('scroll',spy,{passive:true});if(window.ResizeObserver){var ro=new ResizeObserver(function(){if(!a.isConnected||!TOCS){ro.disconnect();return}TOCS()});ro.observe(document.body)}setTimeout(spy,50)}

/* --- рост серии и опыта в шапке --- */
var LSK=null,LXP=null;
function chipFx(){
  var hs=$('hs'),hx=$('hx');if(!hs||!hx)return;
  var s=streakNow(),x=S.xp;
  if(LSK!==null&&s>LSK)snd('streak');
  if(LSK!==null&&s>LSK&&!RM())hs.animate([{transform:'scale(1)'},{transform:'scale(1.25) rotate(-4deg)'},{transform:'scale(1)'}],{duration:520,easing:'cubic-bezier(.3,1.6,.5,1)'});
  if(LXP!==null&&x>LXP){
    var el=hx.querySelector('span:last-child'),a=LXP,t0=performance.now();
    if(RM()){el.textContent=x;snd('xpt',{k:0})}else{hx.animate([{transform:'scale(1)'},{transform:'scale(1.18)'},{transform:'scale(1)'}],{duration:600,easing:'cubic-bezier(.3,1.4,.5,1)'});
    var xt=xpTick();(function st(t){var k=Math.min(1,(t-t0)/700),vv=Math.round(a+(x-a)*(1-Math.pow(1-k,3)));el.textContent=vv;xt(vv-a);if(k<1)requestAnimationFrame(st)})(t0)}}
  LSK=s;LXP=x}
