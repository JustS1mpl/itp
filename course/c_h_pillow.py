from dsl import *

# Нора после «Модули»: картинки на Pillow (пакет Pyodide; dsl.py гонит такой код через Pyodide, PYO_RE). В приложении im.show()
# показывает картинку под выводом (glue.py, _itp_pil). Файлы задач — текстовые: картинки в формате PPM P3 (числа цветов текстом),
# Pillow открывает их как обычные. В задачах проверяется напечатанное: размеры, цвета пикселей, подсчёты. Файлов (open, with) на этом
# месте ещё нет — картинки открывает и сохраняет сам Pillow. Две теории: пиксели и цвета; размер, обрезка и рисование. Мини-проект — галерея.


def ppm(w, h, f):
    """картинка PPM P3: f(x, y) → (r, g, b)"""
    rows = [' '.join('%d %d %d' % f(x, y) for x in range(w)) for y in range(h)]
    return 'P3\n%d %d\n255\n' % (w, h) + '\n'.join(rows) + '\n'


def sunset(x, y):
    return (250 - y * 2, 120 + y, 60 + y * 2) if y < 40 else (30, 60 + x % 20, 120)


def cat(x, y):
    dx, dy = x - 20, y - 24
    if dx * dx + dy * dy < 150:
        return (240, 160, 40)
    return (200, 230, 255)


def boxes(x, y):
    return (220, 40, 60) if (x // 10 + y // 10) % 2 else (250, 250, 250)


def leaf(x, y):
    return (40 + y * 3, 160, 60) if abs(x - 15) < 15 - y // 3 else (255, 255, 240)


PHOTO = {'photo.ppm': ppm(60, 50, sunset)}
GALLERY = {'sunset.ppm': ppm(60, 50, sunset), 'cat.ppm': ppm(40, 48, cat), 'boxes.ppm': ppm(30, 30, boxes), 'leaf.ppm': ppm(30, 45, leaf)}


def th_pixels():
    terms = [
        ('Pillow', 'Библиотека для работы с картинками: открыть, создать, изменить, сохранить. Ставится pip install pillow, а подключается '
                   'под старым именем PIL: from PIL import Image. В ИТП подгружается сама.'),
        ('PIL', 'Имя пакета Pillow в import: from PIL import Image, ImageDraw.'),
        ('Image', 'Модуль Pillow с классом картинки. Image.new — создать, Image.open — открыть файл.'),
        ('пиксель', 'Точка картинки. Цвет пикселя в режиме RGB — три числа от 0 до 255: (красный, зелёный, синий). (0, 0, 0) — чёрный, '
                    '(255, 255, 255) — белый. Координаты (x, y) считают от левого верхнего угла: x вправо, y вниз.'),
        ('Image.new', 'Image.new("RGB", (ширина, высота), цвет) — новая картинка, залитая цветом (кортеж или имя: "white", "red"). '
                      'Размер картинки: im.size — кортеж, im.width и im.height — отдельно.'),
        ('getpixel', 'im.getpixel((x, y)) — цвет пикселя кортежем (r, g, b). Координаты — одним кортежем, отсюда двойные скобки.'),
        ('putpixel', 'im.putpixel((x, y), (r, g, b)) — покрасить один пиксель.'),
        ('show', 'im.show() — показать картинку. На компьютере откроется окно просмотра, в ИТП картинка появится под выводом программы.'),
        ('resize', 'im.resize((ширина, высота)) — новая картинка другого размера. resample=Image.NEAREST увеличивает без размытия — для пиксель-арта.'),
    ]
    body = (
        '<p>Картинка — это таблица [[пиксель|пикселей]], а пиксель — три числа: сколько в нём красного, зелёного и синего. Работают с картинками через '
        'библиотеку [[Pillow]]; в коде она называется [[PIL]], а главный модуль в ней — [[Image]]. Создадим картинку 8 × 6 через [[Image.new]] '
        'и порисуем по пикселю:</p>'
        + ex('from PIL import Image\n\nim = Image.new("RGB", (8, 6), "white")\nfor i in range(6):\n    im.putpixel((i, i), (255, 0, 0))\n'
             'im.putpixel((7, 0), (0, 0, 255))\nprint(im.size, im.mode)\nprint(im.getpixel((2, 2)), im.getpixel((7, 0)), im.getpixel((0, 5)))\n'
             'im = im.resize((80, 60), resample=Image.NEAREST)\nim.show()\nprint("теперь:", im.size)') +
        '<p>[[putpixel]] красит пиксель, [[getpixel]] читает цвет. <code>im.size</code> — кортеж (ширина, высота), <code>im.mode</code> — режим: '
        'RGB — цветная, L — оттенки серого. Картинка 8 × 6 крошечная, поэтому её увеличили [[resize]]: каждый пиксель стал квадратом 10 × 10. '
        '[[show]] показывает результат — скопируй пример в раздел «Код» и запусти, чтобы увидеть.</p>'
        '<h3>Пиксель-арт из текста</h3>'
        '<p>Рисовать по пикселю вручную долго. Удобнее нарисовать картинку символами и раскрасить по словарю-палитре:</p>'
        + ex('from PIL import Image\n\nART = ["..rr.rr..", ".rrrrrrr.", ".rrrrrrr.", "..rrrrr..", "...rrr...", "....r...."]\n'
             'PALETTE = {".": (255, 255, 255), "r": (230, 40, 70)}\nim = Image.new("RGB", (len(ART[0]), len(ART)))\nfor y, row in enumerate(ART):\n'
             '    for x, ch in enumerate(row):\n        im.putpixel((x, y), PALETTE[ch])\nim.resize((im.width * 12, im.height * 12), resample=Image.NEAREST).show()\n'
             'print("красных пикселей:", sum(row.count("r") for row in ART))') +
        '<h3>Фильтры — это формулы</h3>'
        '<p>Любой фильтр в редакторе фото — формула для каждого пикселя. Негатив: каждое число заменить на 255 минус оно. Оттенки серого: '
        'яркость ≈ 0,299·R + 0,587·G + 0,114·B (глаз сильнее всего чувствует зелёный). Цикл по всем пикселям — два вложенных цикла по x и y:</p>'
        + ex('from PIL import Image\n\nim = Image.new("RGB", (3, 2), (200, 100, 50))\nim.putpixel((0, 0), (0, 0, 0))\nw, h = im.size\n'
             'for y in range(h):\n    for x in range(w):\n        r, g, b = im.getpixel((x, y))\n        im.putpixel((x, y), (255 - r, 255 - g, 255 - b))\n'
             'print(im.getpixel((0, 0)), im.getpixel((2, 1)))\nr, g, b = 200, 100, 50\nprint("яркость:", round(0.299 * r + 0.587 * g + 0.114 * b))') +
        '<p>Так работает любой фильтр: яркость, контраст, сепия, «пикселизация» — меняется только формула.</p>'
    )
    return th('Пиксели и цвета', terms, body)


def fl_pixels():
    return fl('Пиксели и цвета', [
        q('Какой цвет у пикселя (0, 0, 0)?', 'Чёрный', ['Белый', 'Прозрачный'], 'Все три канала выключены.'),
        q('Где пиксель с координатами (0, 0)?', 'В левом верхнем углу', ['В левом нижнем углу', 'В центре'], 'y растёт вниз.'),
        q('Почему пишут im.getpixel((x, y)) с двойными скобками?', 'Координаты передаются одним кортежем', ['Так быстрее', 'Иначе вернётся серый'],
          'Внутренние скобки — кортеж (x, y).'),
        q('Пиксель (20, 100, 250). Каким он станет в негативе?', '(235, 155, 5)', ['(20, 100, 250)', '(250, 100, 20)'], 'Каждое число — 255 минус оно.'),
        q('Зачем resample=Image.NEAREST при увеличении пиксель-арта?', 'Чтобы края пикселей остались чёткими', ['Чтобы картинка стала меньше',
          'Без него resize не работает'], 'Обычное увеличение сглаживает и размывает.'),
    ])


def code_pixels():
    return ts('Пиксели и цвета', [
        task('Пиксель-арт. Первая строка ввода — число строк рисунка N, дальше N строк одинаковой длины из символов палитры: «.» — белый (255, 255, 255), '
             '«k» — чёрный (0, 0, 0), «r» — красный (230, 40, 70), «g» — зелёный (60, 180, 75), «y» — жёлтый (255, 220, 0). Собери картинку через '
             'putpixel, увеличь в 10 раз без размытия и покажи. Выведи «Размер: Ш×В» увеличенной картинки (знак ×, не буква x), «Цветных пикселей: K» (всё, кроме белых, '
             'в исходном рисунке) и «Больше всего: БУКВА» — самый частый цветной символ (при равенстве — первый по алфавиту).',
             'Счётчик символов — словарь; самый частый: max(sorted(counts), key=counts.get).',
             'from PIL import Image\n\nPALETTE = {".": (255, 255, 255), "k": (0, 0, 0), "r": (230, 40, 70), "g": (60, 180, 75), "y": (255, 220, 0)}\nn = int(input())\n'
             'art = [input() for _ in range(n)]\nim = Image.new("RGB", (len(art[0]), n))\ncounts = {}\nfor y, row in enumerate(art):\n    for x, ch in enumerate(row):\n'
             '        im.putpixel((x, y), PALETTE[ch])\n        if ch != ".":\n            counts[ch] = counts.get(ch, 0) + 1\n'
             'big = im.resize((im.width * 10, im.height * 10), resample=Image.NEAREST)\nbig.show()\nprint(f"Размер: {big.width}×{big.height}")\n'
             'print(f"Цветных пикселей: {sum(counts.values())}")\nprint(f"Больше всего: {max(sorted(counts), key=counts.get)}")',
             ['4\n.gg.\ngrrg\ngrrg\n.kk.', '3\nyyyyy\ny.k.y\nyyyyy', '2\nrg\ngr']),
        task('Фильтры. На вход подаётся цвет «R G B» и название фильтра: negative, gray или sepia. Создай картинку 4 × 4 этого цвета, примени фильтр '
             'к каждому пикселю через getpixel/putpixel и выведи цвет пикселя (3, 3) после фильтра. Негатив — 255 минус канал. Серый — '
             'яркость Y = round(0.299·R + 0.587·G + 0.114·B) во все три канала. Сепия: R′ = 0.393R + 0.769G + 0.189B, G′ = 0.349R + 0.686G + 0.168B, '
             'B′ = 0.272R + 0.534G + 0.131B — каждое округлить round и ограничить сверху 255.',
             'Фильтр — функция цвет → цвет; в цикле: im.putpixel((x, y), f(im.getpixel((x, y)))).',
             'from PIL import Image\n\n\ndef negative(c):\n    r, g, b = c\n    return (255 - r, 255 - g, 255 - b)\n\n\ndef gray(c):\n    r, g, b = c\n'
             '    y = round(0.299 * r + 0.587 * g + 0.114 * b)\n    return (y, y, y)\n\n\ndef sepia(c):\n    r, g, b = c\n'
             '    return (min(255, round(0.393 * r + 0.769 * g + 0.189 * b)), min(255, round(0.349 * r + 0.686 * g + 0.168 * b)),\n'
             '            min(255, round(0.272 * r + 0.534 * g + 0.131 * b)))\n\n\nFILTERS = {"negative": negative, "gray": gray, "sepia": sepia}\n'
             'r, g, b = map(int, input().split())\nf = FILTERS[input()]\nim = Image.new("RGB", (4, 4), (r, g, b))\nfor y in range(4):\n    for x in range(4):\n'
             '        im.putpixel((x, y), f(im.getpixel((x, y))))\nprint(im.getpixel((3, 3)))',
             ['10 200 30\nnegative', '200 100 50\ngray', '200 100 50\nsepia', '255 255 255\nsepia']),
        task('Шахматка. На вход подаются размер доски N ≥ 2 (клеток) и размер клетки S в пикселях. Нарисуй доску N × N клеток: клетка (0, 0) — светлая '
             '(240, 217, 181), соседние чередуются с тёмной (181, 136, 99). Покажи её и выведи «Размер: Ш×В», цвет пикселя (S, 0) и сколько тёмных пикселей.',
             'Клетка пикселя (x, y) — (x // S, y // S); тёмная, если сумма номеров клеток нечётная.',
             'from PIL import Image\n\nLIGHT, DARK = (240, 217, 181), (181, 136, 99)\nn, s = map(int, input().split())\nim = Image.new("RGB", (n * s, n * s), LIGHT)\n'
             'dark = 0\nfor y in range(n * s):\n    for x in range(n * s):\n        if (x // s + y // s) % 2:\n            im.putpixel((x, y), DARK)\n            dark += 1\n'
             'im.show()\nprint(f"Размер: {im.width}×{im.height}")\nprint(im.getpixel((s, 0)))\nprint(f"Тёмных пикселей: {dark}")',
             ['8 10', '3 4', '2 5']),
    ])


def th_edit():
    terms = [
        ('Image.open', 'Image.open("файл") — открыть картинку из файла (png, jpg, gif, ppm…). Формат Pillow узнаёт сам.'),
        ('save', 'im.save("имя.png") — сохранить картинку; формат — по расширению.'),
        ('crop', 'im.crop((слева, сверху, справа, снизу)) — вырезать прямоугольник. Правая и нижняя границы не входят, как в срезах.'),
        ('rotate', 'im.rotate(угол, expand=True) — повернуть против часовой стрелки; expand=True расширяет холст, чтобы ничего не обрезалось.'),
        ('thumbnail', 'im.thumbnail((макс_ширина, макс_высота)) — уменьшить, сохраняя пропорции. Меняет саму картинку и ничего не возвращает.'),
        ('paste', 'холст.paste(картинка, (x, y)) — вклеить картинку левым верхним углом в точку (x, y).'),
        ('ImageDraw', 'Модуль Pillow для рисования фигур и текста: d = ImageDraw.Draw(im), потом d.rectangle, d.ellipse, d.text.'),
        ('ImageDraw.Draw', 'ImageDraw.Draw(im) — «кисть» для картинки im: всё нарисованное ею сразу попадает на im.'),
        ('rectangle', 'd.rectangle((x1, y1, x2, y2), fill=цвет, outline=цвет, width=толщина) — прямоугольник; обе границы входят.'),
        ('ellipse', 'd.ellipse((x1, y1, x2, y2), fill=цвет) — эллипс, вписанный в прямоугольник.'),
        ('text', 'd.text((x, y), "текст", fill=цвет) — надпись встроенным шрифтом. Встроенный шрифт может не знать кириллицу — для русского текста подключают свой: ImageFont.truetype("шрифт.ttf", размер).'),
    ]
    body = (
        '<p>Обычно картинку не рисуют с нуля, а открывают — [[Image.open]] — и сохраняют результат — [[save]]. Рядом с программой лежит '
        'фото photo.ppm (PPM — простой формат, который Pillow открывает так же, как png или jpg):</p>'
        + ex('from PIL import Image\n\nim = Image.open("photo.ppm")\nprint(im.format, im.size)\nsquare = im.crop((5, 0, 55, 50))\nprint("обрезали:", square.size)\n'
             'small = square.resize((25, 25))\nturned = im.rotate(90, expand=True)\nprint("уменьшили:", small.size, "повернули:", turned.size)\n'
             'small.save("avatar.png")\nprint(Image.open("avatar.png").size)', files=PHOTO) +
        '<p>[[crop]] берёт прямоугольник по четырём границам: левая и верхняя входят, правая и нижняя — нет, как в срезах. [[rotate]] поворачивает '
        'против часовой стрелки. Эти методы возвращают новую картинку, а исходная не меняется. А [[thumbnail]], как putpixel и рисование, меняет саму картинку: '
        'уменьшает её, сохраняя пропорции, и ничего не возвращает (а маленькую не увеличивает):</p>'
        + ex('from PIL import Image\n\nim = Image.open("photo.ppm")\nim.thumbnail((30, 30))\nprint(im.size)\ncanvas = Image.new("RGB", (70, 40), "white")\n'
             'canvas.paste(im, (2, 2))\ncanvas.paste(im, (36, 2))\nprint(canvas.getpixel((1, 1)), canvas.getpixel((2, 2)) == im.getpixel((0, 0)))', files=PHOTO) +
        '<p>60 × 50 вписали в 30 × 30 — вышло 30 × 25: пропорции сохранились. [[paste]] вклеивает картинку в другую — так собирают коллажи и галереи.</p>'
        '<h3>Рисование и подписи</h3>'
        '<p>Фигуры и текст рисует модуль [[ImageDraw]]: [[ImageDraw.Draw]] даёт «кисть» для картинки, и всё нарисованное сразу оказывается на ней:</p>'
        + ex('from PIL import Image, ImageDraw\n\nim = Image.new("RGB", (120, 60), (30, 30, 40))\nd = ImageDraw.Draw(im)\n'
             'd.rectangle((0, 0, 119, 59), outline=(120, 220, 90), width=3)\nd.ellipse((10, 15, 40, 45), fill=(255, 200, 0))\n'
             'd.text((50, 25), "ITP", fill="white")\nim.show()\nprint(im.getpixel((1, 1)), im.getpixel((25, 30)), im.getpixel((60, 5)))') +
        '<p>[[rectangle]] и [[ellipse]] задаются прямоугольником (x1, y1, x2, y2), и обе границы входят в фигуру. Надпись делает [[text]] — '
        'встроенным шрифтом; для красивого текста на компьютере подключают свой шрифт через ImageFont. Так делают водяные знаки, мемы и '
        'открытки.</p>'
    )
    return th('Размер, обрезка и рисование', terms, body)


def fl_edit():
    return fl('Размер, обрезка и рисование', [
        qo('Что выведет программа?', 'from PIL import Image\n\nim = Image.new("RGB", (100, 80))\nprint(im.crop((10, 20, 50, 30)).size)',
           ['(40, 10)', '(50, 30)', '(41, 11)'], 'Ширина 50 − 10, высота 30 − 20.'),
        q('Картинку 200 × 100 уменьшили thumbnail((50, 50)). Какой стал размер?', '(50, 25)', ['(50, 50)', '(25, 50)'],
          'Пропорции сохраняются: вписываем в 50 × 50.'),
        q('Что вернёт im.thumbnail((64, 64))?', 'None — он меняет саму im', ['Новую картинку 64 × 64', 'Размер картинки'],
          'Поэтому пишут просто im.thumbnail(…) без присваивания.'),
        q('Картинку 30 × 20 повернули rotate(90, expand=True). Какой размер?', '(20, 30)', ['(30, 20)', '(30, 30)'],
          'expand расширяет холст под повёрнутую картинку.'),
        q('Как вклеить logo в левый верхний угол картинки im?', 'im.paste(logo, (0, 0))', ['logo.paste(im, (0, 0))', 'im.crop(logo)'],
          'paste вызывают у холста, куда вклеивают.'),
    ])


def code_edit():
    return ts('Размер, обрезка и рисование', [
        task('Аватарка. Рядом с программой лежит своя photo.ppm (не та, что в теории). На вход подаётся размер аватарки N. Вырежи из фото квадрат максимального размера по '
             'центру (по длинной стороне поровну отрезать с двух сторон; если отрезается нечётное число пикселей, лишний — справа или снизу), '
             'уменьши до N × N, покажи и сохрани в avatar.png. Выведи «Фото: Ш×В», «Квадрат: (L, T, R, B)» — рамку обрезки — и «Аватарка: N×N» по '
             'размеру сохранённого файла.',
             'Сторона квадрата — min(w, h); отступ слева — (w − сторона) // 2.',
             'from PIL import Image\n\nn = int(input())\nim = Image.open("photo.ppm")\nw, h = im.size\nside = min(w, h)\nleft, top = (w - side) // 2, (h - side) // 2\n'
             'box = (left, top, left + side, top + side)\navatar = im.crop(box).resize((n, n))\navatar.show()\navatar.save("avatar.png")\n'
             'saved = Image.open("avatar.png")\nprint(f"Фото: {w}×{h}")\nprint(f"Квадрат: {box}")\nprint(f"Аватарка: {saved.width}×{saved.height}")',
             ['32', '50', '7'], files={'photo.ppm': ppm(60, 45, sunset)}),
        task('Открытка. На вход подаются ширина, высота и толщина рамки T, затем надпись латиницей. Создай картинку цвета (30, 30, 40), нарисуй рамку цветом '
             '(255, 200, 0) толщиной T по самому краю (rectangle с outline и width), в центре — жёлтый круг (255, 220, 0) радиусом 10, '
             'вписанный в квадрат от (cx − 10, cy − 10) до (cx + 10, cy + 10), где cx, cy — середина (целочисленным делением), а надпись — белым '
             'в точке (T + 4, T + 4). Покажи открытку и выведи цвета пикселей (0, 0), (T, T) и (cx, cy).',
             'd.rectangle((0, 0, w − 1, h − 1), outline=…, width=T) — рамка шириной T внутрь от края.',
             'from PIL import Image, ImageDraw\n\nw, h, t = map(int, input().split())\ntext = input()\nim = Image.new("RGB", (w, h), (30, 30, 40))\n'
             'd = ImageDraw.Draw(im)\nd.rectangle((0, 0, w - 1, h - 1), outline=(255, 200, 0), width=t)\ncx, cy = w // 2, h // 2\n'
             'd.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), fill=(255, 220, 0))\nd.text((t + 4, t + 4), text, fill="white")\nim.show()\n'
             'print(im.getpixel((0, 0)), im.getpixel((t, t)), im.getpixel((cx, cy)))',
             ['160 90 3\nHappy birthday!', '100 100 1\nGG'], files=None),
        task('Спрайт-лист. В играх кадры анимации хранят одной картинкой. На вход подаются ширина кадра W, высота H и число кадров K. Создай белый '
             'лист K кадров в ряд; в кадре i нарисуй красный (230, 40, 70) квадрат 4 × 4 с левым верхним углом в (i·2, H − 4) внутри кадра — '
             '«прыгающий» вправо мячик. Затем вырежи кадры обратно через crop и для каждого выведи «Кадр i: (x, y)» — координаты первого красного '
             'пикселя в кадре (обход строками сверху, внутри строки слева направо).',
             'Кадр i на листе начинается с x = i·W. Вырезанный кадр — sheet.crop((i * W, 0, (i + 1) * W, H)).',
             'from PIL import Image, ImageDraw\n\nRED = (230, 40, 70)\nw, h, k = map(int, input().split())\nsheet = Image.new("RGB", (w * k, h), "white")\n'
             'd = ImageDraw.Draw(sheet)\nfor i in range(k):\n    x0 = i * w + i * 2\n    d.rectangle((x0, h - 4, x0 + 3, h - 1), fill=RED)\nsheet.show()\n'
             'for i in range(k):\n    frame = sheet.crop((i * w, 0, (i + 1) * w, h))\n    found = None\n    for y in range(h):\n        for x in range(w):\n'
             '            if found is None and frame.getpixel((x, y)) == RED:\n                found = (x, y)\n    print(f"Кадр {i}: {found}")',
             ['16 10 4', '12 6 3']),
    ])


def project():
    return pj('Мини-галерея',
              'Рядом с программой лежат картинки sunset.ppm, cat.ppm, boxes.ppm и leaf.ppm. Первая строка ввода — имена файлов через пробел (в этом '
              'порядке они встанут в галерею), вторая — размер превью T и число столбцов C. Сделай галерею:\n'
              '— каждую картинку уменьши thumbnail((T, T)) с сохранением пропорций;\n'
              '— галерея — белый холст из ячеек T × T с отступом 4 пикселя между ячейками и по краям: ширина 4 + C·(T + 4), высота — так же по числу '
              'строк (последняя строка может быть неполной);\n'
              '— превью вклеивается в свою ячейку по центру (отступ внутри ячейки — (T − ширина) // 2 и (T − высота) // 2);\n'
              '— под галерею ничего не подписывай, просто покажи её и сохрани в gallery.png.\n'
              'Выведи по строке на картинку «ИМЯ: Ш×В → ш×в», затем «Галерея: Ш×В» по размеру сохранённого файла и цвет пикселя галереи (4 + T // 2, 4 + T // 2) — '
              'центра первой ячейки. Маленькую картинку thumbnail не увеличивает — она остаётся как есть.',
              'Строк — (n + C − 1) // C; ячейка номер i — столбец i % C, строка i // C\n'
              'Левый верхний угол ячейки — (4 + столбец·(T + 4), 4 + строка·(T + 4))\nthumbnail меняет саму картинку: размер «до» запомни заранее\nМаленькую картинку thumbnail не увеличивает — она остаётся как есть',
              'from PIL import Image\n\nnames = input().split()\nt, cols = map(int, input().split())\nrows = (len(names) + cols - 1) // cols\n'
              'gallery = Image.new("RGB", (4 + cols * (t + 4), 4 + rows * (t + 4)), "white")\nfor i, name in enumerate(names):\n    im = Image.open(name)\n'
              '    before = im.size\n    im.thumbnail((t, t))\n    x = 4 + (i % cols) * (t + 4) + (t - im.width) // 2\n    y = 4 + (i // cols) * (t + 4) + (t - im.height) // 2\n'
              '    gallery.paste(im, (x, y))\n    print(f"{name}: {before[0]}×{before[1]} → {im.width}×{im.height}")\ngallery.show()\ngallery.save("gallery.png")\n'
              'saved = Image.open("gallery.png")\nprint(f"Галерея: {saved.width}×{saved.height}")\nprint(saved.getpixel((4 + t // 2, 4 + t // 2)))',
              ['sunset.ppm cat.ppm boxes.ppm leaf.ppm\n24 3', 'leaf.ppm boxes.ppm\n40 1', 'cat.ppm sunset.ppm boxes.ppm\n16 3'], files=GALLERY)


def build():
    return topic('Pillow: обработка картинок', 'пиксели, фильтры, обрезка, рисование', [
        th_pixels(), fl_pixels(), code_pixels(),
        th_edit(), fl_edit(), code_edit(),
        project(),
    ], opt=True)
