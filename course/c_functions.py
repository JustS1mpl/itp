from dsl import *

# Тема 14 «Свои функции». Ученик знает всё до словарей и множеств.
# Три теории: def и параметры; return и None; области видимости (local, global, UnboundLocalError) и подсказки типов.
# Задачи на функции проверяются скрытым хвостом TL: тест — код вызова, который проверка выполняет после решения.


def th_def():
    terms = [
        ('def',
         'Объявление своей функции: def ИМЯ(параметры): и блок с отступом. Код блока выполняется только при вызове ИМЯ(аргументы). '
         'Функцию нужно объявить до первого вызова.\n'
         'Пример:\ndef hello(name):\n    print(f"Привет, {name}!")\n\nhello("Ира")\nhello("Ли")\nВывод:\nПривет, Ира!\nПривет, Ли!'),
    ]
    body = (
        '<p>До сих пор мы пользовались готовыми функциями: <code>print</code>, <code>len</code>, <code>sorted</code>. '
        'Теперь будем писать свои. Функция — именованный кусок кода, который можно вызывать сколько угодно раз. '
        'Объявляют её словом [[def]]:</p>'
        + ex('def line(sym, n):\n    print(sym * n)\n\nline("=", 20)\nprint("  Таблица рекордов")\nline("=", 20)\nline("-", 5)') +
        '<p>Строка <code>def line(sym, n):</code> ничего не выполняет — она только запоминает функцию. Код внутри работает '
        'при каждом вызове <code>line(...)</code>. <code>sym</code> и <code>n</code> — <b>параметры</b>: имена, '
        'под которыми функция получает переданные ей аргументы. Аргументы подставляются по порядку: первый — в <code>sym</code>, '
        'второй — в <code>n</code>.</p>'
        '<h3>Зачем</h3>'
        '<ul>'
        '<li>Не повторять код: одна функция вместо трёх одинаковых кусков.</li>'
        '<li>Дать действию имя: <code>print_receipt(order)</code> читается проще, чем двадцать строк.</li>'
        '<li>Исправлять в одном месте: ошибку в функции чинишь один раз.</li>'
        '</ul>'
        '<p>Функции вызывают другие функции. Объявить функцию нужно до того, как её вызовут, — Python читает файл сверху вниз:</p>'
        + ex('def line(sym, n):\n    print(sym * n)\n\ndef card(title, value):\n    line("*", 16)\n    print(f"{title:^16}")\n    print(f"{value:^16}")\n    line("*", 16)\n\ncard("Уровень", 7)') +
        '<p>Между функциями и основной программой принято оставлять пустую строку — так код легче читать.</p>'
    )
    return th('Свои функции', terms, body)


def fl_def():
    return fl('Свои функции', [
        qo('Что выведет программа?', 'def hi():\n    print("hi")\n\nprint("start")', ['hi start', 'hi', 'Ошибка'],
           'Функция объявлена, но не вызвана — выводится только start.'),
        qo('Что выведет программа?', 'def twice(w):\n    print(w * 2, end=" ")\n\ntwice("ля")\ntwice("о")', ['ляля', 'ля о', 'twice twice'],
           'Каждый вызов выполняет тело функции со своим аргументом: ляля оо.'),
        q('Что будет, если вызвать функцию строкой выше её def?', 'NameError: функция ещё не известна',
          ['Всё сработает', 'SyntaxError'], 'Python читает код сверху вниз, имя функции появляется только после def.'),
    ])


def code_def():
    return ts('Свои функции', [
        task('Напиши функцию frame(text, sym), которая выводит текст в рамке: строка из символа sym длиной на 4 больше текста, '
             'затем sym, пробел, текст, пробел, sym, и снова строка из sym. Функция ничего не возвращает.',
             'def frame(text, sym):\n    line = sym * (len(text) + 4)\n    print(line) ... и строка f"{sym} {text} {sym}".',
             'def frame(text, sym):\n    line = sym * (len(text) + 4)\n    print(line)\n    print(f"{sym} {text} {sym}")\n    print(line)',
             ['frame("ИТП", "*")', 'frame("Рекорд!", "#")', 'frame("", "=")'], tail=TL),
        task('Напиши функцию countdown(n), которая выводит обратный отсчёт от n до 1 через пробел и затем «Старт!» на той же строке.',
             'Цикл for i in range(n, 0, -1): print(i, end=" "), после него print("Старт!").',
             'def countdown(n):\n    for i in range(n, 0, -1):\n        print(i, end=" ")\n    print("Старт!")',
             ['countdown(3)', 'countdown(1)', 'countdown(5)\ncountdown(2)'], tail=TL),
        task('Напиши функцию leaderboard(names, scores), которая получает два списка одинаковой длины и выводит таблицу: '
             'номер места, точка, имя в поле шириной 12 влево и очки в поле шириной 5 вправо — от лучшего к худшему, '
             'при равных очках — по алфавиту. Пробелы проверяются точно.',
             'Пары (-очки, имя) в список, sorted, затем for place, (s, name) in enumerate(..., 1): print(f"{place}. {name:<12}{-s:>5}").',
             'def leaderboard(names, scores):\n    pairs = []\n    for n, s in zip(names, scores):\n        pairs.append((-s, n))\n'
             '    for place, (s, n) in enumerate(sorted(pairs), 1):\n        print(f"{place}. {n:<12}{-s:>5}")',
             ['leaderboard(["Ира", "Ли", "Тимур"], [40, 75, 60])', 'leaderboard(["Ким"], [7])'], tail=TL, strict=True),
        task('Напиши функцию hp_bar(hp, max_hp), которая печатает полоску здоровья из 10 клеток: «[####......] 40/100». '
             'Заполненных клеток — hp * 10 // max_hp.',
             'full = hp * 10 // max_hp, затем print("[" + "#" * full + "." * (10 - full) + "]", f"{hp}/{max_hp}").',
             'def hp_bar(hp, max_hp):\n    full = hp * 10 // max_hp\n    print("[" + "#" * full + "." * (10 - full) + "]", f"{hp}/{max_hp}")',
             ['hp_bar(40, 100)', 'hp_bar(100, 100)\nhp_bar(0, 7)', 'hp_bar(5, 9)'], tail=TL),
    ])


def th_return():
    terms = [
        ('return',
         'Возвращает значение из функции туда, где её вызвали, и сразу завершает функцию. Через запятую можно вернуть '
         'несколько значений — они придут кортежем.\n'
         'Пример:\ndef square(x):\n    return x * x\n\nprint(square(4) + 1)\nВывод:\n17'),
        ('None',
         'Особое значение «ничего». Его возвращает функция без return (или с пустым return). '
         'Проверить можно сравнением: r == None.\n'
         'Пример:\ndef hi():\n    print("hi")\n\nr = hi()\nprint(r)\nВывод:\nhi\nNone'),
    ]
    body = (
        '<p>Функции из прошлого островка печатали результат. Но чаще результат нужен программе — чтобы сложить, сравнить, '
        'сохранить. Для этого функция его <b>возвращает</b> словом [[return]]:</p>'
        + ex('def average(nums):\n    return sum(nums) / len(nums)\n\nmy = average([5, 4, 4])\nfriend = average([5, 5, 3])\nprint(round(my, 2), my > friend)') +
        '<p><code>average([5, 4, 4])</code> вычисляется в число, как <code>len</code> или <code>max</code>: его можно положить '
        'в переменную, округлить, сравнить. <code>return</code> сразу завершает функцию — строки после него не выполняются. '
        'Этим пользуются для раннего выхода:</p>'
        + ex('def grade(score):\n    if score >= 85:\n        return 5\n    if score >= 70:\n        return 4\n    return 3\n\nprint(grade(90), grade(72), grade(10))') +
        '<h3>Несколько значений</h3>'
        '<p>Через запятую можно вернуть несколько значений — придёт кортеж, его удобно распаковать:</p>'
        + ex('def min_max(nums):\n    return min(nums), max(nums)\n\nlo, hi = min_max([7, 2, 9, 4])\nprint(lo, hi)') +
        '<h3>print или return</h3>'
        '<p>Частая путаница. <code>print</code> показывает значение человеку, <code>return</code> отдаёт его программе. '
        'Функция без <code>return</code> возвращает [[None]] — особое значение «ничего»:</p>'
        + ex('def show_sum(a, b):\n    print(a + b)\n\ndef get_sum(a, b):\n    return a + b\n\nx = show_sum(2, 3)\ny = get_sum(2, 3)\nprint(x, y)') +
        '<p><code>show_sum</code> напечатала 5, но вернула <code>None</code>, поэтому в <code>x</code> — «ничего». '
        'Если результат нужен дальше — возвращай, а печатай снаружи.</p>'
    )
    return th('return и None', terms, body)


def fl_return():
    return fl('return и None', [
        qo('Что выведет программа?', 'def f(x):\n    return x + 1\n    print("после")\n\nprint(f(1))', ['после 2', 'после', 'None'],
           'return завершает функцию, print после него не выполнится: 2.'),
        qo('Что выведет программа?', 'def f():\n    x = 5\n\nprint(f())', ['5', 'x', 'Ошибка'], 'return нет — функция возвращает None.'),
        qo('Что выведет программа?', 'def pair():\n    return 1, 2\n\na, b = pair()\nprint(b - a)', ['-1', '(1, 2)', '3'], 'Распаковали 1 и 2: 2 - 1 = 1.'),
    ])


def code_return():
    return ts('return и None', [
        task('Напиши функцию is_palindrome(word), которая возвращает True, если слово читается одинаково в обе стороны '
             'без учёта регистра, иначе False.',
             'w = word.lower(), затем return w == w[::-1].',
             'def is_palindrome(word):\n    w = word.lower()\n    return w == w[::-1]',
             ['print(is_palindrome("Шалаш"))', 'print(is_palindrome("кот"))', 'print(is_palindrome("а"), is_palindrome("Радар"))'], tail=TL),
        task('Напиши функцию stats(nums), которая возвращает три значения: среднее, округлённое до двух знаков, минимум и максимум.',
             'return round(sum(nums) / len(nums), 2), min(nums), max(nums).',
             'def stats(nums):\n    return round(sum(nums) / len(nums), 2), min(nums), max(nums)',
             ['print(stats([5, 4, 4]))', 'avg, lo, hi = stats([10, -2, 7, 1])\nprint(avg, hi - lo)', 'print(stats([3]))'], tail=TL),
        task('Напиши функцию find_word(words, target), которая возвращает номер первого вхождения target в список (с нуля) '
             'или None, если такого слова нет. Метод index не используй — пройди циклом.',
             'for i, w in enumerate(words): if w == target: return i. После цикла — return None.',
             'def find_word(words, target):\n    for i, w in enumerate(words):\n        if w == target:\n            return i\n    return None',
             ['print(find_word(["кот", "пёс", "кот"], "кот"))', 'print(find_word(["а", "б"], "в"))', 'print(find_word(["x", "y", "z"], "z"))'], tail=TL),
        task('Напиши функцию rank(points), которая по числу очков возвращает звание: меньше 100 — «новичок», меньше 500 — '
             '«боец», меньше 2000 — «ветеран», иначе — «легенда». И функцию report(names_points), которая получает список '
             'пар (ник, очки) и возвращает список строк «НИК — ЗВАНИЕ», вызывая rank.',
             'rank — цепочка if с return в каждой ветке. report: собери result.append(f"{name} — {rank(p)}") и верни result.',
             'def rank(points):\n    if points < 100:\n        return "новичок"\n    if points < 500:\n        return "боец"\n'
             '    if points < 2000:\n        return "ветеран"\n    return "легенда"\n\n\ndef report(names_points):\n    result = []\n'
             '    for name, p in names_points:\n        result.append(f"{name} — {rank(p)}")\n    return result',
             ['print(rank(99), rank(100), rank(2000))', 'print(report([("Кира", 450), ("Zed", 3000)]))', 'print(report([]))'], tail=TL),
    ])


def th_scope():
    terms = [
        ('global',
         'Объявляет внутри функции, что имя относится к глобальной переменной, — тогда её можно изменять. '
         'Пользоваться осторожно: функции, меняющие глобальные переменные, трудно проверять.\n'
         'Пример:\ncount = 0\ndef click():\n    global count\n    count += 1\n\nclick()\nclick()\nprint(count)\nВывод:\n2'),
        ('UnboundLocalError',
         'Ошибка: функция пытается прочитать локальную переменную, которой ещё не присвоено значение. Частая причина — '
         'изменение глобальной переменной внутри функции без global.\n'
         'Текст: cannot access local variable \'count\' where it is not associated with a value.'),
        ('подсказка типа',
         'Пометка, какого типа ожидаются параметры и результат: def f(x: int, name: str) -> float:. '
         'Python её не проверяет — она для людей и редакторов кода. Без подсказок функция работает так же.\n'
         'Пример:\ndef area(w: float, h: float) -> float:\n    return w * h\n\nprint(area(2, 3.5))\nВывод:\n7.0'),
    ]
    body = (
        '<h3>Локальные и глобальные переменные</h3>'
        '<p>Переменные, созданные внутри функции (в том числе параметры), — <b>локальные</b>: они существуют только во время её '
        'работы и снаружи не видны. Переменные основной программы — <b>глобальные</b>: функция может их читать.</p>'
        + ex('rate = 90\n\ndef rub(dollars):\n    result = dollars * rate\n    return result\n\nprint(rub(3))\nprint(rate)') +
        '<p>Функция прочитала глобальную <code>rate</code>, а её локальная <code>result</code> исчезла после <code>return</code> — '
        'обратиться к ней снаружи нельзя.</p>'
        '<p>А вот изменить глобальную переменную простым присваиванием внутри функции нельзя: присваивание делает имя '
        'локальным для всей функции, и Python не даст прочитать его до присваивания:</p>'
        + exerr('count = 0\n\ndef click():\n    count += 1\n\nclick()') +
        '<p>[[UnboundLocalError]]. Слово [[global]] разрешает менять глобальную переменную, но лучше так не делать: '
        'функции, которые тайно меняют что-то снаружи, трудно понимать и проверять. Правильный путь — передать значение '
        'параметром и вернуть результат: <code>count = click(count)</code>.</p>'
        + ex('def click(count):\n    return count + 1\n\ncount = 0\ncount = click(count)\ncount = click(count)\nprint(count)') +
        '<h3>Подсказки типов</h3>'
        '<p>В объявлении функции можно указать, какие типы ожидаются, — это [[подсказка типа|подсказки типов]]: '
        'двоеточие и тип после параметра, стрелка <code>-&gt;</code> и тип результата. Python их не проверяет, '
        'зато сразу видно, что передавать и что вернётся. Они понадобятся нам в итоговом проекте:</p>'
        + ex('def price_with_discount(price: float, percent: int) -> float:\n    return round(price * (100 - percent) / 100, 2)\n\nprint(price_with_discount(599.0, 15))') +
        '<p><code>(price: float, percent: int) -&gt; float</code> читается как «принимает дробную цену и целый процент, '
        'возвращает дробное число».</p>'
    )
    return th('Области видимости и подсказки типов', terms, body)


def fl_scope():
    return fl('Области видимости и подсказки типов', [
        qo('Что выведет программа?', 'x = 1\n\ndef f():\n    x = 5\n    return x\n\nprint(f(), x)', ['5 5', '1 1', 'Ошибка'],
           'x внутри f — своя, локальная. Глобальная x осталась 1: 5 1.'),
        q('Что случится при вызове f()?', 'UnboundLocalError', ['Выведется 1', 'Выведется 0'],
          'Присваивание делает total локальной, а прочитать её до присваивания нельзя.',
          c='total = 0\n\ndef f():\n    total += 1\n    print(total)\n\nf()'),
        q('Что сделает Python, если в функцию def f(x: int) передать строку?', 'Выполнит функцию как обычно',
          ['Выдаст TypeError сразу при вызове', 'Превратит строку в int'], 'Подсказки типов Python не проверяет.'),
    ])


def code_scope():
    return ts('Области видимости и подсказки типов', [
        task('Функция add_score должна прибавлять очки к счёту и возвращать новый счёт, но падает с UnboundLocalError. '
             'Перепиши её без global: пусть принимает текущий счёт и очки и возвращает новое значение. Объявление начни так: '
             'def add_score(score: int, points: int) -> int:',
             'Никаких внешних переменных внутри: return score + points.',
             'def add_score(score: int, points: int) -> int:\n    return score + points',
             ['s = 0\ns = add_score(s, 10)\ns = add_score(s, 5)\nprint(s)', 'print(add_score(100, -30))'], tail=TL,
             starter='score = 0\n\ndef add_score(points):\n    score += points\n    return score', fix=True),
        task('Напиши функцию bmi(weight: float, height: float) -> float, которая возвращает индекс массы тела — вес в килограммах, '
             'делённый на квадрат роста в метрах, — округлённый до одного знака.',
             'return round(weight / height ** 2, 1).',
             'def bmi(weight: float, height: float) -> float:\n    return round(weight / height ** 2, 1)',
             ['print(bmi(60, 1.7))', 'print(bmi(45.5, 1.58))', 'print(bmi(80, 2))'], tail=TL),
        task('Напиши функцию word_count(text: str) -> dict, которая возвращает словарь «слово: сколько раз встречается» '
             '(без учёта регистра).',
             'd = {}; for w in text.lower().split(): d[w] = d.get(w, 0) + 1; return d.',
             'def word_count(text: str) -> dict:\n    d = {}\n    for w in text.lower().split():\n        d[w] = d.get(w, 0) + 1\n    return d',
             ['print(word_count("Мама мыла раму мама"))', 'd = word_count("a A a b")\nprint(d["a"], d.get("c", 0))'], tail=TL),
        task('Счётчик достижений. В программе есть глобальный словарь unlocked и глобальный счётчик score. Напиши функцию '
             'unlock(name, points): если достижение name ещё не открыто, запиши его в словарь с очками, прибавь очки '
             'к score и верни True; иначе верни False.',
             'Словарь меняется методами и без global, а вот score += … внутри функции требует global score.',
             'unlocked = {}\nscore = 0\n\n\ndef unlock(name, points):\n    global score\n    if name in unlocked:\n        return False\n'
             '    unlocked[name] = points\n    score += points\n    return True',
             ['print(unlock("Первая кровь", 10), unlock("Первая кровь", 10), score)',
              'unlock("Фермер", 5)\nunlock("Рыбак", 7)\nprint(score, unlocked)', 'print(score, unlocked)'], tail=TL, starter='unlocked = {}\nscore = 0\n'),
    ])


def code_final():
    return ts('Задачи: испытание', [
        task('Напиши две функции. format_time(seconds: int) -> str возвращает время в виде «ЧЧ:ММ:СС» (с нулями). '
             'race_report(names: list, times: list) -> str возвращает строку «Победил ИМЯ за ЧЧ:ММ:СС» для участника '
             'с наименьшим временем (при равенстве — первый). Вторая функция должна пользоваться первой.',
             'format_time: h = seconds // 3600, m = seconds % 3600 // 60, s = seconds % 60, return f"{h:02}:{m:02}:{s:02}". '
             'race_report: индекс победителя i = times.index(min(times)), return f"Победил {names[i]} за {format_time(times[i])}".',
             'def format_time(seconds: int) -> str:\n    h = seconds // 3600\n    m = seconds % 3600 // 60\n    s = seconds % 60\n    return f"{h:02}:{m:02}:{s:02}"\n\n'
             'def race_report(names: list, times: list) -> str:\n    i = times.index(min(times))\n    return f"Победил {names[i]} за {format_time(times[i])}"',
             ['print(race_report(["Ира", "Ли", "Ким"], [4000, 3725, 5100]))\nprint(format_time(59))', 'print(format_time(3725))',
              'print(format_time(86399))\nprint(race_report(["Оля", "Макс"], [600, 600]))'], tail=TL),
    ])


def build():
    return topic('Свои функции', 'def, return, None, области видимости', [
        th_def(), fl_def(), code_def(),
        th_return(), fl_return(), code_return(),
        th_scope(), fl_scope(), code_scope(),
        code_final(),
    ])
