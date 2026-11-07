# 7.3.0, ЕГЭ: главы в норах открываются с первой теории, тренажёр в «Практике» появляется после прочтения теории номера,
# ответы проверяются, старое сохранение (до замены нор «Черепаха» и «IP-адреса») переезжает на новые номера тем.
# Запуск из корня: python tests/ege7.py [папка для скриншотов]. Код выхода 1 — ошибки.
import os, sys
from playwright.sync_api import sync_playwright

PAGE = 'file:///' + os.path.abspath('out5.html').replace(chr(92), '/')
OUT = sys.argv[1] if len(sys.argv) > 1 else None
CLICK = "t=>[...document.querySelectorAll('button')].find(b=>b.textContent.trim()===t).click()"
bad = 0


def chk(ok, msg):
    global bad
    bad += not ok
    print('ok ' if ok else 'BAD', msg)


with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    pg = c.new_page(); pg.goto(PAGE); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{appSet({agree:{v:AGV,t:Date.now()}});S.nick='Тест';S.start=0;save()}")
    pg.reload(); pg.wait_for_timeout(2500)
    pg.evaluate("document.querySelectorAll('body>.w98').forEach(e=>e.remove())")
    r = pg.evaluate("""()=>{var H=[];TOPICS.forEach(function(t,i){if(t.opt&&/^ЕГЭ/.test(t.n))H.push(i)});
      var first=0,firstOpen=0,second=0,secondOpen=0,pr=0,nums=[];
      H.forEach(function(i){TOPICS[i].items.forEach(function(x,j){var f=!j||TOPICS[i].items[j-1].ch!==x.ch;
        if(f){first++;firstOpen+=isOpen(i,j)?1:0;pr+=x.pr.length;nums.push(x.ch)}else{second++;secondOpen+=isOpen(i,j)?1:0}})});
      return{H:H.length,first:first,firstOpen:firstOpen,second:second,secondOpen:secondOpen,pr:pr,nums:nums.sort(function(a,b){return a-b}).join(',')}}""")
    chk(r['H'] == 3, 'три норы ЕГЭ: %s' % r['H'])
    chk(r['nums'] == ','.join(map(str, range(1, 28))), 'главы на все 27 номеров')
    chk(r['first'] == r['firstOpen'] == 27, 'первая теория каждой главы открыта: %s из %s' % (r['firstOpen'], r['first']))
    chk(r['secondOpen'] == 0, 'вторая теория закрыта, пока не прочитана первая: открыто %s' % r['secondOpen'])
    chk(r['pr'] >= 350, 'задач в тренажёре: %s' % r['pr'])
    chk(not pg.evaluate("TOPICS.some(function(t){return /^Черепаха|^IP-адреса/.test(t.n)})"), 'старых нор «Черепаха» и «IP-адреса» нет')
    # тренажёр закрыт, пока не прочитана теория
    pg.evaluate(CLICK, 'Практика'); pg.wait_for_timeout(500)
    chk(pg.evaluate("!!document.querySelector('.pcard.ege[disabled]')"), 'карточка ЕГЭ-тренажёра есть и закрыта')
    # открываем главу №10 (читаем первую теорию через сам экран теории) и смотрим нору
    k = pg.evaluate("""()=>{var r;TOPICS.forEach(function(t,i){t.items.forEach(function(x,j){if(x.ch===10&&x.cht)r=[i,j]})});return r}""")
    pg.evaluate("k=>{BACK=home;go(k[0],k[1])}", k); pg.wait_for_timeout(600)
    if OUT:
        pg.screenshot(path=OUT + '/ege_theory.png', full_page=False)
    for _ in range(3):
        if pg.evaluate("k=>!!S.d[k[0]+'-'+k[1]]", k):
            break
        pg.evaluate("()=>{var b=[...document.querySelectorAll('button')].find(b=>/^Прочитано/.test(b.textContent.trim()));if(b)b.click()}"); pg.wait_for_timeout(700)
    chk(pg.evaluate("k=>!!S.d[k[0]+'-'+k[1]]", k), 'первая теория №10 прочитана')
    chk(pg.evaluate("k=>!!isOpen(k[0],k[1]+1)", k), 'после неё открылась вторая теория №10')
    pg.evaluate("k=>{HOLE=k[0];hole(k[0])}", k); pg.wait_for_timeout(700)
    chk(pg.evaluate("document.querySelectorAll('.ech').length") >= 12, 'заголовки глав в норе')
    if OUT:
        pg.evaluate("document.getAnimations().forEach(a=>{try{a.finish()}catch(e){}})")
        pg.screenshot(path=OUT + '/ege_hole.png')
    pg.evaluate("HOLE=-1"); pg.evaluate(CLICK, 'Практика'); pg.wait_for_timeout(500)
    chk(pg.evaluate("!!document.querySelector('.pcard.ege:not([disabled])')"), 'тренажёр открылся после прочтения теории')
    pg.evaluate("S.rnd=1;save();document.querySelector('.pcard.ege').click()"); pg.wait_for_timeout(400)
    chk(pg.evaluate("document.querySelectorAll('.egl0 .li').length") == 2, 'в тренажёре «вперемешку» и №10')
    pg.evaluate("document.querySelector('.egl0 .li[data-n=\"10\"]').click()"); pg.wait_for_timeout(500)
    chk(pg.evaluate("/Задание №10/.test(document.querySelector('.egh').textContent)"), 'задача №10 на экране')
    chk(pg.evaluate("!!document.querySelector('.egt.cl')||document.querySelector('.egt').scrollHeight<=230"), 'длинное условие свёрнуто')
    pg.fill('#code', 'from ipaddress import ip_network\nprint(ip_network("10.0.0.0/30").num_addresses + 1)')
    pg.click('#run')
    for _ in range(60):
        pg.wait_for_timeout(500)
        if '5' in (pg.evaluate("($('o')||{}).textContent||''")):
            break
    chk('5' in pg.evaluate("($('o')||{}).textContent||''"), 'компилятор в тренажёре запускает код: %r' % pg.evaluate("($('o')||{}).textContent||''")[:60])
    if OUT:
        pg.screenshot(path=OUT + '/ege_task.png', full_page=True)
    ans = pg.evaluate("""()=>{var id=EGE.seen[EGE.seen.length-1],a;egeOpen().forEach(function(x){x.pr.forEach(function(p){if(p.id===id)a=p.a})});return a}""")
    pg.fill('#ega', 'неверно'); pg.click('#go'); pg.wait_for_timeout(300)
    chk(pg.evaluate("document.getElementById('dock').classList.contains('bad')"), 'неверный ответ — «Неверно»')
    pg.click('#go'); pg.wait_for_timeout(400)
    ans = pg.evaluate("""()=>{var id=EGE.seen[EGE.seen.length-1],a;egeOpen().forEach(function(x){x.pr.forEach(function(p){if(p.id===id)a=p.a})});return a}""")
    pg.fill('#ega', ' ' + ans.upper() + ' '); pg.click('#go'); pg.wait_for_timeout(300)
    chk(pg.evaluate("document.getElementById('dock').classList.contains('ok')"), 'верный ответ (%s) засчитан' % ans)
    if OUT:
        pg.screenshot(path=OUT + '/ege_ok.png')
    # все ответы задач проходят нормализацию сами с собой и не пустые
    chk(pg.evaluate("egeOpen().length>0&&TOPICS.every(function(t){return t.items.every(function(x){return!x.pr||x.pr.every(function(p){return egeNorm(p.a)!==''})})})"), 'у всех задач есть ответ')
    # миграция: сохранение 7.2 (mv 6), где темы стояли по старым номерам
    r = pg.evaluate("""()=>{var o={nick:'Старый',mv:6,start:11,d:{'11-0':1,'10-0':1,'41-2':1,'40-1':1,'17-0':1},at:{'41-2':'full'}};
      var c=clean(o);return{d:Object.keys(c.d).sort().join(' '),at:Object.keys(c.at).join(' '),start:c.start,mv:c.mv,
        n11:TOPICS[10].n,n41:TOPICS[42].n,n17:TOPICS[16].n}}""")
    chk(r['d'] == '10-0 16-0 42-2' and r['at'] == '42-2' and r['start'] == 10 and r['mv'] == 7,
        'миграция номеров тем: %s / at %s / start %s / mv %s' % (r['d'], r['at'], r['start'], r['mv']))
    chk(r['n11'] == 'Поиск ошибок' and r['n41'] == 'Наследование' and r['n17'] == 'Code review: читаем и объясняем', 'темы после миграции те же: %s, %s, %s' % (r['n11'], r['n41'], r['n17']))
    b.close()
print('bad', bad)
sys.exit(1 if bad else 0)
