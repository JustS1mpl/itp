from dsl import *

# Нора после «Таблицы данных»: графики matplotlib. В приложении plt.show() показывает рисунок картинкой под выводом программы
# (glue.py, _itp_mpl); примеры теории картинку не показывают — их предлагаем запустить в разделе «Код».
# Код с matplotlib dsl.py запускает в Pyodide (PYO_RE). В задачах проверяется напечатанный итог, график — для глаз.
# Две теории: линии и столбцы (plot, bar, подписи, легенда); гистограммы и данные из CSV.

GRADES = 'имя,класс,балл\nАня,9А,87\nБорис,9А,64\nВика,9Б,92\nГлеб,9Б,71\nДина,9А,78\nЕгор,9Б,55\nЖанна,9А,95\nЗоя,9Б,83\nИлья,9А,69\nКира,9Б,88\n'


def th_lines():
    terms = [
        ('matplotlib', 'Библиотека графиков. Рисуют её частью pyplot: import matplotlib.pyplot as plt. В ИТП график появляется под выводом программы.'),
        ('plot', 'plt.plot(xs, ys, label=…, marker="o") — линия по точкам; label — подпись для легенды.'),
        ('bar', 'plt.bar(подписи, значения) — столбчатая диаграмма.'),
        ('title', 'plt.title(текст) — заголовок графика.'),
        ('xlabel', 'plt.xlabel(текст) — подпись горизонтальной оси; ylabel — вертикальной.'),
        ('ylabel', 'plt.ylabel(текст) — подпись вертикальной оси.'),
        ('legend', 'plt.legend() — показать легенду: подписи линий из label.'),
        ('show', 'plt.show() — показать график. В ИТП он появится картинкой под выводом программы.'),
    ]
    body = (
        '<p>Числа в таблице видно не сразу, а на графике — с первого взгляда. Графики рисует библиотека [[matplotlib]], её часть pyplot подключают как '
        '<code>plt</code>. Линию по точкам строит [[plot]], столбцы — [[bar]], а [[title]], [[xlabel]], [[ylabel]] и [[legend]] подписывают '
        'график. Показывает его [[show]]. Картинку здесь не видно — скопируй пример в раздел «Код» и запусти:</p>'
        + ex('import matplotlib.pyplot as plt\n\ndays = ["пн", "вт", "ср", "чт", "пт"]\ntyumen = [-3, -1, 2, 0, -4]\nsochi = [14, 15, 13, 16, 17]\n'
             'plt.plot(days, tyumen, label="Тюмень", marker="o")\nplt.plot(days, sochi, label="Сочи", marker="o")\nplt.title("Температура за неделю")\n'
             'plt.xlabel("день")\nplt.ylabel("°C")\nplt.legend()\nplt.show()\nprint("Разница в среднем:", (sum(sochi) - sum(tyumen)) / len(days))') +
        '<p>Каждый вызов plot добавляет линию на тот же график — так удобно сравнивать. Столбцы подходят для сравнения категорий:</p>'
        + ex('import matplotlib.pyplot as plt\n\nvotes = {"пицца": 12, "суши": 7, "бургеры": 9, "салат": 3}\nplt.bar(list(votes), list(votes.values()))\n'
             'plt.title("Что заказать на праздник")\nplt.ylabel("голосов")\nplt.show()\nprint("Победила", max(votes, key=votes.get))') +
        '<p>Хороший график понятен без объяснений: у него есть заголовок, подписи осей с единицами измерения и легенда, если линий несколько.</p>'
    )
    return th('Линии и столбцы', terms, body)


def fl_lines():
    return fl('Линии и столбцы', [
        q('Как нарисовать две линии на одном графике?', 'Вызвать plt.plot дважды до plt.show()', ['plt.plot2(x, y1, y2)', 'Это невозможно'],
          'Каждый plot добавляет линию.'),
        q('Что нужно, чтобы на графике появились подписи линий?', 'label у каждого plot и вызов plt.legend()', ['Только plt.title', 'plt.xlabel'],
          'legend собирает подписи из label.'),
        q('Какой график лучше для сравнения голосов за пять вариантов?', 'Столбчатая диаграмма', ['Линия по дням', 'Гистограмма'],
          'Варианты — категории, а не время.'),
    ])


def code_lines():
    return ts('Линии и столбцы', [
        task('Шаги. На вход подаются числа шагов по дням недели через пробел (7 чисел). Нарисуй линию по дням 1–7 с точками и подписями осей, '
             'горизонтальную линию цели 10000 шагов (второй plot по двум точкам) и покажи график. Выведи «Дней с целью: N» (не меньше 10000) и '
             '«Лучший день: D (S шагов)» — первый день с максимумом.',
             'plt.plot(range(1, 8), steps, marker="o"); цель — plt.plot([1, 7], [10000, 10000]). Лучший день — steps.index(max(steps)) + 1.',
             'import matplotlib.pyplot as plt\n\nsteps = list(map(int, input().split()))\ndays = list(range(1, 8))\nplt.plot(days, steps, marker="o", label="шаги")\n'
             'plt.plot([1, 7], [10000, 10000], label="цель")\nplt.xlabel("день")\nplt.ylabel("шаги")\nplt.legend()\nplt.show()\n'
             'print(f"Дней с целью: {sum(1 for s in steps if s >= 10000)}")\nbest = steps.index(max(steps))\nprint(f"Лучший день: {best + 1} ({steps[best]} шагов)")',
             ['8000 12000 9500 15000 10000 3000 11000', '500 600 700 800 900 1000 1100']),
        task('Опрос. На вход подаются ответы участников через пробел (одно слово — один голос). Нарисуй столбцы: варианты по убыванию голосов (при '
             'равенстве — по алфавиту), с заголовком «Опрос». Выведи строки «ВАРИАНТ: N» в том же порядке.',
             'Counter(input().split()); отсортированные пары — sorted(counts.items(), key=lambda p: (-p[1], p[0])).\nСтолбцы: plt.bar([p[0] for p in pairs], [p[1] for p in pairs]).',
             'from collections import Counter\nimport matplotlib.pyplot as plt\n\ncounts = Counter(input().split())\npairs = sorted(counts.items(), key=lambda p: (-p[1], p[0]))\n'
             'plt.bar([p[0] for p in pairs], [p[1] for p in pairs])\nplt.title("Опрос")\nplt.show()\nfor name, n in pairs:\n    print(f"{name}: {n}")',
             ['кино каток кино музей каток кино', 'да']),
    ])


def th_hist():
    terms = [
        ('hist', 'plt.hist(значения, bins=k) — гистограмма: делит значения на k интервалов и рисует, сколько попало в каждый.'),
        ('гистограмма', 'График распределения: по горизонтали — интервалы значений, по вертикали — сколько значений в каждом. Показывает, каких '
                        'значений много, а каких мало.'),
    ]
    body = (
        '<p>Когда значений много, интересно не каждое, а как они распределены: сколько учеников набрали 90+, сколько — меньше 60. Это показывает '
        '[[гистограмма]]: значения делят на интервалы и рисуют столбик для каждого. Строит её [[hist]]:</p>'
        + ex('import matplotlib.pyplot as plt\n\nscores = [87, 64, 92, 71, 78, 55, 95, 83, 69, 88, 74, 91]\nplt.hist(scores, bins=[50, 60, 70, 80, 90, 100])\n'
             'plt.title("Баллы за контрольную")\nplt.xlabel("балл")\nplt.ylabel("учеников")\nplt.show()\nfor lo in range(50, 100, 10):\n'
             '    print(f"{lo}–{lo + 9}:", sum(1 for s in scores if lo <= s < lo + 10))') +
        '<p>bins можно задать числом (столько равных интервалов) или списком границ — так интервалы получаются ровными: 50–59, 60–69 и так далее. '
        'Последний интервал у hist включает правую границу, поэтому 100 попадёт в 90–100.</p>'
        '<h3>Данные из CSV</h3>'
        '<p>Обычно данные приходят файлом. pandas читает его, группирует, а matplotlib рисует результат:</p>'
        + ex('import pandas as pd\nimport matplotlib.pyplot as plt\n\ndf = pd.read_csv("grades.csv")\nmeans = df.groupby("класс")["балл"].mean()\n'
             'plt.bar(means.index, means.values)\nplt.title("Средний балл по классам")\nplt.show()\nfor c, m in zip(means.index, means.values):\n    print(c, round(m, 1))', files={'grades.csv': GRADES})
    )
    return th('Гистограммы и данные', terms, body)


def fl_hist():
    return fl('Гистограммы и данные', [
        q('Что показывает гистограмма баллов?', 'Сколько учеников попало в каждый интервал баллов', ['Балл каждого ученика по порядку', 'Средний балл'],
          'Это распределение значений.'),
        q('Что значит bins=[0, 50, 100] в plt.hist?', 'Два интервала: 0–50 и 50–100', ['50 интервалов', 'Три столбика по 50'], 'Список — границы интервалов.'),
        q('Чем гистограмма отличается от столбчатой диаграммы bar?', 'hist сама считает, сколько значений в каждом интервале', ['Ничем', 'bar нельзя подписать'],
          'В bar высоты столбцов задаёшь сам.'),
    ])


def code_hist():
    return ts('Гистограммы и данные', [
        task('Время сна. На вход подаются часы сна учеников через пробел (дробные числа). Нарисуй гистограмму с границами 4, 6, 8, 10, 12 и выведи '
             'строки «A–B ч: N» для интервалов 4–6, 6–8, 8–10, 10–12 (значение попадает в интервал, если A ≤ значение < B; 12 — в последний). '
             'Затем «Высыпаются: P%» — доля спящих 8 часов и больше, округлённая до целого.',
             'Счёт: для каждой пары границ — sum(1 for h in hours if a <= h < b), а для последнего интервала условие h <= b.\nДоля: round(100 * k / len(hours)).',
             'import matplotlib.pyplot as plt\n\nhours = list(map(float, input().split()))\nedges = [4, 6, 8, 10, 12]\nplt.hist(hours, bins=edges)\nplt.xlabel("часы")\nplt.show()\n'
             'for i in range(4):\n    a, b = edges[i], edges[i + 1]\n    n = sum(1 for h in hours if a <= h < b or (i == 3 and h == b))\n    print(f"{a}–{b} ч: {n}")\n'
             'print(f"Высыпаются: {round(100 * sum(1 for h in hours if h >= 8) / len(hours))}%")',
             ['7.5 8 6 9.5 5 8.5 10 12 7', '8 8 8']),
        task('Классы. Рядом с программой лежит grades.csv: имя, класс, балл. Нарисуй столбцы среднего балла по классам и выведи по классам в '
             'алфавитном порядке «КЛАСС: средний X, лучший ИМЯ (Б)», средний — с одним знаком.',
             'means = df.groupby("класс")["балл"].mean(); лучший в классе — строка с максимумом балла: в цикле по классам t = df[df["класс"] == c], '
             'лучший — t.loc[t["балл"].idxmax()].',
             'import pandas as pd\nimport matplotlib.pyplot as plt\n\ndf = pd.read_csv("grades.csv")\nmeans = df.groupby("класс")["балл"].mean()\nplt.bar(means.index, means.values)\n'
             'plt.show()\nfor c in means.index:\n    t = df[df["класс"] == c]\n    best = t.loc[t["балл"].idxmax()]\n'
             '    print(f"{c}: средний {means[c]:.1f}, лучший {best[\'имя\']} ({best[\'балл\']})")',
             [''], files={'grades.csv': GRADES}),
    ])


def build():
    return topic('Matplotlib: графики по данным', 'линии, столбцы, гистограммы, CSV', [
        th_lines(), fl_lines(), code_lines(),
        th_hist(), fl_hist(), code_hist(),
    ], opt=True)
