from dsl import *

# Нора после «Файлы и форматы данных»: свои утилиты командной строки. Две теории: sys.argv и argparse (позиционные аргументы,
# type, choices, необязательные --ключи, store_true); справка (description, help, format_help).
# В приложении нет терминала: список аргументов передаём в parse_args сами (строка ввода → split). prog задан явно, чтобы
# справка не зависела от имени запущенного файла.


def th_args():
    terms = [
        ('sys.argv', 'Список строк: имя запущенной программы и всё, что написали после него в терминале. python conv.py 100 USD → '
                     '["conv.py", "100", "USD"].'),
        ('argparse', 'Модуль для разбора аргументов командной строки: типы, значения по умолчанию, справка --help, сообщения об ошибках.'),
        ('ArgumentParser', 'argparse.ArgumentParser(prog="имя", description="что делает") — разборщик аргументов. Аргументы добавляют '
                           'add_argument, разбирают — parse_args.'),
        ('add_argument', 'parser.add_argument("имя") — обязательный позиционный аргумент; "--имя" — необязательный ключ. Параметры: '
                         'type=int, default=…, choices=[…], action="store_true" (флаг без значения), help="…".'),
        ('parse_args', 'parser.parse_args(список) — разобрать список строк (без списка — sys.argv[1:]). Возвращает объект, у которого '
                       'аргументы — атрибуты: args.amount, args.to.\n'
                       'Пример:\nimport argparse\np = argparse.ArgumentParser(prog="x")\np.add_argument("n", type=int)\np.add_argument("--twice", action="store_true")\n'
                       'a = p.parse_args(["5", "--twice"])\nprint(a.n * (2 if a.twice else 1))\nВывод:\n10'),
    ]
    body = (
        '<p>Многие полезные программы запускают не кнопкой, а командой в терминале, сразу с данными: '
        '<code>python conv.py 100 USD --to EUR</code>. Всё, что написано после имени файла, программа получает списком строк '
        '[[sys.argv]]:</p>'
        '<pre>sys.argv == ["conv.py", "100", "USD", "--to", "EUR"]</pre>'
        '<p>Разбирать такой список вручную неудобно: аргументы могут идти в разном порядке, быть необязательными, а пользователю нужна '
        'справка. Это делает модуль [[argparse]]. Описываешь, какие аргументы ждёшь, — он разбирает, проверяет типы и пишет понятные '
        'сообщения.</p>'
        '<p>В приложении терминала нет, поэтому список аргументов мы будем передавать в [[parse_args]] сами — например, из строки ввода '
        'через <code>split()</code>. На компьютере в терминале пишут <code>parse_args()</code> без списка, и он возьмёт <code>sys.argv[1:]</code>.</p>'
        + ex('import argparse\n\nparser = argparse.ArgumentParser(prog="conv", description="Конвертер валют")\nparser.add_argument("amount", type=float)\n'
             'parser.add_argument("currency", choices=["USD", "EUR", "CNY"])\nparser.add_argument("--round", type=int, default=2)\nparser.add_argument("--verbose", action="store_true")\n\n'
             'args = parser.parse_args("100 USD --verbose".split())\nprint(args.amount, args.currency, args.round, args.verbose)\n'
             'args = parser.parse_args(["5.5", "EUR", "--round", "0"])\nprint(args.amount, args.currency, args.round, args.verbose)') +
        '<p>[[ArgumentParser]] — сам разборщик. [[add_argument]] без дефисов задаёт обязательный позиционный аргумент, с двумя дефисами — '
        'необязательный ключ. <code>type</code> переводит строку в число, <code>choices</code> ограничивает варианты, '
        '<code>action="store_true"</code> делает флаг без значения: есть в списке — True, нет — False.</p>'
        '<p>Если аргументы неверные (нет обязательного, буквы вместо числа, валюта не из списка), argparse сам печатает, что не так, '
        'и завершает программу. В задачах этой норы ввод всегда правильный.</p>'
    )
    return th('Аргументы командной строки', terms, body)


def fl_args():
    return fl('Аргументы командной строки', [
        q('Что лежит в sys.argv[0]?', 'Имя запущенной программы', ['Первый аргумент после имени', 'Число аргументов'],
          'Аргументы начинаются с sys.argv[1].'),
        qo('Что выведет программа?', 'import argparse\np = argparse.ArgumentParser(prog="t")\np.add_argument("--n", type=int, default=3)\nprint(p.parse_args([]).n)',
           ['None', '0', 'Ошибка'], 'Ключ не передан — берётся default.'),
        q('Что делает action="store_true" у ключа --quiet?', 'Делает флаг без значения: есть --quiet — True, нет — False',
          ['Сохраняет следующий аргумент как строку «true»', 'Делает ключ обязательным'], 'Значение после флага не нужно.'),
    ])


def code_args():
    return ts('Аргументы командной строки', [
        task('Калькулятор. На вход подаётся строка аргументов: число, операция (+, -, x или /) и число, например «7 x 6». Разбери её через argparse '
             '(числа — float, операция — choices) и выведи «A ОП B = R». Ключ --int (флаг) просит вывести результат целым (int); без него '
             'результат печатается как есть.',
             'parser.add_argument("a", type=float), ("op", choices=["+", "-", "x", "/"]), ("b", type=float), ("--int", action="store_true").\n'
             'Атрибут ключа --int — args.int.',
             'import argparse\n\nparser = argparse.ArgumentParser(prog="calc")\nparser.add_argument("a", type=float)\nparser.add_argument("op", choices=["+", "-", "x", "/"])\n'
             'parser.add_argument("b", type=float)\nparser.add_argument("--int", action="store_true")\nargs = parser.parse_args(input().split())\n'
             'ops = {"+": args.a + args.b, "-": args.a - args.b, "x": args.a * args.b}\nr = ops[args.op] if args.op in ops else args.a / args.b\n'
             'print(f"{args.a} {args.op} {args.b} = {int(r) if args.int else r}")',
             ['7 x 6', '10 / 4 --int', '--int 2 - 5', '1 + 0.5']),
        task('Приветствие. Строка аргументов: имя (обязательно), ключ --times N (сколько раз повторить, по умолчанию 1) и флаг --shout '
             '(писать большими буквами и с «!» в конце вместо «.»). Выведи N строк «Привет, ИМЯ.» или «ПРИВЕТ, ИМЯ!».',
             'parser.add_argument("name"), ("--times", type=int, default=1), ("--shout", action="store_true").',
             'import argparse\n\nparser = argparse.ArgumentParser(prog="hello")\nparser.add_argument("name")\nparser.add_argument("--times", type=int, default=1)\n'
             'parser.add_argument("--shout", action="store_true")\nargs = parser.parse_args(input().split())\ntext = f"Привет, {args.name}"\n'
             'line = text.upper() + "!" if args.shout else text + "."\nfor _ in range(args.times):\n    print(line)',
             ['Аня', 'Zed --times 3', '--shout Борис --times 2']),
    ])


def th_help():
    terms = [
        ('format_help', 'parser.format_help() — текст справки строкой: то же, что покажет --help. parser.print_help() сразу печатает его.'),
    ]
    body = (
        '<p>Хорошая утилита объясняет себя сама: <code>python conv.py --help</code> печатает справку. argparse собирает её из того, что '
        'ты описал: description у парсера и help у аргументов. Получить текст справки можно через [[format_help]]:</p>'
        + ex('import argparse\n\nparser = argparse.ArgumentParser(prog="notes", description="Заметки в одном файле")\n'
             'parser.add_argument("action", choices=["add", "list"], help="что сделать")\nparser.add_argument("text", nargs="?", default="", help="текст заметки")\n'
             'parser.add_argument("--tag", default="общее", help="метка заметки")\nprint(parser.format_help())') +
        '<p><code>nargs="?"</code> делает позиционный аргумент необязательным: если его нет, берётся default. Справку не нужно '
        'писать и обновлять руками — она всегда совпадает с тем, что программа на самом деле принимает.</p>'
        '<p>Одна утилита часто обрабатывает много команд подряд — например, из файла, по строке на запуск. Парсер создают один раз, '
        'а parse_args вызывают для каждой строки.</p>'
    )
    return th('Справка', terms, body)


def fl_help():
    return fl('Справка', [
        q('Откуда argparse берёт текст для --help?', 'Из description парсера и help у аргументов', ['Из комментариев в коде', 'Его пишут отдельным файлом'],
          'Справка собирается сама из описания аргументов.'),
        qo('Что выведет программа?', 'import argparse\np = argparse.ArgumentParser(prog="t")\np.add_argument("x", nargs="?", default="нет")\nprint(p.parse_args([]).x)',
           ['None', 'Ошибка', '?'], 'nargs="?" — аргумент необязательный, взят default: нет.'),
        q('Где вызывают parse_args, если команд много — по строке на каждую?', 'Для каждой строки, а парсер создают один раз',
          ['Один раз на все строки сразу', 'Парсер создают заново перед каждой строкой'], 'Описание аргументов не меняется.'),
    ])


def code_help():
    return ts('Справка', [
        task('Заметки. Сделай парсер с prog="notes": позиционный action (add, list или del), необязательный позиционный text (по умолчанию пустой) '
             'и ключ --tag (по умолчанию «общее»). На вход подаются строки аргументов, последняя — «стоп». add добавляет заметку и выводит '
             '«Добавлено #N [МЕТКА]»; list выводит заметки с данной меткой (если --tag не указан — все) строками «#N [МЕТКА] ТЕКСТ» или «Пусто»; '
             'del удаляет заметку с номером из text: «Удалено #N» или «Нет заметки #N». Номера не переиспользуются. Текст заметки — одно слово.',
             'Заметки — словарь {номер: (метка, текст)}. Чтобы отличить «--tag не указан» от «указан общее», для list смотри, есть ли "--tag" '
             'в списке аргументов.',
             'import argparse\n\nparser = argparse.ArgumentParser(prog="notes")\nparser.add_argument("action", choices=["add", "list", "del"])\nparser.add_argument("text", nargs="?", default="")\n'
             'parser.add_argument("--tag", default="общее")\nnotes = {}\nlast = 0\nwhile True:\n    s = input()\n    if s == "стоп":\n        break\n    words = s.split()\n'
             '    args = parser.parse_args(words)\n    if args.action == "add":\n        last += 1\n        notes[last] = (args.tag, args.text)\n        print(f"Добавлено #{last} [{args.tag}]")\n'
             '    elif args.action == "list":\n        shown = [(n, t, x) for n, (t, x) in notes.items() if "--tag" not in words or t == args.tag]\n        if not shown:\n'
             '            print("Пусто")\n        for n, t, x in shown:\n            print(f"#{n} [{t}] {x}")\n    else:\n        n = int(args.text)\n        if n in notes:\n'
             '            del notes[n]\n            print(f"Удалено #{n}")\n        else:\n            print(f"Нет заметки #{n}")',
             ['add молоко --tag покупки\nadd алгебра\nadd хлеб --tag покупки\nlist --tag покупки\ndel 1\ndel 1\nlist\nстоп', 'list\nстоп']),
        task('Справка утилиты. Сделай парсер: prog="rename", description «Переименовывает файлы по шаблону», позиционные аргументы folder '
             '(help «папка с файлами») и pattern (help «шаблон имени, например photo_{n}»), ключ --start типа int со значением по умолчанию 1 '
             '(help «первый номер») и флаг --dry (help «только показать, ничего не менять»). Выведи format_help(). Затем на вход подаётся строка '
             'аргументов: разбери её и выведи «папка=…, шаблон=…, старт=…, пробно=True/False».',
             'Справку печатай print(parser.format_help()) — сразу после создания всех аргументов, до чтения ввода.',
             'import argparse\n\nparser = argparse.ArgumentParser(prog="rename", description="Переименовывает файлы по шаблону")\nparser.add_argument("folder", help="папка с файлами")\n'
             'parser.add_argument("pattern", help="шаблон имени, например photo_{n}")\nparser.add_argument("--start", type=int, default=1, help="первый номер")\n'
             'parser.add_argument("--dry", action="store_true", help="только показать, ничего не менять")\nprint(parser.format_help())\nargs = parser.parse_args(input().split())\n'
             'print(f"папка={args.folder}, шаблон={args.pattern}, старт={args.start}, пробно={args.dry}")',
             ['фото img_{n} --start 5', 'downloads file_{n} --dry']),
    ])


def project():
    return pj('Конвертер валют',
              'Утилита conv переводит деньги по фиксированным курсам к рублю: USD — 90, EUR — 98, CNY — 12.5, RUB — 1. Аргументы: сумма (float), '
              'валюта (одна из USD, EUR, CNY, RUB), ключ --to — во что перевести (по умолчанию RUB, те же варианты) и ключ --round — сколько '
              'знаков после точки (int, по умолчанию 2). На вход подаются строки аргументов, последняя — «стоп». Для каждой выведи '
              '«СУММА ВАЛЮТА = РЕЗУЛЬТАТ ВАЛЮТА_TO», где сумма — как её печатает print для float (100 → 100.0), а результат — round(…, знаков). Последней строкой выведи '
              '«Всего в рублях: X» — сумма всех введённых денег в рублях, округлённая до двух знаков.',
              'parser = argparse.ArgumentParser(prog="conv") и четыре add_argument, choices — список валют\n'
              'Через рубли: rub = amount * RATES[currency]; result = rub / RATES[to]',
              'import argparse\n\nRATES = {"USD": 90, "EUR": 98, "CNY": 12.5, "RUB": 1}\nparser = argparse.ArgumentParser(prog="conv")\nparser.add_argument("amount", type=float)\n'
              'parser.add_argument("currency", choices=list(RATES))\nparser.add_argument("--to", choices=list(RATES), default="RUB")\nparser.add_argument("--round", type=int, default=2)\n'
              'total = 0\nwhile True:\n    s = input()\n    if s == "стоп":\n        break\n    args = parser.parse_args(s.split())\n    rub = args.amount * RATES[args.currency]\n'
              '    total += rub\n    print(f"{args.amount} {args.currency} = {round(rub / RATES[args.to], args.round)} {args.to}")\nprint(f"Всего в рублях: {round(total, 2)}")',
              ['100 USD\n50 EUR --to USD\n1000 RUB --to CNY --round 0\nстоп', '3.5 CNY --to EUR --round 4\nстоп'])


def build():
    return topic('Командная строка: свои утилиты', 'sys.argv, argparse, справка', [
        th_args(), fl_args(), code_args(),
        th_help(), fl_help(), code_help(),
        project(),
    ], opt=True)
