from dsl import *

# Тема 19 «Модули». Ученик знает import math и from … import, функции, исключения, коллекции.
# Три теории: import … as и random (с seed для воспроизводимости); datetime; свои модули, __name__, string.
# В примерах и тестах нет «сегодня» и случайности без seed: вывод должен совпадать при любом запуске.


def th_random():
    terms = [
        ('as', 'Даёт модулю или имени короткое название при подключении: import datetime as dt, from math import sqrt as root.'),
        ('random', 'Модуль случайных чисел: randint, choice, shuffle, seed и другие. Числа псевдослучайные: их выдаёт формула, '
                   'и при одинаковом seed последовательность одинаковая.'),
        ('randint', 'random.randint(a, b) — случайное целое от a до b включительно.\nПример:\nimport random\nrandom.seed(1)\nprint(random.randint(1, 6))\nВывод:\n2'),
        ('choice', 'random.choice(набор) — случайный элемент списка или строки.\nПример:\nimport random\nrandom.seed(5)\nprint(random.choice(["камень", "ножницы", "бумага"]))\nВывод:\nбумага'),
        ('shuffle', 'random.shuffle(список) — перемешивает сам список, ничего не возвращает.\nПример:\nimport random\nrandom.seed(2)\ncards = [1, 2, 3, 4]\nrandom.shuffle(cards)\nprint(cards)\nВывод:\n[2, 3, 4, 1]'),
        ('math.factorial', 'Факториал: n! = 1 · 2 · … · n.\nПример:\nimport math\nprint(math.factorial(5))\nВывод:\n120'),
        ('seed', 'random.seed(n) — задаёт начальное значение: после одинакового seed случайные числа идут в одном и том же порядке. '
                 'Нужно для повторяемых опытов и тестов.'),
    ]
    body = (
        '<h3>Способы подключить модуль</h3>'
        '<p>Мы уже видели <code>import math</code> и <code>from functools import reduce</code>. Ещё можно дать модулю '
        'или функции короткое имя словом [[as]] и подключить сразу несколько имён:</p>'
        + ex('import math as m\nfrom math import sqrt, pi\nfrom math import factorial as fact\nprint(m.floor(2.7), sqrt(16), round(pi, 3), fact(5))') +
        '<p>Здесь заодно новая функция [[math.factorial|factorial]] — произведение чисел от 1 до n.</p>'
        '<p><code>from модуль import *</code> подключает всё сразу — так делать не стоит: непонятно, откуда взялось имя, '
        'и чужое имя может затереть твоё.</p>'
        '<h3>Модуль random</h3>'
        '<p>Модуль [[random]] даёт случайные числа: [[randint]] — целое из диапазона, [[choice]] — случайный элемент, '
        '[[shuffle]] — перемешать список. Эти числа <b>псевдослучайные</b>: их вычисляет формула из начального значения. '
        'Если задать его через [[seed]], последовательность будет одинаковой при каждом запуске:</p>'
        + ex('import random\nrandom.seed(42)\nprint(random.randint(1, 6), random.randint(1, 6), random.randint(1, 6))\n'
             'print(random.choice(["Ира", "Ли", "Ким"]))\nteam = ["А", "Б", "В", "Г"]\nrandom.shuffle(team)\nprint(team)\n'
             'random.seed(42)\nprint(random.randint(1, 6))') +
        '<p>После повторного <code>seed(42)</code> первое число снова то же. Без <code>seed</code> числа при каждом запуске разные — '
        'так и нужно в играх, но в задачах проверка задаёт <code>seed</code>, чтобы ответ можно было сравнить.</p>'
    )
    return th('import … as и random', terms, body)


def fl_random():
    return fl('import … as и random', [
        qo('Что выведет программа?', 'import math as mt\nprint(mt.ceil(1.2))', ['1', 'mt', 'Ошибка'], 'mt — другое имя модуля math: ceil(1.2) = 2.'),
        q('Что даст random.randint(1, 3)?', 'Одно из чисел 1, 2 или 3', ['Одно из чисел 1 или 2', 'Список [1, 2, 3]'], 'Оба конца включены.'),
        q('Зачем нужен random.seed(7)?', 'Чтобы числа шли в одном порядке при каждом запуске',
          ['Чтобы числа были больше 7', 'Чтобы выбрать 7 случайных чисел'], 'seed задаёт начальное значение формулы.'),
    ])


def code_random():
    return ts('import … as и random', [
        task('Кубики. На вход подаются seed (целое число) и сколько раз бросить два кубика, каждое в отдельной строке ввода. Выведи суммы бросков '
             'через пробел, а следующей строкой — «Дублей: N» (сколько раз выпали одинаковые числа). В каждом броске сначала '
             'первый кубик, потом второй — randint(1, 6).',
             'random.seed(s); в цикле a = random.randint(1, 6), b = random.randint(1, 6); копи суммы в список, считай a == b.',
             'import random\nrandom.seed(int(input()))\nn = int(input())\nsums = []\ndoubles = 0\nfor i in range(n):\n    a = random.randint(1, 6)\n'
             '    b = random.randint(1, 6)\n    sums.append(a + b)\n    if a == b:\n        doubles += 1\nprint(*sums)\nprint(f"Дублей: {doubles}")',
             ['1\n5', '42\n10', '7\n1']),
        task('Жеребьёвка. На вход подаются seed (целое число) и имена игроков через пробел, игроков не меньше двух. Перемешай список shuffle и раздели: первая половина '
             '(при нечётном числе — на одного меньше) — «Синие: ...», остальные — «Красные: ...».',
             'random.seed(s); names = input().split(); random.shuffle(names); k = len(names) // 2; срезы names[:k] и names[k:].',
             'import random\nrandom.seed(int(input()))\nnames = input().split()\nrandom.shuffle(names)\nk = len(names) // 2\n'
             'print("Синие:", " ".join(names[:k]))\nprint("Красные:", " ".join(names[k:]))',
             ['3\nИра Ли Ким Оля', '10\nА Б В Г Д', '1\nсоло пара']),
        task('Камень-ножницы-бумага. На вход подаются seed (целое число) и ход игрока («камень», «ножницы» или «бумага»). Компьютер выбирает '
             'random.choice из ["камень", "ножницы", "бумага"]. Выведи «Компьютер: ХОД» и «Победа», «Поражение» или «Ничья».',
             'Словарь «кто кого бьёт»: beats = {"камень": "ножницы", "ножницы": "бумага", "бумага": "камень"}. '
             'Победа, если beats[игрок] == компьютер.',
             'import random\nrandom.seed(int(input()))\nme = input()\ncomp = random.choice(["камень", "ножницы", "бумага"])\n'
             'beats = {"камень": "ножницы", "ножницы": "бумага", "бумага": "камень"}\nprint(f"Компьютер: {comp}")\n'
             'if me == comp:\n    print("Ничья")\nelif beats[me] == comp:\n    print("Победа")\nelse:\n    print("Поражение")',
             ['1\nкамень', '2\nбумага', '5\nножницы', '9\nкамень']),
        task('Сундук с лутом. На вход подаются число seed и число открытий n. Задай random.seed(seed) и для каждого открытия '
             'брось число от 1 до 100: от 95 — «легендарный», от 70 — «редкий», иначе «обычный». Выведи «N: ЧИСЛО — РЕДКОСТЬ», '
             'а в конце «Легендарных: K».',
             'random.randint(1, 100) в цикле, редкость — цепочкой if/elif. Seed задай один раз до цикла.',
             'import random\nseed = int(input())\nn = int(input())\nrandom.seed(seed)\nlegend = 0\nfor i in range(1, n + 1):\n'
             '    x = random.randint(1, 100)\n    if x >= 95:\n        kind = "легендарный"\n        legend += 1\n    elif x >= 70:\n        kind = "редкий"\n'
             '    else:\n        kind = "обычный"\n    print(f"{i}: {x} — {kind}")\nprint(f"Легендарных: {legend}")',
             ['7\n5', '42\n3', '2077\n10']),
    ])


def th_datetime():
    terms = [
        ('datetime', 'Модуль дат и времени. В нём классы date (дата), datetime (дата и время), timedelta (промежуток).'),
        ('date', 'Дата: date(год, месяц, день). Даты можно сравнивать и вычитать — разность будет timedelta.\n'
                 'Пример:\nfrom datetime import date\nd = date(2026, 9, 1)\nprint(d.year, d.month, d.day, d.weekday())\nВывод:\n2026 9 1 1'),
        ('timedelta', 'Промежуток времени: timedelta(days=…, hours=…, minutes=…). Прибавляется к дате; .days — сколько дней.\n'
                      'Пример:\nfrom datetime import date, timedelta\nprint(date(2026, 12, 30) + timedelta(days=5))\nВывод:\n2027-01-04'),
        ('strftime', 'Метод даты: превращает её в строку по шаблону. %d — день, %m — месяц, %Y — год, %H:%M — часы и минуты.\n'
                     'Пример:\nfrom datetime import date\nprint(date(2026, 3, 8).strftime("%d.%m.%Y"))\nВывод:\n08.03.2026'),
        ('strptime', 'datetime.strptime(строка, шаблон) — обратное: разбирает строку в дату-время по шаблону. '
                     'Если строка не подходит — ValueError.\n'
                     'Пример:\nfrom datetime import datetime\nd = datetime.strptime("08.03.2026", "%d.%m.%Y")\nprint(d.year)\nВывод:\n2026'),
        ('weekday', 'Метод даты: день недели числом, 0 — понедельник, 6 — воскресенье.\n'
                    'Пример:\nfrom datetime import date\nprint(date(2026, 9, 1).weekday())\nВывод:\n1'),
        ('today', 'date.today() — сегодняшняя дата по часам устройства, datetime.now() — текущие дата и время. '
                  'Результат каждый день разный, поэтому в задачах дату дают во вводе.'),
    ]
    body = (
        '<p>Модуль [[datetime]] работает с датами и временем: [[date]] — дата, класс <code>datetime</code> — дата и время, '
        '[[timedelta]] — промежуток. Сегодняшнюю дату даёт <code>date.today()</code> ([[today]]), но её вывод меняется каждый день, '
        'поэтому в примерах даты заданы явно:</p>'
        + ex('from datetime import date, timedelta\nstart = date(2026, 9, 1)\nend = date(2027, 5, 25)\nprint(start, end)\n'
             'print((end - start).days, "дней учёбы")\nprint(start + timedelta(days=100))\nprint(start.weekday())') +
        '<p>Даты сравнивают и вычитают, как числа; разность — <code>timedelta</code>, а <code>.days</code> даёт число дней. '
        '[[weekday]]<code>()</code> — день недели числом: 0 — понедельник, 6 — воскресенье.</p>'
        '<h3>Строки и даты</h3>'
        '<p>[[strftime]] превращает дату в строку по шаблону, [[strptime]] — разбирает строку в дату. В шаблоне '
        '<code>%d</code> — день, <code>%m</code> — месяц, <code>%Y</code> — год, <code>%H</code> и <code>%M</code> — часы и минуты:</p>'
        + ex('from datetime import datetime\nlesson = datetime(2026, 10, 27, 14, 5)\nprint(lesson.strftime("%d.%m.%Y %H:%M"))\n'
             'd = datetime.strptime("31.12.2026", "%d.%m.%Y")\nprint(d.date(), d.month)') +
        '<p><code>strptime</code> возвращает дату со временем (datetime); если нужна только дата, у неё есть метод <code>.date()</code>. '
        'Если строка не подходит под шаблон (например, «31.02.2026» или «вчера»), <code>strptime</code> выдаст ValueError — '
        'его ловят, как любую ошибку ввода.</p>'
    )
    return th('Дата и время', terms, body)


def fl_datetime():
    return fl('Дата и время', [
        qo('Что выведет программа?', 'from datetime import date\nprint((date(2026, 3, 1) - date(2026, 2, 1)).days)', ['30', '31', '1'], 'В феврале 2026 года 28 дней.'),
        qo('Что выведет программа?', 'from datetime import date, timedelta\nprint(date(2026, 1, 31) + timedelta(days=1))', ['2026-01-32', '2026-02-31', 'Ошибка'],
           'Дата сама переходит через конец месяца: 2026-02-01.'),
        qo('Что выведет программа?', 'from datetime import date\nprint(date(2026, 5, 9).strftime("%d/%m"))', ['9/5', '2026/05', '05/09'], '%d — день с нулём, %m — месяц: 09/05.'),
    ])


def code_datetime():
    return ts('Дата и время', [
        task('До дня рождения. На вход подаются сегодняшняя дата и дата ближайшего дня рождения в формате «ДД.ММ.ГГГГ», '
             'каждая в отдельной строке ввода. Выведи «Осталось дней: N» (если день рождения сегодня — «С днём рождения!»).',
             'datetime.strptime(s, "%d.%m.%Y").date() для обеих дат; разность .days.',
             'from datetime import datetime\nt = datetime.strptime(input(), "%d.%m.%Y").date()\nb = datetime.strptime(input(), "%d.%m.%Y").date()\n'
             'n = (b - t).days\nprint("С днём рождения!" if n == 0 else f"Осталось дней: {n}")',
             ['28.10.2026\n15.01.2027', '01.03.2028\n01.03.2028', '27.02.2028\n01.03.2028']),
        task('День недели. На вход подаётся дата «ДД.ММ.ГГГГ». Выведи день недели словом: понедельник, вторник и так далее.',
             'Список названий от понедельника и индекс d.weekday().',
             'from datetime import datetime\ndays = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]\n'
             'print(days[datetime.strptime(input(), "%d.%m.%Y").weekday()])',
             ['01.09.2026', '31.12.2026', '29.02.2028']),
        task('Дедлайн. На вход подаются дата выдачи проекта «ДД.ММ.ГГГГ» и срок в днях. Выведи дату сдачи в том же формате, '
             'а если она приходится на субботу или воскресенье — перенеси на ближайший понедельник.',
             'deadline = start + timedelta(days=n); пока weekday() >= 5 — прибавляй по дню; вывод через strftime("%d.%m.%Y").',
             'from datetime import datetime, timedelta\nstart = datetime.strptime(input(), "%d.%m.%Y")\nd = start + timedelta(days=int(input()))\n'
             'while d.weekday() >= 5:\n    d += timedelta(days=1)\nprint(d.strftime("%d.%m.%Y"))',
             ['01.09.2026\n10', '01.09.2026\n4', '25.12.2026\n7']),
        task('Серия входов в игру. На вход подаются даты входа «ДД.ММ.ГГГГ» по возрастанию, до слова «стоп»; в один день '
             'можно войти несколько раз. Выведи «Лучшая серия: N дн.» — самое длинное число дней подряд с входами.',
             'datetime.strptime(s, "%d.%m.%Y").date(). Разница соседних дат: 0 дней — тот же день, 1 день — серия растёт, '
             'больше — серия начинается заново.',
             'from datetime import datetime, timedelta\nprev = None\ncur = 0\nbest = 0\nwhile True:\n    s = input()\n    if s == "стоп":\n        break\n'
             '    d = datetime.strptime(s, "%d.%m.%Y").date()\n    if prev is None or d - prev > timedelta(days=1):\n        cur = 1\n'
             '    elif d - prev == timedelta(days=1):\n        cur += 1\n    prev = d\n    best = max(best, cur)\nprint(f"Лучшая серия: {best} дн.")',
             ['30.12.2026\n31.12.2026\n31.12.2026\n01.01.2027\n05.01.2027\nстоп', '01.03.2026\nстоп', '01.02.2024\n28.02.2024\n29.02.2024\n01.03.2024\nстоп']),
    ])


def th_own():
    terms = [
        ('string', 'Модуль с готовыми наборами символов: ascii_lowercase, ascii_uppercase, ascii_letters, digits, punctuation.\n'
                   'Пример:\nimport string\nprint(string.digits)\nВывод:\n0123456789'),
        ('ascii_lowercase', 'string.ascii_lowercase — строка латинских букв a…z (ascii_uppercase — большие).'),
        ('ascii_letters', 'string.ascii_letters — все латинские буквы, маленькие и большие.'),
        ('digits', 'string.digits — строка цифр 0123456789.'),
        ('punctuation', 'string.punctuation — знаки препинания и спецсимволы: !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'),
        ('__name__', 'Особая переменная: при запуске файла как программы в ней "__main__", а при импорте — имя модуля. '
                     'Код под if __name__ == "__main__": выполняется только при прямом запуске.'),
        ('ModuleNotFoundError', 'Ошибка подключения: модуля с таким именем нет. Текст: No module named \'…\'.'),
        ('ImportError', 'Ошибка подключения имени из модуля: модуль есть, а нужного имени в нём нет (from math import nothing).'),
    ]
    body = (
        '<h3>Свой модуль</h3>'
        '<p>Любой файл <code>.py</code> — это модуль. Функции, которые нужны в нескольких программах, выносят в отдельный файл '
        'и подключают по имени файла без <code>.py</code>. Допустим, рядом с программой лежит файл <code>geo.py</code>:</p>'
        '<pre>def area(w, h):\n    return w * h\n\ndef perimeter(w, h):\n    return 2 * (w + h)</pre>'
        + ex('import geo\nfrom geo import perimeter\nprint(geo.area(3, 4), perimeter(3, 4))',
             files={'geo.py': 'def area(w, h):\n    return w * h\n\ndef perimeter(w, h):\n    return 2 * (w + h)\n'}) +
        '<p>В задачах такие файлы уже лежат рядом с программой — они перечислены в условии.</p>'
        '<h3>__name__</h3>'
        '<p>При импорте Python <b>выполняет</b> весь файл модуля. Если в нём есть проверочные <code>print</code>, они '
        'сработают у того, кто модуль подключил. Код, который нужен только при прямом запуске файла, кладут под '
        '<code>if __name__ == "__main__":</code> — переменная [[__name__]] равна <code>"__main__"</code> у запущенной программы '
        'и имени модуля у подключённого:</p>'
        '<pre># geo.py\ndef area(w, h):\n    return w * h\n\nif __name__ == "__main__":\n    print(area(2, 3))  # проверка, только при запуске geo.py</pre>'
        '<h3>Модуль string и ошибки подключения</h3>'
        '<p>Модуль [[string]] хранит готовые наборы символов — [[ascii_lowercase]], [[ascii_letters]], [[digits]], '
        '[[punctuation]]. Удобно для проверок и генерации паролей:</p>'
        + ex('import string\nprint(string.ascii_lowercase)\nprint(string.digits)\npwd = "Kira_2010"\nprint(any(c in string.punctuation for c in pwd))') +
        '<p>Если модуля нет — [[ModuleNotFoundError]], если в модуле нет нужного имени — [[ImportError]]:</p>'
        + exerr('import maths')
    )
    return th('Свои модули', terms, body)


def fl_own():
    return fl('Свои модули', [
        q('Как подключить функции из файла tools.py, лежащего рядом с программой?', 'import tools', ['import tools.py', 'include tools'],
          'Модуль подключают по имени файла без .py.'),
        q('Чему равна __name__ в файле, который запустили как программу?', '"__main__"', ['Имени файла', 'None'],
          'У запущенной программы — "__main__", у подключённого модуля — его имя.'),
        qo('Что выведет программа?', 'import string\nprint(len(string.digits))', ['9', '0123456789', '26'], 'Цифр 10: от 0 до 9.'),
    ])


def code_own():
    return ts('Свои модули', [
        task('Рядом с программой лежит модуль grades.py с функцией to_word(mark), которая принимает оценку-число и возвращает её словом. '
             'На вход подаются оценки через пробел. Выведи каждую словом через запятую с пробелом, пользуясь этой функцией.',
             'from grades import to_word; print(", ".join(to_word(int(m)) for m in input().split())).',
             'from grades import to_word\nprint(", ".join(to_word(int(m)) for m in input().split()))',
             ['5 4 3', '2', '5 5 2 4'],
             files={'grades.py': 'def to_word(mark):\n    return {5: "отлично", 4: "хорошо", 3: "удовлетворительно", 2: "неудовлетворительно"}[mark]\n'}),
        task('Шифр по алфавиту. На вход подаётся слово из маленьких латинских букв. Выведи номера букв в алфавите (a — 1) через '
             'дефис. Алфавит возьми из модуля string, а не набирай вручную.',
             'string.ascii_lowercase.index(c) + 1 для каждой буквы; "-".join(...) — числа сначала в str.',
             'import string\nprint("-".join(str(string.ascii_lowercase.index(c) + 1) for c in input()))', ['abc', 'python', 'z']),
        task('Рядом с программой лежит модуль units.py с функциями km_to_miles(km) и c_to_f(c) — они возвращают числа. '
             'На вход подаются строки «число единица», где единица — km или C, последняя строка — «стоп». Для каждой выведи '
             'перевод, где оба числа — с одним знаком после точки: «5.0 km = 3.1 mi» или «20.0 C = 68.0 F».',
             'import units; для km — units.km_to_miles(x), для C — units.c_to_f(x). Число и единицу раздели split, число — float.',
             'import units\nwhile True:\n    s = input()\n    if s == "стоп":\n        break\n    num, unit = s.split()\n    x = float(num)\n'
             '    if unit == "km":\n        print(f"{x:.1f} km = {units.km_to_miles(x):.1f} mi")\n    else:\n        print(f"{x:.1f} C = {units.c_to_f(x):.1f} F")',
             ['5 km\n20 C\nстоп', '-40 C\nстоп', '42.195 km\n0 C\nстоп'],
             files={'units.py': 'def km_to_miles(km):\n    return km / 1.609344\n\n\ndef c_to_f(c):\n    return c * 9 / 5 + 32\n\n\n'
                                'if __name__ == "__main__":\n    print("проверка:", km_to_miles(1.609344), c_to_f(100))\n'}),
        task('Ник из любого текста. На вход подаётся строка. Сделай из неё ник: латинские буквы и цифры оставь (буквы — '
             'строчными), каждый другой символ замени на «_». Если ник начинается с цифры, допиши в начало «p». Выведи ник.',
             'Проверка символа: c in string.ascii_letters + string.digits. Собирай ник в строку, в конце — lower().',
             'import string\nnick = ""\nfor c in input():\n    if c in string.ascii_letters + string.digits:\n        nick += c\n    else:\n        nick += "_"\n'
             'nick = nick.lower()\nif nick[0] in string.digits:\n    nick = "p" + nick\nprint(nick)',
             ['Dark Knight!', '2077 Night', 'Кира pro', 'ok']),
    ])


def code_final():
    return ts('Задачи: испытание', [
        task('Генератор паролей. На вход подаются seed (целое число), длина пароля и строка-требование: «буквы», «буквы+цифры» или «всё» '
             '(буквы, цифры и знаки string.punctuation). Сгенерируй пароль: каждый символ — random.choice из нужного набора, '
             'наборы склеены в порядке буквы (string.ascii_letters), цифры, знаки. Выведи пароль.',
             'Набор: chars = string.ascii_letters, затем при необходимости += string.digits и += string.punctuation. '
             'Пароль: "".join(random.choice(chars) for i in range(n)) после random.seed(s).',
             'import random\nimport string\nrandom.seed(int(input()))\nn = int(input())\nmode = input()\nchars = string.ascii_letters\n'
             'if mode in ("буквы+цифры", "всё"):\n    chars += string.digits\nif mode == "всё":\n    chars += string.punctuation\n'
             'print("".join(random.choice(chars) for i in range(n)))',
             ['1\n8\nбуквы', '42\n12\nбуквы+цифры', '7\n16\nвсё']),
    ])


def build():
    return topic('Модули', 'import, from, random, datetime, свой модуль', [
        th_random(), fl_random(), code_random(),
        th_datetime(), fl_datetime(), code_datetime(),
        th_own(), fl_own(), code_own(),
        code_final(),
    ])
