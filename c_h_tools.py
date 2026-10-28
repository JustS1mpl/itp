from dsl import *

# Нора после «Итоговые проекты»: инструменты настоящего проекта. Три теории: окружение и пакеты (venv, pip, requirements.txt,
# pyinstaller — команды для компьютера, в приложении не запускаются); логи (logging в stdout с форматом без времени — иначе вывод
# не проверить); тесты (assert, функции test_ в стиле pytest, свой мини-запускатель).

REQ = 'requests==2.32.3\nnumpy==2.2.5\n# графики\nmatplotlib>=3.8\npandas==2.3.3\nnumpy==2.1.0\n'


def th_env():
    terms = [
        ('виртуальное окружение', 'Отдельная папка со своим Python и своими пакетами для одного проекта (python -m venv .venv). '
                                  'Пакеты одного проекта не мешают другому.'),
        ('pip', 'Установщик пакетов: pip install имя, pip install -r requirements.txt, pip freeze — список установленного с версиями.'),
        ('requirements.txt', 'Файл со списком пакетов проекта, по строке на пакет: requests==2.32.3. По нему любой поставит те же версии.'),
        ('pyinstaller', 'Программа, которая собирает .py в один исполняемый файл: pyinstaller --onefile main.py. Python на другом '
                        'компьютере тогда не нужен.'),
    ]
    body = (
        '<p>Большой проект живёт не в одном файле и не только на твоём компьютере. Чтобы его мог запустить другой человек — или ты через год, — '
        'нужны три вещи: отдельное окружение, список пакетов и, по желанию, сборка в программу. Всё это делается командами в терминале '
        'компьютера; в браузере ИТП они не запускаются.</p>'
        '<p>[[виртуальное окружение]] — своя папка с Python и пакетами для проекта. Создают и включают его так:</p>'
        '<pre>python -m venv .venv\n.venv\\Scripts\\activate        (Windows)\nsource .venv/bin/activate     (macOS, Linux)</pre>'
        '<p>Пакеты ставит [[pip]], а их список с версиями хранят в [[requirements.txt]] — тогда проект у всех работает одинаково:</p>'
        '<pre>pip install requests pandas\npip freeze &gt; requirements.txt\npip install -r requirements.txt</pre>'
        '<p>Знак <code>==</code> фиксирует точную версию, <code>&gt;=</code> — «не ниже». Строки с # — комментарии.</p>'
        '<p>Чтобы отдать программу тому, у кого нет Python, её собирают [[pyinstaller]]:</p>'
        '<pre>pip install pyinstaller\npyinstaller --onefile main.py\n# готовая программа — в папке dist</pre>'
    )
    return th('Окружение и пакеты', terms, body)


def fl_env():
    return fl('Окружение и пакеты', [
        q('Зачем проекту своё виртуальное окружение?', 'Чтобы его пакеты и версии не мешали другим проектам', ['Чтобы Python работал быстрее', 'Без него pip не работает'],
          'У каждого проекта — свой набор.'),
        q('Что делает pip install -r requirements.txt?', 'Ставит все пакеты из списка нужных версий', ['Удаляет пакеты из списка', 'Создаёт requirements.txt'],
          'Создаёт список pip freeze.'),
        q('Что значит строка numpy>=2.0 в requirements.txt?', 'Нужна версия 2.0 или новее', ['Ровно версия 2.0', 'Любая версия, кроме 2.0'], '>= — «не ниже».'),
    ])


def th_log():
    terms = [
        ('logging', 'Модуль журналирования: сообщения с уровнем важности, которые можно включать, отключать и направлять в файл.'),
        ('basicConfig', 'logging.basicConfig(level=…, format=…, stream=…) — настроить журнал один раз в начале: какой уровень показывать, '
                        'в каком виде и куда писать.'),
        ('INFO', 'logging.DEBUG, INFO, WARNING, ERROR — уровни; это числа 10, 20, 30, 40, поэтому их можно сравнивать.'),
        ('stdout', 'sys.stdout — поток обычного вывода: туда пишет print. Ошибки и логи по умолчанию идут в sys.stderr.'),
        ('getLogger', 'logging.getLogger(имя) — именованный журнал для части программы; по имени видно, откуда сообщение.'),
        ('уровень лога', 'Важность сообщения: DEBUG — подробности для отладки, INFO — обычные события, WARNING — подозрительное, ERROR — ошибка. '
                         'Показываются сообщения не ниже выбранного уровня.'),
        ('debug', 'журнал.debug(текст) — сообщение уровня DEBUG.'),
        ('info', 'журнал.info(текст) — сообщение уровня INFO.'),
        ('warning', 'журнал.warning(текст) — сообщение уровня WARNING.'),
        ('error', 'журнал.error(текст) — сообщение уровня ERROR.'),
    ]
    body = (
        '<p>print для отладки потом приходится вычищать. Профессионально пишут лог — журнал событий модулем [[logging]]. У каждого сообщения '
        'есть [[уровень лога]], и одной строкой настройки можно показать только важное или, наоборот, всё подряд.</p>'
        '<p>Настраивают журнал один раз — [[basicConfig]]. Обычно лог пишут в файл или в поток ошибок, а здесь направим его в обычный вывод '
        '(<code>stream=sys.stdout</code>) и без времени в формате — чтобы вывод было видно и можно было проверить:</p>'
        + ex('import logging\nimport sys\n\nlogging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s", stream=sys.stdout)\n'
             'log = logging.getLogger("магазин")\n\nlog.debug("корзина: %s", ["мяч"])\nlog.info("заказ принят")\nlog.warning("мало на складе: %s шт.", 2)\n'
             'log.error("оплата не прошла")') +
        '<p>Сообщение [[debug]] не показалось: уровень INFO отсекает всё ниже. [[getLogger]] даёт журналу имя — в большой программе по '
        'нему видно, какая часть написала сообщение. Значения подставляются через <code>%s</code> вторым аргументом, а не f-строкой: '
        'если сообщение отключено, строка даже не будет собираться.</p>'
        '<p>[[info]], [[warning]] и [[error]] — сообщения своих уровней. Для отладки уровень меняют на DEBUG, и все подробности появляются '
        'без единой правки в коде.</p>'
    )
    return th('Логи', terms, body)


def fl_log():
    return fl('Логи', [
        q('Какие сообщения покажет журнал с level=logging.WARNING?', 'WARNING и ERROR', ['Только WARNING', 'Все, кроме DEBUG'], 'Не ниже выбранного уровня.'),
        q('Чем лог лучше print для отладки?', 'Уровни включаются одной настройкой, без правки кода', ['Лог работает быстрее print', 'print нельзя писать в функциях'],
          'Подробности остаются в коде и просто скрыты.'),
        q('Зачем журналу имя: getLogger("оплата")?', 'Чтобы видеть, какая часть программы написала сообщение', ['Без имени журнал не работает', 'Имя задаёт уровень'],
          'Имя попадает в формат %(name)s.'),
    ])


def code_log():
    return ts('Логи', [
        task('Проверка requirements.txt. Рядом с программой лежит requirements.txt. Настрой журнал: уровень INFO, формат «%(levelname)s: %(message)s», '
             'вывод в sys.stdout. Для каждой строки файла: пустые и комментарии (с #) пропусти; строку «пакет==версия» запиши в лог INFO «ПАКЕТ ВЕРСИЯ»; '
             'строку без == — WARNING «версия не зафиксирована: СТРОКА»; если пакет уже встречался с == — ERROR «ПАКЕТ указан дважды». '
             'В конце выведи print «Пакетов: N» — сколько разных пакетов с зафиксированной версией.',
             'line.strip(); if not line or line.startswith("#"): continue. name, ver = line.split("==").\nПакеты храни во множестве.',
             'import logging\nimport sys\n\nlogging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stdout)\nlog = logging.getLogger("req")\n'
             'seen = set()\nwith open("requirements.txt", encoding="utf-8") as f:\n    for line in f:\n        line = line.strip()\n        if not line or line.startswith("#"):\n'
             '            continue\n        if "==" not in line:\n            log.warning("версия не зафиксирована: %s", line)\n            continue\n        name, ver = line.split("==")\n'
             '        if name in seen:\n            log.error("%s указан дважды", name)\n        else:\n            seen.add(name)\n            log.info("%s %s", name, ver)\n'
             'print(f"Пакетов: {len(seen)}")',
             [''], files={'requirements.txt': REQ}),
        task('Уровень по выбору. На вход подаётся уровень (DEBUG, INFO, WARNING или ERROR), затем числа заказов по одному, последняя строка — «стоп». '
             'Настрой журнал с этим уровнем, форматом «%(levelname)s: %(message)s» и выводом в sys.stdout. Для каждой суммы: DEBUG «получено N»; '
             'если сумма не больше нуля — ERROR «неверная сумма N»; если больше 10000 — WARNING «крупный заказ N»; иначе INFO «заказ N принят». '
             'В конце print «Принято: K» — сколько сумм больше нуля.',
             'Уровень по имени: getattr(logging, имя) — атрибуты модуля logging.DEBUG и другие — это числа уровней.',
             'import logging\nimport sys\n\nlevel = input()\nlogging.basicConfig(level=getattr(logging, level), format="%(levelname)s: %(message)s", stream=sys.stdout)\n'
             'log = logging.getLogger("orders")\naccepted = 0\nwhile True:\n    s = input()\n    if s == "стоп":\n        break\n    n = int(s)\n    log.debug("получено %s", n)\n'
             '    if n <= 0:\n        log.error("неверная сумма %s", n)\n        continue\n    accepted += 1\n    if n > 10000:\n        log.warning("крупный заказ %s", n)\n'
             '    else:\n        log.info("заказ %s принят", n)\nprint(f"Принято: {accepted}")',
             ['INFO\n500\n-3\n25000\nстоп', 'DEBUG\n10\nстоп', 'ERROR\n100\n0\n99999\nстоп']),
    ])


def th_test():
    terms = [
        ('тест', 'Маленькая функция, которая вызывает твой код на известных данных и проверяет результат через assert. Тесты запускают после '
                 'каждой правки, чтобы сразу заметить поломку.'),
        ('pytest', 'Программа для запуска тестов на компьютере: находит в файлах test_*.py функции test_… и запускает их — команда pytest в терминале.'),
    ]
    body = (
        '<p>Чем больше проект, тем страшнее его менять: исправил одно — сломал другое. Спасают [[тест]]ы — маленькие функции, которые проверяют '
        'код на примерах с известным ответом. assert ты уже знаешь; тесты — это просто функции с ним:</p>'
        + ex('def cart_total(prices, discount=0):\n    total = sum(prices)\n    return total - total * discount // 100\n\n\ndef test_empty():\n    assert cart_total([]) == 0\n\n\n'
             'def test_discount():\n    assert cart_total([100, 200], 10) == 270\n\n\ndef test_no_discount():\n    assert cart_total([5, 5]) == 10, "без скидки"\n\n\n'
             'for test in [test_empty, test_discount, test_no_discount]:\n    test()\n    print("ok", test.__name__)') +
        '<p>На компьютере тесты запускает [[pytest]]: кладёшь их в файл <code>test_cart.py</code>, пишешь в терминале <code>pytest</code> — '
        'он сам найдёт все функции, чьё имя начинается с <code>test_</code>, запустит и покажет, какие упали и почему.</p>'
        '<pre>pip install pytest\npytest            # все тесты проекта\npytest -q         # коротко</pre>'
        '<p>Хороший тест проверяет одно поведение, а его имя говорит, что именно. Обязательно тестируют граничные случаи: пустой список, '
        'ноль, отрицательные числа, очень большие значения.</p>'
    )
    return th('Тесты', terms, body)


def fl_test():
    return fl('Тесты', [
        q('Какие функции запускает pytest?', 'Функции, чьё имя начинается с test_, в файлах test_*.py', ['Все функции проекта', 'Только функцию main'],
          'По имени он и находит тесты.'),
        q('Что делает тест, если результат неверный?', 'Падает с AssertionError — и видно, какая проверка не прошла', ['Печатает False и работает дальше', 'Исправляет функцию'],
          'assert с ложным условием вызывает ошибку.'),
        q('Какой случай стоит проверить в тестах функции, считающей среднее списка?', 'Пустой список', ['Список из ста одинаковых чисел', 'Список, отсортированный по возрастанию'],
          'Граничные случаи ломают код чаще всего.'),
    ])


def code_test():
    return ts('Тесты', [
        task('Мини-pytest. Напиши функцию run_tests(tests): tests — список функций-тестов. Запусти каждую: если прошла — выведи «ok ИМЯ», если упала с '
             'AssertionError — «FAIL ИМЯ: ТЕКСТ» (текст сообщения assert, а если его нет — «без сообщения»), если упала с другой ошибкой — '
             '«ERROR ИМЯ: ТИП» (имя класса ошибки). В конце выведи «пройдено P из N» и верни True, если упавших нет.',
             'Имя функции — test.__name__, имя класса ошибки — type(e).__name__.\nТекст assert — str(e); пустая строка значит, что сообщения нет.',
             'def run_tests(tests):\n    passed = 0\n    for test in tests:\n        try:\n            test()\n        except AssertionError as e:\n'
             '            print(f"FAIL {test.__name__}: {str(e) or \'без сообщения\'}")\n        except Exception as e:\n            print(f"ERROR {test.__name__}: {type(e).__name__}")\n'
             '        else:\n            passed += 1\n            print(f"ok {test.__name__}")\n    print(f"пройдено {passed} из {len(tests)}")\n    return passed == len(tests)\n',
             ['def test_a():\n    assert 1 + 1 == 2\n\ndef test_b():\n    assert "кот".upper() == "КОТ"\n\nprint(run_tests([test_a, test_b]))',
              'def test_sum():\n    assert sum([1, 2]) == 4, "сумма неверна"\n\ndef test_plain():\n    assert [] \n\ndef test_crash():\n    [][1]\n\ndef test_ok():\n    pass\n\n'
              'print(run_tests([test_sum, test_plain, test_crash, test_ok]))'], tail=TL),
        task('Найди ошибку тестами. Функция grade(score) должна возвращать оценку: 90 и больше — 5, от 75 — 4, от 50 — 3, ниже — 2; для баллов '
             'вне 0…100 — ValueError. В ней спрятаны ошибки на границах. Исправь функцию так, чтобы все тесты из заготовки прошли и программа '
             'вывела «все тесты пройдены».',
             'Прочитай, какой тест падает первым и с каким сообщением. Границы: >= 90, >= 75, >= 50; проверка диапазона — до сравнения.',
             'def grade(score):\n    if not 0 <= score <= 100:\n        raise ValueError("баллы от 0 до 100")\n    if score >= 90:\n        return 5\n    if score >= 75:\n'
             '        return 4\n    if score >= 50:\n        return 3\n    return 2\n\n\ndef test_borders():\n    assert grade(90) == 5, "90 — это 5"\n    assert grade(75) == 4, "75 — это 4"\n'
             '    assert grade(50) == 3, "50 — это 3"\n    assert grade(49) == 2, "49 — это 2"\n\n\ndef test_range():\n    for bad in [-1, 101]:\n        try:\n            grade(bad)\n'
             '        except ValueError:\n            continue\n        assert False, f"{bad} должно вызывать ValueError"\n\n\ntest_borders()\ntest_range()\nprint("все тесты пройдены")',
             [''],
             starter='def grade(score):\n    if score > 90:\n        return 5\n    if score > 75:\n        return 4\n    if score >= 50:\n        return 3\n    if not 0 <= score <= 100:\n'
                     '        raise ValueError("баллы от 0 до 100")\n    return 2\n\n\ndef test_borders():\n    assert grade(90) == 5, "90 — это 5"\n    assert grade(75) == 4, "75 — это 4"\n'
                     '    assert grade(50) == 3, "50 — это 3"\n    assert grade(49) == 2, "49 — это 2"\n\n\ndef test_range():\n    for bad in [-1, 101]:\n        try:\n            grade(bad)\n'
                     '        except ValueError:\n            continue\n        assert False, f"{bad} должно вызывать ValueError"\n\n\ntest_borders()\ntest_range()\nprint("все тесты пройдены")',
             fix=True),
    ])


def build():
    return topic('Инструменты: проект как у профи', 'venv, pip, логи, тесты', [
        th_env(), fl_env(),
        th_log(), fl_log(), code_log(),
        th_test(), fl_test(), code_test(),
    ], opt=True)
