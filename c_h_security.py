from dsl import *

# Нора после «Списочные выражения»: безопасность приложений, минимум из OWASP Top 10. Две теории: не доверяй вводу (инъекции, XSS и экранирование,
# обход пути, белые списки); пароли, секреты и доступ (хэш с солью через hashlib, утечки секретов, проверка прав на каждый запрос).
# try и модули ещё не пройдены: всё на строках, словарях, функциях и выражениях-генераторах; hashlib вводится здесь. Мини-проект — заметки с правами доступа.

ESC = ('def escape(text):\n    text = text.replace("&", "&amp;")\n    text = text.replace("<", "&lt;").replace(">", "&gt;")\n'
       '    return text.replace(\'"\', "&quot;").replace("\'", "&#x27;")\n')


def th_input():
    terms = [
        ('OWASP Top 10', 'Список десяти самых частых и опасных уязвимостей веб-приложений от сообщества OWASP: инъекции, сломанный контроль '
                         'доступа, утечки секретов и другие. Его знает каждый, кто пишет сайты.'),
        ('инъекция', 'Уязвимость: данные пользователя вклеиваются в команду (запрос к базе, команду терминала) и становятся её частью. '
                     'Лечится параметрами: команда отдельно, данные отдельно.'),
        ('XSS', 'Межсайтовый скриптинг: пользователь присылает текст с <script>, сайт показывает его другим как HTML — и чужой код '
                'выполняется в их браузере.'),
        ('экранирование', 'Замена особых символов безопасными: в HTML знак < превращается в &lt;, и браузер показывает знак, а не начинает тег.'),
        ('обход пути', 'Path traversal: имя файла вида ../../секрет.txt выводит программу из разрешённой папки.'),
        ('белый список', 'Проверка «разрешено только это» (буквы, цифры, известные команды). Надёжнее чёрного списка «запрещено это» — '
                         'всё плохое не перечислишь.'),
    ]
    body = (
        '<p>Взломы редко похожи на кино. Чаще кто-то вводит в поле не то, что ждал программист. [[OWASP Top 10]] — список самых частых '
        'дыр, и первая группа — доверие к вводу. Главная — [[инъекция]]. Пусть сайт ищет пользователя запросом к базе, вклеивая имя в строку:</p>'
        + ex('def find_user_query(name):\n    return "SELECT * FROM users WHERE name = \'" + name + "\'"\n\n\nprint(find_user_query("vika"))\n'
             'print(find_user_query("x\' OR \'1\'=\'1"))') +
        '<p>Во втором случае условие стало «имя x <b>или</b> 1 равно 1» — истинно для всех, и база отдаст всех пользователей. Лечение — '
        'никогда не склеивать команду с данными, а передавать данные отдельно, параметром. В Python с базой sqlite3 это выглядит так:</p>'
        '<pre class="pc">cur.execute("SELECT * FROM users WHERE name = ?", (name,))   # база сама поймёт, что name — просто текст</pre>'
        '<h3>XSS и экранирование</h3>'
        '<p>То же с HTML. Если комментарий <code>&lt;script&gt;украсть()&lt;/script&gt;</code> вставить в страницу как есть, браузер других '
        'посетителей выполнит этот код — это [[XSS]]. Перед показом текст проходит [[экранирование]]. Порядок важен: сначала &amp;, иначе '
        'испортишь уже заменённое:</p>'
        + ex(ESC + '\n\nprint(escape(\'<script>alert("hi")</script>\'))\nprint(escape("Tom & Jerry"))') +
        '<h3>Пути и белые списки</h3>'
        '<p>Сайт отдаёт файлы из папки uploads по имени из адреса. Имя <code>../config.py</code> выведет из папки — это [[обход пути]]. '
        'Пытаться запретить все опасные сочетания бесполезно: их много и они хитрые. Надёжнее [[белый список]]: разрешить только то, что '
        'точно безопасно:</p>'
        + ex('ALLOWED = "abcdefghijklmnopqrstuvwxyz0123456789_-."\n\n\ndef is_safe(name):\n    return name != "" and ".." not in name and all(ch in ALLOWED for ch in name.lower())\n\n\n'
             'for name in ["cat.png", "../config.py", "notes 1.txt", "Report_2.PDF"]:\n    print(name, is_safe(name))')
    )
    return th('Не доверяй вводу', terms, body)


def fl_input():
    return fl('Не доверяй вводу', [
        q('Как правильно защититься от SQL-инъекции?', 'Передавать данные параметром, отдельно от запроса', ['Удалять из ввода слово SELECT',
          'Писать запросы маленькими буквами'], 'Склейку не спасут никакие фильтры.'),
        qo('Что выведет программа?', 'print("<b>".replace("&", "&amp;").replace("<", "&lt;"))', ['<b>', '&amp;lt;b>', '&lt;b&gt;'],
           '& в строке не было; < стал &lt;, а > не заменяли.'),
        q('Почему белый список лучше чёрного?', 'Всё опасное не перечислишь, а разрешённое — можно', ['Он работает быстрее',
          'Чёрные списки запрещены законом'], 'Атакующий найдёт вариант, о котором ты не подумал.'),
        q('Почему & экранируют первым?', 'Иначе испортятся уже вставленные &lt; и &gt;', ['Так короче код', '& — самый частый символ'],
          '&lt; содержит &, и он стал бы &amp;lt;.'),
    ])


def code_input():
    return ts('Не доверяй вводу', [
        task('Экранирование. Напиши функцию escape(text) для HTML: & → &amp;, < → &lt;, > → &gt;, " → &quot;, \' → &#x27;. Каждый исходный символ '
             'должен замениться ровно один раз.',
             'Порядок: сначала &, потом остальные. replace возвращает новую строку — присваивай результат.',
             ESC, ['print(escape("<b>Привет</b>"))\nprint(escape("5 > 3 & 2 < 4"))', 'print(escape(\'Он сказал: "Я\\\'м тут"\'))\nprint(escape("&lt;"))\nprint(escape(""))'],
             tail=TL),
        task('Безопасное имя файла. Напиши функцию safe_path(name): если имя пустое, длиннее 50 символов, содержит «..», начинается с точки или содержит '
             'символ не из белого списка (латинские буквы любого регистра, цифры, _ - .), верни None; иначе верни "uploads/" + имя.',
             'Белый список — строка разрешённых символов; проверка — all(ch in ALLOWED for ch in name.lower()).',
             'ALLOWED = "abcdefghijklmnopqrstuvwxyz0123456789_-."\n\n\ndef safe_path(name):\n    if name == "" or len(name) > 50 or ".." in name or name.startswith("."):\n'
             '        return None\n    if not all(ch in ALLOWED for ch in name.lower()):\n        return None\n    return "uploads/" + name\n',
             ['print(safe_path("cat.png"))\nprint(safe_path("../config.py"))\nprint(safe_path("Report_2-final.PDF"))',
              'print(safe_path(".env"))\nprint(safe_path("отчёт.txt"))\nprint(safe_path("a/b.txt"))\nprint(safe_path("x" * 51))\nprint(safe_path(""))'],
             tail=TL),
        task('Ловушка для инъекций. На вход подаются имена, которые пользователи вводили в поиск, последняя строка — «конец». Для каждого выведи запрос, '
             'который получился бы склейкой: SELECT * FROM users WHERE name = \'ИМЯ\'. Если в имени есть одинарная кавычка, допиши ниже строку «  ! инъекция: '
             'кавычка закрыла строку» и безопасный вариант «  безопасно: SELECT * FROM users WHERE name = ? с параметром (\'ИМЯ\',)» — параметр — '
             'кортеж, выведенный print-ом. В конце — «Подозрительных: N из M».',
             'Запрос: "SELECT * FROM users WHERE name = \'" + name + "\'". Кортеж из одного элемента — (name,); print сам расставит кавычки вокруг строки внутри.',
             'n = bad = 0\nwhile True:\n    name = input()\n    if name == "конец":\n        break\n    n += 1\n    print("SELECT * FROM users WHERE name = \'" + name + "\'")\n'
             '    if "\'" in name:\n        bad += 1\n        print("  ! инъекция: кавычка закрыла строку")\n'
             '        print("  безопасно: SELECT * FROM users WHERE name = ? с параметром", (name,))\nprint(f"Подозрительных: {bad} из {n}")',
             ["vika\nx' OR '1'='1\nO'Brien\nконец", 'admin\nконец']),
    ])


def th_secrets():
    terms = [
        ('хэш', 'Результат хэш-функции: строка фиксированной длины, по которой нельзя восстановить исходный текст. Одинаковый текст — '
                'одинаковый хэш, малейшее изменение — совсем другой.'),
        ('hashlib', 'Модуль с хэш-функциями. hashlib.sha256(байты) — объект хэша.'),
        ('hashlib.sha256', 'hashlib.sha256(байты) — хэш SHA-256 от байтов; строку сначала переводят в байты через encode.'),
        ('encode', 'строка.encode() — перевести строку в байты (по умолчанию в кодировке UTF-8). Хэш-функции работают с байтами.'),
        ('hexdigest', 'хэш.hexdigest() — значение хэша строкой из 64 шестнадцатеричных цифр.'),
        ('соль', 'Случайная строка, своя у каждого пользователя, которую добавляют к паролю перед хэшированием. Одинаковые пароли получают '
                 'разные хэши, а готовые таблицы «пароль → хэш» перестают работать.'),
        ('контроль доступа', 'Проверка на каждый запрос: этот пользователь имеет право на это действие с этим объектом? Самая частая дыра из '
                             'OWASP Top 10 — проверку забыли.'),
        ('IDOR', 'Insecure Direct Object Reference: поменял в адресе /notes/15 на /notes/16 — и читаешь чужую заметку, потому что сервер проверил '
                 'только «вошёл ли», но не «чья это».'),
    ]
    body = (
        '<p>Пароли не хранят в открытом виде: базы утекают, и тогда утекут пароли от всего — люди ставят один пароль везде. Хранят [[хэш]] — '
        'отпечаток пароля, по которому пароль не восстановить. При входе считают хэш введённого и сравнивают с сохранённым. В Python есть '
        'модуль [[hashlib]]; [[hashlib.sha256]] принимает байты — строку переводит в них [[encode]], а [[hexdigest]] даёт хэш строкой:</p>'
        + ex('import hashlib\n\nprint(hashlib.sha256("qwerty".encode()).hexdigest())\nprint(hashlib.sha256("qwertY".encode()).hexdigest())') +
        '<p>Но у популярных паролей хэши давно собраны в таблицы. Поэтому к паролю добавляют [[соль]] — свою для каждого пользователя:</p>'
        + ex('import hashlib\n\n\ndef password_hash(password, salt):\n    return hashlib.sha256((salt + password).encode()).hexdigest()\n\n\n'
             'print(password_hash("qwerty", "a91f")[:16])\nprint(password_hash("qwerty", "7c2e")[:16])') +
        '<p>Один пароль — разные хэши. На настоящих сайтах вместо sha256 берут медленные функции bcrypt или argon2 и случайную соль из модуля '
        'secrets — перебор миллиардов вариантов становится слишком долгим:</p>'
        '<pre class="pc">import bcrypt\nstored = bcrypt.hashpw(password.encode(), bcrypt.gensalt())\nbcrypt.checkpw(attempt.encode(), stored)   # True или False</pre>'
        '<h3>Секреты и доступ</h3>'
        '<p>Ключи API и пароли от баз не пишут в коде: репозиторий увидят все, а git помнит историю — удалённый ключ всё равно лежит в старых '
        'коммитах. Утёк — отзывают и выпускают новый. Боты на GitHub ищут ключи в публичных репозиториях круглосуточно — по шаблонам вроде '
        '<code>ghp_</code> (токен GitHub) или <code>sk-</code> (ключи многих API).</p>'
        '<p>И самая частая дыра — забытый [[контроль доступа]]. «Пользователь вошёл» не значит «ему можно всё». На каждый запрос проверяют '
        'право на конкретный объект — иначе получится [[IDOR]]:</p>'
        + ex('notes = {15: {"owner": "vika", "text": "мой пароль от вайфая"}, 16: {"owner": "tim", "text": "купить хлеб"}}\n\n\n'
             'def read(user, note_id):\n    note = notes.get(note_id)\n    if note is None:\n        return "404"\n    if note["owner"] != user:\n        return "403"\n'
             '    return note["text"]\n\n\nprint(read("tim", 16), read("tim", 15), read("tim", 99))')
    )
    return th('Пароли, секреты, доступ', terms, body)


def fl_secrets():
    return fl('Пароли, секреты, доступ', [
        q('Зачем к паролю добавляют соль?', 'Чтобы одинаковые пароли давали разные хэши', ['Чтобы пароль был длиннее для пользователя',
          'Чтобы хэш можно было расшифровать'], 'И чтобы не работали готовые таблицы хэшей.'),
        q('Ключ API случайно закоммитили и тут же удалили. Что делать?', 'Отозвать ключ и выпустить новый', ['Ничего: коммит уже удалён',
          'Переименовать переменную с ключом'], 'git хранит историю — старый коммит с ключом никуда не делся.'),
        q('Сервер проверяет только «вошёл ли пользователь». Какая это дыра?', 'IDOR: можно открыть чужой объект по номеру', ['XSS', 'Инъекция'],
          'Нужна проверка права на конкретный объект.'),
        qo('Сколько символов выведет программа?', 'import hashlib\nprint(len(hashlib.sha256("a".encode()).hexdigest()))', ['32', '1', '256'],
           'SHA-256 — 256 бит, это 64 шестнадцатеричные цифры.'),
    ])


def code_secrets():
    return ts('Пароли, секреты, доступ', [
        task('Хранилище паролей. Пароли храни только как sha256 от (соль + пароль) в hexdigest. Команды до «конец»: «рег ЛОГИН ПАРОЛЬ СОЛЬ» — '
             'зарегистрировать («ЛОГИН: зарегистрирован», а если логин занят — «ЛОГИН: занят»; пароль короче 8 символов — «ЛОГИН: слабый пароль», не '
             'регистрировать); «вход ЛОГИН ПАРОЛЬ» — «ЛОГИН: вход выполнен» или «Неверный логин или пароль» (одинаково для чужого логина и неверного '
             'пароля — чтобы не подсказывать, какие логины есть). В конце для каждого пользователя в порядке регистрации — «ЛОГИН СОЛЬ ПЕРВЫЕ_12_ЗНАКОВ_ХЭША».',
             'users[login] = (salt, hash). Хэш: hashlib.sha256((salt + password).encode()).hexdigest().',
             'import hashlib\n\n\ndef password_hash(password, salt):\n    return hashlib.sha256((salt + password).encode()).hexdigest()\n\n\nusers = {}\nwhile True:\n'
             '    cmd = input().split()\n    if cmd == ["конец"]:\n        break\n    if cmd[0] == "рег":\n        login, password, salt = cmd[1:]\n        if login in users:\n'
             '            print(f"{login}: занят")\n        elif len(password) < 8:\n            print(f"{login}: слабый пароль")\n        else:\n'
             '            users[login] = (salt, password_hash(password, salt))\n            print(f"{login}: зарегистрирован")\n    else:\n        login, password = cmd[1:]\n'
             '        if login in users and password_hash(password, users[login][0]) == users[login][1]:\n            print(f"{login}: вход выполнен")\n'
             '        else:\n            print("Неверный логин или пароль")\nfor login, (salt, h) in users.items():\n    print(login, salt, h[:12])',
             ['рег vika supersecret a91f\nрег tim 12345 77aa\nрег tim qwerty123 77aa\nвход vika supersecret\nвход vika Supersecret\nвход bob supersecret\n'
              'вход tim qwerty123\nрег vika other123 0000\nконец', 'рег a password a\nрег b password b\nконец']),
        task('Сканер секретов. На вход подаются строки кода, последняя — «КОНЕЦ». Найди в каждой строке подозрения (проверяй по порядку, на строку — '
             'первое сработавшее): строковое значение в кавычках (" или \'), которое начинается с ghp_ — «токен GitHub», с sk- — «ключ API», с AKIA — '
             '«ключ AWS»; иначе — если в строке есть «=», а слева от первого «=» (в нижнем регистре) есть password, passwd, secret, token или key и справа '
             'стоит строка в кавычках — «пароль в коде». Для каждой находки выведи «строка N: ПРИЧИНА: ЗНАЧЕНИЕ» — значение без кавычек, где видны только '
             'первые 4 символа, остальные заменены звёздочками. В конце — «Найдено: K» и, если K > 0, «Отзови ключи и вынеси их в переменные окружения».',
             'Значения в кавычках: строку раздели по кавычке — нечётные куски split(\'"\') лежат внутри кавычек (то же для \').\n'
             'Маска: value[:4] + "*" * (len(value) - 4).',
             'def quoted(line):\n    values = []\n    for q in (\'"\', "\'"):\n        values += line.split(q)[1::2]\n    return values\n\n\ndef mask(value):\n'
             '    return value[:4] + "*" * (len(value) - 4)\n\n\nPREFIXES = [("ghp_", "токен GitHub"), ("sk-", "ключ API"), ("AKIA", "ключ AWS")]\n'
             'WORDS = ["password", "passwd", "secret", "token", "key"]\nfound = 0\nn = 0\nwhile True:\n    line = input()\n    if line == "КОНЕЦ":\n        break\n    n += 1\n'
             '    values = quoted(line)\n    hit = None\n    for v in values:\n        for prefix, reason in PREFIXES:\n            if hit is None and v.startswith(prefix):\n'
             '                hit = (reason, v)\n    if hit is None and "=" in line and values:\n        left, right = line.split("=", 1)\n'
             '        if any(w in left.lower() for w in WORDS) and quoted(right):\n            hit = ("пароль в коде", quoted(right)[0])\n    if hit:\n        found += 1\n'
             '        print(f"строка {n}: {hit[0]}: {mask(hit[1])}")\nprint(f"Найдено: {found}")\nif found:\n    print("Отзови ключи и вынеси их в переменные окружения")',
             ['import requests\nAPI_KEY = "sk-live-1234567890"\nheaders = {"Authorization": "token ghp_abcdef123456"}\nurl = "https://api.itp/token"\n'
              'DB_PASSWORD = \'hunter2hunter2\'\nretries = 3\nКОНЕЦ', 'name = "Вика"\nprint("ключ")\nКОНЕЦ', 'aws = "AKIAIOSFODNN7EXAMPLE"\nКОНЕЦ']),
    ])


def project():
    return pj('Заметки с правами',
              'Сервис заметок. Первая строка — пользователи через пробел в виде ЛОГИН:РОЛЬ (роль user или admin). Дальше команды до «конец»:\n'
              '— «ЛОГИН создать ТЕКСТ» — новая заметка с номером по порядку с 1, хозяин — ЛОГИН; вывести «#N создана». Текст перед сохранением '
              'экранируй для HTML (& < > " \'), как в задаче выше;\n'
              '— «ЛОГИН читать N» — показать «#N: ТЕКСТ» хозяину и админу;\n'
              '— «ЛОГИН удалить N» — удалить может только хозяин; админ — тоже, но тогда вывести «#N удалена админом»; хозяин — «#N удалена».\n'
              'Порядок проверок: неизвестный логин — «401»; нет заметки — «404»; нет прав — «403». Каждый ответ 403 — это попытка залезть в чужое: '
              'запоминай её. В конце выведи «Попыток IDOR: K» и, если K > 0, по логинам в алфавитном порядке «ЛОГИН: число попыток».',
              'Заметки — словарь номер → {"owner": …, "text": …}; номер новой — счётчик, не len (после удалений len врёт)\n'
              'Функция allowed(user, action, note) возвращает True/False — так правила в одном месте\n'
              'Текст команды «создать» может быть из нескольких слов: line.split(" ", 2)',
              ESC + '\n\nroles = dict(pair.split(":") for pair in input().split())\nnotes = {}\nlast = 0\nidor = {}\n\n\n'
              'def allowed(user, action, note):\n    if roles[user] == "admin":\n        return True\n    return note["owner"] == user\n\n\nwhile True:\n    line = input()\n'
              '    if line == "конец":\n        break\n    user, action, arg = line.split(" ", 2)\n    if user not in roles:\n        print("401")\n        continue\n'
              '    if action == "создать":\n        last += 1\n        notes[last] = {"owner": user, "text": escape(arg)}\n        print(f"#{last} создана")\n        continue\n'
              '    note = notes.get(int(arg))\n    if note is None:\n        print("404")\n    elif not allowed(user, action, note):\n        print("403")\n'
              '        idor[user] = idor.get(user, 0) + 1\n    elif action == "читать":\n        print(f"#{arg}: {note[\'text\']}")\n    else:\n        del notes[int(arg)]\n'
              '        print(f"#{arg} удалена" + (" админом" if note["owner"] != user else ""))\nprint(f"Попыток IDOR: {sum(idor.values())}")\nfor user in sorted(idor):\n'
              '    print(f"{user}: {idor[user]}")',
              ['vika:user tim:user boss:admin\nvika создать пароль от вайфая <b>12345</b>\ntim создать купить хлеб & молоко\ntim читать 1\ntim читать 2\n'
               'boss читать 1\nvika удалить 2\nboss удалить 2\ntim читать 2\nhacker читать 1\ntim удалить 1\nvika читать 1\nконец',
               'a:user\na создать раз\na удалить 1\na создать два\na читать 2\na читать 1\nконец'])


def build():
    return topic('Безопасность: закрываем дыры', 'инъекции, XSS, пароли, секреты, доступ', [
        th_input(), fl_input(), code_input(),
        th_secrets(), fl_secrets(), code_secrets(),
        project(),
    ], opt=True)
