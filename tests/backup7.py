# Резервная копия: штатные копии принимаются, подделанные (с пересчитанной подписью s — как сделал бы взломщик,
# который прочитал код) отклоняются, а прогресс при отказе не меняется. И режим разработчика выключен в обычной сборке.
# Запуск из корня репозитория: python tests/backup7.py   (нужен Playwright, сначала python build5.py). Код выхода 1 — ошибки.
import json, os, sys
from playwright.sync_api import sync_playwright

PAGE = 'file:///' + os.path.abspath('out5.html').replace('\\', '/')
JS_SETUP = r'''()=>{
  window.T=day(new Date());
  /* новый пользователь 7.x (начал вчера, после выпуска 7.0): прошёл первые островки по-настоящему (bump + award), серия 2 дня */
  window.mkNew=function(){
    S=clean({nick:'Тест',reg:dadd(T,-1),start:0});
    var k=0;for(var i=0;i<TOPICS.length&&k<6;i++){var t=TOPICS[i];for(var j=0;j<(t.items||[]).length&&k<6;j++){bump(i+'-'+j);award(i+'-'+j,20,0,0,1);k++}}
    S.streak=2;S.max=2;S.last=T;S.hist[dadd(T,-1)]={xp:20,les:1};S.xp+=20;save();
    return exportData()};
  /* старый пользователь с 6.x: опыт перенесён, даты регистрации до 7.0, серия 40 */
  window.mkOld=function(){
    S=clean({nick:'Старый',reg:'2026-03-01',start:0,xp:5200,streak:40,max:61,last:T,ach:{w1:'2026-03-10',m1:'2026-05-01'}});
    /* с HISTV каждый день серии штатно попадает в историю */
    for(var d=HISTV;d<=T;d=dadd(d,1))S.hist[d]={xp:20,les:1};save();
    return exportData()};
  /* «взлом»: поменять данные и честно пересчитать s секретом из кода */
  window.forge=function(txt,f){var o=JSON.parse(txt),d=JSON.parse(o.p);f(d.data);o.p=JSON.stringify(d);o.s=sig(o.p,SECRET);return JSON.stringify(o)};
  window.tryImp=function(txt){var before=JSON.stringify(S),e=importData(txt);return{e:e,same:JSON.stringify(S)===before}};
}'''
CASES = [
    ('штатная копия нового пользователя', 'mkNew()', None, True),
    ('штатная копия старого пользователя (6.x)', 'mkOld()', None, True),
    ('опыт подкручен до 41060', 'mkNew()', 'd=>{d.xp=41060}', False),
    ('опыт +100 (отчёт друга: 0 → 100)', 'mkNew()', 'd=>{d.xp+=100}', False),
    ('опыт +1000 и запись в истории', 'mkNew()', 'd=>{d.xp+=1000;var h=d.hist[T]||(d.hist[T]={xp:0,les:0});h.xp+=1000}', False),
    ('опыт за непройденный островок', 'mkNew()', 'd=>{d.at["5-0"]="full";d.xp+=60;var h=d.hist[T]||(d.hist[T]={xp:0,les:0});h.xp+=60}', False),
    ('серия 3660 дней', 'mkNew()', 'd=>{d.streak=3660;d.max=3660}', False),
    ('серия 3660 у старого пользователя', 'mkOld()', 'd=>{d.streak=3660;d.max=3660}', False),
    ('серия больше рекорда', 'mkNew()', 'd=>{d.streak=2;d.max=1}', False),
    ('регистрация в 2015 году', 'mkOld()', 'd=>{d.reg="2015-01-01"}', False),
    ('все темы пройдены', 'mkNew()', 'd=>{TOPICS.forEach(function(t,i){(t.items||[]).forEach(function(x,j){d.d[i+"-"+j]=1})});d.ach.tall=T}', False),
    ('достижение «Сотня» без серии', 'mkNew()', 'd=>{d.ach.s100=T}', False),
    ('достижение из будущего', 'mkNew()', 'd=>{d.ach.intro=dadd(T,5)}', False),
    ('история из будущего', 'mkNew()', 'd=>{d.hist[dadd(T,3)]={xp:10,les:1}}', False),
    ('опыт строкой', 'mkNew()', 'd=>{d.xp="9999"}', False),
    ('история массивом', 'mkNew()', 'd=>{d.hist=[1,2]}', False),
]
bad = 0
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(); pg.goto(PAGE); pg.wait_for_timeout(1500)
    pg.evaluate(JS_SETUP)
    for name, mk, f, ok in CASES:
        r = pg.evaluate('()=>{var t=%s;%sreturn tryImp(t)}' % (mk, ('t=forge(t,%s);' % f) if f else ''))
        good = (r['e'] == '') == ok and (ok or r['same'])
        bad += not good
        print('ok ' if good else 'BAD', name, '→', r['e'] or 'принято', '' if ok or r['same'] else '(ПРОГРЕСС ИЗМЕНИЛСЯ!)')
    # испорченная подпись
    r = pg.evaluate('()=>{var o=JSON.parse(mkNew());o.s="0000000000000000";return tryImp(JSON.stringify(o))}')
    good = r['e'] != '' and r['same']; bad += not good; print('ok ' if good else 'BAD', 'испорченная подпись →', r['e'])
    # дни серии после HISTV должны быть в истории: сдвигаем HISTV в прошлое и выкидываем день из истории
    r = pg.evaluate('()=>{HISTV=dadd(T,-10);var t=forge(mkNew(),function(d){delete d.hist[dadd(T,-1)]});var x=tryImp(t);HISTV="2026-11-06";return x}')
    good = r['e'] != ''; bad += not good; print('ok ' if good else 'BAD', 'день серии без занятия →', r['e'])
    # повторный островок в новый день тоже записывается в историю
    r = pg.evaluate('()=>{mkNew();var t=T;delete S.hist[t];bump("0-0");return !!S.hist[t]}')
    bad += not r; print('ok ' if r else 'BAD', 'повтор островка попадает в историю')
    # режим разработчика выключен в обычной сборке
    r = pg.evaluate('()=>{S.nick="TheCreatorOfNothing";return DEV()}')
    bad += bool(r); print('ok ' if not r else 'BAD', 'режим разработчика в обычной сборке:', 'выключен' if not r else 'ВКЛЮЧЁН')
    b.close()
print('bad', bad)
sys.exit(1 if bad else 0)
