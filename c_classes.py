from dsl import *

# Тема 24 «Классы и объекты». Ученик знает функции, замыкания, декораторы (как @), исключения, коллекции.
# Три теории: класс, __init__, self и методы; атрибуты класса и доступ по имени (hasattr/getattr/setattr);
# скрытые атрибуты по договорённости и property.


def th_class():
    terms = [
        ('class', 'Создаёт свой тип данных — класс: шаблон, по которому делаются объекты. Внутри — методы (функции класса).\n'
                  'Пример:\nclass Dog:\n    def __init__(self, name):\n        self.name = name\n\n    def bark(self):\n        return self.name + ": гав!"\n\n'
                  'print(Dog("Шарик").bark())\nВывод:\nШарик: гав!'),
        ('__init__', 'Конструктор — метод, который Python вызывает сам при создании объекта: Класс(аргументы). В нём объекту задают начальные атрибуты. '
                     'Аргументы из скобок при создании попадают в параметры __init__ после self. Конструктор ничего не возвращает (return не нужен).'),
        ('self', 'Первый параметр каждого метода — сам объект, у которого метод вызвали. Через self.имя метод читает и меняет атрибуты '
                 'именно этого объекта. При вызове obj.метод() его не передают — Python подставляет obj сам.'),
        ('метод', 'Функция внутри класса. Вызывается через объект: obj.метод(аргументы). Методы строк и списков (upper, append) — '
                  'тоже методы встроенных классов.'),
        ('AttributeError', 'Ошибка: у объекта нет такого атрибута или метода. Чаще всего — опечатка в имени.\n'
                           'Пример:\ntry:\n    print((5).upper())\nexcept AttributeError as e:\n    print(e)\nВывод:\n\'int\' object has no attribute \'upper\''),
    ]
    body = (
        '<p>Строка умеет <code>upper()</code>, список — <code>append()</code>: в каждом значении хранятся данные и действия над ними. '
        'Такие значения называют <b>объектами</b>, а их тип — <b>классом</b>. Свой класс создаёт [[class]]:</p>'
        + ex('class Pet:\n    def __init__(self, name):\n        self.name = name\n        self.hunger = 5\n\n    def feed(self):\n        self.hunger = max(0, self.hunger - 3)\n\n'
             '    def status(self):\n        return f"{self.name}: голод {self.hunger}"\n\n\ncat = Pet("Мурка")\ndog = Pet("Бобик")\ncat.feed()\nprint(cat.status())\nprint(dog.status())') +
        '<p><code>Pet("Мурка")</code> создаёт новый объект и сразу вызывает [[__init__]] — <b>конструктор</b>, в нём объекту задают начальные '
        '<b>атрибуты</b>: переменные, которые живут внутри объекта. У каждого объекта атрибуты свои: накормили кошку — голод собаки '
        'не изменился.</p>'
        '<p>[[метод]] — функция внутри класса. Его первый параметр [[self]] — сам объект, на котором метод вызвали. Запись '
        '<code>cat.feed()</code> — это, по сути, <code>Pet.feed(cat)</code>: Python сам передаёт <code>cat</code> в <code>self</code>, '
        'и метод меняет атрибуты именно кошки.</p>'
        '<h3>Атрибуты снаружи</h3>'
        '<p>Атрибуты можно читать и менять и снаружи класса — через точку. Если атрибута нет, будет [[AttributeError]]:</p>'
        + exerr('class Pet:\n    def __init__(self, name):\n        self.name = name\n\n\ncat = Pet("Мурка")\ncat.name = "Мурёнка"\nprint(cat.name)\nprint(cat.age)') +
        '<p>Класс полезен, когда у данных есть правила: голод не уходит ниже нуля, баланс меняется только через пополнение и оплату. '
        'Правила живут в методах рядом с данными, а не разбросаны по программе.</p>'
    )
    return th('Класс и объект', terms, body)


def fl_class():
    return fl('Класс и объект', [
        qo('Что выведет программа?', 'class C:\n    def __init__(self, x):\n        self.x = x\n\n    def grow(self):\n        self.x *= 2\n\n'
           'a = C(3)\nb = C(3)\na.grow()\na.grow()\nprint(a.x, b.x)',
           ['12 12', '6 3', '3 3'], 'У каждого объекта свой x: a удвоился дважды, b не менялся.'),
        q('Что попадает в self, когда вызывают pet.feed()?', 'Сам объект pet', ['Класс Pet', 'Ничего, self нужно передать вручную'],
          'Python подставляет объект, на котором вызвали метод.'),
        q('Когда выполняется __init__?', 'Сразу при создании объекта: Pet("Мурка")',
          ['При первом вызове любого метода', 'Только если вызвать pet.__init__() вручную'], '__init__ — конструктор: задаёт новому объекту начальные атрибуты.'),
        q('Как ещё называют метод __init__?', 'Конструктор', ['Деструктор', 'Декоратор', 'Генератор'],
          'Он «конструирует» новый объект — задаёт ему начальные атрибуты.'),
    ])


def code_class():
    return ts('Класс и объект', [
        task('Напиши класс Rect — прямоугольник. Он создаётся как Rect(w, h) и умеет: area() — площадь, perimeter() — периметр, '
             'is_square() — True, если стороны равны, иначе False.',
             'В __init__: self.w = w, self.h = h. Методы читают self.w и self.h, например return self.w * self.h.',
             'class Rect:\n    def __init__(self, w, h):\n        self.w = w\n        self.h = h\n\n    def area(self):\n        return self.w * self.h\n\n'
             '    def perimeter(self):\n        return 2 * (self.w + self.h)\n\n    def is_square(self):\n        return self.w == self.h\n',
             ['r = Rect(3, 5)\nprint(r.area(), r.perimeter(), r.is_square())', 'print(Rect(4, 4).is_square(), Rect(2.5, 2).area())',
              'a = Rect(1, 2)\nb = Rect(10, 20)\nprint(a.perimeter(), b.perimeter())'], tail=TL),
        task('Напиши класс Wallet — кошелёк. Wallet(owner, balance) создаёт кошелёк, balance по умолчанию 0. Методы: deposit(amount) — '
             'пополнить; pay(amount) — заплатить, если денег хватает, и вернуть True, иначе ничего не менять и вернуть False; '
             'report() — строка «Владелец: ИМЯ, баланс: B».',
             'Параметр со значением по умолчанию: def __init__(self, owner, balance=0).\npay: if amount > self.balance: return False; '
             'иначе self.balance -= amount и return True.',
             'class Wallet:\n    def __init__(self, owner, balance=0):\n        self.owner = owner\n        self.balance = balance\n\n    def deposit(self, amount):\n'
             '        self.balance += amount\n\n    def pay(self, amount):\n        if amount > self.balance:\n            return False\n        self.balance -= amount\n'
             '        return True\n\n    def report(self):\n        return f"Владелец: {self.owner}, баланс: {self.balance}"\n',
             ['w = Wallet("Ира")\nw.deposit(500)\nprint(w.pay(200), w.pay(400))\nprint(w.report())',
              'a = Wallet("Лёша", 100)\nb = Wallet("Катя")\nprint(b.pay(1), a.pay(100))\nprint(a.report())\nprint(b.report())'], tail=TL),
        task('Питомцы. На вход подаются команды, последняя — «стоп»: «новый ИМЯ» — завести питомца (голод 5, радость 0) и вывести '
             '«Появился ИМЯ»; «корми ИМЯ» — голод уменьшается на 3, но не ниже 0, вывести «ИМЯ: голод H»; «играй ИМЯ» — голод +2, '
             'радость +1, вывести «ИМЯ: голод H, радость J»; «статус» — все питомцы в порядке появления строками «ИМЯ — голод H, радость J». '
             'Если питомца с таким именем нет — «Нет питомца ИМЯ». Имена новых питомцев не повторяются. Питомца опиши классом Pet.',
             'Класс Pet с атрибутами name, hunger, joy и методами feed() и play(). Питомцев храни в словаре по имени — порядок появления '
             'словарь сохраняет.\nКоманду разбирай так: parts = s.split(); команда — parts[0], имя — parts[1].',
             'class Pet:\n    def __init__(self, name):\n        self.name = name\n        self.hunger = 5\n        self.joy = 0\n\n    def feed(self):\n'
             '        self.hunger = max(0, self.hunger - 3)\n\n    def play(self):\n        self.hunger += 2\n        self.joy += 1\n\n\npets = {}\nwhile True:\n'
             '    s = input()\n    if s == "стоп":\n        break\n    parts = s.split()\n    cmd = parts[0]\n    if cmd == "статус":\n        for p in pets.values():\n'
             '            print(f"{p.name} — голод {p.hunger}, радость {p.joy}")\n    elif cmd == "новый":\n        pets[parts[1]] = Pet(parts[1])\n'
             '        print(f"Появился {parts[1]}")\n    elif parts[1] not in pets:\n        print(f"Нет питомца {parts[1]}")\n    elif cmd == "корми":\n'
             '        p = pets[parts[1]]\n        p.feed()\n        print(f"{p.name}: голод {p.hunger}")\n    else:\n        p = pets[parts[1]]\n        p.play()\n'
             '        print(f"{p.name}: голод {p.hunger}, радость {p.joy}")',
             ['новый Мурка\nиграй Мурка\nкорми Мурка\nкорми Мурка\nновый Рекс\nстатус\nстоп', 'корми Бобик\nновый Бобик\nиграй Бобик\nстоп']),
    ])


def th_attrs():
    terms = [
        ('атрибут класса', 'Переменная, заданная прямо в теле класса, а не через self. Она общая для всех объектов класса: '
                           'Класс.имя читает и меняет её у всех сразу.\n'
                           'Пример:\nclass Car:\n    wheels = 4\n\na = Car()\nb = Car()\nCar.wheels = 6\nprint(a.wheels, b.wheels)\nВывод:\n6 6'),
        ('hasattr', 'hasattr(obj, "имя") — True, если у объекта есть атрибут или метод с таким именем.\n'
                    'Пример:\nprint(hasattr("abc", "upper"), hasattr("abc", "push"))\nВывод:\nTrue False'),
        ('getattr', 'getattr(obj, "имя") — значение атрибута по имени-строке. С третьим аргументом getattr(obj, "имя", запасное) '
                    'вместо AttributeError возвращает запасное значение.'),
        ('setattr', 'setattr(obj, "имя", значение) — задать атрибут по имени-строке, то же, что obj.имя = значение.'),
    ]
    body = (
        '<p>Атрибуты, заданные через <code>self</code>, у каждого объекта свои. А переменная прямо в теле класса — '
        '[[атрибут класса]] — одна на всех. Удобно для общих настроек и счётчиков:</p>'
        + ex('class Player:\n    max_hp = 100\n    created = 0\n\n    def __init__(self, nick):\n        self.nick = nick\n        self.hp = Player.max_hp\n'
             '        Player.created += 1\n\n\na = Player("zed")\nb = Player("аня")\nprint(a.hp, b.hp, Player.created)') +
        '<p>Если у объекта нет своего атрибута с таким именем, Python ищет его в классе — поэтому <code>a.max_hp</code> тоже сработает. '
        'Но присваивание <code>a.max_hp = 150</code> создаст <b>свой</b> атрибут у <code>a</code>, а у класса и остальных объектов '
        'всё останется как было. Поэтому общие атрибуты меняют через имя класса: <code>Player.created += 1</code>.</p>'
        + ex('class Player:\n    max_hp = 100\n\n\na = Player()\nb = Player()\na.max_hp = 150\nPlayer.max_hp = 120\nprint(a.max_hp, b.max_hp)') +
        '<h3>Атрибут по имени-строке</h3>'
        '<p>Иногда имя атрибута известно только во время работы — например, его ввёл пользователь. Для этого есть [[hasattr]], '
        '[[getattr]] и [[setattr]]:</p>'
        + ex('class Settings:\n    def __init__(self):\n        self.volume = 70\n        self.theme = "тёмная"\n\n\ns = Settings()\nname = "volume"\n'
             'print(hasattr(s, name), getattr(s, name))\nsetattr(s, name, 30)\nprint(s.volume)\nprint(getattr(s, "lang", "не задано"))') +
        '<p>У <code>getattr</code> третий аргумент — запасное значение на случай, если атрибута нет: так обходятся без try/except.</p>'
    )
    return th('Атрибуты класса и доступ по имени', terms, body)


def fl_attrs():
    return fl('Атрибуты класса и доступ по имени', [
        qo('Что выведет программа?', 'class T:\n    n = 0\n\n    def __init__(self):\n        T.n += 1\n\nT()\nT()\nT()\nprint(T.n)',
           ['0', '1', 'Ошибка'], 'n — атрибут класса, каждый новый объект увеличивает общий счётчик.'),
        qo('Что выведет программа?', 'class A:\n    x = 1\n\na = A()\nb = A()\na.x = 5\nprint(a.x, b.x, A.x)',
           ['5 5 5', '5 5 1', '1 1 1'], 'a.x = 5 создало собственный атрибут у a; у класса и у b по-прежнему 1.'),
        q('Что вернёт getattr(obj, "speed", 0), если у obj нет атрибута speed?', '0', ['None', 'AttributeError'],
          'Третий аргумент — запасное значение.'),
    ])


def code_attrs():
    return ts('Атрибуты класса и доступ по имени', [
        task('Напиши класс Student. У всех учеников общая школа — атрибут класса school со значением «Лицей 7», и общий счётчик '
             'созданных учеников — атрибут класса total. Student(name) запоминает имя и увеличивает total. Метод card() возвращает '
             '«ИМЯ, ШКОЛА».',
             'В теле класса: school = "Лицей 7" и total = 0. В __init__: self.name = name и Student.total += 1.\n'
             'card читает self.school — если у объекта своей школы нет, Python возьмёт школу класса.',
             'class Student:\n    school = "Лицей 7"\n    total = 0\n\n    def __init__(self, name):\n        self.name = name\n        Student.total += 1\n\n'
             '    def card(self):\n        return f"{self.name}, {self.school}"\n',
             ['a = Student("Аня")\nb = Student("Борис")\nprint(a.card())\nprint(Student.total)',
              'a = Student("Вика")\nStudent.school = "Гимназия 2"\nb = Student("Глеб")\nb.school = "Колледж"\nprint(a.card(), b.card(), sep="\\n")\nprint(Student.total)'],
             tail=TL),
        task('Настройки. У класса Settings три атрибута, их задаёт __init__: volume = 50, theme = «светлая», lang = «ru». На вход подаются '
             'команды, последняя — «стоп»: «показать ИМЯ» выводит «ИМЯ = ЗНАЧЕНИЕ»; «задать ИМЯ ЗНАЧЕНИЕ» меняет настройку '
             '(значение из цифр сохраняй числом) и выводит «ИМЯ = ЗНАЧЕНИЕ». Если такой настройки нет — «Нет настройки ИМЯ». '
             'Новых настроек не создавай.',
             'parts = s.split(); имя — parts[1]. Проверка: hasattr(settings, name). Чтение — getattr, запись — setattr.\n'
             'Число: value = int(text) if text.isdigit() else text.',
             'class Settings:\n    def __init__(self):\n        self.volume = 50\n        self.theme = "светлая"\n        self.lang = "ru"\n\n\nsettings = Settings()\n'
             'while True:\n    s = input()\n    if s == "стоп":\n        break\n    parts = s.split()\n    name = parts[1]\n    if not hasattr(settings, name):\n'
             '        print(f"Нет настройки {name}")\n        continue\n    if parts[0] == "задать":\n        text = parts[2]\n'
             '        setattr(settings, name, int(text) if text.isdigit() else text)\n    print(f"{name} = {getattr(settings, name)}")',
             ['показать volume\nзадать volume 80\nзадать theme тёмная\nпоказать theme\nстоп', 'показать font\nзадать lang en\nзадать size 3\nстоп']),
        task('Напиши функцию describe(obj, names): names — список имён атрибутов. Функция возвращает строку, в которой для каждого '
             'имени по порядку стоит «имя: значение» или «имя: —», если такого атрибута у obj нет; части разделены «; ».',
             'getattr(obj, name, "—") сразу даёт значение или прочерк.\nСобери части в список и соедини через "; ".join(...).',
             'def describe(obj, names):\n    parts = []\n    for name in names:\n        parts.append(f"{name}: {getattr(obj, name, \'—\')}")\n    return "; ".join(parts)\n',
             ['class Hero:\n    def __init__(self):\n        self.name = "Рыцарь"\n        self.hp = 30\n\nprint(describe(Hero(), ["name", "hp", "mana"]))',
              'class Box:\n    size = 3\n\nprint(describe(Box(), ["size"]))\nprint(describe(Box(), []))\nprint(describe(Box(), ["color", "size", "size"]))'], tail=TL),
    ])


def th_property():
    terms = [
        ('инкапсуляция', 'Принцип: данные объекта и правила работы с ними живут вместе, а снаружи доступно только то, что нужно — '
                         'методы и свойства. Внутреннее устройство можно менять, не ломая код, который пользуется объектом.'),
        ('скрытый атрибут', 'Атрибут, имя которого начинается с подчёркивания: self._balance. Это договорённость: «не трогай снаружи, '
                            'работай через методы». Python доступ не запрещает.'),
        ('property', 'Декоратор: @property над методом делает его «атрибутом» — читается без скобок. @имя.setter задаёт метод, который '
                     'срабатывает при присваивании и может проверить значение.\n'
                     'Пример:\nclass Square:\n    def __init__(self, side):\n        self.side = side\n\n    @property\n    def area(self):\n'
                     '        return self.side ** 2\n\nprint(Square(3).area)\nВывод:\n9'),
    ]
    body = (
        '<p>Если любой код может записать в атрибут что угодно, правила класса легко нарушить: <code>wallet.balance = -1000</code>. '
        'Поэтому атрибуты, которые нельзя менять напрямую, называют с подчёркиванием — [[скрытый атрибут]]. Это не запрет, '
        'а договорённость между программистами: «снаружи не трогать, пользоваться методами».</p>'
        '<h3>property</h3>'
        '<p>Часто хочется читать значение как обычный атрибут, но вычислять его или проверять при записи. Для этого есть '
        '[[property]]. Декоратор <code>@property</code> превращает метод в «атрибут только для чтения»: скобки не нужны.</p>'
        + ex('class Rect:\n    def __init__(self, w, h):\n        self.w = w\n        self.h = h\n\n    @property\n    def area(self):\n        return self.w * self.h\n\n\n'
             'r = Rect(3, 4)\nprint(r.area)\nr.w = 10\nprint(r.area)') +
        '<p>Площадь не хранится, а каждый раз считается заново — поэтому всегда соответствует сторонам. Присвоить '
        '<code>r.area = 5</code> не получится: будет AttributeError.</p>'
        '<p>Чтобы разрешить запись с проверкой, рядом пишут метод с декоратором <code>@имя.setter</code>. Значение хранится в скрытом '
        'атрибуте, а свойство с тем же именем без подчёркивания — вход для чтения и записи:</p>'
        + ex('class Player:\n    def __init__(self, nick, hp):\n        self.nick = nick\n        self.hp = hp\n\n    @property\n    def hp(self):\n        return self._hp\n\n'
             '    @hp.setter\n    def hp(self, value):\n        self._hp = max(0, min(100, value))\n\n\np = Player("zed", 150)\nprint(p.hp)\np.hp -= 130\nprint(p.hp)\np.hp -= 50\nprint(p.hp)') +
        '<p>Уже в <code>__init__</code> строка <code>self.hp = hp</code> идёт через setter, поэтому даже 150 при создании превратилось '
        'в 100. Снаружи код пишет <code>p.hp -= 50</code>, как с обычным атрибутом, а правило «здоровье от 0 до 100» соблюдается всегда.</p>'
        '<p>Если значение недопустимо и тихо исправлять его нельзя, setter вызывает ошибку — так делают с ценами, возрастом, '
        'датами: <code>raise ValueError("...")</code>.</p>'
        + '<p>Всё вместе — данные внутри объекта, доступ к ним только через методы и свойства, правила проверки рядом с данными — '
        'называют [[инкапсуляция]]. Её выгода в том, что внутреннее устройство можно переделать (хранить баланс в копейках, '
        'а температуру в кельвинах), и код снаружи этого даже не заметит.</p>' 
    )
    return th('Скрытые атрибуты и property', terms, body)


def fl_property():
    return fl('Скрытые атрибуты и property', [
        qo('Что выведет программа?', 'class C:\n    def __init__(self):\n        self.n = 2\n\n    @property\n    def double(self):\n        return self.n * 2\n\n'
           'c = C()\nc.n = 7\nprint(c.double)', ['4', '<bound method>', 'Ошибка'], 'Свойство считается при каждом чтении: 7 * 2.'),
        q('Что означает подчёркивание в имени self._balance?', 'Договорённость: снаружи не менять, пользоваться методами',
          ['Python запрещает доступ к атрибуту снаружи', 'Атрибут общий для всех объектов класса'], 'Запрета нет, это соглашение.'),
        q('Когда срабатывает метод с @hp.setter?', 'При присваивании obj.hp = значение',
          ['При чтении obj.hp', 'Только при создании объекта'], 'Чтение идёт через @property, запись — через setter.'),
    ])


def code_property():
    return ts('Скрытые атрибуты и property', [
        task('Напиши класс Temperature. Temperature(c) хранит температуру в градусах Цельсия. Свойство celsius читается и записывается; '
             'при попытке задать значение ниже -273.15 — ValueError «ниже абсолютного нуля». Свойство fahrenheit только читается: '
             'c * 9 / 5 + 32.',
             'Храни значение в self._c. @property celsius возвращает self._c, @celsius.setter проверяет и записывает. '
             'В __init__ пиши self.celsius = c — тогда проверка сработает и при создании.',
             'class Temperature:\n    def __init__(self, c):\n        self.celsius = c\n\n    @property\n    def celsius(self):\n        return self._c\n\n'
             '    @celsius.setter\n    def celsius(self, value):\n        if value < -273.15:\n            raise ValueError("ниже абсолютного нуля")\n        self._c = value\n\n'
             '    @property\n    def fahrenheit(self):\n        return self.celsius * 9 / 5 + 32\n',
             ['t = Temperature(25)\nprint(t.celsius, t.fahrenheit)\nt.celsius = -40\nprint(t.fahrenheit)',
              'try:\n    Temperature(-300)\nexcept ValueError as e:\n    print(e)\nt = Temperature(0)\ntry:\n    t.celsius = -274\nexcept ValueError as e:\n    print(e)\nprint(t.celsius)'],
             tail=TL),
        task('Напиши класс Account — счёт. Account(owner) создаёт счёт с нулевым балансом. Свойство balance только читается. '
             'deposit(amount) и withdraw(amount) вызывают ValueError «сумма должна быть больше нуля», если amount не больше нуля; '
             'withdraw при нехватке денег — ValueError «недостаточно средств». Каждая успешная операция записывается в историю, '
             'а свойство history возвращает копию списка строк вида «+500» и «-200».',
             'Баланс и историю храни в self._balance и self._history. Свойство history возвращает self._history[:] — копию, '
             'чтобы снаружи не испортили историю.',
             'class Account:\n    def __init__(self, owner):\n        self.owner = owner\n        self._balance = 0\n        self._history = []\n\n    @property\n'
             '    def balance(self):\n        return self._balance\n\n    @property\n    def history(self):\n        return self._history[:]\n\n'
             '    def deposit(self, amount):\n        if amount <= 0:\n            raise ValueError("сумма должна быть больше нуля")\n        self._balance += amount\n'
             '        self._history.append(f"+{amount}")\n\n    def withdraw(self, amount):\n        if amount <= 0:\n            raise ValueError("сумма должна быть больше нуля")\n'
             '        if amount > self._balance:\n            raise ValueError("недостаточно средств")\n        self._balance -= amount\n        self._history.append(f"-{amount}")\n',
             ['a = Account("Ира")\na.deposit(500)\na.withdraw(200)\nprint(a.balance, a.history)',
              'a = Account("Лёша")\nfor op, x in [("withdraw", 10), ("deposit", 0), ("deposit", 30)]:\n    try:\n        getattr(a, op)(x)\n    except ValueError as e:\n        print(e)\n'
              'h = a.history\nh.append("+1000000")\nprint(a.balance, a.history)'], tail=TL),
    ])


def code_final():
    return ts('Задачи: испытание', [
        task('Склад. Товар опиши классом Item(name, price, qty) со свойством total — стоимость price * qty. На вход подаются команды, '
             'последняя — «стоп»: «+ ИМЯ ЦЕНА КОЛ-ВО» — привезли товар: если он уже есть, количество прибавляется, а цена становится '
             'новой; «- ИМЯ КОЛ-ВО» — забрали со склада: если товара нет — «Нет товара: ИМЯ», если его меньше, чем просят, — '
             '«Не хватает: ИМЯ», а если товар кончился, он удаляется; «итого» — все товары по убыванию стоимости (при равной — по имени) '
             'строками «ИМЯ: КОЛ-ВО × ЦЕНА = СТОИМОСТЬ», затем «Всего: S» (у пустого склада — только «Всего: 0»). Цены и количества — целые.',
             'Склад — словарь {имя: Item}. Сортировка: sorted(items.values(), key=lambda it: (-it.total, it.name)).\n'
             'Свойство: @property def total(self): return self.price * self.qty.',
             'class Item:\n    def __init__(self, name, price, qty):\n        self.name = name\n        self.price = price\n        self.qty = qty\n\n    @property\n'
             '    def total(self):\n        return self.price * self.qty\n\n\nstock = {}\nwhile True:\n    parts = input().split()\n    if parts == ["стоп"]:\n        break\n'
             '    if parts[0] == "+":\n        name, price, qty = parts[1], int(parts[2]), int(parts[3])\n        if name in stock:\n            stock[name].qty += qty\n'
             '            stock[name].price = price\n        else:\n            stock[name] = Item(name, price, qty)\n    elif parts[0] == "-":\n        name, qty = parts[1], int(parts[2])\n'
             '        if name not in stock:\n            print(f"Нет товара: {name}")\n        elif stock[name].qty < qty:\n            print(f"Не хватает: {name}")\n        else:\n'
             '            stock[name].qty -= qty\n            if stock[name].qty == 0:\n                del stock[name]\n    else:\n'
             '        for it in sorted(stock.values(), key=lambda it: (-it.total, it.name)):\n            print(f"{it.name}: {it.qty} × {it.price} = {it.total}")\n'
             '        print(f"Всего: {sum(it.total for it in stock.values())}")',
             ['+ мяч 300 4\n+ ракетка 1200 1\n+ мяч 350 2\n- ракетка 1\n- сетка 1\nитого\nстоп', '+ кубик 50 10\n+ шашки 250 2\n- кубик 11\nитого\nстоп',
              'итого\n+ гиря 900 1\n- гиря 1\nитого\nстоп']),
    ])


def build():
    return topic('Классы и объекты', 'class, __init__, self, методы, property', [
        th_class(), fl_class(), code_class(),
        th_attrs(), fl_attrs(), code_attrs(),
        th_property(), fl_property(), code_property(),
        code_final(),
    ])
