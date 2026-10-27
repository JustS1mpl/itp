"""Проверка интерфейса v6 по-настоящему: нажатия, ввод, проверка кода в Pyodide.
Запуск из корня репозитория после сборки: python3 tests/ui6.py [файл.html]
Проходит путь нового ученика и основные экраны, падает на первой ошибке."""
import os, sys, json, re
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(__file__))
import h
W = os.getcwd() + '/'
F = sys.argv[1] if len(sys.argv) > 1 else W + 'out5.html'
SHOT = os.environ.get('SHOT')  # папка для снимков экрана (необязательно)


# верный ответ на текущий вопрос: по тексту вопроса и коду под ним (у многих вопросов одинаковый текст)
CUR_A = """(function(){var t=document.querySelector('.q').textContent,pr=document.querySelector('.q~pre'),c=pr?pr.textContent.trim():'';
var q=IT(%d,%d).q.filter(function(x){return x.q===t&&(x.c||'').trim()===c})[0];return q?q.a:0})()"""


def snap(pg, name):
    if SHOT:
        pg.wait_for_timeout(450)
        pg.screenshot(path=os.path.join(SHOT, name + '.png'))


def ok(cond, msg):
    if not cond:
        raise AssertionError(msg)
    print('  ✓', msg)


def no_hscroll(pg, where):
    o = pg.evaluate("[document.documentElement.scrollWidth, innerWidth]")
    ok(o[0] <= o[1], 'нет горизонтальной прокрутки: ' + where + ' ' + str(o))


def tap(pg, sel):
    pg.locator(sel).first.click()
    pg.wait_for_timeout(200)


def run(theme='light', w=390):
    with sync_playwright() as p:
        b, ctx, pg, logs = h.open_page(p, F, None, w, 820, touch=True, color_scheme=theme)
        pg.wait_for_timeout(1800)
        print('== тема', theme, 'ширина', w)
        # --- знакомство (v5/a_boot.js): заставка, терминал, синий экран. Касание пропускает заставку (если звук ещё не разрешён,
        # первое касание только включает его, пропускает второе) и допечатывает реплики
        ok(pg.locator('#crt .spl').count() == 1, 'заставка перед терминалом')
        snap(pg, '00_splash_' + theme)
        tap(pg, '#crt')
        tap(pg, '#crt')
        pg.wait_for_selector('#nk', timeout=20000)
        ok('off' in (pg.get_attribute('#go', 'class') or ''), '«Дальше» приглушено без ника (кнопка не выключается: так надёжнее на экранных клавиатурах)')
        pg.fill('#nk', 'Тестер')
        snap(pg, '01_nick_' + theme)
        tap(pg, '#go')
        pg.wait_for_selector('.tgd[data-g="f"]', timeout=15000)
        tap(pg, '.tgd[data-g="f"]')
        pg.wait_for_selector('.tpc.rec', timeout=15000)
        ok(pg.locator('.tpc').count() == pg.evaluate("TOPICS.filter(function(t){return!t.intro&&!t.opt}).length"), 'на выборе старта все темы из TOPICS')
        snap(pg, '02_place_' + theme)
        tap(pg, '.tpc.rec')
        # пункт меню подтверждается с подсветкой 280 мс (crtMenu → pick), поэтому ждём, а не проверяем сразу
        pg.wait_for_function("S.start>=0", timeout=3000)
        ok(pg.evaluate("S.start") == 0 and pg.evaluate("S.g") == 'f', 'старт с нуля, обращение сохранено')
        pg.wait_for_selector('#bsod:not(.blk)', timeout=15000)
        snap(pg, '03_bsod_' + theme)
        tap(pg, '#bsod')  # касание сразу открывает Путь
        pg.wait_for_function("!document.getElementById('crt')&&!document.getElementById('bsod')&&!document.getElementById('shards')", timeout=10000)
        # --- вводный островок
        ok(pg.locator('.topic.intro').count() == 1, 'видна только вводная тема')
        tap(pg, '.topic.intro .isl')
        ok(pg.locator('.ipop').count() == 1, 'нажатие на островок открывает карточку')
        snap(pg, '03_intro_pop_' + theme)
        pg.wait_for_timeout(500)
        ar = pg.evaluate("(function(){var o=document.querySelector('.ipop'),i=document.querySelector('.isl.sel');var r=i.getBoundingClientRect(),q=o.getBoundingClientRect();return Math.abs(q.left+parseFloat(getComputedStyle(o).getPropertyValue('--ax'))-(r.left+r.width/2))})()")
        ok(ar < 1, 'стрелка карточки точно на центр островка (отклонение %.1f px)' % ar)
        tap(pg, '#ipg')
        ok('И так, программирование' in pg.inner_text('#tb') or pg.evaluate("S.set.ty"), 'теория введения открыта')
        pg.evaluate("var e=document.getElementById('tb');e&&e.click()")  # показать текст сразу
        ok('И так, программирование' in pg.inner_text('#tb'), 'во введении новое название')
        tap(pg, '#go')
        pg.wait_for_timeout(5500)  # эффект «введение → курс»
        ok(pg.locator('.topic:not(.intro)').count() == pg.evaluate("TOPICS.filter(function(t){return!t.intro&&!t.opt}).length"), 'после введения появились все темы (доп. главы это отдельные кнопки .bur)')
        ok(pg.locator('.isl.cur').count() == 1, 'есть текущий островок')
        ok(pg.locator('.gcard #gc').count() == 1, 'на карточке дня есть «Начать»')
        snap(pg, '04_home_' + theme)
        no_hscroll(pg, 'Путь')
        # --- теория из «Продолжить»
        tap(pg, '#gc')
        ok(pg.locator('article.th').count() == 1, '«Начать» ведёт в текущий островок (теория)')
        pg.evaluate("var e=document.getElementById('tb');e&&e.click()")
        if pg.locator('.term').count():
            tap(pg, '.term')
            ok(pg.locator('.modal').count() == 1, 'термин открывает описание')
            pg.keyboard.press('Escape')
            pg.wait_for_timeout(300)
            ok(pg.locator('.modal').count() == 0, 'Esc закрывает окно')
        snap(pg, '05_theory_' + theme)
        tap(pg, '#go')
        ok(pg.evaluate("S.d['1-0']") == 1, 'теория отмечена пройденной')
        # --- вопросы: ошибка, затем все верно, работа над ошибками
        tap(pg, '#gc')
        ok(pg.locator('.opt').count() >= 2, 'островок с вопросами')
        tot = pg.evaluate("IT(1,1).q.length")
        first = True
        for n in range(tot + 3):
            if pg.locator('.opt').count() == 0:
                break
            qa = pg.evaluate(CUR_A % (1, 1))
            pick = qa if not first else (qa + 1) % pg.locator('.opt').count()
            pg.locator('.opt[data-k="%d"]' % pick).click()
            tap(pg, '#go')
            if first:
                ok(pg.locator('#dock.bad').count() == 1, 'неверный ответ: док красный, есть пояснение')
                snap(pg, '06_quiz_bad_' + theme)
                first = False
            tap(pg, '#go')
            pg.wait_for_timeout(150)
        ok(pg.locator('.fin').count() == 1, 'экран итога островка')
        pg.wait_for_timeout(1400)
        snap(pg, '07_done_' + theme)
        ok(pg.evaluate("S.xp") > 0, 'опыт начислен: ' + str(pg.evaluate("S.xp")))
        ok(pg.evaluate("S.es['1-1']") == 1, 'ошибка записана в статистику')
        tap(pg, '#go')
        # --- задание с кодом: неверно, потом эталон
        pg.evaluate("go(1,2)")  # теория 1-2
        tap(pg, '#go')
        pg.evaluate("go(1,3)")
        for n in range(40):
            if pg.locator('.opt').count() == 0:
                break
            qa = pg.evaluate(CUR_A % (1, 3))
            pg.locator('.opt[data-k="%d"]' % qa).click()
            tap(pg, '#go')
            tap(pg, '#go')
        tap(pg, '#go')
        pg.evaluate("BACK=home;go(1,4)")
        ok(pg.locator('#code').count() == 1 and pg.locator('#chk').count() == 1, 'задание с кодом: редактор и «Проверить»')
        pg.evaluate("var c=document.getElementById('code');c.value='print(\"zzz\")';c.dispatchEvent(new Event('input',{bubbles:true}))")
        tap(pg, '#run')
        pg.wait_for_function("document.getElementById('o')&&/zzz/.test(document.getElementById('o').textContent)", timeout=60000)
        ok(not pg.locator('#cons').is_hidden(), 'консоль появилась после «Запустить»')
        tap(pg, '#chk')
        pg.wait_for_selector('#fb .fb.bad', timeout=60000)
        ok(True, 'неверный код: сообщение «Не прошёл тест»')
        snap(pg, '08_task_bad_' + theme)
        T = pg.evaluate("IT(1,4).tasks.length")
        for k in range(T):
            pg.evaluate("var c=document.getElementById('code');c.value=IT(1,4).tasks[%d].sol;c.dispatchEvent(new Event('input',{bubbles:true}))" % k)
            tap(pg, '#chk')
            pg.wait_for_selector('#nx', timeout=60000)
            tap(pg, '#nx')
        ok(pg.locator('.fin').count() == 1, 'все задания решены: экран итога')
        ok(pg.evaluate("S.d['1-4']") == 1, 'островок с кодом пройден')
        tap(pg, '#go')
        # --- проект: пропуск из карточки островка
        pg.evaluate("home()")
        pg.wait_for_timeout(300)
        pg.evaluate("document.querySelector('.isl[data-i=\"1\"][data-j=\"5\"]').scrollIntoView({block:'center'})")
        tap(pg, '.isl[data-i="1"][data-j="5"]')
        ok(pg.locator('#ips').count() == 1, 'у проекта в карточке есть «Пропустить»')
        tap(pg, '#ips')
        ok(pg.evaluate("S.at['1-5']") == 'skip', 'проект пропущен, тема засчитана: ' + str(pg.evaluate("tdone(1)")))
        pg.wait_for_timeout(3500)
        # --- закрытый островок объясняет, почему закрыт
        pg.evaluate("home()")
        pg.wait_for_timeout(300)
        pg.evaluate("document.querySelector('.isl.lk').scrollIntoView({block:'center'})")
        tap(pg, '.isl.lk')
        ok('Откроется' in pg.inner_text('.ipop'), 'закрытый островок: понятное объяснение')
        tap(pg, '#ipc')
        # --- практика
        tap(pg, '.nav button[data-t="pr"]')
        ok(pg.locator('.pcard').count() == 3, 'практика: три режима')
        snap(pg, '09_practice_' + theme)
        tap(pg, '.pcard[data-a="r3"]')
        for n in range(3):
            pg.locator('.opt').first.click()
            tap(pg, '#go')
            tap(pg, '#go')
        ok(pg.locator('.fin').count() == 1, 'разминка завершилась экраном итога')
        tap(pg, '#go')
        # --- раздел «Код»: ввод, остановка, меню файла
        tap(pg, '.nav button[data-t="ed"]')
        pg.evaluate("var c=document.getElementById('code');c.value='a = input(\"Имя? \")\\nprint(\"Привет,\", a)';c.dispatchEvent(new Event('input',{bubbles:true}))")
        tap(pg, '#run')
        pg.wait_for_selector('#ir.on', timeout=60000)
        pg.fill('#ii', 'Мир')
        pg.press('#ii', 'Enter')
        pg.wait_for_function("/Привет, Мир/.test(document.getElementById('o').textContent)", timeout=30000)
        ok(True, 'программа с input(): ввод и вывод работают')
        snap(pg, '10_editor_' + theme)
        pg.evaluate("var c=document.getElementById('code');c.value='i = 0\\nwhile True:\\n    i += 1';c.dispatchEvent(new Event('input',{bubbles:true}))")
        tap(pg, '#run')
        pg.wait_for_timeout(1500)
        ok('Остановить' in pg.inner_text('#run'), 'бесконечный цикл: кнопка «Остановить»')
        tap(pg, '#run')
        pg.wait_for_function("/остановлена/.test(document.getElementById('o').textContent)", timeout=20000)
        ok(True, 'цикл остановлен, страница не зависла')
        tap(pg, '#fn')
        ok(pg.locator('.acts .li').count() == 5, 'меню файла: 5 действий')
        snap(pg, '11_filemenu_' + theme)
        pg.locator('.acts .li').first.click()  # Сохранить
        pg.wait_for_timeout(300)
        pg.fill('#mi', 'Цикл')
        pg.locator('.mb .btn').first.click()
        pg.wait_for_timeout(300)
        ok(any(x['n'] == 'Цикл' for x in pg.evaluate("S.sv")), 'код сохранён под именем')
        tap(pg, '#fn')
        pg.locator('.acts .li').nth(2).click()  # Мои коды
        pg.wait_for_timeout(300)
        ok(pg.locator('.sr').count() == 1, 'список «Мои коды»')
        tap(pg, '.sr .icon')
        ok(pg.locator('.acts .li').count() == 5, 'меню действий кода')
        pg.locator('.acts .li').nth(4).click()  # Удалить
        pg.wait_for_timeout(300)
        pg.locator('.mb .btn').first.click()
        pg.wait_for_timeout(300)
        ok(pg.evaluate("S.sv.length") == 0, 'код удалён')
        # --- профиль, словарь, настройки
        tap(pg, '.nav button[data-t="prof"]')
        ok('Получено: ' in pg.inner_text('.shelfc') and ' из ' not in pg.inner_text('.sh-h'), 'достижения: только «Получено: N»')
        no_hscroll(pg, 'Профиль')
        snap(pg, '12_profile_' + theme)
        tap(pg, '.li[data-a="dc"]')
        ok(pg.locator('.de').count() > 0, 'словарь изученных функций')
        pg.fill('#dq', 'print')
        pg.wait_for_timeout(200)
        ok('Найдено' in pg.inner_text('#dm'), 'поиск по словарю')
        tap(pg, '#x')
        tap(pg, '#ttl')
        ok(pg.locator('h1').first.inner_text() == 'Настройки', '«ИТП» слева сверху открывает настройки')
        ok(not pg.evaluate("NAV.classList.contains('on')"), 'в настройках нет нижней панели')
        snap(pg, '13_settings_' + theme)
        for n in range(12):
            pg.evaluate("document.getElementById('egv').closest('.li').click()")
        pg.wait_for_timeout(300)
        ok(pg.evaluate("!!S.ach.egg") and pg.locator('.egg').count() == 1, 'пасхалка: 12 нажатий на версию')
        pg.keyboard.press('Escape')
        pg.wait_for_timeout(300)
        tap(pg, '.li[data-a="intro"]')
        ok(pg.locator('article.th').count() == 1, 'введение можно перечитать из настроек')
        tap(pg, '#x')
        ok(pg.locator('h1').first.inner_text() == 'Настройки', 'назад из введения возвращает в настройки')
        # --- режим разработчика
        pg.evaluate("S.nick=DVN;save()")
        pg.wait_for_timeout(900)
        ok(pg.locator('#dvb').count() == 1, 'режим разработчика: кнопка появилась')
        pg.evaluate("S.nick='Тестер';save()")
        errs = [l for l in logs if 'PAGEERROR' in l or l.startswith('error')]
        ok(not errs, 'нет ошибок в консоли: ' + str(errs[:3]))
        b.close()


if __name__ == '__main__':
    for th in ('light', 'dark'):
        run(th)
    print('OK')
