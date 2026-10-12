from dsl import *
from json import dumps as _dumps


def _fig(key, alt, cap):
    return '<figure class="fig"><img class="figi" data-x="p-' + key + '" alt="' + alt + '"></figure><p class="mu" style="margin:-6px 0 12px;font-size:.88rem">' + cap + '</p>'


def _logs(pairs, extra=None):
    ls = []
    for n, t in pairs:
        ls.append(_dumps({"handler": "attempt_handler", "params": {"name": n, "task": t}, "response": [200, "Good try, %s! Your attempt on task '%s' is accepted!" % (n, t)]}))
    for n in (extra or []):
        ls.append(_dumps({"handler": "user_handler", "params": {"name": n}, "response": [200, "Hello, %s!" % n]}))
    return ls


H_ALL = '''
def home_handler(params):
    return 200, "Home Page"


def admin_handler(params):
    return 200, "Admin Panel"


def user_handler(params):
    # Должен использовать параметр name из URL
    return 200, f"Hello, {params['name']}!"


def attempt_handler(params):
    # Должен использовать параметр name из URL
    return (
        200,
        f"Good try, {params['name']}! Your attempt on task '{params['task']}' is accepted!",
    )


def not_found_handler(params):
    return 404, "Not Found"
'''

ROUTER = '''
# Функция маршрутизации
def router(path):
    if path == "/":
        return home_handler
    elif path.startswith("/user"):
        return user_handler
    elif path.startswith("/attempt"):
        return attempt_handler
    elif path.startswith("/admin"):
        return admin_handler
    return not_found_handler
'''

SERVER_OK = '''
def wsgi_server():
    """Обрабатывает запросы и возвращает каждый из ответов через yield"""
    request = yield None
    while True:
        method, path = request.split()[:2]
        params = {}
        if "?" in path:
            query = path.split("?")[1]
            for pair in query.split("&"):
                if "=" in pair:
                    key, value = pair.split("=")
                    params[key] = value
        handler = router(path)
        response = handler(params)
        request = yield response
'''

DECOR_OK = '''
def require_auth(func):
    """Декоратор проверки авторизации"""
    @wraps(func)
    def wrapper(params):
        if "name" not in params:
            return 403, "Forbidden"
        return func(params)
    return wrapper


def log_call(func):
    """Декоратор логирования"""
    @wraps(func)
    def wrapper(params):
        result = func(params)
        print(dumps({"handler": func.__name__, "params": params, "response": result}))
        return result
    return wrapper
'''


def _decorated_handlers():
    return '''
@log_call
def home_handler(params):
    return 200, "Home Page"


@log_call
def admin_handler(params):
    return 200, "Admin Panel"


@log_call
@require_auth
def user_handler(params):
    # Должен использовать параметр name из URL
    return 200, f"Hello, {params['name']}!"


@log_call
@require_auth
def attempt_handler(params):
    # Должен использовать параметр name из URL
    return (
        200,
        f"Good try, {params['name']}! Your attempt on task '{params['task']}' is accepted!",
    )


@log_call
def not_found_handler(params):
    return 404, "Not Found"
'''


def build():
    # ============ Теория 1: архитектура ============
    terms1 = [
        ('клиент', 'Часть приложения, которую видит и с которой работает пользователь: сайт в браузере или мобильное приложение. Клиент отправляет запросы и показывает полученные ответы.'),
        ('сервер', 'Программа, которая принимает запросы от клиентов, обрабатывает их и отправляет ответы. Работает постоянно и ждёт новых запросов.'),
        ('микросервис', 'Небольшой самостоятельный сервис, который отвечает за одну часть большого приложения (каталог, корзина, оплата) и имеет собственную базу данных. Его можно менять независимо от остальных.'),
        ('API Gateway', 'Входная точка большого приложения: принимает запрос от клиента, определяет, какому сервису он адресован, и передаёт его. Затем возвращает клиенту ответ сервиса. Что-то вроде секретаря.'),
        ('ASGI/WSGI-сервер', 'Программа внутри сервиса, которая принимает запросы и передаёт их нужным обработчикам. WSGI и ASGI это принятые в Python стандарты такого взаимодействия (ASGI поддерживает асинхронность).'),
        ('ручка', 'Обработчик запроса (handler): функция сервиса, которая выполняет одно действие, например «выдать профиль пользователя». Её вызывает сервер, когда приходит подходящий запрос. Ручку ещё называют хендлером.'),
        ('маршрут', 'Часть запроса, которая определяет, какая ручка должна его обработать. Выглядит как путь в проводнике: /categories/123.\n\nПример:\n/user\n/attempt'),
        ('HTTP-метод', 'Слово в начале запроса, которое говорит, что нужно сделать: GET (получить данные), POST (отправить или создать), PUT (обновить), DELETE (удалить), PATCH (частично изменить).'),
        ('код состояния', 'Трёхзначное число в ответе сервера. 200 означает «успешно», 403 «доступ запрещён», 404 «не найдено».'),
    ]
    body1 = '''
<p>Это заключительная часть блока про функции. Задача, которую ты решишь, очень похожа на то, что делают Python-разработчики на работе. Сначала разберёмся, откуда она берётся.</p>

<h3>Как устроены современные приложения</h3>
<p>В разработке важны две вещи: как быстро новая возможность доходит до пользователя и насколько качественен код. Поэтому команды работают небольшими циклами, спринтами: фиксированный отрезок времени от одной до четырёх недель, за который нужно выпустить небольшую, но готовую часть функциональности. Над одним продуктом обычно параллельно работает несколько команд, и чтобы они не мешали друг другу, придумали особый способ организации кода: микросервисы.</p>
<p>Способ организации кода называется архитектурой. Самая простая архитектура веб-приложения из трёх частей показана на схеме. Пользователь видит интерфейс ([[клиент|клиент]]), интерфейс отправляет запросы [[сервер|веб-серверу]], а сервер при необходимости ходит в базу данных. Часть, которая находится за интерфейсом (сервер и база), называется бэкендом, и в основном её пишут на Python.</p>
''' + _fig('webapp', 'Схема работы веб-приложения: интерфейс (клиент), веб-сервер, база данных; сервер и база вместе образуют backend', 'Упрощённая схема веб-приложения. Стрелки показывают, как запрос идёт от пользователя к базе и как ответ возвращается обратно.') + '''
<h3>Микросервисы</h3>
<p>В микросервисной архитектуре код состоит из множества небольших изолированных сервисов. Каждый можно обновлять независимо, не ломая остальное приложение. Обычно сервис делают таким, чтобы его устройство целиком помещалось в голове одного разработчика. Такой маленький сервис называют [[микросервис|микросервисом]]. Посмотри, как это может выглядеть у маркетплейса:</p>
''' + _fig('market', 'Архитектура маркетплейса: веб-приложение и мобильное приложение обращаются через API Gateway к сервисам каталога, товаров, корзины, оплаты, доставки и отзывов, у каждого своя база данных', 'Пример архитектуры маркетплейса.') + '''
<p>Как это работает:</p>
<ol>
<li>Приходит запрос от клиента (веб- или мобильного приложения).</li>
<li>[[API Gateway|API Gateway]] как секретарь читает запрос и направляет его в нужный сервис.</li>
<li>Сервис обрабатывает запрос по своей логике и использует собственную базу данных.</li>
<li>Готовый ответ возвращается в API Gateway, а тот отправляет его клиенту.</li>
</ol>
<p>Спустимся на уровень глубже, внутрь одного сервиса. Устроен он похоже: принимает запросы и раздаёт их по обработчикам тот же самый посредник, только называется он [[ASGI/WSGI-сервер|ASGI/WSGI-сервером]] (Asynchronous или Web Server Gateway Interface). Обработчики называют [[ручка|ручками]] или хендлерами. Они выясняют, чего хотел клиент, и сами ходят в базу данных.</p>
''' + _fig('catalog', 'Архитектура сервиса каталога: ASGI/WSGI-сервер принимает запросы и по маршрутам вызывает ручки get_all_categories_handler, get_category_by_id_handler и другие, каждая работает со своей базой', 'Пример устройства сервиса каталога. Каждый маршрут (Route) ведёт в свою ручку.') + '''
<h3>Как выглядит запрос</h3>
<p>Запрос это строка, составленная по определённому правилу. Она запускает определённую ручку. Обычно запрос выглядит так:</p>
<pre class="out">[HTTP-метод] /[маршрут]</pre>
<p>Например, <code>GET /categories/123</code>. Здесь <code>GET</code> это [[HTTP-метод|HTTP-метод]] одним словом (бывают ещё POST, PUT, DELETE, PATCH), <code>/categories/123</code> это [[маршрут|маршрут]]. Он может быть сколь угодно длинным, но хорошей практикой считается не больше трёх уровней. Число 123 здесь идентификатор категории.</p>
<p>В запросе могут быть уточняющие параметры. Их пишут после знака вопроса, разделяя символом &amp;, а имя от значения отделяют знаком равенства:</p>
<pre class="out">GET /categories/123/products?price_range=1000-5000&amp;attributes=color:red</pre>
<p>Для «Сервиса каталога» с картинки запросы и ручки могут быть такими:</p>
<div style="overflow-x:auto;margin:0 0 14px"><table style="margin:0">
<tr><th>Метод</th><th>Маршрут</th><th>Что делает</th><th>Ручка</th></tr>
<tr><td>GET</td><td>/categories</td><td>список всех категорий</td><td>get_all_categories_handler</td></tr>
<tr><td>GET</td><td>/categories/{id}</td><td>информация о категории по ID</td><td>get_category_by_id_handler</td></tr>
<tr><td>GET</td><td>/categories/{id}/children</td><td>подкатегории категории</td><td>get_subcategories_handler</td></tr>
<tr><td>GET</td><td>/categories/{id}/filters</td><td>доступные фильтры</td><td>get_category_filters_handler</td></tr>
<tr><td>GET</td><td>/categories/{id}/products</td><td>товары категории</td><td>get_products_by_category_handler</td></tr>
<tr><td>POST</td><td>/categories</td><td>создать категорию (админам)</td><td>create_category_handler</td></tr>
<tr><td>PUT</td><td>/categories/{id}</td><td>обновить категорию</td><td>update_category_handler</td></tr>
<tr><td>DELETE</td><td>/categories/{id}</td><td>удалить категорию</td><td>delete_category_handler</td></tr>
</table></div>
<p>В ответе сервер сообщает, чем всё закончилось, с помощью [[код состояния|кода состояния]]: <b>200</b> всё получилось, <b>403</b> доступ запрещён (нет прав), <b>404</b> такой страницы или объекта нет. С ними мы и будем работать.</p>
'''
    th1 = th('Как устроены сервисы', terms1, body1)

    fl1 = fl('Вопросы: архитектура сервисов', [
        q('Что такое микросервисная архитектура?', 'Много небольших независимых сервисов', ['Один очень большой файл с кодом', 'Приложение без базы данных', 'Приложение, которое работает только на телефоне'], 'Приложение делят на небольшие сервисы, каждый отвечает за свою часть. Их можно менять независимо друг от друга.'),
        q('Что делает API Gateway?', 'Принимает запрос и направляет его нужному сервису', ['Хранит данные пользователей', 'Рисует интерфейс сайта', 'Проверяет орфографию в запросе'], 'Это входная точка приложения: как секретарь, который смотрит, кому адресован запрос, и передаёт его туда.'),
        q('Что такое «ручка» (handler)?', 'Функция сервиса, обрабатывающая определённый запрос', ['Кнопка на сайте', 'Файл с логами', 'Таблица в базе данных'], 'Ручка это обработчик: функция, которую вызывает сервер, когда приходит запрос с подходящим маршрутом.'),
        q('Кто выбирает, какая ручка обработает запрос?', 'ASGI/WSGI-сервер по маршруту', ['Сам пользователь вручную', 'База данных', 'Браузер'], 'Сервер читает маршрут запроса и вызывает подходящую ручку. Для этого в нём используется функция маршрутизации.'),
        q('Какой метод означает «получить данные»?', 'GET', ['POST', 'DELETE', 'PUT'], 'GET запрашивает данные, POST отправляет или создаёт, PUT обновляет, DELETE удаляет.'),
        q('Что означает код состояния 404?', 'Страница или объект не найдены', ['Всё прошло успешно', 'Доступ запрещён', 'Сервер перегружен'], '200 это успех, 403 запрет доступа, 404 «не найдено». Для неизвестных маршрутов сервис возвращает именно 404.'),
        q('Что означает код состояния 403?', 'Доступ запрещён', ['Страница не найдена', 'Всё прошло успешно', 'Запрос слишком длинный'], 'Код 403 (Forbidden) сервер возвращает, когда пользователь не авторизован или у него нет прав на действие.'),
        q('Какая часть запроса GET /user?name=Ann является маршрутом?', '/user', ['GET', 'name=Ann', 'user?name'], 'GET это метод, /user это маршрут (путь к ручке), а после знака вопроса идут параметры: name=Ann.'),
        q('Какой знак разделяет параметры запроса между собой?', '&', ['?', '/', ';'], 'Знак вопроса отделяет параметры от маршрута, символ & разделяет параметры между собой, а = отделяет имя параметра от значения.'),
        q('Что относится к бэкенду?', 'Веб-сервер и база данных', ['Кнопки и цвета на странице', 'Анимации интерфейса', 'Иконка в мобильном приложении'], 'Фронтенд это то, что видит пользователь. Бэкенд это сервер и база данных, которые обрабатывают запросы и хранят данные.'),
    ])

    # ============ Теория 2: условие и инструменты ============
    terms2 = [
        ('router', 'Функция маршрутизации. Получает маршрут и возвращает (не вызывая!) подходящую ручку.\n\nПример:\ndef router(path):\n    if path == "/":\n        return home\n    return not_found'),
        ('мидлвара', 'Дополнительная функциональность, которая выполняется между получением запроса и отправкой ответа: проверка авторизации, логирование. Её удобно делать декораторами. По-английски middleware.'),
        ('лог', 'Журнал работы программы: записи о том, что произошло. Каждая запись содержит данные об одном событии, например, какая ручка вызвана, с какими параметрами и что вернула.'),
        ('defaultdict', 'Особый словарь из модуля collections. При обращении к отсутствующему ключу сам создаёт значение по умолчанию. defaultdict(int) создаёт 0, поэтому им удобно считать.\n\nПример:\nfrom collections import defaultdict\nc = defaultdict(int)\nc["a"] += 1\nprint(dict(c))\nВывод:\n{\'a\': 1}'),
    ]
    body2 = '''
<h3>Задача</h3>
<p>Ты разработчик в компании, которая готовит школьников к экзаменам. Продукт компании это веб-приложение, где школьники проходят варианты тестов. Команда уже написала несколько ручек. Тебе поручили собрать сервер, который ловит запросы, передаёт их в нужные ручки, ведёт журнал и анализирует его.</p>
<p>За один присест такую задачу не решить, поэтому её разбили (декомпозировали) на три последовательных этапа:</p>
<ol>
<li>Сделать генератор запросов и запуск нужного обработчика.</li>
<li>Обернуть ручки декораторами, чтобы собирать логи использования и проверять авторизацию.</li>
<li>Проанализировать логи сервиса и составить небольшую сводку.</li>
</ol>
''' + _fig('fastapi', 'Схема работы сервиса: 1 генератор запросов запускает нужный обработчик, 2 декораторы вокруг обработчиков создают логи, 3 анализ логов работы сервиса', 'Три этапа проекта на схеме сервиса. Сервер принимает запросы, по маршрутам (Route 1 ... Route 5) вызывает ручки, а декораторы между ними пишут логи.') + '''
<p>Запросы приходят в формате <code>[HTTP-метод] /[маршрут]?[параметр1]=[значение1]&amp;[параметр2]=[значение2]</code>, например <code>GET /user?name=John&amp;session=15</code> или <code>POST /attempt?name=Max&amp;task=Snake</code>. В сервисе есть такие ручки:</p>
<div style="overflow-x:auto;margin:0 0 14px"><table style="margin:0">
<tr><th>Метод</th><th>Маршрут</th><th>Что делает</th><th>Ручка</th></tr>
<tr><td>GET</td><td>/</td><td>домашняя страница</td><td>home_handler</td></tr>
<tr><td>GET</td><td>/admin</td><td>страница администратора</td><td>admin_handler</td></tr>
<tr><td>GET</td><td>/user?name=</td><td>профиль пользователя</td><td>user_handler</td></tr>
<tr><td>POST</td><td>/attempt?name=&amp;task=</td><td>попытка решить задачу</td><td>attempt_handler</td></tr>
<tr><td>любой</td><td>всё остальное</td><td>страница ошибки 404</td><td>not_found_handler</td></tr>
</table></div>

<h3>Этап 1: сервер как генератор</h3>
<p>Сервер должен работать «вечно»: принять запрос, ответить и ждать следующий, не останавливаясь. Такое удобно описать генератором, в который запросы попадают через <code>send</code> (мы разбирали это в теме про генераторы). Шаблон имитации сервера, который будет уже написан за тебя:</p>
''' + exs('''app = wsgi_server()
app.send(None)

for request in sys.stdin:
    print(app.send(request))''', '''(каждый запрос из ввода попадает в генератор, а ответ печатается)''') + '''
<p>Тебе нужно написать только функцию-генератор <code>wsgi_server()</code>. Она получает запрос строкой (например, <code>"POST /attempt?name=Max&amp;task=Snake"</code>), а в ответ через <code>yield</code> отдаёт то, что вернула нужная ручка. Нужно сделать три шага:</p>
<ol>
<li>Разобрать строку на метод, маршрут и параметры.</li>
<li>Найти ручку функцией маршрутизации [[router|router]].</li>
<li>Вызвать ручку с параметрами и выдать результат.</li>
</ol>
<p>Разбираем строку методом split. Метод и путь разделены пробелом, путь от параметров отделяет знак вопроса, а параметры между собой знак &amp;:</p>
''' + ex('''request = "POST /attempt?name=Max&task=Snake"
method, path = request.split()
print(method)
print(path)

params = {}
query = path.split("?")[1]
for pair in query.split("&"):
    key, value = pair.split("=")
    params[key] = value
print(params)''') + '''
<p>Теперь функция маршрутизации. Обрати внимание: она не вызывает ручку, а <b>возвращает саму функцию</b>, помнишь, функции можно передавать и возвращать как значения. Вызываем её мы уже сами:</p>
''' + ex('''def home_handler(params):
    return 200, "Home Page"

def not_found_handler(params):
    return 404, "Not Found"

def router(path):
    if path == "/":
        return home_handler
    return not_found_handler

handler = router("/unknown")
print(handler.__name__)
print(handler({}))''') + '''
<p>Если запрос содержит лишние параметры, это не страшно: ручка берёт из словаря только то, что ей нужно. А вот параметров «с запасом» хватать должно, так что ручки сами рассчитывают, что нужные ключи есть.</p>

<h3>Этап 2: декораторы и логи</h3>
<p>Функциональность, которая выполняется «между» получением запроса и ответом, называется [[мидлвара|мидлварой]] (middleware). У нас их две: проверка авторизации и логирование. Обе удобно оформить декораторами, как мы делали в теме про декораторы. В шаблоне каждая ручка уже обёрнута нужными декораторами, и тебе осталось только их написать:</p>
<ul>
<li><b>@require_auth</b> проверяет, есть ли в параметрах name. Если нет, ручка не вызывается, а в ответ возвращается пара (403, "Forbidden").</li>
<li><b>@log_call</b> вызывает ручку и печатает запись журнала ([[лог|лог]]) в формате JSON: имя ручки, параметры и ответ.</li>
</ul>
<p>Пример записи журнала:</p>
<pre class="out">{"handler": "attempt_handler", "params": {"name": "Max", "task": "Snake"}, "response": [200, "Good try, Max! Your attempt on task 'Snake' is accepted!"]}</pre>
<p>Имя ручки берём у функции: <code>func.__name__</code>. Чтобы оно не потерялось, когда над ручкой стоит несколько декораторов, в каждом декораторе обёртку нужно оформить через @wraps. Цепочка <code>@log_call</code> над <code>@require_auth</code> срабатывает так: ручку сначала оборачивает require_auth, а потом получившуюся функцию оборачивает log_call. Поэтому в журнал попадает и ответ 403, если авторизации нет.</p>
<p>Запись журнала печатается функцией dumps из модуля json. Для текста на русском нужно указать ensure_ascii=False, иначе вместо букв будут коды:</p>
''' + ex('''from json import dumps

entry = {"handler": "greet", "params": {"name": "Алиса"}, "response": [200, "Привет!"]}
print(dumps(entry))
print(dumps(entry, ensure_ascii=False))''') + '''
<p>Обрати внимание, что кортеж (200, "Привет!") превращается в JSON-список. Именно такие записи придут тебе на третьем этапе.</p>

<h3>Этап 3: анализ логов</h3>
<p>Записи журнала лежат построчно в формате JSON. Каждую строку превращаем обратно в словарь функцией <code>loads</code>. Потом отбираем нужные записи, считаем и выводим. Здесь пригодятся лямбда-функции вместе с map, filter и max. Недостающая часть это счётчик: словарь, в котором при первом обращении к ключу значение создаётся автоматически. Для этого в модуле collections есть [[defaultdict|defaultdict]]:</p>
''' + ex('''from collections import defaultdict

tasks = ["Snake", "Queens", "Snake", "TwoSum", "Snake", "Queens"]
counts = defaultdict(int)
for t in tasks:
    counts[t] += 1

print(dict(counts))
print(dict(sorted(counts.items())))
best = max(counts.items(), key=lambda item: item[1])
print(best)
print(f"Самая популярная: '{best[0]}', попыток: {best[1]}")''') + '''
<p>Обычный словарь на строке <code>counts[t] += 1</code> выдал бы KeyError для нового ключа. Для defaultdict(int) отсутствующее значение считается нулём. Функция max с параметром key сравнивает элементы по заданному признаку. Здесь это второй элемент пары, то есть количество.</p>
<p>Ещё раз посмотрим, как получить уникальных пользователей: множество убирает повторы, sorted упорядочивает, а join склеивает через запятую:</p>
''' + ex('''from json import loads

lines = [
    '{"handler": "attempt_handler", "params": {"name": "Max", "task": "Snake"}, "response": [200, "ok"]}',
    '{"handler": "user_handler", "params": {"name": "Ivan"}, "response": [200, "Hello, Ivan!"]}',
    '{"handler": "attempt_handler", "params": {"name": "Alex", "task": "Snake"}, "response": [200, "ok"]}',
    '{"handler": "attempt_handler", "params": {"name": "Max", "task": "Queens"}, "response": [200, "ok"]}',
]
logs = map(lambda line: loads(line), lines)
attempts = list(filter(lambda log: log["handler"] == "attempt_handler", logs))
users = sorted(set(map(lambda log: log["params"]["name"], attempts)))
print(len(attempts), len(users))
print(", ".join(users))''') + '''
<p>В реальном сервисе логи лежат в файле app.log. Но чтобы нам было проще проверять программу на разных данных, в заданиях строки журнала будут поступать на ввод построчно: читай их из sys.stdin, как в теме про потоковый ввод. Остальное остаётся тем же.</p>
'''
    th2 = th('Проект: условие и инструменты', terms2, body2)

    fl2 = fl('Вопросы: проект', [
        qo('Что выведет программа?', '''request = "GET /user?name=John"
method, path = request.split()
print(path.split("?")[0])''', ['/user', 'GET', 'name=John'], 'Строка разрезана по пробелу на метод и путь. Путь "/user?name=John" разрезан по знаку вопроса: слева маршрут /user, справа параметры.'),
        qo('Что выведет программа?', '''query = "name=Max&task=Snake"
params = {}
for pair in query.split("&"):
    key, value = pair.split("=")
    params[key] = value
print(params["task"])''', ['Snake', 'Max', 'task'], 'Запрос разрезан на пары по знаку &, пары по знаку =. Получился словарь {"name": "Max", "task": "Snake"}, и params["task"] равно "Snake".'),
        qo('Что выведет программа?', '''def a():
    return 1

def router(path):
    return a

print(router("/x")())''', ['1', 'a', 'None'], 'router возвращает саму функцию a, а скобки в router("/x")() её вызывают. Результат вызова 1.'),
        q('Чем отличается router("/") от router("/")()?', 'Первое даёт ручку, второе вызывает её', ['Ничем, это одно и то же', 'Первое ошибка, второе нет', 'Первое вызывает ручку, второе нет'], 'router("/") возвращает функцию-ручку. Вторые скобки вызывают эту функцию, и мы получаем её результат.'),
        qo('Что выведет программа?', '''def auth(func):
    def w(params):
        if "name" not in params:
            return 403, "Forbidden"
        return func(params)
    return w

@auth
def h(params):
    return 200, "ok"

print(h({"task": "x"}))''', ['(403, \'Forbidden\')', "(200, 'ok')", 'None'], 'В параметрах нет name, поэтому обёртка не вызывает h и сразу возвращает пару (403, "Forbidden").'),
        qo('Что выведет программа?', '''from json import dumps
print(dumps({"a": [1, "б"]}, ensure_ascii=False))''', ['{"a": [1, "б"]}', '{"a": [1, "\\u0431"]}', "{'a': [1, 'б']}"], 'dumps делает JSON: строки в двойных кавычках, кортежи и списки как списки. Параметр ensure_ascii=False оставляет русскую букву как есть.'),
        qo('Что выведет программа?', '''from json import loads
d = loads('{"x": [1, 2, 3]}')
print(d["x"][1])''', ['2', '1', 'x'], 'Строка превращена в словарь, d["x"] это список [1, 2, 3], а индекс 1 даёт второй элемент.'),
        qo('Что выведет программа?', '''from collections import defaultdict
c = defaultdict(int)
for w in "abca":
    c[w] += 1
print(c["a"], c["z"])''', ['2 0', '2 1', 'Ошибка'], 'Буква a встретилась дважды. Для отсутствующего ключа z defaultdict(int) создаёт значение 0 (и не выдаёт KeyError).'),
        qo('Что выведет программа?', '''d = {"x": 3, "y": 7, "z": 5}
print(max(d.items(), key=lambda p: p[1])[0])''', ['y', '7', 'z'], 'Пары сравниваются по второму элементу (значению), максимальное 7 у пары ("y", 7). Индекс [0] берёт из пары ключ.'),
        q('Зачем в декораторах логов нужен @wraps(func)?', 'Чтобы сохранить имя ручки при цепочке декораторов', ['Чтобы ускорить сервер', 'Чтобы ручка не вызывалась', 'Чтобы запросы шифровались'], 'Без wraps вместо имени ручки в журнал попало бы wrapper. С wraps декоратор передаёт имя исходной функции дальше по цепочке.'),
    ])

    # ============ Задания ============
    s1 = ('import sys\n' + H_ALL + '\n' + ROUTER + '''

# WSGI-сервер (генератор): ЭТУ ФУНКЦИЮ НУЖНО РЕАЛИЗОВАТЬ
def wsgi_server():
    """Обрабатывает запросы и возвращает каждый из ответов через yield"""
    request = yield None  # запуск генератора, приём первого запроса app.send(None)
    while True:
        # Здесь надо написать обработку request и вызов нужной ручки для получения response
        request = yield response


# Имитация работы сервера
app = wsgi_server()
app.send(None)

for request in sys.stdin:
    print(app.send(request))''')
    sol1 = ('import sys\n' + H_ALL + '\n' + ROUTER + '\n' + SERVER_OK + '''

# Имитация работы сервера
app = wsgi_server()
app.send(None)

for request in sys.stdin:
    print(app.send(request))''')
    t1 = task('Этап 1. WSGI-сервер как генератор. В редакторе уже лежит шаблон: ручки, функция router и имитация работы сервера. Допиши только функцию-генератор wsgi_server(): она получает запрос строкой вида «метод маршрут?параметры», разбирает его, находит ручку функцией router, вызывает её с параметрами (словарём) и отдаёт результат через yield. Запросы приходят на ввод по одному в строке. На вывод шаблон печатает ответы.',
              'Внутри while True: 1) method, path = request.split()[:2]. 2) params = {}; если "?" in path, то query = path.split("?")[1], потом for pair in query.split("&"): key, value = pair.split("="); params[key] = value. 3) handler = router(path), response = handler(params). Последняя строка шаблона request = yield response уже на месте.',
              sol1,
              ['POST /attempt?name=Dima&task=1\nGET /login\nGET /\nGET /', 'GET /user?name=Sveta\nGET /progress\nGET /unknown', 'POST /attempt?name=Maria&task=1\nGET /profile\nGET /user?name=Sveta', 'GET /\nGET /admin\nGET /user?name=John\nGET /unknown\nPOST /attempt?name=Alex&task=queens\nGET /attempt?name=Vasya&task=snake'],
              exp={'POST /attempt?name=Dima&task=1\nGET /login\nGET /\nGET /': "(200, \"Good try, Dima! Your attempt on task '1' is accepted!\")\n(404, 'Not Found')\n(200, 'Home Page')\n(200, 'Home Page')",
                   'GET /user?name=Sveta\nGET /progress\nGET /unknown': "(200, 'Hello, Sveta!')\n(404, 'Not Found')\n(404, 'Not Found')"},
              starter=s1)

    s2 = ('import sys\nfrom functools import wraps\nfrom json import dumps\n\n\n# ЭТИ ДЕКОРАТОРЫ НУЖНО НАПИСАТЬ\ndef require_auth(func):\n    """Декоратор проверки авторизации"""\n    pass\n\n\ndef log_call(func):\n    """Декоратор логирования"""\n    pass\n\n\n# Ручки для разных маршрутов\n' + _decorated_handlers() + '\n' + ROUTER + '\n\n# Сервер из первого этапа уже готов\n' + SERVER_OK + '''

# Имитация работы сервера
app = wsgi_server()
app.send(None)

for request in sys.stdin:
    app.send(request)''')
    sol2 = ('import sys\nfrom functools import wraps\nfrom json import dumps\n\n' + DECOR_OK + '\n\n# Ручки для разных маршрутов\n' + _decorated_handlers() + '\n' + ROUTER + '\n' + SERVER_OK + '''

app = wsgi_server()
app.send(None)

for request in sys.stdin:
    app.send(request)''')
    t2 = task('Этап 2. Декораторы: авторизация и логи. Шаблон: ручки уже обёрнуты декораторами (@log_call, а у user_handler и attempt_handler ещё и @require_auth), сервер из первого этапа готов. Допиши два декоратора. require_auth: если в params нет ключа "name", вернуть (403, "Forbidden"), иначе выполнить ручку. log_call: вызвать ручку и напечатать одной строкой JSON-запись {"handler": имя ручки, "params": параметры, "response": ответ}, а ответ вернуть. Ответы сервер теперь не печатает: на экране только логи. Имя функции берётся через func.__name__, не забудь @wraps.',
              'require_auth: def wrapper(params): if "name" not in params: return 403, "Forbidden"; иначе return func(params). log_call: result = func(params); print(dumps({"handler": func.__name__, "params": params, "response": result})); return result. В обоих декораторах поставь @wraps(func) над wrapper, иначе в логе будет «wrapper». Русских букв в тестах нет, ensure_ascii не нужен.',
              sol2,
              ['GET /unknown\nGET /\nPOST /attempt?name=Anna&task=Fibonacci\nGET /stats', 'GET /admin\nPOST /attempt?task=CountWords\nGET /admin\nGET /\nGET /settings', 'GET /\nGET /courses\nGET /unknown\nGET /user?name=Anna\nPOST /attempt?task=ReverseString\nGET /unknown', 'POST /attempt?name=Max&task=Frogs\nPOST /user?name=Mari&group=158\nPOST /attempt?nam=Pasha\nPOST /user?nam=Sasha&group=104'],
              exp={'GET /unknown\nGET /\nPOST /attempt?name=Anna&task=Fibonacci\nGET /stats': '{"handler": "not_found_handler", "params": {}, "response": [404, "Not Found"]}\n{"handler": "home_handler", "params": {}, "response": [200, "Home Page"]}\n{"handler": "attempt_handler", "params": {"name": "Anna", "task": "Fibonacci"}, "response": [200, "Good try, Anna! Your attempt on task \'Fibonacci\' is accepted!"]}\n{"handler": "not_found_handler", "params": {}, "response": [404, "Not Found"]}'},
              starter=s2)

    ts1 = ts('Этапы 1 и 2: сервер и декораторы', [t1, t2])

    sol3 = '''import sys
from json import loads
from collections import defaultdict

lines = sys.stdin.read().split("\\n")
lines_to_dicts = map(lambda line: loads(line), filter(lambda line: line.strip(), lines))

attempt_logs = list(filter(lambda log: log["handler"] == "attempt_handler", lines_to_dicts))
unique_users = sorted(set(map(lambda log: log["params"]["name"], attempt_logs)))

task_counts = defaultdict(int)
for log in attempt_logs:
    task_counts[log["params"]["task"]] += 1

most_popular_task = max(task_counts.items(), key=lambda item: item[1])

print("Analytics Results:")
print(f"Unique users who solved tasks: {len(unique_users)}")
print(f"Unique users list: {', '.join(unique_users)}")
print(f"Task popularity: {dict(sorted(task_counts.items()))}")
print(f"Most popular task: '{most_popular_task[0]}' with {most_popular_task[1]} attempts")'''
    s3 = '''import sys
from json import loads
from collections import defaultdict

# Логи приходят построчно в sys.stdin (в сервисе это был бы файл app.log).
# Каждая строка JSON-запись вида {"handler": ..., "params": ..., "response": ...}.
'''
    A = [("Max", "Snake"), ("Ivan", "Queens"), ("Max", "TwoSum"), ("Alex", "Queens"), ("Mari", "Parenthesis"), ("Max", "Parenthesis"), ("Alex", "Snake"), ("Ivan", "Snake")]
    B = [("Maria", "SumDigits"), ("Oleg", "SumDigits"), ("Alex", "MergeSorted"), ("Pavel", "SumDigits"), ("Pavel", "FizzBuzz"), ("Anna", "FizzBuzz"), ("Alex", "SumDigits"), ("Elena", "SumDigits")]
    C = [("Alex", "BracketCheck"), ("Kirill", "TwoSum"), ("Nikita", "CountWords"), ("Ivan", "TwoSum"), ("Anna", "CountWords"), ("Kirill", "FlattenList"), ("Anna", "CountWords"), ("Alex", "CountWords"), ("Nikita", "TwoSum"), ("Dima", "CountWords"), ("Maria", "BracketCheck")]
    D = [("Pavel", "Queens"), ("Yulia", "SumDigits"), ("Pavel", "LongestWord"), ("Oleg", "SortLetters"), ("Mari", "Queens"), ("Yulia", "TwoSum"), ("Sveta", "Queens"), ("Mari", "Queens"), ("Sveta", "TwoSum"), ("Ivan", "Queens")]
    E = [("Zed", "B"), ("Amy", "A"), ("Zed", "A"), ("Amy", "A"), ("Zed", "A")]
    tests = ['\n'.join(_logs(A, ['Ivan', 'Mari'])), '\n'.join(_logs(B)), '\n'.join(_logs(C)), '\n'.join(_logs(D)), '\n'.join(_logs(E, ['Bob']))]
    p1 = pj('Создание ASGI/WSGI-сервера',
            'Этап 3. Аналитика логов. Сервер уже работает и пишет журнал. Прочитай записи журнала (строки JSON поступают на ввод, по одной на строку) и выведи сводку по попыткам решить задачи (записи ручки attempt_handler; остальные записи пропускай). Формат строго такой: «Analytics Results:», затем «Unique users who solved tasks: N» (сколько разных пользователей), «Unique users list: имена через запятую с пробелом в лексикографическом порядке», «Task popularity: словарь {задача: число попыток}, ключи по алфавиту» и «Most popular task: \'задача\' with N attempts». Самая популярная задача всегда единственная. Попытки без имени пользователя в данных не встречаются.',
            'Шаги: 1) Считай все строки ввода и преврати каждую в словарь: map(lambda line: loads(line), ...). Пустые строки отфильтруй. 2) Оставь записи ручки attempt_handler: filter(lambda log: log["handler"] == "attempt_handler", ...). 3) Пользователи: sorted(set(map(lambda log: log["params"]["name"], attempt_logs))). 4) Попытки по задачам считай через defaultdict(int): task_counts[log["params"]["task"]] += 1. 5) Самая популярная: max(task_counts.items(), key=lambda item: item[1]). 6) Выведи результат в точности в нужном формате; словарь для вывода: dict(sorted(task_counts.items())).',
            sol3, tests, bonus=100, starter=s3,
            exp={tests[0]: "Analytics Results:\nUnique users who solved tasks: 4\nUnique users list: Alex, Ivan, Mari, Max\nTask popularity: {'Parenthesis': 2, 'Queens': 2, 'Snake': 3, 'TwoSum': 1}\nMost popular task: 'Snake' with 3 attempts",
                 tests[1]: "Analytics Results:\nUnique users who solved tasks: 6\nUnique users list: Alex, Anna, Elena, Maria, Oleg, Pavel\nTask popularity: {'FizzBuzz': 2, 'MergeSorted': 1, 'SumDigits': 5}\nMost popular task: 'SumDigits' with 5 attempts",
                 tests[2]: "Analytics Results:\nUnique users who solved tasks: 7\nUnique users list: Alex, Anna, Dima, Ivan, Kirill, Maria, Nikita\nTask popularity: {'BracketCheck': 2, 'CountWords': 5, 'FlattenList': 1, 'TwoSum': 3}\nMost popular task: 'CountWords' with 5 attempts",
                 tests[3]: "Analytics Results:\nUnique users who solved tasks: 6\nUnique users list: Ivan, Mari, Oleg, Pavel, Sveta, Yulia\nTask popularity: {'LongestWord': 1, 'Queens': 5, 'SortLetters': 1, 'SumDigits': 1, 'TwoSum': 2}\nMost popular task: 'Queens' with 5 attempts"})

    return topic('Веб-сервер своими руками', 'запросы и маршруты, декораторы-обработчики, сервер-генератор, логи в JSON, аналитика', [th1, fl1, th2, fl2, ts1, p1])
