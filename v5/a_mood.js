/* ===== dev.36: новые спрайты кролика (владелец). Обёртки над готовыми функциями, как в a_img.js:
   • sleep — ночью, в часы «Ночной совы» (23:00–3:59): в профиле всегда, на карточке «Поделиться» — в 40 % случаев;
   • angry — приветствие дня, когда прервалась серия (плачет теперь, если просто не было 3–6 дней);
   • wink — обычное приветствие дня, когда серия идёт, примерно каждый третий раз;
   • back — не было 7+ дней: при входе кролик сидит спиной и говорит короткий жутковатый монолог, потом оборачивается. */
function NIGHT(){var h=new Date().getHours();return h>=23||h<4}
rabKey=(function(f){return function(){return NIGHT()&&IMG.sleep&&Math.random()<.4?'sleep':f()}})(rabKey);

/* монологи: {d} — сколько дней не было; последняя строка — уже лицом к ученику */
function BKL(){return[
  ['…','{d}.','Я считал каждый.','Сидел тут, на Пути. Островки остывали один за другим.','Морковка кончилась на второй день. Я не жаловался.','Где ты пропадал'+G('','а','(а)')+'?','Нет. Не отвечай.','Главное — ты снова здесь. Пойдём.'],
  ['Тише.','Слышишь? Здесь было очень тихо. {d} подряд.','Курсор мигал в пустом редакторе. Мигал. Мигал.','Я пробовал писать код сам. Лапами неудобно.','Ты ведь не уйдёшь снова?','Ладно. Я не обижаюсь. Почти.'],
  ['А.','Это ты.','Я уже думал, что меня удалили.','{d}. Я переставил все островки, потом поставил обратно. Ты не заметишь.','Python без тебя забыл, где у него отступы.','Шучу. Ну что, продолжим?'],
  ['Не оборачивайся.','То есть… это я не оборачиваюсь. Ты-то как раз вернул'+G('ся','ась','ся')+'.','{d} без тебя. Я разговаривал с print(). Он отвечал.','Только то, что я сам ему говорил.','Это было грустно.','Ну всё. Хватит. Я рад тебя видеть.']]}
function backTalk(away,done){
  var B=BKL(),L=B[Math.floor(Math.random()*B.length)].map(function(s){return s.replace('{d}',away+' '+pl(away,['день','дня','дней']))});
  var o=document.createElement('div');o.className='bkt'+(RM()?' rm':'');o.setAttribute('role','dialog');o.setAttribute('aria-modal','true');o.setAttribute('aria-label','Кролик ждал тебя');
  /* экран не пустой (владелец): сверху — сколько дней не было, за кроликом — тусклый дождь символов, как во вступлении */
  o.innerHTML='<canvas class="bkrain" aria-hidden="true"></canvas><div class="bkd" aria-hidden="true"><b>'+away+'</b><span>'+pl(away,['день','дня','дней'])+' без тебя</span></div><div class="bkr"><img src="'+IMG.back+'" alt="" draggable="false"></div><div class="bkl" aria-live="polite"></div><button class="btn bkn" type="button">Дальше</button>';
  document.body.appendChild(o);var RN=typeof rainStart==='function'?rainStart(o.querySelector('.bkrain')):null;
  var box=o.querySelector('.bkl'),btn=o.querySelector('.bkn'),im=o.querySelector('img'),i=0,tm=0,end=false;
  function line(){clearTimeout(tm);if(i>=L.length)return;
    box.querySelectorAll('p.on').forEach(function(p){p.classList.add('old')});
    var p=document.createElement('p');p.textContent=L[i++];box.appendChild(p);requestAnimationFrame(function(){p.classList.add('on')});
    if(i===L.length){end=true;btn.textContent='Я здесь';
      o.querySelector('.bkr').classList.add('turn');setTimeout(function(){im.src=IMG.wink||IMG.eat},RM()?0:250)}
    else tm=setTimeout(line,RM()?2600:1900)}
  function close(){clearTimeout(tm);if(RN)RN.stop();o.classList.add('out');setTimeout(function(){o.remove();if(done)done()},RM()?0:300)}
  btn.onclick=function(){if(end)close();else line()};
  setTimeout(line,RM()?0:900);btn.focus({preventScroll:true})}

(function(){
  var g0=greet;greet=function(){
    var t=day(new Date()),fresh=S.seen!==t,away=0,lost=false;
    try{away=S.seen?dnum(t)-dnum(S.seen):0;lost=S.streak>=2&&streakNow()===0}catch(e){}
    var r=g0.apply(this,arguments);
    if(!fresh)return r;
    var w=app.querySelector('.gr .rw.im');
    function set(k){if(w&&IMG[k]){w.className='rw im '+k;w.querySelector('img').src=IMG[k]}}
    if(lost&&away<7)set('angry');
    else if(away<3&&streakNow()>=1&&Math.random()<1/3)set('wink');
    if(away>=7&&IMG.back)backTalk(away);
    return r};
})();

/* angryhead — пятая неудача подряд в одном задании (первая — хмурый, третья — плачет): кролик злится, но по-доброму */
(function(){
  var ANL=['Кролик злится 💢 Не на тебя — на эту задачу.','Пятый раз! Кролик топнул лапой. Открой подсказку.','Кролик сердито сопит. Перечитай условие по одной фразе.','Всё, кролик рассердился. Сделай паузу и вернись — так часто находится ответ.'],ANI=Math.floor(Math.random()*4);
  var e0=errMood;errMood=function(n){return n===5&&IMG.angryhead?'angryhead':e0(n)};
  var m0=moodLine;moodLine=function(k){return k==='angryhead'?ANL[ANI++%ANL.length]:m0(k)};
})();

/* пришёл с 6.x (from6 в a_core.js): один раз объяснить, что курс новый, а личное сохранено */
(function(){var g0=greet;greet=function(){var r=g0.apply(this,arguments);
  try{if(appGet().from6===1){appSet({from6:2});setTimeout(function(){modal('<h2>ИТП 7.0</h2><p>Курс собран заново: '+(TOPICS.length-1)+' '+pl(TOPICS.length-1,['тема','темы','тем'])+', новые задачи, проекты и кроличьи норы. Старые островки в него не переносятся, поэтому Путь начинается сначала — знакомые темы можно быстро пройти.</p><p>Опыт, уровень, серия, заморозки, календарь, достижения и сохранённые коды — на месте.</p>',[['Понятно',null,1]])},500)}}catch(e){}
  return r}})();
