/* ===== картинки в теории: подстановка из встроенного набора и увеличение по нажатию ===== */
function imgZoom(root){
  (root||app).querySelectorAll('img[data-x]').forEach(function(im){
    var s=(typeof EXIMG!=='undefined')&&EXIMG[im.dataset.x];if(s&&!im.src)im.src=s;
    im.onclick=function(){modal('<div class="figz"><img src="'+im.src+'" alt="'+esc(im.alt||'')+'"></div><p class="mu" style="margin:8px 0 0;font-size:13px">Рисунок можно прокручивать пальцем.</p>',[['Закрыть',null,1]])};
    im.setAttribute('role','button');im.setAttribute('tabindex','0');
    im.onkeydown=function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();im.click()}};
  });
}
(function(){var th0=theory;theory=function(i,j){th0(i,j);imgZoom(app)}})();

/* ===== U2-5: плачущий кролик (cry — во весь рост, cryhead — голова). Места подобраны так, чтобы не править экраны
   учёбы: обёртки над готовыми функциями.
   • приветствие дня, когда серия прервалась или ученика не было 3+ дня (вместо кролика с морковкой);
   • голова — третья неудача подряд в одном задании (первая — хмурый, вторая — без кролика, как раньше);
   Слова под головой свои; звука у кролика нет (звуки — у самих событий). */
var CRYL=['Кролик расстроился, но не сдаётся. И ты не сдавайся.','Третий раз мимо. Открой подсказку — это не стыдно.','Кролик всхлипнул. Перечитай условие, там ответ ближе, чем кажется.'],CRYI=Math.floor(Math.random()*3);
(function(){
  var g0=greet;greet=function(){
    var t=day(new Date()),fresh=S.seen!==t,away=0,sad=false;
    try{away=S.seen?dnum(t)-dnum(S.seen):0}catch(e){}
    var r=g0.apply(this,arguments);
    try{sad=fresh&&!!IMG.cry&&((S.streak>=2&&streakNow()===0)||away>=3)}catch(e){}
    if(sad){var w=app.querySelector('.gr .rw.im');if(w){w.className='rw im cry';w.querySelector('img').src=IMG.cry}}
    return r};
  var e0=errMood;errMood=function(n){return n===3&&IMG.cryhead?'cryhead':e0(n)};
  var m0=moodLine;moodLine=function(k){return k==='cryhead'?CRYL[CRYI++%CRYL.length]:m0(k)};
})();
