/* заставка при запуске приложения на телефоне (владелец, 7.1.0): вместо того чтобы сразу показывать островки — секунда
   по кадрам, которые прислал владелец: мордочка ИТП на её фоне (продолжение системной заставки), мордочка тает,
   проявляется надпись «ИТП» цветом акцента из настроек (картинка-маска, залитая --accent), и весь экран мягко растворяется в Путь (около 1,6 с).
   Только в APK (NATIVE==='android'), только у тех, кто уже прошёл вступление (у новых есть своя заставка), и не при
   «меньше анимаций». Касание — сразу дальше. Для проверки в браузере: адрес с ?launch */
(function(){
  /* и на iPhone/iPad, когда ИТП запущен с экрана «Домой» (STANDALONE, a_web.js) — это тоже «приложение на телефоне» */
  var want=NATIVE==='android'||STANDALONE||/[?&]launch\b/.test(location.search);
  if(!want||!IMG.logo||RM()||!S||!S.nick)return;
  var o=document.createElement('div'),done=0,ts=[];o.className='lnch';o.setAttribute('aria-hidden','true');
  o.innerHTML='<img class="lnl" alt="" src="'+IMG.logo+'">'+(IMG.wordmark?'<i class="lnw" style="-webkit-mask-image:url('+IMG.wordmark+');mask-image:url('+IMG.wordmark+')"></i>':'');
  document.body.appendChild(o);
  function go(){if(done)return;done=1;ts.forEach(clearTimeout);o.classList.add('go');setTimeout(function(){o.remove()},560)}
  o.addEventListener('pointerdown',go);
  ts.push(setTimeout(function(){o.classList.add('wm')},300));
  ts.push(setTimeout(go,1150));
})();
