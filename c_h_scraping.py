import json
from dsl import *

# Нора после «Итоговые проекты»: парсинг страниц. Учебные сайты живут в учебном requests (маршруты "html" и "text" в _itp_servers.json),
# одна страница — файлом рядом с программой. HTML разбирает BeautifulSoup (пакет Pyodide bs4: dsl.py гонит такой код через Pyodide, PYO_RE).
# Две теории: HTML-дерево и BeautifulSoup; этика, robots.txt и обход страниц. Мини-проект — монитор цен в двух магазинах.


def site(addr, pages, robots=None, more=None):
    routes = {p: {'html': h} for p, h in pages.items()}
    if robots is not None:
        routes['/robots.txt'] = {'text': robots}
    spec = {addr: {'routes': routes}}
    spec.update(more or {})
    return spec


def files(*specs):
    d = {}
    for s in specs:
        d.update(s)
    return {'_itp_servers.json': json.dumps(d, ensure_ascii=False)}


NEWS = ('<html><head><title>Школьные новости</title></head><body>\n<h1>Новости 9 «Б»</h1>\n'
        '<article class="news"><h2><a href="/news/robot">Команда собрала робота-сортировщика</a></h2><span class="date">2026-10-28</span>'
        '<p>Робот раскладывает детали конструктора по цветам.</p></article>\n'
        '<article class="ad"><h2>Курсы пиксель-арта со скидкой</h2></article>\n'
        '<article class="news"><h2><a href="/news/chess">Шахматный турнир: три победы подряд</a></h2><span class="date">2026-10-30</span>'
        '<p>Тимур выиграл все партии.</p></article>\n'
        '<article class="news"><h2><a href="/news/garden">Огород на крыше дал урожай</a></h2><span class="date">2026-10-21</span>'
        '<p>Собрали 12 кг томатов.</p></article>\n'
        '<article class="news"><h2><a href="/news/game">Кружок выпустил свою игру про ферму</a></h2><span class="date">2026-11-01</span>'
        '<p>Скачать можно на сайте кружка.</p></article>\n</body></html>\n')

SHOP = ('<html><head><title>Пиксель-маркет</title></head><body>\n<h1>Цены на технику</h1>\n<table class="prices">\n'
        '<tr><th>Товар</th><th>Цена</th><th>Наличие</th></tr>\n'
        '<tr><td class="name">Клавиатура «Неон»</td><td class="price">2 490 ₽</td><td>есть</td></tr>\n'
        '<tr><td class="name">Мышь «Призрак»</td><td class="price">1 150 ₽</td><td>есть</td></tr>\n'
        '<tr><td class="name">Наушники «Метро»</td><td class="price">3 990 ₽</td><td>нет</td></tr>\n'
        '<tr><td class="name">Коврик «Ферма»</td><td class="price">490 ₽</td><td>есть</td></tr>\n'
        '<tr><td class="name">Геймпад «Рыцарь»</td><td class="price">4 200 ₽</td><td>есть</td></tr>\n'
        '<tr><td class="name">Веб-камера «Глаз»</td><td class="price">2 990 ₽</td><td>нет</td></tr>\n'
        '</table>\n</body></html>\n')

TEAM = ('<html><body><nav><a href="/">Главная</a> <a href="/team/">Команда</a> <a href="#top">Наверх</a></nav>\n'
        '<ul class="people"><li><a href="anya.html">Аня</a></li><li><a href="timur.html">Тимур</a></li><li><a href="/team/anya.html">Аня (ещё раз)</a></li></ul>\n'
        '<p>Пишите: <a href="mailto:club@club.itp">почта</a>. Наш код — <a href="https://git.example.org/club">на гитхабе</a>, '
        'видео — <a href="https://video.example.org/c/club">на канале</a>.</p></body></html>\n')
EVENTS = ('<html><body><h1>События</h1><a href="../">Назад</a> <a href="2026/hackathon.html">Хакатон</a> <a href="2026/lan.html">Турнир по сети</a> '
          '<a href="http://club.itp/team/">Команда</a> <a href="https://tickets.example.org/lan">Билеты</a></body></html>\n')
CLUB = files(site('club.itp', {'/team/index.html': TEAM, '/events/index.html': EVENTS}))
NEWSSITE = files(site('news.itp', {'/': NEWS}))
SHOPSITE = files(site('shop.itp', {'/prices': SHOP}))

ROBOTS = 'User-agent: *\nDisallow: /admin/\nDisallow: /cart\nCrawl-delay: 2\n\nUser-agent: greedy-bot\nDisallow: /\n'


def cat_page(n, items, last):
    rows = ''.join(f'<div class="card"><span class="title">{t}</span> <b class="price">{p}</b></div>\n' for t, p in items)
    nxt = '' if last else f'<a class="next" href="/catalog/{n + 1}">Дальше →</a>'
    return f'<html><body><h1>Каталог, страница {n}</h1>\n{rows}{nxt}</body></html>\n'


CAT = [[('Стикеры «Кролик»', 150), ('Значок «Пиксель»', 90), ('Кружка «Python»', 590)],
       [('Футболка «Hello, world»', 1290), ('Блокнот «Баг-трекер»', 350)],
       [('Плед «Кибер»', 2100), ('Брелок «Морковка»', 120), ('Постер «Ферма»', 400), ('Носки «Ошибка 404»', 300)]]
CATSITE = files(site('merch.itp', {f'/catalog/{i + 1}': cat_page(i + 1, c, i == len(CAT) - 1) for i, c in enumerate(CAT)}, ROBOTS))
CATSITE2 = files(site('merch.itp', {f'/catalog/{i + 1}': cat_page(i + 1, c, i == len(CAT) - 1) for i, c in enumerate(CAT)},
                      'User-agent: *\nDisallow: /catalog/3\nCrawl-delay: 5\n'))
SITES = files(site('a.itp', {'/': '<p>Главная</p>'}, ROBOTS), site('b.itp', {'/': '<p>Главная</p>'}, 'User-agent: itp-bot\nDisallow: /private\n\nUser-agent: *\nDisallow: /\n'))


def shop_a():
    rows = [('Клавиатура «Неон»', '2 490 ₽'), ('Мышь «Призрак»', '1 150 ₽'), ('Наушники «Метро»', '3 990 ₽'), ('Коврик «Ферма»', '490 ₽')]
    body = ''.join(f'<li class="item"><span class="name">{n}</span> — <span class="price">{p}</span></li>' for n, p in rows)
    return f'<html><body><ul class="goods">{body}</ul></body></html>\n'


def shop_b():
    rows = [('Мышь «Призрак»', 990), ('Клавиатура «Неон»', 2590), ('Геймпад «Рыцарь»', 3900), ('Коврик «Ферма»', 490)]
    body = ''.join(f'<tr><td>{n}</td><td data-price="{p}">{p} руб.</td></tr>' for n, p in rows)
    return f'<html><body><table id="list"><tr><th>Товар</th><th>Цена</th></tr>{body}</table></body></html>\n'


PRICES = files(site('neon.itp', {'/goods': shop_a()}, 'User-agent: *\nDisallow: /admin/\n'),
               {'pixel.itp': {'routes': {'/list': {'html': shop_b()}, '/robots.txt': {'text': 'User-agent: *\nDisallow: /list\n'},
                                         '/api/prices': {'json': {'Мышь «Призрак»': 990, 'Клавиатура «Неон»': 2590, 'Геймпад «Рыцарь»': 3900,
                                                                  'Коврик «Ферма»': 490}}}}},
               site('cyber.itp', {'/shop': '<html><body><div class="p"><h3>Наушники «Метро»</h3><i>3 500 ₽</i></div>'
                                           '<div class="p"><h3>Мышь «Призрак»</h3><i>1 090 ₽</i></div>'
                                           '<div class="p"><h3>Клавиатура «Неон»</h3><i>2 390 ₽</i></div></body></html>\n'}, 'User-agent: *\nCrawl-delay: 3\n'))


def th_soup():
    terms = [
        ('парсинг', 'Разбор текста по правилам, чтобы достать из него данные. Парсинг сайтов — достать из HTML-страницы нужное: цены, заголовки, ссылки.'),
        ('HTML', 'Язык разметки страниц. Страница — дерево тегов: <h1>заголовок</h1>, <a href="…">ссылка</a>. '
                 'У тега бывают атрибуты: href, class, id.'),
        ('bs4', 'Пакет BeautifulSoup для разбора HTML. На компьютере: pip install beautifulsoup4, в ИТП подгружается сам.'),
        ('BeautifulSoup', 'BeautifulSoup(html, "html.parser") — разобрать страницу в дерево. soup.title, soup.find(…), soup.find_all(…), soup.select(…) — '
                          'поиск в дереве.'),
        ('find_all', 'soup.find_all("a") — список всех тегов a; find_all("div", class_="card") — только с таким классом (class_ с подчёркиванием: '
                     'class — слово Python). find — первый подходящий тег или None.'),
        ('get_text', 'tag.get_text(strip=True) — текст тега и всех вложенных, без пробелов по краям. Атрибут — tag["href"] или tag.get("href").'),
        ('select', 'soup.select("CSS-селектор") — теги по селектору, как в CSS: "table.prices tr", "ul.people a", "#list td". select_one — первый такой тег.'),
        ('select_one', 'soup.select_one("селектор") — первый тег по селектору или None.'),
        ('urljoin', 'from urllib.parse import urljoin; urljoin(адрес_страницы, href) — полный адрес ссылки: относительный путь достраивается от адреса страницы.'),
    ]
    body = (
        '<p>Не у каждого сайта есть API. Тогда данные берут прямо со страницы — это [[парсинг]]. Страница — это текст на языке [[HTML]]: '
        'теги вложены друг в друга, как папки, и образуют дерево. Разбирать его руками или регулярными выражениями — мучение, поэтому берут '
        'пакет [[bs4]] с классом [[BeautifulSoup]]. Учебный сайт школьных новостей живёт по адресу <code>http://news.itp</code>:</p>'
        + ex('import requests\nfrom bs4 import BeautifulSoup\n\nhtml = requests.get("http://news.itp/").text\nsoup = BeautifulSoup(html, "html.parser")\n'
             'print(soup.title.string)\nprint(soup.find("h1").get_text())\nfor art in soup.find_all("article", class_="news"):\n'
             '    link = art.find("a")\n    date = art.find("span", class_="date").get_text()\n    print(date, link.get_text(), link["href"])', files=NEWSSITE) +
        '<p>[[find_all]] возвращает все подходящие теги, find — первый. У каждого найденного тега можно снова искать внутри, а [[get_text]] '
        'отдаёт его текст. Реклама с классом ad в список не попала: искали только class_="news".</p>'
        '<h3>CSS-селекторы</h3>'
        '<p>Цепочку «внутри article.news найди h2, внутри него a» короче записать селектором, как в CSS: точка — класс, решётка — id, пробел — '
        '«где-то внутри». Это делают [[select]] и [[select_one]]:</p>'
        + ex('import requests\nfrom bs4 import BeautifulSoup\n\nsoup = BeautifulSoup(requests.get("http://shop.itp/prices").text, "html.parser")\n'
             'for row in soup.select("table.prices tr")[1:]:\n    name, price, stock = [td.get_text(strip=True) for td in row.find_all("td")]\n'
             '    rub = int(price.replace("₽", "").replace(" ", ""))\n    print(f"{name}: {rub} ({stock})")\n'
             'print("Первая цена на странице:", soup.select_one(".price").get_text())', files=SHOPSITE) +
        '<p>Первая строка таблицы — заголовки th, поэтому её пропускаем срезом. Цены на сайтах пишут для людей («2 490 ₽»), и почти всегда их надо '
        'чистить, прежде чем считать. Страницу не обязательно скачивать: HTML из файла разбирается так же — <code>BeautifulSoup(open("news.html", '
        'encoding="utf-8").read(), "html.parser")</code>.</p>'
    )
    return th('HTML и BeautifulSoup', terms, body)


def fl_soup():
    return fl('HTML и BeautifulSoup', [
        q('Чем find отличается от find_all?', 'find — первый подходящий тег, find_all — список всех', ['find ищет текст, find_all — теги',
          'Ничем'], 'Не нашлось — find вернёт None, find_all — пустой список.'),
        q('Почему пишут class_="news", а не class="news"?', 'class — зарезервированное слово Python', ['Так требует HTML', 'Это другой атрибут'],
          'Подчёркивание обходит запрет.'),
        q('Что найдёт soup.select("ul.people a")?', 'Ссылки внутри списка ul с классом people', ['Только первый ul', 'Все теги с классом a'],
          'Пробел в селекторе — «где-то внутри».'),
        q('Как достать адрес ссылки link?', 'link["href"] или link.get("href")', ['link.get_text()', 'link.find("href")'],
          'get_text — видимый текст ссылки, а не адрес.'),
    ])


def code_soup():
    return ts('HTML и BeautifulSoup', [
        task('Свежие новости. Рядом с программой лежит страница news.html. На вход подаётся дата ГГГГ-ММ-ДД. Выведи новости (только article с классом '
             'news) не раньше этой даты, от новых к старым, строками «ДАТА | ЗАГОЛОВОК», а затем «Найдено: N из M» (M — всего новостей). Реклама '
             'не новость.',
             'Даты в виде ГГГГ-ММ-ДД сравниваются и сортируются как строки. Пары (дата, заголовок) — sorted(…, reverse=True).',
             'from bs4 import BeautifulSoup\n\nsince = input()\nwith open("news.html", encoding="utf-8") as f:\n    soup = BeautifulSoup(f.read(), "html.parser")\n'
             'news = []\nfor art in soup.find_all("article", class_="news"):\n    news.append((art.find("span", class_="date").get_text(), art.find("a").get_text()))\n'
             'fresh = sorted([n for n in news if n[0] >= since], reverse=True)\nfor date, title in fresh:\n    print(f"{date} | {title}")\n'
             'print(f"Найдено: {len(fresh)} из {len(news)}")',
             ['2026-10-25', '2026-11-02', '2000-01-01'], files={'news.html': NEWS}),
        task('Бюджет. Таблица цен — на странице http://shop.itp/prices (таблица с классом prices: товар, цена вида «2 490 ₽», наличие «есть»/«нет»). '
             'На вход подаётся бюджет в рублях. Выведи товары в наличии, которые укладываются в бюджет, от дешёвых к дорогим — «ТОВАР: ЦЕНА», а '
             'затем «Можно купить: N» или, если таких нет, «Ничего не подходит». Последней строкой — «Нет в наличии: ТОВАРЫ» через запятую в порядке таблицы.',
             'Строки — soup.select("table.prices tr")[1:]; ячейки — row.find_all("td"). Цена: price.replace("₽", "").replace(" ", "").',
             'import requests\nfrom bs4 import BeautifulSoup\n\nbudget = int(input())\nsoup = BeautifulSoup(requests.get("http://shop.itp/prices").text, "html.parser")\n'
             'ok, missing = [], []\nfor row in soup.select("table.prices tr")[1:]:\n    name, price, stock = [td.get_text(strip=True) for td in row.find_all("td")]\n'
             '    rub = int(price.replace("₽", "").replace(" ", ""))\n    if stock != "есть":\n        missing.append(name)\n    elif rub <= budget:\n'
             '        ok.append((rub, name))\nfor rub, name in sorted(ok):\n    print(f"{name}: {rub}")\nprint(f"Можно купить: {len(ok)}" if ok else "Ничего не подходит")\n'
             'print("Нет в наличии:", ", ".join(missing))',
             ['2500', '300', '10000'], files=SHOPSITE),
        task('Ссылки. На сайте клуба http://club.itp две страницы: /team/index.html и /events/index.html. На вход подаётся путь страницы. Собери её ссылки '
             'и переведи в полные адреса через urljoin(адрес страницы, href) — относительные «anya.html» и «../» он достроит сам. Ссылки '
             '«#…» и «mailto:» пропусти. Выведи внутренние адреса (на club.itp) по алфавиту без повторов, а затем «Внешних: N» — сколько разных ссылок ведёт '
             'на другие сайты.',
             'Сайт адреса — urlsplit(url).netloc. Без повторов — множество, затем sorted.',
             'from urllib.parse import urljoin, urlsplit\nimport requests\nfrom bs4 import BeautifulSoup\n\npage = "http://club.itp" + input()\n'
             'soup = BeautifulSoup(requests.get(page).text, "html.parser")\ninner, outer = set(), set()\nfor a in soup.find_all("a"):\n    href = a["href"]\n'
             '    if href.startswith("#") or href.startswith("mailto:"):\n        continue\n    url = urljoin(page, href)\n'
             '    if urlsplit(url).netloc == "club.itp":\n        inner.add(url)\n    else:\n        outer.add(url)\nfor url in sorted(inner):\n'
             '    print(url)\nprint(f"Внешних: {len(outer)}")',
             ['/team/index.html', '/events/index.html'], files=CLUB),
    ])


def th_robots():
    terms = [
        ('robots.txt', 'Файл в корне сайта (/robots.txt) с правилами для роботов: каким программам и какие разделы обходить нельзя. Закон его не '
                       'требует, но вежливый парсер его читает и слушается.'),
        ('User-agent', 'Строка robots.txt: для какого робота правила ниже. * — для всех, у кого нет своего блока.'),
        ('Disallow', 'Строка robots.txt: путь, который роботу обходить нельзя. Disallow: / — весь сайт.'),
        ('Crawl-delay', 'Строка robots.txt: сколько секунд ждать между запросами к сайту.'),
        ('RobotFileParser', 'urllib.robotparser.RobotFileParser — разбор robots.txt: rp.parse(строки), rp.can_fetch(имя_робота, адрес) — можно ли, '
                            'rp.crawl_delay(имя_робота) — пауза или None.'),
        ('splitlines', 'текст.splitlines() — список строк текста без символов перевода строки. Нужен, когда функция ждёт строки по одной.'),
        ('parse','rp.parse(text.splitlines()) — загрузить в RobotFileParser строки robots.txt.'),
        ('can_fetch', 'rp.can_fetch("itp-bot", url) — True, если роботу с таким именем этот адрес обходить разрешено.'),
        ('crawl_delay', 'rp.crawl_delay("itp-bot") — сколько секунд ждать между запросами (None — правило не задано).'),
    ]
    body = (
        '<p>Парсер — это робот, который ходит по чужому сайту. Сайт платит за каждый запрос, поэтому у парсинга есть правила приличия:</p>'
        '<ul><li>сначала поищи API или готовый файл с данными — это проще и честнее;</li>'
        '<li>прочитай условия сайта: некоторые прямо запрещают сбор данных;</li>'
        '<li>не трогай личные данные людей (имена, телефоны, профили) — собирать их без согласия нельзя и по закону;</li>'
        '<li>не торопись: пауза между запросами, никаких сотен запросов в секунду;</li>'
        '<li>представляйся: в заголовке User-Agent напиши имя своего робота;</li>'
        '<li>слушайся [[robots.txt]].</li></ul>'
        '<p>robots.txt лежит в корне сайта. Блок начинается строкой [[User-agent]] — имя робота, а строки [[Disallow]] перечисляют запрещённые '
        'пути. [[Crawl-delay]] просит паузу между запросами. Разбирать его руками не нужно: в Python есть [[RobotFileParser]]:</p>'
        + ex('import requests\nfrom urllib.robotparser import RobotFileParser\n\ntext = requests.get("http://merch.itp/robots.txt").text\nprint(text)\n'
             'rp = RobotFileParser()\nrp.parse(text.splitlines())\nfor path in ["/catalog/1", "/admin/users", "/cart?id=7"]:\n'
             '    print(path, rp.can_fetch("itp-bot", "http://merch.itp" + path))\nprint("пауза:", rp.crawl_delay("itp-bot"))\n'
             'print("жадному боту:", rp.can_fetch("greedy-bot", "http://merch.itp/catalog/1"))', files=CATSITE) +
        '<p>[[parse]] загружает строки, [[can_fetch]] отвечает «можно или нет» для конкретного робота и адреса, [[crawl_delay]] — какую паузу '
        'держать. У itp-bot своего блока нет, поэтому для него действуют правила «*»; greedy-bot сайт закрыл целиком.</p>'
        '<h3>Обход нескольких страниц</h3>'
        '<p>Каталоги делят на страницы, и на каждой есть ссылка «Дальше». Парсер идёт по ним, пока ссылка есть. Ссылка обычно относительная — '
        'полный адрес собирает <code>urljoin</code>. Перед каждым запросом спрашиваем robots.txt, а между запросами настоящий парсер ждёт '
        '<code>time.sleep(пауза)</code> (здесь вместо паузы печатаем её, чтобы не ждать):</p>'
        + ex('from urllib.parse import urljoin\nimport requests\nfrom bs4 import BeautifulSoup\nfrom urllib.robotparser import RobotFileParser\n\n'
             'rp = RobotFileParser()\nrp.parse(requests.get("http://merch.itp/robots.txt").text.splitlines())\nurl = "http://merch.itp/catalog/1"\n'
             'while url and rp.can_fetch("itp-bot", url):\n    soup = BeautifulSoup(requests.get(url, headers={"User-Agent": "itp-bot"}).text, "html.parser")\n'
             '    print(soup.h1.get_text(), "— товаров:", len(soup.select(".card")))\n    nxt = soup.select_one("a.next")\n'
             '    url = urljoin(url, nxt["href"]) if nxt else None\n    if url:\n        print(f"  (ждём {rp.crawl_delay(\'itp-bot\')} с)")',
             files=CATSITE) +
        '<p>Сначала скачай одну страницу и посмотри на её HTML — так проще понять, какие теги и классы искать. А сайты меняют вёрстку, поэтому '
        'парсер однажды сломается: проверяй, что find не вернул None.</p>'
    )
    return th('Этика и robots.txt', terms, body)


def fl_robots():
    return fl('Этика и robots.txt', [
        q('У сайта есть открытый API с теми же данными. Что выбрать?', 'API — это проще и честнее', ['Парсинг — он всегда точнее',
          'Оба сразу, чтобы сравнить'], 'Парсинг — когда другого способа нет.'),
        q('В robots.txt: «User-agent: *» и «Disallow: /admin/». Можно ли роботу на /admin/users?', 'Нельзя', ['Можно', 'Можно, если сайт открылся'],
          'Disallow запрещает путь и всё внутри.'),
        q('Что значит «Crawl-delay: 5»?', 'Ждать 5 секунд между запросами', ['Не больше 5 запросов', 'Запрет на 5 страниц'],
          'Пауза бережёт сервер сайта.'),
        q('Какие данные нельзя собирать парсером без согласия людей?', 'Личные: имена, телефоны, профили', ['Цены товаров', 'Заголовки новостей'],
          'Это защищено законом о персональных данных.'),
        qo('Что выведет программа?', 'from urllib.parse import urljoin\nprint(urljoin("http://a.itp/blog/post.html", "img/cat.png"))',
           ['http://a.itp/img/cat.png', 'img/cat.png', 'http://a.itp/blog/post.html/img/cat.png'], 'Путь достраивается от папки страницы.'),
    ])


def code_robots():
    return ts('Этика и robots.txt', [
        task('Вежливый робот. На вход подаются адреса, по одному в строке. Для каждого скачай robots.txt его сайта (http://САЙТ/robots.txt; сайт — '
             'urlsplit(адрес).netloc) и выведи «АДРЕС — можно» или «АДРЕС — нельзя» для робота itp-bot. robots.txt каждого сайта скачивай один раз. '
             'В конце — «Скачано robots.txt: N».',
             'Разобранные robots.txt храни в словаре сайт → RobotFileParser.',
             'import sys\nfrom urllib.parse import urlsplit\nimport requests\nfrom urllib.robotparser import RobotFileParser\n\nparsers = {}\nfor line in sys.stdin:\n'
             '    url = line.strip()\n    host = urlsplit(url).netloc\n    if host not in parsers:\n        rp = RobotFileParser()\n'
             '        rp.parse(requests.get(f"http://{host}/robots.txt").text.splitlines())\n        parsers[host] = rp\n'
             '    print(url, "—", "можно" if parsers[host].can_fetch("itp-bot", url) else "нельзя")\nprint(f"Скачано robots.txt: {len(parsers)}")',
             ['http://a.itp/\nhttp://a.itp/admin/stats\nhttp://b.itp/news\nhttp://b.itp/private/x\nhttp://a.itp/cart',
              'http://b.itp/\nhttp://b.itp/blog'], files=SITES),
        task('Весь каталог. Магазин мерча http://merch.itp: каталог на страницах /catalog/1, /catalog/2, …, на каждой — карточки div.card с span.title '
             'и b.price, внизу — ссылка a.next на следующую страницу (на последней её нет). Обойди каталог с первой страницы, слушаясь robots.txt '
             '(робот itp-bot): запрещённую страницу не скачивай и дальше не иди. На вход подаётся слово. Выведи «Страниц: N», «Товаров: M», '
             'затем товары, в названии которых есть это слово (без учёта регистра), «НАЗВАНИЕ — ЦЕНА» по возрастанию цены, или «Ничего не нашлось».',
             'Цикл while url and rp.can_fetch(…); следующий адрес — urljoin(url, nxt["href"]).',
             'from urllib.parse import urljoin\nimport requests\nfrom bs4 import BeautifulSoup\nfrom urllib.robotparser import RobotFileParser\n\nword = input().lower()\n'
             'rp = RobotFileParser()\nrp.parse(requests.get("http://merch.itp/robots.txt").text.splitlines())\nurl = "http://merch.itp/catalog/1"\npages = 0\ngoods = []\n'
             'while url and rp.can_fetch("itp-bot", url):\n    soup = BeautifulSoup(requests.get(url).text, "html.parser")\n    pages += 1\n'
             '    for card in soup.select("div.card"):\n        goods.append((int(card.select_one(".price").get_text()), card.select_one(".title").get_text()))\n'
             '    nxt = soup.select_one("a.next")\n    url = urljoin(url, nxt["href"]) if nxt else None\nprint(f"Страниц: {pages}")\n'
             'print(f"Товаров: {len(goods)}")\nfound = sorted(g for g in goods if word in g[1].lower())\nfor price, title in found:\n    print(f"{title} — {price}")\n'
             'if not found:\n    print("Ничего не нашлось")',
             ['кибер', 'ферма', 'ракета'], files=CATSITE),
        task('Тот же обход, но владелец магазина закрыл третью страницу (другой robots.txt). Слово на входе то же, вывод тот же: «Страниц: N», '
             '«Товаров: M» и найденные товары. Программа не должна меняться — robots.txt она читает сама.',
             'Если первая задача решена честно, решение то же.',
             'from urllib.parse import urljoin\nimport requests\nfrom bs4 import BeautifulSoup\nfrom urllib.robotparser import RobotFileParser\n\nword = input().lower()\n'
             'rp = RobotFileParser()\nrp.parse(requests.get("http://merch.itp/robots.txt").text.splitlines())\nurl = "http://merch.itp/catalog/1"\npages = 0\ngoods = []\n'
             'while url and rp.can_fetch("itp-bot", url):\n    soup = BeautifulSoup(requests.get(url).text, "html.parser")\n    pages += 1\n'
             '    for card in soup.select("div.card"):\n        goods.append((int(card.select_one(".price").get_text()), card.select_one(".title").get_text()))\n'
             '    nxt = soup.select_one("a.next")\n    url = urljoin(url, nxt["href"]) if nxt else None\nprint(f"Страниц: {pages}")\n'
             'print(f"Товаров: {len(goods)}")\nfound = sorted(g for g in goods if word in g[1].lower())\nfor price, title in found:\n    print(f"{title} — {price}")\n'
             'if not found:\n    print("Ничего не нашлось")',
             ['кибер', 'а'], files=CATSITE2),
    ])


def project():
    return pj('Монитор цен',
              'Ищем, где дешевле. Три магазина, у каждого своя вёрстка:\n'
              '— http://neon.itp/goods — список ul.goods, в каждом li.item: span.name и span.price вида «2 490 ₽»;\n'
              '— http://pixel.itp/list — таблица #list: в строке две ячейки td, цена — в атрибуте data-price второй ячейки; но у магазина есть и API: '
              'http://pixel.itp/api/prices отдаёт JSON «товар → цена»;\n'
              '— http://cyber.itp/shop — блоки div.p: название в h3, цена в i вида «3 500 ₽».\n'
              'Перед тем как скачать страницу, проверь robots.txt магазина для робота itp-bot. Если страница запрещена, а у магазина есть API, '
              'возьми цены из API; если запрещена и API нет — пропусти магазин. На вход подаются названия товаров, по одному в строке. Для каждого '
              'выведи «ТОВАР: ЦЕНА в МАГАЗИН» — лучшая цена (при равенстве — магазин, который идёт раньше в списке выше; магазин — его адрес, например '
              'neon.itp) — или «ТОВАР: нигде нет». В конце — «Источники: …» — как получены данные каждого магазина, в порядке списка: «neon.itp — '
              'страница», «pixel.itp — API» или «… — пропущен», через «; ».',
              'Сделай по функции на магазин: каждая возвращает словарь «товар → цена»\nЦену «2 490 ₽» чисти: replace("₽", "").replace(" ", "")\n'
              'Атрибут: td["data-price"]',
              'import sys\nimport requests\nfrom bs4 import BeautifulSoup\nfrom urllib.robotparser import RobotFileParser\n\n\ndef rub(text):\n'
              '    return int(text.replace("₽", "").replace(" ", ""))\n\n\ndef soup_of(url):\n    return BeautifulSoup(requests.get(url).text, "html.parser")\n\n\n'
              'def neon(url):\n    return {li.select_one(".name").get_text(): rub(li.select_one(".price").get_text()) for li in soup_of(url).select("ul.goods li.item")}\n\n\n'
              'def pixel(url):\n    prices = {}\n    for row in soup_of(url).select("#list tr")[1:]:\n        name, price = row.find_all("td")\n'
              '        prices[name.get_text()] = int(price["data-price"])\n    return prices\n\n\ndef cyber(url):\n'
              '    return {p.find("h3").get_text(): rub(p.find("i").get_text()) for p in soup_of(url).select("div.p")}\n\n\n'
              'SHOPS = [("neon.itp", "/goods", neon, None), ("pixel.itp", "/list", pixel, "/api/prices"), ("cyber.itp", "/shop", cyber, None)]\n'
              'data, sources = [], []\nfor host, path, parse_page, api in SHOPS:\n    rp = RobotFileParser()\n'
              '    rp.parse(requests.get(f"http://{host}/robots.txt").text.splitlines())\n    if rp.can_fetch("itp-bot", f"http://{host}{path}"):\n'
              '        data.append((host, parse_page(f"http://{host}{path}")))\n        sources.append(f"{host} — страница")\n    elif api:\n'
              '        data.append((host, requests.get(f"http://{host}{api}").json()))\n        sources.append(f"{host} — API")\n    else:\n'
              '        sources.append(f"{host} — пропущен")\nfor line in sys.stdin:\n    item = line.strip()\n    offers = [(prices[item], host) for host, prices in data if item in prices]\n'
              '    if offers:\n        price = min(o[0] for o in offers)\n        host = [o[1] for o in offers if o[0] == price][0]\n        print(f"{item}: {price} в {host}")\n'
              '    else:\n        print(f"{item}: нигде нет")\nprint("Источники:", "; ".join(sources))',
              ['Мышь «Призрак»\nКлавиатура «Неон»\nКоврик «Ферма»\nНаушники «Метро»\nВеб-камера «Глаз»', 'Геймпад «Рыцарь»'], files=PRICES)


def build():
    return topic('Парсинг: данные со страниц', 'HTML, BeautifulSoup, robots.txt', [
        th_soup(), fl_soup(), code_soup(),
        th_robots(), fl_robots(), code_robots(),
        project(),
    ], opt=True)
