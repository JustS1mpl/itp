from dsl import *

# Тема 25 «Наследование». Ученик знает классы, __init__, self, атрибуты класса, property, исключения и их иерархию.
# Четыре теории: наследование, super и полиморфизм; __str__, __repr__ и сравнение; арифметика, __len__ и __call__;
# свои исключения.


def th_inherit():
    terms = [
        ('утиная типизация', '«Если ходит как утка и крякает как утка — это утка»: Python не проверяет класс объекта, ему важно, '
                             'чтобы нужный метод был. Полиморфизм работает и без общего родителя.'),
        ('множественное наследование', 'class C(A, B): класс получает методы обоих родителей. Метод ищется по порядку MRO.'),
        ('MRO', 'Method Resolution Order — порядок, в котором Python ищет метод: сам класс, потом родители слева направо, в конце object. '
                'Его показывает Класс.__mro__.'),
        ('наследование', 'class Дочерний(Родитель): новый класс получает все атрибуты и методы родителя и может добавить свои '
                         'или заменить (переопределить) родительские.\n'
                         'Пример:\nclass Animal:\n    def hi(self):\n        return "..."\n\nclass Cat(Animal):\n    def hi(self):\n        return "мяу"\n\n'
                         'print(Animal().hi(), Cat().hi())\nВывод:\n... мяу'),
        ('super', 'super() внутри метода — доступ к методам родителя. Чаще всего: super().__init__(...) — вызов конструктора родителя — в начале своего __init__, '
                  'чтобы родитель задал свои атрибуты.'),
        ('issubclass', 'issubclass(Класс, Родитель) — True, если Класс унаследован от Родителя (напрямую или через цепочку).\n'
                       'Пример:\nprint(issubclass(KeyError, LookupError), issubclass(int, str))\nВывод:\nTrue False'),
        ('полиморфизм', 'Разные классы с методом одного имени: код вызывает obj.area() и не думает, круг перед ним или квадрат — '
                        'каждый объект выполнит свою версию.'),
    ]
    body = (
        '<p>Часто классы похожи: у героя, монстра и торговца в игре есть имя и здоровье, но ведут они себя по-разному. '
        'Общее выносят в класс-родитель, а остальные классы его наследуют — [[наследование]]:</p>'
        + ex('class Character:\n    def __init__(self, name, hp):\n        self.name = name\n        self.hp = hp\n\n    def info(self):\n        return f"{self.name} ({self.hp} hp)"\n\n'
             '    def speak(self):\n        return "..."\n\n\nclass Merchant(Character):\n    def speak(self):\n        return "Заходи, посмотри товар!"\n\n\n'
             'm = Merchant("Торговец", 50)\nprint(m.info())\nprint(m.speak())') +
        '<p><code>Merchant</code> не определяет <code>__init__</code> и <code>info</code> — он взял их у <code>Character</code>. '
        'А <code>speak</code> переопределил: Python ищет метод сначала в классе объекта, потом в родителе.</p>'
        '<h3>super()</h3>'
        '<p>Если дочернему классу нужны свои атрибуты, он пишет свой <code>__init__</code>, но работу родителя не повторяет, '
        'а вызывает её через [[super]]:</p>'
        + ex('class Character:\n    def __init__(self, name, hp):\n        self.name = name\n        self.hp = hp\n\n    def info(self):\n        return f"{self.name} ({self.hp} hp)"\n\n\n'
             'class Mage(Character):\n    def __init__(self, name, hp, mana):\n        super().__init__(name, hp)\n        self.mana = mana\n\n    def info(self):\n'
             '        return super().info() + f", мана {self.mana}"\n\n\nm = Mage("Мерлин", 40, 120)\nprint(m.info())\nprint(isinstance(m, Character), issubclass(Mage, Character))') +
        '<p><code>super().info()</code> берёт строку родителя и дополняет её. Объект Mage — это и Character: [[issubclass]] проверяет '
        'родство классов, <code>isinstance</code> — объекта и класса.</p>'
        '<h3>Полиморфизм</h3>'
        '<p>Главная выгода: код может работать с разными объектами одинаково, если у них есть метод с одним именем. '
        'Это [[полиморфизм]]:</p>'
        + ex('class Shape:\n    def area(self):\n        return 0\n\n\nclass Square(Shape):\n    def __init__(self, a):\n        self.a = a\n\n    def area(self):\n        return self.a ** 2\n\n\n'
             'class Rect(Shape):\n    def __init__(self, w, h):\n        self.w = w\n        self.h = h\n\n    def area(self):\n        return self.w * self.h\n\n\n'
             'shapes = [Square(3), Rect(2, 5), Square(1)]\nprint(sum(s.area() for s in shapes))') +
        '<p>Цикл не знает, какие фигуры в списке, — он просто зовёт <code>area()</code>. Добавится новая фигура — менять цикл не придётся.</p>'

        + '<h3>Утиная типизация</h3>'
        '<p>Общий родитель удобен, но не обязателен. Python не спрашивает, какого класса объект, — он просто вызывает метод. '
        'Есть метод — всё работает. Это [[утиная типизация]]:</p>'
        + ex('class Duck:\n    def speak(self):\n        return "кря"\n\n\nclass Robot:\n    def speak(self):\n        return "бип-буп"\n\n\n'
             'for thing in [Duck(), Robot()]:\n    print(thing.speak())') +
        '<h3>Несколько родителей</h3>'
        '<p>Класс может наследовать сразу от нескольких — [[множественное наследование]]. Если метод есть у обоих родителей, Python '
        'берёт первый по порядку [[MRO]]: сам класс, затем родители слева направо:</p>'
        + ex('class Car:\n    def move(self):\n        return "еду"\n\n\nclass Boat:\n    def move(self):\n        return "плыву"\n\n    def anchor(self):\n'
             '        return "якорь брошен"\n\n\nclass Amphibian(Car, Boat):\n    pass\n\n\na = Amphibian()\nprint(a.move(), a.anchor())\n'
             'print([c.__name__ for c in Amphibian.__mro__])') +
        '<p>Множественное наследование быстро запутывает код, поэтому его используют осторожно — обычно чтобы добавить классу '
        'небольшую «примесь» с парой методов.</p>' 
    )
    return th('Наследование', terms, body)


def fl_inherit():
    return fl('Наследование', [
        qo('Что выведет программа?', 'class A:\n    def who(self):\n        return "A"\n\n    def hello(self):\n        return "я " + self.who()\n\n'
           'class B(A):\n    def who(self):\n        return "B"\n\nprint(B().hello())', ['я A', 'я AB', 'Ошибка'],
           'hello взят у A, но self — объект B, поэтому self.who() — версия B.'),
        q('Зачем в __init__ дочернего класса пишут super().__init__(...)?', 'Чтобы родитель задал свои атрибуты',
          ['Чтобы дочерний класс стал наследником', 'Без этого нельзя вызывать методы родителя'],
          'Наследование задаёт строка class B(A); super() только вызывает метод родителя.'),
        qo('Что выведет программа?', 'class A: pass\nclass B(A): pass\nprint(isinstance(B(), A), issubclass(A, B))',
           ['True True', 'False False', 'False True'], 'Объект B — это и A; но A не наследник B.'),
    ])


def code_inherit():
    return ts('Наследование', [
        task('Фигуры. Напиши класс Shape с атрибутом класса name = «Фигура», методом area() — возвращает 0 — и методом describe(), '
             'который возвращает «ИМЯ: площадь S», где S — площадь, округлённая до двух знаков. Унаследуй от него Circle(r) с именем '
             '«Круг», Square(a) — «Квадрат» и Triangle(a, b) — прямоугольный треугольник с катетами a и b, «Треугольник». '
             'describe в наследниках не пиши — он общий.',
             'В наследнике: name = "Круг" в теле класса и свой area(). describe у Shape: return f"{self.name}: площадь {round(self.area(), 2)}" — '
             'self.name и self.area() возьмутся у настоящего класса объекта.\nПлощадь круга: math.pi * r ** 2.',
             'import math\n\n\nclass Shape:\n    name = "Фигура"\n\n    def area(self):\n        return 0\n\n    def describe(self):\n'
             '        return f"{self.name}: площадь {round(self.area(), 2)}"\n\n\nclass Circle(Shape):\n    name = "Круг"\n\n    def __init__(self, r):\n        self.r = r\n\n'
             '    def area(self):\n        return math.pi * self.r ** 2\n\n\nclass Square(Shape):\n    name = "Квадрат"\n\n    def __init__(self, a):\n        self.a = a\n\n'
             '    def area(self):\n        return self.a ** 2\n\n\nclass Triangle(Shape):\n    name = "Треугольник"\n\n    def __init__(self, a, b):\n        self.a = a\n'
             '        self.b = b\n\n    def area(self):\n        return self.a * self.b / 2\n',
             ['print(Circle(1).describe())\nprint(Square(3).describe())\nprint(Triangle(3, 5).describe())',
              'shapes = [Shape(), Circle(2), Square(1.5), Triangle(1, 1)]\nfor s in shapes:\n    print(s.describe())\nprint(round(sum(s.area() for s in shapes), 2))'],
             tail=TL),
        task('Зарплаты. Класс Employee(name, salary): метод pay() возвращает salary, метод info() — «ИМЯ: ВЫПЛАТА». Класс Manager(name, salary, bonus) '
             'наследует Employee, bonus — процент премии: pay() возвращает salary + salary * bonus // 100. info в Manager не пиши, '
             '__init__ Manager должен вызывать __init__ родителя через super().',
             'Manager.__init__: super().__init__(name, salary), затем self.bonus = bonus.\ninfo у Employee пиши через self.pay() — '
             'тогда у менеджера он сам возьмёт его версию pay.',
             'class Employee:\n    def __init__(self, name, salary):\n        self.name = name\n        self.salary = salary\n\n    def pay(self):\n        return self.salary\n\n'
             '    def info(self):\n        return f"{self.name}: {self.pay()}"\n\n\nclass Manager(Employee):\n    def __init__(self, name, salary, bonus):\n'
             '        super().__init__(name, salary)\n        self.bonus = bonus\n\n    def pay(self):\n        return self.salary + self.salary * self.bonus // 100\n',
             ['print(Employee("Аня", 60000).info())\nprint(Manager("Борис", 80000, 25).info())',
              'team = [Employee("Вика", 50000), Manager("Глеб", 90000, 10), Employee("Дима", 45000)]\nprint(sum(e.pay() for e in team))\n'
              'print(isinstance(team[1], Employee), issubclass(Employee, Manager))'], tail=TL),
        task('Зоопарк. Класс Animal(name) с атрибутом класса sound = «...» и методом speak(), который возвращает «ИМЯ: ЗВУК». Наследники: '
             'Cat — «мяу», Dog — «гав», Duck — «кря». На вход подаются строки «вид имя» (виды: кот, пёс, утка), последняя — «стоп». '
             'Для каждой строки создай животное и выведи его speak(); для неизвестного вида — «Не знаю, кто такой ВИД». '
             'В конце выведи «Всего животных: N» — сколько животных создано (строки с неизвестным видом не считаются).',
             'Классы — тоже значения: kinds = {"кот": Cat, "пёс": Dog, "утка": Duck}, затем animal = kinds[kind](name).\n'
             'У наследника достаточно строки sound = "мяу" в теле класса.',
             'class Animal:\n    sound = "..."\n\n    def __init__(self, name):\n        self.name = name\n\n    def speak(self):\n        return f"{self.name}: {self.sound}"\n\n\n'
             'class Cat(Animal):\n    sound = "мяу"\n\n\nclass Dog(Animal):\n    sound = "гав"\n\n\nclass Duck(Animal):\n    sound = "кря"\n\n\n'
             'kinds = {"кот": Cat, "пёс": Dog, "утка": Duck}\ncount = 0\nwhile True:\n    s = input()\n    if s == "стоп":\n        break\n    kind, name = s.split()\n'
             '    if kind not in kinds:\n        print(f"Не знаю, кто такой {kind}")\n        continue\n    print(kinds[kind](name).speak())\n    count += 1\n'
             'print(f"Всего животных: {count}")',
             ['кот Мурка\nпёс Рекс\nутка Кряка\nстоп', 'ёж Колючка\nкот Барсик\nстоп']),
        task('Враги. Опиши класс Enemy: имя и здоровье; метод take_hit(dmg) уменьшает здоровье и возвращает строку '
             '«ИМЯ: осталось N» (не меньше 0). Наследник Boss в конструкторе получает ещё броню, вызывает конструктор родителя '
             'через super() и переопределяет take_hit: урон уменьшается на броню (но не меньше 1), а когда здоровье впервые '
             'падает до половины от начального или ниже, к строке добавляется « — вторая фаза!».',
             'Boss.take_hit: dmg = max(1, dmg - self.armor); text = super().take_hit(dmg). Флаг self.phase2 и начальное здоровье '
             'запомни в конструкторе.',
             'class Enemy:\n    def __init__(self, name, hp):\n        self.name = name\n        self.hp = hp\n\n    def take_hit(self, dmg):\n'
             '        self.hp = max(0, self.hp - dmg)\n        return f"{self.name}: осталось {self.hp}"\n\n\nclass Boss(Enemy):\n'
             '    def __init__(self, name, hp, armor):\n        super().__init__(name, hp)\n        self.armor = armor\n        self.start = hp\n        self.phase2 = False\n\n'
             '    def take_hit(self, dmg):\n        text = super().take_hit(max(1, dmg - self.armor))\n'
             '        if not self.phase2 and self.hp <= self.start // 2:\n            self.phase2 = True\n            text += " — вторая фаза!"\n        return text',
             ['for e in [Enemy("Слизень", 10), Boss("Рыцарь", 100, 5)]:\n    print(e.take_hit(30))\n    print(e.take_hit(30))',
              'b = Boss("Голем", 10, 50)\nprint(b.take_hit(3))\nprint(isinstance(b, Enemy))', 'b = Boss("Дракон", 60, 0)\nfor i in range(3):\n    print(b.take_hit(20))'], tail=TL),
    ])


def th_str():
    terms = [
        ('__str__', 'Метод, который вызывают print(obj) и str(obj): возвращает строку для человека.'),
        ('__repr__', 'Метод, который вызывает repr(obj): строка для программиста, обычно как объект создать заново — Point(1, 2). '
                     'Её же показывает print списка объектов.'),
        ('repr', 'repr(x) — «техническая» строка значения. У строк — с кавычками.\nПример:\nprint(repr("кот"), repr(5))\nВывод:\n\'кот\' 5'),
        ('__eq__', 'Метод для ==: __eq__(self, other) возвращает True или False. Без него == сравнивает, один ли это объект.'),
        ('__lt__', 'Метод для <: __lt__(self, other). С ним работают sorted, min и max для списка объектов.'),
    ]
    body = (
        '<p>Свой объект пока печатается непонятно — что-то вроде <code>&lt;__main__.Point object at 0x7f…&gt;</code>. Python не знает, '
        'как показать его человеку. Это ему объясняют <b>магическими методами</b> — методами с двойными подчёркиваниями, которые '
        'Python вызывает сам в нужный момент. <code>__init__</code> — один из них.</p>'
        '<p>[[__str__]] вызывается в <code>print</code> и <code>str()</code>, [[__repr__]] — в [[repr]] и при печати списка объектов:</p>'
        + ex('class Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __str__(self):\n        return f"({self.x}; {self.y})"\n\n'
             '    def __repr__(self):\n        return f"Point({self.x}, {self.y})"\n\n\np = Point(3, -1)\nprint(p)\nprint([p, Point(0, 0)])\nprint(repr(p))') +
        '<p>Если написан только <code>__repr__</code>, <code>print</code> возьмёт его. Поэтому, когда лень писать оба, пишут <code>__repr__</code>.</p>'
        '<h3>Сравнение</h3>'
        '<p>По умолчанию <code>==</code> для объектов проверяет, один ли это объект, а не одинаковые ли в них данные. Чтобы сравнивать по '
        'содержимому, пишут [[__eq__]]. Для <code>&lt;</code> — [[__lt__]], и тогда объекты можно сортировать:</p>'
        + ex('class Card:\n    def __init__(self, rank, suit):\n        self.rank = rank\n        self.suit = suit\n\n    def __eq__(self, other):\n'
             '        return self.rank == other.rank and self.suit == other.suit\n\n    def __lt__(self, other):\n        return self.rank < other.rank\n\n'
             '    def __repr__(self):\n        return f"{self.rank}{self.suit}"\n\n\nprint(Card(7, "♠") == Card(7, "♠"), Card(7, "♠") == Card(7, "♥"))\n'
             'hand = [Card(10, "♥"), Card(2, "♣"), Card(7, "♠")]\nprint(sorted(hand), max(hand))') +
        '<p><code>&gt;</code> Python получает сам: <code>a &gt; b</code> — это <code>b &lt; a</code>. А <code>!=</code> — '
        'противоположность <code>__eq__</code>.</p>'
    )
    return th('Строки и сравнение объектов', terms, body)


def fl_str():
    return fl('Строки и сравнение объектов', [
        qo('Что выведет программа?', 'class T:\n    def __repr__(self):\n        return "T()"\n\n    def __str__(self):\n        return "объект T"\n\n'
           'print(T(), [T()])', ['объект T [объект T]', 'T() [T()]', 'T() [объект T]'], 'print объекта — __str__, а список показывает элементы через __repr__.'),
        q('Что сравнивает == для объектов своего класса, если __eq__ не написан?', 'Один ли это и тот же объект',
          ['Все атрибуты по очереди', 'Только первый атрибут'], 'Два разных объекта с одинаковыми данными без __eq__ не равны.'),
        q('Какой метод нужен, чтобы sorted(список_объектов) работал?', '__lt__', ['__eq__', '__str__'],
          'Сортировка сравнивает элементы через <.'),
    ])


def th_ops():
    terms = [
        ('__radd__', 'Сложение «справа»: если x + obj не получилось у x, Python пробует obj.__radd__(x). Нужен, чтобы работала sum, '
                     'которая начинает с 0.'),
        ('__iadd__', 'Метод для +=. Меняет объект на месте и обязательно возвращает self. Без него += работает через __add__ и создаёт новый объект.'),
        ('total_ordering', 'Декоратор класса из functools: если в классе есть __eq__ и __lt__, он сам допишет <=, > и >=.'),
        ('__add__', 'Метод для +: __add__(self, other) возвращает новый объект — результат сложения.'),
        ('__len__', 'Метод для len(obj): возвращает целое число не меньше нуля.'),
        ('__call__', 'Метод, который делает объект вызываемым как функция: obj(аргументы) вызывает obj.__call__(аргументы).'),
    ]
    body = (
        '<p>Магические методы есть почти для всех операторов. [[__add__]] отвечает за <code>+</code>: метод возвращает <b>новый</b> '
        'объект и не меняет слагаемые — как <code>2 + 3</code> не меняет ни двойку, ни тройку:</p>'
        + ex('class Money:\n    def __init__(self, rub):\n        self.rub = rub\n\n    def __add__(self, other):\n        return Money(self.rub + other.rub)\n\n'
             '    def __repr__(self):\n        return f"{self.rub} ₽"\n\n\na = Money(300)\nb = Money(150)\nprint(a + b, a, b)\nprint(a + b + Money(50))') +
        '<p>Похожие методы есть для <code>-</code>, <code>*</code>, <code>/</code> — у них другие имена, принцип тот же.</p>'
        '<h3>len и вызов</h3>'
        '<p>[[__len__]] даёт объекту длину: <code>len(obj)</code>. Заодно Python считает объект с длиной 0 ложным в <code>if</code>. '
        '[[__call__]] позволяет вызывать объект как функцию — это похоже на замыкание, только настройки хранятся в атрибутах:</p>'
        + ex('class Playlist:\n    def __init__(self):\n        self.songs = []\n\n    def __len__(self):\n        return len(self.songs)\n\n\n'
             'class Discount:\n    def __init__(self, percent):\n        self.percent = percent\n\n    def __call__(self, price):\n'
             '        return price - price * self.percent // 100\n\n\np = Playlist()\nprint(len(p), "пусто" if not p else "есть песни")\np.songs.append("Трек")\nprint(len(p))\n'
             'sale = Discount(20)\nprint(sale(1000), sale(250))') +
        '<p>Не стоит придумывать магию без нужды: <code>+</code> должен означать сложение, а <code>len</code> — размер. '
        'Тогда код с объектами читается так же легко, как с числами и списками.</p>'
        + '<h3>sum, += и все сравнения</h3>'
        '<p><code>sum</code> начинает с нуля: <code>0 + Money(300)</code>. У числа нет сложения с деньгами, и тогда Python пробует '
        '«сложение справа» — [[__radd__]] у второго слагаемого. [[__iadd__]] отвечает за <code>+=</code>: он меняет объект на месте '
        'и возвращает self. А декоратор [[total_ordering]] по двум методам — <code>__eq__</code> и <code>__lt__</code> — сам допишет '
        'остальные сравнения:</p>'
        + ex('from functools import total_ordering\n\n\n@total_ordering\nclass Money:\n    def __init__(self, rub):\n        self.rub = rub\n\n    def __add__(self, other):\n'
             '        return Money(self.rub + other.rub)\n\n    def __radd__(self, other):\n        return Money(other + self.rub)\n\n    def __iadd__(self, other):\n'
             '        self.rub += other.rub\n        return self\n\n    def __eq__(self, other):\n        return self.rub == other.rub\n\n    def __lt__(self, other):\n'
             '        return self.rub < other.rub\n\n    def __repr__(self):\n        return f"{self.rub} ₽"\n\n\nwallet = Money(100)\nwallet += Money(50)\n'
             'print(wallet, sum([Money(10), Money(20), Money(5)]))\nprint(Money(5) >= Money(3), Money(5) <= Money(3))')
    )
    return th('Арифметика и вызов', terms, body)


def fl_ops():
    return fl('Арифметика и вызов', [
        qo('Что выведет программа?', 'class V:\n    def __init__(self, x):\n        self.x = x\n\n    def __add__(self, other):\n        return V(self.x + other.x)\n\n'
           'a = V(2)\nb = a + V(5)\nprint(a.x, b.x)', ['7 7', '2 5', 'Ошибка'], '__add__ вернул новый объект, a не изменился.'),
        qo('Что выведет программа?', 'class Box:\n    def __init__(self, n):\n        self.n = n\n\n    def __len__(self):\n        return self.n\n\n'
           'print(len(Box(3)), bool(Box(0)))', ['3 True', '0 False', 'Ошибка'], 'len — 3; объект с длиной 0 считается ложным.'),
        q('Что нужно классу, чтобы его объект можно было вызвать: obj(5)?', 'Метод __call__', ['Метод __init__', 'Декоратор @property'],
          'obj(5) — это obj.__call__(5).'),
    ])


def code_ops():
    return ts('Арифметика и вызов', [
        task('Напиши класс Vector(x, y). Сложение векторов — новый вектор со сложенными координатами; векторы равны, если равны обе координаты; '
             'print показывает «(x, y)», а repr — «Vector(x, y)».',
             'Методы __add__, __eq__, __str__ и __repr__. __add__ возвращает Vector(self.x + other.x, self.y + other.y).',
             'class Vector:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __add__(self, other):\n        return Vector(self.x + other.x, self.y + other.y)\n\n'
             '    def __eq__(self, other):\n        return self.x == other.x and self.y == other.y\n\n    def __str__(self):\n        return f"({self.x}, {self.y})"\n\n'
             '    def __repr__(self):\n        return f"Vector({self.x}, {self.y})"\n',
             ['a = Vector(1, 2)\nb = Vector(3, -5)\nprint(a + b)\nprint([a, b])', 'print(Vector(1, 1) + Vector(0, 0) == Vector(1, 1), Vector(1, 2) == Vector(2, 1))\n'
              'print(Vector(1, 1) + Vector(2, 2) + Vector(3, 3))'], tail=TL),
        task('Напиши класс Playlist(name). add(title, seconds) добавляет песню. len(playlist) — число песен. print показывает '
             '«ИМЯ: N песен, M:SS», где M:SS — общая длительность (секунды двумя цифрами). Плейлисты сравниваются по общей '
             'длительности, чтобы работали sorted и max. Сложение двух плейлистов даёт новый плейлист с именем «А + Б» и всеми песнями '
             'обоих по порядку.',
             'Песни храни списком кортежей (название, секунды). Длительность — sum(s for _, s in self.songs); удобно сделать её методом.\n'
             'Формат: f"{total // 60}:{total % 60:02}". В __add__ создай Playlist(f"{self.name} + {other.name}") и добавь песни обоих.',
             'class Playlist:\n    def __init__(self, name):\n        self.name = name\n        self.songs = []\n\n    def add(self, title, seconds):\n'
             '        self.songs.append((title, seconds))\n\n    def total(self):\n        return sum(s for _, s in self.songs)\n\n    def __len__(self):\n        return len(self.songs)\n\n'
             '    def __lt__(self, other):\n        return self.total() < other.total()\n\n    def __add__(self, other):\n        result = Playlist(f"{self.name} + {other.name}")\n'
             '        for title, seconds in self.songs + other.songs:\n            result.add(title, seconds)\n        return result\n\n    def __str__(self):\n'
             '        t = self.total()\n        return f"{self.name}: {len(self)} песен, {t // 60}:{t % 60:02}"\n',
             ['a = Playlist("Утро")\na.add("Рассвет", 185)\na.add("Кофе", 200)\nprint(a)\nprint(len(a))',
              'a = Playlist("Рок")\na.add("Гроза", 300)\nb = Playlist("Чилл")\nb.add("Волны", 125)\nb.add("Ветер", 61)\nc = a + b\nprint(c)\nprint(max(a, b).name, sorted([a, c, b])[0].name)\n'
              'print(len(a), len(Playlist("Пусто")))'], tail=TL),
        task('Напиши класс Tax(percent) — налог. Объект можно вызвать с суммой: tax(amount) возвращает налог — amount * percent / 100, '
             'округлённый до двух знаков. repr показывает «Tax(13%)». Два налога равны, если равны проценты.',
             '__call__(self, amount): return round(amount * self.percent / 100, 2). __repr__ и __eq__ — по образцу из теории.',
             'class Tax:\n    def __init__(self, percent):\n        self.percent = percent\n\n    def __call__(self, amount):\n        return round(amount * self.percent / 100, 2)\n\n'
             '    def __eq__(self, other):\n        return self.percent == other.percent\n\n    def __repr__(self):\n        return f"Tax({self.percent}%)"\n',
             ['ndfl = Tax(13)\nprint(ndfl(50000), ndfl(1234.5))\nprint(ndfl)', 'taxes = [Tax(20), Tax(6), Tax(20)]\nprint(taxes, taxes[0] == taxes[2], taxes[0] == taxes[1])\n'
              'print([t(999) for t in taxes])'], tail=TL),
        task('Эдди. Опиши класс Eddies: сумма денег. Сложение двух сумм даёт новую сумму, sum по списку сумм тоже работает. '
             'Суммы сравниваются по величине, а печатаются с разделителем разрядов: «1,500 эдди».',
             '__add__ возвращает Eddies(self.amount + other.amount); __radd__ нужен для sum, который начинает с 0 — '
             'сложи с 0 как с числом. __eq__, __lt__ — по amount, __str__ — f"{self.amount:,} эдди".',
             'class Eddies:\n    def __init__(self, amount):\n        self.amount = amount\n\n    def __add__(self, other):\n'
             '        return Eddies(self.amount + other.amount)\n\n    def __radd__(self, other):\n        return Eddies(self.amount + other)\n\n'
             '    def __eq__(self, other):\n        return self.amount == other.amount\n\n    def __lt__(self, other):\n        return self.amount < other.amount\n\n'
             '    def __str__(self):\n        return f"{self.amount:,} эдди"',
             ['a = Eddies(1500)\nb = Eddies(250)\nprint(a + b)\nprint(a < b, a == Eddies(1500))',
              'pay = [Eddies(10000), Eddies(500), Eddies(75000)]\nprint(sum(pay))\nprint(max(pay), min(pay))', 'print(sorted([Eddies(3), Eddies(1)])[0])'], tail=TL),
    ])


def th_exc():
    terms = [
        ('своё исключение', 'Класс-наследник Exception (или другой ошибки): class BankError(Exception): pass. Вызывается raise, '
                            'ловится except по имени класса или по любому его родителю.\n'
                            'Пример:\nclass GameError(Exception):\n    pass\n\ntry:\n    raise GameError("нет хода")\nexcept GameError as e:\n    print("Ошибка:", e)\n'
                            'Вывод:\nОшибка: нет хода'),
        ('pass', 'Пустая команда, знакомая по циклам: ничего не делает. Нужна там, где Python требует блок, а писать в нём нечего, — например, в теле класса.'),
    ]
    body = (
        '<p>Ошибки в Python — тоже классы, и они наследуют друг друга: <code>KeyError</code> — наследник <code>LookupError</code>, '
        'а все обычные ошибки — наследники <code>Exception</code>. Поэтому <code>except LookupError</code> ловит и <code>KeyError</code>.</p>'
        '<p>Своя ошибка — [[своё исключение]] — это просто класс-наследник <code>Exception</code>. Тело часто пустое, тогда в нём, как в пустом цикле, '
        'пишут [[pass]]:</p>'
        + ex('class BankError(Exception):\n    pass\n\n\nclass NotEnoughMoney(BankError):\n    pass\n\n\nclass CardBlocked(BankError):\n    pass\n\n\n'
             'def pay(balance, amount, blocked=False):\n    if blocked:\n        raise CardBlocked("карта заблокирована")\n    if amount > balance:\n'
             '        raise NotEnoughMoney(f"не хватает {amount - balance}")\n    return balance - amount\n\n\n'
             'for args in [(500, 200), (500, 900), (500, 1, True)]:\n    try:\n        print("остаток", pay(*args))\n    except BankError as e:\n'
             '        print(type(e).__name__, "—", e)') +
        '<p>Свои классы ошибок дают две вещи. Во-первых, точный смысл: <code>NotEnoughMoney</code> понятнее, чем общий '
        '<code>ValueError</code>. Во-вторых, гибкий перехват: <code>except NotEnoughMoney</code> ловит только нехватку денег, '
        'а <code>except BankError</code> — все ошибки банка разом, не задевая чужие ошибки.</p>'
        '<p><code>type(e).__name__</code> — имя класса ошибки строкой: удобно для сообщений.</p>'
    )
    return th('Свои исключения', terms, body)


def fl_exc():
    return fl('Свои исключения', [
        qo('Что выведет программа?', 'class AppError(Exception):\n    pass\n\nclass LoginError(AppError):\n    pass\n\n'
           'try:\n    raise LoginError("пароль")\nexcept AppError as e:\n    print("поймали:", e)', ['Ошибка LoginError', 'поймали: LoginError', 'Ничего'],
           'LoginError — наследник AppError, поэтому except AppError её ловит.'),
        q('Зачем делать иерархию своих ошибок с общим родителем?', 'Чтобы ловить все ошибки модуля одним except',
          ['Иначе raise не сработает', 'Чтобы ошибки печатались красивее'], 'except Родитель ловит всех наследников.'),
        q('Что делает pass в теле класса class MyError(Exception): pass?', 'Ничего: класс просто наследует всё у Exception',
          ['Пропускает ошибку, не давая ей остановить программу', 'Запрещает создавать объекты класса'], 'pass — пустая команда.'),
    ])


def code_exc():
    return ts('Свои исключения', [
        task('Напиши иерархию ошибок банковской карты: BankError(Exception), от неё NotEnoughMoney и CardBlocked. Класс Card(balance): '
             'pay(amount) списывает деньги — при блокировке CardBlocked «карта заблокирована», при нехватке NotEnoughMoney «не хватает N», '
             'где N — недостача; block() блокирует карту; свойство balance только читается.',
             'Классы ошибок: class BankError(Exception): pass и наследники так же.\nВ Card храни self._balance и self.blocked = False; '
             'в pay сначала проверь блокировку, потом баланс.',
             'class BankError(Exception):\n    pass\n\n\nclass NotEnoughMoney(BankError):\n    pass\n\n\nclass CardBlocked(BankError):\n    pass\n\n\n'
             'class Card:\n    def __init__(self, balance):\n        self._balance = balance\n        self.blocked = False\n\n    @property\n    def balance(self):\n'
             '        return self._balance\n\n    def block(self):\n        self.blocked = True\n\n    def pay(self, amount):\n        if self.blocked:\n'
             '            raise CardBlocked("карта заблокирована")\n        if amount > self._balance:\n            raise NotEnoughMoney(f"не хватает {amount - self._balance}")\n'
             '        self._balance -= amount\n',
             ['c = Card(1000)\nc.pay(300)\ntry:\n    c.pay(800)\nexcept NotEnoughMoney as e:\n    print(e)\nprint(c.balance)',
              'c = Card(50)\nc.block()\ntry:\n    c.pay(10)\nexcept BankError as e:\n    print(type(e).__name__, e)\nprint(issubclass(CardBlocked, BankError), issubclass(BankError, NotEnoughMoney))'],
             tail=TL),
        task('Регистрация ников. На вход подаются ники, последняя строка — «стоп». Напиши функцию check(nick, taken), которая вызывает '
             'ошибки-наследники NickError(Exception): TooShort «короче 3 символов», BadChars «только буквы, цифры и _» и Taken «уже занят» '
             '(проверки в таком порядке). Если ник подходит — выведи «Добро пожаловать, НИК» и запомни его, иначе — «Ошибка: ТЕКСТ». '
             'Регистр букв при проверке занятости не важен: Zed и zed — один ник.',
             'Буквы, цифры и _: all(c.isalpha() or c.isdigit() or c == "_" for c in nick).\nЗанятые храни во множестве в нижнем регистре.\n'
             'В цикле: try: check(nick, taken) ... except NickError as e: print(f"Ошибка: {e}").',
             'class NickError(Exception):\n    pass\n\n\nclass TooShort(NickError):\n    pass\n\n\nclass BadChars(NickError):\n    pass\n\n\nclass Taken(NickError):\n    pass\n\n\n'
             'def check(nick, taken):\n    if len(nick) < 3:\n        raise TooShort("короче 3 символов")\n    if not all(c.isalpha() or c.isdigit() or c == "_" for c in nick):\n'
             '        raise BadChars("только буквы, цифры и _")\n    if nick.lower() in taken:\n        raise Taken("уже занят")\n\n\ntaken = set()\nwhile True:\n'
             '    nick = input()\n    if nick == "стоп":\n        break\n    try:\n        check(nick, taken)\n    except NickError as e:\n        print(f"Ошибка: {e}")\n'
             '    else:\n        taken.add(nick.lower())\n        print(f"Добро пожаловать, {nick}")',
             ['Zed\nzed\nкот\nx\nтоп-1\nnew_player7\nстоп', 'ab\nabc\nABC\nстоп']),
        task('Верстак. Опиши ошибки CraftError (наследник Exception), NotEnough и UnknownRecipe (наследники CraftError). '
             'Напиши функцию craft(recipe, inventory): рецепты — словарь RECIPES = {"факел": {"палка": 1, "уголь": 1}, '
             '"кирка": {"палка": 2, "камень": 3}}. Неизвестный рецепт — UnknownRecipe с названием; если чего-то не хватает — '
             'NotEnough с текстом «нужно N МАТЕРИАЛ»; иначе материалы списываются из inventory и возвращается название.',
             'Сначала проверь все материалы, потом списывай — иначе при нехватке часть уже пропадёт. '
             'В тестах ошибки ловят except CraftError и печатают type(e).__name__.',
             'class CraftError(Exception):\n    pass\n\n\nclass NotEnough(CraftError):\n    pass\n\n\nclass UnknownRecipe(CraftError):\n    pass\n\n\n'
             'RECIPES = {"факел": {"палка": 1, "уголь": 1}, "кирка": {"палка": 2, "камень": 3}}\n\n\ndef craft(recipe, inventory):\n'
             '    if recipe not in RECIPES:\n        raise UnknownRecipe(recipe)\n    need = RECIPES[recipe]\n    for item, n in need.items():\n'
             '        if inventory.get(item, 0) < n:\n            raise NotEnough(f"нужно {n} {item}")\n    for item, n in need.items():\n'
             '        inventory[item] -= n\n    return recipe',
             ['inv = {"палка": 3, "уголь": 1, "камень": 2}\nfor r in ["факел", "кирка", "меч"]:\n    try:\n        print(craft(r, inv))\n'
              '    except CraftError as e:\n        print(type(e).__name__, e)\nprint(inv)',
              'print(issubclass(NotEnough, CraftError), issubclass(UnknownRecipe, Exception))',
              'inv = {"палка": 9, "камень": 9}\nprint(craft("кирка", inv), craft("кирка", inv), inv)'], tail=TL),
    ])


def code_final():
    return ts('Задачи: испытание', [
        task('Дроби. Напиши класс Fraction(num, den): дробь хранится сокращённой, знаменатель всегда положительный, при знаменателе 0 — '
             'ValueError «знаменатель равен нулю». Нужны сложение, == и < (чтобы работали sorted и max) и print в виде «3/4» '
             '(целые — без знаменателя: «2», «-1»). На вход подаётся строка дробей «a/b» через пробел. Выведи «Сумма: S», '
             '«По возрастанию: …» через пробел и «Наибольшая: M». Если в строке есть дробь с нулевым знаменателем, выведи только '
             '«Ошибка: знаменатель равен нулю».',
             'Сокращение: наибольший общий делитель — алгоритм Евклида: while b: a, b = b, a % b (бери модули чисел).\n'
             'Если den < 0 — поменяй знак обоим. Сложение: Fraction(a.num * b.den + b.num * a.den, a.den * b.den). '
             'Сравнение без дробных чисел: a.num * b.den < b.num * a.den.\nСумму считай циклом от Fraction(0, 1): встроенная sum начинает с числа 0 и без __radd__ с дробью его не сложит.',
             'def gcd(a, b):\n    a, b = abs(a), abs(b)\n    while b:\n        a, b = b, a % b\n    return a\n\n\nclass Fraction:\n    def __init__(self, num, den):\n'
             '        if den == 0:\n            raise ValueError("знаменатель равен нулю")\n        if den < 0:\n            num, den = -num, -den\n        g = gcd(num, den)\n'
             '        self.num = num // g\n        self.den = den // g\n\n    def __add__(self, other):\n        return Fraction(self.num * other.den + other.num * self.den, self.den * other.den)\n\n'
             '    def __eq__(self, other):\n        return self.num == other.num and self.den == other.den\n\n    def __lt__(self, other):\n'
             '        return self.num * other.den < other.num * self.den\n\n    def __str__(self):\n        return str(self.num) if self.den == 1 else f"{self.num}/{self.den}"\n\n\n'
             'try:\n    items = []\n    for part in input().split():\n        a, b = part.split("/")\n        items.append(Fraction(int(a), int(b)))\nexcept ValueError as e:\n'
             '    print(f"Ошибка: {e}")\nelse:\n    total = Fraction(0, 1)\n    for f in items:\n        total = total + f\n    print(f"Сумма: {total}")\n'
             '    print("По возрастанию:", " ".join(str(f) for f in sorted(items)))\n    print(f"Наибольшая: {max(items)}")',
             ['1/2 3/4 -1/3', '2/4 6/-3 5/5', '1/2 3/0', '-7/14 1/2']),
    ])


def build():
    return topic('Наследование', 'super, магические методы, свои исключения', [
        th_inherit(), fl_inherit(), code_inherit(),
        th_str(), fl_str(),
        th_ops(), fl_ops(), code_ops(),
        th_exc(), fl_exc(), code_exc(),
        code_final(),
    ])
