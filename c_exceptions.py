from dsl import *

# Тема 18 «Исключения». Ученик знает функции, коллекции, итераторы, все встроенные ошибки до этого места.
# Три теории: try/except; else, finally и иерархия ошибок (isinstance); raise и assert.


def th_try():
    terms = [
        ('try', 'Блок, в котором ожидают возможную ошибку. Если в нём случилось исключение, Python прыгает в подходящий except, '
                'остаток блока try не выполняется.\nПример:\ntry:\n    n = int("abc")\nexcept ValueError:\n    print("не число")\nВывод:\nне число'),
        ('except', 'Ловит ошибку указанного типа (или нескольких — кортежем). except ValueError as e: — e хранит саму ошибку, '
                   'str(e) — её текст.\nПример:\ntry:\n    print(10 / 0)\nexcept ZeroDivisionError as e:\n    print("ошибка:", e)\nВывод:\nошибка: division by zero'),
        ('Exception', 'Общий тип почти всех ошибок. except Exception ловит любую из них — удобно, но опасно: так легко спрятать настоящую ошибку в коде.'),
    ]
    body = (
        '<p>До сих пор любая ошибка во время работы останавливала программу. Но многие ошибки ожидаемы: пользователь ввёл буквы '
        'вместо числа, нужного ключа нет в словаре. Такие ошибки — <b>исключения</b> — можно перехватить и обработать.</p>'
        + ex('s = input("Возраст: ")\ntry:\n    age = int(s)\n    print("Через год:", age + 1)\nexcept ValueError:\n    print("Это не число")\nprint("Программа работает дальше")', ['пятнадцать']) +
        '<p>Код, где может случиться ошибка, кладут в блок [[try]]. Если там возникло исключение, Python не падает, '
        'а переходит в блок [[except]] с подходящим типом ошибки; остаток <code>try</code> пропускается. '
        'Если ошибки не было, <code>except</code> не выполняется.</p>'
        '<h3>Несколько типов и текст ошибки</h3>'
        '<p>Блоков <code>except</code> может быть несколько, а <code>as e</code> даёт доступ к самой ошибке — её текст '
        'можно вывести:</p>'
        + ex('def divide(a, b):\n    try:\n        return int(a) / int(b)\n    except ZeroDivisionError:\n        return "делить на ноль нельзя"\n'
             '    except ValueError as e:\n        return f"не число ({e})"\n\nprint(divide("10", "4"))\nprint(divide("10", "0"))\nprint(divide("10", "x"))') +
        '<h3>Повторить ввод</h3>'
        '<p>Частый приём — спрашивать, пока не введут правильно:</p>'
        + ex('while True:\n    try:\n        n = int(input("Число: "))\n        break\n    except ValueError:\n        print("Нужно целое число, попробуй ещё")\nprint("Принято:", n)', ['abc', '4.5', '7']) +
        '<p>Ловить нужно конкретные ошибки. <code>except Exception</code> (общий тип [[Exception]]) ловит почти всё — '
        'и тем самым прячет настоящие ошибки в коде, например опечатку в имени. Используй его только там, где действительно '
        'нельзя падать, и выводи текст ошибки.</p>'
    )
    return th('try и except', terms, body)


def fl_try():
    return fl('try и except', [
        qo('Что выведет программа?', 'try:\n    x = int("5")\n    print("ок", end=" ")\nexcept ValueError:\n    print("ошибка", end=" ")\nprint("конец")',
           ['ошибка конец', 'ок ошибка конец', 'ок'], 'Ошибки нет, except пропущен: ок конец.'),
        qo('Что выведет программа?', 'try:\n    print(1, end="")\n    print(1 / 0, end="")\n    print(2, end="")\nexcept ZeroDivisionError:\n    print(3, end="")',
           ['123', '3', '12'], 'После 1 деление на ноль: остаток try пропущен, сработал except — 13.'),
        q('Чем опасен except Exception без особой нужды?', 'Прячет настоящие ошибки в коде, например опечатки',
          ['Он медленный', 'Он не ловит ValueError'], 'Опечатка в имени (NameError) тоже будет тихо поймана.'),
    ])


def code_try():
    return ts('try и except', [
        task('На вход подаются строки, пока не придёт целое число. На каждую неправильную строку выведи «Не число: СТРОКА», '
             'а когда придёт число — «Квадрат: N».',
             'while True: s = input(); try: n = int(s); break; except ValueError: print(f"Не число: {s}"). После цикла — квадрат.',
             'while True:\n    s = input()\n    try:\n        n = int(s)\n        break\n    except ValueError:\n        print(f"Не число: {s}")\nprint(f"Квадрат: {n * n}")',
             ['abc\n2.5\n7', '12', 'пять\n-3']),
        task('Напиши функцию safe_div(a, b), которая возвращает a / b, округлённое до двух знаков, а при делении на ноль — '
             'строку «на ноль делить нельзя».',
             'try: return round(a / b, 2) except ZeroDivisionError: return "на ноль делить нельзя".',
             'def safe_div(a, b):\n    try:\n        return round(a / b, 2)\n    except ZeroDivisionError:\n        return "на ноль делить нельзя"',
             ['print(safe_div(10, 4))', 'print(safe_div(1, 0))', 'print(safe_div(-7, 3))'], tail=TL),
        task('Справочник цен задан словарём. На вход подаются товар и количество, каждое в отдельной строке ввода. Выведи стоимость, '
             'а если товара нет — «Нет товара: ...», если количество не целое число — «Количество — целое число» '
             '(если неверно и то, и другое, — сообщение про товар). Используй try/except, а не in и isdigit.',
             'try: total = prices[item] * int(count) — две возможные ошибки: KeyError и ValueError, по отдельному except на каждую.',
             'prices = {"тетрадь": 45, "ручка": 30, "пенал": 350}\nitem = input()\ncount = input()\ntry:\n    print(prices[item] * int(count))\n'
             'except KeyError:\n    print(f"Нет товара: {item}")\nexcept ValueError:\n    print("Количество — целое число")',
             ['ручка\n3', 'ластик\n2', 'пенал\nдва'],
             starter='prices = {"тетрадь": 45, "ручка": 30, "пенал": 350}\n'),
    ])


def th_finally():
    terms = [
        ('finally', 'Блок, который выполняется всегда: была ошибка или нет, поймали её или нет. Для обязательных завершающих действий.\n'
                    'Пример:\ntry:\n    print(1 / 0)\nexcept ZeroDivisionError:\n    print("поймали")\nfinally:\n    print("готово")\nВывод:\nпоймали\nготово'),
        ('ArithmeticError', 'Общий тип арифметических ошибок: ZeroDivisionError и другие. except ArithmeticError ловит их все.'),
        ('LookupError', 'Общий тип ошибок поиска: IndexError (нет номера) и KeyError (нет ключа).'),
        ('isinstance', 'Проверяет, относится ли значение к типу (или к одному из типов кортежа), с учётом «родства» типов ошибок.\n'
                       'Пример:\nprint(isinstance(5, int), isinstance("5", (int, float)))\nprint(isinstance(KeyError(), LookupError))\nВывод:\nTrue False\nTrue'),
    ]
    body = (
        '<h3>else и finally</h3>'
        '<p>У <code>try</code> есть ещё два необязательных блока. <code>else</code> выполняется, если ошибки <b>не было</b> — туда кладут код, '
        'который должен идти только после успеха (и который сам не нужно охранять). [[finally]] выполняется <b>всегда</b> — '
        'и при ошибке, и без неё:</p>'
        + ex('def check(s):\n    try:\n        n = int(s)\n    except ValueError:\n        print(s, "— не число")\n    else:\n        print(s, "— число", n)\n'
             '    finally:\n        print("проверено:", s)\n\ncheck("42")\ncheck("сорок")') +
        '<h3>Иерархия ошибок</h3>'
        '<p>Типы ошибок связаны «родством»: несколько похожих объединены общим родителем. [[ArithmeticError]] — родитель '
        'ZeroDivisionError, [[LookupError]] — родитель IndexError и KeyError, а над почти всеми стоит Exception. '
        '<code>except</code> с родителем ловит всех его потомков:</p>'
        + ex('def get(data, key):\n    try:\n        return data[key]\n    except LookupError:\n        return "не найдено"\n\nprint(get([10, 20], 5))\nprint(get({"a": 1}, "b"))\nprint(get("кот", 0))') +
        '<p>Одна функция обрабатывает и список (IndexError), и словарь (KeyError). Проверить «родство» можно функцией '
        '[[isinstance]] — она отвечает, относится ли значение к типу, и вообще полезна для проверки типов:</p>'
        + ex('try:\n    {}["x"]\nexcept LookupError as e:\n    print(type(e), isinstance(e, KeyError), isinstance(e, IndexError))\nprint(isinstance(3.5, (int, float)))') +
        '<p>Порядок блоков <code>except</code> важен: Python берёт первый подходящий. Поэтому конкретные типы пишут раньше общих.</p>'
    )
    return th('else, finally и иерархия ошибок', terms, body)


def fl_finally():
    return fl('else, finally и иерархия ошибок', [
        qo('Что выведет программа?', 'try:\n    x = 1\nexcept ValueError:\n    print("A", end="")\nelse:\n    print("B", end="")\nfinally:\n    print("C", end="")',
           ['AC', 'C', 'ABC'], 'Ошибки нет: else и finally — BC.'),
        qo('Что выведет программа?', 'try:\n    [1, 2][5]\nexcept LookupError:\n    print("поиск")\nexcept IndexError:\n    print("индекс")',
           ['индекс', 'поиск индекс', 'Ошибка'], 'IndexError — потомок LookupError, сработал первый подходящий: поиск.'),
        qo('Что выведет программа?', 'print(isinstance(2, int), isinstance("2", int))', ['False False', 'True True', 'False True'],
           '2 — целое число, а "2" — строка: True False.'),
    ])


def code_finally():
    return ts('else, finally и иерархия ошибок', [
        task('Импорт оценок. На вход подаются строки «Фамилия оценка» до слова «стоп». Оценка должна быть целым числом; строки, '
             'где это не так или нет второй части, считай ошибками. Выведи «Принято: N, ошибок: M», а следующей строкой — '
             'среднее принятых с двумя знаками (если принятых нет, вторую строку не выводи).',
             'try: name, mark = s.split(); m = int(mark) — ошибки распаковки и int обе ValueError. else: добавь m в список. '
             'Среднее — через формат :.2f; если принятых нет, среднее не выводи.',
             'marks = []\nbad = 0\nwhile True:\n    s = input()\n    if s == "стоп":\n        break\n    try:\n        name, mark = s.split()\n        m = int(mark)\n'
             '    except ValueError:\n        bad += 1\n    else:\n        marks.append(m)\nprint(f"Принято: {len(marks)}, ошибок: {bad}")\nif marks:\n    print(f"{sum(marks) / len(marks):.2f}")',
             ['Ира 5\nЛи пять\nКим 4\nОля\nстоп', 'Тимур 3\nстоп', 'а\nб в\nстоп']),
        task('Напиши функцию pick(data, key), которая возвращает data[key] для списка или словаря, а если такого номера или ключа '
             'нет — строку «нет такого». Одним except на оба случая.',
             'except LookupError: — родитель и IndexError, и KeyError.',
             'def pick(data, key):\n    try:\n        return data[key]\n    except LookupError:\n        return "нет такого"',
             ['print(pick([1, 2, 3], 1), pick([1], 9))', 'print(pick({"a": 5}, "a"), pick({}, "x"))', 'print(pick("кот", -1))'], tail=TL),
        task('Напиши функцию describe(x), которая возвращает «число», если x — int или float, «текст», если str, '
             '«список», если list, иначе «другое».',
             'isinstance(x, (int, float)) для чисел, дальше isinstance(x, str) и isinstance(x, list).',
             'def describe(x):\n    if isinstance(x, (int, float)):\n        return "число"\n    if isinstance(x, str):\n        return "текст"\n'
             '    if isinstance(x, list):\n        return "список"\n    return "другое"',
             ['print(describe(5), describe(2.5))', 'print(describe("5"), describe([5]))', 'print(describe((5,)), describe({}))'], tail=TL),
    ])


def th_raise():
    terms = [
        ('raise', 'Вызывает исключение самостоятельно: raise ValueError("текст"). Программа ведёт себя так же, как при встроенной ошибке.\n'
                  'Пример:\ntry:\n    raise ValueError("возраст отрицательный")\nexcept ValueError as e:\n    print(e)\nВывод:\nвозраст отрицательный'),
        ('assert', 'Проверка «так должно быть»: assert условие, "сообщение". Если условие ложно — AssertionError. '
                   'Для проверки своих предположений и простых тестов.\nПример:\nassert 2 + 2 == 4\nprint("ок")\nВывод:\nок'),
        ('AssertionError', 'Ошибка, которую вызывает assert с ложным условием. Текст — сообщение после запятой.'),
    ]
    body = (
        '<p>Ошибки можно не только ловить, но и вызывать самому — словом [[raise]]. Так функция сообщает, что ей передали '
        'неподходящие данные: вместо неправильного результата — понятная ошибка, которую вызывающий код поймает:</p>'
        + ex('def set_age(age):\n    if not isinstance(age, int):\n        raise TypeError("возраст — целое число")\n    if age < 0 or age > 150:\n'
             '        raise ValueError(f"странный возраст: {age}")\n    return age\n\nfor a in [15, -3, "15"]:\n    try:\n        print("ок", set_age(a))\n'
             '    except (TypeError, ValueError) as e:\n        print("ошибка:", e)') +
        '<p>Тип выбирают по смыслу: TypeError — не тот тип, ValueError — тип верный, а значение нет. Несколько типов '
        'в одном <code>except</code> перечисляют кортежем. Если ошибку не поймать, программа остановится с Traceback, '
        'как при встроенной.</p>'
        '<h3>assert</h3>'
        '<p>[[assert]] проверяет предположение: <code>assert условие, "сообщение"</code>. Если условие истинно, ничего не происходит, '
        'если ложно — [[AssertionError]]. Так проверяют свои функции на известных примерах — это простейшие тесты:</p>'
        + exerr('def average(nums):\n    return sum(nums) / len(nums)\n\nassert average([4, 6]) == 5\nassert average([5]) == 5\nassert average([1, 2]) == 2, "среднее 1 и 2 — это 1.5"\nprint("все тесты прошли")') +
        '<p>Первые два утверждения верны, третье — нет (ошибка в самом тесте: среднее 1 и 2 равно 1.5), и программа остановилась '
        'с нашим сообщением. <code>assert</code> — для проверки своего кода, а не пользовательского ввода: для ввода нужны '
        '<code>if</code> и <code>raise</code>.</p>'
    )
    return th('raise и assert', terms, body)


def fl_raise():
    return fl('raise и assert', [
        qo('Что выведет программа?', 'try:\n    raise KeyError("нет")\nexcept LookupError:\n    print("поймали")', ['нет', 'KeyError', 'Ошибка'],
           'KeyError — потомок LookupError: поймали.'),
        q('Какую ошибку уместно вызвать, если функции передали число -5 там, где нужно неотрицательное?', 'ValueError',
          ['TypeError', 'NameError'], 'Тип верный (число), неправильное значение — ValueError.'),
        qo('Что выведет программа?', 'x = 3\nassert x > 0\nprint("дальше")', ['AssertionError', 'Ничего', 'True'], 'Условие верно, assert молчит: дальше.'),
    ])


def code_raise():
    return ts('raise и assert', [
        task('Напиши функцию parse_time(s), которая из строки «ЧЧ:ММ» возвращает число минут от полуночи. Если формат неверный '
             '(нет двоеточия, не числа, часы не от 0 до 23, минуты не от 0 до 59), вызови ValueError с текстом «неверное время: s».',
             'Разбор: h, m = s.split(":") и int — их собственные ошибки поймай и вызови свою: try: ... except ValueError: raise ValueError(f"неверное время: {s}"). '
             'Диапазоны проверь if и raise.',
             'def parse_time(s):\n    try:\n        h, m = s.split(":")\n        h, m = int(h), int(m)\n    except ValueError:\n        raise ValueError(f"неверное время: {s}")\n'
             '    if not 0 <= h <= 23 or not 0 <= m <= 59:\n        raise ValueError(f"неверное время: {s}")\n    return h * 60 + m',
             ['print(parse_time("07:30"))', 'try:\n    parse_time("25:00")\nexcept ValueError as e:\n    print(e)',
              'for t in ["0:5", "12-30", "aa:bb"]:\n    try:\n        print(parse_time(t))\n    except ValueError as e:\n        print(e)'], tail=TL),
        task('Напиши функцию withdraw(balance, amount), которая возвращает новый баланс после снятия. Если amount не больше нуля — '
             'ValueError «сумма должна быть больше нуля», если денег не хватает — ValueError «не хватает: нужно ещё X», где X — недостача.',
             'Две проверки if с raise ValueError(...), затем return balance - amount.',
             'def withdraw(balance, amount):\n    if amount <= 0:\n        raise ValueError("сумма должна быть больше нуля")\n    if amount > balance:\n'
             '        raise ValueError(f"не хватает: нужно ещё {amount - balance}")\n    return balance - amount',
             ['print(withdraw(500, 120))', 'for a in [0, 900]:\n    try:\n        withdraw(500, a)\n    except ValueError as e:\n        print(e)'], tail=TL),
        task('В программе функция и три проверки assert, но одна функция работает неверно — проверка падает. Исправь функцию '
             '(а не проверки), чтобы программа вывела «Все проверки пройдены».',
             'Прочитай последнюю строку Traceback: на первой же проверке функция падает с IndexError — у слова «кот» нет второго '
             'элемента. Последнее слово берут через [-1], а не [1].',
             'def last_word(s):\n    return s.split()[-1]\n\nassert last_word("кот") == "кот"\nassert last_word("я люблю Python") == "Python"\n'
             'assert last_word("раз два") == "два"\nprint("Все проверки пройдены")', [''],
             starter='def last_word(s):\n    return s.split()[1]\n\nassert last_word("кот") == "кот", "одно слово"\nassert last_word("я люблю Python") == "Python", "три слова"\n'
                     'assert last_word("раз два") == "два", "два слова"\nprint("Все проверки пройдены")', fix=True),
    ])


def code_final():
    return ts('Задачи: испытание', [
        task('Калькулятор, который не падает. На вход подаются выражения вида «a оп b» через пробелы (оп — + - * /), '
             'последняя строка — «стоп». Числа читай как дробные (float), поэтому результат 2 + 3 — это 5.0; деление округляй '
             'через round(…, 2). Вместо результата выводи сообщение: «Ошибка: нужно a оп b», если частей не три; '
             '«Ошибка: не число», если число неверное (даже если и операция неизвестна); «Ошибка: неизвестная операция»; '
             '«Ошибка: деление на ноль».',
             'В цикле: parts = s.split(); если частей не три — сообщение и continue. Затем try: a = float(parts[0]), b = float(parts[2]) — '
             'неверное число даст ValueError раньше всего остального; дальше выбор операции через match или if/elif, для неизвестной — '
             'своё сообщение. Отдельные except для ValueError и ZeroDivisionError.',
             'def calc(a, op, b):\n    match op:\n        case "+":\n            return a + b\n        case "-":\n            return a - b\n        case "*":\n            return a * b\n'
             '        case "/":\n            return round(a / b, 2)\n        case _:\n            raise LookupError(op)\n\n\nwhile True:\n    s = input()\n    if s == "стоп":\n        break\n'
             '    parts = s.split()\n    if len(parts) != 3:\n        print("Ошибка: нужно a оп b")\n        continue\n    try:\n        print(calc(float(parts[0]), parts[1], float(parts[2])))\n'
             '    except ZeroDivisionError:\n        print("Ошибка: деление на ноль")\n    except ValueError:\n        print("Ошибка: не число")\n'
             '    except LookupError:\n        print("Ошибка: неизвестная операция")',
             ['2 + 3\n10 / 4\n7 / 0\nстоп', 'a * 2\n3 ^ 2\n1 +\nстоп', '-5 - -5\nстоп']),
    ])


def build():
    return topic('Исключения', 'try, except, else, finally, raise, assert', [
        th_try(), fl_try(), code_try(),
        th_finally(), fl_finally(), code_finally(),
        th_raise(), fl_raise(), code_raise(),
        code_final(),
    ])
