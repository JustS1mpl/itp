/* 7.1.1: проверка правдоподобности резервной копии (владелец: друг подправил файл копии — XP, серию, темы — и импорт
   его принял).

   Почему так, а не «настоящей подписью». Поле s — самодельный хеш sig(p, SECRET), а SECRET лежит в коде приложения, и
   код открыт на GitHub: любой пересчитает s после правки. Заменить на HMAC-SHA-256 бесполезно — ключ всё равно был бы в
   приложении. Ключ на сервере тоже не спасает: задачи проверяются на устройстве, сервер не знает, решены ли они, и
   подписал бы что угодно; а на сайте прогресс меняется прямо из консоли браузера. Честная защита — только аккаунты и
   проверка задач на сервере, а ИТП работает без интернета и без аккаунтов. Поэтому s остаётся защитой от порчи файла,
   а от правки — проверка, что прогресс вообще мог получиться в ИТП:
   • даты: регистрация, последний день, история, достижения — не раньше появления ИТП и не позже сегодня;
   • серия ≤ рекорда, рекорд ≤ дней с регистрации, серия ≤ дней от регистрации до последнего дня;
   • дни серии (начиная с HISTV, когда каждый день серии стал попадать в историю) — есть в истории или заморожены;
   • опыт ≤ того, что можно получить за пройденные островки и цели серии (у тех, кто начал в 7.0 и позже: у
     перешедших с 6.x опыт перенесён целиком, его не пересчитать);
   • достижения сходятся со статистикой: серия, темы, уровень, проекты.
   Подогнать цифры в пределах возможного по-прежнему можно (это предел защиты без сервера), но «30 тем из 30,
   3660 дней подряд» — уже нет. Файл отклоняется целиком, текущий прогресс не меняется. */
var ITP0='2023-01-01',      /* раньше этой даты ИТП точно не было: даты раньше — подделка */
    ITP7='2026-11-04',      /* выпуск 7.0.0: кто зарегистрировался с этого дня, начал с нуля в 7.x */
    HISTV='2026-11-06';     /* с этого дня каждый день серии записывается в историю (bump ниже) */

/* каждый день, когда прибавилась серия, — в истории, даже если островок пройден повторно и опыта не дал */
(function(){var _b=bump;bump=function(k){_b(k);var t=day(new Date());if(!S.hist[t]){hit(0,0);save()}}})();

function bkPlaus(r){
  var T=day(new Date()),E='Файл изменён или подделан';
  var vd=function(x){return typeof x==='string'&&!!vdate(x)},n=function(x){return typeof x==='number'&&Number.isFinite(x)&&x>=0?x:0};
  var D=function(a,b){return dnum(b)-dnum(a)};          /* дней от a до b */
  /* от регистрации считаем только у начавших в 7.x: у старых пользователей без даты регистрации ИТП ставит её задним
     числом по самой ранней записи истории (regDay), и она может быть позже настоящего начала серии */
  var reg=vd(r.reg)?r.reg:'',from=reg&&reg>=ITP7?reg:ITP0;
  if(typeof r.reg==='string'&&r.reg&&(!reg||reg<ITP0||reg>T))return E+': дата начала занятий';
  /* пройденный островок с вопросами или кодом всегда оставляет отметку об опыте (award): «пройдено» без неё —
     дописано руками. Теория и проекты не в счёт: теория опыта не даёт, у проекта отметка может пропасть штатно */
  var dd0=r.d&&typeof r.d==='object'?r.d:{},at0=r.at&&typeof r.at==='object'?r.at:{};
  for(var dk in dd0){var mm=/^(\d+)-(\d+)$/.exec(dk),tt=mm&&TOPICS[+mm[1]],ii=tt&&tt.items&&tt.items[+mm[2]];
    if(ii&&(ii.t==='flash'||ii.t==='test')&&dd0[dk]===1&&!at0[dk])return E+': островки пройдены без опыта за них'}
  /* типы: число — только целое неотрицательное (штатная копия других не содержит) */
  var bad=['xp','streak','max'].filter(function(k){return k in r&&!(Number.isInteger(r[k])&&r[k]>=0)});
  if(bad.length)return E+': неверный тип данных ('+bad.join(', ')+')';
  if(['d','tk','at','hist','ach'].some(function(k){return k in r&&(!r[k]||typeof r[k]!=='object'||Array.isArray(r[k]))}))return E+': неверный тип данных';
  var xp=n(r.xp),st=n(r.streak),mx=n(r.max);
  if(st>mx)return E+': серия больше рекорда';
  if(mx>D(from,T)+1)return E+': серия длиннее, чем дней прошло с начала занятий';
  if(st>0){
    if(!vd(r.last)||r.last>T||r.last<from)return E+': дата последнего занятия';
    if(st>D(from,r.last)+1)return E+': серия длиннее, чем дней прошло с начала занятий';
    /* дни серии с HISTV в пределах истории (370 дней): занятие или заморозка */
    var h=r.hist&&typeof r.hist==='object'?r.hist:{},fu=r.fz&&Array.isArray(r.fz.u)?r.fz.u:[];
    var a=dadd(r.last,-(st-1));if(a<HISTV)a=HISTV;var cut=day(ago(369));if(a<cut)a=cut;
    for(var d=a;d<=r.last;d=dadd(d,1))if(!h[d]&&fu.indexOf(d)<0)return E+': в истории нет дней серии';
  }
  if(r.hist&&typeof r.hist==='object')for(var hk in r.hist)if(vd(hk)&&(hk>T||hk<dadd(from,-1)))return E+': история занятий';
  /* опыт: сколько вообще можно получить за то, что пройдено */
  var at=r.at&&typeof r.at==='object'?r.at:{};
  if(reg&&reg>=ITP7){
    var cap=0;
    for(var k in at){var v=at[k],m=/^(\d+)-(\d+)$/.exec(k);if(!m||(v!=='full'&&v!=='low'))continue;
      var t=TOPICS[+m[1]],it=t&&t.items&&t.items[+m[2]];if(!it)continue;
      if(v==='low'){cap+=2;continue}
      cap+=it.t==='project'?(it.bonus>0?it.bonus|0:40):Math.max(60,20+2*Math.max(0,((it.q||[]).length||0)-4))}
    cap+=750*(Math.floor(mx/7)+1);                      /* цели серии: не больше одной на каждые 7 дней рекорда */
    if(xp>cap)return E+': опыта больше, чем можно получить за пройденные островки';
  }
  /* достижения: даты и условия */
  var ac=r.ach&&typeof r.ach==='object'?r.ach:{},dd=r.d&&typeof r.d==='object'?r.d:{};
  var tdn=0,tall=0;TOPICS.forEach(function(t,i){if(t.intro)return;tall++;var its=t.items||[];if(its.length&&its.every(function(x,j){return dd[i+'-'+j]===1}))tdn++});
  var lv=lvlInfo(xp).l,pj=r.cn&&typeof r.cn==='object'?n(r.cn.pj):0;
  var need={w1:mx>=7,m1:mx>=30,s100:mx>=100,t5:tdn>=5,t10:tdn>=10,tall:tdn>=tall,lv5:lv>=5,lv10:lv>=10,proj:pj>=1,pj3:pj>=3};
  for(var id in ac){
    if(vd(ac[id])&&(ac[id]>T||ac[id]<dadd(from,-1)))return E+': дата достижения';
    if(id in need&&!need[id])return E+': достижение не сходится с прогрессом';
  }
  return''}

/* импорт: сначала прежние проверки (формат, s, типы), потом правдоподобность — до того, как что-то поменяется */
(function(){var _imp=importData;importData=function(txt){
  try{var o=JSON.parse(txt),d=o&&typeof o.p==='string'&&typeof o.s==='string'&&o.s===sig(o.p,SECRET)?JSON.parse(o.p):null;
    if(d&&d.data&&typeof d.data==='object'&&!Array.isArray(d.data)){var e=bkPlaus(d.data);if(e)return e}}catch(e){}
  return _imp(txt)}})();
