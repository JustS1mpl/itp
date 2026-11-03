from dsl import *

# Нора после «Модули»: работа с незнакомым кодом. Две теории: как разобраться в чужом проекте (точка входа, карта модулей, запуск на
# известном примере, воспроизвести баг, бисекция); как чинить, не ломая (сначала тест на баг, минимальная правка, поиск похожих мест).
# Задачи «найди и исправь» — чужие мини-проекты в шаблоне; мини-проект — склад с отчётом пользователя о двух ошибках.

DIARY = ('import datetime\n\n\ndef parse(line):\n    """«ДД.ММ предмет оценка» → (дата, предмет, оценка)."""\n    date, subject, mark = line.split()\n'
         '    day, month = date.split(".")\n    return datetime.date(2026, int(month), int(day)), subject, int(mark)\n\n\ndef average(marks):\n'
         '    if not marks:\n        return 0\n    return sum(marks) / len(marks)\n\n\ndef in_week(day, monday):\n    return monday <= day < monday + datetime.timedelta(days=7)\n\n\n'
         'def report(lines, monday):\n    by_subject = {}\n    for line in lines:\n        day, subject, mark = parse(line)\n        if in_week(day, monday):\n'
         '            by_subject.setdefault(subject, []).append(mark)\n    for subject in sorted(by_subject):\n'
         '        print(f"{subject}: {average(by_subject[subject]):.2f} ({len(by_subject[subject])} оц.)")\n    if not by_subject:\n        print("За неделю оценок нет")\n')
DIARY_BUG = DIARY.replace('monday <= day < monday + datetime.timedelta(days=7)', 'monday < day < monday + datetime.timedelta(days=7)') \
    .replace('    return sum(marks) / len(marks)', '    return sum(marks) // len(marks)')
DIARY_MAIN = ('\n\nmonday = parse(input() + " x 0")[0]\nlines = []\nwhile True:\n    line = input()\n    if line == "конец":\n        break\n    lines.append(line)\n'
              'report(lines, monday)')

SCHED = ('import datetime\n\nLESSONS = {"пн": ["алгебра", "физика"], "вт": ["химия"], "ср": ["алгебра", "литература", "информатика"],\n'
         '           "чт": ["физика"], "пт": ["информатика", "английский"]}\nDAYS = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]\n\n\n'
         'def day_name(date):\n    return DAYS[date.weekday()]\n\n\ndef next_lesson(subject, today):\n    for shift in range(1, 8):\n'
         '        date = today + datetime.timedelta(days=shift)\n        if subject in LESSONS.get(day_name(date), []):\n            return date\n    return None\n\n\n'
         'today = datetime.datetime.strptime(input(), "%d.%m.%Y").date()\nprint("Сегодня:", day_name(today))\nfor subject in input().split(", "):\n'
         '    date = next_lesson(subject, today)\n    if date is None:\n        print(f"{subject}: нет в расписании")\n    else:\n'
         '        print(f"{subject}: {date.strftime(\'%d.%m\')} ({day_name(date)})")\n')
SCHED_BUG = SCHED.replace('return DAYS[date.weekday()]', 'return DAYS[date.weekday() - 1]').replace('for shift in range(1, 8)', 'for shift in range(1, 7)')

STOCK = ('def parse(cmd):\n    parts = cmd.split()\n    return parts[0], parts[1], int(parts[2]) if len(parts) > 2 else 0\n\n\n'
         'def apply(stock, action, item, qty):\n    if action == "приход":\n        stock[item] = stock.get(item, 0) + qty\n        return "ok"\n'
         '    if action == "продажа":\n        if stock.get(item, 0) < qty:\n            return "не хватает"\n        stock[item] -= qty\n        return "ok"\n'
         '    if action == "возврат":\n        stock[item] = stock.get(item, 0) + qty\n        return "ok"\n    return "неизвестная команда"\n\n\n'
         'def report(stock):\n    items = [(item, n) for item, n in stock.items() if n > 0]\n    if not items:\n        return ["Склад пуст"]\n'
         '    lines = [f"{item}: {n}" for item, n in sorted(items, key=lambda p: (-p[1], p[0]))]\n'
         '    lines.append(f"Всего: {sum(n for _, n in items)} шт., позиций: {len(items)}")\n    return lines\n\n\nstock = {}\nlog = []\nwhile True:\n'
         '    cmd = input()\n    if cmd == "отчёт":\n        break\n    action, item, qty = parse(cmd)\n    result = apply(stock, action, item, qty)\n'
         '    log.append(result)\n    if result != "ok":\n        print(f"{cmd}: {result}")\nfor line in report(stock):\n    print(line)\n'
         'print(f"Операций: {len(log)}, отказов: {len(log) - log.count(\'ok\')}")\n')
STOCK_BUG = STOCK.replace('        stock[item] = stock.get(item, 0) + qty\n        return "ok"\n    return "неизвестная',
                          '        stock[item] = stock.get(item, 0) + qty * 2\n        return "ok"\n    return "неизвестная') \
    .replace('    if not items:\n        return ["Склад пуст"]\n', '') \
    .replace('sum(n for _, n in items)} шт., позиций: {len(items)}', 'sum(n for _, n in items)} шт., позиций: {len(stock)}') \
    .replace('    return parts[0], parts[1], int(parts[2]) if len(parts) > 2 else 0\n',
             '    return parts[0], parts[1], int(parts[2]) if len(parts) > 2 else 0\n# TODO(Дима): сделать отчёт красивее\n')


def th_map():
    terms = [
        ('точка входа', 'Место, откуда программа начинает работу: main.py, блок if __name__ == "__main__" или код верхнего уровня. Чтение чужого '
                        'проекта начинают с неё.'),
        ('воспроизвести баг', 'Найти точный ввод и действия, при которых ошибка случается каждый раз. Пока баг не воспроизводится, чинить вслепую.'),
        ('бисекция', 'Поиск половинным делением: проверяешь середину, отбрасываешь половину, где ошибки точно нет. Из 1000 версий нужная находится '
                     'за 10 проверок. git bisect так ищет коммит, сломавший программу.'),
    ]
    body = (
        '<p>Свой код с нуля пишут редко. Чаще приходишь в проект, где уже тысячи строк, написанных другими, — и в нём баг. Перечитывать всё '
        'подряд бесполезно: утонешь. Работает план:</p><ol>'
        '<li>Найди [[точка входа|точку входа]] и пройди путь данных: откуда приходит ввод, какие функции его трогают, где печатается результат.</li>'
        '<li>Нарисуй карту: какие модули кто импортирует. Неиспользуемые файлы сразу отбрасываешь.</li>'
        '<li>[[воспроизвести баг|Воспроизведи баг]]: точный ввод, при котором ответ неверный. Сравни, что получилось, с тем, что должно.</li>'
        '<li>Сужай место: print или assert посередине пути данных — значения уже неверные или ещё верные? Отбрось половину и повтори.</li></ol>'
        '<p>Последний шаг — это [[бисекция]], и она работает не только с кодом, но и с историей: была версия, где всё работало, и версия, где '
        'сломалось. Проверяешь середину — и каждый раз отбрасываешь половину:</p>'
        + ex('versions = ["ok", "ok", "ok", "ok", "ok", "bad", "bad", "bad"]\nlow, high = 0, len(versions) - 1   # 0 — точно ok, последняя — точно bad\n'
             'while high - low > 1:\n    mid = (low + high) // 2\n    print("проверяю версию", mid + 1, "→", versions[mid])\n    if versions[mid] == "ok":\n        low = mid\n'
             '    else:\n        high = mid\nprint("сломала версия", high + 1)') +
        '<p>Карту проекта можно составить и кодом — по строкам import:</p>'
        + ex('files = {"main.py": ["menu", "save"], "menu.py": ["ui"], "ui.py": [], "save.py": [], "old_save.py": ["ui"]}\nseen = []\ntodo = ["main.py"]\n'
             'while todo:\n    name = todo.pop()\n    if name not in seen:\n        seen.append(name)\n        todo += [m + ".py" for m in files[name]]\n'
             'print("используются:", sorted(seen))\nprint("лишние:", [f for f in files if f not in seen])') +
        '<p>old_save.py никто не импортирует — его можно не читать (а потом и удалить).</p>'
    )
    return th('Как разобраться', terms, body)


def fl_map():
    return fl('Как разобраться', [
        q('С чего начать знакомство с чужим проектом?', 'С точки входа и пути данных', ['С самого длинного файла', 'С файлов по алфавиту'],
          'Так видно, какой код действительно работает.'),
        q('Сколько проверок нужно бисекции для 1000 версий?', 'Около 10', ['Около 500', 'Ровно 1000'], 'Каждая проверка делит число версий пополам.'),
        q('Зачем сначала воспроизвести баг?', 'Иначе не проверить, что правка его исправила', ['Чтобы показать баг начальнику',
          'Так быстрее работает программа'], 'Воспроизводимый баг — половина починки.'),
    ])


def code_map():
    return ts('Как разобраться', [
        task('Карта проекта. На вход подаётся проект: строка «### ИМЯ.py» начинает файл, дальше его строки кода, последняя строка ввода — «КОНЕЦ». '
             'Локальные модули — файлы этого проекта. Импорт — строка, начинающаяся с «import X» или «from X import …» (X без .py). Для каждого файла '
             'в порядке ввода выведи «ИМЯ.py → импорты локальных модулей через запятую с пробелом» (или «—»). Затем «Используются: …» — файлы, '
             'достижимые от main.py по импортам, по алфавиту, и «Лишние: …» — остальные по алфавиту (или «Лишние: нет»).',
             'Словарь «файл → список локальных импортов». Импорт: words = line.split(); words[1] — имя модуля, если words[0] — import или from.\n'
             'Достижимость — как в теории: список todo и список seen.',
             'files = {}\nlines = []\nwhile True:\n    line = input()\n    if line == "КОНЕЦ":\n        break\n    lines.append(line)\nfor line in lines:\n'
             '    if line.startswith("### "):\n        files[line[4:]] = []\ncurrent = None\nfor line in lines:\n    words = line.split()\n'
             '    if line.startswith("### "):\n        current = line[4:]\n    elif words and words[0] in ("import", "from") and words[1] + ".py" in files:\n'
             '        files[current].append(words[1] + ".py")\nfor name, deps in files.items():\n    print(name, "→", ", ".join(deps) or "—")\nseen = []\ntodo = ["main.py"]\n'
             'while todo:\n    name = todo.pop()\n    if name not in seen:\n        seen.append(name)\n        todo += files[name]\nprint("Используются:", ", ".join(sorted(seen)))\n'
             'extra = sorted(f for f in files if f not in seen)\nprint("Лишние:", ", ".join(extra) or "нет")',
             ['### main.py\nimport random\nfrom game import start\nimport scores\nstart()\n### game.py\nfrom map import load\nimport datetime\n### map.py\n'
              'TILES = 64\n### scores.py\nimport json\n### old_map.py\nfrom map import load\nКОНЕЦ',
              '### main.py\nprint("привет")\n### utils.py\nimport main\nКОНЕЦ']),
        task('Бисекция. На вход подаётся строка результатов проверок версий через пробел: сначала идут ok, потом bad (первая — точно ok, последняя — '
             'точно bad). Найди первую плохую версию бисекцией, как в теории: каждую проверенную версию выведи «проверка N: РЕЗУЛЬТАТ» (N — номер версии '
             'с 1), затем «Сломала версия K» и «Проверок: P из возможных M» — M — сколько версий пришлось бы проверить подряд с начала до K.',
             'low = 0, high = len - 1; середина (low + high) // 2. Подряд с начала пришлось бы проверить версии 2…K — это K - 1 проверок.',
             'versions = input().split()\nlow, high = 0, len(versions) - 1\nchecks = 0\nwhile high - low > 1:\n    mid = (low + high) // 2\n    checks += 1\n'
             '    print(f"проверка {mid + 1}: {versions[mid]}")\n    if versions[mid] == "ok":\n        low = mid\n    else:\n        high = mid\n'
             'print(f"Сломала версия {high + 1}")\nprint(f"Проверок: {checks} из возможных {high}")',
             ['ok ok ok ok ok bad bad bad', 'ok bad', 'ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok ok bad']),
    ])


def th_fix():
    terms = [
        ('регрессия', 'Ошибка, которую внесла правка: чинили одно — сломали другое, что раньше работало.'),
        ('минимальная правка', 'Исправление ровно того места, где баг, без попутных переделок. Переделки — отдельно, когда баг уже закрыт.'),
    ]
    body = (
        '<p>Нашёл баг — не спеши переписывать половину файла. Порядок такой:</p><ol>'
        '<li>Запиши ввод, на котором баг воспроизводится, как тест: assert с правильным ответом. Сейчас он падает.</li>'
        '<li>Сделай [[минимальная правка|минимальную правку]] — и тест проходит.</li>'
        '<li>Прогони остальные тесты: не случилась ли [[регрессия]].</li>'
        '<li>Поищи такие же ошибки рядом: если автор один раз перепутал &lt; и &lt;=, он мог сделать это и в соседней функции.</li></ol>'
        '<p>Типичные места, где прячутся баги в чужом коде: границы (&lt; против &lt;=, range без последнего числа), деление (// вместо /), '
        'нумерация (с 0 или с 1, у weekday() понедельник — 0), изменяемые значения по умолчанию, перепутанные единицы (копейки и рубли).</p>'
        + ex('import datetime\n\nday = datetime.date(2026, 11, 2)\nprint(day.weekday(), ["пн", "вт", "ср", "чт", "пт", "сб", "вс"][day.weekday()])\n\n'
             'def test_weekday():\n    assert ["пн", "вт", "ср", "чт", "пт", "сб", "вс"][datetime.date(2026, 11, 8).weekday()] == "вс"\n\n\ntest_weekday()\nprint("тест пройден")') +
        '<p>И ещё одно правило вежливости: чужой код писали люди в своих обстоятельствах — может, за ночь до дедлайна. «Какой ужас» в чат не '
        'пишут. Пишут «нашёл баг в границе недели, вот тест и правка».</p>'
    )
    return th('Чиним, не ломая', terms, body)


def fl_fix():
    return fl('Чиним, не ломая', [
        q('Что сделать до того, как править найденный баг?', 'Записать тест, который на этом баге падает', ['Переписать файл начисто',
          'Удалить старые тесты'], 'Тест покажет, что правка помогла, и не даст багу вернуться.'),
        qo('Что выведет программа?', 'import datetime\nprint(datetime.date(2026, 11, 2).weekday())', ['1', '2', '7'],
           '2 ноября 2026 — понедельник, а у weekday() понедельник — 0.'),
        q('Ты нашёл баг и заодно хочешь переименовать всё в файле. Как лучше?', 'Сначала закрыть баг, переименовать — отдельно',
          ['Всё одной правкой — быстрее', 'Не трогать баг, только переименовать'], 'Иначе в правке не разглядеть, что именно чинит баг.'),
    ])


def code_fix():
    return ts('Чиним, не ломая', [
        task('Дневник за неделю. Чужая программа: первая строка ввода — дата понедельника «ДД.ММ», дальше записи «ДД.ММ предмет оценка», последняя — '
             '«конец». Она должна вывести по предметам в алфавитном порядке «ПРЕДМЕТ: СРЕДНЕЕ (N оц.)» за неделю с понедельника по воскресенье '
             'включительно (среднее — две цифры после точки), а если за неделю оценок нет — «За неделю оценок нет». Пользователи жалуются: оценки '
             'за понедельник пропадают, а средние какие-то круглые. Найди и исправь ошибки.',
             'Проверь границы недели в in_week и деление в average.',
             DIARY + DIARY_MAIN,
             ['02.11\n02.11 алгебра 5\n03.11 алгебра 4\n05.11 физика 3\n08.11 физика 4\n09.11 алгебра 2\nконец', '02.11\n10.11 химия 5\nконец',
              '28.12\n28.12 история 4\n31.12 история 5\nконец'],
             starter=DIARY_BUG + DIARY_MAIN, fix=True),
        task('Ближайший урок. Чужая программа: на вход подаются сегодняшняя дата «ДД.ММ.ГГГГ» и предметы через запятую с пробелом. Она должна вывести '
             '«Сегодня: ДЕНЬ» и для каждого предмета — дату ближайшего урока после сегодняшнего дня (в пределах недели вперёд, включая тот же день '
             'недели через 7 дней) «ПРЕДМЕТ: ДД.ММ (ДЕНЬ)» или «ПРЕДМЕТ: нет в расписании». Сейчас дни недели съехали, а уроки через ровно неделю не '
             'находятся. Исправь.',
             'У weekday() понедельник — 0. range(1, 7) не доходит до 7.',
             SCHED, ['02.11.2026\nалгебра, химия, физика, рисование', '06.11.2026\nинформатика, химия', '04.11.2026\nалгебра'],
             starter=SCHED_BUG, fix=True),
    ])


def project():
    return pj('Склад после стажёра',
              'Тебе достался учёт склада, который писал стажёр. Команды: «приход ТОВАР N», «продажа ТОВАР N», «возврат ТОВАР N», ввод заканчивается '
              'строкой «отчёт». Неудачные команды выводятся строкой «КОМАНДА: причина». Отчёт — товары с ненулевым остатком строками «ТОВАР: N» по '
              'убыванию остатка (при равенстве — по алфавиту), затем «Всего: S шт., позиций: P» — P — число товаров в отчёте; если товаров нет — '
              'строка «Склад пуст» вместо всего отчёта. Последняя строка — «Операций: K, отказов: F».\n'
              'Сообщения от пользователей: «после возврата товара его становится слишком много», «если всё распродать, отчёт пишет странное — '
              'Всего: 0 шт., позиций: 2», «позиций в отчёте больше, чем строк с товарами». Найди и исправь ошибки, ничего лишнего не переписывая.',
              'Воспроизведи каждый отчёт отдельным вводом и смотри, какая функция даёт неверное значение\nreport отвечает за «Склад пуст» и «позиций»; apply — за остатки',
              STOCK,
              ['приход меч 5\nприход щит 2\nпродажа меч 3\nвозврат меч 1\nпродажа щит 5\nприход зелье 2\nотчёт',
               'приход руна 2\nпродажа руна 2\nвозврат кольцо 1\nпродажа кольцо 1\nотчёт', 'отчёт', 'сжечь склад 1\nприход ключ 1\nотчёт'],
              starter=STOCK_BUG)


def build():
    return topic('Чужой код: найди баг', 'точка входа, карта модулей, бисекция, правка с тестом', [
        th_map(), fl_map(), code_map(),
        th_fix(), fl_fix(), code_fix(),
        project(),
    ], opt=True)
