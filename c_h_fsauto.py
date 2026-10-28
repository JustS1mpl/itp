from dsl import *

# Нора после «Файлы и форматы данных»: автоматизация работы с папками на виртуальной файловой системе приложения.
# Две теории: обход папок (iterdir, rglob, is_file/is_dir, name/stem/suffix, stat); копирование, перенос, удаление
# (mkdir, rename, shutil.copy/move/rmtree, unlink). Мини-проект — разобрать папку «Загрузки».
# Порядок файлов в папке зависит от системы, поэтому везде sorted; пути печатаем через as_posix() (на Windows иначе «\»).

PROJ = {'проект/main.py': 'print("привет")\n', 'проект/readme.md': '# Игра\nЗапуск: python main.py\n', 'проект/данные/уровни.json': '[1, 2, 3]\n',
        'проект/данные/рекорды.csv': 'ник,очки\nzed,1200\n', 'проект/картинки/герой.png': 'PNG-данные', 'проект/картинки/фон.png': 'PNG-данные-фона'}
PHOTOS = {'фото/IMG_0412.jpg': 'a', 'фото/IMG_0398.jpg': 'b', 'фото/IMG_0450.jpg': 'c', 'фото/заметка.txt': 'не фото'}
NOTES = {'заметки/алгебра.txt': '№112', 'заметки/физика.txt': 'стр. 40', 'заметки/план.md': '- поесть', 'архив/физика.txt': 'старое'}
DOWNLOADS = {'Загрузки/отпуск.jpg': '1', 'Загрузки/скрин.png': '2', 'Загрузки/доклад.docx': '3', 'Загрузки/билет.pdf': '4', 'Загрузки/песня.mp3': '5',
             'Загрузки/игра.zip': '6', 'Загрузки/список.txt': '7', 'Загрузки/setup.exe': '8', 'Загрузки/мем.gif': '9'}


def th_walk():
    terms = [
        ('iterdir', 'путь.iterdir() — всё, что лежит прямо в папке (файлы и папки) — объектами Path. Порядок не гарантирован: сортируй.'),
        ('rglob', 'путь.rglob("шаблон") — все файлы и папки на любой глубине, подходящие под шаблон: "*" — всё, "*.txt" — текстовые.'),
        ('glob', 'путь.glob("шаблон") — то же, что rglob, но только прямо в этой папке, без вложенных.'),
        ('is_file', 'путь.is_file() — True, если это файл; is_dir() — если папка.'),
        ('is_dir', 'путь.is_dir() — True, если это папка.'),
        ('stat', 'путь.stat() — сведения о файле; .st_size — размер в байтах.'),
        ('relative_to', 'путь.relative_to(папка) — тот же путь, но относительно папки: Path("проект/данные/a.csv").relative_to("проект") → данные/a.csv.'),
        ('as_posix', 'путь.as_posix() — путь строкой с прямыми косыми «/» — одинаково на Windows, macOS и Linux.'),
    ]
    body = (
        '<p>Разбирать скачанное, переименовывать сотни фотографий, делать резервные копии — скучная работа, которую легко отдать программе. '
        'В приложении у программы своя виртуальная папка: файлы задачи лежат в ней, а всё, что программа создаст или удалит, исчезает '
        'после запуска. На компьютере тот же код работает с настоящими папками — поэтому сначала его проверяют на копии.</p>'
        '<p>Папку перебирает [[iterdir]], а всё на любой глубине — [[rglob]]. [[is_file]] и [[is_dir]] отличают файлы от папок, а у пути '
        'есть части: <code>name</code> — имя целиком, <code>stem</code> — без расширения, <code>suffix</code> — расширение с точкой:</p>'
        + ex('from pathlib import Path\n\nroot = Path("проект")\nfor p in sorted(root.iterdir()):\n    print(p.name, "папка" if p.is_dir() else "файл")\n'
             'for p in sorted(root.rglob("*.png")):\n    print(p.relative_to(root).as_posix(), p.stem, p.suffix)', files=PROJ) +
        '<p>Порядок, в котором система отдаёт файлы, не гарантирован, поэтому список сортируют. <code>relative_to</code> делает путь '
        'относительным, а [[as_posix]] печатает его с прямыми косыми — одинаково на любой системе.</p>'
        '<h3>Размеры</h3>'
        '<p>[[stat]] даёт сведения о файле, размер в байтах — <code>st_size</code>. [[glob]] — как rglob, но без вложенных папок:</p>'
        + ex('from pathlib import Path\n\ntotal = 0\nfor p in sorted(Path("проект").rglob("*")):\n    if p.is_file():\n        total += p.stat().st_size\n'
             'print("Всего байт:", total)\nprint([p.name for p in sorted(Path("проект").glob("*.*"))])', files=PROJ) +
        '<p>Русская буква в UTF-8 занимает 2 байта, латинская — 1, поэтому размер в байтах не равен числу символов.</p>'
    )
    return th('Обход папок', terms, body)


def fl_walk():
    return fl('Обход папок', [
        qo('Что выведет программа?', 'from pathlib import Path\np = Path("фото/отпуск.2026.jpg")\nprint(p.stem, p.suffix)',
           ['отпуск .2026.jpg', 'отпуск.2026.jpg .jpg', 'фото/отпуск.2026 jpg'], 'suffix — последнее расширение, stem — имя без него.'),
        q('Почему список из iterdir сортируют?', 'Порядок файлов зависит от системы и не гарантирован', ['iterdir возвращает файлы задом наперёд', 'Без sorted нельзя пройти циклом'],
          'Отсортированный список одинаков везде.'),
        q('Чем rglob("*.txt") отличается от glob("*.txt")?', 'rglob ищет и во вложенных папках', ['rglob ищет только папки', 'Ничем'], 'r — recursive, «рекурсивно».'),
    ])


def code_walk():
    return ts('Обход папок', [
        task('Рядом с программой лежит папка «проект». Выведи все файлы в ней на любой глубине, по алфавиту путей, строками «путь — N байт», где '
             'путь — относительно папки «проект» с прямыми косыми. Последней строкой — «Файлов: K, всего N байт».',
             'for p in sorted(root.rglob("*")): if p.is_file(): ...\nПуть: p.relative_to(root).as_posix(), размер: p.stat().st_size.',
             'from pathlib import Path\n\nroot = Path("проект")\ncount = total = 0\nfor p in sorted(root.rglob("*")):\n    if p.is_file():\n        size = p.stat().st_size\n'
             '        print(f"{p.relative_to(root).as_posix()} — {size} байт")\n        count += 1\n        total += size\nprint(f"Файлов: {count}, всего {total} байт")',
             [''], files=PROJ),
        task('Что занимает место. Рядом лежит папка «проект». Сгруппируй все файлы на любой глубине по расширению и выведи строками '
             '«.РАСШИРЕНИЕ: файлов K, N байт» по убыванию байт (при равенстве — по расширению).',
             'Словари count[p.suffix] и size[p.suffix]. Сортировка пар: key=lambda s: (-size[s], s).',
             'from pathlib import Path\n\ncount = {}\nsize = {}\nfor p in Path("проект").rglob("*"):\n    if p.is_file():\n        count[p.suffix] = count.get(p.suffix, 0) + 1\n'
             '        size[p.suffix] = size.get(p.suffix, 0) + p.stat().st_size\nfor s in sorted(size, key=lambda s: (-size[s], s)):\n    print(f"{s}: файлов {count[s]}, {size[s]} байт")',
             [''], files=PROJ),
    ])


def th_move():
    terms = [
        ('mkdir', 'путь.mkdir(parents=True, exist_ok=True) — создать папку вместе с недостающими родителями; если она есть — не ошибка.'),
        ('rename', 'путь.rename(новый_путь) — переименовать или перенести файл; возвращает новый путь.'),
        ('unlink', 'путь.unlink() — удалить файл. Без корзины: удалённое не вернуть.'),
        ('shutil', 'Модуль для операций с файлами целиком: copy — копировать, move — перенести, rmtree — удалить папку со всем содержимым.'),
        ('copy', 'shutil.copy(откуда, куда) — копировать файл; «куда» может быть папкой — тогда имя сохранится.'),
        ('move', 'shutil.move(откуда, куда) — перенести файл или папку.'),
        ('rmtree', 'shutil.rmtree(папка) — удалить папку со всем содержимым. Опасно: проверяй путь дважды.'),
        ('with_name', 'путь.with_name(имя) — путь в той же папке, но с другим именем файла.'),
    ]
    body = (
        '<p>Папку создаёт [[mkdir]]: с <code>parents=True</code> — вместе с недостающими родителями, с <code>exist_ok=True</code> — без ошибки, '
        'если она уже есть. Файл переименовывает или переносит [[rename]], удаляет — [[unlink]]. Для операций целиком есть модуль [[shutil]]: '
        '[[copy]], [[move]] и [[rmtree]]:</p>'
        + ex('import shutil\nfrom pathlib import Path\n\nPath("копия/тексты").mkdir(parents=True, exist_ok=True)\nshutil.copy("проект/readme.md", "копия/тексты")\n'
             'Path("копия/тексты/readme.md").rename("копия/тексты/ПРОЧТИ.md")\nshutil.move("копия/тексты", "копия/документы")\n'
             'print([p.relative_to("копия").as_posix() for p in sorted(Path("копия").rglob("*"))])\nshutil.rmtree("копия")\nprint(Path("копия").exists())', files=PROJ) +
        '<h3>Осторожно: без корзины</h3>'
        '<p>unlink и rmtree удаляют сразу и навсегда, rename и move молча заменяют файл, если такое имя уже есть. Поэтому автоматизацию '
        'пишут осторожно: сначала печатают план («что куда переедет»), проверяют его, и только потом делают. Перед переносом '
        'проверяют, свободно ли имя, через <code>exists()</code>.</p>'
        + ex('from pathlib import Path\n\nfor p in sorted(Path("проект").rglob("*.png")):\n    target = p.with_name("old_" + p.name)\n'
             '    print(p.name, "→", target.name, "(занято)" if target.exists() else "")', files=PROJ) +
        '<p>[[with_name]] даёт путь с тем же местом, но другим именем — удобно для переименования.</p>'
    )
    return th('Копировать, переносить, удалять', terms, body)


def fl_move():
    return fl('Копировать, переносить, удалять', [
        q('Что сделает Path("a/b/c").mkdir(parents=True, exist_ok=True), если папки a нет?', 'Создаст a, b и c',
          ['Выдаст ошибку: нет папки a', 'Создаст только c'], 'parents=True создаёт недостающих родителей.'),
        q('Чем опасен shutil.rmtree?', 'Удаляет папку со всем содержимым без корзины', ['Работает очень медленно', 'Удаляет только пустые папки'],
          'Путь проверяют дважды.'),
        qo('Что выведет программа?', 'from pathlib import Path\nprint(Path("фото/a.jpg").with_name("b.png").as_posix())', ['b.png', 'фото/a.png', 'фото/b.jpg'],
           'Место то же, имя новое: фото/b.png.'),
    ])


def code_move():
    return ts('Копировать, переносить, удалять', [
        task('Переименование фото. В папке «фото» лежат снимки IMG_….jpg и другие файлы. Переименуй все .jpg по алфавиту старых имён в '
             '«ПРЕФИКС_001.jpg», «ПРЕФИКС_002.jpg»… — префикс подаётся на вход. Для каждого выведи «старое → новое», затем содержимое папки '
             'по алфавиту строкой через запятую с пробелом.',
             'for i, p in enumerate(sorted(folder.glob("*.jpg")), 1): new = p.with_name(f"{prefix}_{i:03}.jpg"); p.rename(new).\n'
             '{i:03} — номер тремя цифрами с нулями.',
             'from pathlib import Path\n\nprefix = input()\nfolder = Path("фото")\nfor i, p in enumerate(sorted(folder.glob("*.jpg")), 1):\n'
             '    new = p.with_name(f"{prefix}_{i:03}.jpg")\n    print(f"{p.name} → {new.name}")\n    p.rename(new)\nprint(", ".join(p.name for p in sorted(folder.iterdir())))',
             ['отпуск', 'лето2026'], files=PHOTOS),
        task('Резервная копия. Скопируй все .txt из папки «заметки» в папку «архив» (создай её, если нет). Файл, который уже есть в архиве, не '
             'перезаписывай. Для каждого .txt по алфавиту выведи «скопирован: ИМЯ» или «уже есть: ИМЯ», затем «Копий: N».',
             'Path("архив").mkdir(exist_ok=True). target = Path("архив") / p.name; если target.exists() — пропустить, иначе shutil.copy(p, target).',
             'import shutil\nfrom pathlib import Path\n\narchive = Path("архив")\narchive.mkdir(exist_ok=True)\ncopied = 0\nfor p in sorted(Path("заметки").glob("*.txt")):\n'
             '    target = archive / p.name\n    if target.exists():\n        print(f"уже есть: {p.name}")\n    else:\n        shutil.copy(p, target)\n        print(f"скопирован: {p.name}")\n'
             '        copied += 1\nprint(f"Копий: {copied}")',
             [''], files=NOTES),
    ])


def project():
    return pj('Разобрать папку «Загрузки»',
              'В папке «Загрузки» всё вперемешку. Разложи файлы по подпапкам внутри неё: «Картинки» — .jpg, .png, .gif; «Документы» — .pdf, .docx, .txt; '
              '«Музыка» — .mp3; «Архивы» — .zip; всё остальное — «Прочее». Если на вход подана строка «план», только выведи, что куда переедет, '
              'ничего не перенося; если «разобрать» — перенеси. В обоих случаях для каждого файла по алфавиту выведи «ФАЙЛ → ПАПКА», затем по '
              'папкам в алфавитном порядке «ПАПКА: N». После переноса выведи ещё всё содержимое «Загрузки» на любой глубине по алфавиту '
              'путей относительно неё (с прямыми косыми), по строке на путь.',
              'Словарь расширение → папка; папка по умолчанию — «Прочее»\nСписок файлов собери до переноса: files = sorted(p for p in root.iterdir() if p.is_file())\n'
              'Перенос: (root / папка).mkdir(exist_ok=True); p.rename(root / папка / p.name)',
              'from pathlib import Path\n\nKINDS = {".jpg": "Картинки", ".png": "Картинки", ".gif": "Картинки", ".pdf": "Документы", ".docx": "Документы",\n'
              '         ".txt": "Документы", ".mp3": "Музыка", ".zip": "Архивы"}\nroot = Path("Загрузки")\nmode = input()\nfiles = sorted(p for p in root.iterdir() if p.is_file())\n'
              'counts = {}\nfor p in files:\n    folder = KINDS.get(p.suffix.lower(), "Прочее")\n    print(f"{p.name} → {folder}")\n    counts[folder] = counts.get(folder, 0) + 1\n'
              '    if mode == "разобрать":\n        (root / folder).mkdir(exist_ok=True)\n        p.rename(root / folder / p.name)\nfor folder in sorted(counts):\n'
              '    print(f"{folder}: {counts[folder]}")\nif mode == "разобрать":\n    for p in sorted(root.rglob("*")):\n        print(p.relative_to(root).as_posix())',
              ['план', 'разобрать'], files=DOWNLOADS)


def build():
    return topic('Автоматизация: наводим порядок в папках', 'обход папок, копирование, перенос', [
        th_walk(), fl_walk(), code_walk(),
        th_move(), fl_move(), code_move(),
        project(),
    ], opt=True)
