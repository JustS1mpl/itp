import json
from dsl import *

# Нора после «Запросы к серверам»: языковая модель через API. Учебная модель llm.itp живёт в приложении (requests_shim, режим "llm"):
# POST /v1/chat с заголовком Authorization: Bearer КЛЮЧ и json {"messages": [...], "max_tokens"?}; отвечает по правилам — всегда одинаково,
# поэтому вывод можно проверить. Две теории: запрос, роли и история, токены и max_tokens; структурированный вывод — JSON в ответе,
# его проверка и повторный запрос. Мини-проект — сортировщик заявок поддержки.

J = {'sys': 'json'}
T = {'sys': 'заявк'}


def _r(cond, say, **kw):
    d = dict(kw)
    if cond:
        d['if'] = cond
    d['say'] = say
    return d


RULES = [
    # заявки поддержки (проект): системный промпт со словом «заявк»
    _r(['только json'], {'category': 'сбой', 'urgent': True}, ctx=['срочно'], **T),
    _r(['только json'], 'Извините, не могу.', **T),
    _r(['пароль'], {'category': 'доступ', 'urgent': False}, **T),
    _r(['оплат'], '```json\n{"category": "оплата", "urgent": true}\n```', **T),
    _r(['сайт'], {'category': 'сбой', 'urgent': True}, **T),
    _r(['спасибо'], {'category': 'отзыв', 'urgent': False}, **T),
    _r(['котик'], {'category': 'котики', 'urgent': False}, **T),
    _r(['срочно'], 'Это срочная заявка! Передам инженерам.', **T),
    _r([], 'Не понимаю заявку.', **T),
    # оценка отзывов: системный промпт со словом JSON
    _r(['отлично'], {'sentiment': 'positive', 'score': 5}, **J),
    _r(['нормально'], '```json\n{"sentiment": "neutral", "score": 3}\n```', **J),
    _r(['ужасно'], {'sentiment': 'negative', 'score': 1}, **J),
    _r(['сломал'], 'Вот оценка: {"sentiment": "negative", "score": 2}', **J),
    _r(['странно'], {'sentiment': 'strange', 'score': 7}, **J),
    _r(['вкусно'], {'sentiment': 'positive', 'score': '5'}, **J),
    _r([], 'Не могу оценить этот отзыв.', **J),
    # обычный разговор
    _r(['как меня зовут'], 'Тебя зовут Вика.', ctx=['меня зовут вика']),
    _r(['как меня зовут'], 'Тебя зовут Тимур.', ctx=['меня зовут тимур']),
    _r(['как меня зовут'], 'Не знаю: ты не говорил, как тебя зовут.'),
    _r(['меня зовут'], 'Приятно познакомиться!'),
    _r(['столица', 'франц'], 'Столица Франции — Париж.'),
    _r(['кто создал', 'python'], 'Python создал Гвидо ван Россум, первая версия вышла в 1991 году.'),
    _r(['2+2'], '4'),
    _r(['стих', 'кот'], 'Рыжий кот на крыше спит, солнце над трубой горит, ветер шепчет в проводах — кот мурлычет в облаках.'),
    _r(['лучший ученик'], 'Лучшим учеником ИТП в 2025 году стал Артём Соколов из Казани.'),
]
LLM = {'key': 'demo', 'model': 'itp-mini', 'rules': RULES, 'default': 'Не знаю. Спроси иначе.'}
SERVERS = {'_itp_servers.json': json.dumps({
    'llm.itp': {'llm': LLM},
    'busy.llm.itp': {'llm': dict(LLM, statuses=[429, 503, 200])},
}, ensure_ascii=False)}

ASK = ('import os\nimport requests\n\nURL = "http://llm.itp/v1/chat"\nHEADERS = {"Authorization": "Bearer " + os.environ.get("LLM_KEY", "demo")}\n\n\n'
       'def ask(messages, max_tokens=200):\n    r = requests.post(URL, json={"model": "itp-mini", "messages": messages, "max_tokens": max_tokens}, headers=HEADERS)\n'
       '    return r.json()\n')


def th_chat():
    terms = [
        ('LLM', 'Большая языковая модель (large language model): нейросеть, обученная на огромном количестве текстов продолжать текст. '
                'ChatGPT, Claude, GigaChat, YandexGPT — LLM.'),
        ('промпт', 'Текст запроса к модели: задание, вопрос, примеры. От формулировки промпта сильно зависит ответ.'),
        ('роль сообщения', 'У каждого сообщения в запросе есть роль: system — правила для модели («отвечай кратко»), user — реплики '
                           'человека, assistant — прошлые ответы модели.'),
        ('токен', 'Кусочек текста, которым считает модель: часть слова, слово или знак. Плата за API и ограничение длины ответа считаются '
                  'в токенах. Учебная модель считает токеном слово.'),
        ('max_tokens', 'Параметр запроса: сколько токенов модель может написать в ответе. Не хватило — ответ обрывается, а finish_reason '
                       'равен "length" вместо "stop".'),
        ('галлюцинация', 'Уверенный, гладкий, но выдуманный ответ модели. Модель продолжает текст правдоподобно, а не проверяет факты.'),
    ]
    body = (
        '<p>[[LLM]] не «знает» ответы, как база данных: она по кусочкам продолжает текст так, как он вероятнее всего продолжился бы. '
        'Поэтому у неё можно попросить что угодно — и поэтому она иногда уверенно врёт. Программы общаются с моделью через API: '
        'POST-запрос со списком сообщений, ключ — в заголовке. У каждого сообщения есть [[роль сообщения]] и текст — [[промпт]].</p>'
        '<p>В ИТП нет интернета, поэтому здесь работает учебная модель <code>llm.itp</code>. Она устроена как настоящие API, но отвечает '
        'по готовым правилам — одинаково на одинаковые вопросы. Настоящие модели отвечают каждый раз немного по-разному.</p>'
        + ex(ASK + '\n\ndata = ask([{"role": "user", "content": "Какая столица Франции?"}])\nprint(data["message"]["content"])\n'
             'print(data["finish_reason"], data["usage"])', files=SERVERS) +
        '<p>В <code>usage</code> — сколько [[токен]]ов ушло на вопрос и на ответ: за них платят. [[max_tokens]] ограничивает ответ сверху:</p>'
        + ex(ASK + '\n\nfor limit in [6, 100]:\n    data = ask([{"role": "user", "content": "Напиши стих про кота"}], limit)\n'
             '    print(data["finish_reason"], "|", data["message"]["content"])', files=SERVERS) +
        '<h3>Модель ничего не помнит</h3>'
        '<p>Каждый запрос — с чистого листа. Чтобы был «диалог», программа хранит историю и каждый раз отправляет её целиком: реплики '
        'user и прошлые ответы assistant. Поэтому длинный чат дорожает — история растёт.</p>'
        + ex(ASK + '\n\nhistory = []\nfor text in ["Меня зовут Вика", "Как меня зовут?"]:\n    history.append({"role": "user", "content": text})\n'
             '    answer = ask(history)["message"]["content"]\n    history.append({"role": "assistant", "content": answer})\n    print(text, "→", answer)\n\n'
             'print(ask([{"role": "user", "content": "Как меня зовут?"}])["message"]["content"])', files=SERVERS) +
        '<p>И главное правило: ответ модели — не факт, пока его не проверили. Спроси учебную модель про лучшего ученика ИТП — она '
        'назовёт имя и город, которых никто не знает. Это [[галлюцинация]].</p>'
    )
    return th('Запрос к модели', terms, body)


def fl_chat():
    return fl('Запрос к модели', [
        q('Как модель «помнит» начало разговора?', 'Программа каждый раз присылает всю историю', ['Модель хранит чаты у себя', 'По ключу API'],
          'Без истории каждый запрос — с чистого листа.'),
        q('finish_reason равен "length". Что случилось?', 'Ответ упёрся в max_tokens и оборван', ['Модель ответила полностью', 'Ключ неверный'],
          'Полный ответ — "stop".'),
        q('Для чего сообщение с ролью system?', 'Задать модели правила: тон, формат, ограничения', ['Передать ключ API', 'Сохранить ответ модели'],
          'system — инструкция, user — реплики человека.'),
        q('Модель уверенно назвала дату события. Что делать?', 'Проверить по надёжному источнику', ['Поверить: модели не ошибаются',
          'Спросить ещё раз — второй ответ точный'], 'Модель продолжает текст правдоподобно, а не проверяет факты.'),
    ])


def code_chat():
    return ts('Запрос к модели', [
        task('Спроси модель. Учебная модель отвечает на POST http://llm.itp/v1/chat с заголовком Authorization: «Bearer КЛЮЧ» и json '
             '{"model": "itp-mini", "messages": [...]}. Ответ: message (в нём content — текст) и usage (prompt_tokens, completion_tokens). '
             'На вход подаётся ключ, затем вопрос. Выведи текст ответа, затем «Токены: P + C = S». Неверный ключ (код 401) — «Неверный ключ».',
             'headers={"Authorization": "Bearer " + key}; messages — список из одного словаря {"role": "user", "content": вопрос}.',
             'import requests\n\nkey = input()\nquestion = input()\nr = requests.post("http://llm.itp/v1/chat", json={"model": "itp-mini", "messages": [{"role": "user", "content": question}]},\n'
             '                  headers={"Authorization": "Bearer " + key})\nif r.status_code == 401:\n    print("Неверный ключ")\nelse:\n    data = r.json()\n'
             '    print(data["message"]["content"])\n    p, c = data["usage"]["prompt_tokens"], data["usage"]["completion_tokens"]\n    print(f"Токены: {p} + {c} = {p + c}")',
             ['demo\nКакая столица Франции?', 'demo\nКто создал Python?', 'qwerty\nПривет'], files=SERVERS),
        task('Чат с памятью. На вход подаются реплики по одной, последняя — «стоп». Отправляй модели (http://llm.itp/v1/chat, ключ demo) всю '
             'историю: реплики user и ответы assistant. На каждую реплику выводи «> ОТВЕТ». В конце — «Сообщений в истории: N».',
             'После ответа добавь его в историю: history.append({"role": "assistant", "content": answer}).',
             ASK + '\n\nhistory = []\nwhile True:\n    text = input()\n    if text == "стоп":\n        break\n    history.append({"role": "user", "content": text})\n'
             '    answer = ask(history)["message"]["content"]\n    history.append({"role": "assistant", "content": answer})\n    print(">", answer)\n'
             'print(f"Сообщений в истории: {len(history)}")',
             ['Меня зовут Тимур\nКак меня зовут?\nстоп', 'Как меня зовут?\nМеня зовут Вика\nКак меня зовут?\nКакая столица Франции?\nстоп', 'стоп'],
             files=SERVERS),
        task('Обрезанный ответ. На вход подаётся число — max_tokens, затем вопрос. Спроси модель (http://llm.itp/v1/chat, ключ demo) с этим '
             'max_tokens и выведи ответ. Если ответ оборван (finish_reason равен "length") — допиши строку «(обрезано: нужно больше max_tokens)».',
             'max_tokens — ещё одно поле в json запроса.',
             ASK + '\n\nlimit = int(input())\ndata = ask([{"role": "user", "content": input()}], limit)\nprint(data["message"]["content"])\n'
             'if data["finish_reason"] == "length":\n    print("(обрезано: нужно больше max_tokens)")',
             ['5\nНапиши стих про кота', '50\nНапиши стих про кота', '3\nСколько будет 2+2?'], files=SERVERS),
    ])


SYS_REVIEW = 'Оцени отзыв. Ответь только JSON: {"sentiment": "positive" | "neutral" | "negative", "score": целое от 1 до 5}'


def th_json():
    terms = [
        ('структурированный вывод', 'Ответ модели в заранее заданном формате — обычно JSON с нужными полями, — чтобы его читала программа, '
                                    'а не человек.'),
        ('валидация', 'Проверка данных перед использованием: все ли поля на месте, правильного ли они типа, из допустимых ли значений.'),
        ('rfind', 'строка.rfind(подстрока) — как find, но ищет с конца: номер последнего вхождения или -1, если его нет.'),
        ('повторный запрос','Если ответ не подошёл или сервер перегружен (429, 503), запрос повторяют — с паузой, ограниченное число раз.'),
    ]
    body = (
        '<p>Человеку модель может ответить как угодно, а программе нужен порядок: «тональность отзыва — negative, оценка — 2». Поэтому в '
        'системном промпте просят [[структурированный вывод]] — JSON с описанием полей — и разбирают ответ <code>json.loads</code>.</p>'
        + ex(ASK + '\nSYSTEM = ' + json.dumps(SYS_REVIEW, ensure_ascii=False) + '\n\nfor review in ["Всё отлично!", "Нормально, но долго", "Ужасно"]:\n'
             '    answer = ask([{"role": "system", "content": SYSTEM}, {"role": "user", "content": review}])["message"]["content"]\n'
             '    print(repr(answer))', files=SERVERS) +
        '<p>Второй ответ завёрнут в <code>```json … ```</code> — модели так делают постоянно. Ещё бывает текст до JSON («Вот оценка: {…}»), '
        'выдуманные значения и числа строкой. Правило: ответ модели — непроверенные данные. Его разбирают в <code>try</code> '
        '(ошибка разбора JSON — это ValueError) и проходят [[валидация]]. Сам JSON вырезают от первой «{» до последней «}» — '
        'последнюю ищет [[rfind]]:</p>'
        + ex('import json\n\n\ndef parse(answer):\n    start, end = answer.find("{"), answer.rfind("}")\n    if start == -1 or end == -1:\n        return None\n'
             '    try:\n        data = json.loads(answer[start:end + 1])\n    except ValueError:\n        return None\n'
             '    if data.get("sentiment") not in ("positive", "neutral", "negative"):\n        return None\n'
             '    if not isinstance(data.get("score"), int) or not 1 <= data["score"] <= 5:\n        return None\n    return data\n\n\n'
             'for a in [\'```json\\n{"sentiment": "neutral", "score": 3}\\n```\', \'{"sentiment": "strange", "score": 7}\', \'{"score": "5"\', "Не знаю"]:\n'
             '    print(parse(a))') +
        '<p>Не подошло — делают [[повторный запрос]]: добавляют в историю неудачный ответ и просьбу «Ответь только JSON». Так же повторяют '
        'запрос, когда сервер ответил 429 (лимит) или 503 (перегружен), — только с растущей паузой: 1 с, 2 с, 4 с. Попыток всегда '
        'ограниченное число, иначе программа может зависнуть навсегда.</p>'
    )
    return th('Структурированный вывод', terms, body)


def fl_json():
    return fl('Структурированный вывод', [
        q('Модель вернула ```json {…} ```. Что сделает json.loads со всей строкой?', 'Упадёт с ValueError', ['Разберёт JSON внутри',
          'Вернёт None'], 'Лишние символы вокруг — уже не JSON.'),
        q('JSON разобрался. Можно сразу использовать поля?', 'Нет: сначала проверить поля, типы и значения', ['Да: раз JSON, данные верные',
          'Да, если ответ короткий'], 'Модель может выдумать значение или прислать число строкой.'),
        q('Сервер модели ответил 503. Как лучше поступить?', 'Повторить через паузу, но не бесконечно', ['Сразу повторять без пауз',
          'Сменить ключ API'], '503 — сервер перегружен, через время он ответит.'),
    ])


def code_json():
    return ts('Структурированный вывод', [
        task('Оценка отзывов. На вход подаются отзывы по одному, последняя строка — «конец». Каждый отправь модели (http://llm.itp/v1/chat, '
             'ключ demo) с системным промптом:\n' + SYS_REVIEW + '\nРазбери ответ json.loads прямо целиком. Выведи «N: SENTIMENT, SCORE» '
             '(N — номер отзыва с 1); если ответ не разобрался — «N: не JSON»; если sentiment не positive/neutral/negative или score не целое '
             'от 1 до 5 — «N: неверные поля». В конце — «Разобрано: K из M».',
             'Разбор — в try … except ValueError. Целое ли число — isinstance(x, int).',
             'import json\n' + ASK + '\nSYSTEM = ' + json.dumps(SYS_REVIEW, ensure_ascii=False) + '\n\nn = ok = 0\nwhile True:\n    review = input()\n    if review == "конец":\n        break\n    n += 1\n'
             '    answer = ask([{"role": "system", "content": SYSTEM}, {"role": "user", "content": review}])["message"]["content"]\n    try:\n'
             '        data = json.loads(answer)\n    except ValueError:\n        print(f"{n}: не JSON")\n        continue\n'
             '    s = data.get("sentiment")\n    score = data.get("score")\n    if s not in ("positive", "neutral", "negative") or not isinstance(score, int) or not 1 <= score <= 5:\n'
             '        print(f"{n}: неверные поля")\n        continue\n    ok += 1\n    print(f"{n}: {s}, {score}")\nprint(f"Разобрано: {ok} из {n}")',
             ['Всё отлично, спасибо\nУжасно медленно\nНормально\nконец', 'Странно, но работает\nВкусно!\nСломалось через день\nКто вы?\nконец', 'конец'],
             files=SERVERS),
        task('Достань JSON. Напиши функцию extract_json(text): найди в тексте кусок от первой «{» до последней «}» и разбери его json.loads. '
             'Верни словарь; если скобок нет, кусок не разбирается или получился не словарь — верни None.',
             'find("{") и rfind("}"); если любой из них -1 или конец раньше начала — None. Разбор — в try … except ValueError.',
             'import json\n\n\ndef extract_json(text):\n    start, end = text.find("{"), text.rfind("}")\n    if start == -1 or end < start:\n        return None\n'
             '    try:\n        data = json.loads(text[start:end + 1])\n    except ValueError:\n        return None\n    return data if isinstance(data, dict) else None\n',
             ['print(extract_json(\'{"a": 1}\'))\nprint(extract_json(\'```json\\n{"ok": true, "n": [1, 2]}\\n```\'))',
              'print(extract_json("Вот: {\\"x\\": \\"y\\"} — готово"))\nprint(extract_json("без скобок"))\nprint(extract_json("{сломано}"))\nprint(extract_json("} {"))'],
             tail=TL),
        task('Повтор при перегрузке. Сервер http://busy.llm.itp/v1/chat (ключ demo) сначала отвечает 429, потом 503 и только третьим запросом — 200. '
             'На вход подаётся наибольшее число попыток и вопрос. Делай попытки по порядку и выводи «попытка K: КОД». После неудачной попытки, '
             'если попытки ещё есть, выводи «пауза S с» (S = 1, затем 2, 4… — удваивается; ждать по-настоящему не нужно). Получил 200 — выведи '
             'текст ответа. Попытки кончились — «Сдаюсь после N попыток».',
             'for k in range(1, tries + 1); после 200 — break; else у цикла сработает, если break не было.',
             'import requests\n\ntries = int(input())\nquestion = input()\npause = 1\nfor k in range(1, tries + 1):\n'
             '    r = requests.post("http://busy.llm.itp/v1/chat", json={"messages": [{"role": "user", "content": question}]}, headers={"Authorization": "Bearer demo"})\n'
             '    print(f"попытка {k}: {r.status_code}")\n    if r.status_code == 200:\n        print(r.json()["message"]["content"])\n        break\n'
             '    if k < tries:\n        print(f"пауза {pause} с")\n        pause *= 2\nelse:\n    print(f"Сдаюсь после {tries} попыток")',
             ['3\nКакая столица Франции?', '2\nКакая столица Франции?', '5\nСколько будет 2+2?'], files=SERVERS),
    ])


SYS_TICKET = ('Ты сортируешь заявки поддержки. Ответь только JSON: {"category": "доступ" | "оплата" | "сбой" | "отзыв", "urgent": true | false}')


def project():
    return pj('Сортировщик заявок',
              'Поддержка получает заявки, а модель раскладывает их по категориям. На вход подаются заявки по одной, последняя строка — «конец». '
              'Каждую отправь модели (http://llm.itp/v1/chat, ключ demo) отдельным разговором с системным промптом:\n' + SYS_TICKET + '\n'
              'Ответ разбери: JSON может быть завёрнут в ```json … ``` — бери кусок от первой «{» до последней «}». Если ответ не разобрался, '
              'повтори один раз: добавь в историю ответ модели (assistant) и реплику user «Ответь только JSON.». Не помогло — категория '
              '«не разобрано». Если category не из четырёх в промпте — «другое».\n'
              'Выводи «N. КАТЕГОРИЯ» и « !», если urgent истинно (N — номер заявки с 1). Затем «Категории: …» — «категория×K» через запятую '
              'с пробелом по алфавиту, «Срочные: номера через запятую с пробелом» (или «Срочные: нет») и «Токенов: T» — сумма prompt_tokens и '
              'completion_tokens всех запросов, включая повторные.',
              'Функция ask(messages) возвращает (текст, потрачено токенов); функция parse(text) — словарь или None\n'
              'Повтор: messages + [{"role": "assistant", "content": text}, {"role": "user", "content": "Ответь только JSON."}]\n'
              'Подсчёт категорий — Counter, вывод — sorted(counts.items())',
              'import json\nfrom collections import Counter\nimport requests\n\nSYSTEM = ' + json.dumps(SYS_TICKET, ensure_ascii=False) + '\n'
              'CATEGORIES = ("доступ", "оплата", "сбой", "отзыв")\ntokens = 0\n\n\ndef ask(messages):\n    global tokens\n'
              '    r = requests.post("http://llm.itp/v1/chat", json={"messages": messages}, headers={"Authorization": "Bearer demo"})\n    data = r.json()\n'
              '    tokens += data["usage"]["prompt_tokens"] + data["usage"]["completion_tokens"]\n    return data["message"]["content"]\n\n\n'
              'def parse(text):\n    start, end = text.find("{"), text.rfind("}")\n    if start == -1 or end < start:\n        return None\n    try:\n'
              '        data = json.loads(text[start:end + 1])\n    except ValueError:\n        return None\n    return data if isinstance(data, dict) else None\n\n\n'
              'counts = Counter()\nurgent = []\nn = 0\nwhile True:\n    ticket = input()\n    if ticket == "конец":\n        break\n    n += 1\n'
              '    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": ticket}]\n    answer = ask(messages)\n    data = parse(answer)\n'
              '    if data is None:\n        data = parse(ask(messages + [{"role": "assistant", "content": answer}, {"role": "user", "content": "Ответь только JSON."}]))\n'
              '    if data is None:\n        category, hot = "не разобрано", False\n    else:\n        category = data.get("category")\n'
              '        if category not in CATEGORIES:\n            category = "другое"\n        hot = data.get("urgent") is True\n'
              '    counts[category] += 1\n    if hot:\n        urgent.append(str(n))\n    print(f"{n}. {category}" + (" !" if hot else ""))\n'
              'print("Категории:", ", ".join(f"{c}×{k}" for c, k in sorted(counts.items())))\nprint("Срочные:", ", ".join(urgent) or "нет")\nprint(f"Токенов: {tokens}")',
              ['Не могу войти, забыл пароль\nНе прошла оплата картой\nСайт не открывается\nСпасибо за быстрый ответ!\nконец',
               'СРОЧНО всё упало\nХочу больше котиков в приложении\nЧто-то странное\nПароль не подходит\nконец',
               'конец'], files=SERVERS)


def build():
    return topic('LLM API: модель по запросу', 'промпты, роли, токены, JSON-ответы', [
        th_chat(), fl_chat(), code_chat(),
        th_json(), fl_json(), code_json(),
        project(),
    ], opt=True)
