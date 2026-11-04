import json
from dsl import *

# Нора после «Запросы к серверам»: работа с API. Две теории: API и ключи (ключ в параметре, хранение в переменной окружения через
# os.environ.get с запасным значением); вложенный JSON, отсутствующие поля, лимит запросов и кэш. Мини-проект — консольная погода.
# Учебные серверы описаны в служебном _itp_servers.json; ключ учебных API — «demo».

FORECAST = {
    'Тюмень': {'city': 'Тюмень', 'days': [{'date': '28.10', 't_min': -6, 't_max': -1, 'sky': 'снег'},
                                          {'date': '29.10', 't_min': -8, 't_max': -3, 'sky': 'ясно'},
                                          {'date': '30.10', 't_min': -4, 't_max': 1, 'sky': 'облачно'}]},
    'Сочи': {'city': 'Сочи', 'days': [{'date': '28.10', 't_min': 11, 't_max': 17, 'sky': 'ясно'},
                                      {'date': '29.10', 't_min': 12, 't_max': 19, 'sky': 'дождь', 'wind': 9}]},
    'Норильск': {'city': 'Норильск', 'days': [{'date': '28.10', 't_min': -21, 't_max': -15, 'sky': 'метель', 'wind': 14}], 'alert': 'штормовое предупреждение'},
}
SERVERS = {'_itp_servers.json': json.dumps({
    'api.weather.itp': {'routes': {'/forecast': {'param': 'city', 'variants': FORECAST, 'key': 'demo'}}},
    'api.rates.itp': {'routes': {'/latest': {'key': 'demo', 'json': {'base': 'RUB', 'date': '28.10.2026',
                                                                    'rates': {'USD': 90.5, 'EUR': 98.25, 'CNY': 12.4, 'TRY': 2.65}}}}},
    'api.facts.itp': {'routes': {'/facts': {'param': 'topic', 'key': 'demo', 'variants': {
        'космос': {'topic': 'космос', 'items': [{'text': 'На Венере сутки длиннее года.', 'tags': ['планеты', 'время']},
                                                {'text': 'Свет от Солнца идёт до Земли около 8 минут.', 'tags': ['свет', 'время']},
                                                {'text': 'У Сатурна больше 140 спутников.', 'tags': ['планеты']}]},
        'животные': {'topic': 'животные', 'items': [{'text': 'Осьминог имеет три сердца.', 'tags': ['море']},
                                                    {'text': 'Коалы спят до 20 часов в сутки.', 'tags': ['сон', 'сутки']}]}}}}},
    'api.quota.itp': {'routes': {'/ping': {'key': 'demo', 'statuses': [200, 200, 200, 429], 'text': 'pong'}}},
}, ensure_ascii=False)}


def th_key():
    terms = [
        ('API', 'Программный интерфейс: договор, какие адреса есть у сервиса, какие параметры они принимают и в каком виде отвечают. '
                'Описание API — его документация.'),
        ('ключ API', 'Строка, по которой сервис узнаёт, кто к нему обращается, и считает его запросы. Передаётся в параметре или заголовке. '
                     'Это секрет: в код и в чужие руки его не кладут.'),
        ('os', 'Модуль для связи с операционной системой: переменные окружения, папки, процессы.'),
        ('os.environ', 'Словарь переменных окружения — настроек, которые задаются снаружи программы. os.environ.get("ИМЯ", "запасное") — '
                       'значение или запасное, если переменной нет.'),
    ]
    body = (
        '<p>Погода в приложении, курс валют в банке, карта в такси — всё это данные чужих сервисов. Сервис описывает, как к нему обращаться: '
        'адреса, параметры и формат ответа. Такой договор — [[API]]. Многие API бесплатны, но требуют [[ключ API]]: так сервис знает, '
        'кто спрашивает, и не даёт одному пользователю завалить его запросами. Неверный ключ — ответ 401.</p>'
        + ex('import requests\n\nurl = "http://api.rates.itp/latest"\nprint(requests.get(url, params={"key": "qwerty"}).status_code)\n'
             'data = requests.get(url, params={"key": "demo"}).json()\nprint(data["base"], data["date"], data["rates"]["USD"])', files=SERVERS) +
        '<h3>Ключ не пишут в коде</h3>'
        '<p>Код выкладывают на GitHub, отправляют друзьям, показывают учителю — и ключ уходит вместе с ним. Поэтому ключ хранят '
        'в переменной окружения — настройке, заданной снаружи программы, — и читают через [[os.environ]]. На компьютере её задают '
        'в терминале (<code>set WEATHER_KEY=…</code> в Windows, <code>export WEATHER_KEY=…</code> в macOS и Linux). В ИТП переменных '
        'нет, поэтому берём запасное значение — учебный ключ «demo»:</p>'
        + ex('import os\n\nkey = os.environ.get("WEATHER_KEY", "demo")\nprint("ключ получен" if key else "ключа нет", len(key))') +
        '<p>Если ключ всё-таки попал в открытый код, его сразу отзывают в личном кабинете сервиса и выпускают новый.</p>'
    )
    return th('API и ключи', terms, body)


def fl_key():
    return fl('API и ключи', [
        q('Почему ключ API не пишут прямо в коде?', 'Код увидят другие и смогут пользоваться ключом',
          ['Иначе программа работает медленнее', 'Python не разрешает строки длиннее 30 символов'], 'Ключ — секрет, как пароль.'),
        q('Что вернёт os.environ.get("KEY", "demo"), если переменной KEY нет?', '"demo"', ['None', 'Ошибку KeyError'], 'Второй аргумент — запасное значение.'),
        q('Сервис ответил кодом 401. Что проверить первым?', 'Ключ API', ['Интернет-соединение', 'Версию Python'], '401 — «не авторизован».'),
    ])


def code_key():
    return ts('API и ключи', [
        task('Прогноз. Сервис http://api.weather.itp/forecast принимает параметры city и key (ключ возьми из переменной окружения WEATHER_KEY, '
             'запасное значение — demo) и отвечает JSON: city и список days, в котором у каждого дня date, t_min, t_max и sky. На вход подаётся '
             'город. Выведи «ГОРОД, прогноз на N дн.», затем по дню «ДАТА: от MIN до MAX, НЕБО». Если города нет (код 404) — «Нет такого города».',
             'key = os.environ.get("WEATHER_KEY", "demo"); r = requests.get(url, params={"city": city, "key": key}).\nДни — r.json()["days"], у каждого — словарь.',
             'import os\nimport requests\n\nkey = os.environ.get("WEATHER_KEY", "demo")\ncity = input()\nr = requests.get("http://api.weather.itp/forecast", params={"city": city, "key": key})\n'
             'if r.status_code == 404:\n    print("Нет такого города")\nelse:\n    data = r.json()\n    print(f"{data[\'city\']}, прогноз на {len(data[\'days\'])} дн.")\n'
             '    for d in data["days"]:\n        print(f"{d[\'date\']}: от {d[\'t_min\']} до {d[\'t_max\']}, {d[\'sky\']}")',
             ['Тюмень', 'Сочи', 'Москва'], files=SERVERS),
        task('Обменник. Сервис http://api.rates.itp/latest с параметром key отвечает JSON: base (базовая валюта, RUB), date и словарь rates — '
             'сколько рублей стоит одна единица валюты. На вход подаётся первой строкой ключ, второй — «СУММА ИЗ В», например «100 USD EUR» '
             '(валюты из rates или RUB). Выведи «СУММА ИЗ = РЕЗУЛЬТАТ В (курс на ДАТА)»: сумма — как введена, результат — round(…, 2) (например, 9050.0). При неверном '
             'ключе — «Неверный ключ», при незнакомой валюте — «Нет курса для ВАЛЮТА» (если незнакомы обе — про первую).',
             'Рубли сам добавь в курсы: rates["RUB"] = 1. Перевод через рубли: amount * rates[a] / rates[b].',
             'import requests\n\nkey = input()\namount, a, b = input().split()\nr = requests.get("http://api.rates.itp/latest", params={"key": key})\nif r.status_code == 401:\n'
             '    print("Неверный ключ")\nelse:\n    data = r.json()\n    rates = data["rates"]\n    rates["RUB"] = 1\n    bad = [c for c in (a, b) if c not in rates]\n'
             '    if bad:\n        print(f"Нет курса для {bad[0]}")\n    else:\n        result = round(float(amount) * rates[a] / rates[b], 2)\n'
             '        print(f"{amount} {a} = {result} {b} (курс на {data[\'date\']})")',
             ['demo\n100 USD EUR', 'demo\n5000 RUB CNY', 'abc\n1 USD RUB', 'demo\n10 GBP RUB'], files=SERVERS),
    ])


def th_nested():
    terms = [
        ('вложенный JSON', 'Ответ, в котором словари лежат в списках, а списки — в словарях. Путь к значению записывают цепочкой: '
                           'data["days"][0]["sky"].'),
        ('лимит запросов', 'Сколько запросов сервис разрешает за единицу времени. Превысил — ответ 429 Too Many Requests: нужно подождать.'),
        ('кэш', 'Запомненные ответы: если те же данные уже получали, берут их из памяти, а не спрашивают сервер снова.'),
    ]
    body = (
        '<p>Ответы API редко бывают плоскими: в словаре — список дней, в каждом дне — словарь. Это [[вложенный JSON]]. Значение достают '
        'цепочкой ключей и номеров, а необязательные поля — через <code>get</code> с запасным значением, чтобы не упасть с KeyError:</p>'
        + ex('import requests\n\ndata = requests.get("http://api.weather.itp/forecast", params={"city": "Сочи", "key": "demo"}).json()\n'
             'print(data["days"][1]["sky"], data["days"][-1]["t_max"])\nfor d in data["days"]:\n    print(d["date"], "ветер", d.get("wind", "нет данных"))\n'
             'print(data.get("alert", "без предупреждений"))', files=SERVERS) +
        '<h3>Лимиты и кэш</h3>'
        '<p>У бесплатных API почти всегда есть [[лимит запросов]]: например, 1000 в день или 3 в секунду. Превысишь — ответ 429. Поэтому '
        'лишних запросов не делают: если город уже спрашивали, ответ берут из [[кэш]]а — обычного словаря:</p>'
        + ex('import requests\n\ncache = {}\n\n\ndef ping(n):\n    if n in cache:\n        return cache[n] + " (из кэша)"\n'
             '    r = requests.get("http://api.quota.itp/ping", params={"key": "demo"})\n    if r.status_code == 429:\n        return "429: лимит, подожди"\n'
             '    cache[n] = r.text\n    return r.text\n\n\nfor n in [1, 2, 1, 3, 4, 2]:\n    print(n, ping(n))', files=SERVERS) +
        '<p>Учебный сервер разрешает три запроса: четвёртый получил 429, а повторные вопросы обслужил кэш и лимит не потратили.</p>'
    )
    return th('Вложенный JSON и лимиты', terms, body)


def fl_nested():
    return fl('Вложенный JSON и лимиты', [
        qo('Что выведет программа?', 'data = {"days": [{"t": 3}, {"t": -2}], "city": "Омск"}\nprint(data["days"][1]["t"], data.get("alert", "нет"))',
           ['3 нет', '-2 None', 'Ошибка'], 'Второй день — t = -2; ключа alert нет, get вернул запасное «нет».'),
        q('Что означает код 429?', 'Слишком много запросов — нужно подождать', ['Нет такой страницы', 'Сервер сломался'], '429 Too Many Requests.'),
        q('Зачем API-клиенту кэш?', 'Не тратить лимит и время на повторные одинаковые запросы', ['Чтобы хранить ключ', 'Чтобы ускорить сам сервер'],
          'Ответ на тот же вопрос берётся из памяти.'),
    ])


def code_nested():
    return ts('Вложенный JSON и лимиты', [
        task('Факты. Сервис http://api.facts.itp/facts с параметрами topic и key=demo отвечает JSON: topic и список items, у каждого — text и список '
             'tags (у каждого факта хотя бы один тег). На вход подаётся тема. Выведи все факты пронумерованными строками «N. ТЕКСТ [теги через запятую]», затем «Теги: …» — все разные '
             'теги по убыванию частоты (при равенстве — по алфавиту) в виде «тег×K» через пробел. Нет темы (404) — «Нет такой темы».',
             'Теги: Counter(tag for item in items for tag in item["tags"]); сортировка пар key=lambda p: (-p[1], p[0]).',
             'from collections import Counter\nimport requests\n\nr = requests.get("http://api.facts.itp/facts", params={"topic": input(), "key": "demo"})\nif r.status_code == 404:\n'
             '    print("Нет такой темы")\nelse:\n    items = r.json()["items"]\n    for i, item in enumerate(items, 1):\n        print(f"{i}. {item[\'text\']} [{\', \'.join(item[\'tags\'])}]")\n'
             '    tags = Counter(tag for item in items for tag in item["tags"])\n    print("Теги:", " ".join(f"{t}×{k}" for t, k in sorted(tags.items(), key=lambda p: (-p[1], p[0]))))',
             ['космос', 'животные', 'история'], files=SERVERS),
        task('Счётчик лимита. На вход подаются номера запросов через пробел. Для каждого номера: если такой уже был — выведи «N: из кэша», иначе '
             'сделай GET http://api.quota.itp/ping с key=demo и выведи «N: КОД». Как только сервер ответит 429 — выведи «Лимит исчерпан» и больше '
             'запросов не делай (оставшиеся номера не обрабатывай). В конце — «Запросов к серверу: K».',
             'Кэш — множество уже спрошенных номеров. После 429 — break.',
             'import requests\n\nseen = set()\nsent = 0\nfor n in input().split():\n    if n in seen:\n        print(f"{n}: из кэша")\n        continue\n'
             '    r = requests.get("http://api.quota.itp/ping", params={"key": "demo"})\n    sent += 1\n    print(f"{n}: {r.status_code}")\n    if r.status_code == 429:\n'
             '        print("Лимит исчерпан")\n        break\n    seen.add(n)\nprint(f"Запросов к серверу: {sent}")',
             ['1 2 1 3 4 5', '7 7 7', '1 2 3 4'], files=SERVERS),
    ])


def project():
    return pj('Консольная погода',
              'Сделай консольный клиент погоды на сервисе http://api.weather.itp/forecast (параметры city и key; ключ — из переменной окружения '
              'WEATHER_KEY, запасное значение demo). Ответ: city, список days (date, t_min, t_max, sky и иногда wind — ветер в м/с) и иногда alert — '
              'предупреждение. На вход подаются команды, последняя — «выход»:\n'
              '— «ГОРОД» → «ГОРОД: сейчас НЕБО, от MIN до MAX» по первому дню, строка «Ветер: W м/с», если в первом дне есть wind, и «⚠ ПРЕДУПРЕЖДЕНИЕ», '
              'если есть alert; нет города — «Нет такого города»;\n'
              '— «неделя ГОРОД» → по дню «ДАТА: MIN…MAX, НЕБО», затем «Средняя максимальная: X» (одна цифра после точки);\n'
              '— «сравнить ГОРОД1 ГОРОД2» → «Теплее в ГОРОД (на D°)» по максимальной температуре первого дня или «Одинаково».\n'
              'Если города нет — «Нет такого города» и для «неделя», и для «сравнить» (когда нет хотя бы одного из двух). '
              'Каждый город запрашивай у сервера не больше одного раза — повторно бери из кэша. После «выход» выведи «Запросов: N».',
              'Функция forecast(city) с кэшем-словарём: если город есть в кэше — вернуть сохранённое, иначе запрос; для 404 храни None\n'
              'Команду разбирай: words = s.split(); первое слово — «неделя», «сравнить» или город',
              'import os\nimport requests\n\nKEY = os.environ.get("WEATHER_KEY", "demo")\ncache = {}\nrequests_sent = 0\n\n\ndef forecast(city):\n    global requests_sent\n'
              '    if city not in cache:\n        r = requests.get("http://api.weather.itp/forecast", params={"city": city, "key": KEY})\n        requests_sent += 1\n'
              '        cache[city] = r.json() if r.ok else None\n    return cache[city]\n\n\nwhile True:\n    words = input().split()\n    if words == ["выход"]:\n        break\n'
              '    if words[0] == "неделя":\n        data = forecast(words[1])\n        if data is None:\n            print("Нет такого города")\n            continue\n'
              '        for d in data["days"]:\n            print(f"{d[\'date\']}: {d[\'t_min\']}…{d[\'t_max\']}, {d[\'sky\']}")\n'
              '        print(f"Средняя максимальная: {sum(d[\'t_max\'] for d in data[\'days\']) / len(data[\'days\']):.1f}")\n    elif words[0] == "сравнить":\n'
              '        a, b = forecast(words[1]), forecast(words[2])\n        if a is None or b is None:\n            print("Нет такого города")\n            continue\n'
              '        ta, tb = a["days"][0]["t_max"], b["days"][0]["t_max"]\n        if ta == tb:\n            print("Одинаково")\n        else:\n'
              '            warm = words[1] if ta > tb else words[2]\n            print(f"Теплее в {warm} (на {abs(ta - tb)}°)")\n    else:\n        data = forecast(words[0])\n'
              '        if data is None:\n            print("Нет такого города")\n            continue\n        d = data["days"][0]\n'
              '        print(f"{data[\'city\']}: сейчас {d[\'sky\']}, от {d[\'t_min\']} до {d[\'t_max\']}")\n        if "wind" in d:\n            print(f"Ветер: {d[\'wind\']} м/с")\n'
              '        if "alert" in data:\n            print(f"⚠ {data[\'alert\']}")\nprint(f"Запросов: {requests_sent}")',
              ['Тюмень\nнеделя Тюмень\nНорильск\nсравнить Сочи Тюмень\nвыход', 'Москва\nнеделя Сочи\nсравнить Сочи Москва\nвыход', 'выход'],
              files=SERVERS)


def build():
    return topic('API: погода, курсы, факты', 'ключи, вложенный JSON, лимиты', [
        th_key(), fl_key(), code_key(),
        th_nested(), fl_nested(), code_nested(),
        project(),
    ], opt=True)
