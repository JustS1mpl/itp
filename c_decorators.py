from dsl import *

# Тема 23 «Декораторы и генераторы». Ученик знает функции как значения, *args/**kwargs, global и UnboundLocalError,
# итераторы и next, itertools (islice), рекурсию и @lru_cache (декоратор как использование).
# Три теории: замыкания и nonlocal; свои декораторы и wraps; функции-генераторы, yield и yield from.

LOG = '''08:00:01 INFO Сервер запущен
08:00:05 WARN Мало памяти: 12%
08:01:10 ERROR Нет связи с базой
08:01:12 INFO Повторное подключение к базе
08:01:15 ERROR Таймаут запроса /api/users
08:02:00 WARN Медленный ответ базы: 2300 мс
08:03:30 INFO Сохранено 154 записи
08:04:02 ERROR Таймаут запроса /api/orders
'''


def th_closure():
    terms = [
        ('замыкание', 'Вложенная функция, которая запомнила переменные внешней функции и пользуется ими, даже когда внешняя уже закончилась.\n'
                      'Пример:\ndef make_adder(n):\n    def add(x):\n        return x + n\n    return add\n\nplus5 = make_adder(5)\nprint(plus5(10))\nВывод:\n15'),
        ('nonlocal', 'Строка nonlocal имя во вложенной функции: присваивание этому имени меняет переменную внешней функции, '
                     'а не создаёт новую локальную.\n'
                     'Пример:\ndef counter():\n    n = 0\n    def step():\n        nonlocal n\n        n += 1\n        return n\n    return step\n\n'
                     'c = counter()\nc()\nprint(c())\nВывод:\n2'),
    ]
    body = (
        '<p>Функция — такое же значение, как число или список: её можно положить в переменную, передать в <code>sorted</code> как key. '
        'Можно и определить функцию внутри другой и вернуть её наружу:</p>'
        + ex('def make_multiplier(k):\n    def multiply(x):\n        return x * k\n    return multiply\n\n\n'
             'double = make_multiplier(2)\ntriple = make_multiplier(3)\nprint(double(10), triple(10))\nprint(double(triple(5)))') +
        '<p>Каждый вызов <code>make_multiplier</code> создаёт новую функцию <code>multiply</code>, и она помнит своё <code>k</code>, '
        'хотя сама <code>make_multiplier</code> давно закончилась. Функция вместе с запомненными переменными — это [[замыкание]]. '
        'Так делают «фабрики» похожих функций с разными настройками.</p>'
        '<h3>Изменить запомненное</h3>'
        '<p>Читать переменные внешней функции можно свободно, а вот присваивание внутри вложенной функции создаёт новую локальную '
        'переменную — как с <code>global</code> в теме про функции. Счётчик без подготовки упадёт:</p>'
        + exerr('def make_counter():\n    n = 0\n    def step():\n        n += 1\n        return n\n    return step\n\n\nc = make_counter()\nprint(c())') +
        '<p>Строка [[nonlocal]] говорит: «<code>n</code> — переменная внешней функции, меняй её». У каждого счётчика своя '
        '<code>n</code>, они не мешают друг другу:</p>'
        + ex('def make_counter():\n    n = 0\n\n    def step():\n        nonlocal n\n        n += 1\n        return n\n\n    return step\n\n\n'
             'a = make_counter()\nb = make_counter()\na()\na()\nprint(a(), b())') +
        '<p>В отличие от <code>global</code>, данные не лежат на виду у всей программы: до <code>n</code> можно добраться только '
        'через сам счётчик.</p>'
    )
    return th('Замыкания', terms, body)


def fl_closure():
    return fl('Замыкания', [
        qo('Что выведет программа?', 'def make(n):\n    def f(x):\n        return x * n\n    return f\n\na = make(3)\nb = make(10)\nprint(a(2), b(2))',
           ['6 6', '20 20', 'Ошибка'], 'Каждая функция помнит своё n: 2 * 3 и 2 * 10.'),
        qo('Что выведет программа?', 'def counter():\n    n = 0\n    def step():\n        nonlocal n\n        n += 1\n        return n\n    return step\n\n'
           'c1 = counter()\nc2 = counter()\nc1()\nc1()\nprint(c1(), c2())',
           ['3 3', '1 1', '2 1'], 'У c1 и c2 свои n: c1 вызван третий раз, c2 — первый.'),
        q('Зачем во вложенной функции пишут nonlocal n?', 'Чтобы n += 1 меняло переменную внешней функции',
          ['Чтобы n стала видна во всей программе', 'Чтобы вложенную функцию можно было вызвать снаружи'],
          'Без nonlocal присваивание создаёт локальную n, и n += 1 падает с UnboundLocalError.'),
    ])


def code_closure():
    return ts('Замыкания', [
        task('Напиши функцию make_counter(start, step): она возвращает функцию без параметров, которая при каждом вызове возвращает '
             'следующее число: сначала start, потом start + step и так далее. Разные счётчики не должны мешать друг другу.',
             'Внутри make_counter заведи current = start и вложенную next_value(): запомни value = current, сдвинь current += step '
             '(для этого nonlocal current) и верни value.',
             'def make_counter(start, step):\n    current = start\n\n    def next_value():\n        nonlocal current\n        value = current\n'
             '        current += step\n        return value\n\n    return next_value\n',
             ['c = make_counter(10, 5)\nprint(c(), c(), c())', 'a = make_counter(1, 1)\nb = make_counter(100, -10)\nprint(a(), b(), a(), b(), a())',
              'z = make_counter(0, 0)\nprint(z(), z())'], tail=TL),
        task('Напиши функцию make_piggy(goal) — копилку с целью. Она возвращает функцию add(amount), которая кладёт amount в копилку '
             'и возвращает строку «Накоплено: S из G», а как только сумма S дошла до цели G или превысила её — «Цель достигнута: S».',
             'Сумму храни во внешней функции: saved = 0, во вложенной nonlocal saved и saved += amount.\n'
             'Затем if saved >= goal — одна строка, иначе другая.',
             'def make_piggy(goal):\n    saved = 0\n\n    def add(amount):\n        nonlocal saved\n        saved += amount\n        if saved >= goal:\n'
             '            return f"Цель достигнута: {saved}"\n        return f"Накоплено: {saved} из {goal}"\n\n    return add\n',
             ['p = make_piggy(1000)\nprint(p(300))\nprint(p(500))\nprint(p(400))', 'p = make_piggy(50)\nprint(p(50))',
              'a = make_piggy(10)\nb = make_piggy(100)\nprint(a(6), b(6), a(6), sep="\\n")'], tail=TL),
        task('Чат с нумерацией. На вход подаются строки «ник: сообщение», последняя — «стоп». У каждого ника своя нумерация сообщений. '
             'Напиши make_logger(nick) — она возвращает функцию log(text), которая выводит «[ник #K] text», где K — номер сообщения '
             'этого ника. Логгеры храни в словаре по нику и создавай при первом сообщении ника.',
             'В make_logger счётчик count = 0 и вложенная log(text) с nonlocal count.\nНик — всё до первого «: »: i = s.find(": "), nick = s[:i], текст — s[i + 2:].\n'
             'Если ника ещё нет в словаре — loggers[nick] = make_logger(nick), затем loggers[nick](текст).',
             'def make_logger(nick):\n    count = 0\n\n    def log(text):\n        nonlocal count\n        count += 1\n        print(f"[{nick} #{count}] {text}")\n\n'
             '    return log\n\n\nloggers = {}\nwhile True:\n    s = input()\n    if s == "стоп":\n        break\n    i = s.find(": ")\n    nick = s[:i]\n'
             '    if nick not in loggers:\n        loggers[nick] = make_logger(nick)\n    loggers[nick](s[i + 2:])',
             ['zed: всем привет\nаня: привет!\nzed: кто в игру?\nzed: ау\nаня: я: через 5 минут\nстоп', 'одинокий: тут кто-нибудь есть?\nстоп']),
    ])


def th_decorator():
    terms = [
        ('обёртка', 'Функция, которую возвращает декоратор: она вызывает исходную функцию и добавляет что-то до или после. '
                    'Принимает *args и **kwargs, чтобы подойти к функции с любыми аргументами.'),
        ('wraps', 'Декоратор из functools для обёртки: @wraps(func) над wrapper копирует в неё имя и описание исходной функции.\n'
                  'Пример:\nfrom functools import wraps\n\ndef loud(func):\n    @wraps(func)\n    def wrapper(*args, **kwargs):\n'
                  '        return func(*args, **kwargs).upper()\n    return wrapper\n\n@loud\ndef hi(name):\n    return "привет, " + name\n\n'
                  'print(hi("ира"), hi.__name__)\nВывод:\nПРИВЕТ, ИРА hi'),
    ]
    body = (
        '<p>В прошлой теме <code>@lru_cache</code> добавлял функции запоминание. Такой декоратор можно написать и самому: это '
        'функция, которая принимает функцию и возвращает новую — [[обёртка]], — делающую то же самое плюс что-то ещё.</p>'
        + ex('def shout(func):\n    def wrapper(text):\n        return func(text).upper() + "!"\n    return wrapper\n\n\n'
             'def greet(name):\n    return "привет, " + name\n\n\ngreet = shout(greet)\nprint(greet("мир"))') +
        '<p>Строка <code>greet = shout(greet)</code> подменила функцию её обёрткой, а сама обёртка внутри зовёт старую '
        '<code>greet</code> — её она запомнила как замыкание. Запись <code>@shout</code> над <code>def</code> делает ровно это, '
        'только короче:</p>'
        + ex('def shout(func):\n    def wrapper(text):\n        return func(text).upper() + "!"\n    return wrapper\n\n\n'
             '@shout\ndef greet(name):\n    return "привет, " + name\n\n\nprint(greet("мир"))') +
        '<h3>Обёртка для любой функции</h3>'
        '<p>Чтобы декоратор подходил к функциям с любыми аргументами, обёртка принимает <code>*args, **kwargs</code> и передаёт их '
        'дальше без изменений. Вот декоратор, который считает вызовы и печатает их:</p>'
        + ex('def trace(func):\n    calls = 0\n\n    def wrapper(*args, **kwargs):\n        nonlocal calls\n        calls += 1\n'
             '        result = func(*args, **kwargs)\n        print(f"вызов {calls}: {func.__name__}{args} = {result}")\n        return result\n\n'
             '    return wrapper\n\n\n@trace\ndef add(a, b):\n    return a + b\n\n\nadd(2, 3)\nadd(10, -4)') +
        '<p><code>func.__name__</code> — имя функции строкой. Но у декорированной функции имя теперь чужое: снаружи видна обёртка, '
        'и <code>add.__name__</code> выдало бы <code>wrapper</code>. Это мешает при отладке, поэтому обёртку помечают [[wraps]] '
        'из functools — он копирует имя и описание исходной функции.</p>'
        '<h3>Декоратор с настройкой</h3>'
        '<p>Иногда декоратору нужен параметр: <code>@retry(3)</code>, <code>@repeat(2)</code>. Тогда снаружи ещё один уровень: '
        'функция принимает настройку и возвращает сам декоратор:</p>'
        + ex('from functools import wraps\n\n\ndef repeat(times):\n    def decorator(func):\n        @wraps(func)\n        def wrapper(*args, **kwargs):\n'
             '            for _ in range(times):\n                func(*args, **kwargs)\n        return wrapper\n    return decorator\n\n\n'
             '@repeat(3)\ndef cheer(name):\n    print("Давай,", name + "!")\n\n\ncheer("Ира")\nprint(cheer.__name__)') +
        '<p><code>@repeat(3)</code> сначала вызывает <code>repeat(3)</code>, получает декоратор и уже его применяет к функции.</p>'
    )
    return th('Свои декораторы', terms, body)


def fl_decorator():
    return fl('Свои декораторы', [
        q('Запись @deco над def f(...) — это то же самое, что…', 'f = deco(f) сразу после определения f',
          ['Каждый вызов f(x) заменяется на deco(x)', 'deco вызывается внутри f при каждом вызове'],
          'Декоратор применяется один раз, при определении; дальше вызывается обёртка.'),
        qo('Что выведет программа?', 'def twice(func):\n    def w(x):\n        return func(func(x))\n    return w\n\n@twice\ndef inc(x):\n    return x + 1\n\nprint(inc(5))',
           ['6', '10', 'Ошибка'], 'Обёртка вызывает inc дважды: 5 → 6 → 7.'),
        q('Зачем обёртке параметры *args и **kwargs?', 'Чтобы принимать и передавать дальше любые аргументы',
          ['Чтобы функция работала быстрее', 'Без них декоратор не запомнит исходную функцию'],
          'Так один декоратор подходит к функциям с любым числом и видом аргументов.'),
    ])


def code_decorator():
    return ts('Свои декораторы', [
        task('Напиши декоратор numbered: функция, к которой он применён, возвращает строку, а обёртка добавляет к ней номер вызова — '
             '«1) …», «2) …» и так далее. У каждой декорированной функции свой счётчик.',
             'def numbered(func): внутри счётчик n = 0 и обёртка wrapper(*args, **kwargs) с nonlocal n.\n'
             'Обёртка: n += 1, return f"{n}) " + func(*args, **kwargs).',
             'def numbered(func):\n    n = 0\n\n    def wrapper(*args, **kwargs):\n        nonlocal n\n        n += 1\n        return f"{n}) " + func(*args, **kwargs)\n\n'
             '    return wrapper\n',
             ['@numbered\ndef greet(name):\n    return f"Привет, {name}"\n\nprint(greet("Аня"))\nprint(greet("Лёва"))',
              '@numbered\ndef a():\n    return "раз"\n\n@numbered\ndef b(x, y=0):\n    return str(x + y)\n\nprint(a(), b(2), a(), b(1, y=5))'], tail=TL),
        task('Напиши декоратор safe: если функция упала с любой ошибкой, обёртка не падает, а возвращает строку «Ошибка в ИМЯ: текст ошибки», '
             'где ИМЯ — имя функции. Если ошибки нет — возвращает результат функции. Имя функции сохрани через wraps.',
             'Обёртка: try: return func(*args, **kwargs) except Exception as e: return f"Ошибка в {func.__name__}: {e}".\n'
             'Над обёрткой — @wraps(func) из functools.',
             'from functools import wraps\n\n\ndef safe(func):\n    @wraps(func)\n    def wrapper(*args, **kwargs):\n        try:\n            return func(*args, **kwargs)\n'
             '        except Exception as e:\n            return f"Ошибка в {func.__name__}: {e}"\n\n    return wrapper\n',
             ['@safe\ndef div(a, b):\n    return a / b\n\nprint(div(6, 3))\nprint(div(1, 0))\nprint(div.__name__)',
              '@safe\ndef first(items):\n    return items[0]\n\nprint(first([7]), first([]), sep="\\n")'], tail=TL),
        task('Напиши декоратор с настройкой limit(n): функцию можно вызвать не больше n раз, а дальше обёртка уже не вызывает её и '
             'возвращает строку «Лимит исчерпан».',
             'Три уровня, как у repeat: limit(n) возвращает decorator(func), тот — wrapper(*args, **kwargs).\nВ decorator заведи used = 0, '
             'в обёртке nonlocal used: если used >= n — строка, иначе used += 1 и вызов функции.',
             'def limit(n):\n    def decorator(func):\n        used = 0\n\n        def wrapper(*args, **kwargs):\n            nonlocal used\n            if used >= n:\n'
             '                return "Лимит исчерпан"\n            used += 1\n            return func(*args, **kwargs)\n\n        return wrapper\n\n    return decorator\n',
             ['@limit(2)\ndef hint(k):\n    return f"Подсказка {k}"\n\nfor k in range(1, 5):\n    print(hint(k))',
              '@limit(0)\ndef never():\n    return "ок"\n\n@limit(1)\ndef once(x):\n    return x * 2\n\nprint(never(), once(4), once(5))'], tail=TL),
    ])


def th_gen():
    terms = [
        ('yield', 'Делает функцию генератором: yield значение отдаёт значение наружу и ставит функцию на паузу до следующего запроса.\n'
                  'Пример:\ndef abc():\n    yield "a"\n    yield "b"\n\nprint(list(abc()))\nВывод:\n[\'a\', \'b\']'),
        ('функция-генератор', 'Функция, в теле которой есть yield. Вызов не выполняет тело, а возвращает генератор — итератор, который '
                              'на каждый next() выполняет тело до следующего yield. Когда тело закончилось — StopIteration.'),
        ('yield from', 'yield from набор — отдать по очереди все значения набора (или другого генератора), как цикл for с yield внутри.\n'
                       'Пример:\ndef both():\n    yield from [1, 2]\n    yield from "ab"\n\nprint(list(both()))\nВывод:\n[1, 2, \'a\', \'b\']'),
    ]
    body = (
        '<p>Обычная функция возвращает результат один раз и заканчивается. [[функция-генератор]] выдаёт значения по одному: '
        'вместо <code>return</code> в ней [[yield]]. Вызов такой функции ничего не выполняет, а возвращает генератор — итератор '
        'из темы про коллекции. Каждый <code>next()</code> продолжает тело с места паузы до следующего <code>yield</code>:</p>'
        + ex('def countdown(n):\n    print("старт")\n    while n > 0:\n        yield n\n        n -= 1\n    print("финиш")\n\n\n'
             'gen = countdown(3)\nprint("генератор создан")\nprint(next(gen))\nprint(next(gen))\nfor x in gen:\n    print("в цикле", x)') +
        '<p>«старт» напечатался только на первом <code>next</code>: до него тело не выполнялось. Цикл <code>for</code> забрал '
        'оставшееся значение, а когда тело закончилось, генератор сообщил о конце (StopIteration), и цикл остановился.</p>'
        '<h3>Ленивость и бесконечные генераторы</h3>'
        '<p>Генератор не хранит все значения сразу, а вычисляет следующее, когда его попросят. Поэтому он может быть даже '
        'бесконечным — главное, брать из него конечное число значений, например через <code>islice</code>:</p>'
        + ex('from itertools import islice\n\n\ndef fibonacci():\n    a, b = 0, 1\n    while True:\n        yield a\n        a, b = b, a + b\n\n\n'
             'print(list(islice(fibonacci(), 12)))\nfor x in fibonacci():\n    if x > 1000:\n        print("первое больше 1000:", x)\n        break') +
        '<p>Генераторы удобно соединять в цепочку: каждый берёт значения у предыдущего и отдаёт обработанные. Данные проходят '
        'по цепочке по одному, и даже огромный файл не нужно загружать в память целиком:</p>'
        + ex('def numbers(text):\n    for part in text.split():\n        yield int(part)\n\n\ndef only_even(items):\n    for x in items:\n        if x % 2 == 0:\n            yield x\n\n\n'
             'def squares(items):\n    for x in items:\n        yield x * x\n\n\nprint(list(squares(only_even(numbers("3 4 7 10 12")))))') +
        '<h3>yield from</h3>'
        '<p>[[yield from]] отдаёт все значения другого набора или генератора — короче, чем цикл с <code>yield</code>. Особенно '
        'удобно в рекурсии: обход вложенных списков из темы «Рекурсия» становится генератором:</p>'
        + ex('def flatten(x):\n    for item in x:\n        if isinstance(item, list):\n            yield from flatten(item)\n        else:\n            yield item\n\n\n'
             'print(list(flatten([1, [2, [3, 4]], [[5]]])))')
    )
    return th('Генераторы', terms, body)


def fl_gen():
    return fl('Генераторы', [
        qo('Что выведет программа?', 'def g():\n    yield 1\n    yield 2\n\nit = g()\nprint(next(it) + next(it))', ['1', '12', 'Ошибка'],
           'Первый next даёт 1, второй — 2, сумма 3.'),
        q('Что вернёт вызов функции, в теле которой есть yield?', 'Генератор; тело ещё не начало выполняться',
          ['Первое значение из yield', 'Список всех значений'], 'Тело выполняется кусками — по одному на каждый next().'),
        qo('Что выведет программа?', 'def flat(x):\n    for i in x:\n        if isinstance(i, list):\n            yield from flat(i)\n        else:\n            yield i\n\n'
           'print(list(flat([1, [2, [3]]])))',
           ['[1, [2, [3]]]', '[1, 2, [3]]', '[3, 2, 1]'], 'yield from разворачивает вложенные списки на любой глубине.'),
    ])


def code_gen():
    return ts('Генераторы', [
        task('Напиши функцию-генератор chunks(items, size): она отдаёт куски списка или строки items длиной size по порядку, '
             'последний кусок может быть короче. Куски — срезы items.',
             'for start in range(0, len(items), size): yield items[start:start + size]',
             'def chunks(items, size):\n    for start in range(0, len(items), size):\n        yield items[start:start + size]\n',
             ['print(list(chunks([1, 2, 3, 4, 5], 2)))', 'for part in chunks("абвгдежз", 3):\n    print(part)', 'print(list(chunks([], 4)), list(chunks([9], 4)))'],
             tail=TL),
        task('Напиши бесконечный генератор primes(), который отдаёт простые числа по возрастанию: 2, 3, 5, 7… На вход подаётся n. '
             'Выведи первые n простых чисел через пробел, а второй строкой — «Сумма: S».',
             'В primes: x = 2, while True — если x не делится ни на одно d из range(2, int(x ** 0.5) + 1), yield x; затем x += 1.\n'
             'Первые n: list(islice(primes(), n)) из itertools.',
             'from itertools import islice\n\n\ndef primes():\n    x = 2\n    while True:\n        if all(x % d != 0 for d in range(2, int(x ** 0.5) + 1)):\n'
             '            yield x\n        x += 1\n\n\nfirst = list(islice(primes(), int(input())))\nprint(" ".join(map(str, first)))\nprint(f"Сумма: {sum(first)}")',
             ['10', '1', '25']),
    ])


def code_final():
    return ts('Задачи: испытание', [
        task('Рядом с программой лежит журнал сервера server.log: в каждой строке время, уровень (INFO, WARN или ERROR) и сообщение '
             'через пробел. На вход подаются уровень и слово для поиска (вторая строка может быть пустой — тогда подходят все '
             'сообщения уровня). Выведи подходящие записи в виде «время — сообщение», а последней строкой «Найдено: N». '
             'Уровень подаётся заглавными буквами, как в файле. Слово ищи как часть текста сообщения (не времени и не уровня) без учёта регистра. Обработку сделай цепочкой из трёх генераторов: чтение записей, фильтр по уровню, '
             'фильтр по слову.',
             'read_log(path): для каждой строки файла parts = line.split(), yield (parts[0], parts[1], " ".join(parts[2:])).\n'
             'by_level(records, level) и containing(records, word) — циклы for с условием и yield.\n'
             'Цепочка: containing(by_level(read_log("server.log"), level), word).',
             'def read_log(path):\n    with open(path, encoding="utf-8") as f:\n        for line in f:\n            parts = line.split()\n            if parts:\n'
             '                yield parts[0], parts[1], " ".join(parts[2:])\n\n\ndef by_level(records, level):\n    for rec in records:\n        if rec[1] == level:\n'
             '            yield rec\n\n\ndef containing(records, word):\n    for rec in records:\n        if word.lower() in rec[2].lower():\n            yield rec\n\n\n'
             'level = input()\nword = input()\ncount = 0\nfor time, _, text in containing(by_level(read_log("server.log"), level), word):\n'
             '    print(f"{time} — {text}")\n    count += 1\nprint(f"Найдено: {count}")',
             ['ERROR\n', 'ERROR\nтаймаут', 'WARN\nБАЗ', 'INFO\nкосмос'], files={'server.log': LOG}),
    ])


def build():
    return topic('Декораторы и генераторы', 'замыкания, nonlocal, @, yield', [
        th_closure(), fl_closure(), code_closure(),
        th_decorator(), fl_decorator(), code_decorator(),
        th_gen(), fl_gen(), code_gen(),
        code_final(),
    ])
