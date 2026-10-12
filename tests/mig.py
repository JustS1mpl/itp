"""Миграция сохранений до v5.7.0 (раздел ЕГЭ удалён: темы 15-20 выброшены, 21+ сдвинуты на -6)."""
import json, os, sys, datetime
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(__file__))
import h
W = os.getcwd() + '/'
t = datetime.date.today().isoformat()
OLD = {'nick': 'Тест', 'start': 22, 'xp': 500, 'streak': 2, 'last': t, 'seen': t, 'max': 2, 'mode': 'ex',
       'd': {'0-0': 1, '1-0': 1, '16-0': 1, '16-1': 1, '21-0': 1, '21-1': 1, '22-0': 1, '27-2': 1},
       'tk': {'21-4-0': 1, '16-1-0': 1}, 'at': {'21-1': 'full', '17-0': 'low'}, 'es': {'21-1': 0, '16-1': 3},
       'hu': {'21': 1, '17': 1}, 'hist': {t: {'xp': 20, 'les': 1}}}
with sync_playwright() as p:
    b, ctx, pg, logs = h.open_page(p, W + 'out5.html', OLD, 390, 800, touch=True)
    pg.wait_for_timeout(2500)
    n = pg.evaluate("TOPICS.length")
    S = pg.evaluate("JSON.stringify({d:S.d,tk:S.tk,at:S.at,es:S.es,hu:S.hu,start:S.start,mv:S.mv,mode:S.mode})")
    print('topics', n); print(S)
    s = json.loads(S)
    assert n == 22, n
    assert s['d'] == {'0-0': 1, '1-0': 1, '15-0': 1, '15-1': 1, '16-0': 1, '21-2': 1}, s['d']
    assert s['tk'] == {'15-4-0': 1}, s['tk']
    assert s['at'] == {'15-1': 'full'} and s['es'] == {'15-1': 0} and s['hu'] == {'15': 1}, s
    assert s['start'] == 16 and s['mv'] == 2 and 'mode' not in s, s
    nav = pg.evaluate("[].map.call(document.querySelectorAll('nav button, #nav button'),function(x){return x.textContent.trim()})")
    print('nav', nav)
    assert len(nav) == 4, nav
    # повторная загрузка: сдвиг не должен применяться второй раз
    pg.reload(); pg.wait_for_timeout(2500)
    d2 = pg.evaluate("JSON.stringify(S.d)")
    assert json.loads(d2) == s['d'], d2
    assert pg.evaluate("S.start") == 16
    # экспорт-импорт
    ex = pg.evaluate("exportData()")
    assert json.loads(json.loads(ex)['p'])['data']['mv'] == 2
    # все вкладки открываются без ошибок
    for tab in ['pr', 'ed', 'prof', 'home']:
        pg.evaluate("document.querySelector('[data-t=%s]').click()" % tab); pg.wait_for_timeout(500)
    err = [l for l in logs if l.startswith(('PAGEERROR', 'error'))]
    print('errors', err)
    assert not err
    # свежий пользователь
    b.close()
    b, ctx, pg, logs = h.open_page(p, W + 'out5.html', None, 390, 800, touch=True)
    pg.wait_for_timeout(2000)
    print('fresh errors', [l for l in logs if l.startswith(('PAGEERROR', 'error'))])
    b.close()
print('OK')
