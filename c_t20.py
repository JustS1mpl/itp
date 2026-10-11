from dsl import *
from c_t19 import CAR_CLASS

ELEC_SUB = '''class ElectricCar(Car):

    def __init__(self, color, consumption, bat_capacity, mileage=0):
        super().__init__(color, consumption, bat_capacity, mileage)
        self.bat_capacity = bat_capacity

    def drive(self, distance):
        if not self.engine_on:
            return "Двигатель не запущен."
        if self.reserve / self.consumption * 100 < distance:
            return "Малый запас заряда."
        self.mileage += distance
        self.reserve -= distance / 100 * self.consumption
        return f"Проехали {distance} км. Остаток заряда: {self.reserve} кВт*ч."

    def recharge(self):
        self.reserve = self.bat_capacity
'''

ELEC_STR = '''
    def __str__(self):
        return f"Электромобиль. " \\
               f"Цвет: {self.color}. " \\
               f"Пробег: {self.mileage} км. " \\
               f"Остаток заряда: {self.reserve} кВт*ч."
'''

ELEC_REPR = '''
    def __repr__(self):
        return f"ElectricCar('{self.color}', " \\
               f"{self.consumption}, " \\
               f"{self.bat_capacity}, " \\
               f"{self.mileage})"
'''

ELEC_ADD = '''
    def __add__(self, other):
        new_car = ElectricCar(self.color,
                              self.consumption + other.consumption,
                              self.bat_capacity + other.bat_capacity,
                              self.mileage + other.mileage)
        new_car.reserve = self.reserve + other.reserve
        return new_car
'''


def build():
    # ============ Теория 1: наследование ============
    terms1 = [
        ('наследование', 'Механизм ООП: новый класс создаётся на основе уже существующего и получает все его атрибуты и методы. К ним можно добавить свои или изменить унаследованные.\n\nПример:\nclass A:\n    def hi(self):\n        return "привет"\nclass B(A):\n    pass\nprint(B().hi())\nВывод:\nпривет'),
        ('базовый класс', 'Класс, от которого наследуются другие. Его ещё называют родительским. В записи class Pen(Pencil) базовым является Pencil: его имя стоит в скобках.\n\nПример:\nclass Animal:\n    pass\nclass Dog(Animal):\n    pass\nprint(Dog.__base__.__name__)\nВывод:\nAnimal'),
        ('производный класс', 'Класс, созданный на основе другого. Его называют ещё наследником или дочерним классом. Он получает всё, что есть у базового, и может добавлять своё. В записи class Pen(Pencil) производным является Pen.\n\nПример:\nclass A:\n    x = 1\nclass B(A):\n    y = 2\nprint(B.x, B.y)\nВывод:\n1 2'),
        ('переопределение', 'Объявление в производном классе метода с тем же именем, что и в базовом. Для объектов производного класса будет выполняться новая версия метода.\n\nПример:\nclass A:\n    def hi(self):\n        return 1\nclass B(A):\n    def hi(self):\n        return 2\nprint(B().hi())\nВывод:\n2'),
        ('super', 'Функция: даёт доступ к методам базового класса из производного. Чаще всего через неё вызывают __init__ родителя в виде super().__init__(...), чтобы не писать его код заново.\n\nПример:\nclass A:\n    def __init__(self, x):\n        self.x = x\nclass B(A):\n    def __init__(self, x, y):\n        super().__init__(x)\n        self.y = y\nb = B(1, 2)\nprint(b.x, b.y)\nВывод:\n1 2'),
    ]
    body1 = '''
<p>В прошлой теме для электромобиля мы написали класс ElectricCar, который почти целиком повторял Car: цвет, пробег, запуск и остановка двигателя одинаковые, различались лишь бак и аккумулятор. Копировать десятки строк неудобно. Найдёшь ошибку в одном классе, и придётся исправлять её во втором. Когда классов становится много, такой код превращается в кошмар. Чтобы не дублировать код, в ООП есть механизм [[наследование|наследования]].</p>
<p>Наследование позволяет создать новый класс на основе уже существующего. Существующий класс называют [[базовый класс|базовым]], а новый [[производный класс|производным]] (или наследником). Производный класс получает все атрибуты и методы базового, а кроме того, может добавить свои и изменить унаследованные.</p>

<h3>Как записать наследование</h3>
<p>Имя базового класса пишут в скобках после имени нового класса. Возьмём карандаш: он хранит цвет и умеет рисовать. Ручка это тот же карандаш, который к тому же умеет подписывать документы, но только подходящим цветом:</p>
''' + ex('''class Pencil:

    def __init__(self, color="серый"):
        self.color = color

    def draw_picture(self):
        return f"Нарисован рисунок цветом '{self.color}'."


class Pen(Pencil):

    def sign_document(self):
        if self.color not in ("синий", "чёрный", "фиолетовый"):
            return f"Ручкой цвета '{self.color}' нельзя подписать документ."
        return "Подписан документ."


blue_pen = Pen(color="синий")
print(blue_pen.draw_picture())
print(blue_pen.sign_document())
red_pen = Pen(color="красный")
print(red_pen.draw_picture())
print(red_pen.sign_document())''') + '''
<p>Класс Pen унаследовал от Pencil и инициализацию цвета, и метод draw_picture. Мы не писали их заново, они просто перешли к ручке. Мы добавили только то, чего у карандаша нет: метод sign_document.</p>

<h3>Как Python ищет метод</h3>
<p>Когда у объекта вызывают метод, Python сначала ищет его в самом классе объекта. Если не нашёл, идёт в базовый класс. Если и там нет, поднимается ещё выше. Если ни в одном из родительских классов метода нет, возникнет ошибка AttributeError. Так, у ручки найдётся и sign_document (её собственный метод), и draw_picture (взятый из карандаша). А метод, которого нет нигде, вызвать не получится:</p>
''' + exs('''pen = Pen("синий")
pen.erase()''', '''Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
AttributeError: 'Pen' object has no attribute 'erase'
''') + '''
<p>Принадлежность к классу можно проверить функцией isinstance. Ручка относится сразу к двум классам: к своему и к базовому, ведь любая ручка в нашей модели является ещё и карандашом. А карандаш ручкой не является:</p>
''' + ex('''class Pencil:
    pass

class Pen(Pencil):
    pass

pen = Pen()
pencil = Pencil()
print(isinstance(pen, Pen), isinstance(pen, Pencil))
print(isinstance(pencil, Pen))
print(type(pen) is Pencil)''') + '''
<p>Обрати внимание на последнюю строку: type показывает точный класс объекта, а isinstance учитывает и родителей.</p>

<h3>Переопределение методов</h3>
<p>Производный класс может не только добавлять методы, но и менять унаследованные. Для этого в нём объявляют метод с тем же именем. Такое действие называют [[переопределение|переопределением]]. У объектов нового класса будет выполняться новая версия, а у объектов базового прежняя:</p>
''' + ex('''class Animal:

    def speak(self):
        return "..."


class Dog(Animal):

    def speak(self):
        return "Гав!"


class Fish(Animal):
    pass


for pet in (Animal(), Dog(), Fish()):
    print(pet.speak())''') + '''
<p>Собака подменила метод speak своим, а рыба ничего не меняла и пользуется вариантом из Animal. Заметь, что Python выбирает версию метода по классу <b>самого объекта</b>, а не по тому, где его вызвали.</p>

<h3>Электромобиль на основе автомобиля</h3>
<p>Теперь у нас есть всё, чтобы переписать ElectricCar без копирования. Базовым классом будет Car из прошлой темы. Электромобиль унаследует запуск, остановку, заправку и геттеры. Изменить нужно две вещи. Первая: при создании атрибут называется bat_capacity, и в нём хранится ёмкость аккумулятора. Вторая: другие тексты в методе drive и метод recharge вместо refuel.</p>
<p>Для инициализации нужно выполнить и всё, что делает __init__ базового класса, и добавить своё. Повторять тот же код не хочется. Для этого есть функция [[super|super()]]: она возвращает «взгляд» на базовый класс, и через неё можно вызвать его метод. Запись <code>super().__init__(color, consumption, bat_capacity, mileage)</code> запускает инициализацию Car, а следующей строкой мы добавляем электрический атрибут.</p>
''' + ex(CAR_CLASS + '\n' + ELEC_SUB + '''

electric_car = ElectricCar(color="white", consumption=15, bat_capacity=90)
print(electric_car.start_engine())
print(electric_car.drive(100))
print(electric_car.get_reserve())
electric_car.recharge()
print(electric_car.get_reserve())''') + '''
<p>Класс ElectricCar унаследовал поведение Car: запуск двигателя (start_engine) мы не писали, он работает. Мы переопределили метод drive и добавили новый метод recharge. Описание стало компактнее, а исправления в общей логике достаточно внести один раз: в базовом классе.</p>
<p>Через super() можно не только вызывать __init__, но и <b>дополнять</b> любой унаследованный метод, а не заменять целиком. Сначала выполняется версия родителя, а потом добавляется своё:</p>
''' + ex('''class Pencil:

    def __init__(self, color):
        self.color = color

    def draw_picture(self):
        return f"Нарисован рисунок цветом '{self.color}'."


class Pen(Pencil):

    def draw_picture(self):
        return super().draw_picture() + " Рисунок подписан."


print(Pen("синий").draw_picture())''') + '''
'''
    th1 = th('Наследование', terms1, body1)

    fl1 = fl('Вопросы: наследование', [
        q('Для чего нужно наследование?', 'Создать класс на основе другого и не дублировать код', ['Чтобы удалить ненужные классы', 'Чтобы ускорить запуск программы', 'Чтобы скрыть данные внутри объекта'], 'Производный класс получает атрибуты и методы базового, поэтому общий код не нужно писать заново.'),
        q('Как записать, что класс Pen наследуется от Pencil?', 'class Pen(Pencil):', ['class Pencil(Pen):', 'class Pen -> Pencil:', 'class Pen from Pencil:'], 'Имя базового класса пишут в скобках после имени нового класса.'),
        q('Как называется класс Dog в записи class Dog(Animal)?', 'Производный класс (наследник)', ['Базовый класс', 'Метакласс', 'Объект'], 'Dog создан на основе Animal, поэтому он производный. Базовым (родительским) здесь является Animal.'),
        qo('Что выведет программа?', '''class A:

    def hi(self):
        return "привет"


class B(A):
    pass


print(B().hi())''', ['привет', 'Ошибка', 'None'], 'В классе B нет метода hi, поэтому Python ищет его в базовом классе A и находит.'),
        qo('Что выведет программа?', '''class A:

    def name(self):
        return "A"


class B(A):

    def name(self):
        return "B"


print(A().name() + B().name())''', ['AB', 'AA', 'BB'], 'B переопределил метод name. У объекта класса A выполняется версия из A, у объекта класса B версия из B.'),
        qo('Что выведет программа?', '''class A:

    def name(self):
        return "A"


class B(A):
    pass


class C(B):

    def name(self):
        return "C"


print(B().name(), C().name())''', ['A C', 'B C', 'C C'], 'В классе B метода name нет, берётся из A. У C он переопределён.'),
        qo('Что выведет программа?', '''class Pencil:
    pass


class Pen(Pencil):
    pass


pen = Pen()
print(isinstance(pen, Pencil))''', ['True', 'False', 'Ошибка'], 'isinstance учитывает и базовые классы: любая ручка в нашей модели является ещё и карандашом.'),
        qo('Что выведет программа?', '''class Pencil:
    pass


class Pen(Pencil):
    pass


print(isinstance(Pencil(), Pen))''', ['False', 'True', 'Ошибка'], 'Базовый класс не является наследником. Объект класса Pencil не относится к классу Pen.'),
        qo('Что выведет программа?', '''class Pencil:

    def __init__(self, color):
        self.color = color


class Pen(Pencil):

    def __init__(self, color, ink):
        super().__init__(color)
        self.ink = ink


pen = Pen("синий", 5)
print(pen.color, pen.ink)''', ['синий 5', '5 синий', 'Ошибка'], 'super().__init__(color) выполнил инициализацию базового класса и создал атрибут color. Затем наследник добавил свой атрибут ink.'),
        qo('Что выведет программа?', '''class A:

    def hi(self):
        return "A"


class B(A):

    def hi(self):
        return super().hi() + "B"


print(B().hi())''', ['AB', 'BA', 'B'], 'Метод hi в B сначала вызывает версию родителя через super(), получает "A" и добавляет к ней "B".'),
        q('Что произойдёт, если вызвать метод, которого нет ни в классе, ни в его родителях?', 'AttributeError', ['TypeError', 'Метод создастся автоматически', 'Вернётся None'], 'Python проверит класс объекта, затем все базовые, и, если нигде не найдёт, сообщит об AttributeError.'),
        q('Что делает вызов super().__init__(...) в методе __init__ наследника?', 'Запускает инициализацию базового класса', ['Удаляет базовый класс', 'Создаёт новый объект того же класса', 'Запускает программу заново'], 'Так наследник выполняет начальную настройку, которую умеет делать родитель, и не дублирует код.'),
    ])

    # ============ Теория 2: множественное наследование ============
    terms2 = [
        ('множественное наследование', 'Ситуация, когда класс наследуется сразу от нескольких базовых классов. Их перечисляют в скобках через запятую. Производный класс получает все атрибуты и методы всех родителей.\n\nПример:\nclass A:\n    def a(self):\n        return 1\nclass B:\n    def b(self):\n        return 2\nclass C(A, B):\n    pass\nc = C()\nprint(c.a(), c.b())\nВывод:\n1 2'),
        ('MRO', 'Method Resolution Order, порядок разрешения методов: порядок, в котором Python просматривает классы при поиске метода. Сначала сам класс, затем его родители слева направо. Посмотреть порядок можно через атрибут __mro__.\n\nПример:\nclass A:\n    pass\nclass B(A):\n    pass\nprint([c.__name__ for c in B.__mro__])\nВывод:\n[\'B\', \'A\', \'object\']'),
    ]
    body2 = '''
<p>В Python класс может наследоваться сразу от нескольких базовых классов. Это называют [[множественное наследование|множественным наследованием]]. Производный класс при этом получает доступ ко всем атрибутам и методам всех родителей.</p>
<p>Разберём пример с приветствием. У нас три класса. Первый, GreetingFormal, при создании заводит атрибут с формальным приветствием и умеет здороваться по имени. Второй, GreetingInformal, делает то же в неформальном стиле. Третий, GreetingMix, наследуется от обоих и умеет здороваться и так и так. Чтобы задать несколько родителей, их перечисляют в скобках через запятую:</p>
''' + ex('''class GreetingFormal:

    def __init__(self):
        self.formal_greeting = "Добрый день,"

    def greet_formal(self, name):
        return f"{self.formal_greeting} {name}!"


class GreetingInformal:

    def __init__(self):
        self.informal_greeting = "Привет,"

    def greet_informal(self, name):
        return f"{self.informal_greeting} {name}!"


class GreetingMix(GreetingFormal, GreetingInformal):

    def __init__(self):
        GreetingFormal.__init__(self)
        GreetingInformal.__init__(self)


mixed_greeting = GreetingMix()
print(mixed_greeting.greet_formal("Пользователь"))
print(mixed_greeting.greet_informal("Пользователь"))''') + '''
<p>Класс GreetingMix унаследовал методы обоих классов. Обрати внимание на его __init__. У обоих родителей есть собственный __init__, и каждый создаёт свой атрибут. Чтобы получить оба атрибута, мы вызвали инициализацию каждого родителя явно, по имени класса: <code>GreetingFormal.__init__(self)</code>. В таком вызове self приходится передавать самому, ведь мы обращаемся к методу через класс, а не через объект.</p>

<h3>Порядок поиска методов: MRO</h3>
<p>Когда у класса несколько родителей, возникает вопрос: если одинаковое имя есть у двух родителей, чей метод будет выполнен? Python использует [[MRO|порядок разрешения методов]] (MRO). Он ищет метод в самом классе, потом в родителях слева направо, в том порядке, в котором они перечислены в скобках. Посмотреть порядок можно в атрибуте __mro__:</p>
''' + ex('''class A:
    def hello(self):
        return "привет из A"


class B:
    def hello(self):
        return "привет из B"


class C(A, B):
    pass


class D(B, A):
    pass


print(C().hello())
print(D().hello())
print([cls.__name__ for cls in C.__mro__])
print([cls.__name__ for cls in D.__mro__])''') + '''
<p>В списке в конце стоит класс object. Это общий родитель вообще всех классов в Python, от него неявно наследуется всё. Классы C и D отличаются лишь порядком родителей, и это решает, какая версия hello будет выбрана: побеждает тот, кто указан первым.</p>

<h3>Почему со множественным наследованием не стоит торопиться с super()</h3>
<p>Функция super() не просто «берёт родителя». Она идёт по тому самому порядку MRO и вызывает метод <b>следующего по порядку</b> класса. Что будет, если в GreetingMix вместо двух явных вызовов написать один super().__init__()?</p>
''' + exs('''class GreetingMix(GreetingFormal, GreetingInformal):

    def __init__(self):
        super().__init__()


mixed_greeting = GreetingMix()
print(mixed_greeting.greet_formal("Пользователь"))
print(mixed_greeting.greet_informal("Пользователь"))''', '''Добрый день, Пользователь!
Traceback (most recent call last):
  File "<stdin>", line 9, in <module>
    print(mixed_greeting.greet_informal("Пользователь"))
  File "<stdin>", line 19, in greet_informal
    return f"{self.informal_greeting} {name}!"
AttributeError: 'GreetingMix' object has no attribute 'informal_greeting'. Did you mean: 'formal_greeting'?
''') + '''
<p>Вызов super().__init__() выполнил __init__ только первого родителя из MRO, то есть GreetingFormal. А GreetingInformal.__init__ никто не запустил, поэтому атрибута informal_greeting не появилось. Класс GreetingFormal не знает про второго родителя и не передаёт ему управление. (Бывает и по-другому: если каждый родитель сам вызывает super().__init__(), то все инициализации выстраиваются по цепочке MRO. Но это уже не наш случай и требует аккуратного проектирования.)</p>
<p>Поэтому запомни простое правило. Если у класса несколько родителей, у которых есть свои __init__, вызывай их явно по именам, как в примере с приветствием. А super() используй при обычном наследовании от одного родителя.</p>
<p>Когда множественное наследование удобно:</p>
<ul>
<li>нужно объединить поведение из нескольких независимых классов;</li>
<li>базовые классы отвечают за разные стороны объекта (приветствие, запись в журнал, сохранение данных);</li>
<li>хочется переиспользовать код без глубокой цепочки наследования.</li>
</ul>
<p>Платой за это становится запутанность: порядок поиска и порядок инициализации нужно продумывать заранее.</p>
'''
    th2 = th('Множественное наследование', terms2, body2)

    fl2 = fl('Вопросы: множественное наследование', [
        q('Как записать наследование от двух классов?', 'class C(A, B):', ['class C(A + B):', 'class C(A or B):', 'class C: A, B'], 'Базовые классы перечисляют в скобках через запятую.'),
        qo('Что выведет программа?', '''class A:
    def a(self):
        return 1


class B:
    def b(self):
        return 2


class C(A, B):
    pass


c = C()
print(c.a() + c.b())''', ['3', '1', 'Ошибка'], 'Класс C получает методы обоих родителей. a() возвращает 1, b() возвращает 2, сумма 3.'),
        qo('Что выведет программа?', '''class A:
    def hi(self):
        return "A"


class B:
    def hi(self):
        return "B"


class C(A, B):
    pass


print(C().hi())''', ['A', 'B', 'AB'], 'Метод ищется в классе, а потом в родителях слева направо. Первым стоит A, поэтому берётся его версия.'),
        qo('Что выведет программа?', '''class A:
    def hi(self):
        return "A"


class B:
    def hi(self):
        return "B"


class C(B, A):
    pass


print(C().hi())''', ['B', 'A', 'AB'], 'Порядок родителей изменился: теперь первым в скобках стоит B, и его метод побеждает.'),
        qo('Что выведет программа?', '''class A:
    pass


class B(A):
    pass


print(B.__mro__[1].__name__)''', ['A', 'B', 'object'], 'MRO класса B начинается с самого B, затем идёт его родитель A, потом object.'),
        q('Что такое MRO?', 'Порядок просмотра классов при поиске метода', ['Способ скрыть методы класса', 'Название метода инициализации', 'Модуль для работы с объектами'], 'MRO (Method Resolution Order) задаёт последовательность: сам класс, потом родители слева направо, в конце object.'),
        q('Какой класс стоит в конце MRO любого класса?', 'object', ['Base', 'type', 'self'], 'object это общий родитель всех классов в Python.'),
        q('Что делает функция super() при множественном наследовании?', 'Идёт по MRO и вызывает метод следующего класса', ['Вызывает методы всех родителей по очереди', 'Выбирает случайного родителя', 'Копирует методы родителей в наследника'], 'super() обращается к следующему по порядку MRO классу. Остальных родителей он сам не вызовет.'),
        q('Как надёжно запустить __init__ у двух разных родителей?', 'Вызвать каждый явно: Родитель.__init__(self)', ['Один раз написать super().__init__()', 'Ничего не делать, Python вызовет все сам', 'Создать объекты родителей отдельно'], 'При явном вызове по имени класса оба родителя гарантированно выполнят инициализацию. self нужно передавать вручную.'),
        qo('Что выведет программа?', '''class A:

    def __init__(self):
        self.x = 1


class B:

    def __init__(self):
        self.y = 2


class C(A, B):

    def __init__(self):
        A.__init__(self)
        B.__init__(self)


c = C()
print(c.x + c.y)''', ['3', '1', 'Ошибка'], 'Оба __init__ вызваны явно, поэтому у объекта есть и x, и y: 1 + 2 равно 3.'),
        qo('Что выведет программа?', '''class A:

    def __init__(self):
        self.x = 1


class B:

    def __init__(self):
        self.y = 2


class C(A, B):

    def __init__(self):
        A.__init__(self)


c = C()
print(hasattr(c, "x"), hasattr(c, "y"))''', ['True False', 'True True', 'False True'], 'Инициализация B не вызывалась, поэтому атрибута y нет. Функция hasattr проверяет, есть ли у объекта атрибут с таким именем.'),
    ])

    # ============ Теория 3: магические методы ============
    terms3 = [
        ('магический метод', 'Метод, имя которого начинается и заканчивается двумя подчёркиваниями, например __init__, __str__, __add__. Python вызывает его сам, когда выполняется встроенная операция или функция. Их ещё называют специальными методами.\n\nПример:\nclass A:\n    def __len__(self):\n        return 42\nprint(len(A()))\nВывод:\n42'),
        ('__str__', 'Магический метод: должен вернуть удобочитаемую строку с описанием объекта. Вызывается функцией str() и при выводе объекта через print().\n\nПример:\nclass Cat:\n    def __str__(self):\n        return "кот Том"\nprint(Cat())\nВывод:\nкот Том'),
        ('__repr__', 'Магический метод: возвращает строку, представляющую объект для отладки, лучше всего в таком виде, каким объект можно было бы создать. Вызывается функцией repr() и используется при показе объектов внутри списков.\n\nПример:\nclass Cat:\n    def __repr__(self):\n        return "Cat()"\nprint([Cat(), Cat()])\nВывод:\n[Cat(), Cat()]'),
        ('перегрузка операторов', 'Возможность задать, как объекты твоего класса ведут себя с операторами и встроенными функциями: плюс, сравнение, len, индексация и другими. Достигается определением магических методов.\n\nПример:\nclass A:\n    def __add__(self, other):\n        return "сложили"\nprint(A() + A())\nВывод:\nсложили'),
    ]
    body3 = '''
<p>Посмотрим, что произойдёт, если вывести объект собственного класса. Возьмём электромобиль из прошлого раздела и сделаем <code>print(electric_car)</code>. Вывод будет таким (адрес в памяти у тебя будет другой):</p>
''' + exs('''print(electric_car)''', '''<__main__.ElectricCar object at 0x000002365DDD8A00>
''') + '''
<p>Это говорит лишь о том, что electric_car объект класса ElectricCar, лежащий по такому-то адресу в памяти. Для человека это малоинформативно. Но вывод можно улучшить.</p>
<p>Когда print() хочет показать объект, он вызывает встроенную функцию str(), а та в свою очередь вызывает у объекта метод [[__str__|__str__]]. Если его определить, мы сами решаем, что будет выводиться. Добавим этот метод в ElectricCar:</p>
''' + ex(CAR_CLASS + '\n' + ELEC_SUB + ELEC_STR + '''

electric_car = ElectricCar(color="белый", consumption=15, bat_capacity=90)
print(electric_car.start_engine())
print(electric_car.drive(100))
print(electric_car)''') + '''
<h3>Магические методы</h3>
<p>Метод __str__ относится к особой группе методов. Имена таких методов окружены двойными подчёркиваниями: __init__, __str__, __add__. Это [[магический метод|магические (специальные) методы]]. Их никто не вызывает напрямую. Python сам запускает их, когда выполняется подходящая операция: создание объекта, вывод, сложение, сравнение, получение длины. Определяя такие методы, мы настраиваем поведение объектов под свои нужды. Это называют [[перегрузка операторов|перегрузкой операторов]]: свой объект можно сложить, сравнить, измерить, вызвать как функцию, как будто это встроенный тип.</p>
<p>Вот несколько самых частых магических методов:</p>
<ul>
<li><code>__repr__</code> вызывается функцией repr() и возвращает строку для отладки; через него показываются объекты внутри списков;</li>
<li><code>__str__</code> вызывается функцией str() и при печати, должен вернуть удобочитаемое описание;</li>
<li><code>__add__</code> задаёт поведение оператора +;</li>
<li><code>__eq__</code> определяет, равны ли объекты (оператор ==);</li>
<li><code>__len__</code> вызывается функцией len().</li>
</ul>
<p>Ниже более полный обзор по группам. Учить его наизусть не нужно, он нужен как справочник: захотел, чтобы объект вёл себя как число или коллекция, и нашёл нужный метод.</p>
<div style="overflow-x:auto;margin:0 0 14px"><table style="margin:0">
<tr><th>Группа</th><th>Метод</th><th>Срабатывает</th></tr>
<tr><td rowspan="6">Сравнение</td><td><code>__lt__</code></td><td><code>a &lt; b</code></td></tr>
<tr><td><code>__le__</code></td><td><code>a &lt;= b</code></td></tr>
<tr><td><code>__eq__</code></td><td><code>a == b</code></td></tr>
<tr><td><code>__ne__</code></td><td><code>a != b</code></td></tr>
<tr><td><code>__gt__</code></td><td><code>a &gt; b</code></td></tr>
<tr><td><code>__ge__</code></td><td><code>a &gt;= b</code></td></tr>
<tr><td>Вызов как функции</td><td><code>__call__</code></td><td><code>obj(...)</code></td></tr>
<tr><td rowspan="5">Коллекция</td><td><code>__getitem__</code></td><td><code>obj[key]</code></td></tr>
<tr><td><code>__setitem__</code></td><td><code>obj[key] = value</code></td></tr>
<tr><td><code>__delitem__</code></td><td><code>del obj[key]</code></td></tr>
<tr><td><code>__len__</code></td><td><code>len(obj)</code></td></tr>
<tr><td><code>__contains__</code></td><td><code>item in obj</code></td></tr>
<tr><td rowspan="8">Математика</td><td><code>__add__</code>, <code>__sub__</code></td><td><code>+</code>, <code>-</code></td></tr>
<tr><td><code>__mul__</code>, <code>__matmul__</code></td><td><code>*</code>, <code>@</code></td></tr>
<tr><td><code>__truediv__</code>, <code>__floordiv__</code></td><td><code>/</code>, <code>//</code></td></tr>
<tr><td><code>__mod__</code>, <code>__divmod__</code></td><td><code>%</code>, <code>divmod()</code></td></tr>
<tr><td><code>__pow__</code></td><td><code>**</code></td></tr>
<tr><td><code>__lshift__</code>, <code>__rshift__</code></td><td><code>&lt;&lt;</code>, <code>&gt;&gt;</code></td></tr>
<tr><td><code>__and__</code>, <code>__xor__</code>, <code>__or__</code></td><td><code>&amp;</code>, <code>^</code>, <code>|</code></td></tr>
<tr><td><code>__neg__</code></td><td>унарный минус: <code>-a</code></td></tr>
<tr><td>Объект справа</td><td><code>__radd__</code>, <code>__rsub__</code>, <code>__rmul__</code> и другие с буквой r</td><td><code>1 + a</code>, <code>2 * a</code></td></tr>
<tr><td>Изменение на месте</td><td><code>__iadd__</code>, <code>__isub__</code> и другие с буквой i</td><td><code>a += 1</code>, <code>a *= 2</code></td></tr>
</table></div>
<p>Методы сравнения и арифметики объявляются с двумя параметрами, например <code>def __lt__(self, other)</code>. У __getitem__ параметры (self, key), у __call__ (self, *args, **kwargs). Полный список всех специальных методов есть в документации Python, раздел «Data model».</p>

<h3>Метод __repr__</h3>
<p>Для отладки и для показа объектов внутри списков существует метод [[__repr__|__repr__]]. Он возвращает строку, по которой видно, как можно было бы создать такой объект. Сравним, как ведут себя оба метода:</p>
''' + ex('''class Cat:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name}, {self.age} лет"

    def __repr__(self):
        return f"Cat('{self.name}', {self.age})"


tom = Cat("Том", 3)
print(tom)
print(repr(tom))
print([tom, Cat("Мурка", 5)])''') + '''
<p>Видно разделение ролей. Одиночный объект печатается через __str__, это красивый вариант для человека. А внутри списка Python использует __repr__, более точное представление. Если определён только __repr__, то print одиночного объекта тоже его использует. Поэтому, если нужно писать один метод, то обычно пишут __repr__.</p>
'''
    th3 = th('Магические методы: __str__ и __repr__', terms3, body3)

    fl3 = fl('Вопросы: магические методы', [
        q('Что такое магический метод?', 'Метод с двойными подчёркиваниями, его вызывает Python', ['Метод, который нельзя вызывать', 'Метод базового класса object', 'Метод, который скрыт от наследников'], 'Имена вроде __str__ или __add__ связаны со встроенными операциями. Python вызывает их при выполнении этих операций.'),
        q('Какой метод вызывается при print(obj), если он определён?', '__str__', ['__print__', '__show__', '__init__'], 'print сначала преобразует объект в строку функцией str(), а str() вызывает метод __str__.'),
        qo('Что выведет программа?', '''class Cat:

    def __str__(self):
        return "кот"


print(Cat())''', ['кот', '__str__', 'Cat'], 'print вызвал str(), а тот метод __str__, который вернул строку "кот".'),
        qo('Что выведет программа?', '''class Cat:

    def __str__(self):
        return "кот"

    def __repr__(self):
        return "Cat()"


print([Cat()])''', ['[Cat()]', '[кот]', '[<Cat>]'], 'Внутри списка элементы показываются через __repr__, а не __str__.'),
        qo('Что выведет программа?', '''class Cat:

    def __str__(self):
        return "кот"

    def __repr__(self):
        return "Cat()"


print(Cat(), repr(Cat()))''', ['кот Cat()', 'Cat() Cat()', 'кот кот'], 'print одиночного объекта использует __str__, а функция repr всегда вызывает __repr__.'),
        qo('Что выведет программа?', '''class Cat:

    def __repr__(self):
        return "Cat()"


print(Cat())''', ['Cat()', '<__main__.Cat object>', 'Ошибка'], 'Если определён только __repr__, то print использует его вместо отсутствующего __str__.'),
        qo('Что выведет программа?', '''class Bag:

    def __init__(self, items):
        self.items = items

    def __len__(self):
        return len(self.items)


print(len(Bag([1, 2, 3])))''', ['3', '1', 'Ошибка'], 'Функция len вызывает метод __len__ у объекта. Он вернул длину списка внутри.'),
        qo('Что выведет программа?', '''class Adder:

    def __call__(self, x):
        return x + 1


f = Adder()
print(f(5))''', ['6', '5', 'Ошибка'], 'Метод __call__ позволяет вызывать объект как функцию: f(5) превращается в вызов f.__call__(5).'),
        q('Какой метод позволяет вызывать объект как функцию: obj(...)?', '__call__', ['__run__', '__func__', '__init__'], 'Если у класса есть __call__, то его объекты можно вызывать с круглыми скобками.'),
        q('Какой метод вызывается при выражении obj[key]?', '__getitem__', ['__get__', '__index__', '__item__'], '__getitem__ отвечает за получение элемента по ключу или индексу. Для присваивания есть __setitem__, для удаления __delitem__.'),
        q('Какому оператору соответствует метод __eq__?', '==', ['=', '!=', 'is'], '__eq__ определяет равенство объектов (a == b). Для неравенства есть отдельный метод __ne__.'),
        q('Как называется возможность задать поведение операторов для своих классов?', 'Перегрузка операторов', ['Наследование', 'Инкапсуляция', 'Утиная типизация'], 'Определив магические методы, мы «перегружаем» операторы и встроенные функции для собственных объектов.'),
    ])

    # ============ Теория 4: арифметика и сравнение ============
    terms4 = [
        ('__add__', 'Магический метод: определяет, что делает оператор + для объектов класса. Вызывается для a + b, где объект a стоит слева. Обычно возвращает новый объект.\n\nПример:\nclass N:\n    def __init__(self, v):\n        self.v = v\n    def __add__(self, other):\n        return N(self.v + other.v)\nprint((N(1) + N(2)).v)\nВывод:\n3'),
        ('__radd__', 'Магический метод: срабатывает для a + b, когда слева стоит объект, не умеющий складываться (например, число), а справа объект нашего класса.\n\nПример:\nclass N:\n    def __init__(self, v):\n        self.v = v\n    def __radd__(self, other):\n        return other + self.v\nprint(5 + N(2))\nВывод:\n7'),
        ('__iadd__', 'Магический метод: определяет a += b. Должен изменить объект на месте и обязательно вернуть self, иначе после операции в переменной окажется None.\n\nПример:\nclass N:\n    def __init__(self, v):\n        self.v = v\n    def __iadd__(self, other):\n        self.v += other\n        return self\na = N(1)\na += 4\nprint(a.v)\nВывод:\n5'),
        ('total_ordering', 'Декоратор из модуля functools. Если в классе определены __eq__ и один из методов сравнения (например, __lt__), он сам создаёт остальные: <=, > и >=.\n\nПример:\nfrom functools import total_ordering\n@total_ordering\nclass N:\n    def __init__(self, v):\n        self.v = v\n    def __eq__(self, other):\n        return self.v == other.v\n    def __lt__(self, other):\n        return self.v < other.v\nprint(N(2) >= N(1))\nВывод:\nTrue'),
    ]
    body4 = '''
<p>Магические методы делают классы выразительными: объекты начинают вести себя как встроенные типы. Рассмотрим, как задаются арифметические операции и сравнение.</p>

<h3>Сложение: __add__, __radd__ и __iadd__</h3>
<p>Для сложения есть сразу три метода, и Python выбирает нужный по тому, как записана операция. Покажем это на небольшом классе, где каждый метод сообщает о себе:</p>
''' + ex('''class A:

    def __init__(self):
        self.value = 10

    def __add__(self, other):
        return "Выполняется метод __add__."

    def __radd__(self, other):
        return "Выполняется метод __radd__."

    def __iadd__(self, other):
        self.value += other
        return self

    def __str__(self):
        return f"value: {self.value}."


a = A()
print(a + 1)
print(1 + a)
a += 1
print(a)''') + '''
<ul>
<li>выражение <code>a + 1</code> вызывает [[__add__|__add__]] у объекта слева;</li>
<li>выражение <code>1 + a</code>: число 1 не умеет складываться с нашим объектом, поэтому Python пробует метод [[__radd__|__radd__]] у объекта справа (буква r означает right, «справа»);</li>
<li>выражение <code>a += 1</code> вызывает [[__iadd__|__iadd__]]. Он меняет сам объект, и поэтому в конце обязательно <code>return self</code>.</li>
</ul>
<p>Почему так важен return self? Операция <code>a += 1</code> работает как присваивание <code>a = a.__iadd__(1)</code>. Если метод ничего не вернёт, то в переменной a окажется None:</p>
''' + ex('''class A:

    def __init__(self):
        self.value = 10

    def __iadd__(self, other):
        self.value += other


a = A()
a += 1
print(a)''') + '''
<p>Если же метод __iadd__ вообще не определён, то <code>a += b</code> превращается в обычное <code>a = a + b</code>. Тогда создаётся новый объект, а переменная теперь указывает на него. Вот разница, которую стоит знать:</p>
''' + ex('''class N:

    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return N(self.value + other)


class M(N):

    def __iadd__(self, other):
        self.value += other
        return self


a = N(1)
b = a
a += 5
print(a.value, b.value, a is b)

c = M(1)
d = c
c += 5
print(c.value, d.value, c is d)''') + '''
<p>В первом случае (только __add__) переменная a теперь указывает на новый объект со значением 6, а b осталась на старом. Во втором (есть __iadd__) объект изменился «на месте», и обе переменные видят изменение. Именно так ведут себя встроенные типы: у списка += меняет сам список, а у числа создаёт новое число.</p>

<h3>Сложение объектов друг с другом</h3>
<p>С помощью __add__ можно «сложить» два автомобиля в один, суммируя их характеристики. Вместе с __repr__ из прошлого раздела получится так:</p>
''' + ex(CAR_CLASS + '\n' + ELEC_SUB + ELEC_STR + ELEC_REPR + ELEC_ADD + '''

electric_car = ElectricCar(color="белый", consumption=15, bat_capacity=90)
electric_car_1 = ElectricCar(color="чёрный", consumption=17, bat_capacity=80)
print(repr(electric_car))
print([electric_car, electric_car_1])
electric_car.start_engine()
electric_car_1.start_engine()
electric_car.drive(300)
electric_car_1.drive(100)
new_electric_car = electric_car + electric_car_1
print(new_electric_car)''') + '''
<p>Метод __add__ создаёт <b>новый</b> объект и не трогает исходные. Так принято: оператор + не должен менять слагаемые.</p>

<h3>Сравнение объектов</h3>
<p>Чтобы объекты можно было сравнивать, определяют методы сравнения. Рассмотрим класс «деньги» (значение в копейках). Нам достаточно __eq__ (равенство) и __lt__ (меньше). Остальные операции можно вывести из этих двух: <i>a &gt; b</i> это то же, что <i>b &lt; a</i>, а <i>a &lt;= b</i> то же, что «a меньше b или равно b». Чтобы не писать все шесть методов вручную, есть декоратор [[total_ordering|functools.total_ordering]]. Он достроит недостающие методы по двум, которые ты написал:</p>
''' + ex('''from functools import total_ordering


@total_ordering
class Money:

    def __init__(self, kopecks):
        self.kopecks = kopecks

    def __eq__(self, other):
        return self.kopecks == other.kopecks

    def __lt__(self, other):
        return self.kopecks < other.kopecks

    def __repr__(self):
        return f"Money({self.kopecks})"


a = Money(150)
b = Money(300)
print(a < b, a <= b, a > b, a >= b, a == b, a != b)
print(sorted([b, a, Money(100)]))
print(max(Money(5), Money(7)))''') + '''
<p>Раз у объектов есть сравнение, к ним применимы sorted и max: они используют именно операции сравнения. Одна оговорка: если в классе определён __eq__, то объекты по умолчанию перестают быть хешируемыми, то есть их нельзя класть во множества и использовать как ключи словарей. Это нормально для изменяемых объектов, но имей в виду.</p>

<h3>Класс как коллекция: __len__, __getitem__ и __contains__</h3>
<p>Ещё пара магических методов делает объект похожим на список. Определим плейлист, у которого можно спросить длину, достать песню по номеру и проверить, есть ли песня:</p>
''' + ex('''class Playlist:

    def __init__(self, *songs):
        self.songs = list(songs)

    def __len__(self):
        return len(self.songs)

    def __getitem__(self, index):
        return self.songs[index]

    def __contains__(self, song):
        return song in self.songs


p = Playlist("Кино", "Ария", "Земфира")
print(len(p))
print(p[0], p[-1])
print("Ария" in p, "Metallica" in p)''') + '''
<p>Все эти возможности работают потому, что Python за кулисами вызывает те самые магические методы. Тебе остаётся лишь определить, что именно они должны делать.</p>
'''
    th4 = th('Магические методы: операторы и сравнение', terms4, body4)

    fl4 = fl('Вопросы: операторы и сравнение', [
        qo('Что выведет программа?', '''class N:

    def __init__(self, v):
        self.v = v

    def __add__(self, other):
        return N(self.v + other.v)


print((N(2) + N(3)).v)''', ['5', '23', 'Ошибка'], 'Оператор + вызывает __add__, а он создаёт новый объект N с суммой значений 2 + 3.'),
        qo('Что выведет программа?', '''class N:

    def __init__(self, v):
        self.v = v

    def __radd__(self, other):
        return self.v + other


print(10 + N(5))''', ['15', '10', 'Ошибка'], 'Число 10 не умеет складываться с N. Тогда Python вызывает __radd__ у объекта справа, other равно 10.'),
        qo('Что выведет программа?', '''class N:

    def __init__(self, v):
        self.v = v

    def __iadd__(self, other):
        self.v += other
        return self


a = N(1)
b = a
a += 4
print(b.v)''', ['5', '1', '4'], 'Метод __iadd__ изменил объект на месте и вернул self. Переменная b указывает на тот же объект, поэтому тоже видит 5.'),
        qo('Что выведет программа?', '''class N:

    def __init__(self, v):
        self.v = v

    def __add__(self, other):
        return N(self.v + other)


a = N(1)
b = a
a += 4
print(a.v, b.v)''', ['5 1', '5 5', '1 1'], 'Метода __iadd__ нет, поэтому a += 4 равно a = a + 4. Создался новый объект, а b осталась указывать на старый со значением 1.'),
        qo('Что выведет программа?', '''class N:

    def __init__(self, v):
        self.v = v

    def __iadd__(self, other):
        self.v += other


a = N(1)
a += 2
print(a)''', ['None', '3', 'Ошибка'], 'Метод __iadd__ не вернул self, поэтому в a записалось None. Нужно было дописать return self.'),
        q('Зачем __iadd__ должен возвращать self?', 'Результат метода записывается обратно в переменную', ['Чтобы объект нельзя было изменить', 'Без этого метод не вызывается', 'Это требование синтаксиса любого метода'], 'Операция a += b выполняется как a = a.__iadd__(b), поэтому то, что вернёт метод, станет значением a.'),
        q('Какие методы достаточно написать вместе с @total_ordering?', '__eq__ и один из __lt__, __le__, __gt__, __ge__', ['Только __init__', 'Все шесть методов сравнения', 'Только __str__'], 'Декоратор достраивает недостающие методы сравнения по равенству и любому одному сравнению «меньше/больше».'),
        qo('Что выведет программа?', '''from functools import total_ordering


@total_ordering
class N:

    def __init__(self, v):
        self.v = v

    def __eq__(self, other):
        return self.v == other.v

    def __lt__(self, other):
        return self.v < other.v


print(N(2) >= N(2), N(1) > N(2))''', ['True False', 'True True', 'False False'], 'Декоратор строит >= и > из __eq__ и __lt__. Числа равны, значит >= истинно. Единица не больше двойки.'),
        qo('Что выведет программа?', '''class V:

    def __init__(self, x):
        self.x = x

    def __neg__(self):
        return V(-self.x)


print((-V(5)).x)''', ['-5', '5', 'Ошибка'], 'Унарный минус (знак перед объектом) вызывает метод __neg__. Он вернул новый объект с противоположным значением.'),
        qo('Что выведет программа?', '''class V:

    def __init__(self, x):
        self.x = x

    def __eq__(self, other):
        return self.x == other.x


print(V(1) == V(1), V(1) is V(1))''', ['True False', 'True True', 'False False'], 'Равенство определили по полю x, поэтому объекты равны. Но это два разных объекта, оператор is вернёт False.'),
        qo('Что выведет программа?', '''class Row:

    def __init__(self, *items):
        self.items = list(items)

    def __getitem__(self, i):
        return self.items[i]


r = Row(10, 20, 30)
print(r[1] + r[-1])''', ['50', '30', 'Ошибка'], 'r[1] вызывает __getitem__(1) и даёт 20, r[-1] даёт 30. Сумма 50.'),
    ])

    # ============ Задания ============
    t1 = task('Напиши класс Animal: при создании он принимает имя животного. Метод speak() возвращает строку "...". Метод describe() возвращает строку вида «<имя> говорит: <то, что вернул speak()>». Затем напиши два класса-наследника: Dog (его speak возвращает "Гав!") и Cat (его speak возвращает "Мяу!"). Метод describe в наследниках переписывать не нужно.',
              'Базовый класс: __init__(self, name) сохраняет self.name, speak возвращает "...", describe возвращает f"{self.name} говорит: {self.speak()}". Наследники: class Dog(Animal): и в нём только def speak(self): return "Гав!". Метод describe унаследуется, но при вызове self.speak() Python выберет версию из класса самого объекта.',
              'class Animal:\n\n    def __init__(self, name):\n        self.name = name\n\n    def speak(self):\n        return "..."\n\n    def describe(self):\n        return f"{self.name} говорит: {self.speak()}"\n\n\nclass Dog(Animal):\n\n    def speak(self):\n        return "Гав!"\n\n\nclass Cat(Animal):\n\n    def speak(self):\n        return "Мяу!"',
              ['print(Animal("Рыба").describe())\nprint(Dog("Шарик").describe())\nprint(Cat("Мурка").describe())', 'class Cow(Animal):\n    def speak(self):\n        return "Му!"\n\nfor pet in (Cow("Бурёнка"), Dog("Рекс")):\n    print(pet.describe())', 'pets = [Dog("A"), Cat("B"), Animal("C")]\nprint(isinstance(pets[0], Animal), isinstance(pets[1], Dog), isinstance(pets[2], Cat))\nprint([p.speak() for p in pets])'], tail=TL)

    t2 = task('Напиши класс Point с атрибутами x и y и методами move(dx, dy) и length(other) (как в прошлой теме: сдвиг точки и расстояние до другой точки, округлённое до сотых). Затем напиши его наследника PatchedPoint, у которого три способа создания: без параметров (координаты (0, 0)), с одним параметром (кортеж с координатами) и с двумя (x и y). Для инициализации родителя используй super().',
              'Класс Point скопируй из прошлой темы. В PatchedPoint объяви def __init__(self, *args): и разбери случаи по длине args. Если args пустой, то x, y = 0, 0. Если в нём один элемент, то это кортеж: x, y = args[0]. Если два, то x, y = args. В конце вызови super().__init__(x, y).',
              'class Point:\n\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def move(self, dx, dy):\n        self.x += dx\n        self.y += dy\n\n    def length(self, other):\n        return round(((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5, 2)\n\n\nclass PatchedPoint(Point):\n\n    def __init__(self, *args):\n        if len(args) == 0:\n            x, y = 0, 0\n        elif len(args) == 1:\n            x, y = args[0]\n        else:\n            x, y = args\n        super().__init__(x, y)',
              ['point = PatchedPoint()\nprint(point.x, point.y)\npoint.move(2, -3)\nprint(point.x, point.y)', 'first_point = PatchedPoint((2, -7))\nsecond_point = PatchedPoint(7, 9)\nprint(first_point.length(second_point))\nprint(second_point.length(first_point))', 'p = PatchedPoint(5, 6)\nprint(p.x, p.y, isinstance(p, Point))'], tail=TL)

    t3 = task('Научим точки работать с операторами. Возьми класс PatchedPoint из прошлого задания (вместе с Point). Добавь метод __str__, чтобы print(точка) выводил координаты в виде «(x, y)». Добавь оператор +: выражение point + (dx, dy) создаёт НОВУЮ точку, смещённую на кортеж. Добавь оператор +=: point += (dx, dy) сдвигает саму точку и тоже работает (результат должен остаться той же точкой).',
              'Метод __str__ возвращает f"({self.x}, {self.y})". Метод __add__(self, delta) создаёт и возвращает новый объект: PatchedPoint(self.x + delta[0], self.y + delta[1]). Метод __iadd__(self, delta) меняет self.x и self.y на месте и в конце возвращает self. Без return self переменная после += станет None.',
              'class Point:\n\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def move(self, dx, dy):\n        self.x += dx\n        self.y += dy\n\n    def length(self, other):\n        return round(((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5, 2)\n\n\nclass PatchedPoint(Point):\n\n    def __init__(self, *args):\n        if len(args) == 0:\n            x, y = 0, 0\n        elif len(args) == 1:\n            x, y = args[0]\n        else:\n            x, y = args\n        super().__init__(x, y)\n\n    def __str__(self):\n        return f"({self.x}, {self.y})"\n\n    def __add__(self, delta):\n        return PatchedPoint(self.x + delta[0], self.y + delta[1])\n\n    def __iadd__(self, delta):\n        self.x += delta[0]\n        self.y += delta[1]\n        return self',
              ['point = PatchedPoint()\nprint(point)\nnew_point = point + (2, -3)\nprint(point, new_point, point is new_point)', 'first_point = second_point = PatchedPoint((2, -7))\nfirst_point += (7, 3)\nprint(first_point, second_point, first_point is second_point)', 'p = PatchedPoint(1, 1)\nq = p + (1, 1) + (1, 1)\nprint(p, q)'],
              exp={'point = PatchedPoint()\nprint(point)\nnew_point = point + (2, -3)\nprint(point, new_point, point is new_point)': '(0, 0)\n(0, 0) (2, -3) False', 'first_point = second_point = PatchedPoint((2, -7))\nfirst_point += (7, 3)\nprint(first_point, second_point, first_point is second_point)': '(9, -4) (9, -4) True'}, tail=TL)

    t4 = task('Напиши три класса. Flyer: при создании принимает speed (скорость полёта) и сохраняет её; метод fly() возвращает строку «Лечу со скоростью <speed>». Swimmer: принимает depth (глубину) и сохраняет; метод swim() возвращает «Ныряю на <depth>». Duck наследуется от обоих: принимает name, speed и depth, и сохраняет name; метод intro() возвращает «Я утка <имя>». Инициализацию обоих родителей вызывай явно по имени класса.',
              'Duck объявляется как class Duck(Flyer, Swimmer):. В его __init__(self, name, speed, depth) вызови Flyer.__init__(self, speed) и Swimmer.__init__(self, depth), а потом запиши self.name = name. Если вместо этого написать один super().__init__(...), инициализация Swimmer не запустится, и depth не появится.',
              'class Flyer:\n\n    def __init__(self, speed):\n        self.speed = speed\n\n    def fly(self):\n        return f"Лечу со скоростью {self.speed}"\n\n\nclass Swimmer:\n\n    def __init__(self, depth):\n        self.depth = depth\n\n    def swim(self):\n        return f"Ныряю на {self.depth}"\n\n\nclass Duck(Flyer, Swimmer):\n\n    def __init__(self, name, speed, depth):\n        Flyer.__init__(self, speed)\n        Swimmer.__init__(self, depth)\n        self.name = name\n\n    def intro(self):\n        return f"Я утка {self.name}"',
              ['d = Duck("Дональд", 40, 3)\nprint(d.intro())\nprint(d.fly())\nprint(d.swim())', 'd = Duck("Кряква", 70, 1)\nprint(d.speed, d.depth, d.name)\nprint(isinstance(d, Flyer), isinstance(d, Swimmer))', 'print([c.__name__ for c in Duck.__mro__])'], tail=TL)

    t5 = task('Начнём создавать класс Fraction для обыкновенных дробей. Дробь можно создать двумя способами: Fraction(a, b) из двух целых чисел и Fraction("a/b") из строки. Знаменатель может оказаться отрицательным: знак нужно перенести в числитель (например, 4 и -12 дадут -1/3). Дробь всегда хранится сокращённой, а для нуля знаменатель равен 1. Методы numerator() и denominator() возвращают числитель и знаменатель. Метод __str__ возвращает дробь в виде «числитель/знаменатель», например «1/3» или «-1/3». Метод __repr__ возвращает строку «Fraction(\'1/3\')», по которой можно создать такую же дробь. Оператор унарный минус (-a) возвращает новую дробь с противоположным знаком. Деление на ноль считай невозможным (проверять не надо). Все вспомогательные поля называй с подчёркиванием.',
              'Для сокращения нужен наибольший общий делитель: from math import gcd. Сначала разбери вход: если a это строка, раздели её методом split("/") на две части и преврати обе в int. Если знаменатель отрицательный, поменяй знак у обоих чисел. Потом найди g = gcd(числитель, знаменатель) и поделись на него нацело (//). Храни результат в self._n и self._d. __neg__ возвращает Fraction(-self._n, self._d), а __repr__ можно записать как f"Fraction(\'{self}\')": f-строка сама вызовет __str__.',
              'from math import gcd\n\n\nclass Fraction:\n\n    def __init__(self, a, b=1):\n        if isinstance(a, str):\n            a, b = (a.split("/") + ["1"])[:2]\n            a = int(a)\n            b = int(b)\n        if b < 0:\n            a, b = -a, -b\n        g = gcd(a, b)\n        self._n = a // g\n        self._d = b // g\n\n    def numerator(self):\n        return self._n\n\n    def denominator(self):\n        return self._d\n\n    def __str__(self):\n        return f"{self._n}/{self._d}"\n\n    def __repr__(self):\n        return f"Fraction(\'{self}\')"\n\n    def __neg__(self):\n        return Fraction(-self._n, self._d)',
              ['a = Fraction(1, 3)\nb = Fraction(-2, -6)\nc = Fraction(-3, 9)\nd = Fraction(4, -12)\nprint(a, b, c, d)\nprint(*map(repr, (a, b, c, d)))', 'a = Fraction("-1/2")\nb = -a\nprint(a, b, a is b)\nprint(a.numerator(), a.denominator())\nprint(b.numerator(), b.denominator())', 'print(Fraction(0, 5), Fraction("6/4"), Fraction(10, 5))', 'print([Fraction(1, 2), Fraction("3/-9")])'],
              exp={'a = Fraction(1, 3)\nb = Fraction(-2, -6)\nc = Fraction(-3, 9)\nd = Fraction(4, -12)\nprint(a, b, c, d)\nprint(*map(repr, (a, b, c, d)))': "1/3 1/3 -1/3 -1/3\nFraction('1/3') Fraction('1/3') Fraction('-1/3') Fraction('-1/3')"}, tail=TL)

    FR1 = 'from math import gcd\n\n\nclass Fraction:\n\n    def __init__(self, a, b=1):\n        if isinstance(a, str):\n            a, b = (a.split("/") + ["1"])[:2]\n            a = int(a)\n            b = int(b)\n        if b < 0:\n            a, b = -a, -b\n        g = gcd(a, b)\n        self._n = a // g\n        self._d = b // g\n\n    def numerator(self):\n        return self._n\n\n    def denominator(self):\n        return self._d\n\n    def __str__(self):\n        return f"{self._n}/{self._d}"\n\n    def __repr__(self):\n        return f"Fraction(\'{self}\')"\n\n    def __neg__(self):\n        return Fraction(-self._n, self._d)'

    t6 = task('Продолжим класс Fraction (напиши его целиком вместе с тем, что было в прошлом задании). Добавь бинарные операторы. + и - создают НОВУЮ дробь (слагаемые не меняются). += и -= изменяют дробь слева (результат остаётся той же дробью, на которую указывает переменная). Результаты всегда сокращены.',
              'Сложение дробей: a/b + c/d = (a*d + c*b) / (b*d). Метод __add__(self, other) возвращает Fraction(self._n * other._d + other._n * self._d, self._d * other._d). Вычитание сведи к сложению: self + (-other). Метод __iadd__ посчитай через __add__ и перепиши результат в свои поля: result = self + other; self._n = result._n; self._d = result._d; потом return self. __isub__ делается так же.',
              FR1 + '\n\n    def __add__(self, other):\n        return Fraction(self._n * other._d + other._n * self._d, self._d * other._d)\n\n    def __sub__(self, other):\n        return self + (-other)\n\n    def __iadd__(self, other):\n        result = self + other\n        self._n = result._n\n        self._d = result._d\n        return self\n\n    def __isub__(self, other):\n        result = self - other\n        self._n = result._n\n        self._d = result._d\n        return self',
              ['a = Fraction(1, 3)\nb = Fraction(1, 2)\nc = a + b\nprint(a, b, c, a is c, b is c)', 'a = Fraction(1, 8)\nc = b = Fraction(3, 8)\nb -= a\nprint(a, b, c, b is c)', 'a = Fraction(1, 2)\nb = Fraction(1, 2)\nprint(a + b, a - b, b - a)', 'x = Fraction(1, 6)\ny = x\nx += Fraction(1, 3)\nx += Fraction(1, 2)\nprint(x, y)'],
              exp={'a = Fraction(1, 3)\nb = Fraction(1, 2)\nc = a + b\nprint(a, b, c, a is c, b is c)': '1/3 1/2 5/6 False False', 'a = Fraction(1, 8)\nc = b = Fraction(3, 8)\nb -= a\nprint(a, b, c, b is c)': '1/8 1/4 1/4 True'}, tail=TL)

    FR2 = FR1 + '\n\n    def __add__(self, other):\n        return Fraction(self._n * other._d + other._n * self._d, self._d * other._d)\n\n    def __sub__(self, other):\n        return self + (-other)\n\n    def __iadd__(self, other):\n        result = self + other\n        self._n = result._n\n        self._d = result._d\n        return self\n\n    def __isub__(self, other):\n        result = self - other\n        self._n = result._n\n        self._d = result._d\n        return self'

    t7 = task('Научим дроби сравниваться. Возьми класс Fraction из прошлого задания и добавь все шесть операций сравнения: ==, !=, <, <=, >, >=. Подсказка: достаточно написать __eq__ и __lt__, а остальные методы создаст декоратор functools.total_ordering. После этого дроби можно сортировать функцией sorted.',
              'Импортируй декоратор: from functools import total_ordering, и поставь @total_ordering над классом. __eq__ сравнивай по числителю и знаменателю (дроби всегда сокращены, поэтому равные дроби хранятся одинаково): self._n == other._n and self._d == other._d. Для __lt__ приведи дроби к общему знаменателю: self._n * other._d < other._n * self._d (знаменатели положительные, знак неравенства сохраняется).',
              'from functools import total_ordering\n' + FR2.replace('class Fraction:', '@total_ordering\nclass Fraction:', 1) + '\n\n    def __eq__(self, other):\n        return self._n == other._n and self._d == other._d\n\n    def __lt__(self, other):\n        return self._n * other._d < other._n * self._d',
              ['a = Fraction(1, 3)\nb = Fraction(1, 2)\nprint(a > b, a < b, a >= b, a <= b, a == b, a != b)', 'a = Fraction(1, 3)\nb = Fraction(2, 6)\nprint(a > b, a < b, a >= b, a <= b, a == b, a != b)', 'fr = [Fraction(1, 2), Fraction(-1, 3), Fraction(3, 4), Fraction(0)]\nprint(sorted(fr))\nprint(max(fr), min(fr))'], tail=TL)

    t8 = task('Мы знаем, что целые числа тоже являются дробями. Доработай класс Fraction (напиши целиком, вместе со сравнениями из прошлого задания). Дробь должна создаваться и из одного целого числа: Fraction(5) и Fraction("5") дают 5/1. Дроби и целые числа должны работать вместе в операциях +, -, *, / и в сравнениях, причём число может стоять и слева, и справа от дроби: Fraction(1, 2) + 1, 2 * Fraction(1, 3), 1 - Fraction(1, 4), 3 / Fraction(3, 2). Обычные числа с плавающей точкой поддерживать не нужно, только целые. Результат операции с дробями это всегда дробь.',
              'Заведи вспомогательный метод, который превращает число в дробь: если other это int, верни Fraction(other), иначе верни other. Вызывай его в начале каждого оператора. Для операции с числом слева реализуй «зеркальные» методы __radd__, __rsub__, __rmul__ и __rtruediv__: в них self это дробь, а other число слева. __radd__ и __rmul__ равны прямым версиям. __rsub__ считай как Fraction(other) - self, а __rtruediv__ как Fraction(other) / self. Умножение: (a*c)/(b*d). Деление: (a*d)/(b*c).',
              'from functools import total_ordering\nfrom math import gcd\n\n\n@total_ordering\nclass Fraction:\n\n    def __init__(self, a, b=1):\n        if isinstance(a, str):\n            a, b = (a.split("/") + ["1"])[:2]\n            a = int(a)\n            b = int(b)\n        if b < 0:\n            a, b = -a, -b\n        g = gcd(a, b)\n        self._n = a // g\n        self._d = b // g\n\n    def _wrap(self, other):\n        if isinstance(other, int):\n            return Fraction(other)\n        return other\n\n    def numerator(self):\n        return self._n\n\n    def denominator(self):\n        return self._d\n\n    def __str__(self):\n        return f"{self._n}/{self._d}"\n\n    def __repr__(self):\n        return f"Fraction(\'{self}\')"\n\n    def __neg__(self):\n        return Fraction(-self._n, self._d)\n\n    def __add__(self, other):\n        other = self._wrap(other)\n        return Fraction(self._n * other._d + other._n * self._d, self._d * other._d)\n\n    def __radd__(self, other):\n        return self + other\n\n    def __sub__(self, other):\n        return self + (-self._wrap(other))\n\n    def __rsub__(self, other):\n        return Fraction(other) - self\n\n    def __mul__(self, other):\n        other = self._wrap(other)\n        return Fraction(self._n * other._n, self._d * other._d)\n\n    def __rmul__(self, other):\n        return self * other\n\n    def __truediv__(self, other):\n        other = self._wrap(other)\n        return Fraction(self._n * other._d, self._d * other._n)\n\n    def __rtruediv__(self, other):\n        return Fraction(other) / self\n\n    def __eq__(self, other):\n        other = self._wrap(other)\n        return self._n == other._n and self._d == other._d\n\n    def __lt__(self, other):\n        other = self._wrap(other)\n        return self._n * other._d < other._n * self._d',
              ['a = Fraction(1)\nb = Fraction("2")\nprint(a, b, a + 2, b - 1)\nprint(a > b, a + 2 > b - 1)', 'a = Fraction(1, 2)\nb = Fraction("2/3")\nprint(a + 1, 2 * a, 3 - a, 2 / b)\nprint(a >= 1, b >= 1, a < 1, 1 > b)', 'x = Fraction(1, 3)\nprint(x * 3, x / 2, 1 / x, 6 / x, x * x)\nprint(x == 0, Fraction(0) == 0, Fraction(4, 2) == 2)', 'print(sum([Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)]))'], tail=TL)

    t9 = task('Напиши класс Multiplier: он принимает число k и создаёт объект, который можно вызывать как функцию. Вызов m(x) возвращает k * x. Кроме того, объект запоминает, сколько раз его вызывали: метод calls() возвращает это число. У каждого множителя свой счётчик. Метод __repr__ возвращает строку «Multiplier(k)».',
              'Чтобы объект можно было вызвать со скобками, нужен магический метод __call__(self, x). В __init__ сохрани k и заведи счётчик self._calls = 0. В __call__ увеличивай счётчик и возвращай self._k * x. Метод calls() возвращает счётчик. __repr__ собери f-строкой: f"Multiplier({self._k})".',
              'class Multiplier:\n\n    def __init__(self, k):\n        self._k = k\n        self._calls = 0\n\n    def __call__(self, x):\n        self._calls += 1\n        return self._k * x\n\n    def calls(self):\n        return self._calls\n\n    def __repr__(self):\n        return f"Multiplier({self._k})"',
              ['triple = Multiplier(3)\nprint(triple(5), triple(10))\nprint(triple.calls())\nprint(triple)', 'a = Multiplier(2)\nb = Multiplier(10)\nprint(a(1), a(2), a(3), b(1))\nprint(a.calls(), b.calls())', 'print(list(map(Multiplier(4), [1, 2, 3])))\nprint([Multiplier(1), Multiplier(7)])'], tail=TL)

    t10 = task('Напиши класс Vector для векторов произвольной длины: Vector(1, 2, 3). Вектор должен уметь: показываться как «Vector(1, 2, 3)» (метод __repr__); выдавать длину через len(); выдавать компоненту по индексу v[i]; складываться с другим вектором той же длины (v + w даёт новый вектор из сумм компонент); умножаться на число с любой стороны (v * 2 и 2 * v дают новый вектор); сравниваться на равенство (==) с другим вектором.',
               'Компоненты храни в списке (в __init__ с параметром *items): self._items = list(items). __len__ возвращает длину списка, __getitem__(self, i) возвращает self._items[i]. В __add__ собери новые компоненты через zip: Vector(*[a + b for a, b in zip(self._items, other._items)]). Для умножения на число сделай __mul__, а __rmul__ пусть просто вызывает self * number. __eq__ сравнивает списки компонент. Для __repr__ удобно ", ".join(map(str, self._items)).',
               'class Vector:\n\n    def __init__(self, *items):\n        self._items = list(items)\n\n    def __repr__(self):\n        return "Vector(" + ", ".join(map(str, self._items)) + ")"\n\n    def __len__(self):\n        return len(self._items)\n\n    def __getitem__(self, i):\n        return self._items[i]\n\n    def __add__(self, other):\n        return Vector(*[a + b for a, b in zip(self._items, other._items)])\n\n    def __mul__(self, number):\n        return Vector(*[a * number for a in self._items])\n\n    def __rmul__(self, number):\n        return self * number\n\n    def __eq__(self, other):\n        return self._items == other._items',
               ['v = Vector(1, 2, 3)\nw = Vector(10, 20, 30)\nprint(v, len(v), v[0], v[-1])\nprint(v + w)', 'v = Vector(1, 2, 3)\nprint(v * 2)\nprint(2 * v)\nprint(v * 0.5)', 'a = Vector(1, 2)\nb = Vector(1, 2)\nprint(a == b, a is b, a == Vector(2, 1))\nprint(a + b == 2 * a)', 'print(Vector(), len(Vector()))\nprint(Vector(5) + Vector(-5))'], tail=TL)

    ts1 = ts('Задания: наследование и магические методы', [t1, t2, t3, t9, t4, t5, t6, t7, t8, t10])

    return topic('Наследование и магические методы', 'наследование, super, MRO, __str__, __repr__, __add__, сравнение, __call__', [th1, fl1, th2, fl2, th3, fl3, th4, fl4, ts1])
