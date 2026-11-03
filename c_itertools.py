from dsl import *

# Тема 17 «Инструменты для коллекций». Ученик знает выражения-генераторы, lambda/key, map/filter/reduce, from ... import,
# словари, множества, кортежи, enumerate, zip. Три теории: итераторы (iter, next, StopIteration);
# модуль itertools; модуль collections (Counter, defaultdict, deque).


def th_iter():
    terms = [
        ('iter', 'Создаёт итератор — «указатель», который выдаёт элементы набора по одному.\n'
                 'Пример:\nit = iter("ой")\nprint(next(it), next(it))\nВывод:\nо й'),
        ('next', 'Следующий элемент итератора. Если элементы кончились — StopIteration, или значение по умолчанию, если оно передано вторым аргументом.\n'
                 'Пример:\nit = iter([1])\nprint(next(it), next(it, "конец"))\nВывод:\n1 конец'),
        ('StopIteration', 'Сигнал «элементы кончились»: next у пустого итератора. Цикл for ловит его сам и просто заканчивается.'),
    ]
    body = (
        '<p>Как <code>for</code> перебирает и списки, и строки, и словари, и <code>range</code>? Через общий механизм — '
        '<b>итераторы</b>. Функция [[iter]] даёт итератор набора, а [[next]] берёт из него следующий элемент:</p>'
        + ex('it = iter(["старт", "середина", "финиш"])\nprint(next(it))\nprint(next(it))\nprint(next(it))\nprint(next(it, "больше нет"))') +
        '<p>Когда элементы кончаются, <code>next</code> без запасного значения выдаёт [[StopIteration]]. Цикл <code>for</code> '
        'делает то же самое: берёт итератор и вызывает <code>next</code>, пока не получит StopIteration — и тогда тихо заканчивается.</p>'
        + exerr('it = iter([1])\nnext(it)\nnext(it)') +
        '<h3>Итератор одноразовый</h3>'
        '<p>Итератор помнит, где остановился, и второй раз по нему не пройти. Это же верно для <code>map</code>, <code>filter</code>, '
        '<code>zip</code> и выражений-генераторов:</p>'
        + ex('squares = map(lambda x: x * x, [1, 2, 3])\nprint(list(squares))\nprint(list(squares))') +
        '<p>Второй раз список пуст: всё уже выдано. Если результат нужен несколько раз — сохрани его в список.</p>'
        '<p>Зачем <code>next</code> на практике: взять первую строку ввода отдельно от остальных или первый подходящий элемент — '
        '<code>next((x for x in nums if x &lt; 0), None)</code> вернёт первое отрицательное или None.</p>'
    )
    return th('Итераторы', terms, body)


def fl_iter():
    return fl('Итераторы', [
        qo('Что выведет программа?', 'it = iter("abc")\nnext(it)\nprint(next(it))', ['a', 'abc', 'c'], 'Первый next забрал «a», второй — «b».'),
        qo('Что выведет программа?', 'g = (x * 2 for x in [1, 2])\nprint(sum(g), sum(g))', ['6 6', '0 6', '3 3'], 'Генератор одноразовый: 6 и 0.'),
        qo('Что выведет программа?', 'print(next((w for w in ["кот", "слон", "ёж"] if len(w) > 3), "нет"))', ['нет', 'кот', 'ёж'],
           'Первое слово длиннее трёх букв — слон.'),
    ])


def code_iter():
    return ts('Итераторы', [
        task('На вход подаются числа через пробел. Выведи первое отрицательное или «Все неотрицательные».',
             'next((x for x in nums if x < 0), "Все неотрицательные").',
             'nums = map(int, input().split())\nprint(next((x for x in nums if x < 0), "Все неотрицательные"))',
             ['3 5 -2 -7', '1 2', '-1']),
        task('Напиши функцию pairs(items), которая возвращает список пар соседних элементов: для [1, 2, 3] — [(1, 2), (2, 3)].',
             'zip(items, items[1:]) склеивает список со сдвинутой на один копией; list(...) — в список.',
             'def pairs(items):\n    return list(zip(items, items[1:]))',
             ['print(pairs([1, 2, 3]))', 'print(pairs(["а"]))', 'print(pairs("кот"))'], tail=TL),
        task('Первый повтор. На вход подаётся строка. Выведи первый символ, который уже встречался раньше в этой строке, '
             'или «Повторов нет».',
             'Символ с номером i повторяется, если он есть в s[:i]. Первый такой — next((c for i, c in enumerate(s) if c in s[:i]), "Повторов нет").',
             's = input()\nprint(next((c for i, c in enumerate(s) if c in s[:i]), "Повторов нет"))',
             ['программа', 'кот', 'абвгдб', 'aa']),
        task('Пошаговое обучение. Первая строка ввода — шаги обучения через «;». Дальше подаются команды до слова «стоп»: '
             'на «дальше» выведи следующий шаг, а когда шаги закончились — «Обучение пройдено» (и на все следующие «дальше» '
             'тоже). Другие команды пропускай.',
             'it = iter(steps); следующий шаг — next(it, None): второй аргумент вернётся вместо StopIteration.',
             'it = iter(input().split(";"))\nwhile True:\n    cmd = input()\n    if cmd == "стоп":\n        break\n    if cmd == "дальше":\n'
             '        step = next(it, None)\n        print(step if step is not None else "Обучение пройдено")',
             ['Ходьба;Прыжок;Удар\nдальше\nдальше\nпрыг\nдальше\nдальше\nстоп', 'Старт\nдальше\nдальше\nдальше\nстоп', 'А;Б\nдальше\nстоп']),
    ])


def th_itertools():
    terms = [
        ('itertools', 'Модуль с готовыми итераторами для перебора: бесконечные счётчики, склейки, комбинации.'),
        ('itertools.count', 'Бесконечный счётчик с начального числа и шагом. Останавливают его сами (break или islice).\n'
                            'Пример:\nfrom itertools import count\nfor i in count(10, 5):\n    if i > 20:\n        break\n    print(i, end=" ")\nВывод:\n10 15 20'),
        ('cycle', 'Бесконечно повторяет набор по кругу.\nПример:\nfrom itertools import cycle, islice\nprint(list(islice(cycle("аб"), 5)))\nВывод:\n[\'а\', \'б\', \'а\', \'б\', \'а\']'),
        ('islice', 'Срез итератора: islice(it, n) — первые n элементов, islice(it, a, b) — с a до b.\n'
                   'Пример:\nfrom itertools import islice, count\nprint(list(islice(count(1), 3)))\nВывод:\n[1, 2, 3]'),
        ('chain', 'Перебирает несколько наборов подряд, как один.\nПример:\nfrom itertools import chain\nprint(list(chain([1, 2], "ab")))\nВывод:\n[1, 2, \'a\', \'b\']'),
        ('product', 'Все пары (тройки…) из элементов наборов — как вложенные циклы. repeat=n — набор с самим собой n раз.\n'
                    'Пример:\nfrom itertools import product\nprint(list(product("аб", [1, 2])))\nВывод:\n[(\'а\', 1), (\'а\', 2), (\'б\', 1), (\'б\', 2)]'),
        ('permutations', 'Все перестановки — порядок важен. Второй аргумент — сколько элементов брать.\n'
                         'Пример:\nfrom itertools import permutations\nprint(list(permutations("аб")))\nВывод:\n[(\'а\', \'б\'), (\'б\', \'а\')]'),
        ('combinations', 'Все сочетания по k — порядок не важен, повторов нет.\n'
                         'Пример:\nfrom itertools import combinations\nprint(list(combinations([1, 2, 3], 2)))\nВывод:\n[(1, 2), (1, 3), (2, 3)]'),
        ('accumulate', 'Накопительные итоги: каждое значение — сумма всех предыдущих (или результат другой функции).\n'
                       'Пример:\nfrom itertools import accumulate\nprint(list(accumulate([5, 3, 2])))\nВывод:\n[5, 8, 10]'),
    ]
    body = (
        '<p>Модуль [[itertools]] — набор готовых итераторов для частых задач перебора. Подключают нужное через <code>from</code>.</p>'
        '<h3>Бесконечные</h3>'
        '<p>[[itertools.count|count]] считает без конца, [[cycle]] крутит набор по кругу. Их останавливают сами: '
        '<code>break</code> или [[islice]] — срез для итераторов:</p>'
        + ex('from itertools import count, cycle, islice\nprint(list(islice(count(100, 7), 4)))\nturns = cycle(["Ира", "Ли", "Ким"])\nfor i in range(5):\n    print(next(turns), end=" ")') +
        '<h3>Склейка и накопление</h3>'
        + ex('from itertools import chain, accumulate\nweek1 = [3, 5]\nweek2 = [2, 4, 1]\nprint(list(chain(week1, week2)))\nprint(list(accumulate(chain(week1, week2))))') +
        '<p>[[chain]] перебирает наборы подряд, [[accumulate]] даёт накопительные суммы — сколько всего набралось к каждому дню.</p>'
        '<h3>Комбинаторика</h3>'
        '<p>[[product]] заменяет вложенные циклы, [[permutations]] перебирает все перестановки (порядок важен), '
        '[[combinations]] — все сочетания (порядок не важен):</p>'
        + ex('from itertools import product, permutations, combinations\nprint(len(list(product("01", repeat=3))))\n'
             'print(["".join(p) for p in permutations("кот")])\nteams = ["Волки", "Лисы", "Совы"]\nfor a, b in combinations(teams, 2):\n    print(a, "—", b)') +
        '<p>Последний пример — расписание турнира «каждый с каждым». Комбинаций становится очень много очень быстро: '
        '10 элементов дают 3,6 миллиона перестановок — перебирать «всё подряд» можно только для небольших наборов.</p>'
    )
    return th('Модуль itertools', terms, body)


def fl_itertools():
    return fl('Модуль itertools', [
        qo('Что выведет программа?', 'from itertools import combinations\nprint(len(list(combinations("абвг", 2))))', ['4', '12', '16'], 'Пар без учёта порядка из 4 элементов: 6.'),
        qo('Что выведет программа?', 'from itertools import accumulate\nprint(list(accumulate([1, 1, 1])))', ['[1, 1, 1]', '3', '[3]'], 'Накопительные суммы: [1, 2, 3].'),
        qo('Что выведет программа?', 'from itertools import product\nprint(len(list(product([1, 2], "abc"))))', ['5', '2', '3'], '2 × 3 = 6 пар.'),
    ])


def code_itertools():
    return ts('Модуль itertools', [
        task('Турнир «каждый с каждым». На вход подаются названия команд через пробел. Выведи все матчи «A — B» в порядке, '
             'который даёт combinations, и последней строкой — «Матчей: N».',
             'for a, b in combinations(teams, 2): print(f"{a} — {b}"); счётчик или len(list(combinations(...))).',
             'from itertools import combinations\nteams = input().split()\nmatches = list(combinations(teams, 2))\nfor a, b in matches:\n'
             '    print(f"{a} — {b}")\nprint(f"Матчей: {len(matches)}")',
             ['Волки Лисы Совы', 'А Б', 'Альфа Бета Гамма Дельта']),
        task('Подбор пин-кода. Известно, что код из трёх цифр, в нём только цифры из строки ввода (в строке цифры разные, '
             'а в коде могут повторяться) '
             'и сумма цифр равна S. На вход подаются строка цифр и S. Выведи все такие коды в порядке перебора product '
             'через пробел или «Нет вариантов».',
             'product(digits, repeat=3) даёт кортежи символов; сумма — sum(int(d) for d in t); код — "".join(t).',
             'from itertools import product\ndigits = input()\ns = int(input())\ncodes = ["".join(t) for t in product(digits, repeat=3) if sum(int(d) for d in t) == s]\n'
             'if codes:\n    print(*codes)\nelse:\n    print("Нет вариантов")',
             ['123\n6', '05\n10', '9\n1']),
        task('Копилка. На вход подаются суммы, которые откладывались каждую неделю, через пробел, и цель. Выведи номер недели '
             '(с 1), на которой накопленная сумма впервые достигла цели, или «Цель не достигнута».',
             'Накопительные суммы — accumulate; первая подходящая — next((i for i, s in enumerate(accumulate(...), 1) if s >= goal), None).',
             'from itertools import accumulate\nweeks = list(map(int, input().split()))\ngoal = int(input())\n'
             'w = next((i for i, s in enumerate(accumulate(weeks), 1) if s >= goal), None)\nprint(w if w else "Цель не достигнута")',
             ['100 200 150 300\n400', '50 50\n1000', '500\n500']),
        task('Пары артефактов. Первая строка ввода — артефакты «имя:сила» через пробел, вторая — нужная сила пары. '
             'Выведи все пары разных артефактов с такой суммарной силой, по одной в строке: «А + Б», в каждой паре и между '
             'парами — в порядке появления в списке. Если пар нет, выведи «Нет пар».',
             'Разбери в список кортежей (имя, сила). combinations(items, 2) даёт пары в порядке списка без повторов.',
             'from itertools import combinations\nitems = []\nfor p in input().split():\n    name, power = p.split(":")\n    items.append((name, int(power)))\n'
             'need = int(input())\nfound = False\nfor a, b in combinations(items, 2):\n    if a[1] + b[1] == need:\n        print(f"{a[0]} + {b[0]}")\n        found = True\n'
             'if not found:\n    print("Нет пар")',
             ['кольцо:3 амулет:7 меч:5 щит:5 перо:2\n10', 'а:1 б:2\n5', 'x:4 y:4 z:4\n8']),
    ])


def th_collections():
    terms = [
        ('collections', 'Модуль с особыми коллекциями: Counter, defaultdict, deque и другими.'),
        ('Counter', 'Словарь-счётчик: из набора сразу считает, сколько раз встречается каждый элемент. Отсутствующий ключ даёт 0.\n'
                    'Пример:\nfrom collections import Counter\nc = Counter("банан")\nprint(c["а"], c["я"])\nВывод:\n2 0'),
        ('most_common', 'Метод Counter: список пар (элемент, сколько) по убыванию частоты; с аргументом n — первые n.\n'
                        'Пример:\nfrom collections import Counter\nprint(Counter("абба").most_common(1))\nВывод:\n[(\'а\', 2)]'),
        ('defaultdict', 'Словарь, который для нового ключа сам создаёт значение по умолчанию: defaultdict(list) — пустой список, '
                        'defaultdict(int) — 0.\nПример:\nfrom collections import defaultdict\nd = defaultdict(list)\nd["10А"].append("Ира")\nprint(dict(d))\nВывод:\n{\'10А\': [\'Ира\']}'),
        ('deque', 'Двусторонняя очередь: быстро добавлять и забирать с обоих концов. append/appendleft, pop/popleft.\n'
                  'Пример:\nfrom collections import deque\nq = deque([1, 2])\nq.appendleft(0)\nprint(q.popleft(), list(q))\nВывод:\n0 [1, 2]'),
        ('appendleft', 'Метод deque: добавить элемент в начало.'),
        ('popleft', 'Метод deque: забрать и вернуть элемент из начала. Для списка pop(0) медленный на больших данных, popleft — быстрый.'),
    ]
    body = (
        '<p>В модуле [[collections]] — специализированные словари и очереди. Они делают то же, что мы уже писали вручную, '
        'но короче и быстрее.</p>'
        '<h3>Counter</h3>'
        '<p>Подсчёт частот через <code>get</code> — это [[Counter]] в одну строку. Метод [[most_common]] сразу даёт самых частых:</p>'
        + ex('from collections import Counter\nvotes = "Ира Ли Ира Тимур Ира Ли".split()\nc = Counter(votes)\nprint(c)\nprint(c.most_common(2))\nprint(c["Ким"])') +
        '<p>Для отсутствующего ключа Counter возвращает 0, а не KeyError.</p>'
        '<h3>defaultdict</h3>'
        '<p>[[defaultdict]] сам создаёт значение для нового ключа — пустой список, ноль — без <code>setdefault</code> и <code>get</code>:</p>'
        + ex('from collections import defaultdict\npupils = [("Ира", "10А"), ("Ли", "10Б"), ("Тимур", "10А")]\nby_class = defaultdict(list)\nfor name, cls in pupils:\n'
             '    by_class[cls].append(name)\nprint(dict(by_class))') +
        '<h3>deque</h3>'
        '<p>[[deque]] — очередь, из которой быстро брать с обоих концов: [[appendleft]] и [[popleft]] работают мгновенно, '
        'а у списка <code>pop(0)</code> на больших данных медленный — он сдвигает все элементы. Аргумент <code>maxlen</code> '
        'ограничивает длину: лишние элементы с другого конца выталкиваются сами — удобно для «последних N»:</p>'
        + ex('from collections import deque\nq = deque(["Ира", "Ли"])\nq.append("Ким")\nq.appendleft("VIP")\nprint(q.popleft(), list(q))\n'
             'last3 = deque(maxlen=3)\nfor msg in ["a", "b", "c", "d", "e"]:\n    last3.append(msg)\nprint(list(last3))')
    )
    return th('Модуль collections', terms, body)


def fl_collections():
    return fl('Модуль collections', [
        qo('Что выведет программа?', 'from collections import Counter\nprint(Counter("мама")["м"])', ['1', '4', 'Ошибка'], '«м» встречается дважды: 2.'),
        qo('Что выведет программа?', 'from collections import defaultdict\nd = defaultdict(int)\nd["x"] += 5\nprint(d["x"], d["y"])', ['Ошибка', '5', '5 None'],
           'Для нового ключа int даёт 0: 5 и 0.'),
        qo('Что выведет программа?', 'from collections import deque\nq = deque(maxlen=2)\nfor i in range(4):\n    q.append(i)\nprint(list(q))', ['[0, 1]', '[0, 1, 2, 3]', '[3]'],
           'Остаются последние два: [2, 3].'),
    ])


def code_collections():
    return ts('Модуль collections', [
        task('Топ-3 слова. На вход подаётся текст. Выведи три самых частых слова (в нижнем регистре) в виде «слово: N», '
             'по убыванию частоты; при равной частоте Counter.most_common сохраняет порядок первого появления.',
             'Counter(text.lower().split()).most_common(3) и цикл с распаковкой пар.',
             'from collections import Counter\nfor w, n in Counter(input().lower().split()).most_common(3):\n    print(f"{w}: {n}")',
             ['кот пёс кот Кот ёж пёс', 'один', 'а б в г']),
        task('История браузера хранит последние 3 открытые страницы. На вход подаются адреса по одному в строке, последняя строка — '
             '«стоп». Выведи последние три (или меньше) от новой к старой.',
             'deque(maxlen=3), append для каждой; в конце list(reversed(h)) или перебор reversed(h).',
             'from collections import deque\nh = deque(maxlen=3)\nwhile True:\n    s = input()\n    if s == "стоп":\n        break\n    h.append(s)\nfor url in reversed(h):\n    print(url)',
             ['itp.school\nya.ru\nwiki.org\nnews.ru\nстоп', 'one.ru\nстоп']),
        task('Анаграммы. На вход подаются слова через пробел. Сгруппируй слова, составленные из одних и тех же букв, и выведи '
             'группы, где больше одного слова: слова группы через пробел в порядке ввода, группы — в порядке появления первого слова.',
             'Ключ группы — "".join(sorted(w)). groups = defaultdict(list); groups[key].append(w). Словарь хранит порядок появления ключей.',
             'from collections import defaultdict\ngroups = defaultdict(list)\nfor w in input().split():\n    groups["".join(sorted(w))].append(w)\nfor g in groups.values():\n'
             '    if len(g) > 1:\n        print(*g)',
             ['кот ток пила липа кто апельсин', 'рост сорт торс трос', 'сон нос лес']),
        task('Лента убийств. На вход подаются события «УБИЙЦА ЖЕРТВА» до слова «стоп». На экране матча видно только три '
             'последних события. Выведи их — самое новое первым — в виде «УБИЙЦА ✕ ЖЕРТВА», а последней строкой лидера матча '
             '«Лидер: НИК (N)»; при равенстве — того, кто раньше других впервые появился в ленте как убийца.',
             'deque(maxlen=3) сам выбрасывает старое; новое — appendleft, тогда вывод идёт по порядку. Счёт — Counter, '
             'лидер — most_common(1): при равенстве он оставляет того, кто встретился раньше.',
             'from collections import deque, Counter\nfeed = deque(maxlen=3)\nkills = Counter()\nwhile True:\n    s = input()\n    if s == "стоп":\n        break\n'
             '    a, b = s.split()\n    feed.appendleft(f"{a} ✕ {b}")\n    kills[a] += 1\nfor e in feed:\n    print(e)\nname, n = kills.most_common(1)[0]\nprint(f"Лидер: {name} ({n})")',
             ['Кира Zed\nZed Ян\nКира Ян\nЛи Кира\nстоп', 'А Б\nстоп', 'Б А\nА Б\nстоп']),
    ])


def code_final():
    return ts('Задачи: испытание', [
        task('Очередь к кассам. На вход подаются события, по одному в строке, последняя — «стоп»: '
             '«пришёл ИМЯ» — человек встаёт в очередь, «касса» — освободилась касса и берёт первого в очереди, '
             '«vip ИМЯ» — человек встаёт в начало очереди. Для каждой «кассы» выведи «Обслужен ИМЯ» или «Очередь пуста». '
             'В конце выведи «Осталось: N».',
             'deque: append для «пришёл», appendleft для «vip», popleft для «касса». Команду разбери через parts = s.split(): '
             'parts[0] — действие, parts[1] — имя.',
             'from collections import deque\nq = deque()\nwhile True:\n    s = input()\n    if s == "стоп":\n        break\n    parts = s.split()\n'
             '    if parts[0] == "пришёл":\n        q.append(parts[1])\n    elif parts[0] == "vip":\n        q.appendleft(parts[1])\n'
             '    elif q:\n        print("Обслужен", q.popleft())\n    else:\n        print("Очередь пуста")\nprint(f"Осталось: {len(q)}")',
             ['пришёл Ира\nпришёл Ли\nvip Ким\nкасса\nкасса\nстоп', 'касса\nстоп', 'пришёл Оля\nкасса\nкасса\nстоп']),
    ])


def build():
    return topic('Инструменты для коллекций', 'iter, next, itertools, Counter, deque', [
        th_iter(), fl_iter(), code_iter(),
        th_itertools(), fl_itertools(), code_itertools(),
        th_collections(), fl_collections(), code_collections(),
        code_final(),
    ])
