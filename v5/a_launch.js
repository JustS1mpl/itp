/* заставка при запуске приложения на телефоне (владелец, 7.1.0): вместо того чтобы сразу показывать островки — секунда
   по кадрам, которые прислал владелец: мордочка ИТП на её фоне (продолжение системной заставки), мордочка тает,
   проявляется надпись «ИТП» цветом акцента из настроек (картинка-маска, залитая --accent), и весь экран мягко растворяется в Путь (около 1,7 с).
   Только в APK (NATIVE==='android'), только у тех, кто уже прошёл вступление (у новых есть своя заставка), и не при
   «меньше анимаций». Касание — сразу дальше. Для проверки в браузере: адрес с ?launch
   7.1.1: на телефонах шла рывками в пару кадров — шаги запускались таймерами JS, а при запуске главный поток занят.
   Теперь вся последовательность — CSS-анимации (v6.css, .lnch): идут на композиторе. JS только ждёт, пока картинки
   декодируются (не дольше 400 мс) и пока освободится главный поток, снимает паузу и убирает заставку в конце. */
(function(){
  /* и на iPhone/iPad, когда ИТП запущен с экрана «Домой» (STANDALONE, a_web.js) — это тоже «приложение на телефоне» */
  var want=NATIVE==='android'||STANDALONE||/[?&]launch\b/.test(location.search);
  if(!want||!IMG.logo||RM()||!S||!S.nick)return;
  var o=document.createElement('div'),gone=0;o.className='lnch wait';o.setAttribute('aria-hidden','true');
  o.innerHTML='<img class="lnl" alt="" decoding="sync" src="'+IMG.logo+'">'+(IMG.wordmark?'<i class="lnw" style="-webkit-mask-image:url('+IMG.wordmark+');mask-image:url('+IMG.wordmark+')"></i>':'');
  document.body.appendChild(o);
  function dec(src){var i=new Image();i.src=src;return i.decode?i.decode().catch(function(){}):Promise.resolve()}
  function start(){o.classList.remove('wait')}
  /* старт — когда главный поток освободился после запуска (requestIdleCallback, не дольше 900 мс): до этого на экране
     просто мордочка, как у системной заставки, а сама анимация идёт уже без рывков */
  function idle(f){if(window.requestIdleCallback)requestIdleCallback(f,{timeout:900});else setTimeout(f,250)}
  Promise.race([Promise.all([dec(IMG.logo),IMG.wordmark?dec(IMG.wordmark):0]),new Promise(function(r){setTimeout(r,400)})]).then(function(){idle(function(){requestAnimationFrame(start)})});
  function rm(){if(gone)return;gone=1;o.remove()}
  o.addEventListener('animationend',function(e){if(e.target===o&&(e.animationName==='lnGo'||e.animationName==='lnTap'))rm()});
  o.addEventListener('pointerdown',function(){start();o.classList.add('go')});
  setTimeout(rm,6000);   /* страховка: заставка не останется навсегда, даже если анимации не дошли до конца */
})();
