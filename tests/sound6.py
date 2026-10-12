"""Проверка звукового дизайна v6 (нужны Playwright и numpy). Запуск из корня после сборки: python3 tests/sound6.py [файл.html]
1) каждый звук рисуется без динамиков (OfflineAudioContext) и измеряется: длительность, пик, доля резких частот, клиппинг;
2) контекст создаётся только после первого касания;
3) выключенный звук, отсутствие Web Audio и работа без звука ничего не ломают;
4) звуки вызываются в тот же момент, что и события анимации (ответ, опыт, окно, переход, подсказка, серия, достижение)."""
import os, sys, json
import numpy as np
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(__file__))
import h
W = os.getcwd() + '/'
F = sys.argv[1] if len(sys.argv) > 1 else W + 'out5.html'
ST = {'nick': 'Т', 'start': 0, 'seen': '2000-01-01', 'last': '2026-10-11', 'streak': 3, 'mv': 2, 'd': {'0-0': 1, '1-0': 1}}
SR = 44100


def ok(c, m):
    if not c:
        raise AssertionError(m)
    print('  ✓', m)


# запись всех обращений к Web Audio и вызовов snd
HOOK = """
window.__ac=0;window.__osc=0;window.__sl=[];
(function(){var A=window.AudioContext;if(!A)return;
 window.AudioContext=function(o){window.__ac++;window.__acT=performance.now();return new A(o)};window.AudioContext.prototype=A.prototype;
 var st=OscillatorNode.prototype.start;OscillatorNode.prototype.start=function(){window.__osc++;return st.apply(this,arguments)}})();
"""
WRAP = """(function(){var o=window.snd;window.snd=function(x,a){window.__sl.push([typeof x==='string'?x:JSON.stringify(x),performance.now()]);return o.apply(this,arguments)}})()"""


def tap1(pg):
    """первое касание: кнопка приветствия, если оно показано, иначе раздел «Путь»"""
    if pg.locator('#go').count():
        pg.locator('#go').click()
    else:
        pg.locator('.nav button[data-t="home"]').click()
    pg.wait_for_timeout(300)


def page(p, init=None, state=ST, **kw):
    b, ctx, pg, logs = h.open_page(p, F, state, 390, 820, touch=True, **kw)
    if init:
        ctx.add_init_script(init)
        pg.reload()  # скрипт-перехватчик должен работать с самого начала загрузки
    return b, ctx, pg, logs


def run():
    with sync_playwright() as p:
        # ---- 1. измерения каждого звука
        b, ctx, pg, logs = h.open_page(p, F, ST, 390, 820)
        pg.wait_for_timeout(1500)
        names = pg.evaluate("Object.keys(SXV)")
        print('== звуки:', ' '.join(names))
        rows = []
        for n in names:
            a = {'nav': 1} if n == 'tap' else None
            s = np.array(pg.evaluate("sndRender(%s,%s)" % (json.dumps(n), json.dumps(a))), dtype=float)
            ok(len(s) > 0, 'звук «%s» отрисован' % n)
            pk = np.max(np.abs(s))
            env = np.abs(s)
            idx = np.where(env > pk * 10 ** (-40 / 20))[0]
            dur = (idx[-1] + 1) / SR if len(idx) else 0
            sp = np.abs(np.fft.rfft(s[:SR])) ** 2
            fr = np.fft.rfftfreq(SR, 1 / SR)
            hi = sp[fr > 4000].sum() / max(sp.sum(), 1e-12)
            rows.append((n, dur, 20 * np.log10(pk + 1e-12), hi, pk))
        print('%-9s %8s %8s %8s' % ('звук', 'длит,мс', 'пик,дБ', 'доля>4кГц'))
        for n, d, pkdb, hi, pk in rows:
            print('%-9s %8.0f %8.1f %8.3f' % (n, d * 1000, pkdb, hi))
        long_ = [r for r in rows if r[1] > 0.4]
        ok(len(long_) <= 6, 'длиннее 400 мс только редкие награды: ' + ', '.join(r[0] for r in long_))
        for n, d, pkdb, hi, pk in rows:
            ok(d < 1.2, 'длительность «%s» %.0f мс < 1,2 с' % (n, d * 1000))
            ok(pkdb < -8, 'пик «%s» %.1f дБ: далеко от клиппинга' % (n, pkdb))
            ok(hi < 0.12, 'у «%s» мало резких частот (%.3f)' % (n, hi))
        short = {n: pkdb for n, d, pkdb, hi, pk in rows}
        for n in ('tap', 'go', 'back', 'open', 'close', 'tick', 'lock'):
            ok(-32 < short[n] < -15, 'звук интерфейса «%s» тихий, но слышный: %.1f дБ' % (n, short[n]))
        ok(short['bad'] < short['ok'] + 1, 'ошибка не громче верного ответа')
        ok(max(short[n] for n in ('ach', 'fanfare', 'level')) <= max(short[n] for n in ('ok', 'solve', 'done')) + 1, 'награды не громче обычной обратной связи')
        b.close()

        # ---- 2. контекст только после первого касания
        b, ctx, pg, logs = page(p, HOOK)
        pg.wait_for_timeout(2500)  # приветствие, тосты, таймеры: всё это не должно создать контекст
        ok(pg.evaluate("window.__ac") == 0, 'до первого касания AudioContext не создан')
        pg.evaluate("snd('ok');snd('done')")
        ok(pg.evaluate("window.__ac") == 0, 'вызовы snd до касания ничего не создают')
        tap1(pg)
        pg.wait_for_timeout(300)
        ok(pg.evaluate("window.__ac") == 1, 'после первого касания создан один AudioContext')
        pg.wait_for_function("SX.c&&SX.c.state==='running'", timeout=5000)
        ok(True, 'контекст запущен (running)')
        b.close()

        # ---- 3a. звук выключен: полная тишина и ни одной ошибки
        st = dict(ST, mute=1)
        b, ctx, pg, logs = page(p, HOOK, st)
        pg.wait_for_timeout(1200)
        for sel in ('.nav button[data-t="home"]', '.nav button[data-t="pr"]', '.nav button[data-t="prof"]', '#ttl'):
            if pg.locator(sel).count():
                pg.locator(sel).first.click()
                pg.wait_for_timeout(250)
        pg.evaluate("snd('ok');snd('ach');snd('level')")
        ok(pg.evaluate("window.__osc") == 0, 'звук выключен: ни одного осциллятора запущено')
        ok(not [l for l in logs if 'PAGEERROR' in l], 'звук выключен: ошибок нет')
        b.close()

        # ---- 3b. «Звуки интерфейса» выключены: интерфейс молчит, награды звучат
        st = dict(ST, set={'sfx': 0})
        b, ctx, pg, logs = page(p, HOOK, st)
        pg.wait_for_timeout(1200)
        tap1(pg)
        pg.locator('.nav button[data-t="pr"]').click()
        pg.wait_for_timeout(300)
        n0 = pg.evaluate("window.__osc")
        pg.evaluate("snd('tap');snd('go');snd('open');snd('close')")
        ok(pg.evaluate("window.__osc") == n0, 'звуки интерфейса выключены: касания, переходы и окна молчат')
        pg.evaluate("snd('ok')")
        ok(pg.evaluate("window.__osc") > n0, 'но ответы и награды звучат')
        b.close()

        # ---- 3c. нет Web Audio совсем (старый браузер): всё работает
        kill = "window.AudioContext=undefined;window.webkitAudioContext=undefined;window.OfflineAudioContext=undefined;"
        b, ctx, pg, logs = page(p, kill)
        pg.wait_for_timeout(1200)
        tap1(pg)
        pg.evaluate("snd('ok');snd('bad');snd('ach');snd('done');snd('level')")
        pg.evaluate("go(1,1)"); pg.wait_for_timeout(300)
        pg.locator('.opt').first.click(); pg.locator('#go').click(); pg.wait_for_timeout(300)
        ok(pg.locator('#dock.ok,#dock.bad').count() == 1, 'без Web Audio вопрос проверяется как обычно')
        pg.evaluate("home();settings()"); pg.wait_for_timeout(300)
        ok(pg.locator('h1').first.inner_text() == 'Настройки', 'без Web Audio открываются настройки')
        ok(not [l for l in logs if 'PAGEERROR' in l], 'без Web Audio: ошибок нет ' + str(logs[:2]))
        b.close()

        # ---- 4. звук в тот же момент, что и анимация
        st = dict(ST, d={'0-0': 1, '1-0': 1, '1-1': 1, '1-2': 1}, es={'1-1': 0}, at={'1-1': 'full'})
        b, ctx, pg, logs = page(p, HOOK, st)
        pg.wait_for_timeout(1200)
        tap1(pg)  # приветствие → Путь
        pg.evaluate(WRAP)
        pg.evaluate("window.__dock=[];new MutationObserver(function(){var d=document.getElementById('dock');window.__dock.push([d?d.className:'',performance.now()])}).observe(document.body,{subtree:true,attributes:true,attributeFilter:['class']})")
        pg.evaluate("go(1,3)"); pg.wait_for_timeout(500)
        # неверный, потом верный ответ
        qa = pg.evaluate("(function(){var t=document.querySelector('.q').textContent,pr=document.querySelector('.q~pre'),c=pr?pr.textContent.trim():'';var q=IT(1,3).q.filter(function(x){return x.q===t&&(x.c||'').trim()===c})[0];return q.a})()")
        wrong = pg.locator('.opt[data-k="%d"]' % ((qa + 1) % pg.locator('.opt').count()))
        wrong.click(); pg.locator('#go').click(); pg.wait_for_timeout(300)
        log = pg.evaluate("window.__sl"); dock = pg.evaluate("window.__dock")
        bad = [t for n, t in log if n == 'bad']
        ok(len(bad) == 1, 'неверный ответ: один мягкий звук «bad»')
        red = [t for c, t in dock if 'bad' in c.split()]
        ok(red and abs(red[0] - bad[0]) < 25, 'звук ошибки и покраснение панели в один момент (%.0f мс)' % abs(red[0] - bad[0]))
        pg.locator('#go').click(); pg.wait_for_timeout(300)
        # окно и переход
        pg.evaluate("window.__sl.length=0")
        pg.evaluate("streakSheet()"); pg.wait_for_timeout(300)
        ok([n for n, t in pg.evaluate("window.__sl")][:1] == ['open'], 'открытие окна: звук «open»')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        ok('close' in [n for n, t in pg.evaluate("window.__sl")], 'закрытие окна: звук «close»')
        pg.evaluate("home()"); pg.wait_for_timeout(400)
        pg.evaluate("window.__sl.length=0")
        pg.locator('#ttl').click(); pg.wait_for_timeout(400)
        ok('go' in [n for n, t in pg.evaluate("window.__sl")], 'вход в настройки: звук перехода «go»')
        pg.locator('#x').click(); pg.wait_for_timeout(400)
        ok('back' in [n for n, t in pg.evaluate("window.__sl")], 'выход из настроек: звук «back»')
        # нижняя панель: у каждого раздела своя нота, и сработал один звук
        for k, t in enumerate(('home', 'pr', 'ed', 'prof')):
            pg.evaluate("window.__sl.length=0")
            pg.locator('.nav button[data-t="%s"]' % t).click(); pg.wait_for_timeout(200)
            sl = pg.evaluate("window.__sl")
            ok([n for n, _ in sl] == ['tap'], 'раздел «%s»: ровно один звук касания, получено %s' % (t, [n for n, _ in sl]))
        # итог островка: опыт и «пройдено»
        pg.evaluate("window.__sl.length=0")
        pg.evaluate("doneScreen({title:'t',err:0,x:20,btns:'<button class=\"btn\" id=\"go\">Дальше</button>'})"); pg.wait_for_timeout(700)
        names_ = [n for n, t in pg.evaluate("window.__sl")]
        ok(names_[:2] == ['done', 'xp'], 'итог островка: «done», затем «xp» когда число начинает расти: ' + str(names_))
        # новый уровень или тема: один звук вместо каши
        pg.evaluate("window.__sl.length=0")
        pg.evaluate("doneScreen({title:'t',err:0,x:20,lv:3,btns:'<button class=\"btn\" id=\"go\">Дальше</button>'});confetti(1)"); pg.wait_for_timeout(700)
        names_ = [n for n, t in pg.evaluate("window.__sl")]
        ok('done' not in names_ and pg.evaluate("SX.per.level>0&&!SX.per.fanfare||performance.now()-SX.per.level<2000"), 'новый уровень: конфетти играет «level», а не «done»: ' + str(names_))
        # достижение: звук в момент показа карточки
        pg.evaluate("window.__sl.length=0")
        pg.evaluate("delete S.ach.first;ach('first')"); pg.wait_for_timeout(300)
        ok(pg.locator('.toast.ach').count() == 1 and 'ach' in [n for n, t in pg.evaluate("window.__sl")], 'достижение: карточка и звук «ach» вместе')
        # серия: чип в шапке растёт со звуком
        pg.evaluate("home();LSK=0;S.last='2026-10-12';S.streak=5;save()")
        pg.evaluate("window.__sl.length=0"); pg.evaluate("home()"); pg.wait_for_timeout(300)
        ok('streak' in [n for n, t in pg.evaluate("window.__sl")], 'серия выросла: звук «streak» вместе с анимацией чипа')
        # подсказка
        pg.evaluate("S.d['1-3']=1;S.hc=1;go(1,4)"); pg.wait_for_timeout(400)
        pg.evaluate("window.__sl.length=0"); pg.locator('#hb').click(); pg.wait_for_timeout(300)
        ok('hint' in [n for n, t in pg.evaluate("window.__sl")], 'подсказка: звук «hint»')
        ok(not [l for l in logs if 'PAGEERROR' in l], 'ошибок нет ' + str(logs[:2]))
        b.close()


if __name__ == '__main__':
    run()
    print('OK')
