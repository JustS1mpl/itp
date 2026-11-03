import io
import json
from dsl import *

# Тема 29 «Итоговые проекты»: мессенджер и текстовая RPG. Каждый проект — три этапа (проекты «Мессенджер, этап N: …»,
# «RPG, этап N: …»); заготовка этапа — эталон прошлого этапа, так что этапы складываются в одну программу.
# Перед этапами — задачи-части. Эталоны этапов лежат обычными файлами в final/ — их можно запускать и править отдельно.
# Достижения «Связист» и «Герой подземелья» — за все этапы проекта (правило в build5.py по началу названия).


def src(name):
    return io.open('final/' + name, encoding='utf-8').read()


CHAT = {'_itp_servers.json': json.dumps({'chat.itp': {'collection': 'messages', 'users': [
    {'id': 1, 'author': 'Аня', 'text': 'Всем привет! Кто идёт в кино?', 'kind': 'TEXT'},
    {'id': 2, 'author': 'Борис', 'text': '@гость ты с нами?', 'kind': 'TEXT'},
    {'id': 3, 'author': '*', 'text': 'Вика теперь Zed', 'kind': 'SYSTEM'},
    {'id': 4, 'author': 'Zed', 'text': 'Я иду! Билеты взял', 'kind': 'TEXT'}]}}, ensure_ascii=False)}

DUNGEON = json.dumps({
    'start': 'вход', 'goal': 'сокровищница',
    'rooms': {
        'вход': {'desc': 'Сырой вход в пещеру.', 'exits': {'север': 'коридор'}, 'items': ['кинжал:оружие:2'], 'monster': None},
        'коридор': {'desc': 'Узкий коридор с факелами.', 'exits': {'юг': 'вход', 'восток': 'кладовая', 'север': 'зал'}, 'items': [],
                    'monster': 'крыса:8:3:0'},
        'кладовая': {'desc': 'Полки с пыльными банками.', 'exits': {'запад': 'коридор'},
                     'items': ['зелье:зелье:10', 'кольчуга:броня:3', 'меч:оружие:5'], 'monster': None},
        'зал': {'desc': 'Огромный зал, вдали блестит дверь.', 'exits': {'юг': 'коридор', 'север': 'сокровищница'}, 'items': [],
                'monster': 'гоблин:15:5:1'},
        'сокровищница': {'desc': 'Горы золота!', 'exits': {'юг': 'зал'}, 'items': [], 'monster': 'тролль:30:8:2'},
    }}, ensure_ascii=False, indent=2)


def th_data():
    terms = [
        ('dataclasses', 'Модуль с декоратором dataclass и функцией field — для классов-«записей» с полями.'),
        ('enum', 'Модуль с классом Enum — для перечислений: небольших наборов именованных констант.'),
        ('dataclass', 'Декоратор из модуля dataclasses: по списку полей с подсказками типов сам пишет __init__, __repr__ и __eq__.\n'
                      'Пример:\nfrom dataclasses import dataclass\n\n@dataclass\nclass Point:\n    x: int\n    y: int = 0\n\n'
                      'print(Point(3), Point(1, 2) == Point(1, 2))\nВывод:\nPoint(x=3, y=0) True'),
        ('field', 'field(default_factory=list) — значение по умолчанию, которое создаётся заново для каждого объекта: у каждого свой '
                  'пустой список. Написать просто = [] в dataclass нельзя — Python выдаст ошибку.'),
        ('Enum', 'Базовый класс перечисления — набора именованных констант: class Kind(Enum): WEAPON = "оружие". Kind.WEAPON.name — имя, '
                 '.value — значение, Kind("оружие") — элемент по значению.\n'
                 'Пример:\nfrom enum import Enum\n\nclass Color(Enum):\n    RED = "красный"\n    GREEN = "зелёный"\n\n'
                 'print(Color.RED.value, Color("зелёный").name, len(Color))\nВывод:\nкрасный GREEN 2'),
    ]
    body = (
        '<p>Это последняя тема: два больших проекта на всё, что было в курсе. Перед ними — два инструмента, которые сделают код '
        'проектов короче.</p>'
        '<h3>dataclass</h3>'
        '<p>Многие классы — просто «запись с полями»: сообщение, предмет, игрок. Писать для них <code>__init__</code>, '
        '<code>__repr__</code> и <code>__eq__</code> скучно. Декоратор [[dataclass]] делает это сам — достаточно перечислить поля '
        'с подсказками типов:</p>'
        + ex('from dataclasses import dataclass, field\n\n\n@dataclass\nclass Player:\n    nick: str\n    level: int = 1\n'
             '    items: list = field(default_factory=list)\n\n    def level_up(self):\n        self.level += 1\n\n\n'
             'p = Player("zed")\np.items.append("меч")\np.level_up()\nprint(p)\nprint(p == Player("zed", 2, ["меч"]), Player("аня"))') +
        '<p>Поля со значениями по умолчанию идут после полей без них. Для списка или словаря по умолчанию нужен [[field]] с '
        '<code>default_factory</code>: иначе все игроки делили бы один список на всех. Методы и property в dataclass пишут как обычно, '
        'наследовать тоже можно — наследник добавляет свои поля в конец:</p>'
        + ex('from dataclasses import dataclass\n\n\n@dataclass\nclass Creature:\n    name: str\n    hp: int\n\n\n@dataclass\nclass Hero(Creature):\n    level: int = 1\n\n\n'
             'print(Hero("Рыцарь", 30), Hero("Маг", 20, 5).level)') +
        '<h3>Enum</h3>'
        '<p>Виды предметов, типы сообщений, цвета светофора — это небольшой фиксированный набор значений. Можно хранить их строками, '
        'но опечатка <code>"оружеи"</code> молча испортит программу. [[Enum]] делает из набора отдельный тип, и опечатка в имени '
        'сразу даст ошибку:</p>'
        + ex('from enum import Enum\n\n\nclass Kind(Enum):\n    WEAPON = "оружие"\n    ARMOR = "броня"\n    POTION = "зелье"\n\n\n'
             'k = Kind.WEAPON\nprint(k.name, k.value, k == Kind.WEAPON)\nprint(Kind("зелье"), [x.value for x in Kind])\ntry:\n    Kind("лук")\nexcept ValueError as e:\n    print(e)') +
        '<p><code>Kind("зелье")</code> находит элемент по значению — удобно, когда значение пришло из файла или от сервера.</p>'
    )
    return th('dataclass и Enum', terms, body)


def fl_data():
    return fl('dataclass и Enum', [
        qo('Что выведет программа?', 'from dataclasses import dataclass\n\n@dataclass\nclass P:\n    x: int\n    y: int = 5\n\nprint(P(1))',
           ['P(1)', 'P(x=1)', '<P object>'], 'dataclass сам пишет __repr__ со всеми полями: P(x=1, y=5).'),
        q('Зачем в dataclass писать items: list = field(default_factory=list)?', 'Чтобы у каждого объекта был свой новый список',
          ['Чтобы список был отсортирован', 'Без field список нельзя менять'], 'default_factory вызывается заново для каждого объекта.'),
        qo('Что выведет программа?', 'from enum import Enum\n\nclass Light(Enum):\n    RED = "красный"\n    GREEN = "зелёный"\n\nprint(Light("красный").name)',
           ['красный', 'Light.RED', 'Ошибка'], 'Элемент нашёлся по значению, name — его имя: RED.'),
    ])


def code_data():
    return ts('dataclass и Enum', [
        task('Книжная полка. На вход подаются книги строками «Название;Автор;Страниц», последняя строка — «стоп». Опиши книгу через '
             'dataclass Book с полями title, author, pages. Выведи книги по убыванию числа страниц (при равенстве — по названию) '
             'строками «Название — Автор, N стр.», затем «Всего страниц: S».',
             '@dataclass\nclass Book:\n    title: str\n    author: str\n    pages: int\n'
             'Строку разрезай s.split(";"), страницы — int. Сортировка: sorted(books, key=lambda b: (-b.pages, b.title)).',
             'from dataclasses import dataclass\n\n\n@dataclass\nclass Book:\n    title: str\n    author: str\n    pages: int\n\n\nbooks = []\nwhile True:\n'
             '    s = input()\n    if s == "стоп":\n        break\n    title, author, pages = s.split(";")\n    books.append(Book(title, author, int(pages)))\n'
             'for b in sorted(books, key=lambda b: (-b.pages, b.title)):\n    print(f"{b.title} — {b.author}, {b.pages} стр.")\nprint(f"Всего страниц: {sum(b.pages for b in books)}")',
             ['Дюна;Герберт;704\nМастер и Маргарита;Булгаков;480\nМаленький принц;Сент-Экзюпери;96\nстоп', 'Нос;Гоголь;40\nШинель;Гоголь;40\nстоп']),
        task('Светофор. Опиши цвета через Enum Light: RED = «красный», YELLOW = «жёлтый», GREEN = «зелёный». После красного идёт '
             'зелёный, после зелёного — жёлтый, после жёлтого — красный. На вход подаются начальный цвет (по-русски) и число шагов n. '
             'Выведи n + 1 цветов по-русски через « → », начиная с начального. Если такого цвета нет — «Нет такого цвета».',
             'Порядок удобно хранить словарём: NEXT = {Light.RED: Light.GREEN, ...}.\nЦвет по значению — Light(text); неизвестный даст ValueError.',
             'from enum import Enum\n\n\nclass Light(Enum):\n    RED = "красный"\n    YELLOW = "жёлтый"\n    GREEN = "зелёный"\n\n\n'
             'NEXT = {Light.RED: Light.GREEN, Light.GREEN: Light.YELLOW, Light.YELLOW: Light.RED}\ntry:\n    light = Light(input())\nexcept ValueError:\n'
             '    print("Нет такого цвета")\nelse:\n    path = [light]\n    for _ in range(int(input())):\n        path.append(NEXT[path[-1]])\n'
             '    print(" → ".join(x.value for x in path))',
             ['красный\n3', 'жёлтый\n0', 'синий\n2']),
        task('Редкость лута. Опиши Enum Rarity: COMMON = 1, RARE = 3, LEGENDARY = 10 (значение — множитель цены) и dataclass '
             'Item с полями name, rarity и base_price. На вход подаются предметы «название редкость цена» до «стоп», редкость — '
             'имя элемента Enum (COMMON, RARE, LEGENDARY). Выведи «НАЗВАНИЕ (редкость) — ЦЕНА» по убыванию итоговой цены '
             '(base_price × множитель), редкость — именем строчными буквами.',
             'Элемент по имени — Rarity[name]. Итоговая цена — item.base_price * item.rarity.value; имя — item.rarity.name.lower().',
             'from dataclasses import dataclass\nfrom enum import Enum\n\n\nclass Rarity(Enum):\n    COMMON = 1\n    RARE = 3\n    LEGENDARY = 10\n\n\n'
             '@dataclass\nclass Item:\n    name: str\n    rarity: Rarity\n    base_price: int\n\n\nitems = []\nwhile True:\n    s = input()\n    if s == "стоп":\n        break\n'
             '    name, r, p = s.split()\n    items.append(Item(name, Rarity[r], int(p)))\nfor it in sorted(items, key=lambda i: -i.base_price * i.rarity.value):\n'
             '    print(f"{it.name} ({it.rarity.name.lower()}) — {it.base_price * it.rarity.value}")',
             ['меч COMMON 100\nкольцо LEGENDARY 20\nплащ RARE 50\nстоп', 'палка COMMON 1\nстоп']),
        task('Журнал заданий. Опиши dataclass Quest: title, reward (опыт) и steps — список шагов, по умолчанию пустой '
             '(через field), и done — сколько шагов выполнено, по умолчанию 0. Метод progress() возвращает «НАЗВАНИЕ: D/N», '
             'а если все шаги выполнены — «НАЗВАНИЕ: готово, +R опыта». У каждого задания свой список шагов.',
             'steps: list = field(default_factory=list) — иначе все задания делили бы один список. done: int = 0.',
             'from dataclasses import dataclass, field\n\n\n@dataclass\nclass Quest:\n    title: str\n    reward: int\n    steps: list = field(default_factory=list)\n'
             '    done: int = 0\n\n    def progress(self):\n        if self.done >= len(self.steps):\n            return f"{self.title}: готово, +{self.reward} опыта"\n'
             '        return f"{self.title}: {self.done}/{len(self.steps)}"',
             ['q = Quest("Урожай", 50, ["посадить", "полить", "собрать"])\nprint(q.progress())\nq.done = 3\nprint(q.progress())',
              'a = Quest("А", 1)\nb = Quest("Б", 2)\na.steps.append("шаг")\nprint(a.progress(), b.progress(), b.steps)', 'print(Quest("Сон", 5))'], tail=TL),
    ])


def th_msg():
    terms = [
        ('архитектура', 'Как программа поделена на части и как они связаны: данные (классы), действия над ними (функции), '
                        'ввод-вывод (главный цикл). Хорошая архитектура позволяет менять одну часть, не ломая остальные.'),
    ]
    body = (
        '<p>Первый проект — <b>мессенджер</b>: свой чат с никами, историей, поиском, статистикой и сервером. Он строится в три этапа, '
        'и каждый следующий начинается с кода предыдущего — он уже будет в редакторе:</p>'
        '<table><tr><th>Этап</th><th>Что добавляется</th></tr>'
        '<tr><td>1. Чат на одного</td><td>сообщения-объекты, ники, история, разбор команд</td></tr>'
        '<tr><td>2. Поиск и статистика</td><td>системные сообщения через Enum, поиск, упоминания, статистика авторов</td></tr>'
        '<tr><td>3. Сервер</td><td>сообщения живут на сервере: отправка, обновление, удаление своих, свои ошибки</td></tr></table>'
        '<p>[[архитектура]] у всех этапов одна: сообщение — dataclass <code>Message</code>, строка ввода превращается в пару '
        '«команда, аргумент» функцией <code>parse_command</code>, а главный цикл только читает строку и решает, что вызвать:</p>'
        + ex('def parse_command(line):\n    if line.startswith("/"):\n        parts = line[1:].split(" ", 1)\n        return parts[0], parts[1].strip() if len(parts) > 1 else ""\n'
             '    return "", line.strip()\n\n\nfor line in ["/ник Аня", "привет всем", "/история", "/найти   кино "]:\n    print(parse_command(line))') +
        '<p>Строка без косой черты — обычное сообщение: команда пустая, аргумент — текст. Так главный цикл остаётся коротким, '
        'а каждая команда — отдельной веткой или функцией. На третьем этапе ошибки команд удобно вызывать своим исключением '
        '<code>ChatError</code> и ловить в одном месте — в главном цикле.</p>'
        '<p>Сначала — три задачи-части: из них потом складываются этапы. Части можно решать в любом порядке, этапы — по очереди.</p>'
    )
    return th('Мессенджер: устройство', terms, body)


def fl_msg():
    return fl('Мессенджер: устройство', [
        qo('Что выведет программа?', 'def parse_command(line):\n    if line.startswith("/"):\n        parts = line[1:].split(" ", 1)\n'
           '        return parts[0], parts[1].strip() if len(parts) > 1 else ""\n    return "", line.strip()\n\nprint(parse_command("/ник  Зед "))',
           ["('/ник', 'Зед')", "('ник', ' Зед ')", "('', '/ник  Зед ')"], 'Косая черта отрезается, аргумент — после первого пробела, без пробелов по краям.'),
        q('Зачем ошибки команд вызывать своим исключением ChatError, а не печатать на месте?', 'Чтобы обрабатывать их в одном месте — в главном цикле',
          ['Иначе программа не запустится', 'Исключения работают быстрее print'], 'Функции только сообщают об ошибке, а как её показать — решает цикл.'),
        q('С чего начинается код второго этапа?', 'С готового кода первого этапа', ['С пустого редактора', 'С эталона третьего этапа'],
          'Этапы складываются в одну программу.'),
    ])


def code_msg():
    msg_cls = ('from enum import Enum\nfrom dataclasses import dataclass\n\n\nclass Kind(Enum):\n    TEXT = "TEXT"\n    SYSTEM = "SYSTEM"\n\n\n'
               '@dataclass\nclass Message:\n    id: int\n    author: str\n    text: str\n    kind: Kind = Kind.TEXT\n\n    def __str__(self):\n'
               '        if self.kind == Kind.SYSTEM:\n            return f"[{self.id}] * {self.text}"\n        return f"[{self.id}] {self.author}: {self.text}"\n')
    return ts('Мессенджер: устройство', [
        task('Напиши функцию parse_command(line). Если строка начинается с «/», верни кортеж из имени команды (без «/», до первого пробела) '
             'и аргумента — всего после первого пробела, без пробелов по краям (или пустой строки). Иначе верни кортеж из пустой строки '
             'и самой строки без пробелов по краям.',
             'line[1:].split(" ", 1) — второй аргумент split: разрезать не больше одного раза.\nАргумент: parts[1].strip() if len(parts) > 1 else ""',
             'def parse_command(line):\n    if line.startswith("/"):\n        parts = line[1:].split(" ", 1)\n        return parts[0], parts[1].strip() if len(parts) > 1 else ""\n'
             '    return "", line.strip()\n',
             ['print(parse_command("/ник Аня"))\nprint(parse_command("привет"))', 'print(parse_command("/история"), parse_command("/найти   кот  "))',
              'print(parse_command("  a/b  "), parse_command("/a b c"))'], tail=TL),
        task('Сообщения бывают обычные и системные. Опиши Enum Kind с элементами TEXT = «TEXT» и SYSTEM = «SYSTEM» и dataclass Message '
             'с полями id, author, text и kind (по умолчанию Kind.TEXT). print обычного сообщения показывает «[ID] АВТОР: ТЕКСТ», '
             'системного — «[ID] * ТЕКСТ».',
             'В dataclass можно писать свои методы: def __str__(self) с проверкой self.kind == Kind.SYSTEM.',
             msg_cls,
             ['print(Message(1, "Аня", "хай"))\nprint(Message(2, "*", "гость теперь Zed", Kind.SYSTEM))',
              'm = Message(3, "Zed", "ok")\nprint(m == Message(3, "Zed", "ok"), m.kind.value, Message(4, "a", "b").kind == Kind.TEXT)'], tail=TL),
        task('Классы Kind и Message из прошлой задачи уже в заготовке. Напиши функцию stats(messages): список пар (автор, число сообщений) '
             'только по обычным сообщениям — по убыванию числа, при равенстве — по имени автора.',
             'Counter из collections: Counter(m.author for m in messages if m.kind == Kind.TEXT).\nСортировка пар: key=lambda p: (-p[1], p[0]).',
             msg_cls + '\n\nfrom collections import Counter\n\n\ndef stats(messages):\n    counts = Counter(m.author for m in messages if m.kind == Kind.TEXT)\n'
             '    return sorted(counts.items(), key=lambda p: (-p[1], p[0]))\n',
             ['ms = [Message(1, "Аня", "a"), Message(2, "Zed", "b"), Message(3, "Аня", "c"), Message(4, "*", "x", Kind.SYSTEM)]\nprint(stats(ms))',
              'ms = [Message(i, n, "t") for i, n in enumerate(["Борис", "Аня", "Борис", "Аня", "Вика"], 1)]\nprint(stats(ms), stats([]))'],
             tail=TL, starter=msg_cls),
    ])


MSG_COMMON = ('Команды начинаются с «/», всё остальное — текст сообщения (пробелы по краям убираются, пустые строки ничего не делают). '
              'Сообщение печатается в виде «[ID] НИК: ТЕКСТ», ID — номер по порядку с 1. Ник в начале — «гость».\n')


def msg_stages():
    s1 = pj('Мессенджер, этап 1: чат на одного',
            'Сделай чат, в котором пишет один человек. ' + MSG_COMMON +
            'Команды:\n— «/ник ИМЯ» → ник меняется, вывести «Теперь ты ИМЯ»; без имени — «Ник не может быть пустым»;\n'
            '— «/история» → все сообщения по порядку или «Сообщений нет»;\n— «/выход» → «Пока, НИК!» и конец программы;\n'
            '— другая команда → «Неизвестная команда: /КОМАНДА».\nСообщение храни как dataclass Message(id, author, text).',
            'dataclass Message с __str__ — как в задаче-части\nparse_command из задачи-части\nсписок messages, ID нового — len(messages) + 1',
            src('msg1.py'),
            ['привет всем\n/история\n/ник Аня\nкак дела?\n/история\n/выход', '/ник\n/помощь\n/история\n   \n/выход'])
    s2 = pj('Мессенджер, этап 2: поиск и статистика',
            'Продолжи чат с первого этапа — его код уже в редакторе. ' + MSG_COMMON +
            'Что меняется и добавляется:\n— «/ник ИМЯ» теперь создаёт системное сообщение «СТАРЫЙ теперь НОВЫЙ» (автор «*», Kind.SYSTEM) — '
            'оно получает следующий ID и печатается как «[ID] * текст»; строки «Теперь ты …» больше нет;\n'
            '— «/найти СЛОВО» → обычные сообщения, где есть это слово без учёта регистра, или «Ничего не найдено»; без слова подходят все обычные сообщения;\n'
            '— «/упоминания» → обычные сообщения, где есть «@НИК» текущего ника без учёта регистра, или «Тебя не упоминали»;\n'
            '— «/стат» → строки «АВТОР: N» по обычным сообщениям, по убыванию N, при равенстве по имени; если их нет — «Сообщений нет»;\n'
            '— «/история», «/выход», пустой ник и неизвестные команды — как раньше.',
            'Kind и Message с kind — из задачи-части\nstats из задачи-части\nобщая функция show(found, empty): напечатать список или строку empty',
            src('msg2.py'),
            ['привет\n/ник Аня\n@гость ты где?\nКто видел @Аню?\n/найти ПРИВ\n/стат\n/упоминания\n/история\n/выход',
             '/стат\n/найти x\n/упоминания\n/ник Zed\n/ник Аня\nhi @zed\n/упоминания\n/выход', '/код\n/выход'],
            starter=src('msg1.py'))
    s3 = pj('Мессенджер, этап 3: сервер',
            'Перенеси чат на сервер: сообщения хранятся на http://chat.itp/messages. GET отдаёт список словарей с ключами id, author, text '
            'и kind («TEXT» или «SYSTEM»); POST с json={"author": …, "text": …, "kind": …} создаёт сообщение и возвращает его с новым id; '
            'GET и DELETE на http://chat.itp/messages/ID работают с одним сообщением (нет такого — код 404). На сервере уже есть чужие сообщения.\n'
            'В начале выведи «Подключено к серверу». Отправка текста и смена ника идут через POST, сообщение печатается из ответа сервера. '
            '«/история», «/найти», «/упоминания» и «/стат» работают по сообщениям с сервера.\nНовое:\n'
            '— «/обновить» → сообщения с ID больше отметки или «Новых сообщений нет». Отметка в начале равна 0; её сдвигают только «/обновить» '
            '(до наибольшего показанного ID) и твои отправки — текст и смена ника (до ID отправленного). «/история», «/найти» и прочие её не трогают;\n'
            '— «/удалить ID» → «Сообщение ID удалено», если оно твоё (автор — текущий ник); иначе «Можно удалять только свои сообщения», '
            '«Нет сообщения ID» или, если ID не число, «Укажи номер сообщения».\n'
            'Ошибки команд вызывай своим исключением ChatError и печатай его текст в главном цикле.',
            'requests.get(BASE).json() → список словарей; Kind(d["kind"]) — элемент Enum по значению\n'
            'seen — ID последнего показанного; global seen внутри функции\nclass ChatError(Exception): pass; try/except ChatError в цикле',
            src('msg3.py'),
            ['/обновить\nДа, иду!\n/обновить\n/упоминания\n/стат\n/выход',
             '/ник Лёша\nпривет\n/удалить 2\n/удалить 6\n/удалить 9\n/удалить abc\n/история\n/выход', '/найти кино\n/стат\n/неизвестная\n/выход'],
            starter=src('msg2.py'), files=CHAT)
    return [s1, s2, s3]


def th_rpg():
    terms = [
        ('игровой цикл', 'Главный цикл игры: прочитать команду, изменить состояние мира, показать результат — и так, пока игра не кончится.'),
    ]
    body = (
        '<p>Второй проект — <b>текстовая RPG</b>: герой, предметы, бой и подземелье из файла. Тоже три этапа, каждый продолжает код прошлого:</p>'
        '<table><tr><th>Этап</th><th>Что добавляется</th></tr>'
        '<tr><td>1. Герой и вещи</td><td>предметы через dataclass и Enum, сумка, экипировка, зелья</td></tr>'
        '<tr><td>2. Бой</td><td>общий родитель Creature для героя и монстров, бой по раундам, своё исключение GameOver</td></tr>'
        '<tr><td>3. Подземелье</td><td>комнаты из файла dungeon.json, переходы, монстры и предметы в комнатах, победа</td></tr></table>'
        '<p>Сердце игры — [[игровой цикл]]: прочитать команду, поменять мир, показать, что вышло. Всё случайное убрано: урон считается '
        'по формуле, поэтому игру можно проверить тестами.</p>'
        '<p>Удар: урон = атака бьющего − защита того, кого бьют, но не меньше 1. Атака героя — 3 плюс сила оружия в руках, защита — '
        'сила надетой брони. Так бойца описывает dataclass; в этапах к нему добавятся property и наследование:</p>'
        + ex('from dataclasses import dataclass\n\n\n@dataclass\nclass Creature:\n    name: str\n    hp: int\n    attack: int\n    defense: int = 0\n\n'
             '    def hit(self, other):\n        damage = max(1, self.attack - other.defense)\n        other.hp = max(0, other.hp - damage)\n        return damage\n\n\n'
             'rat = Creature("крыса", 8, 3)\nknight = Creature("рыцарь", 20, 7, 4)\nprint(knight.hit(rat), rat.hp)\nprint(rat.hit(knight), knight.hp)') +
        '<p>У крысы атака 3, у рыцаря защита 4 — урон всё равно 1: правило «не меньше 1» не даёт бою зависнуть.</p>'
    )
    return th('RPG: устройство', terms, body)


def fl_rpg():
    return fl('RPG: устройство', [
        qo('Что выведет программа?', 'def damage(attack, defense):\n    return max(1, attack - defense)\n\nprint(damage(8, 3), damage(2, 5))',
           ['5 -3', '5 0', '11 7'], 'Второй удар слабее защиты, но урон не меньше 1.'),
        q('Зачем в бою героя и монстров общий родитель Creature?', 'Чтобы удар и проверка «жив ли» были написаны один раз',
          ['Иначе нельзя создать монстра', 'Чтобы монстры могли носить оружие'], 'Наследники получают hit и alive от родителя.'),
        q('Почему в учебной RPG нет случайного урона?', 'Чтобы результат игры можно было проверить тестами',
          ['random нельзя использовать в классах', 'Случайный урон делает игру слишком лёгкой'], 'С одинаковым вводом — одинаковый вывод.'),
    ])


def code_rpg():
    item_cls = ('from dataclasses import dataclass\nfrom enum import Enum\n\n\nclass Kind(Enum):\n    WEAPON = "оружие"\n    ARMOR = "броня"\n    POTION = "зелье"\n\n\n'
                '@dataclass\nclass Item:\n    name: str\n    kind: Kind\n    power: int\n\n    def __str__(self):\n        return f"{self.name} ({self.kind.value}, {self.power})"\n')
    creature = ('from dataclasses import dataclass\n\n\n@dataclass\nclass Creature:\n    name: str\n    hp: int\n    base_attack: int\n    base_defense: int = 0\n\n'
                '    @property\n    def attack(self):\n        return self.base_attack\n\n    @property\n    def defense(self):\n        return self.base_defense\n\n'
                '    @property\n    def alive(self):\n        return self.hp > 0\n\n    def hit(self, other):\n        damage = max(1, self.attack - other.defense)\n'
                '        other.hp = max(0, other.hp - damage)\n        return damage\n')
    return ts('RPG: устройство', [
        task('Предметы. Опиши Enum Kind: WEAPON = «оружие», ARMOR = «броня», POTION = «зелье», и dataclass Item(name, kind, power), который '
             'печатается как «название (вид, сила)». Напиши функцию parse_items(text): строка вида «меч:оружие:4, зелье:зелье:8» '
             '(части через «, », внутри — через «:») превращается в список Item. Пустая строка — пустой список.',
             'Вид по значению — Kind("оружие"). Части: text.split(", "); пустые куски пропускай — так пустая строка даст пустой список.',
             item_cls + '\n\ndef parse_items(text):\n    items = []\n    for part in text.split(", "):\n        if part:\n            name, kind, power = part.split(":")\n'
             '            items.append(Item(name, Kind(kind), int(power)))\n    return items\n',
             ['for it in parse_items("меч:оружие:4, зелье:зелье:8"):\n    print(it)', 'print(parse_items(""), len(parse_items("щит:броня:2")))\n'
              'print(parse_items("лук:оружие:3")[0].kind == Kind.WEAPON)'], tail=TL),
        task('Бойцы. Напиши dataclass Creature(name, hp, base_attack, base_defense=0). Свойства attack и defense возвращают base_attack и '
             'base_defense (наследники потом добавят к ним оружие и броню), alive — True, пока hp больше нуля. Метод hit(other) наносит '
             'other урон max(1, атака − защита other), не опуская его здоровье ниже нуля, и возвращает урон.',
             'Свойства — @property внутри dataclass, как в обычном классе.\nhit: damage = max(1, self.attack - other.defense); other.hp = max(0, other.hp - damage).',
             creature,
             ['rat = Creature("крыса", 8, 3)\nhero = Creature("герой", 20, 7, 1)\nprint(hero.hit(rat), rat.hp, rat.alive)\nprint(rat.hit(hero), hero.hp)',
              'a = Creature("a", 2, 10)\nb = Creature("b", 5, 1, 9)\nprint(a.hit(b), b.hp, b.hit(a), a.hp, a.alive)\nprint(a.hit(b), b.hit(b), b.hp, b.alive)'],
             tail=TL),
        task('Бой. Класс Creature из прошлой задачи уже в заготовке. Напиши исключение GameOver и функцию fight(hero, monster): бой по '
             'раундам, первым бьёт герой. После удара героя выведи «Ты бьёшь: МОНСТР -УРОН, осталось HP»; если монстр погиб — '
             '«МОНСТР побеждён!» и конец боя. Иначе бьёт монстр: «МОНСТР бьёт: ты -УРОН, осталось HP»; если погиб герой — вызови GameOver.',
             'while True: два удара по очереди, после каждого проверка alive.\nclass GameOver(Exception): pass; raise GameOver, когда not hero.alive.',
             creature + '\n\nclass GameOver(Exception):\n    pass\n\n\ndef fight(hero, monster):\n    while True:\n        damage = hero.hit(monster)\n'
             '        print(f"Ты бьёшь: {monster.name} -{damage}, осталось {monster.hp}")\n        if not monster.alive:\n            print(f"{monster.name} побеждён!")\n'
             '            return\n        damage = monster.hit(hero)\n        print(f"{monster.name} бьёт: ты -{damage}, осталось {hero.hp}")\n        if not hero.alive:\n'
             '            raise GameOver\n',
             ['fight(Creature("Рыцарь", 20, 7), Creature("крыса", 8, 3))', 'try:\n    fight(Creature("Новичок", 6, 2), Creature("волк", 20, 4, 1))\n'
              'except GameOver:\n    print("герой пал")'], tail=TL, starter=creature),
    ])


RPG_COMMON = ('Команды — «действие аргумент»: «статус» → «ИМЯ: здоровье H/M, атака A, защита D»; «сумка» → «В сумке: …» '
              '(предметы как «название (вид, сила)» через запятую) или «Сумка пуста»; «надеть ПРЕДМЕТ» → оружие: «В руках: …», броня: '
              '«Надето: …», зелье: «Это не надеть»; «выпить ПРЕДМЕТ» → зелье лечит на свою силу, но не выше максимума, и исчезает: '
              '«Здоровье: H/M»; не зелье — «Это не выпить»; если предмета нет в сумке — и для «надеть», и для «выпить» — «В сумке нет ПРЕДМЕТ»; '
              '«выход» → «Игра окончена»; '
              'другое — «Не понимаю: ДЕЙСТВИЕ».\n')


def rpg_stages():
    s1 = pj('RPG, этап 1: герой и вещи',
            'Первая строка ввода — имя героя, вторая — предметы на земле в формате задачи-части («меч:оружие:4, зелье:зелье:8», может быть '
            'пустой), дальше — команды. У героя здоровье 20 из 30, атака 3 плюс сила оружия в руках, защита — сила надетой брони.\n' + RPG_COMMON +
            'Ещё две команды:\n— «осмотреться» → «На земле: …» или «На земле пусто»;\n— «взять ПРЕДМЕТ» → «Ты взял ПРЕДМЕТ» (предмет переходит в сумку) '
            'или «Здесь нет ПРЕДМЕТ».\nНадетый предмет остаётся в сумке.',
            'Kind, Item, parse_items — из задачи-части\ndataclass Hero с полем bag: list = field(default_factory=list)\nproperty attack и defense у героя',
            src('rpg1.py'),
            ['Рыцарь\nмеч:оружие:4, кольчуга:броня:3, зелье:зелье:8, кинжал:оружие:2\nосмотреться\nвзять меч\nвзять зелье\nвзять лук\nсумка\nнадеть меч\n'
             'надеть зелье\nстатус\nвыпить зелье\nвыпить меч\nосмотреться\nвыход', 'Тень\n\nосмотреться\nсумка\nстатус\nпрыгнуть\nвыход'])
    s2 = pj('RPG, этап 2: бой',
            'Продолжи игру с первого этапа. Третья строка ввода — монстры в формате «имя:здоровье:атака:защита» через «, ». Герой теперь — наследник '
            'Creature из задачи-части (здоровье 20, базовая атака 3, защита 0, максимум 30): его атака — базовая плюс оружие, защита — базовая плюс броня.\n'
            'Новые команды:\n— «враги» → «Враги: имя (здоровье), …» или «Врагов нет»;\n— «бой ИМЯ» → бой как в задаче-части; побеждённый монстр исчезает; '
            'нет такого — «Здесь нет ИМЯ»; если герой погиб — «Ты погиб. Игра окончена» и конец программы.\nОстальные команды — как на первом этапе.',
            'Creature, GameOver и fight — из задач-частей\n@dataclass class Hero(Creature) с полями max_hp, bag, weapon, armor\n'
            'Hero(имя, 20, 3); монстров разбирай как предметы',
            src('rpg2.py'),
            ['Рыцарь\nмеч:оружие:4, зелье:зелье:8\nкрыса:8:3:0, гоблин:15:5:1\nвраги\nвзять меч\nнадеть меч\nбой крыса\nбой дракон\nвраги\nбой гоблин\nстатус\nвыход',
             'Слабак\n\nтролль:40:9:3\nбой тролль\nвыход'],
            starter=src('rpg1.py'))
    s3 = pj('RPG, этап 3: подземелье',
            'Финал: рядом с программой лежит dungeon.json — карта подземелья. В нём start — комната, где начинает герой, goal — комната с сокровищем, '
            'rooms — комнаты: описание desc, выходы exits («направление»: «комната»), предметы items и монстр monster (строка или null) — '
            'в форматах прошлых этапов (файл виден в блоке «Файлы рядом с программой»). Выходы и предметы печатаются в порядке файла.\nПервая строка ввода — имя героя, дальше команды. В начале и при входе в комнату покажи её: описание, '
            '«Выходы: …» через запятую, «Предметы: …», если есть, и «Враг: имя (здоровье)», если монстр жив.\n'
            '— «осмотреться» → то же описание комнаты;\n— «идти НАПРАВЛЕНИЕ» → пока в комнате жив монстр — «Путь преграждает ИМЯ»; нет такого выхода — '
            '«Туда не пройти»; иначе переход;\n— «взять ПРЕДМЕТ» берёт из комнаты;\n— «бой» → бой с монстром комнаты или «Здесь не с кем драться»; '
            'победа над монстром комнаты goal — «Сокровища твои! Победа!» и конец игры.\nСтатус, сумка, надеть, выпить, выход, проигрыш, '
            '«Здесь нет ПРЕДМЕТ» при взятии и «Не понимаю: ДЕЙСТВИЕ» — как раньше.',
            'json.load для карты; dataclass Room(desc, exits, items, monster)\nlook(room) печатает комнату — вызывай при входе и на «осмотреться»\n'
            'here — имя текущей комнаты, rooms[here] — сама комната',
            src('rpg3.py'),
            ['Рыцарь\nвзять кинжал\nнадеть кинжал\nидти север\nидти восток\nбой\nидти восток\nвзять меч\nвзять кольчуга\nвзять зелье\nнадеть меч\n'
             'надеть кольчуга\nидти запад\nидти север\nбой\nстатус\nвыпить зелье\nидти север\nбой', 'Новичок\nидти север\nбой\nидти север\nбой',
             'Тест\nидти запад\nвзять меч\nвыпить зелье\nбой\nосмотреться\nсумка\nтанцевать\nвыход'],
            starter=src('rpg2.py'), files={'dungeon.json': DUNGEON})
    return [s1, s2, s3]


def build():
    return topic('Итоговые проекты', 'мессенджер и текстовая RPG по этапам', [
        th_data(), fl_data(), code_data(),
        th_msg(), fl_msg(), code_msg(), *msg_stages(),
        th_rpg(), fl_rpg(), code_rpg(), *rpg_stages(),
    ])
