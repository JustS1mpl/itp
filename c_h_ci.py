from dsl import *

# Нора после «Итоговые проекты» (рядом с «Инструментами»): CI/CD и GitHub Actions. YAML-файлы workflow и настройки GitHub — для
# компьютера и сайта (<pre class="pc">); в задачах — логика: разбор workflow, матрица версий, конвейер с needs, правила запуска по
# событиям. Мини-проект — свой маленький CI: найти тесты в модуле через dir/getattr, прогнать, решить про сборку и выкладку.

WF_TEST = ('name: Тесты\non: [push, pull_request]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - name: Забрать код\n'
           '        uses: actions/checkout@v4\n      - name: Поставить Python\n        uses: actions/setup-python@v5\n        with:\n'
           '          python-version: "3.13"\n      - name: Зависимости\n        run: pip install -r requirements.txt\n      - name: Тесты\n        run: pytest -q\n')
WF_DEPLOY = ('name: Выкладка\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n'
             '      - name: Тесты\n        run: pytest\n  deploy:\n    needs: test\n    if: github.ref == \'refs/heads/main\'\n    runs-on: ubuntu-latest\n'
             '    steps:\n      - name: Забрать код\n        uses: actions/checkout@v4\n      - name: На сервер\n        run: ./deploy.sh\n        env:\n'
             '          TOKEN: ${{ secrets.DEPLOY_TOKEN }}\n')
WF_LINT = 'name: Стиль\non: [pull_request]\njobs:\n  lint:\n    runs-on: windows-latest\n    steps:\n      - name: Проверка\n        run: ruff check .\n'
WF = {'test.yml': WF_TEST, 'deploy.yml': WF_DEPLOY, 'lint.yml': WF_LINT}


def th_ci():
    terms = [
        ('CI', 'Continuous Integration — непрерывная интеграция: на каждое изменение кода сервер сам собирает проект и запускает тесты. Сломал — '
               'узнаешь через минуту, а не через месяц.'),
        ('GitHub Actions', 'Встроенный в GitHub CI: по событию (push, pull request) запускает задания на своих серверах по описанию из файла '
                           '.github/workflows/*.yml.'),
        ('workflow', 'Файл-сценарий GitHub Actions: когда запускаться (on), какие задания (jobs) и их шаги (steps). Пишется на YAML — формате, где '
                     'вложенность задают отступы.'),
        ('job', 'Задание внутри workflow: отдельная чистая машина (runs-on), на которой по очереди выполняются шаги. Разные jobs идут параллельно, '
                'если не связаны needs.'),
        ('step', 'Шаг задания: готовое действие (uses: actions/checkout@v4 — забрать код) или команда терминала (run: pytest).'),
        ('pull request', 'Запрос «влей мои изменения в main». На нём CI показывает зелёную галочку или красный крестик; с красным вливать нельзя.'),
        ('матрица', 'strategy.matrix — один job запускается для всех сочетаний параметров: версии Python × системы. 3 версии × 2 системы = 6 запусков.'),
    ]
    body = (
        '<p>В норе «Инструменты» ты писал тесты. Но тесты, которые надо не забыть запустить, однажды забудут. [[CI]] запускает их сам — '
        'на сервере, после каждого изменения. Самый популярный вариант — [[GitHub Actions]]: кладёшь в репозиторий файл [[workflow]], '
        'и GitHub выполняет его на каждый push и [[pull request]]:</p>'
        '<pre class="pc">' + WF_TEST.rstrip('\n') + '</pre>'
        '<p>Читается сверху вниз: на push и pull request запустить [[job]] test на свежей Ubuntu; [[step]]ы — забрать код, поставить Python, '
        'поставить пакеты, прогнать pytest. Упал хоть один шаг — job красный, и в pull request вместо галочки крестик.</p>'
        '<p>Код должен работать везде, где им будут пользоваться. [[матрица]] запускает тот же job на разных версиях и системах:</p>'
        '<pre class="pc">    strategy:\n      matrix:\n        python: ["3.11", "3.12", "3.13"]\n        os: [ubuntu-latest, windows-latest]\n'
        '    runs-on: ${{ matrix.os }}</pre>'
        '<p>Все сочетания — это <code>itertools.product</code>:</p>'
        + ex('from itertools import product\n\nversions = ["3.11", "3.12", "3.13"]\nsystems = ["ubuntu", "windows"]\nruns = list(product(versions, systems))\n'
             'print(len(runs), "запусков")\nfor v, s in runs[:3]:\n    print(f"python {v} на {s}")') +
        '<p>YAML — это текст с отступами, и его разбор — обычная работа со строками: отступ — разница длин строки до и после lstrip:</p>'
        + ex('lines = ["jobs:", "  test:", "    runs-on: ubuntu-latest", "    steps:", "      - name: Тесты"]\nfor line in lines:\n'
             '    indent = len(line) - len(line.lstrip())\n    key, value = line.strip().split(":", 1)\n    print(indent, repr(key), repr(value.strip()))')
    )
    return th('Тесты на каждый push', terms, body)


def fl_ci():
    return fl('Тесты на каждый push', [
        q('Когда запустится workflow с on: [pull_request]?', 'Когда открыли или обновили pull request', ['При каждом push в любую ветку',
          'Раз в сутки'], 'on — список событий-триггеров.'),
        q('Матрица: python 3.12, 3.13; os ubuntu, windows, macos. Сколько запусков?', '6', ['5', '3'], 'Все сочетания: 2 × 3.'),
        q('Шаг «Тесты» упал. Что увидят в pull request?', 'Красный крестик: вливать нельзя', ['Ничего: CI только для main',
          'Зелёную галочку с предупреждением'], 'Упавший шаг делает job красным.'),
        q('Чем uses: отличается от run: в шаге?', 'uses — готовое действие, run — команда терминала', ['Ничем', 'uses работает только на Windows'],
          'actions/checkout — готовое действие «забрать код».'),
    ])


def code_ci():
    return ts('Тесты на каждый push', [
        task('Разбор workflow. Рядом лежат test.yml, deploy.yml и lint.yml; на вход подаётся имя файла. Файл упрощённый: строка «name: …» без отступа — имя '
             'workflow; «on: [a, b]» — события; строка с отступом ровно 2 пробела вида «ИМЯ:» — начало job; «runs-on: …» — его машина; «- name: …» или '
             '«- uses: …» — начало шага (у шага без name имя — «без имени»); «uses: …» и «run: …» — действие текущего шага. Остальные строки пропускай.\n'
             'Выведи «Workflow: ИМЯ», «События: через запятую с пробелом», потом для каждого job «Job ИМЯ (МАШИНА): N шагов» и шаги '
             '«  K. ИМЯ — uses ДЕЙСТВИЕ» или «  K. ИМЯ — run КОМАНДА».',
             'Отступ: len(line) - len(line.lstrip()). Ключ и значение: line.strip().split(":", 1) — но «- name:» начинается с «- ».\n'
             'Job храни словарём {"name", "os", "steps": []}, шаг — списком [имя, вид, действие].',
             'jobs = []\nfor line in open(input(), encoding="utf-8"):\n    indent = len(line) - len(line.lstrip())\n    text = line.strip()\n    if not text:\n        continue\n'
             '    starts_step = text.startswith("- ")\n    if starts_step:\n        text = text[2:]\n    key, value = text.split(":", 1)\n    value = value.strip()\n'
             '    if indent == 0 and key == "name":\n        print("Workflow:", value)\n    elif indent == 0 and key == "on":\n        print("События:", value.strip("[]"))\n'
             '    elif indent == 2 and value == "":\n        jobs.append({"name": key, "os": "?", "steps": []})\n    elif key == "runs-on":\n        jobs[-1]["os"] = value\n'
             '    elif starts_step:\n        jobs[-1]["steps"].append([value if key == "name" else "без имени", "", ""])\n        if key == "uses":\n'
             '            jobs[-1]["steps"][-1][1:] = ["uses", value]\n    elif key in ("uses", "run"):\n        jobs[-1]["steps"][-1][1:] = [key, value]\n'
             'for job in jobs:\n    print(f"Job {job[\'name\']} ({job[\'os\']}): {len(job[\'steps\'])} шагов")\n    for k, (name, kind, action) in enumerate(job["steps"], 1):\n'
             '        print(f"  {k}. {name} — {kind} {action}")',
             ['test.yml', 'deploy.yml', 'lint.yml'], files=WF),
        task('Матрица. На вход подаются строки «ПАРАМЕТР: значения через пробел», затем, возможно, строки «exclude: значения через пробел» (сочетание, '
             'которое не запускать, — значения в порядке параметров), последняя — «конец». Выведи все сочетания по порядку product строками '
             '«значения через « / »», пропуская исключённые, затем «Запусков: N» и «Минут: M» — каждый запуск идёт 3 минуты, но на windows — 6.',
             'Значения параметров — список списков; product(*lists). Исключения храни множеством кортежей.',
             'from itertools import product\n\nparams, excluded = [], set()\nwhile True:\n    line = input()\n    if line == "конец":\n        break\n'
             '    key, values = line.split(":")\n    if key == "exclude":\n        excluded.add(tuple(values.split()))\n    else:\n        params.append(values.split())\n'
             'runs = [combo for combo in product(*params) if combo not in excluded]\nfor combo in runs:\n    print(" / ".join(combo))\n'
             'print(f"Запусков: {len(runs)}")\nprint(f"Минут: {sum(6 if \'windows\' in combo else 3 for combo in runs)}")',
             ['python: 3.12 3.13\nos: ubuntu windows\nконец', 'python: 3.11 3.12 3.13\nos: ubuntu windows macos\nexclude: 3.11 windows\nexclude: 3.11 macos\nконец',
              'node: 20 22\nконец']),
    ])


def th_cd():
    terms = [
        ('CD', 'Continuous Delivery/Deployment — непрерывная выкладка: после зелёных тестов сервер сам собирает и выкладывает новую версию.'),
        ('needs', 'needs: test — job ждёт, пока test пройдёт. Если test упал, зависящий job пропускается.'),
        ('секреты Actions', 'Пароли и токены, сохранённые в настройках репозитория (Settings → Secrets). В workflow — ${{ secrets.ИМЯ }}; в логах '
                            'они заменяются звёздочками.'),
        ('dir', 'dir(объект) — отсортированный список имён его атрибутов: у модуля — его функции, переменные и служебные имена.'),
    ]
    body = (
        '<p>Тесты зелёные — дальше по конвейеру: собрать, выложить. Это [[CD]]. Задания связывают [[needs]], а выкладку разрешают только из '
        'главной ветки:</p>'
        '<pre class="pc">' + WF_DEPLOY.rstrip('\n') + '</pre>'
        '<p>Пароль сервера в файл не пишут — файл видят все, у кого есть доступ к репозиторию. Его кладут в [[секреты Actions]] и подставляют '
        'при запуске. Правило конвейера простое: упал этап — всё, что от него зависит, не запускается, а итог красный:</p>'
        + ex('needs = {"lint": [], "test": [], "build": ["lint", "test"], "deploy": ["build"]}\nresult = {"lint": "ok", "test": "fail", "build": "ok", "deploy": "ok"}\n'
             'status = {}\nfor job in needs:\n    if any(status[n] != "ok" for n in needs[job]):\n        status[job] = "пропущен"\n    else:\n'
             '        status[job] = result[job]\n    print(job, status[job])') +
        '<h3>Как CI находит тесты</h3>'
        '<p>pytest не нужно перечислять тесты: он импортирует файлы test_*.py и берёт функции, чьё имя начинается с test_. То же можно '
        'сделать самим: [[dir]] даёт имена всего, что есть в модуле, а getattr — сам объект по имени:</p>'
        + ex('import math\n\nnames = [n for n in dir(math) if n.startswith("is")]\nprint(names)\nprint(getattr(math, "isqrt")(17))') +
        '<p>В мини-проекте ты так соберёшь свой маленький CI: найдёт тесты, прогонит их и решит, можно ли выкладывать.</p>'
    )
    return th('Конвейер выкладки', terms, body)


def fl_cd():
    return fl('Конвейер выкладки', [
        q('deploy: needs: test. Тесты упали. Что с deploy?', 'Пропускается', ['Запускается, но красный', 'Запускается как обычно'],
          'needs — «только после успешного».'),
        q('Где хранить токен для выкладки?', 'В секретах репозитория, ${{ secrets.ИМЯ }}', ['Прямо в deploy.yml', 'В README.md'],
          'Файлы workflow видны всем с доступом к коду.'),
        qo('Что выведет программа?', 'import math\nprint(len([n for n in dir(math) if n.startswith("log")]))', ['1', '2', '0'],
           'log, log10, log1p, log2.'),
    ])


def code_cd():
    return ts('Конвейер выкладки', [
        task('Прогон конвейера. На вход подаются строки «JOB: ЗАВИСИМОСТИ | РЕЗУЛЬТАТ» (зависимости через пробел, может не быть; результат — ok или fail), '
             'последняя — «конец». Зависимости могут стоять ниже по списку. Статус job: «пропущен», если хоть одна зависимость не ok; иначе его '
             'результат. Выведи статусы в порядке ввода «JOB: СТАТУС», затем «Итог: зелёный», если все ok, иначе «Итог: красный».',
             'Статус удобно считать рекурсивной функцией status(job) с кэшем-словарём: сначала статусы зависимостей.',
             'needs, result, cache = {}, {}, {}\nwhile True:\n    line = input()\n    if line == "конец":\n        break\n    left, res = line.split("|")\n'
             '    job, deps = left.split(":")\n    needs[job.strip()] = deps.split()\n    result[job.strip()] = res.strip()\n\n\ndef status(job):\n'
             '    if job not in cache:\n        if any(status(d) != "ok" for d in needs[job]):\n            cache[job] = "пропущен"\n        else:\n'
             '            cache[job] = result[job]\n    return cache[job]\n\n\nfor job in needs:\n    print(f"{job}: {status(job)}")\n'
             'print("Итог:", "зелёный" if all(status(j) == "ok" for j in needs) else "красный")',
             ['deploy: build | ok\nlint: | ok\ntest: | ok\nbuild: lint test | ok\nконец', 'deploy: build | ok\nbuild: test | ok\ntest: | fail\ndocs: | ok\nконец',
              'a: | ok\nb: a | fail\nc: b | ok\nконец']),
        task('Что запустится. Правила: тесты (test) идут на любой push и на pull_request; выкладка (deploy) — только на push в ветку main или на '
             'тег, который начинается с v и дальше состоит из цифр и точек (v1.2.0). На вход подаются события «push ВЕТКА», «pull_request ВЕТКА» или '
             '«tag ИМЯ», последняя строка — «конец». Для каждого выведи «СОБЫТИЕ → test, deploy», «СОБЫТИЕ → test», «СОБЫТИЕ → deploy» или '
             '«СОБЫТИЕ → ничего». В конце — «Выкладок: N».',
             'Тег: name.startswith("v") and name[1:] and all(ch.isdigit() or ch == "." for ch in name[1:]).',
             'deploys = 0\nwhile True:\n    line = input()\n    if line == "конец":\n        break\n    kind, name = line.split()\n    jobs = []\n'
             '    if kind in ("push", "pull_request"):\n        jobs.append("test")\n    is_version = name.startswith("v") and len(name) > 1 and all(ch.isdigit() or ch == "." for ch in name[1:])\n'
             '    if (kind == "push" and name == "main") or (kind == "tag" and is_version):\n        jobs.append("deploy")\n        deploys += 1\n'
             '    print(line, "→", ", ".join(jobs) or "ничего")\nprint(f"Выкладок: {deploys}")',
             ['push main\npush feature/login\npull_request main\ntag v1.2.0\ntag beta\nконец', 'tag v\ntag v2\npull_request dev\nконец']),
    ])


CALC_OK = ('def add(a, b):\n    return a + b\n\n\ndef average(xs):\n    if not xs:\n        return 0\n    return sum(xs) / len(xs)\n\n\n'
           'def grade(score):\n    if score >= 90:\n        return 5\n    if score >= 75:\n        return 4\n    return 3\n')
CALC_BAD = CALC_OK.replace('    if not xs:\n        return 0\n', '').replace('score >= 90', 'score > 90')
TESTS = ('from {v} import calc\n\n\ndef test_add():\n    assert calc.add(2, 3) == 5\n\n\ndef test_average():\n    assert calc.average([4, 5]) == 4.5\n\n\n'
         'def test_average_empty():\n    assert calc.average([]) == 0, "пустой список — 0"\n\n\ndef test_grade_border():\n    assert calc.grade(90) == 5, "90 — это 5"\n\n\n'
         'def helper():\n    return 42\n')
REPO = {'v1/calc.py': CALC_OK, 'v1/test_calc.py': TESTS.format(v='v1'), 'v2/calc.py': CALC_BAD, 'v2/test_calc.py': TESTS.format(v='v2')}


def project():
    return pj('Свой маленький CI',
              'В репозитории две версии проекта: папки v1 и v2, в каждой calc.py и тесты test_calc.py (функции test_… с assert). На вход подаются версия '
              '(v1 или v2) и ветка. Импортируй нужные тесты (from v1 import test_calc или from v2 import test_calc), найди в модуле через dir все имена, '
              'начинающиеся с test_ (dir отдаёт их по алфавиту), и запусти каждую функцию. Выводи «ok ИМЯ», «FAIL ИМЯ: ТЕКСТ» (текст assert, без него — '
              '«без сообщения») или «ERROR ИМЯ: ТИП» (имя класса ошибки). Затем строки конвейера: «test: ok» или «test: fail»; «build: ok», если test '
              'ok, иначе «build: пропущен»; «deploy: ok», если build ok и ветка main; «deploy: не нужен» — если build ok, а ветка другая; '
              '«deploy: пропущен» — если build пропущен. Последней — «Итог: зелёный» или «Итог: красный» (красный — если test упал).',
              'tests = test_calc if version == "v1" — но проще импортировать нужный модуль в if/else под одним именем: from v1 import test_calc as tests\n'
              'Функцию по имени даёт getattr(tests, name); текст assert — str(e), имя класса — type(e).__name__',
              'version = input()\nbranch = input()\nif version == "v1":\n    from v1 import test_calc as tests\nelse:\n    from v2 import test_calc as tests\n'
              'failed = 0\nfor name in dir(tests):\n    if not name.startswith("test_"):\n        continue\n    try:\n        getattr(tests, name)()\n'
              '    except AssertionError as e:\n        failed += 1\n        print(f"FAIL {name}: {str(e) or \'без сообщения\'}")\n    except Exception as e:\n'
              '        failed += 1\n        print(f"ERROR {name}: {type(e).__name__}")\n    else:\n        print("ok", name)\n'
              'if failed:\n    print("test: fail")\n    print("build: пропущен")\n    print("deploy: пропущен")\n    print("Итог: красный")\nelse:\n'
              '    print("test: ok")\n    print("build: ok")\n    print("deploy: ok" if branch == "main" else "deploy: не нужен")\n    print("Итог: зелёный")',
              ['v1\nmain', 'v2\nmain', 'v1\nfeature/grades'], files=REPO)


def build():
    return topic('CI/CD: тесты сами', 'GitHub Actions, матрица, конвейер, выкладка', [
        th_ci(), fl_ci(), code_ci(),
        th_cd(), fl_cd(), code_cd(),
        project(),
    ], opt=True)
