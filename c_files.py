from dsl import *

# Тема 20 «Файлы и форматы данных». Ученик знает модули, исключения, коллекции, функции, формат.
# Три теории: чтение и запись файлов (open, with, режимы, sys.stdin); pathlib и CSV; JSON.
# Мини-проект — «Дневник расходов» (CSV → итоги → JSON). Файлы заданий — авторские, лежат рядом с программой.

POEM = ('Скрипт запускался в полночь,\n'
        'и в консоли горел курсор.\n'
        'Кролик смотрел на вывод\n'
        'и не понимал, где спор.\n')

GRADES = ('фамилия,математика,физика,информатика\n'
          'Белов,4,3,5\n'
          'Зайцева,5,5,5\n'
          'Ким,3,4,4\n'
          'Орлова,5,4,5\n'
          'Смирнов,2,3,4\n')

EXPENSES = ('дата,категория,сумма\n'
            '2026-09-02,еда,240\n'
            '2026-09-02,транспорт,62\n'
            '2026-09-05,учёба,450\n'
            '2026-09-11,развлечения,700\n'
            '2026-09-14,еда,180\n'
            '2026-09-20,подарки,1200\n'
            '2026-09-28,еда,95\n'
            '2026-10-01,транспорт,62\n'
            '2026-10-03,еда,310\n'
            '2026-10-03,развлечения,450\n'
            '2026-10-09,учёба,1290\n'
            '2026-10-15,еда,205\n'
            '2026-10-21,транспорт,124\n'
            '2026-10-27,еда,160\n')


def th_files():
    terms = [
        ('open', 'Открывает файл: open(имя, режим, encoding="utf-8"). Режимы: "r" — читать (по умолчанию), "w" — записать заново '
                 '(старое содержимое стирается), "a" — дописать в конец. Возвращает файловый объект.'),
        ('with', 'Блок, который сам закрывает файл по выходу, даже при ошибке: with open(...) as f:. Так и принято работать с файлами.\n'
                 'Пример:\nwith open("note.txt", "w", encoding="utf-8") as f:\n    f.write("привет")\nwith open("note.txt", encoding="utf-8") as f:\n    print(f.read())\nВывод:\nпривет'),
        ('read', 'Метод файла: весь текст файла одной строкой.'),
        ('readline', 'Метод файла: следующая строка вместе с \\n в конце; пустая строка — файл кончился.'),
        ('readlines', 'Метод файла: список всех строк, каждая с \\n в конце.'),
        ('write', 'Метод файла: записывает строку и возвращает число записанных символов. Перевод строки сам не добавляет.'),
        ('FileNotFoundError', 'Ошибка открытия для чтения: файла с таким именем нет. Текст: No such file or directory: \'…\'.'),
        ('sys', 'Модуль для связи с системой: sys.stdin — ввод, sys.argv — аргументы командной строки и другое.'),
        ('stdin', 'sys.stdin — весь ввод программы как файл: его можно перебрать по строкам for line in sys.stdin или прочитать sys.stdin.read().'),
    ]
    body = (
        '<p>Данные часто хранят в файлах: тексты, таблицы, настройки, сохранения игры. Файл открывают функцией [[open]], '
        'а работают с ним в блоке [[with]] — он сам закроет файл, когда блок закончится, даже при ошибке. '
        'Кодировку <code>utf-8</code> указывают всегда, иначе русский текст может превратиться в кракозябры.</p>'
        '<h3>Запись и чтение</h3>'
        + ex('with open("plan.txt", "w", encoding="utf-8") as f:\n    f.write("1. Уроки\\n")\n    f.write("2. Тренировка\\n")\n'
             'with open("plan.txt", "a", encoding="utf-8") as f:\n    f.write("3. Сериал\\n")\nwith open("plan.txt", encoding="utf-8") as f:\n    print(f.read())') +
        '<p>Режим <code>"w"</code> создаёт файл заново (старое содержимое стирается), <code>"a"</code> дописывает в конец, '
        'по умолчанию <code>"r"</code> — чтение. [[write]] не добавляет перевод строки сам. [[read]] читает весь файл строкой.</p>'
        '<h3>По строкам</h3>'
        '<p>Файл можно перебрать <code>for</code> по строкам — так удобнее для больших файлов. У каждой строки в конце '
        '<code>\\n</code>, его срезают <code>strip</code>. Есть и [[readline]] (одна строка) и [[readlines]] (список строк). '
        'В задачах файлы уже лежат рядом с программой — их имена указаны в условии:</p>'
        + ex('with open("poem.txt", encoding="utf-8") as f:\n    for i, line in enumerate(f, 1):\n        print(i, line.strip())', files={'poem.txt': POEM}) +
        '<p>Если файла нет — [[FileNotFoundError]], и это обычная ошибка, её ловят <code>try</code>.</p>'
        '<h3>Ввод как файл: sys.stdin</h3>'
        '<p>Весь ввод программы тоже можно читать как файл: [[sys]].[[stdin]]. Это удобно, когда строк неизвестно сколько '
        'и стоп-слова нет — цикл закончится сам, когда ввод кончится:</p>'
        + ex('import sys\ntotal = 0\nfor line in sys.stdin:\n    total += int(line)\nprint("Сумма:", total)', ['10', '25', '7']) +
        '<p>Путь к файлу может включать папки: <code>"data/notes.txt"</code>. Прямая косая черта работает везде, а обратную '
        'в Windows-путях удваивают, как мы обсуждали в первой теме.</p>'
    )
    return th('Чтение и запись файлов', terms, body)


def fl_files():
    return fl('Чтение и запись файлов', [
        q('Что сделает open("data.txt", "w")?', 'Создаст файл заново, стерев старое содержимое',
          ['Допишет в конец файла', 'Откроет файл только для чтения'], 'Режим "w" — запись с нуля. Для дописывания — "a".'),
        q('Зачем открывать файл в блоке with?', 'Файл закроется сам, даже если случится ошибка',
          ['Без with файл не открыть', 'with ускоряет чтение'], 'with гарантирует закрытие файла.'),
        qo('Что выведет программа?', 'with open("t.txt", "w", encoding="utf-8") as f:\n    f.write("а")\n    f.write("б")\nwith open("t.txt", encoding="utf-8") as f:\n    print(len(f.read()))',
           ['1', '4', 'аб'], 'write не добавляет перевод строки: в файле «аб», длина 2.'),
    ])


def code_files():
    return ts('Чтение и запись файлов', [
        task('Рядом с программой лежит файл poem.txt. Выведи «Строк: N, слов: M, самая длинная строка: K символов» '
             '(длину строки считай без перевода строки).',
             'with open("poem.txt", encoding="utf-8") as f: lines = [s.rstrip("\\n") for s in f]. Слова — сумма len(s.split()).',
             'with open("poem.txt", encoding="utf-8") as f:\n    lines = [s.rstrip("\\n") for s in f]\nwords = sum(len(s.split()) for s in lines)\n'
             'print(f"Строк: {len(lines)}, слов: {words}, самая длинная строка: {max(len(s) for s in lines)} символов")',
             [''], files={'poem.txt': POEM}),
        task('Ввод — целые числа по одному в строке, хотя бы одно, без стоп-слова. Выведи количество, сумму и максимум: '
             '«N чисел, сумма S, максимум M».',
             'import sys; nums = [int(line) for line in sys.stdin].',
             'import sys\nnums = [int(line) for line in sys.stdin]\nprint(f"{len(nums)} чисел, сумма {sum(nums)}, максимум {max(nums)}")',
             ['5\n10\n-3', '42', '1\n1\n1\n1']),
        task('Список покупок. На вход подаются товары по одному в строке до конца ввода. Запиши их в файл list.txt с номерами '
             '«1. товар», затем прочитай файл и выведи его содержимое и последней строкой — «Записано: N».',
             'Запись: for i, item in enumerate(items, 1): f.write(f"{i}. {item}\\n"). Чтение — второй with и print(f.read(), end="").',
             'import sys\nitems = [s.strip() for s in sys.stdin]\nwith open("list.txt", "w", encoding="utf-8") as f:\n    for i, item in enumerate(items, 1):\n'
             '        f.write(f"{i}. {item}\\n")\nwith open("list.txt", encoding="utf-8") as f:\n    print(f.read(), end="")\nprint(f"Записано: {len(items)}")',
             ['хлеб\nмолоко\nсыр', 'батарейки']),
    ])


def th_csv():
    terms = [
        ('pathlib', 'Модуль для путей к файлам и папкам: Path, проверки существования, чтение и запись в одну строку.'),
        ('Path', 'Путь к файлу или папке. Части соединяют знаком /: Path("data") / "notes.txt". Есть .name, .suffix, .stem.\n'
                 'Пример:\nfrom pathlib import Path\np = Path("photos") / "cat.png"\nprint(p.name, p.suffix, p.stem)\nВывод:\ncat.png .png cat'),
        ('exists', 'Метод Path: True, если файл или папка существует.'),
        ('read_text', 'Метод Path: прочитать весь файл строкой: Path("a.txt").read_text(encoding="utf-8").'),
        ('write_text', 'Метод Path: записать строку в файл целиком (старое содержимое стирается).'),
        ('csv', 'Модуль для таблиц CSV: строки текста, где значения разделены запятыми; первая строка обычно — заголовки.'),
        ('reader', 'csv.reader(f) — перебирает строки таблицы как списки значений (все значения — строки).'),
        ('DictReader', 'csv.DictReader(f) — перебирает строки как словари «заголовок: значение»; заголовки берутся из первой строки.'),
        ('writer', 'csv.writer(f) — объект для записи таблицы; файл открывают с newline="".'),
        ('writerow', 'Метод writer: записать одну строку таблицы из списка значений.'),
    ]
    body = (
        '<h3>pathlib</h3>'
        '<p>Модуль [[pathlib]] работает с путями как с объектами. [[Path]] соединяет части пути знаком <code>/</code> '
        '(правильно для любой системы) и умеет многое без <code>open</code>: [[exists]], [[read_text]], [[write_text]]:</p>'
        + ex('from pathlib import Path\np = Path("notes") / "todo.txt"\nprint(p.name, p.suffix, p.stem)\nnote = Path("hello.txt")\nprint(note.exists())\n'
             'note.write_text("привет, файл", encoding="utf-8")\nprint(note.exists(), note.read_text(encoding="utf-8"))') +
        '<h3>CSV — таблицы в тексте</h3>'
        '<p>CSV — самый простой формат таблиц: каждая строка файла — строка таблицы, значения разделены запятыми, '
        'в первой строке — заголовки. Так выгружают данные из Excel и Google Таблиц. Модуль [[csv]] разбирает такие файлы. '
        '[[reader]] даёт строки списками, [[DictReader]] — словарями по заголовкам:</p>'
        + ex('import csv\nwith open("grades.csv", encoding="utf-8") as f:\n    for row in csv.DictReader(f):\n'
             '        marks = [int(row["математика"]), int(row["физика"]), int(row["информатика"])]\n        print(f"{row[\'фамилия\']:<8} {sum(marks) / 3:.2f}")',
             files={'grades.csv': GRADES}) +
        '<p>Все значения из CSV — строки, числа превращают вручную. Записывают таблицу через [[writer]] и [[writerow]]; '
        'файл для записи CSV открывают с <code>newline=""</code>, иначе в Windows появятся пустые строки:</p>'
        + ex('import csv\nfrom pathlib import Path\nrows = [["день", "шаги"], ["пн", 8200], ["вт", 10450]]\nwith open("steps.csv", "w", encoding="utf-8", newline="") as f:\n'
             '    w = csv.writer(f)\n    for r in rows:\n        w.writerow(r)\nprint(Path("steps.csv").read_text(encoding="utf-8"), end="")') +
        '<p>Прочитать файл целиком для проверки удобнее всего через <code>Path(...).read_text()</code> — он сам откроет и закроет файл.</p>'
    )
    return th('pathlib и CSV', terms, body)


def fl_csv():
    return fl('pathlib и CSV', [
        qo('Что выведет программа?', 'from pathlib import Path\nprint((Path("games") / "save.json").suffix)', ['save', 'games', 'json'], 'suffix — расширение с точкой: .json.'),
        q('Какого типа значения в строках, которые даёт csv.reader?', 'Все — строки', ['Числа — int, текст — str', 'Все — числа'],
          'CSV — текст; числа превращают через int или float.'),
        q('Что даёт csv.DictReader для каждой строки таблицы?', 'Словарь «заголовок: значение»', ['Список значений', 'Одну строку текста'],
          'Ключи берутся из первой строки файла.'),
    ])


def code_csv():
    return ts('pathlib и CSV', [
        task('Рядом лежит grades.csv: фамилия и оценки по трём предметам. Выведи отличников — у кого все три оценки 5 — '
             'по одному в строке, или «Отличников нет».',
             'DictReader; для строки проверь all(row[s] == "5" for s in ("математика", "физика", "информатика")).',
             'import csv\nbest = []\nwith open("grades.csv", encoding="utf-8") as f:\n    for row in csv.DictReader(f):\n'
             '        if all(row[s] == "5" for s in ("математика", "физика", "информатика")):\n            best.append(row["фамилия"])\nprint("\\n".join(best) if best else "Отличников нет")',
             [''], files={'grades.csv': GRADES}),
        task('По файлу grades.csv выведи средний балл класса по предмету, название которого подаётся на вход, с двумя знаками: '
             '«ПРЕДМЕТ: X». Если это не одна из колонок математика, физика, информатика (в том числе «фамилия»), — «Нет предмета: ...».',
             'Прочитай строки DictReader в список. Проверь предмет по кортежу («математика», «физика», «информатика»). Среднее — sum(int(r[p]) ...) / len(rows).',
             'import csv\nsubj = input()\nwith open("grades.csv", encoding="utf-8") as f:\n    rows = list(csv.DictReader(f))\nif subj not in ("математика", "физика", "информатика"):\n'
             '    print(f"Нет предмета: {subj}")\nelse:\n    print(f"{subj}: {sum(int(r[subj]) for r in rows) / len(rows):.2f}")',
             ['математика', 'информатика', 'химия', 'фамилия'], files={'grades.csv': GRADES}),
        task('Заметки. На вход подаются имя файла и текст заметки. Если такой файл уже есть рядом с программой, выведи '
             '«Файл занят: ИМЯ», иначе запиши текст через Path.write_text и выведи «Сохранено, символов: N». '
             'Рядом лежит только файл grades.csv.',
             'p = Path(name); if p.exists(): ... else: p.write_text(text, encoding="utf-8"), длина — len(text).',
             'from pathlib import Path\np = Path(input())\ntext = input()\nif p.exists():\n    print(f"Файл занят: {p.name}")\nelse:\n'
             '    p.write_text(text, encoding="utf-8")\n    print(f"Сохранено, символов: {len(text)}")',
             ['idea.txt\nСделать бота для расписания', 'grades.csv\nчто-то'], files={'grades.csv': GRADES}),
    ])


def th_json():
    terms = [
        ('json', 'Модуль для формата JSON — текстовой записи словарей, списков, строк, чисел, True/False (true/false) и None (null).'),
        ('dumps', 'json.dumps(данные) — превращает данные Python в строку JSON. ensure_ascii=False — оставить русские буквы, indent=2 — с отступами.\n'
                  'Пример:\nimport json\nprint(json.dumps({"ok": True, "n": None}))\nВывод:\n{"ok": true, "n": null}'),
        ('loads', 'json.loads(строка) — разбирает строку JSON в данные Python. Если строка не JSON — ошибка json.JSONDecodeError (разновидность ValueError).\n'
                  'Пример:\nimport json\nd = json.loads(\'{"level": 7}\')\nprint(d["level"] + 1)\nВывод:\n8'),
        ('dump', 'json.dump(данные, файл) — записать данные в открытый файл в формате JSON.'),
        ('load', 'json.load(файл) — прочитать JSON из открытого файла.'),
    ]
    body = (
        '<p>[[json]] — самый популярный формат обмена данными: так хранят настройки и сохранения игр, так отвечают сайты и приложения. '
        'Он почти совпадает с записью словарей и списков в Python, только строки всегда в двойных кавычках, '
        '<code>true</code>/<code>false</code>/<code>null</code> вместо <code>True</code>/<code>False</code>/<code>None</code>.</p>'
        + ex('import json\nsave = {"nick": "Кира", "level": 7, "items": ["меч", "щит"], "boss": None, "online": True}\n'
             'text = json.dumps(save, ensure_ascii=False)\nprint(text)\nback = json.loads(text)\nprint(back["items"][0], back["boss"])') +
        '<p>[[dumps]] превращает данные в строку JSON, [[loads]] — обратно. <code>ensure_ascii=False</code> оставляет русские '
        'буквы как есть (иначе будут коды вида <code>\\u041a</code>), <code>indent=2</code> добавляет отступы для чтения человеком.</p>'
        '<h3>Файлы JSON</h3>'
        '<p>Для файлов — [[dump]] (записать) и [[load]] (прочитать), без «s» на конце:</p>'
        + ex('import json\nfrom pathlib import Path\nsettings = {"theme": "тёмная", "sound": False, "volume": 70}\nwith open("settings.json", "w", encoding="utf-8") as f:\n'
             '    json.dump(settings, f, ensure_ascii=False, indent=2)\nwith open("settings.json", encoding="utf-8") as f:\n    loaded = json.load(f)\n'
             'loaded["volume"] += 10\nprint(loaded)\nprint(Path("settings.json").read_text(encoding="utf-8"))') +
        '<p>Если строка — не JSON, <code>loads</code> и <code>load</code> выдают <code>json.JSONDecodeError</code>; это разновидность '
        'ValueError, поэтому её ловят <code>except ValueError</code>.</p>'
    )
    return th('JSON', terms, body)


def fl_json():
    return fl('JSON', [
        qo('Что выведет программа?', 'import json\nprint(json.dumps([True, None]))', ['[True, None]', "['true', 'null']", 'Ошибка'], 'В JSON: [true, null].'),
        qo('Что выведет программа?', 'import json\nd = json.loads(\'{"a": [1, 2]}\')\nprint(sum(d["a"]))', ['[1, 2]', '12', 'Ошибка'], 'Разобрали в словарь со списком: 3.'),
        q('Чем json.dump отличается от json.dumps?', 'dump пишет в файл, dumps возвращает строку', ['Ничем', 'dumps пишет в файл, dump возвращает строку'],
          '«s» на конце — от string, строка.'),
    ])


def code_json():
    return ts('JSON', [
        task('На вход подаётся одна строка JSON — сохранение игрока с полями nick, level и items (список). Выведи '
             '«НИК, уровень L, предметов: N» или «Сохранение повреждено», если строка не JSON.',
             'try: d = json.loads(input()) except ValueError: .... Число предметов — len(d["items"]).',
             'import json\ntry:\n    d = json.loads(input())\nexcept ValueError:\n    print("Сохранение повреждено")\nelse:\n'
             '    print(f"{d[\'nick\']}, уровень {d[\'level\']}, предметов: {len(d[\'items\'])}")',
             ['{"nick": "Кира", "level": 7, "items": ["меч", "щит"]}', '{"nick": "Zed", "level": 1, "items": []}', '{nick: Zed}']),
        task('Рядом лежит settings.json. На вход подаются ключ и новое значение — целое число. Обнови настройку (или добавь новую), '
             'сохрани файл обратно с ensure_ascii=False и indent=2 и выведи его содержимое.',
             'load → d[key] = int(value) → dump в тот же файл → print(Path("settings.json").read_text(encoding="utf-8")).',
             'import json\nkey = input()\nvalue = int(input())\nwith open("settings.json", encoding="utf-8") as f:\n    d = json.load(f)\nd[key] = value\n'
             'with open("settings.json", "w", encoding="utf-8") as f:\n    json.dump(d, f, ensure_ascii=False, indent=2)\nfrom pathlib import Path\nprint(Path("settings.json").read_text(encoding="utf-8"))',
             ['volume\n35', 'fps\n60'], files={'settings.json': '{"theme": "тёмная", "volume": 70}'}),
        task('Таблица в JSON. Превращи grades.csv в список словарей, где оценки — числа, и выведи его через json.dumps с '
             'ensure_ascii=False (без отступов).',
             'Для каждой строки DictReader: {"фамилия": r["фамилия"], ...} с int для оценок; или словарное выражение с int там, где ключ не «фамилия».',
             'import csv, json\nwith open("grades.csv", encoding="utf-8") as f:\n    rows = [{k: (v if k == "фамилия" else int(v)) for k, v in r.items()} for r in csv.DictReader(f)]\n'
             'print(json.dumps(rows, ensure_ascii=False))',
             [''], files={'grades.csv': GRADES}),
    ])


def project():
    return pj('Дневник расходов',
              'Рядом с программой лежит expenses.csv — дневник расходов с колонками дата (ГГГГ-ММ-ДД), категория и сумма — целое число рублей.\n'
              'Вход: месяц в виде «ГГГГ-ММ».\n'
              'Что сделать:\n'
              '1) выбрать записи за этот месяц;\n'
              '2) вывести «Расходы за ГГГГ-ММ», затем по строке на каждую категорию: название в поле шириной 14 влево и сумма '
              'в поле шириной 7 вправо — по убыванию суммы, при равенстве по алфавиту;\n'
              '3) вывести «Всего: N» и «Больше всего на: КАТЕГОРИЯ»;\n'
              '4) сохранить итоги в файл summary.json: {"month": ..., "total": ..., "by_category": {категория: сумма}} '
              '(категории в том же порядке, что и в выводе) '
              'с ensure_ascii=False и indent=2, и вывести этот файл.\n'
              'Если записей за месяц нет — вывести только «Нет записей за ГГГГ-ММ».',
              'Чтение: csv.DictReader, отбор по row["дата"].startswith(month).\n'
              'Суммы по категориям: defaultdict(int) или словарь с get.\n'
              'Сортировка: sorted(totals.items(), key=lambda p: (-p[1], p[0])).\n'
              'Сохранение: json.dump({"month": month, "total": total, "by_category": dict(...)}, f, ensure_ascii=False, indent=2).',
              'import csv\nimport json\nfrom collections import defaultdict\nfrom pathlib import Path\n\nmonth = input()\ntotals = defaultdict(int)\n'
              'with open("expenses.csv", encoding="utf-8") as f:\n    for row in csv.DictReader(f):\n        if row["дата"].startswith(month):\n'
              '            totals[row["категория"]] += int(row["сумма"])\nif not totals:\n    print(f"Нет записей за {month}")\nelse:\n'
              '    ranked = sorted(totals.items(), key=lambda p: (-p[1], p[0]))\n    total = sum(totals.values())\n    print(f"Расходы за {month}")\n'
              '    for cat, s in ranked:\n        print(f"{cat:<14}{s:>7}")\n    print(f"Всего: {total}")\n    print(f"Больше всего на: {ranked[0][0]}")\n'
              '    summary = {"month": month, "total": total, "by_category": dict(ranked)}\n    with open("summary.json", "w", encoding="utf-8") as f:\n'
              '        json.dump(summary, f, ensure_ascii=False, indent=2)\n    print(Path("summary.json").read_text(encoding="utf-8"))',
              ['2026-10', '2026-09', '2026-11'], strict=True, files={'expenses.csv': EXPENSES})


def build():
    return topic('Файлы и форматы данных', 'open, with, pathlib, CSV, JSON', [
        th_files(), fl_files(), code_files(),
        th_csv(), fl_csv(), code_csv(),
        th_json(), fl_json(), code_json(),
        project(),
    ])
