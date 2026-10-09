/* ===================== ИТП v5.1.3 — интерфейс ===================== */
function rabbit(st){var s=IMG[st]||IMG.eat;return'<div class="rw im '+st+'"><img src="'+s+'" alt="Кролик" draggable="false"></div>'}
function tabFn(){return({home:home,pr:practice,ed:editor,prof:profile})[CURTAB]||home}
var SBACK=null;
function head(t){
  var f=S.fz.n,s=streakNow();
  return'<div class="top">'+(t?'<h1>'+esc(t)+'</h1>':'<div class="logo" id="ttl">ИТП</div>')+'<div class="chips"><button class="chip" id="hs" aria-label="Серия: '+s+'">🥕 <span>'+s+'</span>'+(f?'<span class="fzm">❄️ '+f+'</span>':'')+'</button><button class="chip" id="hx" aria-label="Опыт: '+S.xp+'">⭐ <span>'+S.xp+'</span></button><button class="icon" id="hg" aria-label="Настройки">⚙️</button></div></div>'}
function bindHead(re){
  HRE=re;$('hs').onclick=streakSheet;$('hx').onclick=levelSheet;chipFx();
  $('hg').onclick=function(){SBACK=tabFn();settings()};
  var tt=$('ttl');if(tt)tt.onclick=function(){window.scrollTo({top:0,behavior:RM()?'auto':'smooth'})}}
function weekRow(mode){
  var w=wkStart(),t=day(new Date()),nm=['Пн','Вт','Ср','Чт','Пт','Сб','Вс'],h='<div class="wk" role="img" aria-label="Неделя">';
  for(var i=0;i<7;i++){
    var d=dadd(w,i),a=S.hist[d]&&S.hist[d].les>0,fz=S.fz.u.indexOf(d)>=0&&!a,g=!!S.gm[d],cl,ic;
    if(mode==='g'){cl=g?'on':(d>t?'fu':'');ic=g?'✓':''}
    else{cl=a?'on':fz?'fz':(d>t?'fu':'');ic=a?'✓':fz?'❄️':''}
    h+='<div class="wd '+cl+(d===t?' td':'')+'"><span>'+nm[i]+'</span><i>'+ic+'</i></div>'}
  return h+'</div>'}
function streakSheet(){
  var s=streakNow(),f=S.fz;
  modal('<div class="ssh"><div class="big">🥕 <b>'+s+'</b></div><p class="mu" style="text-align:center">'+pl(s,['день','дня','дней'])+' подряд'+(s?'':'. Пройди островок сегодня, и серия начнётся')+'</p>'+weekRow('a')+'<div class="fzr"><div class="fzi">'+[0,1].map(function(i){return'<span class="fzs'+(i<f.n?' on':'')+'">❄️</span>'}).join('')+'</div><div class="fzt"><b>Заморозки серии: '+f.n+' из 2</b><span class="mu">'+(f.n>=2?'Максимум. Потратятся сами, если пропустишь день.':'До новой: ещё '+(15-f.p)+' '+pl(15-f.p,['островок','островка','островков'])+'. Тратится сама, если пропустишь день.')+'</span></div></div><p class="mu" style="text-align:center;margin:0">Рекорд серии: '+Math.max(S.max,s)+'</p></div>',[['Понятно']])}
function levelSheet(){
  var L=lvlInfo(S.xp);
  modal('<div class="ssh"><div class="big">⭐ <b>'+S.xp+'</b></div><p class="mu" style="text-align:center">Уровень '+L.l+'</p><div class="bar" style="height:14px;margin:10px 0"><i class="grow" style="width:'+L.p+'%"></i></div><p class="mu" style="text-align:center;margin:0">До уровня '+(L.l+1)+' осталось '+L.left+' ⭐</p></div>',[['Понятно']])}

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
    window.scrollTo(0,0);var c=app.querySelector('.cur');if(c)c.scrollIntoView({block:'center'});
    links();
  }
  if(!intro||!rest.length){end();return}
  if(rm){
    A(intro,[{opacity:1},{opacity:0}],{duration:400,fill:'forwards'});
    rest.forEach(function(e,k){A(e,[{opacity:0},{opacity:1}],{duration:500,delay:400+k*120,fill:'both'})});
    T(end,1300);return}
  var ib=intro.querySelector('.isl'),ir=ib.getBoundingClientRect(),cx=ir.left+ir.width/2,cy=ir.top+ir.height/2;
  var rc=getComputedStyle(ib).getPropertyValue('--ti').trim()||'#3B82F6';
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
  T(function(){
    intro.style.display='none';window.scrollTo(0,0);snd('level');
    rest.forEach(function(e,k){A(e,[{opacity:0,transform:'translateY(30px) scale(.97)',filter:'blur(8px)'},{opacity:1,transform:'none',filter:'blur(0)'}],{duration:800,delay:k*140,easing:'cubic-bezier(.2,.8,.2,1)',fill:'both'})});
    var k2=0;rest.forEach(function(e){[].forEach.call(e.querySelectorAll('.ilw'),function(il){A(il,[{opacity:0,scale:'.55'},{opacity:1,scale:'1.06',offset:.7},{opacity:1,scale:'1'}],{duration:620,delay:520+(k2++)*95,easing:'cubic-bezier(.3,1.1,.5,1)',fill:'both'})})});
  },1230);
  T(end,1230+1500+rest.length*140+Math.min(k2max(rest),10)*95);
  function k2max(r){var c=0;r.forEach(function(e){c+=e.querySelectorAll('.ilw').length});return c}
}

/* --- линии между островами: считаем по раскладке (offset*), а не по getBoundingClientRect,
       чтобы анимации появления (translate/scale) и переходы не сдвигали линии --- */
var LRO=null,LFT=0;
function lkX(el){var m=/translateX\((-?[\d.]+)px\)/.exec(el.style.transform||'');return m?+m[1]:0}
function links(){
  var ns='http://www.w3.org/2000/svg';
  app.querySelectorAll('.path').forEach(function(pa){
    var old=pa.querySelector('.cn');if(old)old.remove();
    var it=pa.querySelectorAll('.ilw'),i=pa.dataset.i;
    if(it.length<2)return;
    var pw=pa.offsetWidth,ph=pa.offsetHeight;pa.dataset.lsz=pw+'x'+ph;
    var sv=document.createElementNS(ns,'svg');sv.setAttribute('class','cn');sv.setAttribute('width',pw);sv.setAttribute('height',ph);
    var fresh=[];
    for(var j=0;j<it.length-1;j++){
      var a=it[j],b=it[j+1],bi=b.querySelector('.isl');
      var x1=a.offsetLeft+lkX(a)+a.offsetWidth/2,y1=a.offsetTop+a.offsetHeight-2;
      var x2=b.offsetLeft+lkX(b)+bi.offsetLeft+bi.offsetWidth/2,y2=b.offsetTop+bi.offsetTop+6,ym=(y1+y2)/2;
      var d='M'+x1+' '+y1+' C'+x1+' '+ym+' '+x2+' '+ym+' '+x2+' '+y2,key=i+'-'+j;
      var base=document.createElementNS(ns,'path');base.setAttribute('d',d);base.setAttribute('class','seg');sv.appendChild(base);
      if(S.d[key]&&isOpen(i,j+1)){var lp=document.createElementNS(ns,'path');lp.setAttribute('d',d);var tc=(bi.className.match(/ty-\w/)||[''])[0];lp.setAttribute('class','seg lit '+tc);sv.appendChild(lp);if(!LIT[key]){LIT[key]=1;fresh.push([lp,b])}}
    }
    if(!pa.dataset.lk)pa.dataset.lk=Date.now();
    if(pa.classList.contains('stg')&&!RM()){var el=(Date.now()-pa.dataset.lk)/1000,dl=.2+Math.min(it.length,8)*.05;if(el<dl+.6)sv.style.animation='cnin .6s ease '+(dl-el)+'s both'}
    pa.insertBefore(sv,pa.firstChild);
    fresh.forEach(function(f,n){
      var L=f[0].getTotalLength();f[0].style.strokeDasharray=L;f[0].style.strokeDashoffset=L;f[0].getBoundingClientRect();
      f[0].style.transition='stroke-dashoffset .9s ease-out '+(n*.9)+'s';f[0].style.strokeDashoffset=0;
      setTimeout(function(){f[1].classList.remove('wait')},900*(n+1)+100);
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
/* --- островки и главная --- */
function island(i,j,n){
  var k=i+'-'+j,it=IT(i,j),d=S.d[k],op=isOpen(i,j),c=cur()===k,nx=!c&&!d&&nxI(i,j),wt=j>0&&S.d[i+'-'+(j-1)]&&!LIT[i+'-'+(j-1)];
  var ty={theory:['t','📖','Теория'],flash:['f','✏️','Вопросы'],test:['c','💻','Код'],project:['p','🚀','Мини-проект'],ans:['a','🎓','Задание ЕГЭ']}[it.t],lb=it.n||'',off=[0,46,0,-46][j%4];
  return'<div class="ilw'+(wt?' wait':'')+'" style="--n:'+Math.min(n||0,9)+';transform:translateX('+off+'px)">'+(c&&!TOPICS[i].intro?'<div class="flag">🚩 Ты остановился здесь</div>':'')+'<button class="isl ty-'+ty[0]+' '+(d?'dn':(op?'op':'lk'))+(c?' cur':'')+(nx?' nx':'')+'" data-i="'+i+'" data-j="'+j+'" aria-label="'+esc(ty[2]+': '+lb)+(d?' (пройдено)':(op?'':' (закрыто)'))+'">'+PEN+'<span class="ic">'+ty[1]+'</span>'+(d?'<i class="bd ok">✓</i>':(op?'':'<i class="bd">🔒</i>'))+'</button><div class="mu">'+esc(lb)+(it.t==='project'?'<br><small>'+(S.at[k]==='skip'?'пропущен':'по желанию')+'</small>':'')+'</div></div>'}
function goalCard(all){
  var d=goalDone(),g=S.goal,p=Math.min(100,Math.round(d/g*100)),ok=d>=g,cu=cur(),left=g-d;
  return'<section class="gcard"><div class="gtx"><div class="gh">Привет, '+nk(S.nick)+'!</div><div class="gs">'+(all?'Ты прошёл всё. Кролик гордится тобой.':ok?'Цель дня выполнена.':'Сегодня: '+d+' из '+g+' '+(g===1?'островка':'островков')+'.')+'</div><div class="bar" aria-label="Цель дня"><i class="grow" style="width:'+p+'%"></i></div>'+(cu&&!all?'<button class="btn s" id="gc">'+(d?'Продолжить':'Начать')+'</button>':'')+'</div><div class="grb">'+rabbit(all?'happy':'eat')+'</div></section>'}
function home(){BACK=home;fzApply();
  var all=allDone();
  if(PE.length){show(head()+'<div class="fb bad"><b>Ошибка в данных тем</b>'+PE.map(esc).join('<br>')+'</div>','home');bindHead(home);return}
  var ex=S.mode==='ex',first=!ex&&TOPICS[0]&&TOPICS[0].intro&&S.start===0&&!tdone(0)&&!REV;
  var h=head()+(first?'':goalCard(all))+(ex?exBar():''),num=0;
  TOPICS.forEach(function(t,i){
    if(ex?!(t.ex&&t.ex===EXK):!!t.ex)return;if(!t.intro)num++;if(!vis(i))return;
    var c=0;(t.items||[]).forEach(function(x,j){if(S.d[i+'-'+j])c++});
    h+='<section class="topic'+(t.intro?' intro':'')+(REV&&!t.intro?' rv':'')+'">'+(t.intro?'<div class="ihead"><h2>'+esc(t.n)+'</h2><p class="mu">'+esc(t.s||'')+'</p></div>':'<div class="thead'+(tdone(i)?' done':'')+'" style="--tp:'+Math.round(c/Math.max(1,ni(i))*100)+'%"><div class="tn">'+num+'</div><div class="tt"><h2>'+esc(t.n)+'</h2><div class="mu">'+esc(t.s||'')+(i<S.start&&!tdone(i)?' · пропущено':'')+'</div></div><div class="tp">'+c+'/'+ni(i)+'</div></div>')+'<div class="path'+(RM()?'':' stg')+'" data-i="'+i+'">';
    for(var j=0;j<ni(i);j++)h+=island(i,j,j);
    h+='</div></section>'});
  if(ex)h+=exTail();
  show(h,'home');bindHead(home);links();exBind();
  app.querySelectorAll('.isl').forEach(function(b){b.onclick=function(){go(+b.dataset.i,+b.dataset.j)}});
  var c=app.querySelector('.cur');if(c&&!REV)c.scrollIntoView({block:'center'});
  var gc=$('gc');if(gc)gc.onclick=function(){var k=cur();if(!k)return;var p=k.split('-');BACK=home;go(+p[0],+p[1])};
  var gb=app.querySelector('.grb');if(gb){gb.onclick=function(){var t=app.querySelector('.isl.cur')||app.querySelector('.isl.nx');if(t)t.scrollIntoView({block:'center',behavior:RM()?'auto':'smooth'})}}
}
/* --- приветствие и повторение после перерыва --- */
function greet(){
  var t=day(new Date());fzApply();
  if(S.seen===t)return home();
  var away=S.seen?dnum(t)-dnum(S.seen):0;S.seen=t;save();
  show('<div class="center">'+rabbit('eat')+'<h2>Привет, '+nk(S.nick)+'!</h2><p>'+(away>=3?'Тебя не было '+away+' '+pl(away,['день','дня','дней'])+'. Кролик скучал.':'Кролик завтракает и ждёт тебя.')+'</p><button class="btn pulse" id="go">Начать</button></div>');
  $('go').onclick=function(){home();if(away>=3)setTimeout(function(){repeatAsk(away)},400)};
}
function passed(type){var a=[];TOPICS.forEach(function(t,i){(t.items||[]).forEach(function(x,j){if(x.t===type&&S.d[i+'-'+j])a.push([i,j])})});return a}
function repeatAsk(away){
  if(!ST('rep')||S.rp===day(new Date())||!passed('flash').length)return;
  modal('<h2>Давно не виделись</h2><p>Ты не заходил '+away+' '+pl(away,['день','дня','дней'])+'. Давай быстро повторим 3 вопроса из пройденного?</p><p class="mu">Опыт за это не начисляется, это просто разминка.</p>',[['Давай',function(){S.rp=day(new Date());save();repeat3()}],['Позже',function(){S.rp=day(new Date());save()},1]])}
/* --- практика --- */
function row(ic,t,sub,a,dis,rt){return'<button class="li" data-a="'+a+'"'+(dis?' disabled':'')+'><span class="lic">'+ic+'</span><span class="lt">'+t+'<small>'+sub+'</small></span>'+(rt?'<span class="lv">'+rt+'</span>':'<span class="ch">›</span>')+'</button>'}
function practice(){BACK=practice;
  var nf=passed('flash').length,nt=passed('test').length;
  show(head('Практика')+'<p class="mu" style="margin:0 0 14px">Тренировки без опыта: прогресс и серия не меняются. Задания берутся из пройденных островков.</p><div class="lst">'+row('🎲','Случайный вопрос','Бесконечный режим, пока не закроешь','rf',false,nf?'':'нужен островок')+row('💻','Случайный код','Задание из пройденных, без опыта','rc',false,nt?'':'нужен островок')+row('🎓','Тренажёр ЕГЭ','Бесконечные задания по ЕГЭ, без опыта','re',false,'')+row('🔁','Повторить 3 вопроса','Быстрая разминка по пройденному','r3',false,nf?'':'нужен островок')+'</div>','pr');
  bindHead(practice);
  app.querySelectorAll('.li').forEach(function(b){b.onclick=function(){({rf:rndFlash,rc:rndCode,r3:repeat3,re:function(){EXDASH=0;exMenu()}})[b.dataset.a]()}})}
function oge(){practice()}
function askQ(q,o){
  var sel=-1,ch=false,right=false,ord=q.o.map(function(x,n){return n}).sort(function(){return Math.random()-.5});
  var h='<div class="top"><button class="icon" id="x" aria-label="Выйти">✕</button>'+o.mid+'<span></span></div><div class="q">'+esc(q.q)+'</div>'+(q.v||'')+(q.c?'<pre>'+hl(q.c)+'</pre>':'');
  ord.forEach(function(k){h+='<button class="opt" data-k="'+k+'">'+esc(q.o[k])+'</button>'});
  show(h+'<div id="fb"></div><button class="btn" id="go" disabled>Проверить</button>');if(q.v&&window.exImgs)exImgs(app);
  $('x').onclick=o.exit;
  var g=$('go'),os=app.querySelectorAll('.opt'),fb=$('fb');
  os.forEach(function(b){b.onclick=function(){if(ch)return;sel=+b.dataset.k;os.forEach(function(x){x.classList.remove('sel')});b.classList.add('sel');g.disabled=false;snd('click')}});
  g.onclick=function(){
    if(ch){o.next();return}
    ch=true;right=sel===q.a;fx(right);
    os.forEach(function(x){var k=+x.dataset.k;x.disabled=true;if(k===q.a)x.classList.add('ok');else if(k===sel)x.classList.add('no')});
    fb.innerHTML='<div class="fb'+(right?'':' bad')+'"><b>'+(right?'Верно!':'Неверно')+'</b>'+esc(q.e||'')+xm(q)+'</div>';
    g.textContent=o.last&&o.last()?'Закончить':'Дальше';o.done(right);g.classList.add('pulse')}}
var RND={r:0,t:0,last:null};
function rndWarn(go){if(S.rnd)return go();modal('<h2>Бесконечный режим</h2><p>Задания идут одно за другим, пока ты сам не закроешь режим крестиком. Опыт здесь не начисляется, прогресс не меняется.</p>',[['Понятно',function(){S.rnd=1;save();go()}],['Отмена',null,1]])}
function allFlashQ(){var a=[];passed('flash').forEach(function(p){IT(p[0],p[1]).q.forEach(function(q,n){a.push({q:q,k:p[0]+'-'+p[1]+'-'+n})})});return a}
function rndFlash(){
  if(!passed('flash').length){toast('Сначала пройди хотя бы один островок');return}
  rndWarn(function(){RND.r=0;RND.t=0;RND.last=null;rfNext()})}
function rfNext(){
  var P=allFlashQ();if(!P.length){practice();return}
  var x;do{x=P[Math.floor(Math.random()*P.length)]}while(P.length>1&&x.k===RND.last);RND.last=x.k;
  askQ(x.q,{mid:'<span class="chip s">🎲 '+RND.r+' из '+RND.t+'</span>',exit:practice,next:rfNext,done:function(r){RND.t++;if(r){RND.r++;rcInc()}}})}
function repeat3(){
  var P=allFlashQ();if(!P.length){toast('Сначала пройди хотя бы один островок');return}
  P.sort(function(){return Math.random()-.5});var Q=P.slice(0,3),st=Q.map(function(){return 0}),n=0,ok=0;
  function step(){
    if(n>=Q.length){
      show('<div class="center">'+rabbit(ok===Q.length?'happy':'eat')+'<h2>Повторено: '+ok+' из '+Q.length+'</h2><p>'+(ok===Q.length?'Всё помнишь. Отлично.':'Ничего страшного, это просто разминка.')+'</p><button class="btn pulse" id="go">Готово</button><button class="btn g" id="rp">Ещё раз</button></div>');
      $('go').onclick=home;$('rp').onclick=repeat3;if(ok===Q.length){snd('chord');ach('rep1')}return}
    askQ(Q[n].q,{mid:'<div class="sbar">'+st.map(function(v){return'<i class="'+(v===1?'ok':v===2?'bad':'')+'"></i>'}).join('')+'</div>',exit:home,last:function(){return n===Q.length-1},next:function(){n++;step()},done:function(r){st[n]=r?1:2;if(r)ok++;var sb=app.querySelector('.sbar');if(sb)sb.innerHTML=st.map(function(v){return'<i class="'+(v===1?'ok':v===2?'bad':'')+'"></i>'}).join('')}})}
  step()}
function rndCode(){
  if(!passed('test').length){toast('Сначала пройди хотя бы один островок');return}
  rndWarn(function(){RND.last=null;rcNext()})}
function rcNext(){
  var P=passed('test'),T=[];P.forEach(function(p){IT(p[0],p[1]).tasks.forEach(function(q,n){T.push({q:q,k:p[0]+'-'+p[1]+'-'+n})})});
  if(!T.length){practice();return}
  var x;do{x=T[Math.floor(Math.random()*T.length)]}while(T.length>1&&x.k===RND.last);RND.last=x.k;var q=x.q;
  show('<div class="top"><button class="icon" id="x" aria-label="Выйти">✕</button><span class="chip s">🎲 Случайный код</span><span></span></div><h2 style="font-size:1.25rem">'+esc(q.q)+'</h2>'+(q.strict?'<pre class="cmp">'+esc(q.ex||'')+'</pre>':'<p class="mu" style="margin:0 0 12px">'+esc(q.ex||'').replace(/\n/g,'<br>')+'</p>')+edHtml('# Пиши код здесь\n')+(q.h?'<button class="btn g" id="hb" style="margin:0 0 10px">💡 Подсказка</button><div id="hint"></div>':'')+'<div class="row"><button class="btn g" id="run">Запустить</button><button class="btn" id="chk">Проверить</button></div><pre class="out" id="o" style="margin-top:14px;display:none"></pre>'+IOHTML+'<div id="fb"></div>');
  $('x').onclick=practice;
  var c=$('code'),sync=initEd(c,function(){});sync();
  if(q.h)$('hb').onclick=function(){$('hint').innerHTML='<div class="fb"><b>Подсказка</b>'+esc(q.h).replace(/\n/g,'<br>')+'</div>'};
  skReady();chkPulse();
  $('run').onclick=function(){var o=$('o');if(!SKOK){o.style.display='block';o.textContent='Загружаю среду Python…'}needSk().then(function(ok){if(ok)liveRun(c.value)})};
  $('chk').onclick=async function(){
    if(!SKOK)$('fb').innerHTML='<div class="fb"><b>Загружаю среду Python…</b></div>';
    if(!(await needSk()))return;
    var b=$('chk');b.disabled=true;var v=await judge(q,c.value);
    if(!v.ok){fx(false);b.disabled=false;$('fb').innerHTML=v.h;return}
    fx(true,'test');rcInc();
    $('fb').innerHTML='<div class="fb"><b>Все тесты пройдены!</b>Опыт не начисляется, это тренировка.</div><button class="btn pulse" id="nx">Ещё одно задание</button>'+(q.sol?'<button class="btn g" id="sl">👀 Посмотреть, как задумано</button>':'');
    $('nx').onclick=rcNext;if(q.sol)$('sl').onclick=function(){solModal(q.sol)}}}
function chkPulse(){var c=$('code'),b=$('chk');if(!c||!b)return;function u(){var v=c.value.trim();b.classList.toggle('pulse',v!==''&&v!=='# Пиши код здесь')}u();c.addEventListener('input',u)}
function xpStrip(){var L=lvlInfo(S.xp);return'<div class="xps"><div class="xph"><b>Уровень '+L.l+'</b><span class="mu">ещё '+L.left+' ⭐</span></div><div class="bar" style="height:12px"><i class="grow" style="width:'+L.p+'%"></i></div></div>'}
/* --- достижения-дискеты --- */
function hsh(s){var h=0;for(var i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))|0;return Math.abs(h)}
function fdate(d){var p=d.split('-');return(+p[2])+' '+MON[+p[1]-1]+' '+p[0]}
function floppyFace(a){return'<div class="fface" style="--fc:'+a.c+'"><div class="fsh"><i></i></div><div class="flb"><div class="fe">'+a.e+'</div><div class="fn">'+esc(a.n)+'</div></div></div>'}
function floppyBtn(a){return'<button class="fd" data-id="'+a.id+'" style="--fc:'+a.c+';--lean:'+((hsh(a.id)%5)-2)*1.4+'deg" aria-label="'+esc(a.n)+'"><span class="fb3"><span class="ff"><span class="fm"></span><span class="fl"><em>'+a.e+'</em></span></span><span class="fsx"><span class="fsn"></span><em>'+a.e+'</em></span><span class="fbk"></span></span><i class="fsd"></i></button>'}
function shelf(){
  var L=ACH.filter(function(a){return S.ach[a.id]}).sort(function(a,b){return S.ach[a.id]<S.ach[b.id]?-1:S.ach[a.id]>S.ach[b.id]?1:0}),hz=ST('sh')==='h',per=Math.max(4,Math.min(10,Math.floor((Math.min(innerWidth,620)-70)/(ST('fl')==='flat'?22:44))));
  var h='<div class="card shelfc"><div class="sh-h"><b>Достижения</b><span class="mu">Получено: '+L.length+'</span></div>';
  if(!L.length)return h+'<div class="shrow"></div><p class="mu" style="margin:8px 0 0">Здесь будут появляться дискеты за твои успехи.</p></div>';
  if(hz)h+='<div class="shrow hs" tabindex="0" aria-label="Полка с дискетами">'+L.map(floppyBtn).join('')+'</div>';
  else for(var r=0;r<L.length;r+=per){h+='<div class="shrow">'+L.slice(r,r+per).map(floppyBtn).join('')+'</div>'}
  return h+'</div>'}
function fdOpen(btn){
  var a=achDef(btn.dataset.id);if(!a||btn.dataset.busy)return;btn.dataset.busy=1;
  snd('disk');vib(12);
  var an=RM()?null:btn.animate([{transform:'translateY(0)'},{transform:'translateY(-30px) rotate(-3deg)'}],{duration:260,easing:'cubic-bezier(.2,.9,.3,1.2)',fill:'forwards'});
  setTimeout(function(){
    var m=modal('<div class="fwin">'+floppyFace(a)+'<h2>'+esc(a.n)+'</h2><p class="fd2">'+esc(a.d)+'</p><p class="mu">Получено: '+fdate(S.ach[a.id])+'</p></div>',[['Закрыть',null,1]]);
    new MutationObserver(function(x,o){if(!document.body.contains(m)){o.disconnect();if(an)an.cancel();delete btn.dataset.busy}}).observe(document.body,{childList:true});
  },RM()?0:230)}
/* --- профиль --- */
function profile(){BACK=profile;
  var n=ND(),pct=Math.round(n/NT()*100),LV=lvlInfo(S.xp),d=goalDone(),g=S.goal,gp=Math.min(100,Math.round(d/g*100)),f=S.fz;
  var rows=TOPICS.map(function(t,i){var c=0,l=[];(t.items||[]).forEach(function(x,j){var e=S.es[i+'-'+j]||0;c+=e;if(e>0)l.push({j:j,n:x.n,e:e,ic:x.t==='flash'?'✏️':x.t==='test'?'💻':x.t==='ans'?'🎓':'🚀'})});return{i:i,n:t.n,c:c,l:l}}).filter(function(r){return r.c>0}).sort(function(a,b){return b.c-a.c}),mx=rows.length?rows[0].c:1;
  show(head('Профиль')+
   '<div class="hero"><div class="pav" id="pr" role="button" tabindex="0" aria-label="Погладить кролика">'+rabbit('lie')+'</div><div class="hn"><b class="nmx">'+nk(S.nick)+'</b><div class="lvp"><span class="pill">Уровень '+LV.l+'</span><span class="mu">до '+(LV.l+1)+': ещё '+LV.left+' ⭐</span></div><div class="bar"><i class="grow" style="width:'+LV.p+'%"></i></div></div></div>'+
   '<div class="tiles"><div class="tile"><span>🥕</span><b>'+streakNow()+'</b><small>серия</small></div><div class="tile"><span>🏆</span><b>'+Math.max(S.max,streakNow())+'</b><small>рекорд</small></div><div class="tile"><span>⭐</span><b>'+S.xp+'</b><small>опыта</small></div></div>'+
   '<div class="card"><div class="ch2"><b>Цель дня</b><span class="mu">выполнено '+Math.min(d,g)+' из '+g+(d>g?' (+'+(d-g)+' сверх цели)':'')+'</span></div><div class="bar" style="margin:10px 0 12px"><i class="grow" style="width:'+gp+'%"></i></div>'+weekRow('g')+'<p class="mu" style="margin:8px 0 0;font-size:.82rem">Выполни цель в 5 днях недели и получи бонус +50 ⭐ (сейчас '+wkCount()+' из 5). Сколько островков в день, можно выбрать в настройках.</p></div>'+
   '<div class="card"><div class="ch2"><b>Заморозки серии</b><span class="mu">'+f.n+' из 2</span></div><div class="fzr" style="margin-top:8px"><div class="fzi">'+[0,1].map(function(i){return'<span class="fzs'+(i<f.n?' on':'')+'">❄️</span>'}).join('')+'</div><div class="fzt"><span class="mu">'+(f.n>=2?'У тебя максимум. Заморозка тратится сама, если пропустишь день.':'До новой: ещё '+(15-f.p)+' '+pl(15-f.p,['островок','островка','островков'])+'.')+'</span></div></div></div>'+
   shelf()+
   '<div class="card"><div class="ch2"><b>Пройдено тем</b><span class="mu">'+n+' из '+NT()+' · '+pct+'%</span></div><div class="bar" style="margin-top:10px"><i class="grow" style="width:'+pct+'%"></i></div></div>'+
   '<div class="card"><b>Активность</b><div style="margin-top:10px">'+calHtml()+'</div></div>'+
   '<div class="card"><b>Где ты чаще ошибаешься</b>'+(rows.length?rows.map(function(r){return'<div class="erow"><span>'+esc(r.n)+'</span><div class="bar"><i style="width:'+Math.round(r.c/mx*100)+'%"></i></div><b>'+r.c+'</b></div><div class="elist">'+r.l.map(function(x){return'<button class="elink" data-i="'+r.i+'" data-j="'+x.j+'"><span class="et">'+x.ic+' '+esc(x.n)+'<small>ошибок: '+x.e+'</small></span><span class="eg">Отработать →</span></button>'}).join('')+'</div>'}).join('')+'<p class="mu" style="margin:6px 0 0;font-size:.85rem">Нажми на островок, чтобы отработать ошибки. Пройдёшь без ошибок, и он пропадёт из списка.</p>':'<p style="margin:8px 0 0">Пока ты справляешься отлично 👍</p>')+'</div>'+
   '<div class="lst">'+row('📖','Изученные функции','Твой словарь с заметками','dc')+(TOPICS[0]&&TOPICS[0].intro&&!S.d['0-0']?row('🏝️','Знакомство с ИТП','Вводная теория','intr'):'')+row('📤','Поделиться прогрессом','Картинка со статистикой','sh')+row('⚙️','Настройки','Внешний вид, звук, обучение, данные','st')+'</div>'+
   '<p class="mu" style="text-align:center;margin-top:18px"><span class="ver" id="vr" tabindex="0" aria-label="ИТП v5.1.3. ИТП означает: И так Пайтон">ИТП v5.1.3<span class="vt" role="tooltip">ИТП означает «И так Пайтон»</span></span></p>','prof');
  bindHead(profile);calBind();
  var vr=$('vr'),vt;vr.onclick=function(){vr.classList.add('on');clearTimeout(vt);vt=setTimeout(function(){vr.classList.remove('on')},2500)};
  var pr=$('pr'),tm,hc=0;
  function love(){var rw=pr.firstChild;rw.classList.add('love');snd([659,784]);var hr=document.createElement('i');hr.className='hrt';hr.textContent='💗';hr.style.left=(30+Math.random()*40)+'%';pr.appendChild(hr);setTimeout(function(){hr.remove()},1300);clearTimeout(tm);tm=setTimeout(function(){rw.classList.remove('love')},1400)}
  pr.onclick=love;pr.onkeydown=function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();love()}};
  app.querySelectorAll('.fd').forEach(function(b){b.onclick=function(){fdOpen(b)}});
  app.querySelectorAll('.lst .li').forEach(function(b){b.onclick=function(){var a=b.dataset.a;if(a==='dc')dict();else if(a==='sh')share();else if(a==='intr'){BACK=profile;theory(0,0)}else if(a==='st'){SBACK=profile;settings()}}});
  app.querySelectorAll('.elink').forEach(function(b){b.onclick=function(){BACK=profile;go(+b.dataset.i,+b.dataset.j)}});
}
/* --- настройки --- */
function SW(k,on){return'<button class="sw" role="switch" aria-checked="'+(on?'true':'false')+'" data-k="'+k+'"></button>'}
function SG(k,opts,cur){return'<div class="segc">'+opts.map(function(o){return'<button data-k="'+k+'" data-v="'+o[0]+'" class="'+(String(cur)===String(o[0])?'on':'')+'">'+o[1]+'</button>'}).join('')+'</div>'}
function SR(ic,t,sub,ctl,a){var blk=ctl&&/segc|swa|type="range"/.test(ctl);return(a?'<button class="li" data-a="'+a+'">':'<div class="li static'+(blk?' blk':'')+'">')+'<span class="lic">'+ic+'</span><span class="lt">'+t+(sub?'<small>'+sub+'</small>':'')+'</span>'+(ctl||'<span class="ch">›</span>')+(a?'</button>':'</div>')}
function setSet(k,v){
  if(k==='theme'){themeFx();S.theme=v}else if(k==='mute'){S.mute=v?0:1}else if(k==='goal'){S.goal=+v}else if(k==='g'){S.g=v}else if(k==='hc'){S.hc=v?0:1}
  else{S.set[k]=(typeof v==='number'||typeof v==='boolean')?v:(/^\d+$/.test(v)?+v:v)}
  save();applyPrefs();
  if(k==='emo'){if(ST('emo')){emoLoad();if(EM.map)emoOn()}else emoOff()}
  if(k==='goal')goalCheck()}
function settings(){
  var y=window.scrollY,S2=S.set;
  var h='<div class="top"><button class="icon" id="x" aria-label="Назад">←</button><h1>Настройки</h1><span></span></div>';
  h+='<div class="sec">Внешний вид</div><div class="lst">'+
   SR('🎨','Тема','',SG('theme',[['','Авто'],['light','Светлая'],['dark','Тёмная']],S.theme))+
   SR('🖌️','Цвет акцента','Кнопки, полоски, выделение','<div class="swa" role="group" aria-label="Цвет акцента">'+[['','#46A32F'],['carrot','#F28A12'],['pink','#E8557A'],['blue','#2F7BEF'],['violet','#7B5CE6']].map(function(c){return'<button data-k="acc" data-v="'+c[0]+'" style="background:'+c[1]+'" class="'+(ST('acc')===c[0]?'on':'')+'" aria-label="'+(c[0]||'green')+'"></button>'}).join('')+'</div>')+
   SR('🔤','Размер текста','',SG('tz',[[90,'Мелкий'],[100,'Обычный'],[115,'Крупный'],[130,'Огромный']],ST('tz')))+
   SR('✨','Анимации','Выкл — для слабых устройств и тех, кого они отвлекают',SG('anim',[['full','Все'],['less','Меньше'],['off','Выкл']],ST('anim')))+
   SR('🗄️','Полка достижений','Когда дискет станет много',''+SG('sh',[['v','Вторая полка ниже'],['h','Листать вбок']],ST('sh'))+'')+
   SR('💾','Вид дискет','Как они стоят на полке',''+SG('fl',[['tilt','Объёмные'],['flat','Плоские']],ST('fl'))+'')+
   SR('😀','Смайлики Windows 11','Встроенные, одинаковые на всех устройствах',SW('emo',ST('emo')))+
   SR('🎉','Конфетти','Салют при завершении темы',SW('gc',ST('gc')))+'</div>';
  h+='<div class="sec">Звук и отклик</div><div class="lst">'+
   SR('🔊','Звук','Главный выключатель всех звуков',SW('mute',!S.mute))+
   SR('🎚️','Громкость','','<input type="range" min="0" max="100" step="5" value="'+ST('vol')+'" id="vol" aria-label="Громкость">')+
   SR('👆','Звуки нажатий','Тихий щелчок по кнопкам',SW('sfx',ST('sfx')))+
   SR('📳','Вибрация','На телефоне при ошибке и успехе',SW('vib',ST('vib')))+'</div>';
  h+='<div class="sec">Обучение</div><div class="lst">'+
   SR('🎯','Цель дня','Сколько островков в день',SG('goal',[[1,'1'],[2,'2'],[3,'3']],S.goal))+
   SR('⌨️','Печатать теорию по буквам','Выкл — текст появится сразу',SW('ty',ST('ty')))+
   SR('📑','Оглавление теории','Слева на широких экранах',SW('toc',ST('toc')))+
   SR('🔁','Повторение после перерыва','Предложить 3 вопроса, если не заходил 3+ дня',SW('rep',ST('rep')))+
   SR('💡','Спрашивать про подсказку','Предупреждение, что опыт будет вдвое меньше',SW('hc',!S.hc))+'</div>';
  h+='<div class="sec">Редактор кода</div><div class="lst">'+
   SR('🔠','Размер кода','',SG('cf',[[13,'S'],[15,'M'],[17,'L'],[19,'XL']],ST('cf')))+
   SR('🔢','Номера строк','',SW('ln',ST('ln')))+
   SR('🧩','Автозакрытие скобок и кавычек','',SW('ac',ST('ac')))+'</div>';
  h+='<div class="sec">Профиль и данные</div><div class="lst">'+
   SR('🐰','Никнейм',esc(S.nick),'','nick')+
   SR('🙂','Обращение','Для правильных окончаний в тексте',SG('g',[['m','Парень'],['f','Девушка'],['','Не указывать']],S.g||''))+
   SR('💾','Резервная копия','Сохранить или загрузить прогресс','','bk')+
   SR('🧹','Сбросить оформление','Вернуть настройки внешнего вида и звука','','rs1')+
   SR('🗑️','Сбросить прогресс','Удалит всё, кроме сохранённых кодов','','rs2')+'</div>';
  h+='<div class="sec">О приложении</div><div class="lst">'+(KBD?SR('⌨️','Горячие клавиши','','','kb'):'')+SR('📖','Прочитать введение','Знакомство с ИТП ещё раз','','intro')+SR('🐇','ИТП v5.1.3','«И так Пайтон»','<span class="lv" id="egv">5.1.3</span>')+'</div><div style="height:20px"></div>';
  show(h,'prof');HRE=settings;
  $('x').onclick=function(){(SBACK||profile)()};
  function again(){var yy=window.scrollY;settings();window.scrollTo(0,yy)}
  app.querySelectorAll('.sw').forEach(function(b){b.onclick=function(){var on=b.getAttribute('aria-checked')!=='true';var k=b.dataset.k;b.setAttribute('aria-checked',on?'true':'false');setSet(k,on?1:0);if(k==='sfx'||k==='mute')snd('click')}});
  app.querySelectorAll('.segc button,.swa button').forEach(function(b){b.onclick=function(){var g=b.parentNode;g.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b)});setSet(b.dataset.k,b.dataset.v);snd('click');if(g.classList.contains('segc'))segPos(g,true)}});
  eggBind();
  var v=$('vol');v.oninput=function(){S.set.vol=+v.value;save()};v.onchange=function(){snd('ok')};
  app.querySelectorAll('.lst button.li').forEach(function(b){b.onclick=function(){var a=b.dataset.a;
    if(a==='nick')askName('Никнейм',S.nick,function(n){n=Array.from(n).slice(0,16).join('');S.nick=n;save();again();toast('Никнейм изменён')});
    else if(a==='bk')backup();
    else if(a==='kb')keys();
    else if(a==='intro'){BACK=function(){settings()};theory(0,0)}
    else if(a==='rs1')modal('<h2>Сбросить оформление?</h2><p>Тема, цвет, размер текста, звук и остальные настройки вернутся к начальным. Прогресс не изменится.</p>',[['Сбросить',function(){S.set=clean({}).set;S.theme='';S.mute=0;save();applyPrefs();emoLoad();again();toast('Настройки сброшены')}],['Отмена',null,1]]);
    else if(a==='rs2')modal('<h2>Сбросить весь прогресс?</h2><p>Опыт, серия, пройденные острова и достижения будут удалены. Сохранённые коды и настройки останутся. Это нельзя отменить.</p>',[['Да, сбросить',function(){S=clean({theme:S.theme,mute:S.mute,sv:S.sv,ec:S.ec,cur:S.cur,set:S.set,nick:''});seedLit();save();nick()}],['Отмена',null,1]])}});
}
/* --- оглавление теории (экспериментально) --- */
var TOCS=null;
function tocKill(){var o=document.getElementById('toc');if(o)o.remove();if(TOCS){window.removeEventListener('scroll',TOCS);TOCS=null}}
function tocBuild(){
  tocKill();if(!ST('toc'))return;var tb=$('tb');if(!tb)return;
  var hs=[].slice.call(tb.querySelectorAll('h3'));if(hs.length<4)return;
  var a=document.createElement('aside');a.id='toc';a.setAttribute('aria-label','Оглавление');
  a.innerHTML='<div class="tct">Оглавление</div>'+hs.map(function(h,k){h.id='tcs'+k;return'<button data-k="'+k+'">'+esc(h.textContent)+'</button>'}).join('');
  document.body.appendChild(a);
  var bs=[].slice.call(a.querySelectorAll('button'));
  bs.forEach(function(b){b.onclick=function(){tb.click();hs[+b.dataset.k].scrollIntoView({behavior:RM()?'auto':'smooth',block:'start'})}});
  function spy(){var y=innerHeight*.32,c=-1;hs.forEach(function(h,k){if(h.offsetParent&&h.getBoundingClientRect().top<y)c=k});bs.forEach(function(b,k){b.classList.toggle('on',k===c)})}
  TOCS=spy;window.addEventListener('scroll',spy,{passive:true});setTimeout(spy,50)}

var LSK=null,LXP=null;
function chipFx(){
  var hs=$('hs'),hx=$('hx');if(!hs||!hx)return;
  var s=streakNow(),x=S.xp;
  if(LSK!==null&&s>LSK&&!RM())hs.animate([{transform:'scale(1)'},{transform:'scale(1.25) rotate(-4deg)'},{transform:'scale(1)'}],{duration:520,easing:'cubic-bezier(.3,1.6,.5,1)'});
  if(LXP!==null&&x>LXP){
    var el=hx.querySelector('span:last-child'),a=LXP,t0=performance.now();
    if(RM())el.textContent=x;else{hx.animate([{transform:'scale(1)'},{transform:'scale(1.18)'},{transform:'scale(1)'}],{duration:600});
    (function st(t){var k=Math.min(1,(t-t0)/700);el.textContent=Math.round(a+(x-a)*k);if(k<1)requestAnimationFrame(st)})(t0)}}
  LSK=s;LXP=x}
