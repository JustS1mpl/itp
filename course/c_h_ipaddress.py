from dsl import *

# Нора после «Классы и объекты»: модуль ipaddress. Две теории: адреса и сети (ip_address, ip_network, маска, hosts, in,
# strict=False, ValueError); деление на подсети (subnets). Мини-проект — калькулятор подсетей.


def th_addr():
    terms = [
        ('ipaddress', 'Модуль для IP-адресов и сетей: проверяет адреса, считает маски, делит сети на части.'),
        ('ip_address', 'ipaddress.ip_address("192.168.1.10") — адрес-объект: его можно сравнивать, прибавлять к нему число, узнавать is_private. '
                       'Неверная строка — ValueError.\nПример:\nimport ipaddress\na = ipaddress.ip_address("10.0.0.255")\nprint(a + 1, a.is_private)\n'
                       'Вывод:\n10.0.1.0 True'),
        ('ip_network', 'ipaddress.ip_network("192.168.1.0/24") — сеть: адрес сети и длина префикса. Атрибуты: netmask, num_addresses, '
                       'network_address, broadcast_address. strict=False разрешает адрес с ненулевыми «хостовыми» битами.'),
        ('hosts', 'сеть.hosts() — генератор адресов, которые можно выдать устройствам: все, кроме адреса сети и широковещательного.'),
        ('префикс', 'Число после «/»: сколько первых бит адреса — номер сети. /24 — первые 24 бита общие, на устройства остаётся 8 бит, '
                    'то есть 256 адресов.'),
    ]
    body = (
        '<p>Каждое устройство в сети имеет IP-адрес. В IPv4 это 4 байта, записанные через точку: <code>192.168.1.10</code> — каждое число '
        'от 0 до 255. Модуль [[ipaddress]] понимает такие адреса как объекты, а не строки:</p>'
        + ex('import ipaddress\n\na = ipaddress.ip_address("192.168.1.10")\nprint(a, a + 5, a.is_private)\nprint(ipaddress.ip_address("8.8.8.8").is_private)\n'
             'print(ipaddress.ip_address("10.0.0.1") < ipaddress.ip_address("10.0.0.20"))\ntry:\n    ipaddress.ip_address("300.1.1.1")\nexcept ValueError as e:\n    print(e)') +
        '<p>[[ip_address]] проверяет формат за тебя: 300 не помещается в байт, и это ValueError. is_private — адрес из «домашних» диапазонов '
        '(192.168.x.x, 10.x.x.x и других), которые не видны из интернета. Сравнение адресов-объектов идёт по числам, а не по буквам, '
        'поэтому 10.0.0.1 меньше 10.0.0.20.</p>'
        '<h3>Сеть</h3>'
        '<p>Сеть записывают как адрес и [[префикс]]: <code>192.168.1.0/24</code>. Первые 24 бита общие для всех адресов сети, '
        'остальные 8 — номер устройства. [[ip_network]] знает всё про сеть:</p>'
        + ex('import ipaddress\n\nnet = ipaddress.ip_network("192.168.1.0/24")\nprint(net.netmask, net.num_addresses)\nprint(net.network_address, net.broadcast_address)\n'
             'hosts = list(net.hosts())\nprint(len(hosts), hosts[0], hosts[-1])\nprint(ipaddress.ip_address("192.168.1.77") in net, ipaddress.ip_address("192.168.2.1") in net)') +
        '<p>Первый адрес — адрес самой сети, последний — широковещательный (для сообщения всем сразу), устройствам их не выдают. '
        'Остальные даёт [[hosts]] — их 254. Оператор <code>in</code> проверяет, входит ли адрес в сеть.</p>'
        '<p>Если в записи сети «хвост» не нулевой (<code>192.168.1.77/24</code>), ip_network считает это ошибкой. Параметр '
        '<code>strict=False</code> разрешает такую запись и сам обнуляет хвост:</p>'
        + ex('import ipaddress\n\nprint(ipaddress.ip_network("192.168.1.77/24", strict=False))\ntry:\n    ipaddress.ip_network("192.168.1.77/24")\nexcept ValueError as e:\n    print(e)')
    )
    return th('Адреса и сети', terms, body)


def fl_addr():
    return fl('Адреса и сети', [
        qo('Что выведет программа?', 'import ipaddress\nprint(ipaddress.ip_network("10.0.0.0/30").num_addresses)', ['30', '2', '256'],
           'Под устройства остаётся 2 бита: 4 адреса.'),
        q('Сколько адресов можно выдать устройствам в сети /24?', '254', ['256', '255'], 'Из 256 вычитаем адрес сети и широковещательный.'),
        qo('Что выведет программа?', 'import ipaddress\nprint(ipaddress.ip_address("192.168.0.255") + 1)', ['192.168.0.256', '192.168.1.0', 'Ошибка'],
           'Байт переполнился и перенёсся в следующий: 192.168.1.0.'),
    ])


def code_addr():
    return ts('Адреса и сети', [
        task('Проверка адресов. На вход подаются строки, последняя — «стоп». Для каждой выведи «СТРОКА: частный», «СТРОКА: публичный» или '
             '«СТРОКА: не адрес».',
             'try: a = ipaddress.ip_address(s) except ValueError: не адрес. Иначе — по a.is_private.',
             'import ipaddress\n\nwhile True:\n    s = input()\n    if s == "стоп":\n        break\n    try:\n        a = ipaddress.ip_address(s)\n    except ValueError:\n'
             '        print(f"{s}: не адрес")\n        continue\n    print(f"{s}: {\'частный\' if a.is_private else \'публичный\'}")',
             ['192.168.0.15\n8.8.8.8\n10.1.2.3\n256.0.0.1\nпривет\n77.88.55.242\nстоп', '172.16.5.4\n1.1.1.1\nстоп']),
        task('Сеть по адресу. На вход подаётся адрес устройства с префиксом, например «192.168.1.77/24». Выведи строками «Сеть: …», «Маска: …», '
             '«Широковещательный: …», «Устройств: N» (сколько адресов можно выдать) и «Первый: …», «Последний: …» — первый и последний '
             'из них.',
             'net = ipaddress.ip_network(s, strict=False). Адреса для устройств — list(net.hosts()).',
             'import ipaddress\n\nnet = ipaddress.ip_network(input(), strict=False)\nhosts = list(net.hosts())\nprint(f"Сеть: {net}")\nprint(f"Маска: {net.netmask}")\n'
             'print(f"Широковещательный: {net.broadcast_address}")\nprint(f"Устройств: {len(hosts)}")\nprint(f"Первый: {hosts[0]}")\nprint(f"Последний: {hosts[-1]}")',
             ['192.168.1.77/24', '10.20.30.40/16', '172.16.0.9/29']),
    ])


def th_sub():
    terms = [
        ('subnets', 'сеть.subnets(new_prefix=n) — генератор подсетей с более длинным префиксом n: сеть делится на равные части.'),
    ]
    body = (
        '<p>Большую сеть часто делят на части: отдельно ученики, учителя, камеры. Каждая лишняя единица префикса делит сеть пополам: '
        '/24 — это две /25, четыре /26 и так далее. Делит [[subnets]]:</p>'
        + ex('import ipaddress\n\nnet = ipaddress.ip_network("192.168.10.0/24")\nfor sub in net.subnets(new_prefix=26):\n'
             '    print(sub, "устройств:", sub.num_addresses - 2)') +
        '<p>Подсеть подбирают под нужное число устройств: адресов должно хватить с учётом двух служебных. Устройств 50 — '
        'нужно минимум 52 адреса, ближайшая степень двойки — 64, это префикс /26 (32 − 6, ведь 2⁶ = 64):</p>'
        + ex('need = 50\nbits = 0\nwhile 2 ** bits - 2 < need:\n    bits += 1\nprint("префикс /" + str(32 - bits), "адресов:", 2 ** bits)') +
        '<p>Проверить, к какой подсети относится адрес, можно перебором подсетей и <code>in</code>.</p>'
    )
    return th('Подсети', terms, body)


def fl_sub():
    return fl('Подсети', [
        q('На сколько подсетей /26 делится сеть /24?', '4', ['2', '26'], 'Два лишних бита префикса — 2² = 4 части.'),
        q('Какая самая маленькая подсеть подойдёт для 100 устройств?', '/25', ['/24', '/26'], '/25 — 128 адресов, 126 устройств; /26 — только 62, а /24 больше нужного.'),
        qo('Что выведет программа?', 'import ipaddress\nnet = ipaddress.ip_network("10.0.0.0/24")\nprint(len(list(net.subnets(new_prefix=27))))',
           ['27', '4', '32'], 'Три лишних бита: 2³ = 8 подсетей.'),
    ])


def code_sub():
    return ts('Подсети', [
        task('На вход подаются сеть (например, «10.0.0.0/24») и число частей k — степень двойки, каждое в своей строке. Раздели сеть на k равных '
             'подсетей и выведи каждую строкой «ПОДСЕТЬ — устройств N». Если k больше, чем можно (подсети должны оставаться не меньше /30), '
             'выведи «Слишком много частей».',
             'Новый префикс: prefixlen + log₂ k. log₂ k найди циклом: while 2 ** extra < k: extra += 1.\nnet.prefixlen — текущий префикс.',
             'import ipaddress\n\nnet = ipaddress.ip_network(input())\nk = int(input())\nextra = 0\nwhile 2 ** extra < k:\n    extra += 1\nif net.prefixlen + extra > 30:\n'
             '    print("Слишком много частей")\nelse:\n    for sub in net.subnets(new_prefix=net.prefixlen + extra):\n        print(f"{sub} — устройств {sub.num_addresses - 2}")',
             ['10.0.0.0/24\n4', '192.168.0.0/16\n2', '172.16.0.0/28\n8']),
        task('Где адрес. Первая строка — сеть, вторая — на сколько равных подсетей её делят (степень двойки). Дальше — адреса, последняя строка '
             '«стоп». Для каждого адреса выведи «АДРЕС → ПОДСЕТЬ» или «АДРЕС → вне сети».',
             'subs = list(net.subnets(new_prefix=...)); для адреса a = ipaddress.ip_address(s) найди подсеть с a in sub.',
             'import ipaddress\n\nnet = ipaddress.ip_network(input())\nk = int(input())\nextra = 0\nwhile 2 ** extra < k:\n    extra += 1\n'
             'subs = list(net.subnets(new_prefix=net.prefixlen + extra))\nwhile True:\n    s = input()\n    if s == "стоп":\n        break\n    a = ipaddress.ip_address(s)\n'
             '    found = [sub for sub in subs if a in sub]\n    print(f"{s} → {found[0] if found else \'вне сети\'}")',
             ['192.168.1.0/24\n4\n192.168.1.5\n192.168.1.130\n192.168.2.1\n192.168.1.255\nстоп', '10.0.0.0/8\n2\n10.200.0.1\n11.0.0.1\nстоп']),
    ])


def project():
    return pj('Калькулятор подсетей',
              'Школе нужна сеть. Первая строка ввода — сеть школы (например, «10.10.0.0/22»), дальше — отделы строками «НАЗВАНИЕ УСТРОЙСТВ», '
              'последняя — «стоп». Каждому отделу выдай подсеть самого маленького подходящего размера (устройств плюс 2 служебных адреса не '
              'больше размера подсети). Выдавай подряд с начала сети, по убыванию числа устройств (при равенстве — по '
              'названию). Выведи по отделу строку «НАЗВАНИЕ: ПОДСЕТЬ (адресов A)», затем «Свободно адресов: F». Если отдел не помещается — '
              'вместо его строки «НАЗВАНИЕ: не хватает места» и переходи к следующему.',
              'Размер подсети для n устройств: наименьшая степень двойки 2 ** bits, где 2 ** bits - 2 >= n; префикс — 32 - bits\n'
              'Следующая подсеть начинается с адреса start: ipaddress.ip_network(f"{start}/{prefix}")\n'
              'Сдвиг: start = подсеть.broadcast_address + 1; подсеть влезла, если её broadcast_address <= сеть.broadcast_address\n'
              'Если подсеть больше всей сети (32 - bits меньше net.prefixlen), её и создавать не надо — места не хватает',
              'import ipaddress\n\nnet = ipaddress.ip_network(input())\ndeps = []\nwhile True:\n    s = input()\n    if s == "стоп":\n        break\n    name, n = s.split()\n'
              '    bits = 0\n    while 2 ** bits - 2 < int(n):\n        bits += 1\n    deps.append((name, int(n), bits))\ndeps.sort(key=lambda d: (-d[1], d[0]))\nstart = net.network_address\n'
              'used = 0\nfor name, n, bits in deps:\n    if 32 - bits < net.prefixlen:\n        print(f"{name}: не хватает места")\n        continue\n'
              '    sub = ipaddress.ip_network(f"{start}/{32 - bits}")\n    if sub.broadcast_address > net.broadcast_address:\n'
              '        print(f"{name}: не хватает места")\n        continue\n    print(f"{name}: {sub} (адресов {sub.num_addresses})")\n    used += sub.num_addresses\n'
              '    start = sub.broadcast_address + 1\nprint(f"Свободно адресов: {net.num_addresses - used}")',
              ['10.10.0.0/22\nученики 300\nучителя 60\nкамеры 20\nадмины 5\nстоп', '192.168.0.0/24\nзал 200\nкласс 100\nстоп', '172.16.0.0/28\nсервер 2\nвсе 1000\nстоп'])


def build():
    return topic('IP-адреса: сети и подсети', 'ipaddress, маски, подсети', [
        th_addr(), fl_addr(), code_addr(),
        th_sub(), fl_sub(), code_sub(),
        project(),
    ], opt=True)
