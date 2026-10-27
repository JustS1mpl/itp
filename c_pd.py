import os
from dsl import *

_D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'npdata')
FILESETS['students'] = {'students.csv': open(os.path.join(_D, 'students.csv'), encoding='utf-8', newline='').read().replace('\r\n', '\n')}
FILESETS['shots'] = {'data.csv': open(os.path.join(_D, 'data.csv'), encoding='utf-8', newline='').read().replace('\r\n', '\n')}
STU = FILESETS['students']


def _fig(key, alt, cap):
    return '<figure class="fig"><img class="figi" data-x="p-' + key + '" alt="' + alt + '"></figure><p class="mu" style="margin:-6px 0 12px;font-size:.88rem">' + cap + '</p>'


IMP = 'import numpy as np\nimport pandas as pd\n'


def build():
    # ============ Теория 1: Series ============
    terms1 = [
        ('pandas', 'Библиотека для работы с таблицами и рядами данных: загрузка из файлов, фильтрация, сортировка, группировка, подсчёты. Построена на numpy. Подключают так: import pandas as pd.\n\nПример:\nimport pandas as pd\nprint(pd.Series([1, 2, 3]))\nВывод:\n0    1\n1    2\n2    3\ndtype: int64'),
        ('Series', 'Одномерная структура pandas: значения вместе с подписями (индексом). Похожа и на список, и на словарь. Создаётся через pd.Series(данные, index=подписи).\n\nПример:\nimport pandas as pd\nprint(pd.Series([5, 7], index=["a", "b"]))\nВывод:\na    5\nb    7\ndtype: int64'),
        ('индекс Series', 'Подписи значений Series (index). По умолчанию это числа 0, 1, 2, ..., но можно задать любые, например названия товаров или имена. Индекс не обязан быть уникальным, но обычно таким бывает.'),
        ('NaN', 'Специальное значение «пропуск» (Not a Number): появляется там, где данных нет. Любой массив с NaN становится вещественным.\n\nПример:\nimport pandas as pd\nprint(pd.Series([1, None]))\nВывод:\n0    1.0\n1    NaN\ndtype: float64'),
        ('idxmax', 'Метод Series: возвращает не само наибольшее значение, а его подпись из индекса. Парный метод idxmin ищет наименьшее.\n\nПример:\nimport pandas as pd\nprint(pd.Series([3, 9, 5], index=["a", "b", "c"]).idxmax())\nВывод:\nb'),
    ]
    body1 = '''
<p>В прошлой теме мы работали с числами, а на практике данные редко живут «в одиночку». Чаще это таблицы: журналы оценок, список покупок, результаты измерений. Для них создана библиотека [[pandas|pandas]] (читается «пандас»). Это следующая ступень после numpy: pandas хранит данные в массивах numpy, но добавляет к ним подписи, умеет читать файлы и удобно считать итоги. Ей пользуются аналитики, учёные и разработчики.</p>
<p>Как и numpy, pandas не входит в стандартную поставку Python. В ИТП она подгружается автоматически при первом запуске программы с <code>import pandas</code> (нужен интернет, первый запуск занимает несколько секунд). Принято подключать обе библиотеки под короткими именами:</p>
<pre>import numpy as np
import pandas as pd</pre>
<p>В pandas два основных типа данных: [[Series|Series]] (один столбец или ряд значений) и DataFrame (таблица из нескольких столбцов). Начнём с первого.</p>

<h3>Series: значения с подписями</h3>
<p>[[Series|Series]] похож и на список (значения идут по порядку), и на словарь (у каждого значения есть подпись). Подписи называются [[индекс Series|индексом]]. Если ничего не указать, индекс будет числовым: 0, 1, 2, ...</p>
''' + ex(IMP + '''
s = pd.Series([10, 20, 30])
print(s)''') + '''
<p>Слева в выводе индекс, справа значения. Внизу pandas сообщает тип данных: <code>dtype: int64</code>. Чтобы задать свои подписи, передаём их в параметре <code>index</code>:</p>
''' + ex(IMP + '''
s = pd.Series(np.arange(5), index=["a", "b", "c", "d", "e"])
print(s)
print()
s = pd.Series(np.linspace(0, 1, 5))
print(s)''') + '''
<p>В качестве данных подходит список, массив numpy или словарь. Для словаря ключи становятся подписями:</p>
''' + ex(IMP + '''
d = {"a": 10, "b": 20, "c": 30, "g": 40}
print(pd.Series(d))''') + '''
<p>Если дополнительно передать <code>index</code>, то pandas возьмёт из словаря значения только для перечисленных подписей, а для тех, которых в словаре нет, поставит [[NaN|NaN]], то есть «значение отсутствует». NaN — особое вещественное число, поэтому весь ряд становится вещественным:</p>
''' + ex(IMP + '''
d = {"a": 10, "b": 20, "c": 30, "g": 40}
print(pd.Series(d, index=["a", "b", "c", "d"]))''') + '''
<p>А если передать одно число, обязательно нужно указать индекс. Число повторится для каждой подписи:</p>
''' + ex(IMP + '''
print(pd.Series(5, index=["a", "b", "c"]))''') + '''
<h3>Обращение к значениям</h3>
<p>К значениям обращаются по подписи в квадратных скобках. Если подписей несколько, передаём список подписей (скобки получаются двойными). Срез с числами работает по позициям, как у списков, а вот срез по подписям, наоборот, <b>включает конец</b>:</p>
''' + ex(IMP + '''
s = pd.Series(np.arange(5), index=["a", "b", "c", "d", "e"])
print(s["a"])
print(s[["a", "d"]])
print(s[1:3])
print(s["b":"d"])''') + '''
<p>Чтобы не путать позиции и подписи, у Series есть два явных способа: <code>s.loc[подпись]</code> и <code>s.iloc[номер позиции]</code>. Например, <code>s.iloc[0]</code> — первое значение, а <code>s.loc["e"]</code> — значение с подписью «e».</p>

<h3>Арифметика и фильтрация</h3>
<p>Как и у массивов numpy, операции применяются ко всем значениям сразу. Но есть важное отличие: при действиях между двумя Series значения подбираются <b>по подписям</b>, а не по позициям. Если пары не нашлось, получаем <code>NaN</code>:</p>
''' + ex(IMP + '''
s = pd.Series(np.arange(5), index=["a", "b", "c", "d", "e"])
print(s + s)
print(s * 10)
other = pd.Series([1, 2, 3], index=["a", "b", "z"])
print(s + other)''') + '''
<p>Условие создаёт Series из <code>True</code> и <code>False</code>, им можно «отфильтровать» значения, как и в numpy:</p>
''' + ex(IMP + '''
s = pd.Series(np.arange(5), index=["a", "b", "c", "d", "e"])
print(s > 2)
print(s[s > 2])''') + '''
<h3>Итоги по Series</h3>
<p>Привычные методы <code>sum()</code>, <code>mean()</code>, <code>min()</code>, <code>max()</code>, а также <code>len(s)</code> работают как и раньше. Кроме того, есть методы, которые отвечают не «сколько?», а «где?»: [[idxmax|idxmax()]] и <code>idxmin()</code> возвращают подпись наибольшего и наименьшего значения. Метод <code>sort_values()</code> упорядочивает Series по значениям, а <code>sort_index()</code> по подписям:</p>
''' + ex(IMP + '''
price = pd.Series([37, 58, 99, 72], index=["bread", "milk", "soda", "cream"])
print(price.sum())
print(price.mean())
print(price.idxmax())
print(price.idxmin())
print(price.sort_values())
print(price.sort_index())''') + '''
<p>Самый дорогой товар: «soda», самый дешёвый: «bread». Обратите внимание: <code>sort_values()</code> и <code>sort_index()</code> не меняют исходную серию, а возвращают новую.</p>

<h3>Имена</h3>
<p>У Series и у её индекса можно задать имена. Они ни на что не влияют, но выводятся и помогают понимать, что перед нами:</p>
''' + ex(IMP + '''
s = pd.Series(np.arange(5), index=["a", "b", "c", "d", "e"])
s.name = "Данные"
s.index.name = "Индекс"
print(s)''') + '''
<h3>Слова и их длины</h3>
<p>Серию удобно строить из результатов <code>map</code>: подписи берём из слов, значения из их длин. Подписи при этом могут быть строками, и тогда обращаться к значению можно по слову, как в словаре:</p>
''' + ex(IMP + '''
words = ["мама", "мыла", "раму", "мир"]
lengths = pd.Series(map(len, words), index=words)
print(lengths)
print(lengths["мир"])
print(lengths[lengths % 2 == 0])''') + '''
<p>Последняя строка выбирает слова чётной длины. Остаток от деления применяется ко всей серии сразу и создаёт серию из логических значений.</p>
'''
    th1 = th('pandas: Series', terms1, body1)

    fl1 = fl('Series', [
        qo('Что выведет программа?', 'import pandas as pd\ns = pd.Series([4, 6, 8], index=["a", "b", "c"])\nprint(s["b"])', ['6', '4', 'b'], 'Обращение по подписи «b» возвращает значение 6.'),
        qo('Что выведет программа?', 'import pandas as pd\ns = pd.Series([4, 6, 8], index=["a", "b", "c"])\nprint(s.idxmax())', ['c', '8', '2'], 'idxmax возвращает подпись наибольшего значения, а не само значение: 8 лежит под подписью c.'),
        qo('Что выведет программа?', 'import pandas as pd\ns = pd.Series([4, 6, 8], index=["a", "b", "c"])\nprint(len(s[s > 5]))', ['2', '3', '1'], 'Условие s > 5 оставляет значения 6 и 8. Их два.'),
        qo('Что выведет программа?', 'import pandas as pd\ns = pd.Series([4, 6, 8], index=["a", "b", "c"])\nprint(s["a":"b"].sum())', ['10', '4', '18'], 'Срез по подписям включает конец: берутся значения 4 и 6, их сумма 10.'),
        qo('Что выведет программа?', 'import pandas as pd\ns = pd.Series([4, 6, 8])\nprint(s.iloc[-1])', ['8', '6', '4'], 'iloc работает по позиции, как индексы списка: -1 это последнее значение.'),
        qo('Что выведет программа?', 'import pandas as pd\nprint(pd.Series([1, 2, 3]).sum() + pd.Series([10, 20]).sum())', ['36', '9', '33'], 'Сумма первой серии 6, второй серии 30, вместе 36.'),
        qo('Что выведет программа?', 'import pandas as pd\nprint((pd.Series([1, 2], index=["a", "b"]) + pd.Series([10, 20], index=["b", "c"])).isna().sum())', ['2', '0', '1'], 'Складываются значения с одинаковыми подписями. У «a» и «c» нет пары, поэтому там NaN. isna() отмечает их, а sum считает: 2.'),
        qo('Что выведет программа?', 'import pandas as pd\nprint(pd.Series(7, index=list("abc")).sum())', ['21', '7', '3'], 'Число 7 повторяется для каждой из трёх подписей: 7 + 7 + 7 = 21.'),
    ])

    # ============ Задачи на Series ============
    PD = 'import pandas as pd\n'
    t_ls = task(
        'Напиши функцию length_stats(text), которая получает текст и возвращает Series: в индексе слова, в значениях их длины. Слова нужно привести к нижнему регистру, убрать знаки препинания и цифры, оставить без повторов и упорядочить по алфавиту. Для проверки тесты используют pd, поэтому подключи pandas как pd.',
        ['Очисти текст: оставь только буквы и пробелы, например "".join(c for c in text.lower() if c.isalpha() or c.isspace()).', 'Разбей на слова и убери повторы: words = sorted(set(clean.split())).', 'Построй серию: pd.Series(map(len, words), index=words, dtype="int64").'],
        PD + '\n\ndef length_stats(text):\n    clean = "".join(c for c in text.lower() if c.isalpha() or c.isspace())\n    words = sorted(set(clean.split()))\n    return pd.Series(map(len, words), index=words, dtype="int64")',
        ["print(length_stats('Мама мыла раму'))", "print(length_stats('Лес, опушка, странный домик. Лес, опушка и зверушка.'))", "print(length_stats('Раз, два, три! Раз 2 раз 3'))"],
        tail=TL, starter=PD + '\n\n')
    t_oe = task(
        'Напиши функцию odd_even_words(text), которая делает то же, что length_stats из прошлой задачи (слова в нижнем регистре, без знаков препинания и цифр, без повторов, по алфавиту), но возвращает пару Series: сначала слова нечётной длины, потом слова чётной длины. Функцию length_stats повторно писать не нужно: опиши её в решении ещё раз, тесты вызывают обе.',
        ['Используй решение прошлой задачи: series = length_stats(text).', 'Слова чётной длины: series[series % 2 == 0].', 'Слова нечётной длины: series[series % 2 == 1]. Верни их парой: return odd, even.'],
        PD + '\n\ndef length_stats(text):\n    clean = "".join(c for c in text.lower() if c.isalpha() or c.isspace())\n    words = sorted(set(clean.split()))\n    return pd.Series(map(len, words), index=words, dtype="int64")\n\n\ndef odd_even_words(text):\n    series = length_stats(text)\n    return series[series % 2 == 1], series[series % 2 == 0]',
        ["odd, even = odd_even_words('Мама мыла раму')\nprint(odd)\nprint(even)", "odd, even = odd_even_words('Лес, опушка, странный домик. Лес, опушка и зверушка.')\nprint(odd)\nprint(even)", "odd, even = odd_even_words('Я и ты')\nprint(odd)\nprint(even)"],
        tail=TL, starter=PD + '\n\n')
    t_gl = task(
        'Напиши функцию get_long(series, min_length=5), которая принимает Series из задачи про длины слов (слова в индексе, длины в значениях) и возвращает только те слова, длина которых не меньше min_length. Исходную серию менять нельзя.',
        ['Условие на значения: series >= min_length.', 'Отфильтруй серию этим условием через квадратные скобки: series[series >= min_length].'],
        PD + '\n\ndef get_long(series, min_length=5):\n    return series[series >= min_length]',
        ["data = pd.Series([3, 5, 6, 6], ['мир', 'питон', 'привет', 'яндекс'])\nfiltered = get_long(data)\nprint(data)\nprint(filtered)", "data = pd.Series([3, 5, 6, 6], ['мир', 'питон', 'привет', 'яндекс'])\nfiltered = get_long(data, min_length=6)\nprint(data)\nprint(filtered)", "data = pd.Series([1, 2], ['я', 'ты'])\nprint(get_long(data, 3))"],
        tail=TL, starter=PD + '\n\n')
    ts1 = ts('Задачи на Series', [t_ls, t_oe, t_gl])

    # ============ Теория 2: DataFrame ============
    terms2 = [
        ('DataFrame', 'Таблица pandas: строки с подписями и именованные столбцы. Каждый столбец — это Series. Обычно создаётся из словаря «название столбца: список значений».\n\nПример:\nimport pandas as pd\nprint(pd.DataFrame({"a": [1, 2], "b": [3, 4]}))\nВывод:\n   a  b\n0  1  3\n1  2  4'),
        ('loc', 'Способ выбора данных DataFrame по подписям: df.loc[строки, столбцы]. Строки можно выбирать списком подписей, срезом или условием.\n\nПример:\nimport pandas as pd\ndf = pd.DataFrame({"a": [1, 2, 3]})\nprint(df.loc[df["a"] > 1, "a"].sum())\nВывод:\n5'),
        ('assign', 'Метод DataFrame: возвращает новую таблицу с добавленным или заменённым столбцом. Значение столбца можно задать функцией (например, lambda t: t["a"] * 2).\n\nПример:\nimport pandas as pd\nprint(pd.DataFrame({"a": [1, 2]}).assign(b=lambda t: t["a"] * 2))\nВывод:\n   a  b\n0  1  2\n1  2  4'),
        ('sort_values', 'Метод DataFrame: сортирует строки по одному или нескольким столбцам. Параметр ascending задаёт порядок (по возрастанию или по убыванию), для нескольких столбцов можно передать список.\n\nПример:\nimport pandas as pd\nprint(pd.DataFrame({"a": [2, 1]}).sort_values("a"))\nВывод:\n   a\n1  1\n0  2'),
        ('axis в pandas', 'Работает как в numpy: axis=0 обрабатывает столбцы (идём вниз по строкам), axis=1 обрабатывает строки (идём вправо по столбцам). Например, df.mean(axis=1) считает среднее по каждой строке.'),
    ]
    body2 = '''
<h3>DataFrame: таблица из столбцов</h3>
<p>[[DataFrame|DataFrame]] (по-русски «датафрейм») — основной тип pandas: таблица, у которой есть названия столбцов и подписи строк. Каждый столбец — отдельный Series, причём подписи строк у них общие. Проще всего создать таблицу из словаря: ключ — название столбца, значение — список данных:</p>
''' + ex(IMP + '''
students_marks_dict = {
    "student": ["Студент_1", "Студент_2", "Студент_3"],
    "math": [5, 3, 4],
    "physics": [4, 5, 5]
}
students = pd.DataFrame(students_marks_dict)
print(students)''') + '''
<p>Слева без названия подписи строк (по умолчанию 0, 1, 2, ...), сверху названия столбцов. Порядок столбцов можно задать параметром <code>columns</code>:</p>
''' + ex(IMP + '''
data = {"math": [5, 3, 4], "student": ["Студент_1", "Студент_2", "Студент_3"]}
print(pd.DataFrame(data, columns=["student", "math"]))''') + '''
<h3>Устройство таблицы</h3>
<p>Подписи строк и названия столбцов лежат в атрибутах <code>index</code> и <code>columns</code>. Размер таблицы: <code>shape</code> (строки, столбцы). Подписи строк можно заменить вручную:</p>
''' + ex(IMP + '''
students = pd.DataFrame({"student": ["Студент_1", "Студент_2", "Студент_3"], "math": [5, 3, 4]})
print(students.index)
print(students.columns)
print(students.shape)
students.index = ["A", "B", "C"]
print(students)''') + '''
<p>Столбец достаём по названию в квадратных скобках, и это настоящий Series. Если нужно несколько столбцов, передаём список названий (снова двойные скобки), получится уже таблица:</p>
''' + ex(IMP + '''
students = pd.DataFrame({"student": ["Студент_1", "Студент_2", "Студент_3"], "math": [5, 3, 4], "physics": [4, 5, 5]})
print(type(students["math"]))
print(students["math"].mean())
print(students[["student", "physics"]])''') + '''
<h3>Выбор строк и значений: loc</h3>
<p>Чтобы выбрать строки по подписям, используют [[loc|.loc]]. В квадратных скобках две части через запятую: что взять по строкам и что по столбцам. Для строк подойдёт подпись, список подписей, срез (с включением конца!) или условие. Если столбцы не нужны, их часть можно опустить:</p>
''' + ex(IMP + '''
students = pd.DataFrame({"student": ["Студент_1", "Студент_2", "Студент_3"], "math": [5, 3, 4], "physics": [4, 5, 5]},
                        index=["A", "B", "C"])
print(students.loc["B":])
print(students.loc["A", "math"])
print(students.loc[students["math"] > 3, ["student", "math"]])''') + '''
<p>Последняя строка отбирает только тех, у кого по математике больше трёх, и показывает только два столбца. Это самый частый приём фильтрации таблиц. Условия можно объединять: <code>&amp;</code> означает «и», <code>|</code> «или», а каждое условие обязательно берут в скобки (приоритет у этих знаков выше, чем у сравнений):</p>
''' + ex(IMP + '''
students = pd.DataFrame({"student": ["Студент_1", "Студент_2", "Студент_3"], "math": [5, 3, 4], "physics": [4, 5, 5]})
good = students.loc[(students["math"] >= 4) & (students["physics"] >= 5)]
print(good)
print(students.loc[students["math"].between(3, 4), "student"])''') + '''
<p>Метод <code>between(a, b)</code> проверяет, что число лежит между a и b включительно, и заменяет запись <code>(x &gt;= a) &amp; (x &lt;= b)</code>.</p>

<h3>Проверка сразу по нескольким столбцам: all и any</h3>
<p>Часто нужно проверить условие для нескольких столбцов сразу. Сравнение таблицы с числом даёт таблицу из <code>True</code> и <code>False</code>. Методы <code>all</code> и <code>any</code> с параметром [[axis в pandas|axis=1]] сворачивают её по строкам: <code>all</code> даёт <code>True</code>, если условие верно для <b>всех</b> выбранных столбцов, а <code>any</code>, если хотя бы для <b>одного</b>:</p>
''' + ex(IMP + '''
journal = pd.DataFrame({
    "name": ["Иванов", "Петров", "Сидоров"],
    "maths": [5, 4, 5],
    "physics": [4, 4, 2],
})
columns = ["maths", "physics"]
print(journal[columns] > 3)
print((journal[columns] > 3).all(axis=1))
print(journal.loc[(journal[columns] > 3).all(axis=1)])
print(journal.loc[(journal[columns] == 2).any(axis=1)])''') + '''
<p>Вторая таблица отвечает на вопрос «у кого все оценки выше трёх?», а последняя выбирает тех, у кого есть хотя бы одна двойка.</p>

<h3>Новые столбцы и сортировка</h3>
<p>Новый столбец можно добавить простым присваиванием, и таблица изменится. Среднее по нескольким столбцам считает <code>mean(axis=1)</code> (по каждой строке вдоль столбцов):</p>
''' + ex(IMP + '''
journal = pd.DataFrame({
    "name": ["Иванов", "Петров", "Сидоров"],
    "maths": [5, 4, 5],
    "physics": [4, 4, 2],
})
journal["average"] = journal[["maths", "physics"]].mean(axis=1)
print(journal)''') + '''
<p>Метод [[assign|assign]] делает то же самое, но не трогает исходную таблицу, а возвращает новую. В параметре передают столбец целиком или функцию от таблицы (удобно, когда нужно сослаться на столбцы, которые только что создали):</p>
''' + ex(IMP + '''
journal = pd.DataFrame({
    "name": ["Иванов", "Петров", "Сидоров"],
    "maths": [5, 4, 5],
    "physics": [4, 4, 2],
})
new = journal.assign(total=lambda t: t["maths"] + t["physics"])
print(new)
print(journal.columns.tolist())''') + '''
<p>Исходная таблица осталась без столбца <code>total</code>. Чтобы упорядочить строки, есть [[sort_values|sort_values]]: в первом параметре название столбца (или список названий), а <code>ascending</code> отвечает за порядок. Список ascending позволяет сортировать по одному столбцу по убыванию, а по другому по возрастанию (при одинаковых значениях первого столбца строки упорядочиваются по второму):</p>
''' + ex(IMP + '''
journal = pd.DataFrame({
    "name": ["Иванов", "Петров", "Сидоров", "Васечкин"],
    "maths": [5, 4, 5, 4],
    "physics": [4, 4, 2, 5],
})
print(journal.sort_values("maths"))
print(journal.sort_values(["maths", "name"], ascending=[False, True]))''') + '''
<p>Обратите внимание: подписи строк после сортировки «приехали» вместе со своими строками, поэтому идут вразнобой. Так pandas помнит, какая строка была какой.</p>

<h3>Меняем значения в таблице</h3>
<p>Присваивание через <code>.loc[условие, столбец]</code> меняет нужные значения прямо в таблице. Допустим, в магазине акция: если куплено больше двух штук, то цена товара снижается вдвое. Чтобы не испортить исходную таблицу, сначала делаем копию методом <code>copy()</code>:</p>
''' + ex(IMP + '''
cheque = pd.DataFrame({"product": ["cream", "milk", "soda"], "number": [1, 2, 3], "cost": [72, 116, 297]})
sale = cheque.copy()
sale.loc[sale["number"] > 2, "cost"] *= 0.5
print(cheque)
print(sale)''') + '''
<p>В копии стоимость соды упала вдвое, а исходная таблица осталась прежней. После умножения на <code>0.5</code> столбец стал вещественным: целые числа превратились в <code>72.0</code> и <code>116.0</code>.</p>
'''
    th2 = th('pandas: DataFrame', terms2, body2)

    fl2 = fl('DataFrame', [
        qo('Что выведет программа?', 'import pandas as pd\ndf = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})\nprint(df["b"].sum())', ['60', '6', '66'], 'df["b"] — столбец b как Series. Его сумма 10 + 20 + 30 = 60.'),
        qo('Что выведет программа?', 'import pandas as pd\ndf = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})\nprint(df.shape)', ['(3, 2)', '(2, 3)', '6'], 'Три строки и два столбца: shape равен (3, 2).'),
        qo('Что выведет программа?', 'import pandas as pd\ndf = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})\nprint(len(df.loc[df["a"] > 1]))', ['2', '3', '1'], 'Условие a > 1 отбирает две строки: со значениями 2 и 3.'),
        qo('Что выведет программа?', 'import pandas as pd\ndf = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})\nprint(df.loc[(df["a"] > 1) & (df["b"] < 30), "b"].sum())', ['20', '50', '30'], 'Обоим условиям удовлетворяет только вторая строка, где b равно 20.'),
        qo('Что выведет программа?', 'import pandas as pd\ndf = pd.DataFrame({"a": [1, 2], "b": [3, 4]})\nprint(df.mean(axis=1).sum())', ['5.0', '2.0', '10.0'], 'Среднее по строкам: 2.0 и 3.0. Их сумма 5.0.'),
        qo('Что выведет программа?', 'import pandas as pd\ndf = pd.DataFrame({"a": [1, 5], "b": [4, 6]})\nprint((df > 3).all(axis=1).sum())', ['1', '2', '3'], 'Во второй строке оба числа больше трёх, в первой нет. Подходящих строк одна.'),
        qo('Что выведет программа?', 'import pandas as pd\ndf = pd.DataFrame({"a": [1, 5], "b": [4, 2]})\nprint((df > 3).any(axis=1).sum())', ['2', '1', '0'], 'Хотя бы одно число больше трёх есть в обеих строках: 4 в первой и 5 во второй.'),
        qo('Что выведет программа?', 'import pandas as pd\ndf = pd.DataFrame({"a": [2, 1, 3]})\nprint(df.sort_values("a", ascending=False).index[0])', ['2', '0', '3'], 'Сортировка по убыванию ставит первой строку со значением 3. Её подпись 2 (строки нумеруются с нуля).'),
        qo('Что выведет программа?', 'import pandas as pd\ndf = pd.DataFrame({"a": [1, 2]})\nnew = df.assign(b=lambda t: t["a"] * 2)\nprint(list(df.columns))', ["['a']", "['a', 'b']", "['b']"], 'assign возвращает новую таблицу и не меняет исходную. В df по-прежнему один столбец.'),
    ])

    # ============ Задачи на DataFrame ============
    t_ch = task(
        'Магазин оформляет чеки. Напиши функцию cheque(price_list, **purchases): price_list — Series, где в индексе названия товаров, а в значениях цены; purchases — именованные аргументы вида «товар=количество». Функция возвращает DataFrame с колонками product, price, number, cost (название, цена, количество, стоимость = цена * количество). Строки идут по алфавиту названий товаров, подписи строк 0, 1, 2, ... Тесты используют pd, подключи pandas как pd.',
        ['Названия купленных товаров по алфавиту: names = sorted(purchases).', 'Цены этих товаров: prices = price_list[names] (список подписей даёт Series в том же порядке).', 'Собери таблицу: pd.DataFrame({"product": names, "price": prices.values, "number": [purchases[n] for n in names]}).', 'Добавь стоимость через assign: .assign(cost=lambda t: t["price"] * t["number"]).'],
        PD + '\n\ndef cheque(price_list, **purchases):\n    names = sorted(purchases)\n    prices = price_list[names]\n    table = pd.DataFrame({"product": names, "price": prices.values, "number": [purchases[n] for n in names]})\n    return table.assign(cost=lambda t: t["price"] * t["number"])',
        ["price_list = pd.Series([37, 58, 99, 72], ['bread', 'milk', 'soda', 'cream'])\nprint(cheque(price_list, soda=3, milk=2, cream=1))", "price_list = pd.Series([10, 5], ['a', 'b'])\nprint(cheque(price_list, b=4))", "price_list = pd.Series([37, 58, 99, 72], ['bread', 'milk', 'soda', 'cream'])\nprint(cheque(price_list, bread=1, soda=2).cost.sum())"],
        tail=TL, starter=PD + '\n\n')
    CHQ = PD + '\n\ndef cheque(price_list, **purchases):\n    names = sorted(purchases)\n    prices = price_list[names]\n    table = pd.DataFrame({"product": names, "price": prices.values, "number": [purchases[n] for n in names]})\n    return table.assign(cost=lambda t: t["price"] * t["number"])'
    t_di = task(
        'Магазин проводит акцию: на товары, купленные в количестве больше двух штук, скидка 50 процентов. Напиши функцию discount(cheque_table), которая принимает чек из прошлой задачи и возвращает новый чек с учётом акции (исходный менять нельзя). Функцию cheque из прошлой задачи оставь в решении, тесты её используют.',
        ['Сделай копию: result = cheque_table.copy().', 'Выбери строки с количеством больше двух и умножь их стоимость на 0.5: result.loc[result["number"] > 2, "cost"] *= 0.5.', 'Верни result.'],
        CHQ + '\n\n\ndef discount(cheque_table):\n    result = cheque_table.copy()\n    result.loc[result["number"] > 2, "cost"] *= 0.5\n    return result',
        ["price_list = pd.Series([37, 58, 99, 72], ['bread', 'milk', 'soda', 'cream'])\nresult = cheque(price_list, soda=3, milk=2, cream=1)\nwith_discount = discount(result)\nprint(result)\nprint(with_discount)", "price_list = pd.Series([10, 5], ['a', 'b'])\nr = cheque(price_list, a=5, b=1)\nprint(discount(r))", "price_list = pd.Series([10, 5], ['a', 'b'])\nr = cheque(price_list, a=1, b=2)\nprint(discount(r).cost.sum())"],
        tail=TL, starter=PD + '\n\n')
    JR = '''columns = ['name', 'maths', 'physics', 'computer science']
data = {
    'name': ['Иванов', 'Петров', 'Сидоров', 'Васечкин', 'Николаев'],
    'maths': [5, 4, 5, 2, 4],
    'physics': [4, 4, 4, 5, 5],
    'computer science': [5, 2, 5, 4, 3]
}
journal = pd.DataFrame(data, columns=columns)
'''
    t_be = task(
        'В журнале летней олимпиадной школы есть таблица (DataFrame) с колонками: name (имя), maths, physics и computer science (оценки по предметам). Напиши функцию best(journal), которая возвращает только «ударников»: строки учеников, у которых все три оценки выше тройки (больше 3). Тесты используют pd.',
        ['Список колонок с оценками: columns = ["maths", "physics", "computer science"].', 'Условие по всем колонкам сразу: (journal[columns] > 3).all(axis=1).', 'Выбери строки: journal.loc[условие].'],
        PD + '\n\ndef best(journal):\n    columns = ["maths", "physics", "computer science"]\n    return journal.loc[(journal[columns] > 3).all(axis=1)]',
        [JR + 'filtered = best(journal)\nprint(journal)\nprint(filtered)', "journal = pd.DataFrame({'name': ['А', 'Б'], 'maths': [4, 5], 'physics': [4, 3], 'computer science': [5, 5]})\nprint(best(journal))", "journal = pd.DataFrame({'name': ['А'], 'maths': [3], 'physics': [3], 'computer science': [3]})\nprint(len(best(journal)))"],
        tail=TL, starter=PD + '\n\n')
    t_nw = task(
        'Продолжим работать с журналом из прошлой задачи. Напиши функцию need_to_work_better(journal), которая возвращает строки учеников, у которых есть хотя бы одна двойка.',
        ['Колонки с оценками: columns = ["maths", "physics", "computer science"].', 'Хотя бы одна двойка: (journal[columns] == 2).any(axis=1).', 'Выбери строки: journal.loc[условие].'],
        PD + '\n\ndef need_to_work_better(journal):\n    columns = ["maths", "physics", "computer science"]\n    return journal.loc[(journal[columns] == 2).any(axis=1)]',
        [JR + 'filtered = need_to_work_better(journal)\nprint(journal)\nprint(filtered)', "journal = pd.DataFrame({'name': ['А', 'Б'], 'maths': [2, 5], 'physics': [4, 2], 'computer science': [5, 5]})\nprint(need_to_work_better(journal))", "journal = pd.DataFrame({'name': ['А'], 'maths': [5], 'physics': [5], 'computer science': [5]})\nprint(len(need_to_work_better(journal)))"],
        tail=TL, starter=PD + '\n\n')
    t_up = task(
        'Продолжим работать с журналом. Напиши функцию update(journal), которая возвращает новую таблицу: к данным добавлен столбец average (средняя оценка ученика по трём предметам), а строки упорядочены по убыванию средней оценки, а при равных оценках по имени (по алфавиту). Исходная таблица не должна меняться.',
        ['Добавь среднее через assign: journal.assign(average=lambda t: t[columns].mean(axis=1)), где columns = ["maths", "physics", "computer science"].', 'Отсортируй: .sort_values(["average", "name"], ascending=[False, True]).'],
        PD + '\n\ndef update(journal):\n    columns = ["maths", "physics", "computer science"]\n    result = journal.assign(average=lambda t: t[columns].mean(axis=1))\n    return result.sort_values(["average", "name"], ascending=[False, True])',
        [JR + 'filtered = update(journal)\nprint(journal)\nprint(filtered)', "journal = pd.DataFrame({'name': ['Б', 'А'], 'maths': [3, 3], 'physics': [4, 4], 'computer science': [5, 5]})\nprint(update(journal))", "journal = pd.DataFrame({'name': ['А', 'Б'], 'maths': [2, 5], 'physics': [2, 5], 'computer science': [2, 5]})\nprint(update(journal).name.tolist())"],
        tail=TL, starter=PD + '\n\n')
    ts2 = ts('Задачи на DataFrame', [t_ch, t_di, t_be, t_nw, t_up])

    # ============ Теория 3: таблицы из файлов ============
    terms3 = [
        ('CSV', 'Текстовый формат таблиц: одна строка файла — одна строка таблицы, значения разделены запятыми, первая строка обычно содержит названия столбцов.'),
        ('read_csv', 'Функция pandas: читает CSV-файл и возвращает DataFrame. Первая строка файла становится названиями столбцов.\n\nПример:\nimport pandas as pd\ndata = pd.read_csv("students.csv")\nprint(data.shape)'),
        ('head', 'Метод DataFrame: возвращает первые n строк таблицы (по умолчанию пять). Парный метод tail возвращает последние n строк.\n\nПример:\nimport pandas as pd\nprint(pd.Series([1, 2, 3]).head(2))\nВывод:\n0    1\n1    2\ndtype: int64'),
        ('groupby', 'Метод DataFrame: разбивает строки на группы по значениям одного или нескольких столбцов. После него вызывают подсчёт: count, sum, mean или agg.\n\nПример:\nimport pandas as pd\ndf = pd.DataFrame({"k": ["a", "b", "a"], "v": [1, 2, 3]})\nprint(df.groupby("k")["v"].sum())\nВывод:\nk\na    4\nb    2\nName: v, dtype: int64'),
        ('agg', 'Метод для сгруппированных данных: считает сразу несколько итогов. В словаре указывают столбец и список функций, например {"math score": ["mean", "median"]}.'),
    ]
    body3 = '''
<h3>Данные живут в файлах</h3>
<p>Таблицы с данными обычно хранят в файлах, а такие наборы данных называют <b>датасетами</b>. Самый популярный формат: [[CSV|CSV]]: обычный текстовый файл, в котором значения разделены запятыми, а первая строка содержит названия столбцов. Мы уже читали такие файлы в прошлых темах вручную. В pandas это делается одной строкой.</p>
<p>Для примеров мы возьмём файл <code>students.csv</code> с результатами тестов тысячи школьников (оценки вымышленные, но устроены как настоящие). Вот его начало:</p>
<pre>gender,race/ethnicity,parental level of education,lunch,test preparation course,math score,reading score,writing score
female,group B,bachelor's degree,standard,completed,66,71,80
female,group B,some college,free/reduced,completed,80,100,95
female,group E,associate's degree,free/reduced,completed,90,100,100</pre>
<p>В нём 8 столбцов: пол, группа, образование родителей, тип обеда, прошёл ли подготовительный курс и баллы за тесты по математике, чтению и письму. В примерах ниже файл лежит рядом с программой. Читает его функция [[read_csv|pd.read_csv]], она возвращает DataFrame:</p>
''' + ex(IMP + '''
students = pd.read_csv("students.csv")
print(type(students))
print(students.shape)
print(students.columns.tolist())''', files=STU) + '''
<p>В файле 1000 строк и 8 столбцов. Сохранить таблицу в файл можно методом <code>to_csv("имя.csv")</code>. А для других форматов есть <code>read_json</code> и <code>to_json</code>, <code>read_excel</code> и <code>to_excel</code>, остальные настройки смотрите в документации pandas.</p>

<h3>Заглянуть в таблицу: head и tail</h3>
<p>Печатать тысячу строк не нужно: pandas при выводе большой таблицы сам прячет середину и показывает многоточие. Метод [[head|head(n)]] возвращает первые <code>n</code> строк (по умолчанию пять), а <code>tail(n)</code> последние:</p>
''' + ex(IMP + '''
students = pd.read_csv("students.csv")
print(students[["gender", "math score", "reading score"]].head())
print(students[["gender", "math score", "reading score"]].tail(3))''', files=STU) + '''
<p>Обратите внимание на подписи строк: они идут от 0 до 999. Срез <code>students[10:13]</code> тоже работает, как у списка, и берёт строки с номерами 10, 11 и 12. Чтобы узнать, сколько каких значений встречается в столбце, есть метод <code>value_counts()</code>:</p>
''' + ex(IMP + '''
students = pd.read_csv("students.csv")
print(students[10:13][["gender", "math score"]])
print(students["gender"].value_counts())
print(students["math score"].max())
print(students["math score"].mean())''', files=STU) + '''
<h3>Фильтры и сортировка на реальных данных</h3>
<p>Те же условия, что и раньше. Выберем первых пять человек, прошедших подготовительный курс, и посмотрим на их результаты по математике:</p>
''' + ex(IMP + '''
students = pd.read_csv("students.csv")
done = students[students["test preparation course"] == "completed"]
print(done["math score"].head())''', files=STU) + '''
<p>Теперь выведем пять лучших результатов этой группы по трём предметам. Сортируем по математике, а при равных баллах по чтению, а затем по письму:</p>
''' + ex(IMP + '''
students = pd.read_csv("students.csv")
done = students[students["test preparation course"] == "completed"]
top = done[["math score", "reading score", "writing score"]].sort_values(
    ["math score", "reading score", "writing score"], ascending=False)
print(top.head())''', files=STU) + '''
<p>Столбец с суммарным баллом добавляется арифметикой над столбцами. Затем сортируем таблицу по нему. Покажем только нужные столбцы, чтобы вывод поместился в строку. Учтите, что у нескольких учеников суммы одинаковые (три лучших набрали по 300), и в какой последовательности pandas выведет такие строки, заранее не гарантируется:</p>
''' + ex(IMP + '''
students = pd.read_csv("students.csv")
scores = students.assign(total=lambda t: t["math score"] + t["reading score"] + t["writing score"])
best = scores.sort_values("total", ascending=False).head()
print(best[["gender", "math score", "reading score", "writing score", "total"]])''', files=STU) + '''
<h3>Группировка и итоги</h3>
<p>Метод [[groupby|groupby]] разбивает таблицу на группы по значениям столбцов. За ним указывают столбец, который нас интересует, и функцию подсчёта. Узнаем, сколько учеников каждого пола прошло и не прошло курс:</p>
''' + ex(IMP + '''
students = pd.read_csv("students.csv")
print(students.groupby(["gender", "test preparation course"])["writing score"].count())''', files=STU) + '''
<p>Подписи результата теперь составные: пол и наличие курса. А если нужны сразу несколько итогов, помогает метод [[agg|agg]]: в словаре указываем столбец и список функций. Сравним среднее и медиану баллов по математике:</p>
''' + ex(IMP + '''
students = pd.read_csv("students.csv")
agg_functions = {"math score": ["mean", "median"]}
print(students.groupby(["gender", "test preparation course"]).agg(agg_functions))''', files=STU) + '''
<p>Видно, что ученики, прошедшие курс, в среднем набрали больше баллов. Одно число группы считают проще: достаточно написать <code>.mean()</code> сразу после столбца:</p>
''' + ex(IMP + '''
students = pd.read_csv("students.csv")
print(students.groupby("lunch")["math score"].mean().round(2))''', files=STU) + '''
<p>Метод <code>round(2)</code> округляет все числа серии до двух знаков после запятой.</p>
'''
    th3 = th('pandas: файлы CSV, фильтры, groupby', terms3, body3)

    # ============ Теория 4: matplotlib ============
    terms4 = [
        ('matplotlib', 'Библиотека для построения графиков и диаграмм. Подключают модуль pyplot под коротким именем: import matplotlib.pyplot as plt.'),
        ('гистограмма', 'Диаграмма из столбиков: диапазон значений разбивают на равные корзины и по высоте столбика показывают, сколько значений попало в каждую.'),
        ('plt.hist', 'Функция matplotlib: строит гистограмму по данным. Параметр bins задаёт число корзин (по умолчанию 10), label добавляет подпись для легенды.'),
        ('plt.show', 'Функция matplotlib: показывает построенный график. В ИТП график появляется картинкой под выводом программы.'),
    ]
    body4 = '''
<h3>График по данным</h3>
<p>Таблицы хорошо считают, а картинки хорошо показывают. Для графиков в Python есть библиотека [[matplotlib|matplotlib]] (читается «мэтплотлиб»), и pandas использует её для своих графиков. Подключается она так же: в ИТП сама подгрузится при первом запуске. Принято подключать модуль <code>pyplot</code> под именем <code>plt</code>:</p>
<pre>import matplotlib.pyplot as plt</pre>
<p>Построим [[гистограмма|гистограмму]] баллов по математике: диапазон от 0 до 100 делится на 10 корзин по 10 баллов, а высота столбика показывает, сколько школьников попало в корзину. Функция [[plt.hist|plt.hist]] принимает данные, а остальные функции подписывают оси и добавляют легенду. В конце [[plt.show|plt.show()]] выводит график:</p>
<pre>import pandas as pd
import matplotlib.pyplot as plt

students = pd.read_csv("students.csv")
plt.hist(students["math score"], label="Тест по математике")
plt.xlabel("Баллы за тест")
plt.ylabel("Количество студентов")
plt.legend()
plt.show()</pre>
''' + _fig('pd_hist', 'Гистограмма баллов за тест по математике: большинство результатов между 50 и 80 баллами', 'Распределение баллов: чем выше столбик, тем больше школьников набрали столько баллов. Больше всего результатов между 60 и 70.') + '''
<p>Читаем график: по горизонтали баллы, по вертикали количество школьников. Самый высокий столбик над промежутком от 60 до 70: около 270 человек. Очень низких и очень высоких результатов мало, и вся картина похожа на «горку» (в статистике её называют нормальным распределением).</p>
<p>Цифры можно получить и без картинки: функция numpy <code>np.histogram</code> возвращает количество значений в каждой корзине (а также границы корзин):</p>
''' + ex(IMP + '''
students = pd.read_csv("students.csv")
counts, edges = np.histogram(students["math score"])
print(counts)
print(edges)''', files=STU) + '''
<p>Корзин десять, поэтому столбиков десять. Чтобы разбить диапазон мельче, передайте <code>bins=20</code> в <code>plt.hist</code>. Каждую функцию библиотеки <code>plt</code> можно вызывать по очереди, пока график не показан: сначала <code>hist</code>, потом подписи, и только в конце <code>show</code>.</p>
'''
    th4 = th('matplotlib: гистограмма', terms4, body4)

    fl3 = fl('Файлы и группировка', [
        qo('Что выведет программа?', 'import pandas as pd\ndf = pd.DataFrame({"k": ["a", "b", "a"], "v": [1, 2, 3]})\nprint(df.groupby("k")["v"].sum()["a"])', ['4', '3', '6'], 'Группа «a» состоит из строк со значениями 1 и 3. Их сумма 4.'),
        qo('Что выведет программа?', 'import pandas as pd\ndf = pd.DataFrame({"k": ["a", "b", "a"], "v": [1, 2, 3]})\nprint(df.groupby("k")["v"].count()["b"])', ['1', '2', '3'], 'В группе «b» одна строка, поэтому count даёт 1.'),
        qo('Что выведет программа?', 'import pandas as pd\ndf = pd.DataFrame({"k": ["a", "b", "a"], "v": [1, 2, 3]})\nprint(df.groupby("k")["v"].mean()["a"])', ['2.0', '4.0', '1.5'], 'Среднее значений 1 и 3 равно 2.0 (мы делим на два, поэтому число вещественное).'),
        qo('Что выведет программа?', 'import pandas as pd\ndf = pd.DataFrame({"v": range(10)})\nprint(len(df.head()))', ['5', '10', '1'], 'Если число строк не указано, head возвращает пять строк.'),
        qo('Что выведет программа?', 'import pandas as pd\ndf = pd.DataFrame({"v": range(10)})\nprint(df.tail(3)["v"].iloc[0])', ['7', '3', '9'], 'tail(3) возвращает три последние строки: 7, 8, 9. Первая из них 7.'),
        qo('Что выведет программа?', 'import pandas as pd\ndf = pd.DataFrame({"v": [3, 1, 2]})\nprint(df.sort_values("v").index[0])', ['1', '0', '3'], 'Наименьшее значение 1 лежит в строке с подписью 1.'),
        qo('Что выведет программа?', 'import pandas as pd\ndf = pd.DataFrame({"v": [1, 5, 9]})\nprint(df["v"].between(2, 9).sum())', ['2', '3', '1'], 'between включает концы: 5 и 9 подходят, а 1 нет.'),
        qo('Что выведет программа?', 'import pandas as pd\ndf = pd.DataFrame({"v": [1, 5, 9]})\nprint(df["v"].mean())', ['5.0', '5', '15'], 'Среднее (1 + 5 + 9) / 3 = 5.0. Среднее всегда вещественное число.'),
    ])

    # ============ Задачи по DataFrame из файлов ============
    t_sh = task(
        'В игре «Морской бой» поле не имеет границ, а выстрелы противника записаны в файл data.csv: столбцы x и y содержат координаты выстрелов. Игрок хочет узнать, какие выстрелы пришлись на прямоугольный участок. В первой строке ввода записаны координаты левого верхнего угла прямоугольника (x1 y1), во второй правого нижнего (x2 y2). Выведи часть датасета, лежащую в прямоугольнике (границы входят), в том виде, как её печатает pandas (с подписями строк). Файл data.csv лежит рядом с программой. Подключи pandas как pd.',
        ['Загрузи данные: data = pd.read_csv("data.csv").', 'Прочитай оба угла: x1, y1 = map(int, input().split()) и x2, y2 = map(int, input().split()).', 'Выбери строки: data.loc[data["x"].between(x1, x2) & data["y"].between(y2, y1)] (y1 в верхнем углу, а значит он больше y2). Выведи результат.'],
        PD + 'data = pd.read_csv("data.csv")\nx1, y1 = map(int, input().split())\nx2, y2 = map(int, input().split())\nprint(data.loc[data["x"].between(x1, x2) & data["y"].between(y2, y1)])',
        ['-20 20\n20 -20', '0 5\n5 0', '100 100\n140 60', '-300 -250\n-260 -290'], files='shots')
    t_ex = task(
        'Экстремум функции — это её наибольшее или наименьшее значение на заданном участке. Напиши три функции: values(func, start, end, step) строит Series значений функции func (функция одной переменной) в точках диапазона от start до end (конец не включается) с шагом step: в индексе точки, в значениях значения функции. min_extremum(data) возвращает точку, в которой на диапазоне достигнут минимум, а max_extremum(data) возвращает точку, где достигнут максимум. В решении оставь только функции и импорты, вызовы функций тесты сделают сами. Подключи numpy как np и pandas как pd.',
        ['Точки диапазона: x = np.arange(start, end, step).', 'Значения: pd.Series([func(v) for v in x], index=x).', 'Минимум и максимум по подписи нашёл бы idxmin и idxmax.'],
        IMP + '\n\ndef values(func, start, end, step):\n    x = np.arange(start, end, step)\n    return pd.Series([func(v) for v in x], index=x)\n\n\ndef min_extremum(data):\n    return data.idxmin()\n\n\ndef max_extremum(data):\n    return data.idxmax()',
        ['data = values(lambda x: x ** 2 + 2 * x + 1, -1.5, 1.75, 0.25)\nprint(data)\nprint(min_extremum(data))\nprint(max_extremum(data))', 'data = values(lambda x: -x ** 2 + 4, -3, 3.5, 0.5)\nprint(min_extremum(data), max_extremum(data))', 'data = values(lambda x: 3 * x - 1, 0, 2, 0.5)\nprint(len(data), min_extremum(data), max_extremum(data))'],
        tail=TL, starter=IMP + '\n\n')
    t_gr = task(
        'В файле students.csv лежат результаты тестов школьников (столбцы gender, race/ethnicity, parental level of education, lunch, test preparation course, math score, reading score, writing score). С клавиатуры вводится название столбца, по которому нужно сгруппировать данные (например, gender или lunch). Выведи средний балл по математике (math score) для каждого значения этого столбца, округлив до 2 знаков после запятой.',
        ['Прочитай название столбца: column = input().', 'Загрузи таблицу: students = pd.read_csv("students.csv").', 'Сгруппируй и посчитай: students.groupby(column)["math score"].mean().round(2). Выведи результат через print.'],
        PD + 'column = input()\nstudents = pd.read_csv("students.csv")\nprint(students.groupby(column)["math score"].mean().round(2))',
        ['gender', 'lunch', 'test preparation course', 'race/ethnicity'], files='students')
    t_ni = task(
        'В файле students.csv лежат результаты тестов школьников. Сколько школьников набрали не менее 90 баллов по всем трём предметам сразу (math score, reading score и writing score)? Выведи одно число.',
        ['Загрузи таблицу: students = pd.read_csv("students.csv").', 'Колонки с баллами: scores = students[["math score", "reading score", "writing score"]].', 'Условие по всем колонкам: (scores >= 90).all(axis=1). Количество подходящих строк: .sum().'],
        PD + 'students = pd.read_csv("students.csv")\nscores = students[["math score", "reading score", "writing score"]]\nprint((scores >= 90).all(axis=1).sum())',
        [''], files='students')
    ts3 = ts('Задачи на pandas и данные из файлов', [t_sh, t_ex, t_gr, t_ni])

    return topic('Модуль pandas', 'Series и DataFrame, фильтры, сортировка, группировка, файлы CSV и график matplotlib',
                 [th1, fl1, ts1, th2, fl2, ts2, th3, th4, fl3, ts3])
