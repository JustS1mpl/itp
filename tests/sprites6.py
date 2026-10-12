"""Спрайты кролика v6.3: тишина (нет фоновых и реактивных анимаций), логика ошибок, иконка профиля, светлая и тёмная тема.
Запуск из корня после сборки: python3 tests/sprites6.py [файл.html]"""
import os, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(__file__))
import h
F = sys.argv[1] if len(sys.argv) > 1 else os.getcwd() + '/out5.html'
ST = {'nick': 'Т', 'start': 0, 'seen': '2026-10-12', 'mv': 2, 'streak': 3, 'last': '2026-10-11', 'xp': 50,
      'd': {'0-0': 1, '1-0': 1, '1-1': 1, '1-2': 1}}
DONE = "doneScreen({title:'t',err:%d,x:20,btns:'<button class=\"btn\" id=\"go\">Дальше</button>'})"


def ok(c, m):
    if not c:
        raise AssertionError(m)
    print('  ✓', m)


def mood(pg):
    return pg.evaluate("(function(){var m=document.querySelector('#fb .mood');return m?(m.classList.contains('rolled')?'rolled':'grump'):''})()")


def sprite_anims(pg):
    return pg.evaluate("[].map.call(document.querySelectorAll('.rw.im img'),function(i){return getComputedStyle(i).animationName})")


with sync_playwright() as p:
    b, ctx, pg, logs = h.open_page(p, F, ST, 390, 820, touch=True)
    pg.wait_for_timeout(1500)
    # --- спрайты не двигаются сами: ни в приветствии, ни на итоге, ни на профиле
    pg.evaluate("S.seen='';greet()"); pg.wait_for_timeout(300)
    ok(pg.locator('.onb .rw.eat').count() == 1, 'приветствие при идущей серии: один кролик с морковкой')
    ok(set(sprite_anims(pg)) == {'none'}, 'приветствие: кролик не анимируется сам')
    pg.evaluate(DONE % 0); pg.wait_for_timeout(300)
    ok(pg.locator('.fin .rw.happy').count() == 1 and pg.locator('.fin .rw').count() == 1, 'итог без ошибок: один ликующий кролик')
    ok(set(sprite_anims(pg)) == {'none'}, 'итог: кролик не подпрыгивает')
    pg.evaluate(DONE % 3); pg.wait_for_timeout(300)
    ok(pg.locator('.fin .rw.happy').count() == 1, '3 ошибки на островке: ещё ликующий')
    pg.evaluate(DONE % 4); pg.wait_for_timeout(300)
    ok(pg.locator('.fin .rw.rolled').count() == 1 and pg.locator('.fin .rw').count() == 1, '4 ошибки и больше: один «закатил глаза», ликующего нет')
    pg.evaluate("profile()"); pg.wait_for_timeout(300)
    ok(pg.locator('.rw').count() == 0 and pg.locator('.pav .pi').count() == 1, 'профиль: вместо кролика иконка профиля, реакции на нажатие нет')
    pg.evaluate("home()"); pg.wait_for_timeout(300)
    ok(pg.locator('.gcard .rw').count() == 0 and pg.locator('.gcard .ring').count() == 1, 'карточка дня: без кролика, кольцо цели')
    # --- хмурый: только первая ошибка в серии, потом без спрайта, без повторных анимаций
    pg.evaluate("go(1,3)"); pg.wait_for_timeout(400)
    seq = []
    for step in ('w', 'w', 'w', 'r', 'w'):
        qa = pg.evaluate("(function(){var t=document.querySelector('.q').textContent,pr=document.querySelector('.q~pre'),c=pr?pr.textContent.trim():'';var q=IT(1,3).q.filter(function(x){return x.q===t&&(x.c||'').trim()===c})[0];return q.a})()")
        n = pg.locator('.opt').count()
        pg.locator('.opt[data-k="%d"]' % (qa if step == 'r' else (qa + 1) % n)).click()
        pg.locator('#go').click(); pg.wait_for_timeout(250)
        seq.append(mood(pg))
        if step == 'w' and len(seq) == 1:
            anim = pg.evaluate("(function(){var c=getComputedStyle(document.querySelector('#fb .mood'));return [c.animationName,c.animationIterationCount,c.animationDuration]})()")
            ok(anim[1] == '1' and float(anim[2].rstrip('s')) <= .2, 'хмурый: короткое появление, один раз: ' + str(anim))
        pg.locator('#go').click(); pg.wait_for_timeout(250)
    print('  последовательность спрайта:', seq)
    ok(seq[0] == 'grump' and seq[1] == '' and seq[2] == '' and seq[3] == '', 'неверно, неверно, неверно, верно: хмурый только на первом')
    # --- консоль
    pg.evaluate("editor()"); pg.wait_for_timeout(300)
    def run(code):
        pg.evaluate("var c=document.getElementById('code');c.value=%r;c.dispatchEvent(new Event('input',{bubbles:true}));document.getElementById('run').click()" % code)
        pg.wait_for_function("/завершил|не запущена|завершена/.test((document.getElementById('rst')||{}).textContent||'')&&!/выполняется/.test(document.getElementById('rst').textContent)", timeout=60000)
        pg.wait_for_timeout(250)
        return pg.evaluate("(function(){var q=document.getElementById('cmq');if(!q||q.hidden)return '';return q.querySelector('.mood')?'grump':''})()")
    r = [run(c) for c in ('print(1/0)', 'print(1/0)', 'print(1/0)', 'print("ок")', 'print(1/0)')]
    print('  консоль:', r)
    ok(r == ['grump', '', '', '', 'grump'], 'код с ошибкой: хмурый на первой ошибке, дальше текст; успех сбрасывает серию')
    # --- иконка профиля в нижней панели: маска и два состояния
    pg.evaluate("home()"); pg.wait_for_timeout(400)
    m = pg.evaluate("(function(){var i=document.querySelector('.nav .pi'),a=getComputedStyle(i,'::after'),f=getComputedStyle(i,'::before');return [a.maskImage||a.webkitMaskImage,f.opacity,a.backgroundColor]})()")
    ok('data:image/png' in m[0] and m[1] == '0', 'иконка профиля: маска из PNG, заливка выключена, пока раздел не выбран')
    pg.evaluate("profile()"); pg.wait_for_timeout(400)
    f = pg.evaluate("getComputedStyle(document.querySelector('.nav .pi'),'::before').opacity")
    ok(abs(float(f) - .28) < .02, 'иконка профиля в выбранном состоянии: заливка %s' % f)
    # --- светлая и тёмная тема
    for th, light in (('light', True), ('dark', False)):
        pg.evaluate("S.theme='%s';applyPrefs();S.seen='';greet()" % th); pg.wait_for_timeout(400)
        c = pg.evaluate("(function(){var r=document.querySelector('.rw.im'),i=getComputedStyle(r.querySelector('img'));return [getComputedStyle(r,'::before').content,getComputedStyle(r,'::after').content,i.filter]})()")
        ok(c[0] == 'none', 'тема %s: за кроликом нет фигуры (::before пуст)' % th)
        ok(c[2] == 'none' and (c[1] != 'none') == light, 'тема %s: обводки нет, контактная тень %s' % (th, 'есть' if light else 'не применяется'))
        tr = pg.evaluate("getComputedStyle(document.querySelector('.rw.im.eat')||document.body).transform")
        ok(tr != 'none', 'тема %s: LoveCarrot сдвинут к центру (%s)' % (th, tr))
    ok(not [l for l in logs if 'PAGEERROR' in l], 'ошибок нет ' + str(logs[:2]))
    b.close()
    # --- уменьшить движение
    b, ctx, pg, logs = h.open_page(p, F, ST, 390, 820, touch=True, reduced_motion='reduce')
    pg.wait_for_timeout(1500)
    pg.evaluate("go(1,3)"); pg.wait_for_timeout(400)
    pg.locator('.opt').first.click(); pg.locator('#go').click(); pg.wait_for_timeout(300)
    d = pg.evaluate("(function(){var m=document.querySelector('#fb .mood');if(!m)return null;return getComputedStyle(m).animationDuration})()")
    ok(d is None or float(d.rstrip('s')) < .001, 'reduced-motion: спрайт ошибки без движения: ' + str(d))
    b.close()
print('OK')
