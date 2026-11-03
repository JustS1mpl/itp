from dsl import *

# Нора после «Поиск и сортировка»: свой Paint. Рабочая программа рисования на tkinter Canvas — код для компьютера (<pre class="pc">,
# в браузере окон нет). В приложении — логика холста: холст как сетка символов, точки, линии, прямоугольники, отмена и повтор
# (стек снимков), заливка обходом в ширину (deque). Две теории: холст и инструменты; заливка. Мини-проект — Paint по командам.

PAINT = '''import tkinter as tk
from tkinter import colorchooser

root = tk.Tk()
root.title("Мой Paint")
canvas = tk.Canvas(root, width=640, height=480, bg="white", cursor="pencil")
canvas.pack(side="left", fill="both", expand=True)
pen = {"color": "black", "size": 4, "last": None}
strokes = []   # каждый штрих — список номеров линий на холсте: так работает отмена


def press(event):              # кнопку мыши нажали — начинается новый штрих
    pen["last"] = (event.x, event.y)
    strokes.append([])


def drag(event):               # мышь двигается с нажатой кнопкой — рисуем отрезок
    x0, y0 = pen["last"]
    item = canvas.create_line(x0, y0, event.x, event.y, fill=pen["color"],
                              width=pen["size"], capstyle="round")
    strokes[-1].append(item)
    pen["last"] = (event.x, event.y)


def undo(event=None):          # убрать последний штрих целиком
    if strokes:
        for item in strokes.pop():
            canvas.delete(item)


def pick_color():
    color = colorchooser.askcolor(pen["color"])[1]
    if color:
        pen["color"] = color


def clear():
    canvas.delete("all")
    strokes.clear()


panel = tk.Frame(root)
panel.pack(side="right", fill="y", padx=6)
for c in ["black", "red", "orange", "green", "blue", "white"]:   # white — ластик
    tk.Button(panel, bg=c, width=4, command=lambda c=c: pen.update(color=c)).pack(pady=2)
tk.Button(panel, text="Цвет…", command=pick_color).pack(pady=4)
size = tk.Scale(panel, from_=1, to=30, orient="horizontal", label="Кисть",
                command=lambda v: pen.update(size=int(v)))
size.set(4)
size.pack()
tk.Button(panel, text="Отменить", command=undo).pack(pady=4)
tk.Button(panel, text="Очистить", command=clear).pack()

canvas.bind("<Button-1>", press)
canvas.bind("<B1-Motion>", drag)
root.bind("<Control-z>", undo)
root.mainloop()'''

GRID = ('W, H = 12, 6\ncanvas = [["."] * W for _ in range(H)]\n\n\ndef dot(x, y, c):\n    if 0 <= x < W and 0 <= y < H:\n        canvas[y][x] = c\n\n\n'
        'def line(x1, y1, x2, y2, c):\n    n = max(abs(x2 - x1), abs(y2 - y1), 1)\n    for i in range(n + 1):\n'
        '        dot(x1 + round(i * (x2 - x1) / n), y1 + round(i * (y2 - y1) / n), c)\n\n\n'
        'def rect(x1, y1, x2, y2, c):\n    line(x1, y1, x2, y1, c)\n    line(x2, y1, x2, y2, c)\n    line(x2, y2, x1, y2, c)\n    line(x1, y2, x1, y1, c)\n')
FILL = ('def fill(x, y, c):\n    old = canvas[y][x]\n    if old == c:\n        return 0\n    canvas[y][x] = c\n    queue = deque([(x, y)])\n    count = 0\n'
        '    while queue:\n        x, y = queue.popleft()\n        count += 1\n        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):\n'
        '            if 0 <= nx < W and 0 <= ny < H and canvas[ny][nx] == old:\n                canvas[ny][nx] = c\n                queue.append((nx, ny))\n'
        '    return count\n')


def th_canvas():
    terms = [
        ('Canvas', 'Виджет tkinter «холст»: на нём рисуют линии, прямоугольники, овалы и текст (create_line, create_rectangle…). Каждая фигура '
                   'получает номер, по нему её можно удалить или подвинуть.'),
        ('bind', 'canvas.bind("<B1-Motion>", функция) — вызывать функцию на событие: нажатие кнопки мыши, движение с нажатой кнопкой, клавишу. '
                 'Функция получает event с координатами event.x и event.y.'),
        ('холст-сетка', 'Модель картинки в программе: список строк, в каждой — клетки (пиксели). canvas[y][x] — клетка в столбце x, строке y.'),
        ('отрезок по точкам', 'Как нарисовать линию из клеток: сделать n = max(|dx|, |dy|) шагов и на каждом округлить координаты. '
                              'Так рисуют линии и графические программы (быстрая версия — алгоритм Брезенхэма).'),
        ('стек отмены', 'Список прошлых состояний: перед каждым действием кладём снимок холста, «Отменить» достаёт последний. '
                        'Снятое кладут во второй стек — для «Повторить»; новое действие этот второй стек очищает.'),
    ]
    body = (
        '<p>Свой Paint — это окно с холстом, палитрой и кнопкой «Отменить». На компьютере его делают на tkinter: виджет [[Canvas]] умеет рисовать '
        'линии, а [[bind]] связывает движения мыши с функциями. Вот рабочая программа — скопируй её в файл paint.py на компьютере и запусти '
        '(в браузере окон нет):</p>'
        '<pre class="pc">' + esc(PAINT) + '</pre>'
        '<p>Мышь двигается с нажатой кнопкой — tkinter много раз в секунду вызывает drag, и каждый вызов дорисовывает короткий отрезок от прошлой '
        'точки до новой. Отрезки одного штриха собраны в список — так «Отменить» убирает штрих целиком. Ластик — просто белая кисть.</p>'
        '<h3>Холст изнутри</h3>'
        '<p>В графических редакторах картинка — сетка пикселей, а инструменты — функции, которые меняют клетки. Сделаем такую модель: '
        '[[холст-сетка]] из символов, точка — клетка, а линию строим как [[отрезок по точкам]]:</p>'
        + ex(GRID + '\n\nline(0, 0, 11, 5, "#")\nrect(7, 0, 11, 3, "o")\ndot(20, 20, "!")   # за краем — ничего не рисуем\nfor row in canvas:\n'
             '    print("".join(row))') +
        '<p>Точки за краем dot просто пропускает — как настоящий редактор, когда ведёшь мышью за окно. Прямоугольник — четыре линии.</p>'
        '<h3>Отмена и повтор</h3>'
        '<p>Самый простой способ отменять — [[стек отмены]]: перед каждым действием сохранить копию холста. Копия нужна глубокая — '
        '<code>[row[:] for row in canvas]</code>, иначе снимок будет меняться вместе с холстом:</p>'
        + ex(GRID + '\n\nundo, redo = [], []\n\n\ndef do(action, *args):\n    undo.append([row[:] for row in canvas])\n    redo.clear()\n    action(*args)\n\n\n'
             'do(line, 0, 2, 11, 2, "-")\ndo(dot, 5, 4, "*")\ncanvas = undo.pop()            # «Отменить»: точка пропала\nredo.append(canvas)\n'
             'print(len(undo), len(redo))\nfor row in canvas:\n    print("".join(row))') +
        '<p>Снимок всего холста — просто, но для большой картинки дорого. Настоящие редакторы хранят только изменения: какие клетки были до '
        'действия (как strokes в программе выше).</p>'
    )
    return th('Холст и инструменты', terms, body)


def fl_canvas():
    return fl('Холст и инструменты', [
        q('Что делает canvas.bind("<B1-Motion>", drag)?', 'Вызывает drag, пока мышь движется с нажатой кнопкой', ['Рисует линию сразу',
          'Запрещает рисовать мышью'], 'event.x, event.y — где сейчас мышь.'),
        qo('Что выведет программа?', 'x1, y1, x2, y2 = 0, 0, 4, 2\nn = max(abs(x2 - x1), abs(y2 - y1), 1)\nprint(n + 1)', ['3', '6', '4'],
           'Шагов — по большей разнице, точек на одну больше.'),
        q('Почему снимок холста — [row[:] for row in canvas], а не canvas[:]?', 'canvas[:] копирует только список строк, строки общие',
          ['canvas[:] не работает со списками', 'Так быстрее'], 'Внутренние списки надо копировать тоже.'),
        q('После «Отменить» нарисовали новую точку. Что со стеком «Повторить»?', 'Очищается', ['Остаётся как был', 'В него кладут точку'],
          'Повторять старое после нового действия бессмысленно.'),
    ])


def code_canvas():
    return ts('Холст и инструменты', [
        task('Рисунок по командам. Первая строка ввода — ширина и высота холста, дальше команды до конца ввода: «dot X Y C» — точка, «line X1 Y1 X2 Y2 C» — '
             'отрезок, «rect X1 Y1 X2 Y2 C» — рамка прямоугольника (углы могут быть в любом порядке). C — символ цвета. Отрезок — как в теории: '
             'n = max(|dx|, |dy|, 1) шагов, координаты округляются round. Что за краем — не рисуется. Пустой холст — точки «.». Выведи холст и '
             '«Закрашено клеток: N» (не «.»).',
             'Функции dot, line, rect — из теории. Первая строка — sys.stdin.readline(), команды — for text in sys.stdin: cmd, *args = text.split().',
             'import sys\n\nW, H = map(int, sys.stdin.readline().split())\n' + GRID.split('\n', 1)[1].replace('W, H = 12, 6\n', '') + '\n\n'
             'for text in sys.stdin:\n    cmd, *args = text.split()\n    nums = list(map(int, args[:-1]))\n    {"dot": dot, "line": line, "rect": rect}[cmd](*nums, args[-1])\n'
             'for row in canvas:\n    print("".join(row))\nprint(f"Закрашено клеток: {sum(ch != \'.\' for row in canvas for ch in row)}")',
             ['10 5\nline 0 0 9 4 #\nrect 6 0 9 2 o\ndot 0 4 @', '8 4\nrect 6 3 1 0 *\nline 2 1 5 2 -\ndot 9 9 x', '5 5\nline 4 0 0 4 /\nline 0 0 4 4 \\']),
        task('Отмена и повтор. Холст и команды dot и line — как в прошлой задаче, плюс «undo» и «redo». Перед каждым рисованием сохраняй снимок холста; '
             'undo возвращает прошлое состояние (а текущее кладёт в стек повтора), redo — наоборот; новое рисование очищает стек повтора. Если отменять '
             'или повторять нечего, выведи «Нечего отменять» или «Нечего повторять». В конце — холст и «Отмен: A, повторов: B» (сколько undo и redo '
             'сработало).',
             'Снимок: [row[:] for row in canvas]. undo: redo.append(снимок текущего); canvas = undo_stack.pop().\n'
             'Внутри функций canvas меняется по месту, а присваивание canvas = … делай на верхнем уровне программы.',
             'import sys\n\nW, H = map(int, sys.stdin.readline().split())\n' + GRID.split('\n', 1)[1].split('\n\n\ndef rect')[0] + '\n\n\n'
             'undo_stack, redo_stack = [], []\nundone = redone = 0\nfor text in sys.stdin:\n    cmd, *args = text.split()\n    if cmd == "undo":\n'
             '        if undo_stack:\n            redo_stack.append([row[:] for row in canvas])\n            canvas = undo_stack.pop()\n            undone += 1\n'
             '        else:\n            print("Нечего отменять")\n    elif cmd == "redo":\n        if redo_stack:\n'
             '            undo_stack.append([row[:] for row in canvas])\n            canvas = redo_stack.pop()\n            redone += 1\n        else:\n'
             '            print("Нечего повторять")\n    else:\n        undo_stack.append([row[:] for row in canvas])\n        redo_stack.clear()\n'
             '        {"dot": dot, "line": line}[cmd](*map(int, args[:-1]), args[-1])\nfor row in canvas:\n    print("".join(row))\n'
             'print(f"Отмен: {undone}, повторов: {redone}")',
             ['6 3\nline 0 1 5 1 -\ndot 2 0 *\nundo\nundo\nredo\ndot 5 2 #', '4 2\nundo\ndot 0 0 a\ndot 1 1 b\nundo\ndot 3 0 c\nredo', '3 3\nredo\nline 0 0 2 2 x\nundo\nredo\nredo']),
    ])


def th_fill():
    terms = [
        ('заливка', 'Инструмент «ведро»: перекрасить область — все клетки того же цвета, до которых можно дойти от начальной через соседей '
                    'слева, справа, сверху и снизу.'),
        ('обход в ширину', 'Обход «волной»: очередь клеток; берём клетку из начала очереди, а её подходящих соседей красим и ставим в конец. '
                           'По-английски BFS. Очередь — collections.deque.'),
        ('связная область', 'Клетки одного цвета, между которыми можно пройти по соседям. Заливка красит ровно одну связную область.'),
    ]
    body = (
        '<p>[[заливка]] — «ведро» в Paint: щёлкнули по клетке — перекрасилась вся область того же цвета. Как найти эту область? Красим начальную '
        'клетку, потом её соседей того же старого цвета, потом их соседей — пока есть кого красить. Это [[обход в ширину]]: клетки ждут в очереди, '
        'и закрашенная область расползается волной:</p>'
        + ex('from collections import deque\n\nPIC = ["........", ".####...", ".#..#...", ".####.##", "......#."]\nW, H = len(PIC[0]), len(PIC)\n'
             'canvas = [list(row) for row in PIC]\n\n\n' + FILL + '\n\nprint(fill(2, 2, "o"))\nprint(fill(0, 0, "~"))\nprint(fill(7, 4, "~"))\nfor row in canvas:\n'
             '    print("".join(row))') +
        '<p>Клетку красим сразу, как только ставим в очередь, — так она не попадёт в очередь дважды. Заливка внутри рамки не вытекла наружу: '
        'соседи — только по горизонтали и вертикали, а углы рамки сплошные. Ячейка (7, 4) — отдельная [[связная область]] из одной клетки: '
        'по диагонали заливка не проходит.</p>'
        '<p>Заливку можно написать и рекурсией: «покрась клетку и вызови себя для четырёх соседей». Это короче, но на холсте 1000 × 1000 '
        'рекурсия уйдёт на миллион вызовов вглубь — будет RecursionError. Очередь такой границы не имеет, поэтому редакторы используют её.</p>'
        '<h3>Подсчёт областей</h3>'
        '<p>Тем же обходом считают области: идём по всем клеткам, и каждая ещё не тронутая клетка нужного цвета начинает новую область — '
        'заливаем её «служебным» цветом, чтобы не посчитать дважды. Так в программах считают острова на карте, комнаты в лабиринте и пятна '
        'на снимке.</p>'
    )
    return th('Заливка', terms, body)


def fl_fill():
    return fl('Заливка', [
        q('Почему клетку красят сразу, когда ставят в очередь?', 'Чтобы она не попала в очередь дважды', ['Так красивее', 'Иначе deque не работает'],
          'Иначе соседи добавят её снова.'),
        q('Залили клетку цветом, который у неё уже есть. Что должно произойти?', 'Ничего: закрашено 0 клеток', ['Бесконечный цикл — это нормально',
          'Перекрасится весь холст'], 'Поэтому fill сразу проверяет old == c.'),
        q('Почему для большого холста заливку пишут очередью, а не рекурсией?', 'Глубокая рекурсия даёт RecursionError', ['Рекурсия красит неверно',
          'Очередь красит только край'], 'Очередь растёт в памяти, а не в глубину вызовов.'),
        q('Две клетки «#» касаются только углами. Одна это область или две?', 'Две: соседи — только сверху, снизу, слева, справа', ['Одна', 'Зависит от цвета'],
          'Так устроена обычная заливка в Paint.'),
    ])


def code_fill():
    return ts('Заливка', [
        task('Ведро. Первая строка ввода — число строк картинки H, дальше H строк одинаковой длины, последняя строка — «X Y C»: залить от клетки (X, Y) '
             'цветом C (соседи — по горизонтали и вертикали). Выведи картинку после заливки и «Закрашено: N». Если (X, Y) за краем — выведи '
             'картинку без изменений и «Мимо холста».',
             'Функция fill из теории (from collections import deque).',
             'from collections import deque\n\nH = int(input())\ncanvas = [list(input()) for _ in range(H)]\nW = len(canvas[0])\nx, y, c = input().split()\nx, y = int(x), int(y)\n\n\n'
             + FILL + '\n\nif 0 <= x < W and 0 <= y < H:\n    msg = f"Закрашено: {fill(x, y, c)}"\nelse:\n    msg = "Мимо холста"\nfor row in canvas:\n'
             '    print("".join(row))\nprint(msg)',
             ['5\n........\n.####...\n.#..#...\n.####.##\n......#.\n2 2 o', '5\n........\n.####...\n.#..#...\n.####.##\n......#.\n0 0 ~',
              '3\nab\nba\nab\n0 0 a', '2\n...\n...\n5 0 x']),
        task('Пятна. Первая строка — число строк картинки H, дальше H строк из «.» и «#». Посчитай связные области из «#» (соседи — по горизонтали и '
             'вертикали) и выведи «Пятен: N», «Самое большое: S» (клеток в наибольшем; 0, если пятен нет) и размеры всех пятен по убыванию через пробел '
             '(или «-»).',
             'Обходи все клетки; «#» — новое пятно: fill(x, y, "o") вернёт его размер и закрасит, чтобы не посчитать снова.',
             'from collections import deque\n\nH = int(input())\ncanvas = [list(input()) for _ in range(H)]\nW = len(canvas[0])\n\n\n' + FILL + '\n\n'
             'sizes = []\nfor y in range(H):\n    for x in range(W):\n        if canvas[y][x] == "#":\n            sizes.append(fill(x, y, "o"))\n'
             'sizes.sort(reverse=True)\nprint(f"Пятен: {len(sizes)}")\nprint(f"Самое большое: {sizes[0] if sizes else 0}")\n'
             'print(" ".join(map(str, sizes)) if sizes else "-")',
             ['4\n##..#\n#..##\n..#..\n##...', '3\n#.#\n.#.\n#.#', '2\n...\n...', '3\n####\n#..#\n####']),
    ])


def project():
    return pj('Paint по командам',
              'Консольный Paint. Первая строка ввода — ширина и высота холста, пустой холст — «.». Дальше команды до конца ввода:\n'
              '— «color C» — цвет кисти (сначала «#»);\n'
              '— «dot X Y», «line X1 Y1 X2 Y2», «rect X1 Y1 X2 Y2» — точка, отрезок (как в теории), рамка; «box X1 Y1 X2 Y2» — закрашенный '
              'прямоугольник (углы в любом порядке); за краем не рисуется;\n'
              '— «fill X Y» — заливка цветом кисти; за краем — вывести «Мимо холста»;\n'
              '— «clear» — очистить холст;\n'
              '— «undo» — отменить последнее рисование (dot, line, rect, box, fill или clear; color не отменяется), нечего — «Нечего отменять»;\n'
              '— что-то другое — «Не знаю команду X».\n'
              'Снимок для отмены делается перед каждой командой рисования, даже если она ничего не изменила (заливка «мимо» снимок не делает). '
              'В конце выведи холст и строку «Цвета: …» — сколько клеток каждого цвета, кроме «.», в виде «C×N» через пробел по убыванию N '
              '(при равенстве — по символу), или «Цвета: нет».',
              'Команды-рисования — словарь имя → функция; аргументы — map(int, args)\nbox — два цикла по строкам и столбцам между min и max углов\n'
              'Счёт цветов — словарь; сортировка: sorted(counts.items(), key=lambda p: (-p[1], p[0]))',
              'import sys\nfrom collections import deque\n\nW, H = map(int, sys.stdin.readline().split())\n' + GRID.split('\n', 1)[1] + '\n\n'
              'def box(x1, y1, x2, y2, c):\n    for y in range(min(y1, y2), max(y1, y2) + 1):\n        for x in range(min(x1, x2), max(x1, x2) + 1):\n            dot(x, y, c)\n\n\n'
              + FILL + '\n\nTOOLS = {"dot": dot, "line": line, "rect": rect, "box": box}\npen = "#"\nhistory = []\nfor text in sys.stdin:\n'
              '    cmd, *args = text.split()\n    if cmd == "color":\n        pen = args[0]\n    elif cmd in TOOLS:\n        history.append([row[:] for row in canvas])\n'
              '        TOOLS[cmd](*map(int, args), pen)\n    elif cmd == "fill":\n        x, y = map(int, args)\n        if 0 <= x < W and 0 <= y < H:\n'
              '            history.append([row[:] for row in canvas])\n            fill(x, y, pen)\n        else:\n            print("Мимо холста")\n'
              '    elif cmd == "clear":\n        history.append([row[:] for row in canvas])\n        canvas = [["."] * W for _ in range(H)]\n'
              '    elif cmd == "undo":\n        if history:\n            canvas = history.pop()\n        else:\n            print("Нечего отменять")\n'
              '    else:\n        print(f"Не знаю команду {cmd}")\nfor row in canvas:\n    print("".join(row))\ncounts = {}\nfor row in canvas:\n'
              '    for ch in row:\n        if ch != ".":\n            counts[ch] = counts.get(ch, 0) + 1\n'
              'pairs = sorted(counts.items(), key=lambda p: (-p[1], p[0]))\nprint("Цвета:", " ".join(f"{c}×{n}" for c, n in pairs) if pairs else "нет")',
              ['10 6\nrect 0 0 9 5\ncolor ~\nfill 4 3\ncolor @\ndot 4 3\nbox 7 1 8 2\nundo\nline 1 4 8 1\nspray 1 1',
               '6 4\nundo\ncolor *\nbox 0 0 5 3\nclear\nfill 9 9\nundo\ncolor o\nfill 2 2\ndot 0 0',
               '5 3\ncolor x\nline 0 0 4 2\nundo\nundo\nclear\nundo'])


def build():
    return topic('Свой Paint: программа рисования', 'холст, линии, отмена, заливка', [
        th_canvas(), fl_canvas(), code_canvas(),
        th_fill(), fl_fill(), code_fill(),
        project(),
    ], opt=True)
