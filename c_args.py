from dsl import *

# Тема 15 «Гибкие функции». Ученик знает свои функции (def, return, None, области видимости, подсказки типов),
# словари, множества, срезы, кортежи, map(int, ...) как готовый приём.
# Три теории: аргументы (по умолчанию, именованные, *args, **kwargs, распаковка при вызове); функции как значения,
# key и lambda; map, filter, reduce и from ... import. Мини-проект — «Шифр Цезаря».


def th_params():
    terms = [
        ('*args',
         'Параметр со звёздочкой собирает все лишние позиционные аргументы в кортеж. Имя может быть любым, args — традиция.\n'
         'Пример:\ndef total(*prices):\n    return sum(prices)\n\nprint(total(10, 20, 5))\nВывод:\n35'),
        ('**kwargs',
         'Параметр с двумя звёздочками собирает лишние именованные аргументы в словарь.\n'
         'Пример:\ndef info(**data):\n    print(data)\n\ninfo(age=15, city="Тула")\nВывод:\n{\'age\': 15, \'city\': \'Тула\'}'),
    ]
    body = (
        '<h3>Значения по умолчанию</h3>'
        '<p>Параметру можно задать значение по умолчанию — тогда аргумент при вызове можно не передавать. '
        'Так работают <code>sep</code> и <code>end</code> у <code>print</code>:</p>'
        + ex('def greet(name, greeting="Привет", mark="!"):\n    print(f"{greeting}, {name}{mark}")\n\ngreet("Ира")\ngreet("Ли", "Здравствуй")\ngreet("Тимур", mark="...")') +
        '<p>Параметры со значением по умолчанию пишут после обычных. Любой аргумент можно передать <b>по имени</b>: '
        '<code>mark="..."</code> — тогда порядок не важен и можно пропустить те, что посередине. Именованные аргументы '
        'при вызове идут после позиционных.</p>'
        '<h3>Сколько угодно аргументов</h3>'
        '<p>Параметр со звёздочкой [[*args]] собирает все лишние позиционные аргументы в кортеж, '
        'с двумя звёздочками [[**kwargs]] — лишние именованные в словарь:</p>'
        + ex('def order(table, *dishes, **notes):\n    print(f"Стол {table}: {\', \'.join(dishes)}")\n    for k, v in notes.items():\n        print(f"  {k}: {v}")\n\n'
             'order(5, "суп", "чай", "блин", spicy="нет", call="после 19:00")') +
        '<p>Так устроены <code>print</code> и <code>max</code>: они принимают любое число значений.</p>'
        '<h3>Звёздочка при вызове</h3>'
        '<p>Звёздочка работает и в обратную сторону: при вызове <code>*список</code> раскладывает список по позиционным '
        'аргументам, <code>**словарь</code> — по именованным:</p>'
        + ex('scores = [5, 3, 8]\nprint(*scores)\nprint(*scores, sep=" | ")\nopts = {"sep": "-", "end": "!\\n"}\nprint(1, 2, 3, **opts)') +
        '<p><code>print(*scores)</code> — то же, что <code>print(5, 3, 8)</code>: удобный способ вывести список через пробел без скобок.</p>'
    )
    return th('Аргументы функций', terms, body)


def fl_params():
    return fl('Аргументы функций', [
        qo('Что выведет программа?', 'def f(a, b=10):\n    return a + b\n\nprint(f(1), f(1, 2))', ['11', '3 3', 'Ошибка'], 'b по умолчанию 10: 11 и 3.'),
        qo('Что выведет программа?', 'def f(*a):\n    return len(a)\n\nprint(f(4, 5, 6))', ['1', '15', '(4, 5, 6)'], '*a собрал три аргумента в кортеж: 3.'),
        qo('Что выведет программа?', 'print(*[1, 2, 3], sep="")', ['[1, 2, 3]', '1 2 3', 'Ошибка'], 'Список разложен в три аргумента, sep пустой: 123.'),
        q('Какое объявление вызовет SyntaxError?', 'def f(a=1, b):', ['def f(a, b=1):', 'def f(a, *b):'],
          'Параметры со значением по умолчанию должны идти после обычных.'),
    ])


def code_params():
    return ts('Аргументы функций', [
        task('Напиши функцию price(cost, count=1, discount=0), которая возвращает итоговую цену: стоимость × количество '
             'со скидкой в процентах, округлённую до двух знаков.',
             'return round(cost * count * (100 - discount) / 100, 2).',
             'def price(cost, count=1, discount=0):\n    return round(cost * count * (100 - discount) / 100, 2)',
             ['print(price(100))', 'print(price(99.9, 3))', 'print(price(500, discount=20), price(250, 2, 10))'], tail=TL),
        task('Напиши функцию average(*marks), которая возвращает среднее любого числа оценок, округлённое до двух знаков, '
             'или None, если оценок нет.',
             'marks — кортеж: if not marks: return None; иначе round(sum(marks) / len(marks), 2).',
             'def average(*marks):\n    if not marks:\n        return None\n    return round(sum(marks) / len(marks), 2)',
             ['print(average(5, 4, 4))', 'print(average(3))', 'print(average())'], tail=TL),
        task('Напиши функцию profile(name, **info), которая выводит имя, а под ним каждую пару «  ключ: значение» '
             'в алфавитном порядке ключей.',
             'print(name), затем for k in sorted(info): print(f"  {k}: {info[k]}").',
             'def profile(name, **info):\n    print(name)\n    for k in sorted(info):\n        print(f"  {k}: {info[k]}")',
             ['profile("Ира", city="Тула", age=15)', 'profile("Ли")', 'profile("Ким", level=7, clan="Волки", age=16)'], tail=TL),
    ])


def th_lambda():
    terms = [
        ('lambda',
         'Короткая безымянная функция в одну строку: lambda параметры: выражение. Возвращает значение выражения. '
         'Чаще всего — как key для sorted, min, max.\n'
         'Пример:\nwords = ["кит", "ёж", "слон"]\nprint(sorted(words, key=lambda w: len(w)))\nВывод:\n[\'ёж\', \'кит\', \'слон\']'),
    ]
    body = (
        '<h3>Функция — тоже значение</h3>'
        '<p>Имя функции без скобок — это сама функция. Её можно положить в переменную или передать в другую функцию:</p>'
        + ex('def shout(s):\n    return s.upper() + "!"\n\nf = shout\nprint(f("привет"))\nprint(len)') +
        '<h3>key: по какому признаку сравнивать</h3>'
        '<p><code>sorted</code>, <code>min</code> и <code>max</code> принимают именованный аргумент <code>key</code> — функцию, '
        'которая для каждого элемента говорит, по чему его сравнивать:</p>'
        + ex('words = ["слон", "ёж", "кот", "жираф"]\nprint(sorted(words, key=len))\nprint(max(words, key=len))') +
        '<h3>lambda</h3>'
        '<p>Если функция нужна в одном месте и умещается в одно выражение, её пишут прямо на месте — [[lambda]]: '
        '<code>lambda параметры: выражение</code>. Это то же, что <code>def</code> с одним <code>return</code>, только без имени:</p>'
        + ex('scores = {"Ира": 40, "Ли": 75, "Ким": 75, "Тимур": 60}\nranking = sorted(scores.items(), key=lambda p: (-p[1], p[0]))\nprint(ranking)\n'
             'best = max(scores, key=lambda name: scores[name])\nprint(best)') +
        '<p>В первом случае <code>key</code> возвращает кортеж: сначала минус очки (по убыванию), при равенстве — имя по алфавиту. '
        'Это короче приёма с парами из темы «Словари и множества». Во втором <code>max</code> перебирает имена, '
        'а сравнивает их по очкам из словаря.</p>'
    )
    return th('Функции как значения и lambda', terms, body)


def fl_lambda():
    return fl('Функции как значения и lambda', [
        qo('Что выведет программа?', 'f = lambda x: x * 2\nprint(f(4))', ['4', 'lambda', 'x * 2'], 'lambda вернула 4 * 2 = 8.'),
        qo('Что выведет программа?', 'print(sorted(["bb", "a", "ccc"], key=len, reverse=True))', ["['a', 'bb', 'ccc']", "['bb', 'a', 'ccc']", 'Ошибка'],
           'По длине, от большей: [\'ccc\', \'bb\', \'a\'].'),
        qo('Что выведет программа?', 'print(min([-5, 3, -1], key=abs))', ['-5', '3', '1'], 'Меньше всего по модулю -1.'),
    ])


def code_lambda():
    return ts('Функции как значения и lambda', [
        task('На вход подаются слова через пробел. Выведи их через пробел, отсортированными по длине, а при равной длине — по алфавиту.',
             'sorted(words, key=lambda w: (len(w), w)) и print(*результат).',
             'words = input().split()\nprint(*sorted(words, key=lambda w: (len(w), w)))',
             ['слон ёж кот жираф кит', 'а б а', 'программа код']),
        task('Строки «Фамилия очки» подаются до слова «стоп». Выведи рейтинг: «МЕСТО. ФАМИЛИЯ ОЧКИ» по убыванию очков, '
             'при равенстве — по алфавиту.',
             'Собери список кортежей (фамилия, очки), затем sorted(data, key=lambda p: (-p[1], p[0])) и enumerate с 1.',
             'data = []\nwhile True:\n    s = input()\n    if s == "стоп":\n        break\n    name, pts = s.split()\n    data.append((name, int(pts)))\n'
             'for i, (name, pts) in enumerate(sorted(data, key=lambda p: (-p[1], p[0])), 1):\n    print(f"{i}. {name} {pts}")',
             ['Орлова 40\nКим 75\nБелов 75\nстоп', 'Ли 1\nстоп']),
        task('Самый тёплый день. Словарь temps задан: день недели → температура. Выведи день с самой высокой температурой '
             'и саму температуру: «ДЕНЬ: T».',
             'best = max(temps, key=lambda d: temps[d]) — max перебирает ключи, сравнивая по значениям.',
             'temps = {"пн": 3, "вт": 7, "ср": -1, "чт": 12, "пт": 9}\nbest = max(temps, key=lambda d: temps[d])\nprint(f"{best}: {temps[best]}")',
             [''], starter='temps = {"пн": 3, "вт": 7, "ср": -1, "чт": 12, "пт": 9}\n'),
    ])


def th_functional():
    terms = [
        ('filter', 'filter(функция, набор) оставляет элементы, для которых функция вернула истину. Результат перебирают или превращают в список.\n'
                   'Пример:\nprint(list(filter(lambda x: x > 0, [3, -1, 5])))\nВывод:\n[3, 5]'),
        ('reduce', 'reduce(функция двух аргументов, набор) сворачивает набор в одно значение: применяет функцию к первому и второму, '
                   'потом к результату и третьему и так далее. Находится в модуле functools.\n'
                   'Пример:\nfrom functools import reduce\nprint(reduce(lambda a, b: a * b, [2, 3, 4]))\nВывод:\n24'),
        ('functools', 'Модуль с инструментами для работы с функциями: reduce, lru_cache и другие.'),
        ('from', 'from модуль import имя — подключить из модуля только нужное имя; потом им пользуются без точки.\n'
                 'Пример:\nfrom math import sqrt\nprint(sqrt(25))\nВывод:\n5.0'),
    ]
    body = (
        '<p>Три функции, которые принимают другую функцию и применяют её к целому набору значений.</p>'
        '<h3>map</h3>'
        '<p><code>map(функция, набор)</code> применяет функцию к каждому элементу. Мы уже использовали '
        '<code>map(int, ...)</code>; теперь видно, что вместо <code>int</code> подойдёт любая функция:</p>'
        + ex('words = ["кот", "жираф", "ёж"]\nprint(list(map(len, words)))\nprint(list(map(lambda w: w.upper(), words)))') +
        '<h3>filter</h3>'
        '<p>[[filter]] оставляет только те элементы, для которых функция вернула истину:</p>'
        + ex('nums = [4, -2, 7, 0, -5, 3]\nprint(list(filter(lambda x: x > 0, nums)))\nprint(list(filter(lambda s: s.isdigit(), ["12", "a", "7"])))') +
        '<p><code>map</code> и <code>filter</code> не создают список сразу — они выдают значения по одному, когда их перебирают. '
        'Поэтому для вывода их оборачивают в <code>list</code> или перебирают в цикле.</p>'
        '<h3>reduce и from ... import</h3>'
        '<p>[[reduce]] сворачивает набор в одно значение. Он живёт в модуле [[functools]], и подключают его командой '
        '[[from]]: <code>from модуль import имя</code> берёт из модуля только нужное имя, и им пользуются без точки:</p>'
        + ex('from functools import reduce\nfrom math import sqrt\n\nprint(reduce(lambda a, b: a * b, [1, 2, 3, 4, 5]))\nprint(reduce(lambda a, b: a if a > b else b, [3, 9, 2]))\nprint(sqrt(16))') +
        '<p>В первом случае: 1·2 = 2, 2·3 = 6, 6·4 = 24, 24·5 = 120. Для суммы и максимума удобнее готовые <code>sum</code> '
        'и <code>max</code>; <code>reduce</code> нужен там, где готовой функции нет — например, для произведения.</p>'
    )
    return th('map, filter и reduce', terms, body)


def fl_functional():
    return fl('map, filter и reduce', [
        qo('Что выведет программа?', 'print(list(map(lambda x: x ** 2, [1, 2, 3])))', ['[1, 2, 3]', '[2, 4, 6]', '14'], 'Каждый элемент в квадрате: [1, 4, 9].'),
        qo('Что выведет программа?', 'print(list(filter(lambda s: len(s) > 2, ["ой", "ура", "да"])))', ["['ой', 'да']", '[3]', 'ура'],
           'Длиннее двух символов только «ура»: [\'ура\'].'),
        qo('Что выведет программа?', 'from functools import reduce\nprint(reduce(lambda a, b: a + b, ["a", "b", "c"]))', ["['a', 'b', 'c']", 'a b c', 'Ошибка'],
           'Склейка по очереди: abc.'),
    ])


def code_functional():
    return ts('map, filter и reduce', [
        task('На вход подаются целые числа через пробел. Выведи через пробел только чётные из них, возведённые в квадрат, '
             'или «Нет чётных».',
             'evens = list(filter(lambda x: x % 2 == 0, nums)), squares = list(map(lambda x: x * x, evens)). Пустой список — ложь.',
             'nums = list(map(int, input().split()))\nevens = list(filter(lambda x: x % 2 == 0, nums))\nsquares = list(map(lambda x: x * x, evens))\n'
             'if squares:\n    print(*squares)\nelse:\n    print("Нет чётных")',
             ['1 2 3 4 5 6', '7 9', '0 -2']),
        task('Факториал. На вход подаётся n ≥ 1. Выведи n! = 1 · 2 · … · n с помощью reduce.',
             'from functools import reduce; reduce(lambda a, b: a * b, range(1, n + 1)).',
             'from functools import reduce\nn = int(input())\nprint(reduce(lambda a, b: a * b, range(1, n + 1)))', ['5', '1', '20']),
        task('Длины слов. На вход подаётся фраза. Выведи длины слов через пробел, а следующей строкой — длину самого '
             'длинного слова.',
             'lens = list(map(len, words)); print(*lens); print(max(lens)).',
             'lens = list(map(len, input().split()))\nprint(*lens)\nprint(max(lens))', ['я люблю Python', 'ой', 'это очень длинное предложение']),
    ])


def project():
    return pj('Шифр Цезаря',
              'Шифр Цезаря сдвигает каждую букву на одно и то же число позиций по алфавиту, по кругу: при сдвиге 3 «а» → «г», «я» → «в».\n'
              'Вход: первая строка — «шифр» или «расшифр», вторая — сдвиг (целое число, может быть больше 33 или отрицательным), '
              'третья — текст.\n'
              'Правила: алфавит русский, 33 буквы с «ё» на своём месте после «е»; большие буквы остаются большими, маленькие — маленькими; '
              'все остальные символы (пробелы, цифры, знаки, латиница) не меняются. «расшифр» — сдвиг в обратную сторону.\n'
              'Вывод: одна строка — результат.\n'
              'Сделай функцию shift_char(c, k), которая сдвигает один символ, и функцию caesar(text, k), которая применяет её ко всему тексту.',
              'Алфавит строкой: ABC = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя". Номер буквы — ABC.find(c.lower()), новый — (номер + k) % 33. '
              'Это работает и для отрицательных: в Python остаток при положительном делителе всегда от 0 до 32, например -1 % 33 = 32.\n'
              'Для большой буквы ищи по c.lower(), а результат возвращай через .upper().\n'
              'caesar: "".join(map(lambda c: shift_char(c, k), text)). Для «расшифр» вызови caesar(text, -k).',
              'ABC = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"\n\n\ndef shift_char(c, k):\n    i = ABC.find(c.lower())\n    if i == -1:\n        return c\n'
              '    new = ABC[(i + k) % 33]\n    return new.upper() if c.isupper() else new\n\n\ndef caesar(text, k):\n    return "".join(map(lambda c: shift_char(c, k), text))\n\n\n'
              'mode = input()\nk = int(input())\ntext = input()\nprint(caesar(text, k) if mode == "шифр" else caesar(text, -k))',
              ['шифр\n3\nПривет, мир!', 'расшифр\n3\nТулеих, плу!', 'шифр\n33\nЁжик', 'шифр\n-1\nабв ABC 123', 'расшифр\n40\nЖёлтый'])


def build():
    return topic('Гибкие функции', '*args, **kwargs, lambda, map, filter, key', [
        th_params(), fl_params(), code_params(),
        th_lambda(), fl_lambda(), code_lambda(),
        th_functional(), fl_functional(), code_functional(),
        project(),
    ])
