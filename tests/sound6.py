"""Проверка звука ИТП в приложении (нужны Playwright и numpy). Запуск из корня после сборки: python3 tests/sound6.py [файл.html]
Сами звуки (форма, пик, спектр, WAV) меряет tests/sound_wav.py; здесь проверяется поведение:
1) контекст создаётся только после первого касания, выключенный звук и «Звуки интерфейса» молчат;
2) нет Web Audio, браузер блокирует звук, вкладка скрыта, беззвучный режим: ничего не ломается и не копится;
3) звуки вызываются в тот же момент, что и события (ответ, опыт, окно, переход, подсказка, серия, достижение, запуск и ошибка кода);
4) настройки: громкость, выключатели on/off, «Звуки набора кода» (по умолчанию выключено), старые сохранения читаются."""
import os, sys, json
import numpy as np
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(__file__))
import h
W = os.getcwd() + '/'
F = sys.argv[1] if len(sys.argv) > 1 else W + 'out5.html'
ST = {'nick': 'Т', 'start': 0, 'seen': '2000-01-01', 'last': '2026-10-11', 'streak': 3, 'mv': 2, 'd': {'0-0': 1, '1-0': 1}}


def ok(c, m):
    if not c:
        raise AssertionError(m)
    print('  ✓', m)


# запись всех обращений к Web Audio и вызовов snd
HOOK = """
window.__ac=0;window.__osc=0;window.__src=0;window.__sl=[];
(function(){var A=window.AudioContext;if(!A)return;
 window.AudioContext=function(o){window.__ac++;return new A(o)};window.AudioContext.prototype=A.prototype;
 var st=OscillatorNode.prototype.start;OscillatorNode.prototype.start=function(){window.__osc++;return st.apply(this,arguments)};
 var sb=AudioBufferSourceNode.prototype.start;AudioBufferSourceNode.prototype.start=function(){window.__src++;return sb.apply(this,arguments)}})();
"""
WRAP = """(function(){var o=window.snd;window.snd=function(x,a){window.__sl.push([typeof x==='string'?x:JSON.stringify(x),performance.now(),a?JSON.stringify(a):'']);return o.apply(this,arguments)}})()"""


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


def names(pg):
    return [n for n, t, a in pg.evaluate("window.__sl")]


def run():
    with sync_playwright() as p:
        # ---- 1. набор звуков и их отрисовка без динамиков
        b, ctx, pg, logs = h.open_page(p, F, ST, 390, 820)
        pg.wait_for_timeout(1500)
        snames = pg.evaluate("Object.keys(SXD)")
        print('== звуки:', ' '.join(snames))
        for need in ('tap', 'tick', 'on', 'off', 'lock', 'run', 'err', 'key', 'go', 'back', 'open', 'close', 'ok', 'solve', 'bad', 'hint', 'xpt', 'done', 'level', 'fanfare', 'streak', 'ach', 'freeze', 'unlock', 'disk', 'theory', 'pet'):
            ok(need in snames, 'есть звук «%s»' % need)
        for n in snames:
            a = {'nav': 1} if n == 'tap' else None
            s = np.array(pg.evaluate("sndRender(%s,%s)" % (json.dumps(n), json.dumps(a))), dtype=float)
            ok(len(s) > 0 and np.isfinite(s).all() and s[0] == 0 and s[-1] == 0 and np.abs(s).max() < .3, 'звук «%s» отрисован: начало и конец ровно 0, пик %.1f дБ' % (n, 20 * np.log10(np.abs(s).max())))
        ok(pg.evaluate("typeof sndRender")=='function' and pg.evaluate("S.set.ks")==0, 'по умолчанию «Звуки набора кода» выключены, громкость %d %%' % pg.evaluate("S.set.vol"))
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
        ok(pg.evaluate("window.__osc") > 0, 'первое же касание уже играет звук (не теряется)')
        b.close()

        # ---- 3a. звук выключен: полная тишина и ни одной ошибки
        st = dict(ST, mute=1)
        b, ctx, pg, logs = page(p, HOOK, st)
        pg.wait_for_timeout(1200)
        for sel in ('.nav button[data-t="home"]', '.nav button[data-t="pr"]', '.nav button[data-t="prof"]', '#ttl'):
            if pg.locator(sel).count():
                pg.locator(sel).first.click()
                pg.wait_for_timeout(250)
        pg.evaluate("snd('ok');snd('ach');snd('level');snd('go');snd('key',{k:0})")
        ok(pg.evaluate("window.__osc+window.__src") == 0, 'звук выключен: ни один источник звука не запущен')
        ok(not [l for l in logs if 'PAGEERROR' in l], 'звук выключен: ошибок нет')
        b.close()

        # ---- 3b. «Звуки интерфейса» выключены: интерфейс молчит, награды звучат
        st = dict(ST, set={'sfx': 0})
        b, ctx, pg, logs = page(p, HOOK, st)
        pg.wait_for_timeout(1200)
        tap1(pg)
        pg.locator('.nav button[data-t="pr"]').click()
        pg.wait_for_timeout(300)
        n0 = pg.evaluate("window.__osc+window.__src")
        pg.evaluate("snd('tap');snd('go');snd('open');snd('close');snd('on');snd('off');snd('run')")
        ok(pg.evaluate("window.__osc+window.__src") == n0, 'звуки интерфейса выключены: касания, переходы, окна и переключатели молчат')
        pg.evaluate("snd('ok')")
        ok(pg.evaluate("window.__osc+window.__src") > n0, 'но ответы и награды звучат')
        b.close()

        # ---- 3c. нет Web Audio совсем (старый браузер): всё работает
        kill = "window.AudioContext=undefined;window.webkitAudioContext=undefined;window.OfflineAudioContext=undefined;"
        b, ctx, pg, logs = page(p, kill)
        pg.wait_for_timeout(1200)
        tap1(pg)
        pg.evaluate("snd('ok');snd('bad');snd('ach');snd('done');snd('level');snd('xpt',{k:3});snd('key',{k:1})")
        pg.evaluate("go(1,1)"); pg.wait_for_timeout(300)
        pg.locator('.opt').first.click(); pg.locator('#go').click(); pg.wait_for_timeout(300)
        ok(pg.locator('#dock.ok,#dock.bad').count() == 1, 'без Web Audio вопрос проверяется как обычно')
        pg.evaluate("home();settings()"); pg.wait_for_timeout(300)
        ok(pg.locator('h1').first.inner_text() == 'Настройки', 'без Web Audio открываются настройки')
        ok(not [l for l in logs if 'PAGEERROR' in l], 'без Web Audio: ошибок нет ' + str(logs[:2]))
        b.close()

        # ---- 3d. браузер блокирует звук: контекст остаётся suspended, resume не срабатывает
        block = """(function(){var A=window.AudioContext;window.__res=0;window.__osc=0;
          window.AudioContext=function(o){var c=new A(o);c.resume=function(){window.__res++;return new Promise(function(){})};c.suspend=function(){return Promise.resolve()};
            Object.defineProperty(c,'state',{get:function(){return'suspended'}});return c};window.AudioContext.prototype=A.prototype;
          var st=OscillatorNode.prototype.start;OscillatorNode.prototype.start=function(){window.__osc++;return st.apply(this,arguments)}})();"""
        b, ctx, pg, logs = page(p, block)
        pg.wait_for_timeout(1200)
        tap1(pg)
        for i in range(30):
            pg.evaluate("snd('ok');snd('tap')"); pg.wait_for_timeout(30)
        pg.evaluate("go(1,1)"); pg.wait_for_timeout(300)
        pg.locator('.opt').first.click(); pg.locator('#go').click(); pg.wait_for_timeout(300)
        ok(pg.locator('#dock.ok,#dock.bad').count() == 1, 'звук заблокирован: вопросы проверяются как обычно')
        ok(pg.evaluate("window.__osc") == 0, 'звук заблокирован: звуки не копятся и не проигрываются «пачкой» позже (источников: %d)' % pg.evaluate("window.__osc"))
        ok(not [l for l in logs if 'PAGEERROR' in l], 'звук заблокирован: ошибок нет ' + str(logs[:2]))
        b.close()

        # ---- 3e. конструктор AudioContext бросает исключение
        boom = "window.AudioContext=function(){throw new Error('blocked')};window.webkitAudioContext=undefined;"
        b, ctx, pg, logs = page(p, boom)
        pg.wait_for_timeout(1000)
        tap1(pg)
        pg.evaluate("snd('ok');snd('ach')")
        ok(pg.evaluate("SX.dead") is True, 'исключение при создании контекста: звук отключён тихо')
        ok(not [l for l in logs if 'PAGEERROR' in l], 'исключение контекста: ошибок на странице нет')
        b.close()

        # ---- 3f. скрытая вкладка: всё обрывается, контекст засыпает, при возврате просыпается
        b, ctx, pg, logs = page(p, HOOK + "window.__as=null;navigator.audioSession={type:'auto'};")
        pg.wait_for_timeout(1000)
        tap1(pg)
        pg.wait_for_function("SX.c&&SX.c.state==='running'", timeout=5000)
        ok(pg.evaluate("navigator.audioSession.type") == 'ambient', 'беззвучный режим телефона учитывается: audioSession.type = ambient')
        pg.evaluate("snd('ach')"); pg.wait_for_timeout(100)
        pg.evaluate("Object.defineProperty(document,'hidden',{value:true,configurable:true});document.dispatchEvent(new Event('visibilitychange'))")
        pg.wait_for_function("SX.c.state==='suspended'", timeout=3000)
        ok(pg.evaluate("SX.x.voices.length") == 0, 'вкладка скрыта: все голоса оборваны, контекст приостановлен')
        o0 = pg.evaluate("window.__osc+window.__src")
        pg.evaluate("snd('ok');snd('tap');snd('ach')")
        ok(pg.evaluate("window.__osc+window.__src") == o0, 'на скрытой вкладке новые звуки не запускаются')
        pg.evaluate("Object.defineProperty(document,'hidden',{value:false,configurable:true});document.dispatchEvent(new Event('visibilitychange'))")
        pg.wait_for_function("SX.c.state==='running'", timeout=3000)
        ok(True, 'вкладка вернулась: контекст снова running без нового касания')
        pg.wait_for_timeout(100)
        pg.evaluate("snd('ok')")
        ok(pg.evaluate("window.__osc") > 0, 'после возвращения звуки снова играют')
        ok(not [l for l in logs if 'PAGEERROR' in l], 'скрытая вкладка: ошибок нет')
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
        bad = [t for n, t, a in log if n == 'bad']
        ok(len(bad) == 1, 'неверный ответ: один мягкий звук «bad»')
        red = [t for c, t in dock if 'bad' in c.split()]
        ok(red and abs(red[0] - bad[0]) < 25, 'звук ошибки и покраснение панели в один момент (%.0f мс)' % abs(red[0] - bad[0]))
        pg.locator('#go').click(); pg.wait_for_timeout(300)
        # окно и переход
        pg.evaluate("window.__sl.length=0")
        pg.evaluate("streakSheet()"); pg.wait_for_timeout(300)
        ok(names(pg)[:1] == ['open'], 'открытие окна: звук «open»')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        ok('close' in names(pg), 'закрытие окна: звук «close»')
        pg.evaluate("home()"); pg.wait_for_timeout(400)
        pg.evaluate("window.__sl.length=0")
        pg.locator('#ttl').click(); pg.wait_for_timeout(400)
        ok('go' in names(pg), 'вход в настройки: звук перехода «go»')
        # переключатели в настройках: вниз при выключении, вверх при включении
        pg.evaluate("window.__sl.length=0")
        pg.locator('.sw[data-k="gc"]').click(); pg.wait_for_timeout(150)
        ok(names(pg) == ['off'], 'переключатель выключен: один звук «off», без касания: ' + str(names(pg)))
        pg.evaluate("window.__sl.length=0")
        pg.locator('.sw[data-k="gc"]').click(); pg.wait_for_timeout(150)
        ok(names(pg) == ['on'], 'переключатель включён: один звук «on»: ' + str(names(pg)))
        pg.evaluate("window.__sl.length=0")
        pg.locator('.sw[data-k="mute"]').click(); pg.wait_for_timeout(150)
        ok(names(pg) == ['off'] and pg.evaluate("S.mute") == 1, 'главный выключатель «Звук»: перед выключением звучит «off»')
        pg.evaluate("window.__sl.length=0")
        pg.locator('.sw[data-k="mute"]').click(); pg.wait_for_timeout(150)
        ok(names(pg) == ['on'] and pg.evaluate("S.mute") == 0, 'и «on» при включении')
        # громкость: ползунок меняет усиление шины
        pg.evaluate("var v=document.getElementById('vol');v.value=35;v.dispatchEvent(new Event('input'))"); pg.wait_for_timeout(200)
        g = pg.evaluate("SX.x.mst.gain.value")
        ok(abs(g - pg.evaluate("sxGain(35)")) < .02 and pg.evaluate("S.set.vol") == 35, 'ползунок громкости: усиление %.2f, сохранено 35 %%' % g)
        pg.evaluate("var v=document.getElementById('vol');v.value=70;v.dispatchEvent(new Event('input'))")
        # выключатель печати есть, по умолчанию выключен
        ok(pg.locator('.sw[data-k="ks"]').get_attribute('aria-checked') == 'false', 'выключатель «Звуки набора кода» есть и выключен')
        pg.locator('#x').click(); pg.wait_for_timeout(400)
        ok('back' in names(pg), 'выход из настроек: звук «back»')
        # нижняя панель: у каждого раздела своя высота, и сработал один звук
        for k, t in enumerate(('home', 'pr', 'ed', 'prof')):
            pg.evaluate("window.__sl.length=0")
            pg.locator('.nav button[data-t="%s"]' % t).click(); pg.wait_for_timeout(200)
            sl = pg.evaluate("window.__sl")
            ok([n for n, _, _ in sl] == ['tap'] and json.loads(sl[0][2])['nav'] == k, 'раздел «%s»: ровно один звук касания с высотой раздела %d' % (t, k))
        # запуск кода и ошибка (редактор)
        pg.locator('.nav button[data-t="ed"]').click(); pg.wait_for_timeout(500)
        pg.evaluate("window.__sl.length=0")
        pg.evaluate("document.getElementById('code').value='print(1';document.getElementById('code').dispatchEvent(new Event('input'))")
        pg.locator('#run').click(); pg.wait_for_timeout(500)
        ok(names(pg) == ['run', 'err'] or names(pg)[:1] == ['run'] and 'err' in names(pg), 'запуск с синтаксической ошибкой: «run», затем мягкий «err»: ' + str(names(pg)))
        pg.evaluate("window.__sl.length=0")
        pg.evaluate("document.getElementById('code').value='print(1/0)';document.getElementById('code').dispatchEvent(new Event('input'))")
        pg.locator('#run').click()
        pg.wait_for_function("document.getElementById('rst')&&/Программа завершилась с ошибкой/.test(document.getElementById('rst').textContent)", timeout=90000)
        pg.wait_for_timeout(200)
        nm = names(pg)
        ok(nm[0] == 'run' and nm.count('err') == 1 and 'tap' not in nm, 'запуск с ошибкой выполнения: «run», один «err», без лишнего касания: ' + str(nm))
        pg.evaluate("window.__sl.length=0")
        pg.evaluate("document.getElementById('code').value='print(2)';document.getElementById('code').dispatchEvent(new Event('input'))")
        pg.locator('#run').click()
        pg.wait_for_function("document.getElementById('rst')&&/✓/.test(document.getElementById('rst').textContent)", timeout=60000)
        pg.wait_for_timeout(200)
        nm = names(pg)
        ok(nm == ['run'], 'успешный запуск: только «run»: ' + str(nm))
        # печать в редакторе: по умолчанию тихо
        pg.evaluate("window.__sl.length=0")
        pg.locator('#code').click(); pg.keyboard.type('abc'); pg.wait_for_timeout(100)
        pg.evaluate("window.__osc=0"); pg.keyboard.type('def'); pg.wait_for_timeout(100)
        ok(pg.evaluate("window.__osc") == 0, 'печать в редакторе по умолчанию без звука (ни одного осциллятора)')
        pg.evaluate("S.set.ks=1;save()")
        pg.evaluate("window.__sl.length=0;window.__osc=0")
        pg.keyboard.type('xy'); pg.wait_for_timeout(120)
        ok(names(pg).count('key') >= 1 and pg.evaluate("window.__osc") > 0, 'с включённым «Звуки набора кода» буквы дают тихий щелчок: ' + str(names(pg)))
        pg.evaluate("window.__sl.length=0;window.__osc=0")
        pg.keyboard.press('Enter'); pg.keyboard.press('Backspace'); pg.wait_for_timeout(120)
        ok(names(pg).count('key') >= 1, 'Enter и стирание тоже')
        pg.evaluate("S.set.ks=0;save()")
        # итог островка: «пройдено», затем опыт ступенями
        pg.evaluate("home()"); pg.wait_for_timeout(300)
        pg.evaluate("window.__sl.length=0")
        pg.evaluate("doneScreen({title:'t',err:0,x:20,btns:'<button class=\"btn\" id=\"go\">Дальше</button>'})"); pg.wait_for_timeout(1200)
        sl = pg.evaluate("window.__sl")
        nm = [n for n, t, a in sl]
        ok(nm[:1] == ['done'] and nm.count('xpt') >= 5, 'итог островка: «done», затем тики опыта (%d шт.)' % nm.count('xpt'))
        ks = [json.loads(a)['k'] for n, t, a in sl if n == 'xpt']
        ok(ks == list(range(len(ks))), 'тики опыта идут ступенями 0,1,2…: ' + str(ks))
        ok(len(ks) <= 14, 'тиков опыта не больше 14 за счёт (%d)' % len(ks))
        # новый уровень: один звук вместо каши
        pg.evaluate("window.__sl.length=0;window.__t0=performance.now()")
        pg.evaluate("doneScreen({title:'t',err:0,x:20,lv:3,btns:'<button class=\"btn\" id=\"go\">Дальше</button>'});confetti(1)"); pg.wait_for_timeout(700)
        per = pg.evaluate("[SX.per.level||0,SX.per.done||0,SX.per.fanfare||0,window.__t0]")
        ok(per[0] >= per[3] and per[1] < per[3] and per[2] < per[3], 'новый уровень: играет «level», а не «done» или «fanfare»')
        # достижение: звук в момент показа карточки
        pg.evaluate("window.__sl.length=0")
        pg.evaluate("delete S.ach.first;ach('first')"); pg.wait_for_timeout(300)
        ok(pg.locator('.toast.ach').count() == 1 and 'ach' in names(pg), 'достижение: карточка и звук «ach» вместе')
        # серия: чип в шапке растёт со звуком
        pg.evaluate("home();LSK=0;S.last='2026-10-12';S.streak=5;save()")
        pg.evaluate("window.__sl.length=0"); pg.evaluate("home()"); pg.wait_for_timeout(300)
        ok('streak' in names(pg), 'серия выросла: звук «streak» вместе с анимацией чипа')
        # подсказка
        pg.evaluate("S.d['1-3']=1;S.hc=1;go(1,4)"); pg.wait_for_timeout(400)
        pg.evaluate("window.__sl.length=0"); pg.locator('#hb').click(); pg.wait_for_timeout(300)
        ok('hint' in names(pg), 'подсказка: звук «hint»')
        ok(not [l for l in logs if 'PAGEERROR' in l], 'ошибок нет ' + str(logs[:2]))
        b.close()

        # ---- 5. настройки и совместимость сохранений
        old = dict(ST, set={'vol': 35, 'sfx': 0, 'tz': 115, 'acc': 'blue'}, mute=0)   # сохранение без поля ks
        b, ctx, pg, logs = page(p, None, old)
        pg.wait_for_timeout(1200)
        s = pg.evaluate("S.set")
        ok(s['ks'] == 0 and s['vol'] == 35 and s['sfx'] == 0 and s['tz'] == 115 and s['acc'] == 'blue', 'старое сохранение: прежние настройки целы, «набор» по умолчанию 0: ' + json.dumps(s))
        ok(pg.evaluate("S.d['1-0']") == 1 and pg.evaluate("S.streak") == 3, 'прогресс (острова, серия) не тронут')
        pg.evaluate("S.set.ks=1;save()")
        ok(pg.evaluate("clean(JSON.parse(localStorage.getItem('pyshag2'))).set.ks") == 1 and pg.evaluate("JSON.parse(localStorage.getItem('pyshag2')).set.ks") == 1, 'включённый «набор» записан в сохранение и читается при загрузке (clean)')
        pg.evaluate("S.set=clean({set:{ks:'yes',vol:500}}).set")
        ok(pg.evaluate("S.set.ks") == 0 and pg.evaluate("S.set.vol") == 70, 'мусор в настройках звука заменяется значениями по умолчанию')
        b.close()


if __name__ == '__main__':
    run()
    print('OK')
