import json
from dsl import *

# Нора после «Наследование»: Pydantic — проверка данных по описанию модели. Пакет есть в Pyodide (докачивается при первом import),
# в сборке — тот же pydantic 2.12.5 в окружении itp-tools. Две теории: модель и ошибки (BaseModel, приведение типов, ValidationError
# с путём к полю, model_validate/model_validate_json/model_dump, вложенные модели); свои правила (Field с границами, field_validator).
# Ответы «сервера» лежат в файлах — запросы к серверам на этом месте ещё не пройдены. Мини-проект — импорт каталога игр.

RESP = ('{"name": "Ash", "level": 12, "hp": 87.5}\n{"name": "Lucy", "level": "7"}\n{"name": "V", "level": "семь", "hp": 100}\n'
        '{"level": 3}\n{"name": "Rebecca", "level": 30, "guild": "Edgerunners", "hp": "много"}\n')
GAMES = json.dumps([
    {'title': 'Stardew Valley', 'year': 2016, 'rating': 9.4, 'tags': ['ферма', 'уют']},
    {'title': 'Elden Ring', 'year': '2022', 'rating': 9.6, 'tags': ['souls', 'открытый мир']},
    {'title': '', 'year': 2020, 'rating': 7.0, 'tags': []},
    {'title': 'Hotline Miami', 'year': 2012, 'rating': 11, 'tags': ['экшен']},
    {'title': 'Metro Exodus', 'year': 2019, 'rating': 8.7},
    {'title': 'Minecraft', 'year': 2011, 'rating': '9.0', 'tags': 'песочница'},
    {'title': 'The Binding of Isaac', 'year': 1985, 'rating': 9.1, 'tags': ['рогалик']},
    {'title': 'MiSide', 'year': 2024, 'rating': 8.9, 'tags': ['хоррор', 'аниме']},
], ensure_ascii=False, indent=1)


def th_model():
    terms = [
        ('pydantic', 'Библиотека проверки данных: описываешь модель — какие поля и каких типов, — и Pydantic проверяет и приводит данные. '
                     'На ней построены FastAPI и многие SDK к API нейросетей.'),
        ('BaseModel', 'pydantic.BaseModel — класс-основа: наследуешься от него и пишешь поля с подсказками типов, name: str, level: int = 1.'),
        ('model_validate', 'Модель.model_validate(словарь) — проверить словарь и создать объект модели или вызвать ValidationError.'),
        ('model_validate_json', 'Модель.model_validate_json(текст) — то же сразу из JSON-строки: разбор и проверка в одном вызове.'),
        ('model_dump', 'объект.model_dump() — обратно в словарь; model_dump_json() — в JSON-строку.'),
        ('ValidationError', 'Ошибка Pydantic: данные не подходят под модель. Внутри — все найденные проблемы, а не только первая.'),
        ('errors', 'ошибка.errors() — список словарей по каждой проблеме: loc — путь к полю (кортеж), type — код ошибки (missing, int_parsing…), '
                   'msg — описание по-английски.'),
        ('pydantic.ValidationError', 'Класс ошибки проверки — его ловят в except.'),
    ]
    body = (
        '<p>Данные снаружи — от сервера, из файла, от пользователя — бывают кривыми: число пришло строкой, поле забыли, вместо уровня — «семь». '
        'Проверять всё вручную через if — долго и скучно. [[pydantic|Pydantic]] делает это по описанию: наследуешь класс от [[BaseModel]], пишешь поля '
        'с типами — и получаешь проверку. Это сейчас стандарт для структур данных в Python.</p>'
        '<p>Программы в ИТП в интернет не ходят, но само приложение при первом import pydantic скачивает пакет (как numpy) и запоминает — нужно, чтобы телефон или компьютер был онлайн один раз. Офлайн до первой загрузки будет ModuleNotFoundError.</p>'
        + ex('from pydantic import BaseModel\n\n\nclass Player(BaseModel):\n    name: str\n    level: int\n    hp: float = 100\n    guild: str | None = None\n\n\n'
             'p = Player.model_validate({"name": "Ash", "level": "12"})\nprint(p)\nprint(p.level + 1, p.model_dump())') +
        '<p>Строку «12» Pydantic сам привёл к числу: это безопасно, смысл не потерян. А вот «семь» числом не станет — будет [[ValidationError]], '
        'и в нём сказано, где именно проблема. [[errors]] даёт список: путь к полю, код и описание:</p>'
        + ex('from pydantic import BaseModel, ValidationError\n\n\nclass Player(BaseModel):\n    name: str\n    level: int\n\n\ntry:\n'
             '    Player.model_validate({"level": "семь"})\nexcept ValidationError as e:\n    for err in e.errors():\n        print(err["loc"], err["type"])') +
        '<p>Обе ошибки найдены сразу. JSON-текст проверяет [[model_validate_json]], обратно в словарь — [[model_dump]]. Модели вкладываются '
        'друг в друга, и путь к ошибке показывает всю дорогу — до номера элемента в списке:</p>'
        + ex('from pydantic import BaseModel, ValidationError\n\n\nclass Item(BaseModel):\n    name: str\n    qty: int\n\n\nclass Inventory(BaseModel):\n'
             '    owner: str\n    items: list[Item]\n\n\ntext = \'{"owner": "Tarnished", "items": [{"name": "зелье", "qty": 3}, {"name": "руна", "qty": "x"}]}\'\n'
             'try:\n    Inventory.model_validate_json(text)\nexcept ValidationError as e:\n    print(e.errors()[0]["loc"])') +
        '<p>Ошибка во втором предмете (номер 1), поле qty. Без Pydantic такая находка — полчаса print-ов. В итоговых проектах будет '
        'dataclass — он только хранит поля, а Pydantic ещё и проверяет их.</p>'
    )
    return th('Модель и ошибки', terms, body)


def fl_model():
    return fl('Модель и ошибки', [
        qo('Что выведет программа?', 'from pydantic import BaseModel\n\n\nclass P(BaseModel):\n    level: int\n\n\nprint(P.model_validate({"level": "5"}).level * 2)',
           ['55', 'Ошибка', '"5""5"'], '«5» приведено к int, 5 · 2 = 10.'),
        q('Что лежит в err["loc"]?', 'Путь к полю с ошибкой', ['Номер строки в программе', 'Текст исправленного значения'],
          'Например, ("items", 1, "qty").'),
        q('В данных три ошибки. Сколько их будет в e.errors()?', 'Три — Pydantic собирает все', ['Одна — первая', 'Ноль: ошибки печатаются сразу'],
          'Не надо исправлять по одной и перезапускать.'),
    ])


def code_model():
    return ts('Модель и ошибки', [
        task('Профили игроков. В файле players.jsonl по JSON-объекту в строке — так их прислал сервер. Модель: name — строка, level — целое, hp — дробное '
             '(по умолчанию 100), guild — строка или None (по умолчанию None). Для каждой строки (N — номер с 1) выведи «N. ИМЯ: ур. L, hp H, гильдия G» (hp — как печатает Python дробное: 100.0) '
             '(вместо None — «нет») или, если данные не прошли проверку, «N. ошибка: поле/код, поле/код» — по всем ошибкам, где поле — последний '
             'элемент loc. Затем «Принято: K из M». На вход подаётся минимальный уровень: принятые игроки ниже него не выводятся (но считаются).',
             'Player.model_validate_json(line.strip()) в try … except ValidationError as e. Части ошибки: err["loc"][-1], err["type"].',
             'from pydantic import BaseModel, ValidationError\n\n\nclass Player(BaseModel):\n    name: str\n    level: int\n    hp: float = 100\n    guild: str | None = None\n\n\n'
             'min_level = int(input())\nok = total = 0\nfor n, line in enumerate(open("players.jsonl", encoding="utf-8"), 1):\n    total += 1\n    try:\n'
             '        p = Player.model_validate_json(line.strip())\n    except ValidationError as e:\n'
             '        print(f"{n}. ошибка: " + ", ".join(f"{err[\'loc\'][-1]}/{err[\'type\']}" for err in e.errors()))\n        continue\n    ok += 1\n'
             '    if p.level >= min_level:\n        print(f"{n}. {p.name}: ур. {p.level}, hp {p.hp}, гильдия {p.guild or \'нет\'}")\nprint(f"Принято: {ok} из {total}")',
             ['1', '10'], files={'players.jsonl': RESP}),
        task('Где именно. На вход подаётся одна строка — JSON инвентаря, который прислал сервер. Модель Item: name — строка, qty — целое; Inventory: owner — '
             'строка, items — список Item. Если всё верно — выведи «ВЛАДЕЛЕЦ: N предм., всего Q шт.». Иначе для каждой ошибки — путь через точку '
             '(«items.1.qty») и через пробел код ошибки; если JSON вообще не разобрался, путь пустой — выводи «(весь ответ)».',
             'Путь: ".".join(str(x) for x in err["loc"]) or "(весь ответ)".',
             'from pydantic import BaseModel, ValidationError\n\n\nclass Item(BaseModel):\n    name: str\n    qty: int\n\n\nclass Inventory(BaseModel):\n    owner: str\n'
             '    items: list[Item]\n\n\ntry:\n    inv = Inventory.model_validate_json(input())\nexcept ValidationError as e:\n    for err in e.errors():\n'
             '        print(".".join(str(x) for x in err["loc"]) or "(весь ответ)", err["type"])\nelse:\n'
             '    print(f"{inv.owner}: {len(inv.items)} предм., всего {sum(i.qty for i in inv.items)} шт.")',
             ['{"owner": "Steve", "items": [{"name": "алмаз", "qty": 3}, {"name": "кирка", "qty": "1"}]}',
              '{"owner": "Isaac", "items": [{"name": "слеза", "qty": "много"}, {"qty": 2}]}', '{"items": 5}', '{"owner": "Artyom", "items": [}']),
    ])


def th_rules():
    terms = [
        ('Field', 'pydantic.Field(...) — описание поля с правилами: gt/ge/lt/le — границы числа, min_length/max_length — длина, default — '
                  'значение по умолчанию. Пишется после = в поле модели.'),
        ('pydantic.Field', 'Функция описания поля модели — импортируется из pydantic.'),
        ('field_validator', '@field_validator("поле") над методом класса — своя проверка поля. Метод получает значение и возвращает его '
                            '(можно исправленное) или вызывает ValueError с понятным текстом.'),
        ('pydantic.field_validator', 'Декоратор своей проверки поля — импортируется из pydantic.'),
        ('classmethod', '@classmethod — метод класса: первым получает сам класс (cls), а не объект. Валидаторы Pydantic пишут так.'),
    ]
    body = (
        '<p>Типа мало: уровень −5 — целое число, но бред. Правила пишут через [[Field]]: границы чисел, длину строк:</p>'
        + ex('from pydantic import BaseModel, Field, ValidationError\n\n\nclass Lot(BaseModel):\n    title: str = Field(min_length=2, max_length=30)\n'
             '    price: int = Field(gt=0)\n    qty: int = Field(default=1, ge=1, le=99)\n\n\nfor data in [{"title": "Меч", "price": 500}, {"title": "Щ", "price": 0, "qty": 120}]:\n'
             '    try:\n        print(Lot.model_validate(data))\n    except ValidationError as e:\n        for err in e.errors():\n            print(" ", err["loc"][0], err["type"])') +
        '<p>Если правило сложнее границ — пишут свою проверку, [[field_validator]]. Это метод класса ([[classmethod]]) с декоратором: получает '
        'значение, может его поправить и вернуть, а если оно никуда не годится — вызывает ValueError. Текст ошибки попадёт в msg:</p>'
        + ex('from pydantic import BaseModel, ValidationError, field_validator\n\n\nclass Account(BaseModel):\n    nick: str\n\n    @field_validator("nick")\n'
             '    @classmethod\n    def clean_nick(cls, value):\n        value = value.strip().lower()\n        if not value.isalnum():\n'
             '            raise ValueError("только буквы и цифры")\n        return value\n\n\nprint(Account.model_validate({"nick": "  NetRunner77 "}).nick)\ntry:\n'
             '    Account.model_validate({"nick": "bad nick!"})\nexcept ValidationError as e:\n    print(e.errors()[0]["msg"])') +
        '<p>Модель — договор о данных в одном месте: что пришло снаружи и прошло проверку, дальше в программе можно не проверять.</p>'
    )
    return th('Свои правила', terms, body)


def fl_rules():
    return fl('Свои правила', [
        q('Как в Field записать «больше нуля»?', 'gt=0', ['ge=0', 'min=0'], 'gt — greater than, ge — больше или равно.'),
        q('Что делает field_validator, когда значение плохое?', 'Вызывает ValueError с понятным текстом', ['Возвращает False',
          'Печатает предупреждение и идёт дальше'], 'Pydantic превратит его в ошибку проверки.'),
        q('Можно ли в field_validator исправить значение?', 'Да: вернуть исправленное', ['Нет, только проверить', 'Только через print'],
          'Возвращённое значение и попадёт в поле.'),
    ])


def code_rules():
    return ts('Свои правила', [
        task('Заявка на турнир. На вход подаются строки JSON, последняя — «конец». Модель Entry: team — строка от 3 до 20 символов; players — целое '
             'от 2 до 5; nick_captain — строка, своя проверка: убрать пробелы по краям, перевести в нижний регистр, а если в нике не только буквы, '
             'цифры и «_», — ValueError «ник: только буквы, цифры и _». Для верной заявки выведи «N. TEAM (P игр.), капитан NICK», для неверной — '
             '«N. отклонена: поле — msg» по каждой ошибке (msg — как есть). В конце — «Принято: K».',
             'Ник без «_» и проверь isalnum: value.replace("_", "").isalnum().',
             'from pydantic import BaseModel, Field, ValidationError, field_validator\n\n\nclass Entry(BaseModel):\n    team: str = Field(min_length=3, max_length=20)\n'
             '    players: int = Field(ge=2, le=5)\n    nick_captain: str\n\n    @field_validator("nick_captain")\n    @classmethod\n    def clean(cls, value):\n'
             '        value = value.strip().lower()\n        if not value.replace("_", "").isalnum():\n            raise ValueError("ник: только буквы, цифры и _")\n'
             '        return value\n\n\nok = n = 0\nwhile True:\n    line = input()\n    if line == "конец":\n        break\n    n += 1\n    try:\n'
             '        e = Entry.model_validate_json(line)\n    except ValidationError as err:\n        print(f"{n}. отклонена: " + "; ".join(f"{x[\'loc\'][0]} — {x[\'msg\']}" for x in err.errors()))\n'
             '        continue\n    ok += 1\n    print(f"{n}. {e.team} ({e.players} игр.), капитан {e.nick_captain}")\nprint(f"Принято: {ok}")',
             ['{"team": "Edgerunners", "players": 4, "nick_captain": " David_M "}\n{"team": "AB", "players": 7, "nick_captain": "x"}\n'
              '{"team": "Night City", "players": 3, "nick_captain": "Lucy!"}\nконец', '{"team": "Metro", "players": "2", "nick_captain": "Artyom"}\nконец']),
        task('Исправь модель. В шаблоне модель Order для ответа магазина: id — целое больше 0, item — непустая строка, price — дробное не меньше 0, '
             'count — целое от 1 до 100 (по умолчанию 1). Программа проверяет заказы из ввода и печатает итог. Модель написана с ошибками: правила '
             'не совпадают с описанием. Исправь только модель, чтобы вывод стал верным.',
             'Сравни каждое поле с описанием: gt и ge, min_length, границы count и значение по умолчанию.',
             'from pydantic import BaseModel, Field, ValidationError\n\n\nclass Order(BaseModel):\n    id: int = Field(gt=0)\n    item: str = Field(min_length=1)\n'
             '    price: float = Field(ge=0)\n    count: int = Field(default=1, ge=1, le=100)\n\n\ntotal = 0\nwhile True:\n    line = input()\n    if line == "конец":\n        break\n'
             '    try:\n        o = Order.model_validate_json(line)\n    except ValidationError as e:\n        print("брак:", ", ".join(str(x["loc"][0]) for x in e.errors()))\n'
             '        continue\n    total += o.price * o.count\n    print(f"#{o.id} {o.item} × {o.count}")\nprint(f"Сумма: {total:.2f}")',
             ['{"id": 1, "item": "мышь", "price": 990}\n{"id": 0, "item": "", "price": -5, "count": 0}\n{"id": 2, "item": "коврик", "price": 0, "count": 100}\nконец',
              '{"id": 3, "item": "клавиатура", "price": 2500.5, "count": 2}\n{"id": 4, "item": "кабель", "price": 150, "count": 101}\nконец'],
             starter='from pydantic import BaseModel, Field, ValidationError\n\n\nclass Order(BaseModel):\n    id: int = Field(ge=0)\n    item: str\n'
                     '    price: float = Field(gt=0)\n    count: int = Field(default=0, ge=1, le=99)\n\n\ntotal = 0\nwhile True:\n    line = input()\n    if line == "конец":\n        break\n'
                     '    try:\n        o = Order.model_validate_json(line)\n    except ValidationError as e:\n        print("брак:", ", ".join(str(x["loc"][0]) for x in e.errors()))\n'
                     '        continue\n    total += o.price * o.count\n    print(f"#{o.id} {o.item} × {o.count}")\nprint(f"Сумма: {total:.2f}")',
             fix=True),
    ])


def project():
    return pj('Каталог игр',
              'Сервер прислал каталог игр — games.json, список объектов. Модель Game: title — строка от 1 символа; year — целое от 1990 до 2026; rating — '
              'дробное от 0 до 10; tags — список строк (по умолчанию пустой). Своя проверка title: обрезать пробелы по краям. Проверь каждую запись и '
              'выведи отчёт. На вход подаётся команда:\n'
              '— «отчёт» → «Принято: K из N», затем по каждой отклонённой «#НОМЕР (с 1): поле/код, поле/код» и «Чаще всего ломается: поле» — поле, '
              'которое встречается в ошибках чаще всех (при равенстве — первое по алфавиту);\n'
              '— «топ M» → M лучших принятых игр строками «RATING TITLE (YEAR)» (рейтинг — как печатает Python дробное: 9.0) по убыванию рейтинга (при равенстве — по названию);\n'
              '— «тег ТЕГ» → названия принятых игр с этим тегом через запятую с пробелом в порядке файла или «Нет игр с тегом ТЕГ».',
              'Список принятых — объекты Game; отклонённые — пары (номер, список ошибок)\n'
              'tags: list[str] = [] — Pydantic даёт каждому объекту свою копию значения по умолчанию\nСчётчик полей ошибок — Counter',
              'import json\nfrom collections import Counter\nfrom pydantic import BaseModel, Field, ValidationError, field_validator\n\n\nclass Game(BaseModel):\n'
              '    title: str = Field(min_length=1)\n    year: int = Field(ge=1990, le=2026)\n    rating: float = Field(ge=0, le=10)\n    tags: list[str] = []\n\n'
              '    @field_validator("title")\n    @classmethod\n    def strip_title(cls, value):\n        return value.strip()\n\n\n'
              'games, bad = [], []\nfor n, raw in enumerate(json.load(open("games.json", encoding="utf-8")), 1):\n    try:\n        games.append(Game.model_validate(raw))\n'
              '    except ValidationError as e:\n        bad.append((n, [(err["loc"][0], err["type"]) for err in e.errors()]))\n\ncmd = input().split(maxsplit=1)\n'
              'if cmd[0] == "отчёт":\n    print(f"Принято: {len(games)} из {len(games) + len(bad)}")\n    fields = Counter()\n    for n, errs in bad:\n'
              '        print(f"#{n}: " + ", ".join(f"{f}/{t}" for f, t in errs))\n        fields.update(f for f, t in errs)\n'
              '    print("Чаще всего ломается:", min(fields, key=lambda f: (-fields[f], f)))\nelif cmd[0] == "топ":\n'
              '    for g in sorted(games, key=lambda g: (-g.rating, g.title))[:int(cmd[1])]:\n        print(f"{g.rating} {g.title} ({g.year})")\nelse:\n'
              '    found = [g.title for g in games if cmd[1] in g.tags]\n    print(", ".join(found) if found else f"Нет игр с тегом {cmd[1]}")',
              ['отчёт', 'топ 3', 'тег аниме', 'тег шутер'], files={'games.json': GAMES})


def build():
    return topic('Pydantic: проверяем данные', 'модели, ошибки с адресом, свои правила', [
        th_model(), fl_model(), code_model(),
        th_rules(), fl_rules(), code_rules(),
        project(),
    ], opt=True)
