import json
from dsl import *

# Нора после «Итоговые проекты»: бот-синоптик — API погоды + учебный мессенджер + расписание «пн 07:00» в поясе собеседника.
# Ждать неделю в задаче нельзя, поэтому время в задачах «модельное»: у сообщений есть дата (поле date, как в Telegram), конец
# проверки задаётся вводом, а рассылки срабатывают между сообщениями — дискретная симуляция. Настоящий цикл со sleep — код для компьютера.
# Две теории: время, часовые пояса и следующий запуск; бот по расписанию (симуляция событий, настройки чата). Мини-проект — бот-синоптик.

DAYS = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
WEEK = {
    'Тюмень': [(-6, -2, 'снег'), (-8, -4, 'ясно'), (-5, -1, 'облачно'), (-3, 0, 'снег'), (-7, -3, 'ясно'), (-9, -5, 'ясно'), (-4, -1, 'облачно')],
    'Сочи': [(9, 15, 'ясно'), (10, 16, 'ясно'), (8, 13, 'дождь'), (7, 12, 'дождь'), (9, 14, 'облачно'), (11, 17, 'ясно'), (10, 15, 'ясно')],
    'Калининград': [(2, 6, 'дождь'), (1, 5, 'облачно'), (0, 4, 'облачно'), (3, 7, 'дождь'), (2, 5, 'ветер'), (1, 4, 'облачно'), (0, 3, 'ясно')],
    'Владивосток': [(-2, 4, 'ясно'), (-4, 2, 'ветер'), (-3, 3, 'ясно'), (-1, 5, 'облачно'), (-5, 0, 'снег'), (-6, -1, 'ясно'), (-3, 2, 'ясно')],
}
WEATHER = {'api.weather.itp': {'routes': {'/week': {'param': 'city', 'variants': {
    c: {'city': c, 'days': [{'day': DAYS[i], 'min': a, 'max': b, 'sky': s} for i, (a, b, s) in enumerate(w)]} for c, w in WEEK.items()}}}}}


def chat(updates, weather=True):
    spec = {'bot.itp': {'routes': {}, 'bot': {'token': 'bot-demo', 'updates': [
        {'update_id': i, 'message': {'chat_id': c, 'from': n, 'text': t, 'date': d}} for i, (d, c, n, t) in enumerate(updates, 1)]}}}
    if weather:
        spec.update(WEATHER)
    return {'_itp_servers.json': json.dumps(spec, ensure_ascii=False)}


MINI = chat([('2026-11-02T06:00:00+00:00', 7, 'Аня', '/start'), ('2026-11-02T06:05:00+00:00', 9, 'Zed', 'привет')], weather=False)
SETUP = chat([('2026-11-02T06:00:00+00:00', 7, 'Аня', '/settings'), ('2026-11-02T06:01:00+00:00', 7, 'Аня', '/tz +5'),
              ('2026-11-02T06:02:00+00:00', 9, 'Zed', '/time сб 10:30'), ('2026-11-02T06:03:00+00:00', 7, 'Аня', '/time пн 7:00'),
              ('2026-11-02T06:04:00+00:00', 7, 'Аня', '/tz +20'), ('2026-11-02T06:05:00+00:00', 9, 'Zed', '/tz -4'),
              ('2026-11-02T06:06:00+00:00', 9, 'Zed', '/time пт 25:00'), ('2026-11-02T06:07:00+00:00', 7, 'Аня', '/settings'),
              ('2026-11-02T06:08:00+00:00', 9, 'Zed', '/settings')], weather=False)
FORECAST = chat([('2026-11-02T06:00:00+00:00', 7, 'Аня', '/forecast Тюмень'), ('2026-11-02T06:01:00+00:00', 9, 'Zed', '/forecast Атлантида'),
                 ('2026-11-02T06:02:00+00:00', 12, 'Вика', '/forecast'), ('2026-11-02T06:03:00+00:00', 12, 'Вика', '/forecast Сочи')])
PROJECT = chat([('2026-11-01T10:00:00+00:00', 7, 'Аня', '/next'), ('2026-11-01T10:01:00+00:00', 7, 'Аня', '/city Тюмень'),
                ('2026-11-01T10:02:00+00:00', 7, 'Аня', '/tz +5'), ('2026-11-01T18:00:00+00:00', 9, 'Zed', '/city Сочи'),
                ('2026-11-01T18:01:00+00:00', 9, 'Zed', '/time вс 21:30'), ('2026-11-02T05:00:00+00:00', 12, 'Вика', '/city Атлантида'),
                ('2026-11-03T09:00:00+00:00', 7, 'Аня', '/next'), ('2026-11-03T09:01:00+00:00', 7, 'Аня', '/time ср 08:00'),
                ('2026-11-03T09:02:00+00:00', 7, 'Аня', '/next'), ('2026-11-05T12:00:00+00:00', 9, 'Zed', '/stop'),
                ('2026-11-05T12:01:00+00:00', 9, 'Zed', '/next'), ('2026-11-05T12:02:00+00:00', 12, 'Вика', '/tz +10'),
                ('2026-11-05T12:03:00+00:00', 12, 'Вика', '/city Владивосток'), ('2026-11-05T12:04:00+00:00', 12, 'Вика', '/time пт 9:00'),
                ('2026-11-05T12:05:00+00:00', 12, 'Вика', 'спасибо'), ('2026-11-05T12:06:00+00:00', 9, 'Zed', '/city'),
                ('2026-11-05T12:07:00+00:00', 9, 'Zed', '/stop')])

LOOP = ('import time\nfrom datetime import datetime, timezone\n\nwhile True:\n    now = datetime.now(timezone.utc)   # настоящее время, а не модельное\n'
        '    send_due(now)                       # разослать всё, чему пора\n    handle_updates()                    # ответить на новые сообщения\n'
        '    time.sleep(20)                      # и подождать: рассылка опоздает максимум на 20 секунд')
ZONE = ('from datetime import datetime\nfrom zoneinfo import ZoneInfo\n\nnow = datetime.now(ZoneInfo("Asia/Yekaterinburg"))   # Тюмень, UTC+5\n'
        'print(now.strftime("%H:%M"), now.tzname())\n# ZoneInfo знает переходы на летнее время: «Europe/Berlin» зимой UTC+1, летом UTC+2')

NEXT_RUN = ('def next_run(now, hours, day, hhmm):\n    """ближайший момент «день ЧЧ:ММ» по местному времени пояса UTC+hours, строго позже now"""\n'
            '    local = now.astimezone(timezone(timedelta(hours=hours)))\n    h, m = map(int, hhmm.split(":"))\n'
            '    target = local.replace(hour=h, minute=m, second=0, microsecond=0)\n    target += timedelta(days=(DAYS.index(day) - local.weekday()) % 7)\n'
            '    if target <= local:\n        target += timedelta(days=7)\n    return target\n')


def th_time():
    terms = [
        ('часовой пояс', 'Сдвиг местного времени от UTC: Москва — UTC+3, Тюмень — UTC+5, Нью-Йорк зимой — UTC-5. Одно и то же мгновение '
                         'в разных поясах — разные часы, а иногда и разные дни.'),
        ('UTC', 'Всемирное координированное время — «нулевой» пояс. Серверы хранят и сравнивают время в UTC, а местное показывают только людям.'),
        ('timezone', 'datetime.timezone(timedelta(hours=5)) — пояс с постоянным сдвигом UTC+5; timezone.utc — сам UTC. Время с поясом '
                     'называют «осведомлённым»: его можно сравнивать с временем в другом поясе.'),
        ('astimezone', 'момент.astimezone(пояс) — тот же момент на часах другого пояса: datetime в UTC 04:00 → 09:00 в UTC+5.'),
        ('fromisoformat', 'datetime.fromisoformat("2026-11-02 04:30+00:00") — время из строки ISO; +00:00 в конце — пояс.'),
    ]
    body = (
        '<p>Бот, который присылает прогноз «по понедельникам в 7:00», должен понимать: 7:00 у кого? В Калининграде и во Владивостоке 7 утра '
        'наступает с разницей в 8 часов. Каждый [[часовой пояс]] — это сдвиг от [[UTC]]. Серверы считают время в UTC, а в местное переводят '
        'только для людей. Пояс в Python — [[timezone]], а перевести момент на часы другого пояса — [[astimezone]]:</p>'
        + ex('from datetime import datetime, timedelta, timezone\n\nnow = datetime.fromisoformat("2026-11-02 04:30+00:00")\nDAYS = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]\n'
             'for city, hours in [("Калининград", 2), ("Москва", 3), ("Тюмень", 5), ("Владивосток", 10), ("Нью-Йорк", -5)]:\n'
             '    local = now.astimezone(timezone(timedelta(hours=hours)))\n    print(f"{city:12} UTC{hours:+d}  {DAYS[local.weekday()]} {local.strftime(\'%H:%M\')}")') +
        '<p>[[fromisoformat]] читает время из строки, а <code>+00:00</code> в её конце — это пояс. Обрати внимание на Нью-Йорк: там ещё воскресенье. '
        'Поэтому день недели считают по местному времени, а не по UTC. <code>{hours:+d}</code> печатает число со знаком: +5, -5.</p>'
        '<h3>Когда следующая рассылка</h3>'
        '<p>Расписание собеседник задаёт по своим часам: «пн 07:00». Чтобы найти ближайший такой момент, переводим «сейчас» в его пояс, '
        'ставим нужные часы и сдвигаемся вперёд до нужного дня недели. Если момент уже прошёл — плюс неделя:</p>'
        + ex('from datetime import datetime, timedelta, timezone\n\nDAYS = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]\n\n\n' + NEXT_RUN + '\n\n'
             'for s in ["2026-11-02 01:00+00:00", "2026-11-02 02:00+00:00", "2026-11-05 15:20+00:00"]:\n    now = datetime.fromisoformat(s)\n'
             '    t = next_run(now, 5, "пн", "07:00")\n    print(s, "→", t.strftime("%Y-%m-%d %H:%M"), "| UTC:", t.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M"))') +
        '<p>В 02:00 UTC в Тюмени ровно 7:00 понедельника — этот момент уже наступил (<code>target &lt;= local</code>), значит, следующая рассылка '
        'через неделю. Время с поясом можно сравнивать с любым другим временем с поясом: Python сам приведёт их к UTC.</p>'
        '<p>У постоянного сдвига есть ограничение: в странах с летним временем сдвиг меняется дважды в год. На компьютере для этого есть модуль '
        'zoneinfo с базой поясов по именам:</p>'
        '<pre class="pc">' + ZONE + '</pre>'
    )
    return th('Время и часовые пояса', terms, body)


def fl_time():
    return fl('Время и часовые пояса', [
        q('В UTC 22:00 воскресенья. Какой день во Владивостоке (UTC+10)?', 'Понедельник, 08:00', ['Воскресенье, 22:00', 'Воскресенье, 12:00'],
          '22 + 10 = 32 часа — это 8 утра следующего дня.'),
        q('В каком поясе сервер хранит время рассылок?', 'В UTC', ['В поясе того, кто написал первым', 'В поясе сервера, как удобно'],
          'UTC одинаково для всех; местное — только для показа.'),
        q('Рассылка «пн 07:00», сейчас ровно пн 07:00, и эта рассылка уже ушла. Когда следующая?', 'Через неделю', ['Прямо сейчас и через неделю', 'Завтра'],
          'Момент уже наступил: строгое «позже» отбрасывает его.'),
        qo('Что выведет программа?', 'from datetime import datetime, timedelta, timezone\n\nt = datetime.fromisoformat("2026-11-02 23:30+00:00")\n'
           'print(t.astimezone(timezone(timedelta(hours=3))).strftime("%d %H:%M"))', ['02 23:30', '03 23:30', '02 20:30'], '23:30 + 3 часа = 02:30 следующего дня.'),
    ])


def code_time():
    return ts('Время и часовые пояса', [
        task('Часы мира. Первая строка ввода — момент в UTC «ГГГГ-ММ-ДД ЧЧ:ММ», вторая — сдвиги поясов через пробел (+3, -5, 10…). Для каждого, '
             'в порядке ввода, выведи «UTC+N: ДЕНЬ ЧЧ:ММ» (день — пн, вт, … по местному времени; 0 печатается как «UTC+0»), а затем «Другой день: K» — во скольких '
             'поясах местная дата не совпадает с датой в UTC.',
             'Момент: datetime.fromisoformat(строка + "+00:00"). Сдвиг: int("+3") == 3; со знаком — f"{h:+d}".',
             'from datetime import datetime, timedelta, timezone\n\nDAYS = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]\nnow = datetime.fromisoformat(input() + "+00:00")\n'
             'other = 0\nfor h in map(int, input().split()):\n    local = now.astimezone(timezone(timedelta(hours=h)))\n'
             '    print(f"UTC{h:+d}: {DAYS[local.weekday()]} {local.strftime(\'%H:%M\')}")\n    if local.date() != now.date():\n        other += 1\nprint(f"Другой день: {other}")',
             ['2026-11-02 04:30\n+3 +5 -5 +10 0', '2026-12-31 22:15\n+2 +3 +14 -10'], ex_=None),
        task('Следующая рассылка. На вход подаются: момент сейчас в UTC «ГГГГ-ММ-ДД ЧЧ:ММ», сдвиг пояса собеседника и расписание «ДЕНЬ ЧЧ:ММ». '
             'Найди ближайшую рассылку строго позже «сейчас» и выведи «Местное сейчас: ДЕНЬ ГГГГ-ММ-ДД ЧЧ:ММ», «Рассылка: ДЕНЬ ГГГГ-ММ-ДД ЧЧ:ММ (UTC+N)», '
             '«В UTC: ГГГГ-ММ-ДД ЧЧ:ММ» и «Ждать: Д д Ч ч М мин» (все три числа, даже нули). Пояс печатай со знаком: UTC+0, UTC-5.',
             'Функция next_run из теории. Ожидание — разность (target - now): .days и .seconds // 3600, (.seconds % 3600) // 60.',
             'from datetime import datetime, timedelta, timezone\n\nDAYS = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]\n\n\n' + NEXT_RUN + '\n\n'
             'def show(t):\n    return f"{DAYS[t.weekday()]} {t.strftime(\'%Y-%m-%d %H:%M\')}"\n\n\nnow = datetime.fromisoformat(input() + "+00:00")\nhours = int(input())\n'
             'day, hhmm = input().split()\nlocal = now.astimezone(timezone(timedelta(hours=hours)))\ntarget = next_run(now, hours, day, hhmm)\nwait = target - now\n'
             'print(f"Местное сейчас: {show(local)}")\nprint(f"Рассылка: {show(target)} (UTC{hours:+d})")\n'
             'print(f"В UTC: {target.astimezone(timezone.utc).strftime(\'%Y-%m-%d %H:%M\')}")\n'
             'print(f"Ждать: {wait.days} д {wait.seconds // 3600} ч {wait.seconds % 3600 // 60} мин")',
             ['2026-11-02 04:30\n5\nпн 07:00', '2026-11-01 23:00\n3\nпн 07:00', '2026-11-04 12:00\n-5\nср 07:00']),
        task('Расписание рассылок. Первая строка — начало и конец проверки в UTC «ГГГГ-ММ-ДД ЧЧ:ММ ГГГГ-ММ-ДД ЧЧ:ММ» (4 слова), вторая — число чатов N, '
             'дальше N строк «ИМЯ СДВИГ ДЕНЬ ЧЧ:ММ». Выведи все рассылки строго позже начала и не позже конца, по времени UTC (при равенстве — по имени, как сравнивает строки Python): '
             '«ГГГГ-ММ-ДД ЧЧ:ММ UTC — ИМЯ (местное ДЕНЬ ЧЧ:ММ)», а затем «Всего: K».',
             'Для каждого чата: t = next_run(start, …); пока t <= end — записать и t = next_run(t, …). Сортировать пары (время, имя).',
             'from datetime import datetime, timedelta, timezone\n\nDAYS = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]\n\n\n' + NEXT_RUN + '\n\n'
             'a, b, c, d = input().split()\nstart = datetime.fromisoformat(f"{a} {b}+00:00")\nend = datetime.fromisoformat(f"{c} {d}+00:00")\nsends = []\n'
             'for _ in range(int(input())):\n    name, hours, day, hhmm = input().split()\n    t = next_run(start, int(hours), day, hhmm)\n    while t <= end:\n'
             '        sends.append((t.astimezone(timezone.utc), name, f"{DAYS[t.weekday()]} {t.strftime(\'%H:%M\')}"))\n        t = next_run(t, int(hours), day, hhmm)\n'
             'for t, name, local in sorted(sends):\n    print(f"{t.strftime(\'%Y-%m-%d %H:%M\')} UTC — {name} (местное {local})")\nprint(f"Всего: {len(sends)}")',
             ['2026-11-01 00:00 2026-11-15 00:00\n3\nАня +5 пн 07:00\nZed -5 вс 20:00\nВика +10 пн 07:00', '2026-11-02 02:00 2026-11-03 00:00\n2\nГлеб +5 пн 07:00\nБорис +3 пн 07:00']),
    ])


def th_bot():
    terms = [
        ('рассылка по расписанию', 'Сообщение, которое бот отправляет сам, без запроса, когда наступает время из расписания. Бот хранит для каждого '
                                   'чата момент следующей рассылки и раз за разом проверяет, не пора ли.'),
        ('симуляция времени', 'Проверка логики без ожидания: вместо настоящих часов программа идёт по «модельному» времени — дате каждого сообщения — '
                              'и запускает рассылки, которые наступили между сообщениями.'),
        ('date сообщения', 'Время отправки сообщения в ответе getUpdates. В учебном мессенджере — строка ISO с поясом, её читает fromisoformat; '
                           'в Telegram — число секунд с 1970 года.'),
    ]
    body = (
        '<h3>Учебный мессенджер bot.itp — коротко</h3>'
        '<p>Бот в ИТП переписывается через учебный мессенджер <code>http://bot.itp</code> (подробно он разобран в норе «Чат-боты»). Два запроса, '
        'оба с параметром <code>token</code>: <code>GET /getUpdates?token=…&amp;offset=N</code> отдаёт <code>{"ok": true, "result": [обновления]}</code>, '
        'у обновления — <code>update_id</code> и <code>message</code> с <code>chat_id</code>, <code>from</code>, <code>text</code> и <code>date</code>; '
        '<code>POST /sendMessage?token=…</code> с <code>json={"chat_id": …, "text": …}</code> отправляет ответ. offset — номер последнего '
        'обработанного обновления плюс один: так бот не получит одно сообщение дважды:</p>'
        + ex('import requests\n\nAPI, TOKEN = "http://bot.itp", "bot-demo"\nupdates = requests.get(f"{API}/getUpdates", params={"token": TOKEN}).json()["result"]\n'
             'for u in updates:\n    m = u["message"]\n    print(u["update_id"], m["chat_id"], m["from"], m["text"], m["date"])\n'
             '    requests.post(f"{API}/sendMessage", params={"token": TOKEN}, json={"chat_id": m["chat_id"], "text": "Принято!"})\n'
             'again = requests.get(f"{API}/getUpdates", params={"token": TOKEN, "offset": updates[-1]["update_id"] + 1}).json()["result"]\n'
             'print("новых:", len(again))', files=MINI) +
        '<p>Поэтому у задач с ботом в примере нет «Вход»: программа ничего не читает с клавиатуры — сообщения ей присылает сервер мессенджера, '
        'а проверка смотрит на то, что бот ответил.</p>'
        '<h3>Рассылка в цикле</h3>'
        '<p>Настоящий бот с [[рассылка по расписанию|рассылкой по расписанию]] — вечный цикл: посмотреть на часы, разослать всё, чему пора, ответить '
        'на новые сообщения, подождать. Вот его скелет для компьютера:</p>'
        '<pre class="pc">' + LOOP + '</pre>'
        '<p>Проверять такого бота неделю никто не будет. Поэтому логику пишут так, чтобы «сейчас» передавалось в функции, а не бралось из часов. '
        'Тогда работает [[симуляция времени]]: берём сообщения по порядку, у каждого есть [[date сообщения]], и перед ответом на него запускаем '
        'рассылки, которые наступили до этого момента:</p>'
        + ex('from datetime import datetime, timedelta, timezone\n\nDAYS = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]\n\n\n' + NEXT_RUN + '\n\n'
             'chats = {7: {"name": "Аня", "tz": 5, "day": "пн", "time": "07:00"}, 9: {"name": "Zed", "tz": -5, "day": "вс", "time": "20:00"}}\n'
             'start = datetime.fromisoformat("2026-11-01 00:00+00:00")\nfor c in chats.values():\n    c["next"] = next_run(start, c["tz"], c["day"], c["time"])\n\n\n'
             'def send_due(now):\n    while True:\n        due = [(c["next"], cid) for cid, c in chats.items() if c["next"] <= now]\n'
             '        if not due:\n            return\n        t, cid = min(due)\n        c = chats[cid]\n'
             '        print(t.astimezone(timezone.utc).strftime("%m-%d %H:%M UTC"), "→", c["name"], "прогноз")\n'
             '        c["next"] = next_run(t, c["tz"], c["day"], c["time"])\n\n\n'
             'for when, cid, text in [("2026-11-01 12:00", 9, "привет"), ("2026-11-02 03:00", 7, "что с погодой?")]:\n'
             '    now = datetime.fromisoformat(when + "+00:00")\n    send_due(now)\n    print(when, "←", chats[cid]["name"], text)\n'
             'send_due(datetime.fromisoformat("2026-11-09 12:00+00:00"))') +
        '<p>Рассылка Ани (пн 07:00 по UTC+5 = 02:00 UTC) ушла раньше её вопроса в 03:00. Рассылки идут строго по времени: send_due раз за разом берёт самую раннюю '
        'из наступивших (min по парам «время, чат»), пока такие есть, — так не перепутаются ни чаты, ни недели, если между сообщениями прошло много времени. Эта же функция send_due будет работать и в настоящем цикле — ей просто передадут настоящее «сейчас».</p>'
        '<h3>Настройки чата</h3>'
        '<p>Город, пояс и время у каждого собеседника свои: настройки — словарь по chat_id. Команда меняет настройку и сразу пересчитывает '
        'следующую рассылку от времени сообщения — иначе бот пришлёт прогноз по старому расписанию. Неправильный ввод (пояс +20, время 25:00) бот '
        'не принимает и объясняет, как надо. Вот пересчёт после смены пояса:</p>'
        + ex('from datetime import datetime, timedelta, timezone\n\nDAYS = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]\n\n\n' + NEXT_RUN + '\n\n'
             'def set_tz(c, hours, now):\n    c["tz"] = hours\n    if c["city"]:                    # рассылка включена — пересчитать от «сейчас»\n'
             '        c["next"] = next_run(now, c["tz"], c["day"], c["time"])\n    return f"Пояс: UTC{hours:+d}"\n\n\n'
             'now = datetime.fromisoformat("2026-11-02 01:00+00:00")\nc = {"city": "Тюмень", "tz": 3, "day": "пн", "time": "07:00"}\n'
             'c["next"] = next_run(now, c["tz"], c["day"], c["time"])\nprint("было:", c["next"].astimezone(timezone.utc).strftime("%m-%d %H:%M UTC"))\n'
             'print(set_tz(c, 5, now))\nprint("стало:", c["next"].astimezone(timezone.utc).strftime("%m-%d %H:%M UTC"))') +
        '<p>Расписание «пн 07:00» осталось тем же, но 7 утра по UTC+5 наступает на 2 часа раньше по UTC. В Telegram то же делают готовые планировщики: JobQueue в python-telegram-bot, cron на сервере — но '
        'внутри у них та же идея «следующий момент запуска».</p>'
    )
    return th('Бот по расписанию', terms, body)


def fl_bot():
    return fl('Бот по расписанию', [
        q('Зачем передавать «сейчас» в функцию, а не брать из часов внутри?', 'Так логику можно проверить без ожидания', ['Так бот работает быстрее',
          'Иначе datetime не работает'], 'В проверке «сейчас» — модельное время.'),
        q('Собеседник с расписанием «пн 07:00» по своим часам сменил пояс с +3 на +5. Что сделать с рассылкой?', 'Пересчитать следующий запуск от текущего момента', ['Ничего, она в UTC',
          'Отправить прогноз прямо сейчас'], 'Иначе «пн 07:00» наступит по старым часам.'),
        q('Зачем send_due каждый раз берёт min из наступивших рассылок?', 'Чтобы рассылки шли по времени, а не по чатам', ['min быстрее перебора',
          'Чтобы отправить только одну рассылку'], 'Наступить могли рассылки разных чатов и разных недель.'),
    ])


def code_bot():
    return ts('Бот по расписанию', [
        task('Настройки. Учебный мессенджер http://bot.itp (токен bot-demo; getUpdates — сообщения с chat_id, from, text и date). Настройки чата по '
             'умолчанию: пояс +3, расписание «пн 07:00». Команды: «/tz N» — пояс, целое от -12 до +14 (иначе «Пояс — целое число от -12 до +14»), '
             'ответ «Пояс: UTC+N» (со знаком: UTC+5, UTC-4, UTC+0); «/time ДЕНЬ ЧЧ:ММ» — день из пн…вс и время с часами 0–23 и минутами 0–59, можно «7:00» (иначе «Пиши так: /time пн 07:00»), '
             'ответ «Расписание: ДЕНЬ ЧЧ:ММ» с двумя цифрами часов и минут (7:5 → 07:05; день — строчными, ровно два слова после команды); «/settings» — '
             '«Пояс UTC+N, прогноз ДЕНЬ ЧЧ:ММ». На другие сообщения бот не отвечает. Ответ отправляй sendMessage и выводи его «→ CHAT_ID: ТЕКСТ».',
             'Проверка времени: часы и минуты через split(":"), оба .isdigit(), затем диапазоны. Красиво: f"{h:02d}:{m:02d}".\n'
             'int("+5") работает; проверка целого со знаком: (s[1:] if s[0] in "+-" else s).isdigit().',
             'import requests\n\nAPI, TOKEN = "http://bot.itp", "bot-demo"\nDAYS = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]\nsettings = {}\n\n\n'
             'def parse_time(args):\n    if len(args) != 2 or args[0] not in DAYS or ":" not in args[1]:\n        return None\n    h, m = args[1].split(":", 1)\n'
             '    if not (h.isdigit() and m.isdigit() and int(h) < 24 and int(m) < 60):\n        return None\n    return args[0], f"{int(h):02d}:{int(m):02d}"\n\n\n'
             'def reply(cid, text):\n    sent = requests.post(f"{API}/sendMessage", params={"token": TOKEN}, json={"chat_id": cid, "text": text}).json()["result"]\n'
             '    print(f"→ {sent[\'chat_id\']}: {sent[\'text\']}")\n\n\nfor u in requests.get(f"{API}/getUpdates", params={"token": TOKEN}).json()["result"]:\n'
             '    m = u["message"]\n    cid = m["chat_id"]\n    s = settings.setdefault(cid, {"tz": 3, "day": "пн", "time": "07:00"})\n    cmd, *args = m["text"].split()\n'
             '    if cmd == "/tz":\n        ok = len(args) == 1 and (args[0][1:] if args[0][0] in "+-" else args[0]).isdigit() and -12 <= int(args[0]) <= 14\n        if ok:\n'
             '            s["tz"] = int(args[0])\n            reply(cid, f"Пояс: UTC{s[\'tz\']:+d}")\n        else:\n            reply(cid, "Пояс — целое число от -12 до +14")\n'
             '    elif cmd == "/time":\n        t = parse_time(args)\n        if t:\n            s["day"], s["time"] = t\n            reply(cid, f"Расписание: {t[0]} {t[1]}")\n'
             '        else:\n            reply(cid, "Пиши так: /time пн 07:00")\n    elif cmd == "/settings":\n'
             '        reply(cid, f"Пояс UTC{s[\'tz\']:+d}, прогноз {s[\'day\']} {s[\'time\']}")',
             [''], files=SETUP),
        task('Прогноз на неделю. Сервис погоды http://api.weather.itp/week?city=ГОРОД отдаёт {"city": …, "days": [{"day": "пн", "min": -6, "max": -2, '
             '"sky": "снег"}, …]} — 7 дней, неизвестный город — 404. Бот в мессенджере http://bot.itp (токен bot-demo) отвечает на «/forecast ГОРОД» '
             'одним сообщением (город — всё после команды, как написал собеседник): первая строка «Прогноз: ГОРОД», дальше по дню «ДЕНЬ: MIN…MAX, НЕБО» (числа со знаком: «-6…-2», «+9…+15»; ноль — «+0»), '
             'последняя — «Теплее всего: ДЕНЬ» (наибольший max, первый из равных). Без города — «Напиши город: /forecast Сочи», неизвестный — '
             '«Не знаю город ГОРОД». Выводи ответы «→ CHAT_ID: ТЕКСТ».',
             'Строки собери списком и соедини "\\n".join(lines). Знак: f"{d[\'min\']:+}".',
             'import requests\n\nAPI, TOKEN = "http://bot.itp", "bot-demo"\n\n\ndef forecast(city):\n'
             '    r = requests.get("http://api.weather.itp/week", params={"city": city})\n    if r.status_code == 404:\n        return f"Не знаю город {city}"\n'
             '    days = r.json()["days"]\n    lines = [f"Прогноз: {city}"]\n    for d in days:\n        lines.append(f"{d[\'day\']}: {d[\'min\']:+}…{d[\'max\']:+}, {d[\'sky\']}")\n'
             '    warm = max(days, key=lambda d: d["max"])\n    lines.append(f"Теплее всего: {warm[\'day\']}")\n    return "\\n".join(lines)\n\n\n'
             'for u in requests.get(f"{API}/getUpdates", params={"token": TOKEN}).json()["result"]:\n    m = u["message"]\n    cmd, *args = m["text"].split()\n'
             '    text = forecast(" ".join(args)) if args else "Напиши город: /forecast Сочи"\n'
             '    sent = requests.post(f"{API}/sendMessage", params={"token": TOKEN}, json={"chat_id": m["chat_id"], "text": text}).json()["result"]\n'
             '    print(f"→ {sent[\'chat_id\']}: {sent[\'text\']}")',
             [''], files=FORECAST),
    ])


def project():
    return pj('Бот-синоптик',
              'Бот присылает прогноз на неделю по расписанию. Мессенджер http://bot.itp (токен bot-demo; у сообщений есть date — время в ISO с поясом), '
              'погода — http://api.weather.itp/week?city=ГОРОД (как в задаче «Прогноз на неделю»). Настройки чата по умолчанию: города нет, пояс +3, '
              'расписание «пн 07:00». Команды:\n'
              '— «/city ГОРОД» — проверить город в сервисе погоды (нет — «Не знаю город ГОРОД», без города — «Напиши город: /city Сочи») и включить рассылку: «Город: ГОРОД. Прогноз — ДЕНЬ ЧЧ:ММ (UTC+N)»;\n'
              '— «/tz N» и «/time ДЕНЬ ЧЧ:ММ» — как в задаче «Настройки», с теми же ответами и проверками;\n'
              '— «/next» — «Следующий прогноз: ДЕНЬ ГГГГ-ММ-ДД ЧЧ:ММ (UTC+N)» по местному времени, или «Рассылка выключена. Включи: /city ГОРОД», если города нет;\n'
              '— «/stop» — выключить рассылку (город забыть): «Рассылка выключена» — тот же ответ, если она уже выключена;\n'
              '— всё остальное — «Команды: /city, /tz, /time, /next, /stop».\n'
              'После любой смены города, пояса или времени (если город выбран) следующая рассылка пересчитывается от даты сообщения — строго позже неё; '
              'при ошибке настройки не меняются, «/stop» забывает только город (пояс и расписание остаются). '
              'Перед ответом на каждое сообщение и в конце (момент конца — строка ввода «ГГГГ-ММ-ДД ЧЧ:ММ» в UTC) бот рассылает наступившие прогнозы '
              '(момент рассылки не позже даты сообщения или конца; прогноз каждый раз запрашивается у сервиса) '
              'по времени рассылки (при равенстве — по возрастанию chat_id): текст как в «Прогнозе на неделю», первая строка — «Прогноз: ГОРОД». '
              'Выводи каждое отправленное сообщение строкой «[ГГГГ-ММ-ДД ЧЧ:ММ UTC] → CHAT_ID: ТЕКСТ» (время — в UTC): время ответа — дата сообщения, время рассылки — её момент.',
              'Настройки — словарь chat_id → {"city", "tz", "day", "time", "next"}; next — время с поясом или None\n'
              'send_due(now): пока есть наступившие — взять самую раннюю min((next, chat_id)), отправить и next = next_run(next, …)\n'
              'Модельное «сейчас» сообщения — datetime.fromisoformat(m["date"])',
              'import requests\nfrom datetime import datetime, timedelta, timezone\n\nAPI, TOKEN = "http://bot.itp", "bot-demo"\nDAYS = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]\n'
              'HELP = "Команды: /city, /tz, /time, /next, /stop"\nchats = {}\n\n\n' + NEXT_RUN + '\n\n'
              'def utc(t):\n    return t.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M")\n\n\ndef send(cid, text, when):\n'
              '    sent = requests.post(f"{API}/sendMessage", params={"token": TOKEN}, json={"chat_id": cid, "text": text}).json()["result"]\n'
              '    print(f"[{utc(when)} UTC] → {sent[\'chat_id\']}: {sent[\'text\']}")\n\n\ndef forecast(city):\n'
              '    days = requests.get("http://api.weather.itp/week", params={"city": city}).json()["days"]\n    lines = [f"Прогноз: {city}"]\n'
              '    for d in days:\n        lines.append(f"{d[\'day\']}: {d[\'min\']:+}…{d[\'max\']:+}, {d[\'sky\']}")\n    warm = max(days, key=lambda d: d["max"])\n'
              '    lines.append(f"Теплее всего: {warm[\'day\']}")\n    return "\\n".join(lines)\n\n\ndef send_due(now):\n    while True:\n        due = [(c["next"], cid) for cid, c in chats.items() if c["next"] and c["next"] <= now]\n'
              '        if not due:\n            return\n        t, cid = min(due)\n        c = chats[cid]\n        send(cid, forecast(c["city"]), t)\n'
              '        c["next"] = next_run(t, c["tz"], c["day"], c["time"])\n\n\ndef parse_time(args):\n'
              '    if len(args) != 2 or args[0] not in DAYS or ":" not in args[1]:\n        return None\n    h, m = args[1].split(":", 1)\n'
              '    if not (h.isdigit() and m.isdigit() and int(h) < 24 and int(m) < 60):\n        return None\n    return args[0], f"{int(h):02d}:{int(m):02d}"\n\n\n'
              'def handle(c, cmd, args, now):\n    if cmd == "/city":\n        if not args:\n            return "Напиши город: /city Сочи"\n        city = " ".join(args)\n'
              '        if requests.get("http://api.weather.itp/week", params={"city": city}).status_code == 404:\n            return f"Не знаю город {city}"\n'
              '        c["city"] = city\n        reply = f"Город: {city}. Прогноз — {c[\'day\']} {c[\'time\']} (UTC{c[\'tz\']:+d})"\n'
              '    elif cmd == "/tz":\n        if not (len(args) == 1 and (args[0][1:] if args[0][0] in "+-" else args[0]).isdigit() and -12 <= int(args[0]) <= 14):\n'
              '            return "Пояс — целое число от -12 до +14"\n        c["tz"] = int(args[0])\n        reply = f"Пояс: UTC{c[\'tz\']:+d}"\n'
              '    elif cmd == "/time":\n        t = parse_time(args)\n        if not t:\n            return "Пиши так: /time пн 07:00"\n        c["day"], c["time"] = t\n'
              '        reply = f"Расписание: {t[0]} {t[1]}"\n    elif cmd == "/next":\n        if not c["next"]:\n            return "Рассылка выключена. Включи: /city ГОРОД"\n'
              '        t = c["next"]\n        return f"Следующий прогноз: {DAYS[t.weekday()]} {t.strftime(\'%Y-%m-%d %H:%M\')} (UTC{c[\'tz\']:+d})"\n'
              '    elif cmd == "/stop":\n        c["city"], c["next"] = None, None\n        return "Рассылка выключена"\n    else:\n        return HELP\n'
              '    if c["city"]:\n        c["next"] = next_run(now, c["tz"], c["day"], c["time"])\n    return reply\n\n\n'
              'end = datetime.fromisoformat(input() + "+00:00")\nfor u in requests.get(f"{API}/getUpdates", params={"token": TOKEN}).json()["result"]:\n'
              '    m = u["message"]\n    now = datetime.fromisoformat(m["date"])\n    send_due(now)\n'
              '    c = chats.setdefault(m["chat_id"], {"city": None, "tz": 3, "day": "пн", "time": "07:00", "next": None})\n    cmd, *args = m["text"].split()\n'
              '    send(m["chat_id"], handle(c, cmd, args, now), now)\nsend_due(end)',
              ['2026-11-12 00:00'], files=PROJECT)


def build():
    return topic('Бот-синоптик: прогноз по расписанию', 'часовые пояса, расписание, симуляция времени', [
        th_time(), fl_time(), code_time(),
        th_bot(), fl_bot(), code_bot(),
        project(),
    ], opt=True)
