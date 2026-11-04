/* веб-версия на сайте — прежде всего для iPhone и iPad (владелец, 7.1.0): приложение для iOS без Mac и аккаунта Apple не
   собрать, а файл HTML iPhone со всем кодом открыть не умеет. Поэтому ИТП лежит на сайте (папка app/web, make_web.py),
   и его ставят на экран «Домой» из Safari: значок, без строки адреса, работает без интернета (sw.js хранит страницу).
   Здесь: признаки iOS и запуска с экрана «Домой», манифест и sw.js только на сайте (не в APK, не в программе для
   Windows и не в файле), запрет «приближения» поля кода на iOS и однажды — подсказка, как поставить на экран «Домой» */
var IOS=/iP(hone|ad|od)/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
var STANDALONE=!!(navigator.standalone||(window.matchMedia&&matchMedia('(display-mode: standalone)').matches));
var ONWEB=/^https?:$/.test(location.protocol)&&!NATIVE;
if(IOS)document.documentElement.classList.add('ios');
if(STANDALONE)document.documentElement.classList.add('pwa');
(function(){
  /* Safari на iPhone приближает страницу, когда фокус попадает в поле с текстом мельче 16px (поле кода), и обратно
     не отдаляет. maximum-scale=1 это выключает; щипком приближать по-прежнему можно (iOS 10+) */
  if(IOS){var v=document.querySelector('meta[name="viewport"]');if(v&&!/maximum-scale/.test(v.content))v.content+=', maximum-scale=1'}
  if(!ONWEB)return;
  var l=document.createElement('link');l.rel='manifest';l.href='manifest.webmanifest';document.head.appendChild(l);
  /* просим браузер не стирать данные сайта сам (Safari иначе может удалить их, если сайт долго не открывали) */
  try{if(navigator.storage&&navigator.storage.persist)navigator.storage.persist()}catch(e){}
  if('serviceWorker' in navigator)addEventListener('load',function(){try{navigator.serviceWorker.register('sw.js').catch(function(){})}catch(e){}});
})();
/* подсказка «Поставь на экран Домой» — один раз, в Safari на iPhone/iPad, если ИТП открыт как сайт, а не с экрана «Домой».
   Ждёт, пока уйдут вступление, соглашение и другие окна */
function webHint(n){
  if(!ONWEB||!IOS||STANDALONE||appGet().a2hs)return;
  if(document.querySelector('#crt,body>.w98,body>.bkt,.agvw,body>.modal,.lnch')||!S.nick||!agOk()){if((n||0)<150)setTimeout(function(){webHint((n||0)+1)},800);return}
  appSet({a2hs:1});
  modal('<h2>Поставь ИТП на экран «Домой»</h2>'
    +'<div class="a2h"><p><b>1.</b> Внизу Safari нажми <span class="a2i" aria-label="Поделиться"></span> «Поделиться».</p>'
    +'<p><b>2.</b> Пролистай и выбери <b>«На экран „Домой“»</b>, затем «Добавить».</p></div>'
    +'<p>Появится значок с кроликом: ИТП будет открываться на весь экран, как приложение, и работать без интернета.</p>'
    +'<p class="mu">Так прогресс надёжнее: данные сайтов, которые давно не открывали, Safari может стереть, а данные приложений с экрана «Домой» — нет. Резервная копия — в настройках.</p>',[['Понятно']])}
(function(){var g0=greet;greet=function(){var r=g0.apply(this,arguments);setTimeout(webHint,1600);return r}})();
