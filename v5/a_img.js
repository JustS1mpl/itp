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
