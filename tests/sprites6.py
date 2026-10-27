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
    return pg.evaluate("(function(){var m=document.querySelector('#fb .mood');return m?(m.classList.contains('rolled')?'rolled':'grumphead'):''})()")


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
    ok(pg.locator('.hero .pav .rw.eat').count() == 1 and pg.locator('.hero .pav .pi').count() == 0 and pg.locator('button.pav').count() == 0, 'профиль: кролик в шапке (LoveCarrot), без реакции на нажатие')
    ok(pg.evaluate("document.documentElement.dataset.ph") == 'card', 'шапка профиля по умолчанию: «Карточка»')
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
    ok(seq[0] == 'grumphead' and seq[1] == '' and seq[2] == '' and seq[3] == '', 'неверно, неверно, неверно, верно: хмурый только на первом')
    # --- консоль
    pg.evaluate("editor()"); pg.wait_for_timeout(300)
    def run(code):
        pg.evaluate("var c=document.getElementById('code');c.value=%r;c.dispatchEvent(new Event('input',{bubbles:true}));document.getElementById('run').click()" % code)
        pg.wait_for_function("/завершил|не запущена|завершена/.test((document.getElementById('rst')||{}).textContent||'')&&!/выполняется/.test(document.getElementById('rst').textContent)", timeout=60000)
        pg.wait_for_timeout(250)
        return pg.evaluate("(function(){var q=document.getElementById('cmq');if(!q||q.hidden)return '';return q.querySelector('.mood')?'grumphead':''})()")
    r = [run(c) for c in ('print(1/0)', 'print(1/0)', 'print(1/0)', 'print("ок")', 'print(1/0)')]
    print('  консоль:', r)
    ok(r == ['grumphead', '', '', '', 'grumphead'], 'код с ошибкой: хмурый на первой ошибке, дальше текст; успех сбрасывает серию')
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
    # --- тень стоит под лапами: центр и ширина тени против нижних 10 % строк самого спрайта (светлая тема)
    from PIL import Image
    import numpy as np
    pg.evaluate("S.theme='light';applyPrefs()")
    for st, fn in (('eat', 'lovecarrot'), ('happy', 'cheer'), ('rolled', 'grump')):
        a = np.array(Image.open('assets/mascot/%s.webp' % fn).convert('RGBA'))[:, :, 3] > 40
        H, W = a.shape; y1 = np.nonzero(a)[0].max(); xx = np.nonzero(a[int(y1 - .1 * H):y1 + 1])[1]
        fc, fw = (xx.min() + xx.max()) / 2 / W, (xx.max() - xx.min()) / W
        pg.evaluate("document.body.insertAdjacentHTML('beforeend','<div id=\"shx\" style=\"position:absolute;left:0;top:0;width:300px\">'+rabbit('%s')+'</div>')" % st)
        r = pg.evaluate("(function(){var w=document.querySelector('#shx .rw'),c=getComputedStyle(w,'::after'),W=w.getBoundingClientRect().width;var l=parseFloat(c.left),wd=parseFloat(c.width);return [(l+wd/2)/W,wd/W]})()")
        pg.evaluate("document.getElementById('shx').remove()")
        ok(abs(r[0] - fc) < .03 and r[1] >= fw, 'тень под лапами у %s: центр тени %.1f%% против %.1f%% у лап, ширина %.0f%% >= %.0f%%' % (st, r[0] * 100, fc * 100, r[1] * 100, fw * 100))
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
