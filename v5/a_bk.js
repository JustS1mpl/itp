/* ===== v5.4.2: напоминание о резервной копии =====
   Прогресс хранится только в браузере. Раз в 14 дней приложение предлагает сохранить копию.
   Дата последней копии лежит в отдельном ключе localStorage (itp-bk), поэтому формат сохранения pyshag2 не меняется. */
(function(){
  var KB='itp-bk',KA='itp-bka';
  function get(k){try{return localStorage.getItem(k)||''}catch(e){return''}}
  function put(k,v){try{localStorage.setItem(k,v)}catch(e){}}
  var ex0=exportData;
  exportData=function(){var r=ex0.apply(this,arguments);put(KB,day(new Date()));return r};
  var im0=importData;
  importData=function(){var r=im0.apply(this,arguments);if(!r)put(KB,day(new Date()));return r};
  function ask(){
    if(!S.nick||PE.length||document.querySelector('.modal'))return;
    if(Object.keys(S.d).length<5)return;
    var t=day(new Date()),mine=vdate(get(KB)),last=mine||S.reg||'',asked=vdate(get(KA));
    var since=last?dnum(t)-dnum(last):99;
    if(since<14)return;
    if(asked&&dnum(t)-dnum(asked)<7)return;
    put(KA,t);
    modal('<h2>Сохрани резервную копию</h2><p>Прогресс хранится только в этом браузере. Если очистить данные, сменить телефон или переустановить приложение, он пропадёт.</p><p class="mu">'+(mine?'Последняя копия: '+since+' '+pl(since,['день','дня','дней'])+' назад.':'Копию ты ещё не сохранял.')+'</p>',
      [['Сохранить копию',function(){saveFile('itp-backup-'+t+'.json',new Blob([exportData()],{type:'application/json'}));toast('Копия сохранена')}],['Позже',null,1]]);
  }
  setTimeout(ask,2600);
})();
