from dsl import *

# Нора после «Запросы к серверам»: свой веб-сервер. Настоящий Flask/FastAPI слушает порт, а в браузере сети нет, поэтому в ИТП —
# учебный мини-фреймворк miniweb (v5/py/miniweb_shim.py): маршруты декораторами, тест-клиент, мидлвары before/after, serve — подключить
# приложение к учебному requests. Две теории: маршруты и ответы (JSON, коды, параметры пути и запроса); мидлвары и «как на самом деле»
# (Flask и FastAPI — код для компьютера в <pre class="pc">). Задачи читают запросы из ввода и печатают «код тело» через тест-клиент.

FLASK = ('from flask import Flask, request\n\napp = Flask(__name__)\nnotes = []\n\n\n@app.get("/notes")\ndef list_notes():\n    return notes\n\n\n'
         '@app.post("/notes")\ndef add_note():\n    text = request.get_json().get("text", "").strip()\n    if not text:\n        return {"error": "пустая заметка"}, 400\n'
         '    note = {"id": len(notes) + 1, "text": text}\n    notes.append(note)\n    return note, 201\n\n\n@app.get("/notes/&lt;int:note_id&gt;")\ndef get_note(note_id):\n'
         '    for note in notes:\n        if note["id"] == note_id:\n            return note\n    return {"error": "not found"}, 404\n\n\n'
         'if __name__ == "__main__":\n    app.run(debug=True)   # сервер на http://127.0.0.1:5000')
FASTAPI = ('from fastapi import FastAPI, HTTPException\nfrom pydantic import BaseModel\n\napp = FastAPI()\nnotes = []\n\n\nclass NoteIn(BaseModel):\n    text: str\n\n\n'
           '@app.post("/notes", status_code=201)\ndef add_note(data: NoteIn):\n    note = {"id": len(notes) + 1, "text": data.text}\n    notes.append(note)\n    return note\n\n\n'
           '@app.get("/notes/{note_id}")\ndef get_note(note_id: int):\n    for note in notes:\n        if note["id"] == note_id:\n            return note\n'
           '    raise HTTPException(status_code=404, detail="not found")\n\n# запуск в терминале: uvicorn main:app --reload\n# документация API сама появится на http://127.0.0.1:8000/docs')
MW = ('@app.before_request\ndef check_token():\n    if request.headers.get("X-Token") != "s3cret":\n        return {"error": "нужен токен"}, 401\n\n\n'
      '@app.after_request\ndef add_header(response):\n    response.headers["X-Server"] = "itp"\n    return response')


def th_routes():
    terms = [
        ('веб-сервер', 'Программа, которая ждёт HTTP-запросы и отвечает на них. Клиент (браузер, requests, бот) спрашивает — сервер отвечает кодом и телом.'),
        ('маршрут', 'Пара «метод + путь» и функция, которая отвечает на такой запрос: GET /notes → list_notes.'),
        ('miniweb', 'Учебный веб-фреймворк ИТП: устроен как ядро Flask, но работает без сети. from miniweb import App.'),
        ('App', 'App() — приложение-сервер miniweb. Маршруты добавляют декораторами @app.get(путь), @app.post(путь), @app.put, @app.delete.'),
        ('route', '@app.route(путь, methods=["GET", "POST"]) — один обработчик на несколько методов.'),
        ('параметр пути', 'Изменяемая часть пути в угловых скобках: /hello/<name> или /notes/<int:id>. Значение приходит в обработчик '
                          'аргументом с тем же именем; int: превращает его в число, а нечисло даёт 404.'),
        ('обработчик запроса', 'Функция маршрута. Получает объект запроса req (req.method, req.path, req.args — параметры после ?, req.json — тело, '
                               'req.headers) и параметры пути. Вернёт словарь или список — уйдёт JSON с кодом 200, строку — текст, пару (тело, код) — свой код.'),
        ('test_client', 'app.test_client() — клиент для проверки сервера без сети: client.get(путь), client.post(путь, json=…), client.put, client.delete '
                        'возвращают ответ с status_code, text и json().'),
    ]
    body = (
        '<p>В теме «Запросы к серверам» ты спрашивал чужие серверы. Теперь сделаем свой. [[веб-сервер]] — программа, которая на каждый запрос '
        'находит подходящую функцию и возвращает её ответ. Пара «метод + путь» и функция к ней — это [[маршрут]].</p>'
        '<p>Настоящие серверы на Python пишут на Flask или FastAPI — к ним вернёмся во второй теории. В браузере у программ нет сети, поэтому '
        'в ИТП есть учебный фреймворк [[miniweb]]: маршруты в нём объявляются так же, как во Flask. Создаём [[App]] и вешаем на функции '
        'декораторы:</p>'
        + ex('from miniweb import App\n\napp = App()\n\n\n@app.get("/")\ndef index(req):\n    return "Привет! Это мой первый сервер"\n\n\n'
             '@app.get("/hello/<name>")\ndef hello(req, name):\n    return {"greeting": f"Привет, {name}!"}\n\n\nclient = app.test_client()\n'
             'r = client.get("/")\nprint(r.status_code, r.text)\nr = client.get("/hello/Аня")\nprint(r.status_code, r.json())\n'
             'print(client.get("/nope").status_code)') +
        '<p>Декоратор <code>@app.get("/")</code> не меняет функцию, а записывает её в таблицу маршрутов приложения. Каждый [[обработчик запроса]] '
        'первым аргументом получает запрос <code>req</code>. <code>&lt;name&gt;</code> в пути — [[параметр пути]]: что стоит на этом месте, '
        'приходит аргументом name. Пути без маршрута сервер отвечает 404 сам. Проверяем сервер [[test_client]]ом: он отправляет запросы прямо '
        'в приложение и возвращает ответ, как requests.</p>'
        '<h3>JSON API: читать и создавать</h3>'
        '<p>Сервер, который отвечает JSON, — это API, как те, к которым ты уже обращался. Параметры после <code>?</code> лежат в '
        '<code>req.args</code>, тело POST-запроса — в <code>req.json</code>. Чтобы ответить не 200, верни пару (тело, код): 201 — «создано», '
        '400 — «запрос неправильный», 404 — «не найдено»:</p>'
        + ex('from miniweb import App\n\napp = App()\nnotes = []\n\n\n@app.get("/notes")\ndef list_notes(req):\n    limit = int(req.args.get("limit", "10"))\n'
             '    return notes[:limit]\n\n\n@app.post("/notes")\ndef add_note(req):\n    text = (req.json or {}).get("text", "").strip()\n    if not text:\n'
             '        return {"error": "пустая заметка"}, 400\n    note = {"id": len(notes) + 1, "text": text}\n    notes.append(note)\n    return note, 201\n\n\n'
             '@app.get("/notes/<int:note_id>")\ndef get_note(req, note_id):\n    for note in notes:\n        if note["id"] == note_id:\n            return note\n'
             '    return {"error": "not found"}, 404\n\n\nclient = app.test_client()\nfor text in ["купить хлеб", "  ", "позвонить Тимуру"]:\n'
             '    r = client.post("/notes", json={"text": text})\n    print(r.status_code, r.text)\nprint(client.get("/notes?limit=1").json())\n'
             'print(client.get("/notes/2").json(), client.get("/notes/9").status_code, client.get("/notes/abc").status_code)') +
        '<p><code>&lt;int:note_id&gt;</code> пропускает только целые и сразу превращает их в число: <code>/notes/abc</code> не подходит к маршруту — 404. '
        'Если запросить существующий путь другим методом (DELETE /notes), сервер ответит 405 — «метод не разрешён». Один обработчик на '
        'несколько методов вешают через [[route]].</p>'
    )
    return th('Маршруты и ответы', terms, body)


def fl_routes():
    return fl('Маршруты и ответы', [
        q('Что делает декоратор @app.get("/notes")?', 'Записывает функцию как ответ на GET /notes', ['Сразу отправляет запрос GET /notes',
          'Скачивает /notes из интернета'], 'Функция вызывается, когда придёт такой запрос.'),
        q('Обработчик вернул ({"error": "пусто"}, 400). Что получит клиент?', 'Код 400 и JSON с ошибкой', ['Код 200 и кортеж', 'Ошибку TypeError'],
          'Пара (тело, код) задаёт свой код ответа.'),
        q('Маршрут /users/<int:uid>. Что ответит сервер на GET /users/vasya?', '404 — путь не подошёл ни к одному маршруту', ['200 и uid = "vasya"',
          '500 — ошибка в обработчике'], 'int: пропускает только целые числа.'),
        q('Где обработчик найдёт ?page=2 из адреса?', 'В req.args', ['В req.json', 'В параметре пути page'], 'Тело запроса — в req.json.'),
        q('Какой код вернуть, когда POST создал новую запись?', '201', ['200', '404'], '201 Created — «создано».'),
    ])


def code_routes():
    return ts('Маршруты и ответы', [
        task('Визитка. Сделай сервер на miniweb: GET / → текст «API Лисы»; GET /about → JSON {"name": "Лиса", "skills": ["Python", "API"]}; '
             'GET /square/<int:n> → JSON {"n": n, "square": n²} (в miniweb <int:…> принимает и отрицательные). На вход подаются пути через пробел. Для каждого отправь GET тест-клиентом и выведи '
             '«КОД ТЕЛО», где тело — r.text.',
             '@app.get("/square/<int:n>") — n придёт числом. Цикл: for path in input().split().',
             'from miniweb import App\n\napp = App()\n\n\n@app.get("/")\ndef index(req):\n    return "API Лисы"\n\n\n@app.get("/about")\ndef about(req):\n'
             '    return {"name": "Лиса", "skills": ["Python", "API"]}\n\n\n@app.get("/square/<int:n>")\ndef square(req, n):\n    return {"n": n, "square": n * n}\n\n\n'
             'client = app.test_client()\nfor path in input().split():\n    r = client.get(path)\n    print(r.status_code, r.text)',
             ['/ /about /square/12', '/square/-3 /square/x /contacts', '/about/ /square/0']),
        task('Каталог игр. Список игр в программе: [{"title": "Звёздная ферма", "genre": "фермы", "price": 300}, {"title": "Подземелье 2", "genre": "рогалик", '
             '"price": 450}, {"title": "Неоновый город", "genre": "экшен", "price": 1200}, {"title": "Шахтёры", "genre": "песочница", "price": 0}, '
             '{"title": "Рыцарь-пепел", "genre": "экшен", "price": 2000}]. Маршрут GET /games отдаёт названия игр (JSON-список) по возрастанию цены; '
             'параметр genre оставляет игры одного жанра, max_price — не дороже (включительно); параметры можно указать вместе через &. Если max_price не из одних цифр — 400 и {"error": "max_price — число"}. '
             'На вход — пути с параметрами, по одному в строке, до конца ввода. Выводи «КОД ТЕЛО».',
             'req.args.get("genre"), req.args.get("max_price"); проверка числа — .isdigit().\nЧтение до конца: for line in sys.stdin.',
             'import sys\nfrom miniweb import App\n\nGAMES = [{"title": "Звёздная ферма", "genre": "фермы", "price": 300}, {"title": "Подземелье 2", "genre": "рогалик", "price": 450},\n'
             '         {"title": "Неоновый город", "genre": "экшен", "price": 1200}, {"title": "Шахтёры", "genre": "песочница", "price": 0},\n'
             '         {"title": "Рыцарь-пепел", "genre": "экшен", "price": 2000}]\napp = App()\n\n\n@app.get("/games")\ndef games(req):\n    found = GAMES\n'
             '    genre = req.args.get("genre")\n    if genre:\n        found = [g for g in found if g["genre"] == genre]\n    limit = req.args.get("max_price")\n'
             '    if limit is not None:\n        if not limit.isdigit():\n            return {"error": "max_price — число"}, 400\n'
             '        found = [g for g in found if g["price"] <= int(limit)]\n    return [g["title"] for g in sorted(found, key=lambda g: g["price"])]\n\n\n'
             'client = app.test_client()\nfor line in sys.stdin:\n    r = client.get(line.strip())\n    print(r.status_code, r.text)',
             ['/games\n/games?genre=экшен\n/games?max_price=500', '/games?genre=экшен&max_price=1500\n/games?max_price=дёшево\n/games?genre=гонки',
              '/games?max_price=0\n/game']),
        task('Заметки. Сервер заметок: GET /notes — список заметок; POST /notes с JSON {"text": …} создаёт заметку {"id": N, "text": …} (id по порядку '
             'с 1, текст без пробелов по краям) и отвечает 201, а пустой текст — 400 {"error": "пустая заметка"}; GET /notes/<int:id> — заметка '
             'или 404 {"error": "not found"}; DELETE /notes/<int:id> — удалить и ответить 204 с пустым телом (return "", 204), нет такой — 404. Номера '
             'удалённых не используются снова. Каждая строка ввода — «МЕТОД ПУТЬ» или «POST ПУТЬ ТЕКСТ»; текст отправляй как json={"text": ТЕКСТ}. '
             'Выводи «КОД ТЕЛО».',
             'method, path, *rest = line.strip().split(maxsplit=2); client.post(path, json={"text": rest[0] if rest else ""}).\n'
             'Следующий id храни в переменной — длина списка после удаления не подходит.',
             'import sys\nfrom miniweb import App\n\napp = App()\nnotes = []\nnext_id = 1\n\n\n@app.get("/notes")\ndef list_notes(req):\n    return notes\n\n\n'
             '@app.post("/notes")\ndef add_note(req):\n    global next_id\n    text = req.json.get("text", "").strip()\n    if not text:\n'
             '        return {"error": "пустая заметка"}, 400\n    note = {"id": next_id, "text": text}\n    next_id += 1\n    notes.append(note)\n    return note, 201\n\n\n'
             'def find(note_id):\n    for note in notes:\n        if note["id"] == note_id:\n            return note\n    return None\n\n\n'
             '@app.get("/notes/<int:note_id>")\ndef get_note(req, note_id):\n    note = find(note_id)\n    return note if note else ({"error": "not found"}, 404)\n\n\n'
             '@app.delete("/notes/<int:note_id>")\ndef delete_note(req, note_id):\n    note = find(note_id)\n    if not note:\n        return {"error": "not found"}, 404\n'
             '    notes.remove(note)\n    return "", 204\n\n\nclient = app.test_client()\nfor line in sys.stdin:\n    method, path, *rest = line.strip().split(maxsplit=2)\n'
             '    if method == "POST":\n        r = client.post(path, json={"text": rest[0] if rest else ""})\n    elif method == "DELETE":\n        r = client.delete(path)\n'
             '    else:\n        r = client.get(path)\n    print(r.status_code, r.text)',
             ['POST /notes купить хлеб\nPOST /notes позвонить Тимуру\nGET /notes\nGET /notes/2\nDELETE /notes/1\nGET /notes\nPOST /notes сдать проект\nGET /notes/3',
              'POST /notes\nGET /notes/1\nDELETE /notes/5\nPOST /notes   полить кактус  \nGET /notes']),
    ])


def th_mw():
    terms = [
        ('мидлвар', 'Функция, через которую проходит каждый запрос до обработчика или каждый ответ после него: журнал, проверка токена, лимиты. '
                    'По-английски middleware — «прослойка».'),
        ('before', '@app.before — мидлвар до обработчика: функция(req). Вернула None — запрос идёт дальше; вернула ответ — обработчик не вызывается.'),
        ('after', '@app.after — мидлвар после обработчика: функция(req, resp). Видит готовый ответ, может записать его в журнал или поменять.'),
        ('request', 'client.request(метод, путь, json=…, headers=…) — запрос тест-клиента методом, заданным строкой: client.request("PUT", "/tasks/1", '
                    'json={"done": True}). Удобно, когда метод приходит из данных.'),
        ('serve', 'app.serve("адрес") — подключить приложение к учебному requests: запросы на http://адрес/… теперь обработает оно.'),
        ('Flask', 'Популярный веб-фреймворк для Python: pip install flask, маршруты — декораторами, app.run() запускает сервер на компьютере.'),
        ('FastAPI', 'Современный веб-фреймворк: типы параметров из подсказок типов, проверка данных, документация API сама по адресу /docs. '
                    'Запуск — uvicorn main:app.'),
    ]
    body = (
        '<p>У серверов есть дела, общие для всех маршрутов: записать каждый запрос в журнал, проверить токен, посчитать запросы клиента. Писать это '
        'в каждом обработчике — плохая идея. Такие дела выносят в [[мидлвар]]ы — функции, через которые проходит каждый запрос. Мидлвар [[before]] '
        'работает до обработчика и может сразу ответить вместо него, [[after]] — после, когда ответ уже готов:</p>'
        + ex('from miniweb import App\n\napp = App()\nlog = []\n\n\n@app.before\ndef check_token(req):\n    if req.path.startswith("/admin") and req.headers.get("x-token") != "s3cret":\n'
             '        return {"error": "нужен токен"}, 401\n\n\n@app.after\ndef write_log(req, resp):\n    log.append(f"{req.method} {req.path} → {resp.status_code}")\n\n\n'
             '@app.get("/")\ndef index(req):\n    return "Главная"\n\n\n@app.get("/admin/stats")\ndef stats(req):\n    return {"requests": len(log)}\n\n\n'
             'client = app.test_client()\nclient.get("/")\nclient.get("/admin/stats")\nprint(client.get("/admin/stats", headers={"X-Token": "s3cret"}).json())\n'
             'print(*log, sep="\\n")') +
        '<p>Второй запрос до обработчика не дошёл: before вернул 401. А журнал записал все три запроса — after видит и ответы мидлваров. '
        'Имена заголовков не зависят от регистра, поэтому miniweb хранит их строчными: <code>req.headers.get("x-token")</code>.</p>'
        '<h3>Сервер и клиент вместе</h3>'
        '<p>Тест-клиент удобен для проверки, но обычно к серверу обращаются по адресу. [[serve]] подключает приложение к учебному requests — и '
        'к своему API можно ходить так же, как к чужим:</p>'
        + ex('import requests\nfrom miniweb import App\n\napp = App("погода")\n\n\n@app.get("/now")\ndef now(req):\n    temps = {"Сочи": 14, "Тюмень": -3}\n'
             '    city = req.args.get("city")\n    if city not in temps:\n        return {"error": "нет города"}, 404\n    return {"city": city, "temp": temps[city]}\n\n\n'
             'app.serve("api.my.itp")\nr = requests.get("http://api.my.itp/now", params={"city": "Сочи"})\nprint(r.status_code, r.json())\n'
             'print(requests.get("http://api.my.itp/now", params={"city": "Марс"}).status_code)') +
        '<h3>Как это на самом деле: Flask и FastAPI</h3>'
        '<p>miniweb повторяет устройство [[Flask]] — самого известного фреймворка. Тот же сервер заметок на Flask (на компьютере: '
        '<code>pip install flask</code>, затем запустить файл и открыть адрес в браузере):</p>'
        '<pre class="pc">' + FLASK + '</pre>'
        '<p>Отличия от miniweb: запрос во Flask не аргумент, а общий объект <code>request</code>; параметр пути — <code>&lt;int:note_id&gt;</code>, '
        'как у нас; <code>app.run()</code> запускает настоящий сервер, к которому можно обратиться из браузера и из requests. Мидлвары во Flask '
        'выглядят так:</p>'
        '<pre class="pc">' + MW + '</pre>'
        '<p>[[FastAPI]] — более новый фреймворк. Он берёт типы из подсказок типов: <code>note_id: int</code> сам проверит число, а класс-модель pydantic '
        'проверит тело запроса. Документацию API он строит сам:</p>'
        '<pre class="pc">' + FASTAPI + '</pre>'
        '<p>Логику, которую ты пишешь в задачах — маршруты, коды, проверки, мидлвары, — можно почти без изменений перенести на Flask.</p>'
    )
    return th('Мидлвары и настоящие фреймворки', terms, body)


def fl_mw():
    return fl('Мидлвары и настоящие фреймворки', [
        q('Мидлвар before вернул ({"error": "нужен токен"}, 401). Что будет?', 'Обработчик не вызовется, клиент получит 401',
          ['Обработчик вызовется, код станет 401', 'Сервер упадёт с ошибкой'], 'Ответ мидлвара заменяет обработчик.'),
        q('Где удобнее всего вести журнал всех запросов с кодами?', 'В мидлваре after', ['В каждом обработчике', 'В мидлваре before'],
          'after видит и запрос, и готовый ответ.'),
        q('Чем Flask отличается от miniweb?', 'Он запускает настоящий сервер, доступный по сети', ['У него нет декораторов маршрутов', 'Он работает только в браузере'],
          'app.run() слушает порт на компьютере.'),
        q('Что даёт FastAPI подсказка note_id: int?', 'Сам проверит, что в пути число', ['Ничего, это комментарий', 'Сделает note_id глобальной'],
          'Нечисло — ошибка 422 без твоего кода.'),
    ])


def code_mw():
    return ts('Мидлвары и настоящие фреймворки', [
        task('Охранник. Сервер: GET /public → «для всех», GET /admin/users → JSON ["Аня", "Тимур"], GET /admin/logs → JSON {"lines": 42}. Мидлвар before: '
             'пути, начинающиеся с /admin, требуют заголовок X-Token со значением s3cret, иначе 401 и {"error": "нужен токен"}. Мидлвар after печатает '
             'журнал «МЕТОД ПУТЬ → КОД» сразу, как только ответ готов (до того, как программа напечатает тело). Каждая строка ввода — путь и, возможно, токен через пробел. Отправь GET с заголовком {"X-Token": токен} '
             '(без токена — без заголовков) и выведи тело ответа. После всех запросов — «Отказов: N» (сколько ответов 401).',
             'path, *token = line.split(); headers={"X-Token": token[0]} if token else {}.\nОтказы считай в after: resp.status_code == 401.',
             'import sys\nfrom miniweb import App\n\napp = App()\ndenied = 0\n\n\n@app.before\ndef guard(req):\n    if req.path.startswith("/admin") and req.headers.get("x-token") != "s3cret":\n'
             '        return {"error": "нужен токен"}, 401\n\n\n@app.after\ndef journal(req, resp):\n    global denied\n    if resp.status_code == 401:\n        denied += 1\n'
             '    print(f"{req.method} {req.path} → {resp.status_code}")\n\n\n@app.get("/public")\ndef public(req):\n    return "для всех"\n\n\n'
             '@app.get("/admin/users")\ndef users(req):\n    return ["Аня", "Тимур"]\n\n\n@app.get("/admin/logs")\ndef logs(req):\n    return {"lines": 42}\n\n\n'
             'client = app.test_client()\nfor line in sys.stdin:\n    path, *token = line.split()\n    r = client.get(path, headers={"X-Token": token[0]} if token else {})\n'
             '    print(r.text)\nprint(f"Отказов: {denied}")',
             ['/public\n/admin/users\n/admin/users s3cret\n/admin/logs 12345', '/admin/logs s3cret\n/public s3cret\n/nothing']),
        task('Лимит запросов. Сервер с одним маршрутом GET /joke → JSON {"joke": "Почему питон не кусается? У него нет багов."}. Мидлвар before считает '
             'запросы каждого клиента (заголовок X-User) и с 4-го запроса отвечает 429 и {"error": "слишком часто, подожди"}. Запрос без X-User — 400 и '
             '{"error": "кто ты?"}. Строка ввода — имя клиента или «-» (без заголовка). Выведи «ИМЯ: КОД» на каждый запрос, а в конце — клиентов по '
             'алфавиту «ИМЯ — запросов: N» (считаются все запросы с заголовком, и отклонённые тоже).',
             'Счётчики — словарь имя → число; в before: counts[user] = counts.get(user, 0) + 1, затем if counts[user] > 3.',
             'import sys\nfrom miniweb import App\n\napp = App()\ncounts = {}\n\n\n@app.before\ndef limit(req):\n    user = req.headers.get("x-user")\n    if not user:\n'
             '        return {"error": "кто ты?"}, 400\n    counts[user] = counts.get(user, 0) + 1\n    if counts[user] > 3:\n        return {"error": "слишком часто, подожди"}, 429\n\n\n'
             '@app.get("/joke")\ndef joke(req):\n    return {"joke": "Почему питон не кусается? У него нет багов."}\n\n\nclient = app.test_client()\n'
             'for line in sys.stdin:\n    name = line.strip()\n    r = client.get("/joke", headers={} if name == "-" else {"X-User": name})\n    print(f"{name}: {r.status_code}")\n'
             'for name in sorted(counts):\n    print(f"{name} — запросов: {counts[name]}")',
             ['Аня\nАня\nТимур\nАня\nАня\n-', 'Зоя\nЗоя\nЗоя\nЗоя\nЗоя\nБорис']),
        task('Свой роутер. Как miniweb устроен внутри? Напиши класс Router: метод get(path) — декоратор, который запоминает функцию в словаре путь → '
             'функция и возвращает её же; метод handle(path) вызывает функцию пути без аргументов и возвращает пару (200, результат), а для '
             'неизвестного пути — (404, "not found"). Параметры пути не нужны.',
             'def get(self, path):\n    def deco(f):\n        self.routes[path] = f\n        return f\n    return deco',
             'class Router:\n    def __init__(self):\n        self.routes = {}\n\n    def get(self, path):\n        def deco(f):\n            self.routes[path] = f\n'
             '            return f\n        return deco\n\n    def handle(self, path):\n        if path not in self.routes:\n            return 404, "not found"\n'
             '        return 200, self.routes[path]()\n',
             ['r = Router()\n\n@r.get("/")\ndef index():\n    return "главная"\n\nprint(r.handle("/"), r.handle("/x"))\nprint(index())',
              'r = Router()\n\n@r.get("/a")\ndef a():\n    return [1, 2]\n\n@r.get("/b")\ndef b():\n    return {"b": True}\n\nprint(r.handle("/b"), r.handle("/a"), sorted(r.routes))'],
             tail=TL),
    ])


def project():
    return pj('API списка дел',
              'Сервер списка дел на miniweb. Каждый запрос должен нести заголовок Authorization со значением «Bearer demo», иначе — 401 и '
              '{"error": "нужен токен"} (мидлвар before). Маршруты:\n'
              '— POST /tasks с JSON {"title": …} → 201 и задача {"id": N, "title": …, "done": false} (id по порядку с 1, без повторов); '
              'нет title или он пустой после strip → 400 {"error": "нужно название"};\n'
              '— GET /tasks → список задач; ?done=1 — только сделанные, ?done=0 — только несделанные;\n'
              '— PUT /tasks/<int:id> с JSON {"done": true или false} → обновлённая задача; нет задачи → 404 {"error": "not found"};\n'
              '— DELETE /tasks/<int:id> → 204 с пустым телом; нет задачи → 404 {"error": "not found"}.\n'
              'Строка ввода — «ТОКЕН МЕТОД ПУТЬ» или «ТОКЕН МЕТОД ПУТЬ JSON» (JSON-тело одной строкой); токен «-» — запрос без заголовка. '
              'Токен проверяется для любого пути; другой метод на существующий путь miniweb отклонит сам кодом 405, несуществующий путь — 404; они тоже ошибки. done из тела приводи к bool, а фильтр ?done бывает только 1 или 0. Выводи «КОД ТЕЛО», а в конце — «Запросов: N, ошибок: M» (ошибка — ответ с кодом 400 и выше; считай в мидлваре after).',
              'Разбор строки: token, method, path, *rest = line.strip().split(maxsplit=3); тело — json.loads(rest[0]) if rest else None\n'
              'Отправка любым методом — client.request(method, path, json=body, headers=headers)\n'
              'Фильтр done: req.args.get("done") == "1" — сделанные',
              'import json\nimport sys\nfrom miniweb import App\n\napp = App()\ntasks = []\nnext_id = 1\nstats = {"all": 0, "errors": 0}\n\n\n@app.before\ndef auth(req):\n'
              '    if req.headers.get("authorization") != "Bearer demo":\n        return {"error": "нужен токен"}, 401\n\n\n@app.after\ndef count(req, resp):\n'
              '    stats["all"] += 1\n    if resp.status_code >= 400:\n        stats["errors"] += 1\n\n\ndef find(task_id):\n    for t in tasks:\n'
              '        if t["id"] == task_id:\n            return t\n    return None\n\n\n@app.post("/tasks")\ndef add(req):\n    global next_id\n'
              '    title = str((req.json or {}).get("title", "")).strip()\n    if not title:\n        return {"error": "нужно название"}, 400\n'
              '    t = {"id": next_id, "title": title, "done": False}\n    next_id += 1\n    tasks.append(t)\n    return t, 201\n\n\n@app.get("/tasks")\ndef list_tasks(req):\n'
              '    done = req.args.get("done")\n    if done is None:\n        return tasks\n    return [t for t in tasks if t["done"] == (done == "1")]\n\n\n'
              '@app.put("/tasks/<int:task_id>")\ndef update(req, task_id):\n    t = find(task_id)\n    if not t:\n        return {"error": "not found"}, 404\n'
              '    t["done"] = bool((req.json or {}).get("done"))\n    return t\n\n\n@app.delete("/tasks/<int:task_id>")\ndef remove(req, task_id):\n    t = find(task_id)\n'
              '    if not t:\n        return {"error": "not found"}, 404\n    tasks.remove(t)\n    return "", 204\n\n\nclient = app.test_client()\nfor line in sys.stdin:\n'
              '    token, method, path, *rest = line.strip().split(maxsplit=3)\n    body = json.loads(rest[0]) if rest else None\n'
              '    headers = {} if token == "-" else {"Authorization": f"Bearer {token}"}\n    r = client.request(method, path, json=body, headers=headers)\n'
              '    print(r.status_code, r.text)\nprint(f"Запросов: {stats[\'all\']}, ошибок: {stats[\'errors\']}")',
              ['demo POST /tasks {"title": "выучить декораторы"}\ndemo POST /tasks {"title": "  "}\ndemo POST /tasks {"title": "сделать API"}\n'
               '- GET /tasks\ndemo PUT /tasks/1 {"done": true}\ndemo GET /tasks?done=1\ndemo GET /tasks?done=0\ndemo DELETE /tasks/2\ndemo DELETE /tasks/2\n'
               'demo POST /tasks {"title": "отдохнуть"}\ndemo GET /tasks',
               'hacker GET /tasks\ndemo PUT /tasks/7 {"done": true}\ndemo POST /tasks {}\ndemo GET /tasks\ndemo POST /tasks {"title": "один"}\ndemo GET /tasks/1'])


def build():
    return topic('Веб-сервер: свой API', 'маршруты, JSON, мидлвары, Flask и FastAPI', [
        th_routes(), fl_routes(), code_routes(),
        th_mw(), fl_mw(), code_mw(),
        project(),
    ], opt=True)
