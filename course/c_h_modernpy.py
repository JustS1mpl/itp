import json
from dsl import *

# Нора после «Декораторы и генераторы»: что нового в Python 3.13–3.14. t-строки (3.14) и сборка без GIL (free-threading) в браузерном
# Python 3.13 не запустить — их код показан для компьютера (<pre class="pc">), а в задачах — то же поведение своими руками: шаблон как
# список частей, безопасная подстановка, модель потоков с GIL и без, потерянные обновления. sys._is_gil_enabled() работает и здесь.

T_DEMO = ('name = "<b>Вика</b>"\ntemplate = t"Привет, {name}!"\nprint(type(template).__name__)          # Template, а не str\n'
          'print(template.strings)                  # (\'Привет, \', \'!\')\nprint(template.interpolations[0].value)  # <b>Вика</b>\n'
          'print(template.interpolations[0].expression)  # name')
T_HTML = ('from string.templatelib import Interpolation\n\n\ndef html(template):\n    out = []\n    for part in template:              # части по порядку\n'
          '        if isinstance(part, Interpolation):\n            out.append(escape(str(part.value)))   # подставленное — экранируем\n'
          '        else:\n            out.append(part)                      # текст шаблона — как есть\n    return "".join(out)\n\n\n'
          'print(html(t"<p>Привет, {name}!</p>"))   # <p>Привет, &lt;b&gt;Вика&lt;/b&gt;!</p>')
ESC = 'def escape(text):\n    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")\n'


def th_tstr():
    terms = [
        ('t-строка', 'Строка-шаблон с буквой t перед кавычками (Python 3.14+): t"Привет, {name}". В отличие от f-строки не склеивается сразу, '
                     'а даёт объект Template, где текст и подставленные значения лежат отдельно.'),
        ('Template', 'Результат t-строки: strings — кусочки текста, interpolations — подстановки (у каждой value — значение, expression — '
                     'текст выражения, format_spec — формат после двоеточия). При обходе циклом выдаёт части по порядку.'),
        ('шаблонизатор', 'Функция, которая из шаблона и значений собирает итог по своим правилам: экранирует HTML, делает параметры SQL, пишет логи.'),
    ]
    body = (
        '<p>Python развивается: раз в год выходит новая версия. Две большие новинки последних лет — t-строки и Python без GIL. Браузерный '
        'Python в ИТП — версии 3.13, поэтому код с ними здесь показан для компьютера, а их устройство мы повторим своими руками.</p>'
        '<p>f-строка удобна, но опасна: она склеивает всё сразу, и функция, получившая результат, уже не отличит текст программиста от '
        'данных пользователя. Вспомни XSS и инъекции: <code>f"&lt;p&gt;{comment}&lt;/p&gt;"</code> вставит чужой HTML как есть. '
        '[[t-строка]] из Python 3.14 ничего не склеивает, а возвращает [[Template]]:</p>'
        '<pre class="pc">' + T_DEMO.replace('<', '&lt;').replace('>', '&gt;') + '</pre>'
        '<p>Теперь функция-[[шаблонизатор]] сама решает, что делать с каждой подстановкой. Например, экранировать только значения:</p>'
        '<pre class="pc">' + T_HTML.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') + '</pre>'
        '<p>В Python 3.13 то же самое можно смоделировать: шаблон — список частей, где строки — текст, а кортежи (выражение, значение) — '
        'подстановки:</p>'
        + ex(ESC + '\n\ndef html(parts):\n    out = []\n    for part in parts:\n        if type(part) is tuple:\n            out.append(escape(str(part[1])))\n'
             '        else:\n            out.append(part)\n    return "".join(out)\n\n\nname = "<b>Вика</b>"\nparts = ["<p>Привет, ", ("name", name), "!</p>"]\n'
             'print(html(parts))\nprint(f"<p>Привет, {name}!</p>")') +
        '<p>Вторая строка — f-строка: тег прошёл насквозь. Тот же шаблон можно отдать и другому шаблонизатору — например, тому, что делает '
        'безопасный запрос к базе с параметрами вместо склейки.</p>'
    )
    return th('t-строки', terms, body)


def fl_tstr():
    return fl('t-строки', [
        q('Что возвращает t"Привет, {name}"?', 'Объект Template с текстом и подстановками отдельно', ['Готовую строку, как f-строка',
          'Функцию, которую надо вызвать'], 'Склеивает уже шаблонизатор.'),
        q('Чем t-строка безопаснее f-строки для HTML?', 'Шаблонизатор отличает текст от данных и экранирует данные', ['Она работает быстрее',
          't-строки не могут содержать <'], 'f-строка смешивает всё в одну строку.'),
        q('Почему в ИТП t-строки не запустятся?', 'Здесь Python 3.13, а t-строки появились в 3.14', ['t-строки работают только в Linux',
          'Браузер запрещает букву t'], 'Новый синтаксис требует новой версии.'),
    ])


def code_tstr():
    return ts('t-строки', [
        task('Шаблон для SQL. Шаблон — список частей: строки — текст запроса, кортежи (выражение, значение) — подстановки. Напиши функцию sql(parts), '
             'которая возвращает кортеж из двух элементов: запрос, где вместо каждой подстановки стоит знак ?, и список значений по порядку.',
             'Два списка: куски запроса и значения. type(part) is tuple — подстановка.',
             'def sql(parts):\n    query = []\n    values = []\n    for part in parts:\n        if type(part) is tuple:\n            query.append("?")\n'
             '            values.append(part[1])\n        else:\n            query.append(part)\n    return "".join(query), values\n',
             ['name = "x\' OR \'1\'=\'1"\nprint(sql(["SELECT * FROM users WHERE name = ", ("name", name)]))',
              'print(sql(["UPDATE scores SET points = ", ("p", 10), " WHERE id = ", ("uid", 7), " AND game = ", ("g", "tetris")]))\nprint(sql(["SELECT 1"]))'],
             tail=TL),
        task('Шаблон из текста. t-строку собирает Python, а мы соберём части из обычной строки. Напиши функцию parse(text, values): в тексте '
             'подстановки записаны в фигурных скобках {имя}; values — словарь значений. Верни список частей: непустые куски текста — строками, '
             'подстановки — кортежами (имя, значение). Если имени нет в values, значение — None.',
             'Ищи "{" через find начиная с позиции pos; от неё — "}". Кусок перед «{» добавляй, только если он не пустой.',
             'def parse(text, values):\n    parts = []\n    pos = 0\n    while True:\n        start = text.find("{", pos)\n        if start == -1:\n            break\n'
             '        end = text.find("}", start)\n        if text[pos:start]:\n            parts.append(text[pos:start])\n        name = text[start + 1:end]\n'
             '        parts.append((name, values.get(name)))\n        pos = end + 1\n    if text[pos:]:\n        parts.append(text[pos:])\n    return parts\n',
             ['print(parse("Привет, {name}!", {"name": "Вика"}))\nprint(parse("{a}+{b}", {"a": 1}))', 'print(parse("без подстановок", {}))\nprint(parse("{x}", {"x": [1, 2]}))'],
             tail=TL),
    ])


def th_gil():
    terms = [
        ('GIL', 'Global Interpreter Lock — глобальная блокировка в обычном Python: в каждый момент байт-код выполняет только один поток. '
                'Потоки ускоряют ожидание (сеть, диск), но не вычисления.'),
        ('free-threading', 'Сборка Python без GIL (python3.13t, с 3.14 — официально поддерживается): потоки считают на разных ядрах по-настоящему '
                           'одновременно.'),
        ('sys.version_info', 'Версия Python, на которой идёт программа: кортеж (3, 13, 2, …); срез [:2] — главная и малая версии.'),
        ('sys._is_gil_enabled', 'sys._is_gil_enabled() — True, если GIL включён (есть с Python 3.13). Подчёркивание в начале имени значит '
                                '«служебное»: функцию могут поменять в будущих версиях.'),
        ('гонка данных','Два потока одновременно читают и меняют одну переменную, и часть изменений теряется. counter += 1 — это три шага: '
                         'прочитать, прибавить, записать.'),
        ('блокировка', 'threading.Lock — «замок»: пока один поток внутри with lock:, другие ждут. Защищает общие данные от гонки.'),
    ]
    body = (
        '<p>Поток — отдельная «линия выполнения» внутри одной программы: у каждого свой порядок действий, а память (переменные) общая. '
        'В Python их создаёт threading.Thread(target=функция): start() запускает, join() ждёт конца (подробнее — в норе «Асинхронность» после темы «Запросы к серверам»).</p>'
        '<p>В обычном Python есть [[GIL]]: сколько бы потоков ты ни запустил, Python-код в каждый момент выполняет один. Пока поток ждёт ответа '
        'сервера, GIL отпускается — поэтому загрузки потоками ускоряются. А вот вычисления на 8 ядрах в 8 потоках идут не быстрее, чем в одном.</p>'
        '<p>[[free-threading]] — сборка Python без GIL. В ней тот же код считает на всех ядрах:</p>'
        '<pre class="pc">import threading, time\n\ndef work():\n    sum(i * i for i in range(10_000_000))\n\nstart = time.perf_counter()\n'
        'threads = [threading.Thread(target=work) for _ in range(4)]\nfor t in threads: t.start()\nfor t in threads: t.join()\n'
        'print(round(time.perf_counter() - start, 1))\n# python3.13  (с GIL):  4.8\n# python3.14t (без GIL): 1.3</pre>'
        '<p>Узнать версию — [[sys.version_info]], а есть ли GIL — [[sys._is_gil_enabled]]. Работает и здесь:</p>'
        + ex('import sys\n\nprint(sys.version_info[:2])\nprint(sys._is_gil_enabled())') +
        '<h3>Цена свободы: гонки</h3>'
        '<p>Без GIL потоки по-настоящему одновременно трогают общие данные — и всплывает [[гонка данных]]. <code>counter += 1</code> — это '
        '«прочитать, прибавить, записать». Если два потока прочитали одно и то же значение, одно прибавление потеряется. Честно говоря, это бывает '
        'и с GIL — он переключает потоки между шагами, — но редко, и GIL скрывал ошибку. Без него она вылезет сразу. Смоделируем по шагам:</p>'
        + ex('counter = 0\nlocal = {}\nsteps = [("A", "read"), ("B", "read"), ("A", "write"), ("B", "write")]\nfor who, step in steps:\n'
             '    if step == "read":\n        local[who] = counter\n    else:\n        counter = local[who] + 1\n    print(who, step, "→", counter)\n'
             'print("итог", counter, "вместо 2")') +
        '<p>Лечится [[блокировка|блокировкой]]: участок «прочитать-изменить-записать» обёртывают в <code>with lock:</code>, и второй поток ждёт, '
        'пока первый закончит:</p>'
        '<pre class="pc">lock = threading.Lock()\n\ndef add():\n    global counter\n    with lock:\n        counter += 1</pre>'
    )
    return th('Python без GIL', terms, body)


def fl_gil():
    return fl('Python без GIL', [
        q('Что ускорят потоки в Python с GIL?', 'Ожидание сети и диска', ['Вычисления на всех ядрах', 'Ничего'],
          'При ожидании GIL отпускается.'),
        qo('Что выведет программа?', 'counter = 5\na = counter\nb = counter\ncounter = a + 1\ncounter = b + 1\nprint(counter)', ['7', '5', '8'],
           'Оба «потока» прочитали 5, второй записал 6 поверх первого.'),
        q('Зачем with lock: вокруг counter += 1?', 'Чтобы другой поток не вклинился между чтением и записью', ['Чтобы ускорить сложение',
          'Чтобы counter нельзя было прочитать'], 'Замок делает три шага неделимыми.'),
    ])


def code_gil():
    return ts('Python без GIL', [
        task('Потерянные обновления. Общий счётчик равен 0. На вход подаётся расписание шагов через пробел вида A:r, A:w, B:r … (поток и шаг: r — '
             'прочитать счётчик в свою переменную, w — записать в счётчик своё прочитанное + 1). Выполни шаги по порядку и выведи «счётчик: N», '
             '«записей: W» и «потеряно: W − N» (запись без чтения перед ней — прочитанное считается 0). Если ничего не потеряно — ещё «гонки не было».',
             'Словарь «поток → прочитанное значение»; get(поток, 0).',
             'counter = 0\nseen = {}\nwrites = 0\nfor step in input().split():\n    who, action = step.split(":")\n    if action == "r":\n        seen[who] = counter\n'
             '    else:\n        counter = seen.get(who, 0) + 1\n        writes += 1\nprint(f"счётчик: {counter}")\nprint(f"записей: {writes}")\n'
             'print(f"потеряно: {writes - counter}")\nif writes == counter:\n    print("гонки не было")',
             ['A:r B:r A:w B:w', 'A:r A:w B:r B:w C:r C:w', 'A:r B:r C:r A:w B:w C:w A:r A:w']),
        task('Потоки с GIL и без. Первая строка — число потоков K. Вторая — длительности вычислительных задач в секундах через пробел. Задачи '
             'раздаются по порядку: каждая следующая — потоку, который освободится раньше всех (при равенстве — с меньшим номером). Без GIL потоки '
             'считают одновременно: время — когда закончит последний. С GIL вычисления идут по одной: время — сумма. Выведи «с GIL: X с», «без GIL: '
             'Y с» и «ускорение: Z» (две цифры после точки). Затем по потокам «поток N: задачи через пробел» (номера задач с 1; у потока без задач — «—»). '
             'Длительности — целые.',
             'busy — список «когда поток освободится»; поток = busy.index(min(busy)).',
             'k = int(input())\ntasks = list(map(int, input().split()))\nbusy = [0] * k\ngot = [[] for _ in range(k)]\nfor i, t in enumerate(tasks, 1):\n'
             '    n = busy.index(min(busy))\n    busy[n] += t\n    got[n].append(str(i))\nwith_gil = sum(tasks)\nfree = max(busy)\nprint(f"с GIL: {with_gil} с")\n'
             'print(f"без GIL: {free} с")\nprint(f"ускорение: {with_gil / free:.2f}")\nfor n in range(k):\n    print(f"поток {n + 1}: {\' \'.join(got[n]) or \'—\'}")',
             ['2\n3 3 3 3', '3\n5 1 1 1 4', '4\n10']),
    ])


DATA = json.dumps({'title': 'Мой <блог>', 'user': '<script>украсть()</script>', 'likes': 42, 'price': 7.5}, ensure_ascii=False)


def project():
    return pj('Безопасный шаблонизатор',
              'Сделай шаблонизатор в духе t-строк. Рядом лежит data.json — словарь значений. На вход подаются строки шаблона, последняя — «конец». '
              'В строке подстановки пишутся {имя} или {имя:формат} — формат как в f-строке (например >6 или .2f). Для каждой строки:\n'
              '1) разбери её на части: текст и подстановки (имя, формат);\n'
              '2) если какого-то имени нет в данных — выведи «строка N: нет значения ИМЯ» (про первое такое) и переходи к следующей строке;\n'
              '3) иначе собери строку: текст — как есть, значение — отформатируй по формату (без формата — просто str) и экранируй для HTML '
              '(& < > в этом порядке).\n'
              'В конце выведи «Строк: S, подстановок: P, экранировано: E» — S — сколько строк собрано успешно, P — сколько подстановок во всех успешно собранных строках, E — сколько '
              'из них изменились при экранировании.',
              'Разбор — как в задаче «Шаблон из текста»; имя и формат: if ":" in inner: name, spec = inner.split(":", 1), иначе формат пустой\n'
              'Форматирование по строке формата: f"{value:{spec}}" — формат тоже можно подставить',
              'import json\n\n\n' + ESC + '\n\ndef parse(text):\n    parts = []\n    pos = 0\n    while True:\n        start = text.find("{", pos)\n        if start == -1:\n            break\n'
              '        end = text.find("}", start)\n        if text[pos:start]:\n            parts.append(text[pos:start])\n        inner = text[start + 1:end]\n'
              '        if ":" in inner:\n            name, spec = inner.split(":", 1)\n        else:\n            name, spec = inner, ""\n        parts.append((name, spec))\n'
              '        pos = end + 1\n    if text[pos:]:\n        parts.append(text[pos:])\n    return parts\n\n\ndata = json.load(open("data.json", encoding="utf-8"))\n'
              'lines = subs = escaped = 0\nn = 0\nwhile True:\n    line = input()\n    if line == "конец":\n        break\n    n += 1\n    parts = parse(line)\n'
              '    missing = [p[0] for p in parts if type(p) is tuple and p[0] not in data]\n    if missing:\n        print(f"строка {n}: нет значения {missing[0]}")\n'
              '        continue\n    out = []\n    for p in parts:\n        if type(p) is tuple:\n            raw = f"{data[p[0]]:{p[1]}}" if p[1] else str(data[p[0]])\n'
              '            safe = escape(raw)\n            subs += 1\n            escaped += safe != raw\n            out.append(safe)\n        else:\n            out.append(p)\n'
              '    lines += 1\n    print("".join(out))\nprint(f"Строк: {lines}, подстановок: {subs}, экранировано: {escaped}")',
              ['<h1>{title}</h1>\n<p>{user} поставил лайк, всего {likes:>4}</p>\nЦена: {price:.2f} ₽\n{нет} и {title}\nконец', 'Просто текст\nконец', '{likes}{likes}\nконец'],
              files={'data.json': DATA})


def build():
    return topic('Новый Python: t-строки и потоки', 'шаблоны вместо f-строк, Python без GIL, гонки', [
        th_tstr(), fl_tstr(), code_tstr(),
        th_gil(), fl_gil(), code_gil(),
        project(),
    ], opt=True)
