import json
from dsl import *

# Нора после «Запросы к серверам»: чат-боты на учебном мессенджере (устроен как Telegram Bot API, но внутри приложения).
# Сервер бота: GET /getUpdates?token=…&offset=N — сообщения с update_id ≥ N; POST /sendMessage?token=… с json {chat_id, text}.
# Две теории: как устроен бот (токен, обновления, offset, ответы); команды и обработчики (словарь функций, состояние по чатам).
# Мини-проект — бот погоды. Токен — из переменной окружения с запасным учебным значением.


def chat(updates, token='bot-demo', extra=None):
    spec = {'bot.itp': {'routes': {}, 'bot': {'token': token, 'updates': [{'update_id': i, 'message': m} for i, m in enumerate(updates, 1)]}}}
    spec.update(extra or {})
    return {'_itp_servers.json': json.dumps(spec, ensure_ascii=False)}


def msg(chat_id, name, text):
    return {'chat_id': chat_id, 'from': name, 'text': text}


DEMO = chat([msg(7, 'Аня', 'привет'), msg(9, 'Zed', 'кто тут?'), msg(7, 'Аня', 'как дела?')])
ECHO = chat([msg(7, 'Аня', 'привет, бот'), msg(9, 'Zed', 'ау'), msg(7, 'Аня', 'повтори за мной'), msg(12, 'Вика', 'эхо-эхо')])
COUNT = chat([msg(7, 'Аня', 'раз'), msg(9, 'Zed', 'йо'), msg(7, 'Аня', 'два'), msg(7, 'Аня', 'три'), msg(9, 'Zed', 'ещё')])
CMDS = chat([msg(7, 'Аня', '/start'), msg(7, 'Аня', '/sum 2 3 10'), msg(9, 'Zed', 'просто текст'), msg(9, 'Zed', '/help'),
             msg(7, 'Аня', '/sum'), msg(9, 'Zed', '/dance'), msg(12, 'Вика', '/sum 7 x')])
REMIND = chat([msg(7, 'Аня', '/remind 18:00 тренировка'), msg(7, 'Аня', '/remind 09:30 позвонить бабушке'), msg(9, 'Zed', '/list'),
               msg(7, 'Аня', '/list'), msg(7, 'Аня', '/remind 7 утра'), msg(9, 'Zed', '/remind 21:15 матч'), msg(9, 'Zed', '/list')])
WEATHER = chat([msg(7, 'Аня', '/start'), msg(7, 'Аня', '/weather Тюмень'), msg(9, 'Zed', '/weather Сочи'), msg(9, 'Zed', '/weather Атлантида'),
                msg(7, 'Аня', '/city Сочи'), msg(7, 'Аня', '/weather'), msg(12, 'Вика', '/weather'), msg(12, 'Вика', 'спасибо')],
               extra={'api.weather.itp': {'routes': {'/now': {'param': 'city', 'variants': {
                   'Тюмень': {'temp': -3, 'sky': 'снег'}, 'Сочи': {'temp': 14, 'sky': 'ясно'}}}}}})


def th_bot():
    terms = [
        ('бот', 'Программа, которая переписывается с людьми в мессенджере: получает их сообщения через API мессенджера и отвечает.'),
        ('токен бота', 'Секретная строка, которую выдаёт мессенджер при создании бота. По ней сервер понимает, от чьего имени запрос. Хранят в '
                       'переменной окружения, не в коде.'),
        ('os', 'Модуль для связи с операционной системой; в нём os.environ — переменные окружения.'),
        ('os.environ', 'Словарь переменных окружения. os.environ.get("ИМЯ", "запасное") — значение или запасное, если переменной нет. '
                       'В ИТП переменных нет, поэтому срабатывает запасное.'),
        ('getUpdates', 'Запрос «какие новые сообщения пришли боту»: ответ — список обновлений с номерами update_id.'),
        ('offset', 'Параметр getUpdates: присылать только обновления с номером не меньше offset. Бот передаёт номер последнего + 1, '
                   'чтобы не отвечать дважды на одно сообщение.'),
        ('sendMessage', 'Запрос «отправь сообщение»: chat_id — в какой чат, text — что написать.'),
    ]
    body = (
        '<p>[[бот]] в Telegram или другом мессенджере — обычная программа. Она раз за разом спрашивает у сервера мессенджера, не пришло ли '
        'новых сообщений, и отвечает на них. В ИТП вместо Telegram — учебный мессенджер по адресу <code>http://bot.itp</code>: он устроен '
        'так же, но живёт прямо в приложении.</p>'
        '<p>Каждый запрос бот подписывает [[токен бота]]ом. Новые сообщения отдаёт [[getUpdates]] — список обновлений, у каждого номер '
        '<code>update_id</code> и само сообщение: чат, автор и текст:</p>'
        + ex('import os\nimport requests\n\nTOKEN = os.environ.get("BOT_TOKEN", "bot-demo")\nAPI = "http://bot.itp"\n\n'
             'updates = requests.get(f"{API}/getUpdates", params={"token": TOKEN}).json()["result"]\nfor u in updates:\n'
             '    m = u["message"]\n    print(u["update_id"], m["chat_id"], m["from"], m["text"])', files=DEMO) +
        '<p>Чтобы ответить, бот отправляет [[sendMessage]] с номером чата и текстом. Сервер возвращает отправленное сообщение. А чтобы при следующем '
        'опросе не получить те же сообщения ещё раз, бот передаёт [[offset]] — номер последнего обработанного обновления плюс один:</p>'
        + ex('import requests\n\nAPI, TOKEN = "http://bot.itp", "bot-demo"\nupdates = requests.get(f"{API}/getUpdates", params={"token": TOKEN}).json()["result"]\n'
             'for u in updates:\n    m = u["message"]\n    r = requests.post(f"{API}/sendMessage", params={"token": TOKEN}, json={"chat_id": m["chat_id"], "text": "Привет, " + m["from"] + "!"})\n'
             '    sent = r.json()["result"]\n    print("→", sent["chat_id"], sent["text"])\nlast = updates[-1]["update_id"]\n'
             'again = requests.get(f"{API}/getUpdates", params={"token": TOKEN, "offset": last + 1}).json()["result"]\nprint("новых:", len(again))', files=DEMO) +
        '<p>Настоящий бот делает это в бесконечном цикле с паузой в пару секунд. Здесь сообщения уже пришли, поэтому хватает одного прохода.</p>'
    )
    return th('Как устроен бот', terms, body)


def fl_bot():
    return fl('Как устроен бот', [
        q('Зачем бот передаёт offset в getUpdates?', 'Чтобы не получать одни и те же сообщения снова',
          ['Чтобы сервер отвечал быстрее', 'Без offset токен не проверяется'], 'offset — номер последнего обработанного + 1.'),
        q('Что нужно sendMessage?', 'Номер чата и текст', ['Только текст', 'Имя пользователя и пароль'], 'chat_id говорит, кому отвечать.'),
        q('Где хранят токен бота?', 'В переменной окружения, а не в коде', ['В начале файла бота', 'В тексте приветствия'],
          'Кто знает токен, может писать от имени бота.'),
    ])


def code_bot():
    return ts('Как устроен бот', [
        task('Эхо-бот. Учебный мессенджер http://bot.itp: GET /getUpdates с параметром token отдаёт {"ok": true, "result": [обновления]}, у обновления — '
             'update_id и message с chat_id, from и text; POST /sendMessage с token и json={"chat_id": …, "text": …} отправляет сообщение и возвращает '
             'его в result. Токен — из переменной окружения BOT_TOKEN, запасное значение bot-demo. Ответь на каждое сообщение его же текстом и после '
             'каждой отправки выведи «→ CHAT_ID: ТЕКСТ» из ответа сервера. В конце — «Ответов: N».',
             'params={"token": TOKEN} — и для GET, и для POST. Отправленное — r.json()["result"].',
             'import os\nimport requests\n\nTOKEN = os.environ.get("BOT_TOKEN", "bot-demo")\nAPI = "http://bot.itp"\n'
             'updates = requests.get(f"{API}/getUpdates", params={"token": TOKEN}).json()["result"]\nfor u in updates:\n    m = u["message"]\n'
             '    sent = requests.post(f"{API}/sendMessage", params={"token": TOKEN}, json={"chat_id": m["chat_id"], "text": m["text"]}).json()["result"]\n'
             '    print(f"→ {sent[\'chat_id\']}: {sent[\'text\']}")\nprint(f"Ответов: {len(updates)}")',
             [''], files=ECHO),
        task('Счётчик. Тот же мессенджер. На каждое сообщение бот отвечает автору «ИМЯ, это твоё N-е сообщение», где N — сколько сообщений этот чат '
             'уже прислал, считая текущее. Выведи отправленные ответы «→ CHAT_ID: ТЕКСТ», затем строку «Самый болтливый: ИМЯ» — автор с наибольшим '
             'числом сообщений (при равенстве — тот, кто написал первым).',
             'Счётчики по chat_id — словарь; имя автора запомни отдельно. «Первым» — порядок появления в словаре.',
             'import os\nimport requests\n\nTOKEN = os.environ.get("BOT_TOKEN", "bot-demo")\nAPI = "http://bot.itp"\ncounts = {}\nnames = {}\n'
             'for u in requests.get(f"{API}/getUpdates", params={"token": TOKEN}).json()["result"]:\n    m = u["message"]\n    cid = m["chat_id"]\n'
             '    counts[cid] = counts.get(cid, 0) + 1\n    names[cid] = m["from"]\n    text = f"{m[\'from\']}, это твоё {counts[cid]}-е сообщение"\n'
             '    sent = requests.post(f"{API}/sendMessage", params={"token": TOKEN}, json={"chat_id": cid, "text": text}).json()["result"]\n'
             '    print(f"→ {sent[\'chat_id\']}: {sent[\'text\']}")\nbest = max(counts, key=counts.get)\nprint(f"Самый болтливый: {names[best]}")',
             [''], files=COUNT),
    ])


def th_cmds():
    terms = [
        ('команда бота', 'Сообщение со слешем: /start, /help, /sum 2 3. Первое слово — команда, остальное — аргументы.'),
        ('обработчик команды', 'Функция, которая отвечает на одну команду. Обработчики хранят в словаре «команда → функция», и главный цикл только '
                               'находит нужную.'),
    ]
    body = (
        '<p>Боту пишут [[команда бота]]ми: <code>/start</code>, <code>/help</code>, <code>/sum 2 3</code>. Удобная архитектура — по функции на команду и '
        'словарь «команда → функция». Каждый [[обработчик команды]] получает аргументы и возвращает текст ответа, а главный цикл только находит нужную '
        'функцию и отправляет её ответ:</p>'
        + ex('def start(args):\n    return "Привет! Я умею /sum"\n\n\ndef add(args):\n    return str(sum(int(a) for a in args))\n\n\n'
             'HANDLERS = {"/start": start, "/sum": add}\n\nfor text in ["/start", "/sum 2 3 10", "/dance", "привет"]:\n    cmd, *args = text.split()\n'
             '    handler = HANDLERS.get(cmd)\n    print(text, "→", handler(args) if handler else "Не знаю такую команду")') +
        '<p><code>cmd, *args = text.split()</code> кладёт первое слово в cmd, а все остальные — списком в args (звёздочка собирает «всё остальное», '
        'как *args у функций). Новая команда — новая функция и строка в словаре, главный цикл не меняется.</p>'
        '<h3>Память бота</h3>'
        '<p>Боту часто нужно помнить что-то про каждого собеседника: выбранный город, список дел, счёт в игре. Это словарь по chat_id: у каждого чата '
        'своя запись, и собеседники друг другу не мешают.</p>'
    )
    return th('Команды и обработчики', terms, body)


def fl_cmds():
    return fl('Команды и обработчики', [
        qo('Что выведет программа?', 'cmd, *args = "/sum 4 5 6".split()\nprint(cmd, args)', ["/sum 4 5 6", "/sum ['4 5 6']", "/sum 4"],
           'args собирает все остальные слова списком: /sum [\'4\', \'5\', \'6\'].'),
        q('Зачем обработчики команд хранят в словаре?', 'Чтобы добавлять команды, не трогая главный цикл', ['Иначе бот не запустится', 'Словарь работает без интернета'],
          'Цикл только ищет функцию по команде.'),
        q('Как бот помнит город каждого собеседника отдельно?', 'Словарь, где ключ — chat_id', ['Одна переменная city', 'Файл на компьютере собеседника'],
          'У каждого чата — своя запись.'),
    ])


def code_cmds():
    return ts('Команды и обработчики', [
        task('Бот-калькулятор. Тот же мессенджер http://bot.itp (токен bot-demo). Команды: «/start» → «Привет! Команды: /sum, /help»; «/help» → '
             '«/sum ЧИСЛА — сложу целые числа»; «/sum A B …» → сумма; если чисел нет — «Напиши числа после /sum», если какое-то не целое — '
             '«Только целые числа». Сообщение без слеша → «Я понимаю только команды», незнакомая команда → «Не знаю команду /X». Сделай обработчики '
             'функциями в словаре. Выводи отправленные ответы «→ CHAT_ID: ТЕКСТ».',
             'cmd, *args = text.split(); проверка целого: все ли a.lstrip("-").isdigit().',
             'import requests\n\nAPI, TOKEN = "http://bot.itp", "bot-demo"\n\n\ndef start(args):\n    return "Привет! Команды: /sum, /help"\n\n\ndef help_(args):\n'
             '    return "/sum ЧИСЛА — сложу целые числа"\n\n\ndef add(args):\n    if not args:\n        return "Напиши числа после /sum"\n'
             '    if not all(a.lstrip("-").isdigit() for a in args):\n        return "Только целые числа"\n    return str(sum(int(a) for a in args))\n\n\n'
             'HANDLERS = {"/start": start, "/help": help_, "/sum": add}\nfor u in requests.get(f"{API}/getUpdates", params={"token": TOKEN}).json()["result"]:\n'
             '    m = u["message"]\n    cmd, *args = m["text"].split()\n    if not cmd.startswith("/"):\n        reply = "Я понимаю только команды"\n'
             '    elif cmd in HANDLERS:\n        reply = HANDLERS[cmd](args)\n    else:\n        reply = f"Не знаю команду {cmd}"\n'
             '    sent = requests.post(f"{API}/sendMessage", params={"token": TOKEN}, json={"chat_id": m["chat_id"], "text": reply}).json()["result"]\n'
             '    print(f"→ {sent[\'chat_id\']}: {sent[\'text\']}")',
             [''], files=CMDS),
        task('Напоминалка. Тот же мессенджер. «/remind ЧЧ:ММ ТЕКСТ» сохраняет напоминание этого чата и отвечает «Запомнил: ЧЧ:ММ ТЕКСТ»; если время не в '
             'формате ЧЧ:ММ (две цифры, двоеточие, две цифры) — «Время пиши как ЧЧ:ММ». «/list» отвечает списком напоминаний этого чата по времени, '
             'строками «ЧЧ:ММ ТЕКСТ» через перевод строки, или «Напоминаний нет». Выводи отправленные ответы «→ CHAT_ID: ТЕКСТ» (ответ из нескольких '
             'строк печатается как есть).',
             'Напоминания — словарь chat_id → список пар (время, текст). Разбор: cmd, *args = text.split(); время — args[0], текст — " ".join(args[1:]).\n'
             'Строки «ЧЧ:ММ» сравниваются правильно и как текст.',
             'import requests\n\nAPI, TOKEN = "http://bot.itp", "bot-demo"\nreminders = {}\nfor u in requests.get(f"{API}/getUpdates", params={"token": TOKEN}).json()["result"]:\n'
             '    m = u["message"]\n    cid = m["chat_id"]\n    cmd, *args = m["text"].split()\n    if cmd == "/remind":\n        t = args[0] if args else ""\n'
             '        ok = len(t) == 5 and t[2] == ":" and t[:2].isdigit() and t[3:].isdigit()\n        if ok:\n            reminders.setdefault(cid, []).append((t, " ".join(args[1:])))\n'
             '            reply = f"Запомнил: {t} {\' \'.join(args[1:])}"\n        else:\n            reply = "Время пиши как ЧЧ:ММ"\n    else:\n'
             '        items = sorted(reminders.get(cid, []))\n        reply = "\\n".join(f"{t} {x}" for t, x in items) if items else "Напоминаний нет"\n'
             '    sent = requests.post(f"{API}/sendMessage", params={"token": TOKEN}, json={"chat_id": cid, "text": reply}).json()["result"]\n'
             '    print(f"→ {sent[\'chat_id\']}: {sent[\'text\']}")',
             [''], files=REMIND),
    ])


def project():
    return pj('Бот погоды',
              'Бот погоды в учебном мессенджере http://bot.itp (токен — из переменной окружения BOT_TOKEN, запасное bot-demo). Погоду он берёт у сервиса '
              'http://api.weather.itp/now с параметром city: JSON с temp и sky, нет города — код 404. Команды:\n'
              '— «/start» → «Привет! Напиши /weather ГОРОД или выбери город: /city ГОРОД»;\n'
              '— «/city ГОРОД» → запомнить город этого чата и ответить «Запомнил: ГОРОД»;\n'
              '— «/weather ГОРОД» → «ГОРОД: T°, НЕБО» (плюс у положительной температуры: «+14°»); без города — по запомненному городу чата, а если его '
              'нет — «Сначала выбери город: /city ГОРОД»; неизвестный город — «Не знаю город ГОРОД»;\n'
              '— всё остальное → «Не понимаю. Напиши /start».\n'
              'Обработчики — функции в словаре, они получают chat_id и аргументы. Выводи отправленные ответы «→ CHAT_ID: ТЕКСТ», а в конце — «Запросов '
              'погоды: N» (сколько раз бот обращался к сервису погоды).',
              'Город из нескольких слов собирай " ".join(args)\nПамять — словарь chat_id → город\nЗнак: f"{t:+}" даёт «+14» и «-3»',
              'import os\nimport requests\n\nTOKEN = os.environ.get("BOT_TOKEN", "bot-demo")\nAPI = "http://bot.itp"\ncities = {}\nweather_calls = 0\n\n\n'
              'def start(cid, args):\n    return "Привет! Напиши /weather ГОРОД или выбери город: /city ГОРОД"\n\n\ndef city(cid, args):\n    cities[cid] = " ".join(args)\n'
              '    return f"Запомнил: {cities[cid]}"\n\n\ndef weather(cid, args):\n    global weather_calls\n    name = " ".join(args) or cities.get(cid)\n    if not name:\n'
              '        return "Сначала выбери город: /city ГОРОД"\n    weather_calls += 1\n    r = requests.get("http://api.weather.itp/now", params={"city": name})\n'
              '    if r.status_code == 404:\n        return f"Не знаю город {name}"\n    w = r.json()\n    return f"{name}: {w[\'temp\']:+}°, {w[\'sky\']}"\n\n\n'
              'HANDLERS = {"/start": start, "/city": city, "/weather": weather}\nfor u in requests.get(f"{API}/getUpdates", params={"token": TOKEN}).json()["result"]:\n'
              '    m = u["message"]\n    cmd, *args = m["text"].split()\n    handler = HANDLERS.get(cmd)\n    reply = handler(m["chat_id"], args) if handler else "Не понимаю. Напиши /start"\n'
              '    sent = requests.post(f"{API}/sendMessage", params={"token": TOKEN}, json={"chat_id": m["chat_id"], "text": reply}).json()["result"]\n'
              '    print(f"→ {sent[\'chat_id\']}: {sent[\'text\']}")\nprint(f"Запросов погоды: {weather_calls}")',
              [''], files=WEATHER)


def build():
    return topic('Чат-боты: учебный мессенджер', 'обновления, команды, обработчики', [
        th_bot(), fl_bot(), code_bot(),
        th_cmds(), fl_cmds(), code_cmds(),
        project(),
    ], opt=True)
