import json
from dsl import *

# Тема 28 «Запросы к серверам». Ученик знает JSON, словари, исключения, классы.
# В приложении нет интернета: запросы обслуживает учебный модуль requests (v5/py/requests_shim.py) с виртуальными серверами.
# 127.0.0.1:5000 есть всегда; серверы задач описаны в служебном файле _itp_servers.json (ученику он не показывается).
# Три теории: клиент, сервер, HTTP и GET; параметры, заголовки и методы; ошибки сети. Проект — клиент сервера заметок.

D = 'http://127.0.0.1:5000'


def servers(**spec):
    return {'_itp_servers.json': json.dumps(spec, ensure_ascii=False)}


SHOP = servers(**{'shop.itp': {'routes': {'/products': {'json': [
    {'name': 'наушники', 'price': 2490, 'count': 4}, {'name': 'мышь', 'price': 890, 'count': 0},
    {'name': 'клавиатура', 'price': 3200, 'count': 2}, {'name': 'коврик', 'price': 450, 'count': 12},
    {'name': 'веб-камера', 'price': 4100, 'count': 1}, {'name': 'флешка', 'price': 690, 'count': 7}]}}}})
DICE = servers(**{'dice.itp': {'routes': {'/roll': {'seq': ['4', '2', '6', '6', '1', '3']}}}})
WEATHER = servers(**{'weather.itp': {'routes': {'/now': {'param': 'city', 'variants': {
    'Тюмень': {'temp': -3, 'wind': 5, 'sky': 'снег'}, 'Сочи': {'temp': 14, 'wind': 2, 'sky': 'ясно'},
    'Мурманск': {'temp': -11, 'wind': 9, 'sky': 'метель'}}}}}})
DIARY = servers(**{'diary.itp': {'routes': {}, 'token': 'ITP-2026'}})
CLUB = servers(**{'club.itp': {'collection': 'members', 'users': [{'id': 1, 'name': 'Аня'}, {'id': 2, 'name': 'Борис'}]}})
NEWS = servers(**{'news.itp': {'routes': {'/': {'text': 'Новости школы: завтра субботник'}, '/sport': {'text': 'Наши выиграли кубок!'},
                                          '/broken': {'status': 500, 'text': 'Internal Server Error'}}}})
FLAKY = servers(**{'flaky.itp': {'routes': {'/data': {'statuses': [503, 503, 200], 'text': 'Расписание: 8:30 алгебра'},
                                            '/down': {'statuses': [503], 'text': 'Service Unavailable'},
                                            '/ok': {'text': 'Всё работает'}}}})
NOTES = servers(**{'notes.itp': {'collection': 'notes', 'users': [
    {'id': 1, 'title': 'Покупки', 'text': 'молоко, хлеб'}, {'id': 2, 'title': 'ДЗ', 'text': 'алгебра №112'}]}})


def th_http():
    terms = [
        ('urllib', 'Стандартный модуль для работы с адресами; его часть urllib.parse разбирает и собирает URL.'),
        ('urlsplit','urllib.parse.urlsplit(адрес) — разбирает URL на части: scheme, netloc (хост и порт), path, query.'),
        ('content', 'r.content — тело ответа байтами (bytes), как пришло. r.text — то же, раскодированное в строку. Картинки и файлы берут через content.'),
        ('сервер', 'Программа, которая ждёт запросы по сети и отвечает на них. Клиент — тот, кто спрашивает: браузер, приложение, твоя программа.'),
        ('URL', 'Адрес ресурса: схема://хост:порт/путь?параметры. Например, http://127.0.0.1:5000/numbers — схема http, хост 127.0.0.1, '
                'порт 5000, путь /numbers.'),
        ('HTTP', 'Язык, на котором клиент и сервер договариваются. Запрос: метод (GET, POST…), адрес, заголовки и тело. '
                 'Ответ: код, заголовки и тело.'),
        ('код ответа', 'Число в ответе сервера: 2xx — успех (200 OK, 201 создано, 204 без содержимого), 4xx — ошибка клиента '
                       '(400 неверный запрос, 401 нужна авторизация, 404 не найдено), 5xx — ошибка сервера (500, 503).'),
        ('requests', 'Библиотека для HTTP-запросов: requests.get, post, put, delete. Ответ — объект с status_code, text, json().'),
        ('get', 'requests.get(адрес) — запрос GET: «дай данные». Возвращает ответ: r.status_code — код, r.text — тело строкой.'),
        ('json', 'У ответа: r.json() — тело ответа, разобранное из JSON в списки и словари Python.'),
    ]
    body = (
        '<p>Почти любое приложение общается с сервером: мессенджер отправляет сообщения, игра сохраняет рекорды, погода берёт прогноз. '
        'Твоя программа — <b>клиент</b>: она посылает запрос, [[сервер]] отвечает. Куда именно — задаёт адрес [[URL]].</p>'
        '<p>По дороге данные проходят несколько уровней, и каждый отвечает за своё:</p>'
        '<table><tr><th>Уровень</th><th>Пример</th><th>Отвечает за</th></tr>'
        '<tr><td>Прикладной</td><td>HTTP</td><td>что сказать: «дай список товаров»</td></tr>'
        '<tr><td>Транспортный</td><td>TCP</td><td>доставить всё целиком и по порядку</td></tr>'
        '<tr><td>Сетевой</td><td>IP</td><td>найти дорогу к нужному адресу</td></tr>'
        '<tr><td>Физический</td><td>провод, Wi-Fi</td><td>передать сигнал</td></tr></table>'
        '<p>Программисту обычно нужен только верхний уровень — [[HTTP]]: запрос с методом и адресом, ответ с кодом и телом.</p>'
        '<h3>Первый запрос</h3>'
        '<p>Запросы делает библиотека [[requests]]. В ИТП нет выхода в интернет, поэтому отвечают учебные серверы прямо внутри приложения; '
        'адрес <code>' + D + '</code> работает всегда. Код такой же, как с настоящими сайтами:</p>'
        + ex('import requests\n\nr = requests.get("' + D + '/")\nprint(r.status_code)\nprint(r.text)\nprint(r.headers["Content-Type"])') +
        '<p>[[get]] вернул ответ: [[код ответа]] 200 значит «всё хорошо», <code>r.text</code> — тело строкой. Заголовок Content-Type '
        'говорит, что внутри: обычный текст или JSON.</p>'
        '<h3>JSON в ответе</h3>'
        '<p>Данные серверы чаще всего отдают в JSON. Метод [[json]] у ответа сразу превращает тело в списки и словари:</p>'
        + ex('import requests\n\nnumbers = requests.get("' + D + '/numbers").json()\nprint(numbers, sum(numbers))\n'
             'city = requests.get("' + D + '/city").json()\nprint(city["name"], city["population"])\nr = requests.get("' + D + '/nothing")\nprint(r.status_code, r.text)') +
        '<p>Если пути нет, сервер отвечает кодом 404. Это не ошибка Python: программа не падает, просто нужно проверить код.</p>'
        + '<h3>Части адреса и тело ответа</h3>'
        '<p>Адрес состоит из частей, и разобрать его помогает [[urlsplit]] из стандартного модуля urllib.parse. А у ответа, '
        'кроме <code>text</code>, есть [[content]] — те же данные байтами: так приходят картинки и файлы.</p>'
        + ex('from urllib.parse import urlsplit\nimport requests\n\nparts = urlsplit("http://127.0.0.1:5000/numbers?sort=asc")\nprint(parts.scheme, parts.netloc, parts.path, parts.query)\n'
             'r = requests.get("http://127.0.0.1:5000/")\nprint(len(r.text), len(r.content), r.content[:6])')
    )
    return th('Клиент, сервер и HTTP', terms, body)


def fl_http():
    return fl('Клиент, сервер и HTTP', [
        qo('Что выведет программа?', 'import requests\nr = requests.get("' + D + '/numbers")\nprint(r.status_code, sum(r.json()))',
           ['200 31415', 'OK 14', '404 0'], 'Путь есть — код 200; числа 3, 1, 4, 1, 5 в сумме дают 14.'),
        q('Сервер ответил кодом 404. Что это значит?', 'Такого адреса на сервере нет', ['Сервер сломался', 'Нет интернета'],
          '4xx — ошибка в запросе клиента; 404 — «не найдено». Поломка сервера — 5xx.'),
        q('Какой уровень сети отвечает за то, чтобы данные дошли целиком и по порядку?', 'Транспортный (TCP)',
          ['Прикладной (HTTP)', 'Сетевой (IP)'], 'IP ищет дорогу, TCP следит за целостностью и порядком.'),
    ])


def code_http():
    return ts('Клиент, сервер и HTTP', [
        task('Интернет-магазин отдаёт список товаров по адресу http://shop.itp/products — JSON-список словарей с ключами name, price и '
             'count (сколько на складе). На вход подаётся наибольшая цена. Выведи товары в наличии (count больше нуля) с ценой не выше '
             'заданной, по возрастанию цены (цены у товаров разные), строками «название — цена ₽», затем «Найдено: N». Если ничего не подошло — только «Найдено: 0».',
             'products = requests.get("http://shop.itp/products").json()\nФильтр — списочное выражение с двумя условиями, сортировка — '
             'sorted(..., key=lambda p: p["price"]).',
             'import requests\n\nlimit = int(input())\nproducts = requests.get("http://shop.itp/products").json()\n'
             'found = sorted([p for p in products if p["count"] > 0 and p["price"] <= limit], key=lambda p: p["price"])\nfor p in found:\n'
             '    print(f"{p[\'name\']} — {p[\'price\']} ₽")\nprint(f"Найдено: {len(found)}")',
             ['3000', '100000', '400'], files=SHOP),
        task('Сервер кубика: каждый GET-запрос к http://dice.itp/roll возвращает текстом следующий бросок. На вход подаётся n ≥ 1 — сколько раз '
             'бросить. Выведи броски через пробел, затем «Сумма: S» и «Шестёрок: K».',
             'В цикле n раз: int(requests.get(...).text). Броски собери в список.',
             'import requests\n\nn = int(input())\nrolls = [int(requests.get("http://dice.itp/roll").text) for _ in range(n)]\nprint(" ".join(map(str, rolls)))\n'
             'print(f"Сумма: {sum(rolls)}")\nprint(f"Шестёрок: {rolls.count(6)}")',
             ['3', '6', '8'], files=DICE),
        task('Таблица лидеров арены: GET http://arena.itp/top возвращает JSON-список словарей с ключами nick и score. '
             'На вход подаётся n. Выведи n лучших по убыванию очков (при равенстве — по нику) строками «N. НИК — ОЧКИ», '
             'очки с разделителем разрядов, а затем «Всего игроков: K».',
             'top = requests.get(...).json(); sorted(top, key=lambda p: (-p["score"], p["nick"]))[:n]; формат :, для очков.',
             'import requests\n\nn = int(input())\ntop = requests.get("http://arena.itp/top").json()\n'
             'for i, p in enumerate(sorted(top, key=lambda p: (-p["score"], p["nick"]))[:n], 1):\n    print(f"{i}. {p[\'nick\']} — {p[\'score\']:,}")\n'
             'print(f"Всего игроков: {len(top)}")',
             ['3', '1', '10'],
             files=servers(**{'arena.itp': {'routes': {'/top': {'json': [
                 {'nick': 'Кира', 'score': 15200}, {'nick': 'Zed', 'score': 99000}, {'nick': 'Ли', 'score': 15200},
                 {'nick': 'neo', 'score': 870}, {'nick': 'Тень', 'score': 120500}]}}}})),
    ])


def th_methods():
    terms = [
        ('параметры запроса', 'Часть адреса после ?: ключ=значение через &, например ?city=Омск&days=3. В requests их передают словарём '
                              'params — он сам соберёт и закодирует строку.'),
        ('заголовок', 'Дополнительные сведения в запросе или ответе: тип данных, язык, токен доступа. В requests — словарь headers: '
                      'headers={"Authorization": "OAuth токен"}.'),
        ('os', 'Модуль для связи с операционной системой; в нём os.environ — переменные окружения.'),
        ('os.environ', 'Словарь переменных окружения — настроек, заданных снаружи программы. os.environ.get("ИМЯ", "запасное") — '
                       'значение или запасное, если переменной нет.'),
        ('post', 'requests.post(адрес, json=данные) — запрос POST: «создай». Сервер обычно отвечает кодом 201 и созданной записью.'),
        ('put', 'requests.put(адрес, json=данные) — запрос PUT: «замени или обнови запись по этому адресу».'),
        ('delete', 'requests.delete(адрес) — запрос DELETE: «удали». Успешный ответ часто с кодом 204 и пустым телом.'),
    ]
    body = (
        '<p>Чтобы уточнить, что именно нужно, к адресу добавляют [[параметры запроса]]. Руками собирать строку '
        '<code>?city=Омск&amp;days=3</code> не нужно: передай словарь <code>params</code>. Учебный адрес <code>/echo</code> возвращает то, '
        'что получил, — видно, что ушло на сервер:</p>'
        + ex('import requests\n\nr = requests.get("' + D + '/echo", params={"city": "Омск", "days": 3})\nprint(r.url)\nprint(r.json()["args"])') +
        '<p>Русские буквы в адресе закодированы — так требует стандарт, requests делает это сам.</p>'
        '<h3>Заголовки и доступ</h3>'
        '<p>Многие данные доступны только своим. Клиент доказывает право доступа токеном — секретной строкой, которую передают в '
        '[[заголовок]] Authorization. Без него сервер отвечает 401:</p>'
        + ex('import requests\n\nurl = "' + D + '/secret"\nprint(requests.get(url).status_code)\nr = requests.get(url, headers={"Authorization": "OAuth demo-token"})\n'
             'print(r.status_code, r.json()["message"])') +
        '<p>Настоящие токены — как пароли: их не публикуют и не вставляют в код, который увидят другие. Их кладут в переменную окружения — '
        'настройку, заданную снаружи программы (в терминале: <code>set ITP_TOKEN=…</code> в Windows, <code>export ITP_TOKEN=…</code> в macOS и Linux), — '
        'и читают через [[os.environ]]. В ИТП переменных нет, поэтому срабатывает запасное значение:</p>'
        + ex('import os\nimport requests\n\ntoken = os.environ.get("ITP_TOKEN", "demo-token")\n'
             'r = requests.get("http://127.0.0.1:5000/secret", headers={"Authorization": "OAuth " + token})\nprint(r.status_code)') +
        '<h3>Методы: создать, изменить, удалить</h3>'
        '<p>GET только читает. Чтобы менять данные, есть другие методы: [[post]] — создать, [[put]] — изменить, [[delete]] — удалить. '
        'Данные для сервера передают параметром <code>json</code>. На учебном сервере есть список пользователей:</p>'
        + ex('import requests\n\nusers = "' + D + '/users"\nprint([u["username"] for u in requests.get(users).json()])\n'
             'r = requests.post(users, json={"username": "zed", "first_name": "Зед"})\nprint(r.status_code, r.json()["id"])\n'
             'r = requests.put(users + "/1", json={"first_name": "Лиза"})\nprint(r.status_code, r.json()["first_name"])\n'
             'r = requests.delete(users + "/2")\nprint(r.status_code, repr(r.text))\nprint([u["username"] for u in requests.get(users).json()])') +
        '<p>Адрес <code>/users/1</code> — конкретная запись, <code>/users</code> — весь список. Так устроено большинство серверов: '
        'одни и те же адреса, а действие задаёт метод.</p>'
    )
    return th('Параметры, заголовки и методы', terms, body)


def fl_methods():
    return fl('Параметры, заголовки и методы', [
        qo('Что выведет программа?', 'import requests\nr = requests.post("' + D + '/users", json={"username": "new"})\nprint(r.status_code, r.json()["id"])',
           ['200 1', '201 1', '204 3'], 'Создание — код 201; в списке уже две записи, новая получает id 3.'),
        q('Какой запрос нужен, чтобы удалить заметку с id 5?', 'requests.delete(адрес + "/notes/5")',
          ['requests.get(адрес + "/notes/5/delete")', 'requests.post(адрес + "/notes", json={"id": -5})'], 'Действие задаёт метод, адрес — запись.'),
        q('Сервер ответил 401. Что, скорее всего, не так?', 'Нет токена доступа или он неверный', ['Неверный путь', 'Сервер перегружен'],
          '401 — «не авторизован»; неверный путь дал бы 404, перегрузка — 503.'),
    ])


def code_methods():
    return ts('Параметры, заголовки и методы', [
        task('Погода. Сервер отдаёт текущую погоду по адресу http://weather.itp/now с параметром city: JSON со словарём temp (градусы), '
             'wind (м/с) и sky (описание). На вход подаётся город. Выведи «Город: T°, ветер W м/с, небо», а если сервер ответил 404 — '
             '«Город не найден». Положительную температуру выводи со знаком плюс.',
             'r = requests.get("http://weather.itp/now", params={"city": city}); проверь r.status_code == 404.\n'
             'Знак у положительных: sign = "+" if t > 0 else "", затем f"{city}: {sign}{t}°, …".',
             'import requests\n\ncity = input()\nr = requests.get("http://weather.itp/now", params={"city": city})\nif r.status_code == 404:\n    print("Город не найден")\nelse:\n'
             '    w = r.json()\n    t = w["temp"]\n    sign = "+" if t > 0 else ""\n    print(f"{city}: {sign}{t}°, ветер {w[\'wind\']} м/с, {w[\'sky\']}")',
             ['Тюмень', 'Сочи', 'Москва', 'Мурманск'], files=WEATHER),
        task('Личный дневник. Записи лежат на http://diary.itp/secret и доступны только с токеном. На вход подаётся токен. Сделай запрос '
             'с заголовком Authorization: «OAuth ТОКЕН». Если код 200 — выведи «Доступ открыт: СООБЩЕНИЕ», где сообщение — значение '
             'message из ответа; иначе — «Нет доступа (КОД)».',
             'headers={"Authorization": f"OAuth {token}"}; дальше по r.status_code.',
             'import requests\n\ntoken = input()\nr = requests.get("http://diary.itp/secret", headers={"Authorization": f"OAuth {token}"})\nif r.status_code == 200:\n'
             '    print(f"Доступ открыт: {r.json()[\'message\']}")\nelse:\n    print(f"Нет доступа ({r.status_code})")',
             ['ITP-2026', 'qwerty', 'itp-2026'], files=DIARY),
        task('Клуб. Список участников — на http://club.itp/members: GET отдаёт список словарей с id и name, POST с json={"name": ИМЯ} '
             'добавляет участника и возвращает его запись с новым id, DELETE на http://club.itp/members/ID удаляет (код 204) или отвечает 404. '
             'На вход подаются команды, последняя — «стоп»: «добавить ИМЯ» → «Добавлен #ID»; «список» → строки «ID. ИМЯ» или «Пусто»; '
             '«удалить ID» → «Удалён #ID» или «Нет участника #ID».',
             'Адрес списка — base = "http://club.itp/members", записи — f"{base}/{id}".\nКоманду разбирай: cmd, arg = s.split(" ", 1) — '
             'второй аргумент split: разрезать не больше одного раза, поэтому имя из нескольких слов останется целым. '
             '«Список» без аргумента проверяй заранее: s == "список".',
             'import requests\n\nbase = "http://club.itp/members"\nwhile True:\n    s = input()\n    if s == "стоп":\n        break\n    if s == "список":\n'
             '        members = requests.get(base).json()\n        if not members:\n            print("Пусто")\n        for m in members:\n            print(f"{m[\'id\']}. {m[\'name\']}")\n'
             '        continue\n    cmd, arg = s.split(" ", 1)\n    if cmd == "добавить":\n        m = requests.post(base, json={"name": arg}).json()\n        print(f"Добавлен #{m[\'id\']}")\n'
             '    elif cmd == "удалить":\n        r = requests.delete(f"{base}/{arg}")\n        print(f"Удалён #{arg}" if r.status_code == 204 else f"Нет участника #{arg}")',
             ['список\nдобавить Вика\nудалить 1\nсписок\nстоп', 'удалить 7\nудалить 2\nудалить 1\nсписок\nдобавить Глеб\nсписок\nстоп'], files=CLUB),
        task('Вики рецептов: GET http://craft.itp/recipe с параметром item возвращает JSON-словарь «материал → количество» '
             'для этого предмета. На вход подаются предмет и сколько штук сделать. Выведи материалы по алфавиту строками '
             '«МАТЕРИАЛ: N» — на все штуки сразу. Если рецепта нет (код ответа 404), выведи «Рецепт не найден».',
             'r = requests.get(url, params={"item": item}); проверь r.status_code == 404, иначе r.json() и умножение на количество.',
             'import requests\n\nitem = input()\nn = int(input())\nr = requests.get("http://craft.itp/recipe", params={"item": item})\n'
             'if r.status_code == 404:\n    print("Рецепт не найден")\nelse:\n    need = r.json()\n    for m in sorted(need):\n        print(f"{m}: {need[m] * n}")',
             ['факел\n4', 'кирка\n1', 'бластер\n2'],
             files=servers(**{'craft.itp': {'routes': {'/recipe': {'param': 'item', 'variants': {
                 'факел': {'палка': 1, 'уголь': 1}, 'кирка': {'палка': 2, 'камень': 3}}}}}})),
    ])


def th_errors():
    terms = [
        ('ConnectionError', 'requests.ConnectionError — связи с сервером нет: неверный адрес, сервер выключен, нет интернета. '
                            'Ответа нет совсем, поэтому нет и кода.'),
        ('raise_for_status', 'r.raise_for_status() — ничего не делает при успешном коде и вызывает HTTPError, если код 4xx или 5xx.'),
        ('HTTPError', 'requests.HTTPError — ошибка, которую вызывает raise_for_status при коде ответа 4xx или 5xx.'),
    ]
    body = (
        '<p>Сеть ненадёжна: сервер может не ответить вовсе, а может ответить ошибкой. Это два разных случая.</p>'
        '<p>Если до сервера не достучаться — неверный адрес, сервер выключен, нет интернета — ответа нет совсем, и requests вызывает '
        '[[ConnectionError]]. Её ловят, как любую ошибку:</p>'
        + ex('import requests\n\ntry:\n    requests.get("http://nowhere.itp/")\nexcept requests.ConnectionError:\n    print("Нет связи с сервером")') +
        '<p>А если сервер ответил кодом 404 или 500, программа не падает: ответ есть, просто плохой. Проверить его можно через '
        '<code>r.ok</code> (True для кодов меньше 400) или [[raise_for_status]], который при плохом коде вызывает [[HTTPError]]. '
        'Это удобно, когда проверок много: одна строка вместо if на каждый код.</p>'
        + ex('import requests\n\nr = requests.get("' + D + '/missing")\nprint(r.ok, r.status_code)\ntry:\n    r.raise_for_status()\nexcept requests.HTTPError as e:\n    print("Ошибка:", e)') +
        '<h3>Повторить попытку</h3>'
        '<p>Код 503 значит «сервер перегружен, попробуй позже». Такие запросы повторяют несколько раз, а не сдаются сразу. '
        'Настоящие программы ещё ставят <code>timeout=5</code>, чтобы не ждать ответа вечно, и делают паузу между попытками.</p>'
        + ex('import requests\n\nfor attempt in range(1, 4):\n    try:\n        r = requests.get("' + D + '/count")\n        r.raise_for_status()\n'
             '        print("Попытка", attempt, "— ответ", r.text)\n        break\n    except (requests.ConnectionError, requests.HTTPError) as e:\n'
             '        print("Попытка", attempt, "не удалась:", e)\nelse:\n    print("Сервер недоступен")') +
        '<p>Здесь первая же попытка удалась. <code>else</code> у цикла сработал бы, только если все три попытки закончились без '
        '<code>break</code>.</p>'
    )
    return th('Ошибки сети', terms, body)


def fl_errors():
    return fl('Ошибки сети', [
        q('Чем ConnectionError отличается от ответа с кодом 404?', 'При ConnectionError ответа нет совсем, а 404 — ответ сервера',
          ['Ничем, это одно и то же', '404 вызывает исключение, а ConnectionError — нет'], 'Нет связи — нет и кода ответа.'),
        qo('Что выведет программа?', 'import requests\nr = requests.get("' + D + '/abc")\nprint(r.ok)', ['True', 'Ошибка', '404'],
           'Сервер ответил 404 — ok равно False, исключения нет.'),
        q('Что сделает r.raise_for_status() при коде 200?', 'Ничего', ['Вызовет HTTPError', 'Вернёт True'],
          'Исключение — только для кодов 4xx и 5xx.'),
    ])


def code_errors():
    return ts('Ошибки сети', [
        task('Проверка ссылок. На вход подаются адреса, по одному в строке, последняя строка — «стоп». Для каждого выведи «АДРЕС: ok, N символов», '
             'где N — длина текста ответа (r.text), если сервер ответил успешно, «АДРЕС: код C», если ответил ошибкой, и «АДРЕС: нет связи», если связаться не удалось.',
             'try: r = requests.get(url) except requests.ConnectionError: нет связи. Дальше r.ok и len(r.text).',
             'import requests\n\nwhile True:\n    url = input()\n    if url == "стоп":\n        break\n    try:\n        r = requests.get(url)\n    except requests.ConnectionError:\n'
             '        print(f"{url}: нет связи")\n        continue\n    print(f"{url}: ok, {len(r.text)} символов" if r.ok else f"{url}: код {r.status_code}")',
             ['http://news.itp/\nhttp://news.itp/sport\nhttp://news.itp/broken\nhttp://news.itp/old\nhttp://olds.itp/\nстоп', 'http://127.0.0.1:5000/\nстоп'],
             files=NEWS),
        task('Капризный сервер. На вход подаётся путь на сервере http://flaky.itp, например «/data». Сделай до трёх попыток: на каждой выведи '
             '«Попытка K: код C». Как только код 200 — выведи «Данные: ТЕКСТ» и остановись. Если после трёх попыток успеха нет — '
             '«Сервер недоступен».',
             'for attempt in range(1, 4): r = requests.get("http://flaky.itp" + path); вывести код; if r.ok: ... break\nПосле цикла — '
             'else у for сработает, только если не было break.',
             'import requests\n\npath = input()\nfor attempt in range(1, 4):\n    r = requests.get("http://flaky.itp" + path)\n    print(f"Попытка {attempt}: код {r.status_code}")\n'
             '    if r.ok:\n        print(f"Данные: {r.text}")\n        break\nelse:\n    print("Сервер недоступен")',
             ['/data', '/down', '/ok', '/nope'], files=FLAKY),
        task('Мониторинг серверов. На вход подаются адреса до слова «стоп». Для каждого выведи «АДРЕС — OK», если ответ '
             'успешный, «АДРЕС — код N», если сервер ответил ошибкой, и «АДРЕС — нет связи», если сервера нет. '
             'В конце — «Работают: K из M».',
             'try: r = requests.get(url) / except requests.ConnectionError. Успех — r.ok, иначе r.status_code.',
             'import requests\n\nok = 0\ntotal = 0\nwhile True:\n    url = input()\n    if url == "стоп":\n        break\n    total += 1\n    try:\n'
             '        r = requests.get(url)\n    except requests.ConnectionError:\n        print(f"{url} — нет связи")\n        continue\n    if r.ok:\n'
             '        print(f"{url} — OK")\n        ok += 1\n    else:\n        print(f"{url} — код {r.status_code}")\nprint(f"Работают: {ok} из {total}")',
             ['http://game.itp/\nhttp://game.itp/admin\nhttp://dead.itp/\nстоп', 'http://game.itp/\nстоп', 'http://dead.itp/x\nстоп'],
             files=servers(**{'game.itp': {'routes': {'/': {'text': 'онлайн'}}}})),
    ])


def project():
    return pj('Клиент сервера заметок',
              'Сервер заметок работает по адресу http://notes.itp/notes. GET на список отдаёт заметки — словари с id, title и text; GET, PUT и '
              'DELETE на http://notes.itp/notes/ID работают с одной заметкой (PUT с json={"text": …} меняет текст и возвращает заметку, '
              'DELETE отвечает 204); POST на список с json={"title": …, "text": …} создаёт заметку и возвращает её с новым id. '
              'Нет такой заметки — код 404.\n'
              'Напиши клиент. На вход подаются команды, последняя — «выход»:\n'
              '— «список» → строки «ID. ЗАГОЛОВОК» или «Заметок нет»;\n'
              '— «показать ID» → «ЗАГОЛОВОК: ТЕКСТ»;\n'
              '— «новая ЗАГОЛОВОК | ТЕКСТ» → «Создана заметка ID»;\n'
              '— «изменить ID | ТЕКСТ» → «Заметка ID изменена»;\n'
              '— «удалить ID» → «Заметка ID удалена».\n'
              'Если заметки с таким ID нет — «Нет заметки ID». После «выход» выведи «Всего заметок: N».',
              'base = "http://notes.itp/notes", адрес заметки — f"{base}/{id}"\nparts = s.split(" ", 1) — второй аргумент split: разрезать не больше одного раза; команда — parts[0], остальное — parts[1], если есть\n'
              'title, text = rest.split(" | ") — для «новая» и «изменить»\nr.status_code == 404 — заметки нет',
              'import requests\n\nbase = "http://notes.itp/notes"\nwhile True:\n    s = input()\n    if s == "выход":\n        break\n    parts = s.split(" ", 1)\n    cmd = parts[0]\n    rest = parts[1] if len(parts) > 1 else ""\n'
              '    if cmd == "список":\n        notes = requests.get(base).json()\n        if not notes:\n            print("Заметок нет")\n        for n in notes:\n'
              '            print(f"{n[\'id\']}. {n[\'title\']}")\n    elif cmd == "новая":\n        title, text = rest.split(" | ")\n'
              '        note = requests.post(base, json={"title": title, "text": text}).json()\n        print(f"Создана заметка {note[\'id\']}")\n    else:\n'
              '        if cmd == "изменить":\n            nid, text = rest.split(" | ")\n            r = requests.put(f"{base}/{nid}", json={"text": text})\n'
              '            done = f"Заметка {nid} изменена"\n        elif cmd == "удалить":\n            nid = rest\n            r = requests.delete(f"{base}/{nid}")\n'
              '            done = f"Заметка {nid} удалена"\n        else:\n            nid = rest\n            r = requests.get(f"{base}/{nid}")\n'
              '            done = f"{r.json()[\'title\']}: {r.json()[\'text\']}" if r.ok else ""\n        print(f"Нет заметки {nid}" if r.status_code == 404 else done)\n'
              'print(f"Всего заметок: {len(requests.get(base).json())}")',
              ['список\nпоказать 2\nновая Кино | в субботу в 18:00\nизменить 1 | молоко, хлеб, сыр\nпоказать 1\nудалить 2\nсписок\nвыход',
               'показать 9\nудалить 9\nизменить 9 | ?\nудалить 1\nудалить 2\nсписок\nвыход', 'выход'],
              files=NOTES)


def build():
    return topic('Запросы к серверам', 'HTTP, requests, get, post, JSON', [
        th_http(), fl_http(), code_http(),
        th_methods(), fl_methods(), code_methods(),
        th_errors(), fl_errors(), code_errors(),
        project(),
    ])
