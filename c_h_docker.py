from dsl import *

# Нора после «Рекурсия»: Docker. Сам Docker в браузере не запустить — Dockerfile, compose и команды показываем в <pre class="pc">,
# а в задачах проверяем логику: разбор Dockerfile, кэш слоёв, порядок запуска сервисов (рекурсией), проброс портов, линтер.
# Две теории: образ и контейнер (инструкции, слои, кэш); несколько контейнеров (compose, порты, тома, depends_on).

DF_GOOD = ('# сервис погоды\nFROM python:3.13-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\n'
           'COPY . .\nENV PORT=8000\nEXPOSE 8000\nUSER app\nCMD ["python", "main.py"]\n')
DF_BOT = ('FROM python:3.12\nWORKDIR /bot\nCOPY . .\nRUN pip install -r requirements.txt\nENV BOT_TOKEN=12345:secret\n'
          'EXPOSE 8080\nEXPOSE 9090\nCMD ["python", "bot.py"]\n')
DF_BAD = ('# собирал в спешке\nWORKDIR /site\nFROM node\nCOPY . .\nRUN npm install\nENV API_KEY=abc DEBUG=1\nCMD ["npm", "start"]\n'
          'RUN pip install requests\nCMD ["node", "server.js"]\n')
DF_MIN = 'FROM alpine:3.20\nCMD ["echo", "привет"]\n'
FILES = {'Dockerfile': DF_GOOD, 'bot.Dockerfile': DF_BOT, 'old.Dockerfile': DF_BAD, 'tiny.Dockerfile': DF_MIN}


def th_image():
    terms = [
        ('Docker', 'Программа, которая запускает приложения в контейнерах: изолированных «коробках» со своей системой, Python и пакетами.'),
        ('образ', 'Шаблон контейнера: файловая система с ОС, языком, пакетами и кодом. Собирается по Dockerfile командой docker build, '
                  'не меняется.'),
        ('контейнер', 'Запущенный экземпляр образа: процесс в своей коробке. Из одного образа можно запустить сколько угодно контейнеров.'),
        ('Dockerfile', 'Рецепт образа: по инструкции в строке. FROM — базовый образ, WORKDIR — рабочая папка, COPY — скопировать файлы, '
                       'RUN — выполнить команду при сборке, ENV — переменная окружения, EXPOSE — порт, CMD — что запустить при старте.'),
        ('базовый образ', 'Образ, с которого начинается сборка (FROM python:3.13-slim). Часть после двоеточия — тег, обычно версия.'),
        ('слой', 'Каждая инструкция Dockerfile даёт слой — снимок изменений файлов. Образ — стопка слоёв.'),
        ('кэш слоёв', 'Docker помнит слои прошлых сборок. Если инструкция и её файлы не изменились, слой берётся из кэша. Но после первого '
                      'изменённого слоя все следующие собираются заново.'),
    ]
    body = (
        '<p>«У меня всё работает!» — а у друга другая версия Python, нет нужного пакета, другая система. [[Docker]] решает это раз и навсегда: '
        'приложение едет вместе со своим окружением в [[контейнер]]е. Контейнер запускается из [[образ]]а, а образ собирается по рецепту — '
        '[[Dockerfile]]:</p>'
        '<pre class="pc">' + DF_GOOD.rstrip('\n') + '</pre>'
        '<p>Начинаем с [[базовый образ|базового образа]] с Python, копируем список пакетов, ставим их, копируем код и говорим, что запускать. '
        'На компьютере с установленным Docker это превращается в работающий сервис двумя командами:</p>'
        '<pre class="pc">docker build -t weather .              # собрать образ с именем weather\ndocker run -p 8000:8000 weather        # запустить контейнер\n'
        'docker ps                              # какие контейнеры работают\ndocker logs ID                         # что контейнер напечатал\n'
        'docker stop ID                         # остановить</pre>'
        '<h3>Слои и кэш</h3>'
        '<p>Каждая инструкция — [[слой]]. При пересборке Docker идёт сверху вниз и берёт слои из [[кэш слоёв|кэша]], пока инструкция и '
        'скопированные ею файлы те же. Первый изменившийся слой и <b>все после него</b> собираются заново. Поэтому порядок важен:</p>'
        '<pre class="pc">COPY requirements.txt .        # меняется редко\nRUN pip install -r requirements.txt   # долгий шаг остаётся в кэше\n'
        'COPY . .                       # код меняется часто — копируем последним</pre>'
        '<p>Если написать <code>COPY . .</code> до <code>pip install</code>, любая правка в коде заставит заново ставить все пакеты — '
        'минуты ожидания на каждую сборку. Разбирать Dockerfile — обычная работа со строками:</p>'
        + ex('text = """FROM python:3.13-slim\nWORKDIR /app\nCOPY . .\nCMD ["python", "main.py"]"""\nfor n, line in enumerate(text.split("\\n"), 1):\n'
             '    cmd, _, rest = line.partition(" ")\n    print(n, cmd, "→", rest)') +
        '<p><code>partition(" ")</code> делит строку по первому пробелу на три части: до, сам разделитель и после.</p>'
    )
    return th('Образ и контейнер', terms + [('partition', 'строка.partition(разделитель) — кортеж из трёх строк: до первого разделителя, '
                                                         'сам разделитель, после. Если разделителя нет — (строка, "", "").')], body)


def fl_image():
    return fl('Образ и контейнер', [
        q('Чем образ отличается от контейнера?', 'Образ — шаблон, контейнер — запущенный экземпляр', ['Это одно и то же',
          'Контейнер — шаблон, образ — запущенный'], 'Из одного образа — сколько угодно контейнеров.'),
        q('В Dockerfile поменяли третью инструкцию из восьми. Что пересоберётся?', 'Третья и все после неё', ['Только третья',
          'Все восемь'], 'После первого изменённого слоя кэш не используется.'),
        q('Почему COPY . . пишут после pip install?', 'Чтобы правка кода не сбрасывала кэш установки пакетов', ['Иначе pip не найдёт Python',
          'Так образ меньше весит'], 'Код меняется часто, пакеты — редко.'),
        qo('Что выведет программа?', 'print("RUN pip install x".partition(" ")[2])', ['RUN', 'pip', ' '], 'Третья часть — всё после первого пробела.'),
    ])


def code_image():
    return ts('Образ и контейнер', [
        task('Разбор Dockerfile. Рядом лежат файлы Dockerfile, bot.Dockerfile, old.Dockerfile и tiny.Dockerfile. На вход подаётся имя файла. Пропусти пустые '
             'строки и комментарии (начинаются с #). Выведи «Базовый образ: …» (аргумент первой FROM или «нет», если FROM нет), «Порты: …» (аргументы '
             'всех EXPOSE через запятую с пробелом или «нет»), «Запуск: …» (аргумент последней CMD или «нет») и «Инструкций: N», а затем '
             'по инструкциям в алфавитном порядке «ИНСТРУКЦИЯ×K».',
             'cmd, _, rest = line.partition(" "). Счётчик — Counter; for c in sorted(counts).',
             'from collections import Counter\n\nbase, ports, run = "нет", [], "нет"\ncounts = Counter()\nfor line in open(input(), encoding="utf-8"):\n'
             '    line = line.strip()\n    if not line or line.startswith("#"):\n        continue\n    cmd, _, rest = line.partition(" ")\n    counts[cmd] += 1\n'
             '    if cmd == "FROM" and base == "нет":\n        base = rest\n    elif cmd == "EXPOSE":\n        ports.append(rest)\n    elif cmd == "CMD":\n        run = rest\n'
             'print("Базовый образ:", base)\nprint("Порты:", ", ".join(ports) or "нет")\nprint("Запуск:", run)\nprint(f"Инструкций: {sum(counts.values())}")\n'
             'for c in sorted(counts):\n    print(f"{c}×{counts[c]}")',
             ['Dockerfile', 'bot.Dockerfile', 'old.Dockerfile', 'tiny.Dockerfile'], files=FILES),
        task('Кэш слоёв. Первая строка — «изменены:» и через пробел файлы, которые поменялись с прошлой сборки (может не быть ни одного). Дальше — '
             'старый Dockerfile до строки «---» и новый до строки «конец» (без пустых строк и комментариев). Docker идёт по новому файлу сверху вниз: '
             'слой берётся из кэша, если все слои выше из кэша, в старом файле на том же месте та же строка, а для COPY — ни один из её источников не '
             'изменён. Источники COPY — все аргументы, кроме последнего (куда копировать); источник «.» задевает любой файл, источник «src/» — файлы, '
             'начинающиеся на «src/». Выведи «N. СТРОКА — кэш» или «N. СТРОКА — сборка», затем «Из кэша: K из M».',
             'changed = input().split()[1:]. Флаг cached = True; как только слой собирается, флаг навсегда False.\n'
             'Совпадение источника: src == "." or f == src or f.startswith(src) при src, кончающемся на «/».',
             'def read(stop):\n    lines = []\n    while True:\n        line = input()\n        if line == stop:\n            return lines\n        lines.append(line)\n\n\n'
             'def touched(src, changed):\n    for f in changed:\n        if src == "." or f == src or (src.endswith("/") and f.startswith(src)):\n            return True\n    return False\n\n\n'
             'changed = input().split()[1:]\nold = read("---")\nnew = read("конец")\ncached = True\nk = 0\nfor i, line in enumerate(new):\n'
             '    if cached and (i >= len(old) or old[i] != line):\n        cached = False\n    parts = line.split()\n'
             '    if cached and parts[0] == "COPY" and any(touched(src, changed) for src in parts[1:-1]):\n        cached = False\n    if cached:\n        k += 1\n'
             '    print(f"{i + 1}. {line} — {\'кэш\' if cached else \'сборка\'}")\nprint(f"Из кэша: {k} из {len(new)}")',
             ['изменены: main.py\nFROM python:3.13-slim\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD ["python", "main.py"]\n---\n'
              'FROM python:3.13-slim\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD ["python", "main.py"]\nконец',
              'изменены: main.py\nFROM python:3.13-slim\nCOPY . .\nRUN pip install -r requirements.txt\nCMD ["python", "main.py"]\n---\n'
              'FROM python:3.13-slim\nCOPY . .\nRUN pip install -r requirements.txt\nCMD ["python", "main.py"]\nконец',
              'изменены:\nFROM python:3.12\nRUN pip install flask\n---\nFROM python:3.13\nRUN pip install flask\nконец',
              'изменены: docs/readme.md\nFROM python:3.13\nCOPY src/ /app/src/\nCOPY config.toml /app/\nRUN python -m compileall /app\n---\n'
              'FROM python:3.13\nCOPY src/ /app/src/\nCOPY config.toml /app/\nRUN python -m compileall /app\nENV MODE=prod\nконец']),
    ])


COMPOSE = ('services:\n  web:\n    build: .\n    ports:\n      - "8000:8000"\n    environment:\n      - DB_URL=postgres://db:5432/shop\n'
           '    depends_on:\n      - db\n  db:\n    image: postgres:16\n    volumes:\n      - dbdata:/var/lib/postgresql/data\n\nvolumes:\n  dbdata:')


def th_compose():
    terms = [
        ('docker compose', 'Инструмент для запуска нескольких контейнеров вместе по одному файлу compose.yaml: сервисы, порты, тома, переменные. '
                           'docker compose up — поднять всё, down — остановить.'),
        ('проброс порта', 'Связь порта компьютера с портом контейнера: "8080:8000" — запрос на localhost:8080 попадёт в контейнер на порт 8000. '
                          'Один порт компьютера может занять только один контейнер.'),
        ('том', 'Volume — папка с данными, которая живёт отдельно от контейнера. Контейнер удалили — данные в томе остались.'),
        ('depends_on', 'Список сервисов, которые compose запускает раньше этого: сайт зависит от базы — база стартует первой.'),
    ]
    body = (
        '<p>Настоящее приложение — это несколько программ: сайт, база данных, бот, очередь задач. Каждую запускают в своём контейнере, а '
        'вместе ими управляет [[docker compose]] по одному файлу:</p>'
        '<pre class="pc">' + COMPOSE + '</pre>'
        '<p>Что здесь важно:</p><ul>'
        '<li><code>ports</code> — [[проброс порта]]: открываешь в браузере localhost:8000 и попадаешь в контейнер web;</li>'
        '<li>внутри compose контейнеры видят друг друга по имени сервиса: сайт ходит в базу по адресу <code>db:5432</code>;</li>'
        '<li><code>volumes</code> — [[том]]: контейнер базы можно пересоздать, а данные не пропадут. Без тома всё, что записано внутри '
        'контейнера, исчезает вместе с ним;</li>'
        '<li>[[depends_on]] задаёт порядок запуска: сначала db, потом web.</li></ul>'
        '<p>Порядок запуска — та же рекурсия, что обход дерева: чтобы запустить сервис, сначала запусти всё, от чего он зависит. Если '
        'зависимости закольцованы (A ждёт B, B ждёт A), запустить ничего нельзя:</p>'
        + ex('deps = {"web": ["db", "cache"], "db": [], "cache": [], "worker": ["db"]}\nstarted = []\n\n\ndef start(name):\n    if name in started:\n        return\n'
             '    for d in deps[name]:\n        start(d)\n    started.append(name)\n\n\nfor name in deps:\n    start(name)\nprint(" → ".join(started))') +
        '<pre class="pc">docker compose up -d        # поднять все сервисы в фоне\ndocker compose logs web     # логи одного сервиса\n'
        'docker compose down         # остановить и удалить контейнеры (тома остаются)</pre>'
    )
    return th('Несколько контейнеров', terms, body)


def fl_compose():
    return fl('Несколько контейнеров', [
        q('ports: "3000:80". Куда попадёт запрос на localhost:3000?', 'В контейнер на порт 80', ['В контейнер на порт 3000',
          'На порт 80 компьютера'], 'Слева — порт компьютера, справа — контейнера.'),
        q('Контейнер базы удалили и создали заново. Где данные?', 'Сохранились, если лежали в томе', ['Всегда сохраняются',
          'Всегда пропадают'], 'Без тома данные живут и умирают вместе с контейнером.'),
        q('web зависит от db, db — от web. Что будет?', 'Запустить нельзя: зависимости закольцованы', ['Сначала web, потом db',
          'Оба запустятся одновременно'], 'Каждый ждёт другого.'),
    ])


def code_compose():
    return ts('Несколько контейнеров', [
        task('Порядок запуска. На вход подаются строки «СЕРВИС: ЗАВИСИМОСТИ» (зависимости через пробел, может не быть ни одной), последняя — «конец». '
             'Запусти все сервисы в порядке ввода рекурсивно: перед сервисом — его зависимости в порядке перечисления; уже запущенный второй раз '
             'не запускается. Выведи порядок через « → ». Если зависимость не описана — выведи «Нет сервиса ИМЯ» и больше ничего. Если зависимости '
             'закольцованы — «Цикл: ИМЯ» (на сервисе, к которому вернулись) и больше ничего.',
             'Кроме списка запущенных храни множество «запускаются сейчас»: встретил сервис оттуда — это цикл. Ошибку проще всего пробросить '
             'исключением с текстом и поймать снаружи.',
             'deps = {}\nwhile True:\n    line = input()\n    if line == "конец":\n        break\n    name, _, rest = line.partition(":")\n    deps[name.strip()] = rest.split()\n'
             'started = []\nstarting = set()\n\n\ndef start(name):\n    if name in started:\n        return\n    if name not in deps:\n        raise ValueError(f"Нет сервиса {name}")\n'
             '    if name in starting:\n        raise ValueError(f"Цикл: {name}")\n    starting.add(name)\n    for d in deps[name]:\n        start(d)\n'
             '    starting.discard(name)\n    started.append(name)\n\n\ntry:\n    for name in deps:\n        start(name)\n    print(" → ".join(started))\n'
             'except ValueError as e:\n    print(e)',
             ['web: db cache\ndb:\ncache:\nworker: db queue\nqueue:\nконец', 'site: api\napi: db\ndb: site\nконец', 'bot: redis\nконец', 'one:\nконец']),
        task('Проброс портов. На вход подаются строки «СЕРВИС ПОРТ_КОМПЬЮТЕРА:ПОРТ_КОНТЕЙНЕРА», последняя — «конец». Для каждой выведи '
             '«localhost:П → СЕРВИС:К». Если порт компьютера уже занят — «Ошибка: порт П занят сервисом ИМЯ» вместо этого (порт остаётся за первым). '
             'Порт вне 1…65535 — «Ошибка: порт П недопустим». В конце — «Работает: N».',
             'busy — словарь «порт компьютера → сервис». Порты — int(…) после split(":").',
             'busy = {}\nwhile True:\n    line = input()\n    if line == "конец":\n        break\n    name, ports = line.split()\n    host, inner = ports.split(":")\n'
             '    if not 1 <= int(host) <= 65535:\n        print(f"Ошибка: порт {host} недопустим")\n    elif host in busy:\n        print(f"Ошибка: порт {host} занят сервисом {busy[host]}")\n'
             '    else:\n        busy[host] = name\n        print(f"localhost:{host} → {name}:{inner}")\nprint(f"Работает: {len(busy)}")',
             ['web 8000:8000\ndb 5432:5432\nadmin 8000:80\nbot 8080:8080\nконец', 'a 70000:80\nb 80:80\nконец', 'x 1:1\nконец']),
    ])


def project():
    return pj('Линтер Dockerfile',
              'Напиши проверку Dockerfile, как у настоящих линтеров. Рядом лежат файлы Dockerfile, bot.Dockerfile, old.Dockerfile и tiny.Dockerfile; на вход '
              'подаётся имя файла. Пустые строки и комментарии пропускай, но номера строк считай по файлу (с 1). Инструкция — первое слово строки. Правила:\n'
              '— первая инструкция не FROM → «строка N: первой должна быть FROM»;\n'
              '— у образа в FROM нет тега (нет «:») или тег latest → «строка N: закрепи версию образа»;\n'
              '— в ENV есть переменная, в имени которой KEY, TOKEN, PASSWORD или SECRET → «строка N: секрет в образе — передавай при запуске» '
              '(переменные ENV — через пробел в виде ИМЯ=значение; одно замечание на строку);\n'
              '— RUN с «pip install» без «--no-cache-dir» → «строка N: pip install без --no-cache-dir»;\n'
              '— «COPY . .» раньше какого-либо RUN с «install» → «строка N: COPY . . до установки зависимостей» (N — строка COPY);\n'
              '— CMD больше одной → «строка N: лишняя CMD» для каждой, кроме последней.\n'
              'Замечания выводи по возрастанию номера строки (на одной строке — в порядке правил выше). Затем общие: «нет CMD», если CMD нет, и '
              '«нет USER — контейнер работает от root», если нет USER. В конце — «Замечаний: K» или «Замечаний нет».',
              'Сначала собери список (номер, инструкция, остальное) без пустых строк и комментариев\n'
              'Замечания копи списком пар (номер, текст) и в конце отсортируй — sorted по номеру сохранит порядок правил (сортировка устойчива)\n'
              '«COPY . . раньше RUN с install»: найди номер первой такой RUN и сравни',
              'def lint(lines):\n    notes = []\n    if lines and lines[0][1] != "FROM":\n        notes.append((lines[0][0], "первой должна быть FROM"))\n'
              '    installs = [n for n, cmd, rest in lines if cmd == "RUN" and "install" in rest]\n    cmds = [n for n, cmd, rest in lines if cmd == "CMD"]\n'
              '    for n, cmd, rest in lines:\n        if cmd == "FROM":\n            image = rest.split()[0]\n            if ":" not in image or image.endswith(":latest"):\n'
              '                notes.append((n, "закрепи версию образа"))\n        elif cmd == "ENV":\n            names = [v.partition("=")[0].upper() for v in rest.split()]\n'
              '            if any(w in name for name in names for w in ("KEY", "TOKEN", "PASSWORD", "SECRET")):\n'
              '                notes.append((n, "секрет в образе — передавай при запуске"))\n        elif cmd == "RUN" and "pip install" in rest and "--no-cache-dir" not in rest:\n'
              '            notes.append((n, "pip install без --no-cache-dir"))\n        elif cmd == "COPY" and rest == ". ." and installs and n < max(installs):\n'
              '            notes.append((n, "COPY . . до установки зависимостей"))\n    for n in cmds[:-1]:\n        notes.append((n, "лишняя CMD"))\n'
              '    result = [f"строка {n}: {text}" for n, text in sorted(notes, key=lambda p: p[0])]\n    if not cmds:\n        result.append("нет CMD")\n'
              '    if all(cmd != "USER" for n, cmd, rest in lines):\n        result.append("нет USER — контейнер работает от root")\n    return result\n\n\n'
              'lines = []\nfor n, line in enumerate(open(input(), encoding="utf-8"), 1):\n    line = line.strip()\n    if line and not line.startswith("#"):\n'
              '        cmd, _, rest = line.partition(" ")\n        lines.append((n, cmd, rest))\nnotes = lint(lines)\nfor note in notes:\n    print(note)\n'
              'print(f"Замечаний: {len(notes)}" if notes else "Замечаний нет")',
              ['old.Dockerfile', 'bot.Dockerfile', 'Dockerfile', 'tiny.Dockerfile'], files=FILES)


def build():
    return topic('Docker: контейнер за вечер', 'образы, слои и кэш, compose, порты', [
        th_image(), fl_image(), code_image(),
        th_compose(), fl_compose(), code_compose(),
        project(),
    ], opt=True)
