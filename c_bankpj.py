"""Большой проект «Банк» (тема 25): модель банка на классах. Исходник решений лежит в bankpj_src.txt с пометками этапов:
   #<N-M> — код есть в решении этапов с N по M (в стартовом коде этапа K есть то, что относится к этапам до K-1),
   #<gN-M> — готовый код, который выдаётся ученику уже на этапе N, #<tN> — заготовка-комментарий только в стартовом коде этапа N."""
import re
from dsl import *


def _pick(k, mode):
    out = []
    on = True
    for line in open('bankpj_src.txt', encoding='utf-8').read().split('\n'):
        if line == '#<>':
            on = True
            continue
        m = re.match(r'#<([gt]?)(\d+)(?:-(\d+|\*))?>$', line)
        if m:
            kind, lo, hi = m.group(1), int(m.group(2)), m.group(3)
            hi = 999 if hi in (None, '*') else int(hi)
            if kind == 'g':
                on = lo <= k <= hi
            elif kind == 't':
                on = mode == 'start' and k == lo
            else:
                kk = k if mode == 'sol' else k - 1
                on = lo <= kk <= hi
            continue
        if on:
            out.append(line)
    return re.sub(r'\n{4,}', '\n\n\n', '\n'.join(out)).strip('\n') + '\n'


def _fig(key, alt, cap):
    return '<figure class="fig"><img class="figi" data-x="p-' + key + '" alt="' + alt + '"></figure><p class="mu" style="margin:-6px 0 12px;font-size:.88rem">' + cap + '</p>'


def _out(code, lines=None):
    return run(code.strip('\n'), lines)[0].rstrip('\n')


# помощники для примеров в теории: те же функции, что выдаются ученику в стартовом коде
HELP = '''from datetime import datetime, timedelta

BINS = {"MIR": "220400", "VISA": "400000", "MASTERCARD": "510000"}


def luhn_digit(body):
    total = 0
    for i, ch in enumerate(reversed(body)):
        d = int(ch)
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return str((10 - total % 10) % 10)


def make_pan(system, serial):
    body = BINS[system] + str(serial).zfill(9)
    return body + luhn_digit(body)


def make_account_number(bic, serial):
    head = "40817810"
    tail = "0000" + str(serial).zfill(7)
    probe = bic[-3:] + head + "0" + tail
    weights = [7, 1, 3] * 8
    total = sum(int(d) * w % 10 for d, w in zip(probe, weights))
    return head + str(total % 10 * 3 % 10) + tail
'''


def build():
    # ============ Теория 1: что мы строим ============
    terms1 = [
        ('бэкенд', 'Серверная часть приложения: «машинное отделение», которого пользователь не видит. Приложение на телефоне только показывает кнопки и цифры, а проверять данные, хранить информацию и выполнять операции должен бэкенд. В этой теме ты напишешь бэкенд-часть банка: классы, которые умеют выпускать карты и проводить операции.\n\nПример:\nclass Counter:\n    def __init__(self):\n        self.value = 0\n\n    def add(self):\n        self.value += 1\n\nc = Counter()\nc.add()\nc.add()\nprint(c.value)\nВывод:\n2'),
        ('транзакция', 'Запись об одной денежной операции: пополнение, перевод, покупка или начисление процентов. Каждая операция в банке оставляет такую запись, поэтому по журналу транзакций можно восстановить всю историю денег.\n\nПример:\nlog = []\nlog.append(("deposit", 100))\nlog.append(("pay", 45))\nprint(len(log), log[-1])\nВывод:\n2 (\'pay\', 45)'),
    ]
    body1 = '''
<p>До сих пор твои программы были короткими: одна идея, один файл, один результат. Теперь у нас большой проект: симуляция бэкенда банковского приложения. Если ты хоть раз пользовался банковским приложением на телефоне, то видел только его лицо: экран, кнопки, цифры баланса. А за ним стоит [[бэкенд|бэкенд]]: программа, которая заводит клиентов и карты, проверяет, хватает ли денег, не слишком ли большая сумма, не заблокирована ли карта, и записывает каждую операцию в журнал. Именно его мы и напишем.</p>
<p>Проект «со звёздочкой»: он объёмнее обычных заданий, и это нормально. Здесь нет ничего нового про циклы или строки. Главное, что нужно: умение держать в голове много связанных объектов и аккуратно двигаться шаг за шагом. Если что-то не получается, остановись, перечитай теорию, посмотри подсказки и возвращайся. Через пять этапов у тебя будет работающий мини-банк.</p>
''' + _fig('bank_tasks', 'Структура проекта: пять задач, первые три это фундамент, две последние поддержка работы приложения', 'Пять этапов проекта. Первые три строят «фундамент»: карты, операции и новые типы карт. Последние два заставляют приложение работать надёжно: ловить ошибки и обрабатывать команды пользователя.') + '''
<h3>Из каких классов состоит банк</h3>
<p>Всё, что есть в банке, описывается пятью классами. Из них при работе программы создаются настоящие объекты: один банк, много клиентов, счетов, карт и операций.</p>
<table>
<tr><th>Класс</th><th>За что отвечает</th></tr>
<tr><td><code>Bank</code></td><td>выпускает карты и хранит всё, что было выпущено и проведено: клиентов, счета, карты, журнал транзакций</td></tr>
<tr><td><code>User</code></td><td>клиент банка: фамилия, имя, ПИН-код, телефон, его счета и карты</td></tr>
<tr><td><code>Account</code></td><td>счёт: номер, баланс, накопленный кешбэк и владелец</td></tr>
<tr><td><code>Card</code></td><td>банковская карта: её данные и все действия с ней: баланс, пополнение, покупка, перевод</td></tr>
<tr><td><code>Transaction</code></td><td>запись об одной операции (появится на втором этапе)</td></tr>
</table>
<p>Обрати внимание: карта и счёт это разные вещи. Деньги лежат на <b>счёте</b>, а <b>карта</b> лишь инструмент, чтобы ими распоряжаться. У клиента может быть несколько карт, и у каждой в нашем банке свой счёт.</p>
<h3>План работы</h3>
<ol>
<li><b>Заявка на карту.</b> Клиент приходит в банк, банк заводит ему счёт и выпускает карту. Все объекты связываются друг с другом.</li>
<li><b>Работа с картой.</b> Пополнение, покупки, переводы между картами, смена ПИН-кода, закрытие карты и журнал транзакций.</li>
<li><b>Новые типы карт.</b> Дебетовая карта с кешбэком и накопительный счёт с процентами. Это наследование.</li>
<li><b>Правила и ошибки.</b> Банк не должен ломаться от неверных данных: проверяем ввод, лимиты и права, а на нарушения отвечаем своими исключениями.</li>
<li><b>Командная строка банка.</b> Программа читает команды пользователя, выполняет их и сообщает, что пошло не так, а в конце печатает статистику ошибок.</li>
</ol>
<p>Каждый этап это отдельный мини-проект. В редакторе тебя ждёт заготовка: код предыдущих этапов уже написан, поэтому, даже если какой-то этап не получился, следующий ты сможешь начать с готовой основы. Проверка запускает тестовый сценарий (его текст виден в примере) и сравнивает печать программы с эталонной.</p>
<p>Перед проектом мы разберём три новых инструмента: <b>Enum</b> (набор допустимых значений), <b>dataclass</b> (быстрые классы для данных) и <b>дерево ошибок</b> (как организовать свои исключения). Они пригодятся, чтобы написать банк аккуратно, как это делают настоящие разработчики.</p>
<p><b>Важно:</b> деньги в реальных банках хранят не в обычных дробных числах, а в специальном типе Decimal (почему, расскажем чуть позже). Чтобы тебе было проще, в нашем проекте суммы это обычные числа с плавающей точкой <code>float</code>.</p>
'''
    th1 = th('О проекте: что мы строим', terms1, body1)

    # ============ Теория 2: Enum ============
    terms2 = [
        ('Enum', 'Специальный класс из модуля enum для набора допустимых значений с понятными именами. Вместо «магических» строк и чисел ты описываешь все варианты один раз, а потом пользуешься ими по имени.\n\nКласс-наследник Enum превращает каждый вариант в объект: у него есть имя .name и значение .value. Сравнивать варианты можно через == и is, перебирать циклом for, находить по значению: Класс("значение").\n\nПример:\nfrom enum import Enum\n\nclass Color(Enum):\n    RED = "red"\n    GREEN = "green"\n\nprint(Color.RED)\nprint(Color.RED.name, Color.RED.value)\nprint(Color("green"))\nВывод:\nColor.RED\nRED red\nColor.GREEN'),
    ]
    code_bug = '''status = "Active"
if status == "Activ":
    print("Карта активна")
else:
    print("Неизвестный статус")'''
    code_enum1 = '''from enum import Enum


class CardStatus(Enum):
    ACTIVE = "Active"
    BLOCKED = "Blocked"
    CLOSED = "Closed"


status = CardStatus.ACTIVE
print(status)
print(status.name)
print(status.value)
print(type(status).__name__)'''
    code_enum2 = '''from enum import Enum


class CardStatus(Enum):
    ACTIVE = "Active"
    BLOCKED = "Blocked"
    CLOSED = "Closed"


print(CardStatus("Blocked"))
print(CardStatus["CLOSED"])
status = CardStatus.ACTIVE
print(status == CardStatus.ACTIVE, status == CardStatus.CLOSED)
print(status is CardStatus.ACTIVE)
print(status == "Active")
for s in CardStatus:
    print(s.name, "->", s.value)
print(len(CardStatus))
print(list(CardStatus)[0])'''
    code_enum3 = '''from enum import Enum


class CardStatus(Enum):
    ACTIVE = "Active"
    BLOCKED = "Blocked"
    CLOSED = "Closed"


class Card:
    def __init__(self):
        self.status = CardStatus.ACTIVE

    def block(self):
        self.status = CardStatus.BLOCKED

    def info(self):
        return f"Статус карты: {self.status.value}"


card = Card()
print(card.info())
card.block()
print(card.info())
if card.status == CardStatus.BLOCKED:
    print("Операции запрещены")'''
    body2 = '''
<p>В банке полно «ограниченных множеств»: у карты может быть всего три состояния (активна, заблокирована, закрыта), у операции четыре вида (пополнение, перевод, покупка, проценты). Можно хранить их строками, но тогда легко ошибиться. Смотри, что бывает:</p>
''' + ex(code_bug) + '''
<p>Статус в карте записан правильно («Active»), а в проверке мы случайно написали «Activ». Ошибки нет, программа спокойно работает, просто делает не то. В большом проекте таких мест десятки, а искать опечатки в строках очень тяжело. Помогает класс [[Enum|Enum]] (от англ. enumeration, «перечисление»).</p>
<h3>Как описать Enum</h3>
<p>Пишем класс, который наследуется от <code>Enum</code>, и перечисляем варианты. Слева имя варианта (принято писать ЗАГЛАВНЫМИ), справа его значение:</p>
''' + ex(code_enum1) + '''
<p>Разберём вывод. <code>print(status)</code> показывает <code>CardStatus.ACTIVE</code>: имя класса и имя варианта. Свойство <code>.name</code> это имя варианта («ACTIVE»), а <code>.value</code> это то значение, которое мы записали справа («Active»). Каждый вариант это объект класса <code>CardStatus</code>, не строка.</p>
<p>Строка со значением понадобится, когда статус нужно красиво напечатать (например, в карточке карты). Поэтому в проекте мы будем писать <code>status.value</code>.</p>
<h3>Что можно делать с вариантами</h3>
''' + ex(code_enum2) + '''
<p>Разбираем построчно:</p>
<ul>
<li><code>CardStatus("Blocked")</code> находит вариант <b>по значению</b>. Если такого значения нет, будет ошибка ValueError.</li>
<li><code>CardStatus["CLOSED"]</code> находит вариант <b>по имени</b> (имя пишется строкой в квадратных скобках).</li>
<li>Варианты сравниваются через <code>==</code> или <code>is</code>. Вариант всегда один и тот же объект, поэтому <code>is</code> работает надёжно.</li>
<li>Вариант Enum <b>не равен</b> своей строке: <code>CardStatus.ACTIVE == "Active"</code> даёт False. Сравнивай варианты с вариантами.</li>
<li>Цикл <code>for</code> перебирает все варианты по порядку, <code>len</code> даёт их количество, а <code>list(CardStatus)</code> превращает их в список.</li>
</ul>
<p>Если пытаться найти вариант, которого нет, Python сразу скажет об этом:</p>
''' + exs('''print(CardStatus("Frozen"))''', '''Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: 'Frozen' is not a valid CardStatus''') + '''
<p>И опечатка в имени тоже не пройдёт незамеченной: <code>CardStatus.ACTIV</code> сразу вызовет AttributeError, а не будет тихо работать неправильно, как наша строка «Activ». Кроме того, редактор кода подсказывает варианты, когда ты набираешь <code>CardStatus.</code>.</p>
<h3>Enum внутри класса</h3>
<p>Вот как это выглядит в программе: у карты есть поле <code>status</code>, и в нём хранится вариант Enum.</p>
''' + ex(code_enum3) + '''
<p>Вся работа со статусом идёт через <code>CardStatus.ACTIVE</code>, <code>CardStatus.BLOCKED</code> и т. д. Нет ни одной строки, в которой можно ошибиться. В банке мы поступим так с двумя множествами: <code>CardStatus</code> (статус карты) и <code>TransactionType</code> (тип операции).</p>
'''
    th2 = th('Enum: набор допустимых значений', terms2, body2)

    # ============ Теория 3: dataclass ============
    terms3 = [
        ('dataclass', 'Декоратор из модуля dataclasses для классов, которые в основном хранят данные. Над классом пишешь @dataclass, а внутри перечисляешь поля с типами. Python сам создаст __init__, красивый __repr__ (для print) и сравнение ==.\n\nПример:\nfrom dataclasses import dataclass\n\n@dataclass\nclass Point:\n    x: int\n    y: int = 0\n\np = Point(3)\nprint(p)\nprint(p == Point(3, 0))\nВывод:\nPoint(x=3, y=0)\nTrue'),
        ('field', 'Функция из dataclasses для тонкой настройки поля. Чаще всего нужна запись field(default_factory=list): она говорит «для каждого нового объекта создай свой пустой список». Без неё список по умолчанию был бы один на всех.\n\nПример:\nfrom dataclasses import dataclass, field\n\n@dataclass\nclass Basket:\n    items: list = field(default_factory=list)\n\na = Basket()\nb = Basket()\na.items.append("хлеб")\nprint(a.items, b.items)\nВывод:\n[\'хлеб\'] []'),
    ]
    code_plain = '''class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"User(name={self.name!r}, age={self.age!r})"


user = User("Иван", 23)
print(user)'''
    code_dc1 = '''from dataclasses import dataclass


@dataclass
class User:
    name: str
    age: int


user = User("Иван", 23)
print(user)
print(user.name, user.age)
print(user == User("Иван", 23), user == User("Пётр", 23))'''
    code_dc2 = '''from dataclasses import dataclass


@dataclass
class Account:
    acc_id: str
    balance: float = 0.0
    currency: str = "RUB"


a = Account("4081781")
b = Account("4081782", 150.5)
c = Account("4081783", currency="USD")
print(a)
print(b)
print(c)
a.balance += 100
print(a.balance)'''
    code_shared = '''class Basket:
    def __init__(self, items=[]):
        self.items = items


a = Basket()
b = Basket()
a.items.append("хлеб")
b.items.append("молоко")
print(a.items)
print(b.items)'''
    code_dc3 = '''from dataclasses import dataclass, field


@dataclass
class Basket:
    owner: str
    items: list = field(default_factory=list)

    def total_items(self):
        return len(self.items)


a = Basket("Аня")
b = Basket("Боря")
a.items.append("хлеб")
b.items.append("молоко")
b.items.append("сыр")
print(a)
print(b)
print(a.total_items(), b.total_items())'''
    code_dc4 = '''from dataclasses import dataclass
from typing import Optional


@dataclass
class Transaction:
    amount: float
    from_card: Optional[int] = None
    to_card: Optional[int] = None


deposit = Transaction(100, to_card=7)
transfer = Transaction(50, from_card=7, to_card=9)
print(deposit)
print(transfer)
print(deposit.from_card is None)'''
    body3 = '''
<p>В банке много классов, которые почти ничего не умеют, а только хранят данные: клиент (фамилия, имя, телефон), счёт (номер, баланс), запись об операции. Для них приходится писать однотипный код. Смотри на обычный класс с двумя полями:</p>
''' + ex(code_plain) + '''
<p>Нужно написать <code>__init__</code>, чтобы записать поля, и <code>__repr__</code>, чтобы <code>print(user)</code> показывал что-то понятное (без него ты увидел бы нечитаемое «&lt;User object at 0x...&gt;»). А если полей двадцать? Для этого придумали [[dataclass|декоратор dataclass]]:</p>
''' + ex(code_dc1) + '''
<p>Что тут произошло. Мы написали над классом <code>@dataclass</code> и перечислили поля в виде <code>имя: тип</code>. Python сам создал конструктор (поэтому <code>User("Иван", 23)</code> работает), красивую печать (<code>User(name='Иван', age=23)</code>) и сравнение: два объекта равны, если равны все их поля. Типы в аннотациях (str, int) это подсказки для человека и редактора, Python их не проверяет: можно создать <code>User(5, "abc")</code>, и ошибки не будет.</p>
<h3>Значения по умолчанию</h3>
<p>У поля может быть значение по умолчанию. Тогда его можно не передавать при создании объекта, как у обычной функции:</p>
''' + ex(code_dc2) + '''
<p>Правило как у функций: поля <b>без</b> значения по умолчанию идут <b>раньше</b> полей со значением. Иначе будет ошибка TypeError: non-default argument follows default argument. Поля можно менять, как обычные атрибуты (<code>a.balance += 100</code>).</p>
<h3>Список внутри dataclass</h3>
<p>В банке у клиента будет список карт, у банка список транзакций. Начинающие часто пишут так, и у них возникает ловушка. Сначала посмотри, как она работает в обычном классе:</p>
''' + ex(code_shared) + '''
<p>Мы добавили хлеб только в первую корзину, а молоко только во вторую, но видим <b>оба</b> товара в обеих. Причина в том, что значение по умолчанию <code>[]</code> создаётся один раз, когда Python читает определение, и дальше оба объекта делят один и тот же список. Если в dataclass написать <code>items: list = []</code>, Python даже не даст создать класс и скажет: ValueError: mutable default &lt;class 'list'&gt; for field items is not allowed: use default_factory.</p>
<p>Решение называется [[field|<code>field(default_factory=list)</code>]]: «для каждого нового объекта вызови <code>list()</code> и получи свой пустой список».</p>
''' + ex(code_dc3) + '''
<p>Теперь у каждой корзины свой список. То же самое работает для словарей: <code>field(default_factory=dict)</code>. Запомни: <b>список или словарь в dataclass только через default_factory</b>.</p>
<p>Внутри dataclass можно писать обычные методы (как <code>total_items</code>), поэтому классы с небольшой логикой тоже подходят.</p>
<h3>Поле «может быть пустым»</h3>
<p>Иногда значения может не быть: у пополнения нет карты-отправителя, у покупки нет карты-получателя. Для этого используют значение <code>None</code> и тип <code>Optional[int]</code> из модуля <code>typing</code> (он значит «целое число или None»):</p>
''' + ex(code_dc4) + '''
<p>Так мы запишем и пополнение (карта только получатель), и перевод (обе карты) одним классом.</p>
<h3>Где в банке обычный класс, а где dataclass</h3>
<p>В нашем проекте <code>User</code>, <code>Account</code>, <code>Bank</code> и <code>Transaction</code> это классы-хранилища, поэтому им подойдёт <code>@dataclass</code>. А вот <code>Card</code> остаётся обычным классом: у него будет свой конструктор, и от него мы позже унаследуем другие типы карт.</p>
'''
    th3 = th('dataclass: класс для хранения данных', terms3, body3)

    # ============ Флеш 1 ============
    fl1 = fl('Вопросы по Enum и dataclass', [
        q('Для чего в банковском проекте нужен класс Enum?', 'Чтобы задать набор допустимых значений с понятными именами', ['Чтобы считать баланс карты', 'Чтобы хранить список карт клиента', 'Чтобы ускорить работу программы'],
          'Enum описывает ограниченное множество вариантов (статусы карты, типы операций) в одном месте, и ошибиться в написании значения становится трудно.'),
        qo('Что выведет программа?', '''from enum import Enum


class Kind(Enum):
    PAY = "pay"
    DEPOSIT = "deposit"


print(Kind.PAY.value)''', ['PAY', 'Kind.PAY', 'pay Kind'], 'Свойство .value возвращает значение, записанное справа от имени: «pay». А .name дало бы «PAY».'),
        qo('Что выведет программа?', '''from enum import Enum


class Kind(Enum):
    PAY = "pay"
    DEPOSIT = "deposit"


print(Kind("deposit").name)''', ['deposit', 'Kind.DEPOSIT', 'DEPOSIT Kind'], 'Kind("deposit") ищет вариант по значению и находит Kind.DEPOSIT, а .name у него «DEPOSIT».'),
        qo('Что выведет программа?', '''from enum import Enum


class Kind(Enum):
    PAY = "pay"
    DEPOSIT = "deposit"


print(Kind.PAY == "pay")''', ['True', 'pay', 'Ошибка'], 'Вариант Enum это объект, а не строка, поэтому с самой строкой он не равен. Правильно сравнивать с другим вариантом: Kind.PAY == Kind.PAY или смотреть .value.'),
        qo('Что выведет программа?', '''from dataclasses import dataclass


@dataclass
class P:
    x: int
    y: int = 5


print(P(1))''', ['P(x=1, y=5)', 'P(1, 5)', '<P object>'], 'dataclass сам создаёт __init__ и __repr__. Поле y взяло значение по умолчанию, а print показывает объект в виде P(x=1, y=5).'),
        q('Как правильно завести пустой список в поле dataclass?', 'cards: list = field(default_factory=list)', ['cards: list = []', 'cards: list = list', 'cards: list = None()'],
          'Изменяемое значение нельзя писать прямо: оно было бы одним на все объекты (а Python вообще запретит). Нужна фабрика: field(default_factory=list).'),
        q('Почему Card в нашем проекте не dataclass?', 'Нужен свой __init__, а от Card наследуют другие карты', ['Dataclass не умеет хранить числа', 'Dataclass нельзя использовать с Enum', 'Класс Card слишком маленький'],
          'Dataclass удобен для простых хранилищ. Card требует своего __init__ и служит родителем для новых типов карт, поэтому его пишем обычным классом.'),
    ])

    # ============ Задания 1 ============
    ts1 = ts('Задания: Enum и dataclass', [
        task('Заведи Enum Status с тремя вариантами: ACTIVE со значением "Active", BLOCKED со значением "Blocked", CLOSED со значением "Closed". Программа читает слово, находит вариант Status по этому значению и выводит его имя (name). Если такого значения нет, выведи «Нет такого статуса».',
             'Класс: class Status(Enum). Поиск по значению: Status(word). Если значения нет, Status(word) вызывает ValueError, поймай его через try и except ValueError. Имя варианта лежит в .name.',
             '''from enum import Enum


class Status(Enum):
    ACTIVE = "Active"
    BLOCKED = "Blocked"
    CLOSED = "Closed"


word = input()
try:
    print(Status(word).name)
except ValueError:
    print("Нет такого статуса")''', ['Blocked', 'Active', 'Frozen', 'closed']),
        task('Заведи Enum TransactionType с вариантами DEPOSIT = "deposit", TRANSFER = "transfer", PAY = "pay", INTEREST = "interest". Выведи в цикле по одному варианту на строку в формате «имя = значение» (например, DEPOSIT = deposit), а в последней строке количество вариантов.',
             'Цикл for kind in TransactionType: перебирает варианты по порядку объявления. Для печати возьми kind.name и kind.value. Количество вариантов даёт len(TransactionType).',
             '''from enum import Enum


class TransactionType(Enum):
    DEPOSIT = "deposit"
    TRANSFER = "transfer"
    PAY = "pay"
    INTEREST = "interest"


for kind in TransactionType:
    print(f"{kind.name} = {kind.value}")
print(len(TransactionType))''', ['']),
        task('Заведи dataclass Product с полями name (str), price (float) и qty (int, по умолчанию 1). Программа читает название, цену и количество (три строки ввода), создаёт Product и выводит сам объект через print, а следующей строкой стоимость товара (price * qty) с двумя знаками после точки. Если количество не вводили (третья строка пустая), берётся 1.',
             'Импорт: from dataclasses import dataclass. Объект печатается красиво без своего __repr__: print(product). Для пустой строки используй условие: если строка не пуста, создавай Product(name, price, int(text)), иначе Product(name, price).',
             '''from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float
    qty: int = 1


name = input()
price = float(input())
text = input()
product = Product(name, price, int(text)) if text else Product(name, price)
print(product)
print(f"{product.price * product.qty:.2f}")''', ['Хлеб\n45.5\n3', 'Молоко\n89\n', 'Сыр\n320.99\n2']),
        task('Заведи dataclass Wallet с полями owner (str) и coins (list, у каждого кошелька свой пустой список). Программа читает имя первого владельца, имя второго владельца и число n. Первому кошельку добавь n монет номиналом 10, а потом выведи оба кошелька через print (по одному на строке). Монетки второго кошелька добавлять не нужно: его список должен остаться пустым.',
             'Список в поле dataclass только через field(default_factory=list): from dataclasses import dataclass, field. Монеты в первый кошелёк добавляй в цикле for _ in range(n): first.coins.append(10).',
             '''from dataclasses import dataclass, field


@dataclass
class Wallet:
    owner: str
    coins: list = field(default_factory=list)


first = Wallet(input())
second = Wallet(input())
for _ in range(int(input())):
    first.coins.append(10)
print(first)
print(second)''', ['Аня\nБоря\n3', 'Лена\nМиша\n0', 'Тим\nСаша\n5']),
    ])

    # ============ Теория 4: номера, деньги, время ============
    terms4 = [
        ('PAN', 'Primary Account Number, основной номер карты: те самые 16 цифр на лицевой стороне. Состоит из БИНа платёжной системы (первые 6 цифр: у MIR это 220400, у VISA 400000, у MASTERCARD 510000), порядкового номера карты (9 цифр) и контрольной цифры, которая считается по алгоритму Луна.\n\nПример:\nbin_code = "220400"\nserial = "000000001"\nprint(bin_code + serial)\nprint(len(bin_code + serial) + 1)\nВывод:\n220400000000001\n16'),
        ('алгоритм Луна', 'Способ проверить, что номер карты набран без опечатки. Берём цифры без контрольной, идём справа налево и каждую вторую (начиная с самой правой) удваиваем; если получилось больше 9, вычитаем 9. Складываем все цифры. Контрольная цифра дополняет сумму до числа, кратного 10.\n\nПример:\ntotal = 0\nfor i, ch in enumerate(reversed("1234")):\n    d = int(ch)\n    if i % 2 == 0:\n        d *= 2\n        if d > 9:\n            d -= 9\n    total += d\nprint(total, (10 - total % 10) % 10)\nВывод:\n16 4'),
        ('zfill', 'Метод строки: дополняет строку нулями слева до нужной длины. Принимает длину и возвращает новую строку, исходная не меняется. Если строка уже достаточно длинная, возвращает её как есть.\n\nПример:\nprint("17".zfill(5))\nprint("12345".zfill(3))\nВывод:\n00017\n12345'),
    ]
    code_float = '''print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
print(round(0.1 + 0.2, 2))

from decimal import Decimal

print(Decimal("0.1") + Decimal("0.2"))
print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))'''
    code_luhn = '''def luhn_digit(body):
    total = 0
    for i, ch in enumerate(reversed(body)):
        d = int(ch)
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return str((10 - total % 10) % 10)


print(luhn_digit("1234"))
print(luhn_digit("7992739871"))'''
    code_pan = '''print(make_pan("MIR", 1))
print(make_pan("VISA", 25))
print(make_pan("MASTERCARD", 3))'''
    code_acc = '''print(make_account_number("044452345", 1))
print(make_account_number("044452345", 17))'''
    code_time = '''from datetime import datetime, timedelta

moment = datetime(2025, 1, 10, 9, 30)
moment += timedelta(hours=7, minutes=13)
print(moment)
print(moment.date())
issued = moment.date()
print(issued.replace(year=issued.year + 4))'''
    body4 = '''
<p>Прежде чем писать банк, договоримся о нескольких технических вещах, которые в реальном банке тоже есть. Реализовывать их тебе не придётся: готовые функции будут лежать в заготовке с первого этапа. Но понимать, что они делают, нужно.</p>
<h3>Деньги и дробные числа</h3>
<p>Обычные дробные числа <code>float</code> хранятся в двоичной системе, и многие десятичные дроби в ней записываются не точно (ты видел это в теме про числа). Для денег это опасно: копейки могут «потеряться».</p>
''' + ex(code_float) + '''
<p>Сумма 0.1 и 0.2 в float даёт <code>0.30000000000000004</code>, и сравнение с 0.3 неверно. Тип <code>Decimal</code> из модуля <code>decimal</code> считает так, как мы привыкли на бумаге. Поэтому в настоящих банках деньги хранят в Decimal (или в целых копейках). Чтобы не усложнять проект, у нас суммы будут обычными числами, а при печати мы будем округлять до двух знаков: <code>f"{balance:.2f}"</code>.</p>
<h3>Номер карты</h3>
<p>Номер карты ([[PAN|PAN]]) это 16 цифр. Он не случайный, а собран по правилам:</p>
<table>
<tr><th>Часть</th><th>Сколько цифр</th><th>Что это</th></tr>
<tr><td>БИН</td><td>6</td><td>код платёжной системы: MIR 220400, VISA 400000, MASTERCARD 510000</td></tr>
<tr><td>Серийный номер</td><td>9</td><td>порядковый номер карты в банке (с нулями слева)</td></tr>
<tr><td>Контрольная цифра</td><td>1</td><td>считается по алгоритму Луна</td></tr>
</table>
<p>Контрольная цифра нужна, чтобы случайная опечатка в номере почти наверняка обнаруживалась. Считает её [[алгоритм Луна|алгоритм Луна]]. Разберём на коротком числе 1234. Идём справа налево: цифры 4, 3, 2, 1. Каждую вторую, начиная с самой правой, удваиваем: 4 → 8, 3 остаётся, 2 → 4, 1 остаётся. Сумма 8 + 3 + 4 + 1 = 16. До ближайшего числа, кратного 10, не хватает 4, значит контрольная цифра 4, а полный номер 12344. Вот функция, которая делает то же самое для любого числа:</p>
''' + ex(code_luhn) + '''
<p>Метод <code>zfill</code> ([[zfill|дополняет нулями слева]]) нужен, чтобы серийный номер всегда занимал 9 цифр: <code>"1".zfill(9)</code> даёт <code>000000001</code>. Функция <code>make_pan(платёжная_система, порядковый_номер)</code> склеивает БИН, серийный номер и контрольную цифру:</p>
''' + exs(code_pan, _out(HELP + code_pan)) + '''
<h3>Номер счёта</h3>
<p>Номер счёта в российском банке состоит из 20 цифр:</p>
<table>
<tr><th>Тип счёта</th><th>Валюта</th><th>Контрольный ключ</th><th>Филиал</th><th>Серийный номер</th></tr>
<tr><td>5 цифр</td><td>3 цифры</td><td>1 цифра</td><td>4 цифры</td><td>7 цифр</td></tr>
<tr><td>40817</td><td>810</td><td>считается</td><td>0000</td><td>0000001, 0000002, ...</td></tr>
</table>
<p>Код 40817 означает счёт физического лица, 810 это рубли, филиалов у нашего банка нет (четыре нуля), а ключ считается по специальной формуле Центробанка от БИКа банка и остальных цифр. Эту формулу за тебя уже написала функция <code>make_account_number(бик, порядковый_номер)</code>:</p>
''' + exs(code_acc, _out(HELP + code_acc)) + '''
<h3>Даты</h3>
<p>Даты в проекте не берутся из настоящих часов, иначе результаты были бы разными при каждом запуске. Вместо этого есть «игрушечные часы» <code>tick()</code>: при каждом вызове они возвращают момент времени на несколько часов позже предыдущего. А функция <code>issue_and_expiry()</code> возвращает пару: дату выпуска карты и дату окончания срока (ровно через 4 года). Вот как это работает внутри на настоящих датах:</p>
''' + ex(code_time) + '''
<p>Дата выводится в виде <code>2025-01-10</code>. Тебе нужно просто вызвать <code>issue_and_expiry()</code> при выпуске карты и сохранить обе даты.</p>
'''
    th4 = th('Деньги, номера карт и даты', terms4, body4)

    # ============ Теория 5: схема связей ============
    code_links = '''class User:
    def __init__(self, name):
        self.name = name
        self.accounts = []


class Account:
    def __init__(self, owner):
        self.owner = owner
        self.balance = 0


class Card:
    def __init__(self, account):
        self.account = account


user = User("Иван")
account = Account(user)
user.accounts.append(account)
card = Card(account)

print(card.account.owner.name)
print(user.accounts[0] is card.account)
print(card.account.owner is user)'''
    body5 = '''
<p>Главная сложность этого проекта в том, что объекты <b>связаны друг с другом</b>. У карты есть счёт, у счёта есть владелец, у владельца есть список его карт, а банк знает обо всех. Чтобы не запутаться, нужно мыслить схемой. Начнём с маленького примера, где связи видны:</p>
''' + ex(code_links) + '''
<p>Здесь нет копирования данных: <code>card.account</code> это <b>ссылка</b> на тот же самый объект счёта, на который ссылается и <code>user.accounts[0]</code>. Поэтому цепочка <code>card.account.owner.name</code> проходит по ссылкам от карты к счёту, а от счёта к владельцу, и достаёт его имя. (Про ссылки и «один и тот же объект» ты уже знаешь из темы про модель памяти: проверка <code>is</code> вернула True.)</p>
<p>В банке схема такая. Посмотри, какие атрибуты у классов и куда они ссылаются (жирным выделены связи, то есть атрибуты, в которых лежат другие объекты):</p>
''' + _fig('bank_attrs', 'Схема классов Bank, Account, Card, User и их атрибутов', 'Атрибуты классов. Банк хранит всё выпущенное в словарях (customers, accounts, cards), карта знает свой счёт и банк, счёт знает владельца, клиент знает свои счета и карты.') + '''
<p>Благодаря таким ссылкам из карты можно добраться до любых данных. Например, чтобы напечатать информацию о карте, нужны данные из <b>четырёх</b> объектов, и все они достижимы по цепочке от самой карты:</p>
''' + _fig('bank_data', 'Откуда подтягиваются данные для информации о карте', 'Откуда берутся данные для информации о карте: из самой карты, из банка (через card.bank), из счёта (card.account) и из клиента (card.account.owner).') + '''
<p>Чтобы не писать длинную цепочку каждый раз, её сокращают переменной: <code>owner = self.account.owner</code>, а дальше <code>owner.last_name</code>, <code>owner.phone</code>.</p>
<h3>Как банк выпускает карту</h3>
<p>Метод <code>apply_for_card</code> («подать заявку на карту») работает по шагам, и у каждого шага своя часть схемы. Банк получает данные заявки (фамилию, имя, ПИН-код, телефон, платёжную систему) и:</p>
<ol>
<li><b>Клиент.</b> Если клиент с такими фамилией, именем и телефоном уже есть, берём его, иначе создаём нового и записываем в <code>bank.customers</code>.</li>
<li><b>Счёт.</b> Заводим счёт на этого клиента и записываем его в <code>bank.accounts</code> и в <code>user.accounts</code>.</li>
<li><b>Карта.</b> Заводим карту со счётом и банком, записываем в <code>bank.cards</code> и в <code>user.cards</code>.</li>
</ol>
''' + _fig('bank_apply', 'Схема взаимодействия классов для метода apply_for_card: три шага', 'Схема метода apply_for_card: входные данные превращаются в клиента, счёт и карту, которые записываются и в банк, и в клиента.') + '''
<p>Идентификаторы выдаём просто по порядку. У нового клиента <code>user_id</code> равен числу клиентов в банке плюс один, то же самое для карт и счетов. Банк хранит всё в <b>словарях</b>: ключ это идентификатор, значение это объект. Тогда найти любую карту можно по её номеру: <code>bank.cards[3]</code>.</p>
<p>Совет на весь проект: когда пишешь метод, который трогает сразу несколько объектов, нарисуй для себя такую схему на бумаге. Это в разы проще, чем держать связи в голове.</p>
'''
    th5 = th('Схема связей: как классы знают друг о друге', [], body5)

    fl2 = fl('Вопросы по помощникам и связям', [
        q('Почему в настоящих банках деньги хранят в Decimal, а не в float?', 'Float неточно хранит многие десятичные дроби', ['Float не умеет хранить числа больше 100', 'Decimal быстрее работает', 'Float нельзя печатать'],
          'В float сумма 0.1 + 0.2 даёт 0.30000000000000004. Для денег такая погрешность недопустима, Decimal считает точно.'),
        qo('Что выведет программа?', '''print("17".zfill(5))''', ['17', '17000', '00170'], 'zfill дополняет строку нулями слева до длины 5: «00017».'),
        qo('Что выведет программа?', '''total = 0
for i, ch in enumerate(reversed("12")):
    d = int(ch)
    if i % 2 == 0:
        d *= 2
        if d > 9:
            d -= 9
    total += d
print(total)''', ['5', '3', '4'], 'Справа налево идут цифры 2 и 1. Первую (2) удваиваем: 4, вторая остаётся 1. Сумма 4 + 1 = 5.'),
        qo('Что выведет программа?', '''class Owner:
    def __init__(self, name):
        self.name = name


class Account:
    def __init__(self, owner):
        self.owner = owner


class Card:
    def __init__(self, account):
        self.account = account


user = Owner("Аня")
card = Card(Account(user))
print(card.account.owner.name)''', ['Аня', 'Owner', 'Ошибка'], 'Цепочка идёт по ссылкам: карта → её счёт → владелец счёта → его имя «Аня».'),
        q('Как в банке удобнее всего найти карту по её номеру?', 'Хранить карты в словаре, где ключ это номер карты', ['Хранить карты в строке', 'Перебирать все слова в файле', 'Хранить карты в кортеже из одного элемента'],
          'Словарь находит значение по ключу сразу: bank.cards[3]. Для этого и заведены словари customers, accounts и cards.'),
    ])

    # ============ Проект 1 ============
    SC = __import__('bankpj_scen')
    p1 = pj('Банк, этап 1: заявка на карту',
            'Ты разработчик бэкенда нового банка. Первая задача: научить банк выпускать карты. Напиши классы и два метода, а всё остальное (Enum статусов, функции номеров и дат) уже лежит в заготовке.\n'
            'Классы и атрибуты (имена обязательны, тест обращается к ним):\n'
            '— User (dataclass): user_id, last_name, first_name, pin, phone, accounts (список), cards (список).\n'
            '— Account (dataclass): acc_id, owner (объект User), balance (по умолчанию 0.0), cashback_balance (по умолчанию 0.0).\n'
            '— Card (обычный класс с __init__): card_id, account, bank, payment_system, pan, issue_date, expiry_date, status (по умолчанию CardStatus.ACTIVE), currency (по умолчанию "RUB").\n'
            '— Bank (dataclass): name, bic, customers (словарь «user_id → User»), accounts (словарь «acc_id → Account»), cards (словарь «card_id → Card»), transaction_log (пустой список, понадобится на втором этапе).\n'
            'Метод Bank.apply_for_card(last_name, first_name, pin, phone, payment_system="MIR", card_class=Card, **kwargs) выпускает карту и возвращает её:\n'
            '1) Ищет клиента среди bank.customers с такими же фамилией, именем и телефоном. Если не нашёл, создаёт нового: user_id равен числу клиентов в банке плюс один.\n'
            '2) Заводит новый счёт клиента: acc_id берётся из make_account_number(self.bic, число счетов в банке + 1).\n'
            '3) Заводит карту: card_id равен числу карт в банке плюс один, pan берётся из make_pan(payment_system, card_id), а даты выпуска и окончания из issue_and_expiry(). Карту создавай как card_class(...) и передавай в неё **kwargs (это понадобится на третьем этапе).\n'
            '4) Записывает новые объекты в банк (customers, accounts, cards) и в клиента (accounts, cards). Если клиент уже был, нового клиента не создаётся, но карта и счёт ему добавляются.\n'
            'Метод Card.get_card_info() возвращает строку-визитку карты в том формате, который виден в примере: 9 строк, затем строка из 50 дефисов. Баланс и кешбэк печатай с двумя знаками после точки.',
            'Сначала заведи классы по описанию. User, Account и Bank это @dataclass (списки и словари через field(default_factory=list) и field(default_factory=dict)), Card это обычный класс.\n'
            'Поиск клиента: цикл for u in self.customers.values() и сравнение (u.last_name, u.first_name, u.phone) с данными заявки.\n'
            'Создавай объекты по порядку: клиент, счёт, карта. Карту строй так: card_class(card_id=..., account=..., bank=self, ..., **kwargs). Только в конце клади всё в словари банка и в списки клиента.\n'
            'В get_card_info возьми owner = self.account.owner, собери список строк из f-строк, а склей методом join: "\\n".join(lines) + "\\n" + "-" * 50. Суммы печатай как {число:.2f}₽.\n'
            'Все PAN карт клиента: [c.pan for c in owner.cards]. Карта клиента, у которого уже были карты, увидит в этом списке и прежние, и новую.\n'
            'Если запутался в связях, нарисуй схему на бумаге: какой объект на какой ссылается.',
            _pick(1, 'sol'), SC.S1, bonus=60, tail=TL, starter=_pick(1, 'start'))

    # ============ Теория 6: транзакции и журнал ============
    code_row = '''from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class Kind(Enum):
    DEPOSIT = "deposit"
    PAY = "pay"


@dataclass
class Tx:
    timestamp: datetime
    type: Kind
    amount: float
    from_card: Optional[int] = None
    to_card: Optional[int] = None

    def row(self, sign=""):
        return f"{self.timestamp:%Y-%m-%d %H:%M} | {self.type.value:<8} | {sign}{self.amount:.2f}₽"


log = [
    Tx(datetime(2025, 1, 12, 9, 5), Kind.PAY, 45, from_card=1),
    Tx(datetime(2025, 1, 11, 18, 40), Kind.DEPOSIT, 1000, to_card=1),
]
for tx in sorted(log, key=lambda t: t.timestamp):
    print(tx.row())'''
    code_fmt = '''from datetime import datetime

moment = datetime(2025, 1, 11, 7, 10)
print(moment)
print(f"{moment:%Y-%m-%d %H:%M}")
print(f"{moment:%d.%m.%Y}")
print(f"[{'pay':<8}] [{'deposit':<8}] [{'transfer':<8}]")'''
    body6 = '''
<p>На втором этапе в банке появляется пятый класс: <b>Transaction</b>. Каждая операция с деньгами (пополнение, покупка, перевод) оставляет в банке запись. Все такие записи лежат в списке <code>bank.transaction_log</code> (это «журнал»), а карта и банк умеют показывать из него нужные строки.</p>
''' + _fig('bank_attrs_full', 'Схема классов банка с добавленным классом Transaction', 'Теперь на схеме появилась Transaction. Банк хранит её в списке transaction_log, а у самой записи есть поля from_card, to_card, amount, type, mcc, description, timestamp и cashback.') + '''
<p>У записи об операции такие поля: <code>timestamp</code> (когда), <code>type</code> (вид операции, это Enum <code>TransactionType</code>), <code>amount</code> (сумма), <code>from_card</code> (номер карты, с которой списали, или <code>None</code>), <code>to_card</code> (номер карты, на которую зачислили, или <code>None</code>), <code>mcc</code> (код категории магазина, только для покупок), <code>cashback</code> (сколько кешбэка вернули) и <code>description</code> (текст для человека). Как их заполнять:</p>
<ul>
<li><b>Пополнение</b>: <code>from_card=None</code> (деньги пришли «снаружи»), <code>to_card</code> номер карты.</li>
<li><b>Покупка</b>: <code>from_card</code> номер карты, <code>to_card=None</code> (деньги ушли магазину), есть <code>mcc</code>.</li>
<li><b>Перевод</b>: заполнены обе карты.</li>
</ul>
<p>Вид операции задаёт Enum, как ты и тренировался:</p>
<pre>class TransactionType(Enum):
    DEPOSIT = "deposit"
    TRANSFER = "transfer"
    PAY = "pay"
    INTEREST = "interest"</pre>
<p>Деньги на счёте меняются в самом методе карты, а запись в журнал кладёт готовый метод <code>_log</code>. Он уже есть в заготовке: создаёт <code>Transaction</code> с текущим «игрушечным» временем из <code>tick()</code> и добавляет в <code>bank.transaction_log</code>.</p>
<h3>Как напечатать историю</h3>
<p>Одну запись удобно превращать в строку методом <code>row</code>. В нём встретятся три приёма форматирования:</p>
''' + ex(code_fmt) + '''
<p>Через двоеточие внутри фигурных скобок f-строки можно задавать формат. Для даты и времени используют коды: <code>%Y</code> год, <code>%m</code> месяц, <code>%d</code> день, <code>%H</code> часы, <code>%M</code> минуты. А <code>:&lt;8</code> выравнивает слово по левому краю в поле из 8 символов (ты изучал это в теме про форматирование вывода). Теперь соберём всё вместе: журнал, строка записи и сортировка по времени.</p>
''' + ex(code_row) + '''
<p>Записи в журнале лежат в том порядке, в котором мы их добавили, а нам нужно показать их по времени. Для этого <code>sorted</code> с ключом-лямбдой: <code>key=lambda t: t.timestamp</code>. Для истории <b>одной карты</b> из журнала берём только те записи, где её номер стоит среди <code>from_card</code> и <code>to_card</code>, а перед суммой добавляем знак: «-» если деньги с этой карты ушли и «+» если пришли. Для общей истории банка знак не нужен.</p>
<h3>Что должна уметь карта</h3>
<p>На этом этапе ты напишешь методы карты <code>get_balance</code>, <code>deposit</code>, <code>pay</code>, <code>transfer</code>, <code>close</code> и <code>get_history</code>, метод банка <code>get_global_history</code> и метод клиента <code>change_pin</code>. Правильность данных пока не проверяем (сумма положительная, денег хватает, карта не закрыта): это тема четвёртого этапа. Сейчас важно, чтобы основа работала.</p>
<p>Одна из деталей: <code>change_pin(old_pin, new_pin)</code> принимает ПИН-коды <b>строками</b>. Если записать ПИН-код числом, то 0070 превратится в 70 и нули потеряются, поэтому в банках такие коды всегда строки.</p>
'''
    th6 = th('Транзакции и журнал операций', [], body6)

    p2 = pj('Банк, этап 2: работа с картой',
            'Банк уже выпускает карты. Теперь научи карты работать с деньгами и вести журнал. Дополни код этапа 1 (он уже есть в заготовке):\n'
            '1) Enum TransactionType с вариантами DEPOSIT = "deposit", TRANSFER = "transfer", PAY = "pay", INTEREST = "interest".\n'
            '2) Dataclass Transaction. Поля по порядку: timestamp (datetime), type (TransactionType), amount (float), from_card (номер карты или None), to_card (номер карты или None), mcc (строка или None), cashback (по умолчанию 0.0), description (по умолчанию ""). У последних пяти полей есть значения по умолчанию, у остальных нет. Метод row(sign="") возвращает строку f"{время:%Y-%m-%d %H:%M} | {тип.value:<8} | {sign}{сумма:.2f}₽ | {описание}".\n'
            '3) Методы Card. get_balance() возвращает строку "Баланс: 100.00₽". deposit(amount) увеличивает баланс счёта и пишет в журнал пополнение. pay(amount, mcc) уменьшает баланс и пишет покупку. transfer(to_card, amount) переводит деньги на другую карту (to_card это объект Card): у одной баланс уменьшается, у другой растёт, запись одна. close() ставит статус CardStatus.CLOSED. get_history() возвращает список строк row() записей этой карты по возрастанию времени: со знаком "-" там, где она отправитель, и "+" там, где получатель.\n'
            'Записывать в журнал помогает готовый метод self._log(kind, amount, from_card=None, to_card=None, mcc=None, cashback=0.0, description=""). Описания: пополнение «Пополнение 100.00₽ на карту #1», покупка «Покупка 45.00₽, MCC 5814», перевод «Перевод 50.00₽: карта #1 → карта #2».\n'
            '4) Bank.get_global_history() возвращает список строк row() (без знаков) всех транзакций банка по времени.\n'
            '5) User.change_pin(old_pin, new_pin): если old_pin совпал с текущим pin, меняет его на new_pin, иначе ничего не делает. Остальные проверки пока не нужны.',
            'Начни с Enum и dataclass Transaction, а метод row собери одной f-строкой: формат времени %Y-%m-%d %H:%M пиши прямо в фигурных скобках, выравнивание типа через {self.type.value:<8}.\n'
            'Деньги лежат на счёте, поэтому баланс меняй так: self.account.balance += amount. Запись вызывай через self._log(TransactionType.DEPOSIT, amount, to_card=self.card_id, description=...).\n'
            'transfer: у отправителя self.account.balance уменьшается, у получателя to_card.account.balance растёт. В записи обе карты: from_card=self.card_id, to_card=to_card.card_id.\n'
            'get_history: пройди по sorted(self.bank.transaction_log, key=lambda t: t.timestamp), оставь записи, где self.card_id есть среди (tx.from_card, tx.to_card). Знак "-" ставь, если tx.from_card == self.card_id, иначе "+".\n'
            'Чтобы получить значение Enum в строке, используй .value (например, tx.type.value).',
            _pick(2, 'sol'), SC.S2, bonus=60, tail=TL, starter=_pick(2, 'start'))

    # ============ Теория 7: наследование, новые типы карт ============
    terms7 = [
        ('keyword-only параметр', 'Параметр функции, который можно передать только по имени. Чтобы сделать такие параметры, в списке параметров перед ними ставят звёздочку *. Так нельзя перепутать порядок аргументов.\n\nПример:\ndef rate(*, value=0.05):\n    return value\n\nprint(rate())\nprint(rate(value=0.1))\nВывод:\n0.05\n0.1'),
    ]
    code_sub1 = '''class Card:
    def __init__(self, number, balance=0):
        self.number = number
        self.balance = balance

    def pay(self, amount):
        self.balance -= amount
        return f"Оплата {amount:.2f}"


class SimpleDebitCard(Card):
    pass


card = SimpleDebitCard("0001", 500)
print(card.pay(120))
print(card.balance, isinstance(card, Card))'''
    code_sub2 = '''class Card:
    def __init__(self, number, balance=0):
        self.number = number
        self.balance = balance

    def pay(self, amount):
        self.balance -= amount
        return f"Оплата {amount:.2f}"


class CashbackCard(Card):
    def __init__(self, *, cashback_rate=0.05, **kwargs):
        super().__init__(**kwargs)
        self.cashback_rate = cashback_rate
        self.cashback = 0

    def pay(self, amount):
        bonus = round(amount * self.cashback_rate, 2)
        self.cashback += bonus
        return super().pay(amount) + f", кешбэк {bonus:.2f}"


plain = Card("0001", 500)
base = CashbackCard(number="0002", balance=500)
custom = CashbackCard(number="0003", balance=500, cashback_rate=0.1)
for card in (plain, base, custom):
    print(card.pay(120))
print(base.cashback, custom.cashback)
print(base.balance, custom.balance)'''
    code_sub3 = '''class Card:
    def pay(self, amount):
        return "обычная оплата"


class SavingsCard(Card):
    def pay(self, amount):
        return "оплата с накопительной карты запрещена"


class CashbackCard(Card):
    def pay(self, amount):
        return "оплата с кешбэком"


for card in (Card(), SavingsCard(), CashbackCard()):
    print(type(card).__name__, "->", card.pay(100))'''
    body7 = '''
<p>Банк захотел выпускать разные карты. В классе <code>Card</code> уже есть всё основное, и придумывать новые классы с нуля не нужно: мы возьмём <code>Card</code> и «надстроим» его через наследование (ты изучал его в теме про классы). Сравним три типа карт:</p>
''' + _fig('bank_types', 'Таблица отличий трёх типов карт: новые атрибуты, новые методы, переопределение методов', 'Чем отличаются типы карт. Дебетовая: ничего нового. Дебетовая с кешбэком: новый атрибут cashback_rate и переопределённый pay. Накопительный счёт: новый атрибут interest_rate и новый метод accrue_interest.') + '''
<ul>
<li><b>Обычная дебетовая карта</b> (<code>SimpleDebitCard</code>) ничем не отличается от <code>Card</code>. Пустой класс-наследник, внутри только <code>pass</code>.</li>
<li><b>Дебетовая карта с кешбэком</b> (<code>CashbackCard</code>) при покупке возвращает часть суммы бонусами: нужен новый атрибут <code>cashback_rate</code> и свой метод <code>pay</code>.</li>
<li><b>Накопительный счёт</b> (<code>SavingsCard</code>) начисляет проценты на остаток: нужен атрибут <code>interest_rate</code> и новый метод <code>accrue_interest</code>.</li>
</ul>
<h3>Пустой наследник</h3>
''' + ex(code_sub1) + '''
<p>Наследник получает все атрибуты и методы родителя. Поэтому <code>SimpleDebitCard</code> без единой своей строки умеет платить, а <code>isinstance(card, Card)</code> даёт <code>True</code>: объект подкласса считается и объектом родителя.</p>
<h3>Новый параметр и переопределённый метод</h3>
<p>Чтобы добавить карте с кешбэком ставку, у наследника появляется свой <code>__init__</code>. Но остальные данные карты (номер, счёт, банк и т. д.) по-прежнему должен обработать родитель. Для этого есть два приёма:</p>
<ul>
<li><code>def __init__(self, *, cashback_rate=0.05, **kwargs)</code>: звёздочка делает ставку [[keyword-only параметр|параметром, который передают только по имени]], а <code>**kwargs</code> собирает все остальные именованные аргументы в словарь.</li>
<li><code>super().__init__(**kwargs)</code>: передаёт этот словарь родителю, чтобы он сделал свою часть работы.</li>
</ul>
<p>Метод, который нужно изменить, просто пишем в наследнике заново (это называется переопределением). Если нужна работа родителя, вызываем её через <code>super()</code>:</p>
''' + ex(code_sub2) + '''
<p>Разбор: обычная карта просто списывает деньги. Карта с кешбэком копит бонус 5 % (120 × 0.05 = 6.0), у третьей ставка 10 % (12.0). Ставку можно не указывать (тогда по умолчанию 0.05) или указать по имени: <code>cashback_rate=0.1</code>. Заметь, что бонусы лежат отдельно от баланса: баланс уменьшился ровно на сумму покупки. В нашем банке кешбэк будет накапливаться на отдельном поле счёта <code>cashback_balance</code>.</p>
<h3>Одно имя метода, разное поведение</h3>
<p>Самое полезное в наследовании: код, который работает с картами, вызывает <code>card.pay(100)</code> и ему не важно, какая именно карта перед ним. Каждый класс отвечает по-своему:</p>
''' + ex(code_sub3) + '''
<p>Это называется <b>полиморфизмом</b>. Банк вызывает <code>card.pay(...)</code>, а Python сам подбирает нужный вариант метода по типу объекта. Имя класса объекта можно узнать так: <code>type(card).__name__</code>.</p>
<h3>Формулы этапа</h3>
<ul>
<li><b>Кешбэк</b> при покупке: <code>round(amount * cashback_rate, 2)</code>. С баланса списывается вся сумма покупки, а кешбэк прибавляется к <code>account.cashback_balance</code> и записывается в транзакцию.</li>
<li><b>Проценты</b>: <code>round(balance * interest_rate, 2)</code> прибавляются к балансу счёта; в журнал идёт запись типа <code>INTEREST</code>, где карта только получатель.</li>
</ul>
<p>Чтобы выпустить карту нужного типа, ты будешь использовать уже написанный <code>apply_for_card</code>: <code>bank.apply_for_card(..., card_class=CashbackCard, cashback_rate=0.07)</code>. Класс из <code>card_class</code> создаст объект, а <code>cashback_rate</code> попадёт в <code>**kwargs</code> и пробросится в наследник.</p>
'''
    th7 = th('Наследование: новые типы карт', terms7, body7)

    fl3 = fl('Вопросы по наследованию карт', [
        q('Зачем в __init__ наследника пишут super().__init__(**kwargs)?', 'Чтобы родитель получил свои параметры и сделал свою часть', ['Чтобы удалить родительский класс', 'Чтобы сделать все параметры необязательными', 'Чтобы запретить новые атрибуты'],
          'Наследник забирает свой параметр, а все остальные именованные аргументы отдаёт родителю через **kwargs. Иначе родитель не получит номер, счёт и другие данные.'),
        q('Что значит звёздочка в def __init__(self, *, rate=0.05, **kwargs)?', 'Параметры после неё передают только по имени', ['Параметр rate обязателен', 'Параметр rate можно не писать', 'Параметры нужно передавать списком'],
          'Параметры после одиночной * называются keyword-only: rate нужно писать в виде rate=0.1. Порядок аргументов перепутать нельзя.'),
        qo('Что выведет программа?', '''class A:
    def hi(self):
        return "A"


class B(A):
    def hi(self):
        return "B"


print(B().hi())''', ['B', 'A', 'AB'], 'B переопределил метод hi, поэтому у объекта B вызывается его собственная версия.'),
        qo('Что выведет программа?', '''class A:
    pass


class B(A):
    pass


print(isinstance(B(), A), isinstance(A(), B))''', ['True False', 'True True', 'False True'], 'Объект подкласса считается и объектом родителя (B() это A), а наоборот нет: обычный A не является B.'),
        qo('Что выведет программа?', '''balance = 200
amount = 120
rate = 0.05
cashback = round(amount * rate, 2)
print(balance - amount, cashback)''', ['80 6.0', '80 0.05', '75 6.0'], 'С баланса списывается вся сумма покупки (200 - 120 = 80), а кешбэк это 120 × 0.05 = 6.0, он копится отдельно.'),
    ])

    p3 = pj('Банк, этап 3: новые типы карт',
            'Банк запускает новые продукты. Добавь в код этапа 2 (он в заготовке) три класса-наследника Card:\n'
            '— SimpleDebitCard: обычная дебетовая карта, ничего нового.\n'
            '— CashbackCard: дебетовая карта с кешбэком. Параметр cashback_rate (по умолчанию 0.05) принимается только по имени и сохраняется в атрибут cashback_rate. Метод pay переопределён: кешбэк = round(amount * cashback_rate, 2); с баланса списывается вся сумма покупки, кешбэк прибавляется к account.cashback_balance, в журнал идёт запись PAY с этим кешбэком в поле cashback и описанием «Покупка 120.00₽, MCC 5814, кешбэк 6.00₽».\n'
            '— SavingsCard: накопительная карта. Параметр interest_rate (по умолчанию 0.02) только по имени, сохраняется в атрибут interest_rate. Новый метод accrue_interest(): interest = round(баланс * interest_rate, 2) прибавляется к балансу, в журнал идёт запись INTEREST (to_card это номер карты, amount это interest) с описанием «Проценты 20.00₽ на карту #1».\n'
            'Остальные аргументы наследники отдают родителю через **kwargs. Карты выпускаются уже написанным apply_for_card, например: bank.apply_for_card(..., card_class=CashbackCard, cashback_rate=0.07). Остальное (переводы, история) должно продолжать работать у всех типов.',
            'SimpleDebitCard: достаточно class SimpleDebitCard(Card): pass.\n'
            'У двух других класса свой __init__: def __init__(self, *, cashback_rate=0.05, **kwargs). Первой строкой super().__init__(**kwargs), потом сохрани свой атрибут.\n'
            'В CashbackCard.pay сначала посчитай cashback = round(amount * self.cashback_rate, 2), потом self.account.balance -= amount и self.account.cashback_balance += cashback, затем запись self._log(TransactionType.PAY, amount, from_card=self.card_id, mcc=mcc, cashback=cashback, description=...).\n'
            'В SavingsCard.accrue_interest в запись пиши to_card=self.card_id (проценты приходят на карту), а тип TransactionType.INTEREST.\n'
            'Описания пиши с двумя знаками после точки: {cashback:.2f}, {interest:.2f}.',
            _pick(3, 'sol'), SC.S3, bonus=60, tail=TL, starter=_pick(3, 'start'))

    # ============ Теория 8: дерево ошибок ============
    terms8 = [
        ('иерархия ошибок', 'Семейство своих исключений, у которых один общий родитель. Например, BankError — корень, а ValidationError, AccessError и другие — его потомки. Благодаря этому можно поймать любую ошибку банка одним except BankError, а можно отдельно ловить конкретный вид.\n\nПример:\nclass BankError(Exception):\n    pass\n\nclass AccessError(BankError):\n    pass\n\ntry:\n    raise AccessError("нет доступа")\nexcept BankError as err:\n    print(type(err).__name__, err)\nВывод:\nAccessError нет доступа'),
    ]
    code_h1 = '''class BankError(Exception):
    """Корень: от него наследуются все ошибки банка."""


class ValidationError(BankError):
    PIN_INVALID = "ПИН-код должен быть строкой из 4 символов"
    PIN_FORMAT = "ПИН-код должен состоять только из цифр"


class AccessError(BankError):
    CARD_INACTIVE = "Карта закрыта или заблокирована"


def check_pin(pin):
    if not (isinstance(pin, str) and len(pin) == 4):
        raise ValidationError(ValidationError.PIN_INVALID)
    if not pin.isdigit():
        raise ValidationError(ValidationError.PIN_FORMAT)
    return pin


for value in ("1234", "12", "12a4", 1234):
    try:
        print("OK:", check_pin(value))
    except BankError as err:
        print(type(err).__name__ + ":", err)'''
    code_h2 = '''class BankError(Exception):
    pass


class AccessError(BankError):
    pass


try:
    raise AccessError("Карта заблокирована")
except BankError as err:
    print("Общий обработчик:", err)
except AccessError as err:
    print("Точный обработчик:", err)'''
    code_h3 = '''class BankError(Exception):
    pass


class ValidationError(BankError):
    pass


class BusinessRuleError(BankError):
    MCC_FORBIDDEN = "Покупки в категории {mcc} запрещены банком"


print(issubclass(ValidationError, BankError))
print(issubclass(ValidationError, BusinessRuleError))
err = BusinessRuleError(BusinessRuleError.MCC_FORBIDDEN.format(mcc="7995"))
print(isinstance(err, BankError), isinstance(err, ValueError))
print(err)'''
    code_h4 = '''letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя-"


def is_russian_name(text):
    return isinstance(text, str) and text != "" and all(ch.lower() in letters for ch in text)


for name in ("Иванов", "Анна-Мария", "Ivanov", "Иван1", ""):
    print(repr(name), is_russian_name(name))'''
    body8 = '''
<p>Банковское приложение не имеет права «падать» из-за неверного ввода. Если пользователь набрал не ту сумму или карта заблокирована, нужно спокойно сообщить, что именно не так. Для этого в проекте есть своё <b>дерево ошибок</b>: каждый вид проблемы это отдельный класс исключения, а все они наследуются от одного родителя <code>BankError</code>.</p>
''' + _fig('bank_errors', 'Иерархия ошибок банковского приложения: ValidationError, NotFoundError, AccessError, BusinessRuleError, InsufficientFundsError', 'Пять видов ошибок банка в том порядке, в котором их проверяют: сначала ввод, потом существование, доступ, бизнес-правила и в конце нехватка денег.') + '''
<table>
<tr><th>Ошибка</th><th>Что означает</th></tr>
<tr><td><code>ValidationError</code></td><td>неправильный ввод: формат ПИН-кода, имя, некорректная сумма</td></tr>
<tr><td><code>NotFoundError</code></td><td>объект не найден: нет такой карты, счёта или клиента</td></tr>
<tr><td><code>AccessError</code></td><td>нет доступа: карта заблокирована или закрыта, не привязана к счёту</td></tr>
<tr><td><code>BusinessRuleError</code></td><td>нарушены правила банка: лимит, запрещённая операция, слишком много карт</td></tr>
<tr><td><code>InsufficientFundsError</code></td><td>не хватает денег на карте или счёте</td></tr>
</table>
<h3>Как их описывать</h3>
<p>Классы пустые, но удобно хранить тексты сообщений в <b>атрибутах класса</b>: тогда они лежат в одном месте, и в коде пишется не длинная фраза, а понятное имя. Вот маленькая версия с двумя ошибками:</p>
''' + ex(code_h1) + '''
<p>Разбор. <code>ValidationError.PIN_INVALID</code> это просто строка, мы передали её в исключение как сообщение. Функция <code>check_pin</code> последовательно проверяет данные: сначала «это строка из 4 символов» (проверку типа делает <code>isinstance</code>, а <code>len</code> считает символы), затем «одни цифры» (метод <code>isdigit</code>). Для числа <code>1234</code> первая проверка сразу срабатывает: это не строка. Все исключения мы ловим одним <code>except BankError</code>, потому что все они потомки <code>BankError</code>. В <code>print</code> выводим имя класса (<code>type(err).__name__</code>) и сообщение (<code>err</code>).</p>
<h3>Порядок обработчиков</h3>
<p>Если у одного <code>try</code> несколько <code>except</code>, Python выбирает <b>первый подходящий</b>. Поэтому конкретные ошибки пишут <b>раньше</b> общих. Что будет, если перепутать:</p>
''' + ex(code_h2) + '''
<p>Исключение <code>AccessError</code> подходит и под <code>BankError</code> (родитель), поэтому сработал первый, общий, обработчик. Второй до исполнения вообще не дойдёт. Правило: сначала узкие классы, потом широкие.</p>
<h3>Принадлежность к классу и текст с подстановкой</h3>
''' + ex(code_h3) + '''
<p><code>issubclass(A, B)</code> проверяет, что класс <code>A</code> наследует от <code>B</code>, а <code>isinstance(объект, класс)</code> проверяет объект. Заметь, что <code>ValidationError</code> не потомок <code>BusinessRuleError</code> (они «братья»), а сообщение с пропуском <code>{mcc}</code> мы заполнили методом <code>format</code>.</p>
<h3>Порядок проверок в методе</h3>
<p>Дерево ошибок — это ещё и порядок проверок внутри метода. Сначала проверяем самое «дешёвое» и общее: правильность ввода (ValidationError). Если с вводом проблема, дальше смотреть бессмысленно. Потом существует ли объект (NotFoundError), потом доступ (AccessError), правила банка (BusinessRuleError) и в конце достаточно ли денег (InsufficientFundsError). Так метод ведёт себя предсказуемо: для одних и тех же неверных данных всегда выдаёт одну и ту же ошибку.</p>
<p>Два совета, которые отличают аккуратный код от неряшливого:</p>
<ul>
<li><b>Сначала все проверки, потом изменения.</b> Если уже списал деньги, а потом нашёл ошибку, придётся откатывать. Пусть метод сначала проверит всё, а менять балансы начнёт, когда ошибок точно нет.</li>
<li><b>Подозрительная операция блокирует карту.</b> Если превышен лимит пополнения, перевода или покупки, банк сначала ставит карте статус <code>CardStatus.BLOCKED</code>, а потом вызывает ошибку. После этого карта не работает, пока не разберутся.</li>
</ul>
<h3>Проверка типов и имён</h3>
<p>Сумма должна быть числом, а не строкой: проверка <code>isinstance(amount, (int, float))</code> (в скобках перечислены допустимые типы). Код категории магазина (MCC) это строка ровно из 4 цифр: <code>isinstance(mcc, str) and len(mcc) == 4 and mcc.isdigit()</code>. А имя и фамилия должны быть русскими, допускается дефис (для двойных фамилий). В заготовке этапа 4 для этого уже есть функция:</p>
''' + ex(code_h4) + '''
<p>Что уже лежит в заготовке этапа 4: константы лимитов (<code>DEPOSIT_LIMIT</code>, <code>TRANSFER_LIMIT</code>, <code>PAY_LIMIT</code>, <code>FORBIDDEN_MCC</code>, <code>MAX_CARDS</code>, <code>MAX_RATE</code>), весь каталог ошибок с готовыми сообщениями и функция <code>is_russian_name</code>. Твоя задача: расставить проверки в методах в правильном порядке.</p>
'''
    th8 = th('Дерево ошибок банка', terms8, body8)

    fl4 = fl('Вопросы по ошибкам банка', [
        q('Зачем все ошибки банка наследуют от общего класса BankError?', 'Чтобы поймать любую ошибку банка одним except BankError', ['Чтобы они выполнялись быстрее', 'Чтобы их нельзя было вызвать', 'Чтобы они не имели сообщений'],
          'Общий родитель позволяет написать один except BankError и поймать всех потомков, а при желании ловить и отдельные виды.'),
        qo('Что выведет программа?', '''class BankError(Exception):
    pass


class AccessError(BankError):
    pass


try:
    raise AccessError("закрыта")
except BankError as err:
    print("общий")
except AccessError as err:
    print("точный")''', ['общий', 'точный', 'общий точный'], 'Python берёт первый подходящий обработчик. AccessError подходит под BankError, поэтому сработал первый.'),
        q('В каком порядке проверяют ошибки в методе банка?', 'Ввод, существование, доступ, правила банка, нехватка денег', ['Нехватка денег, правила банка, доступ, ввод', 'Правила банка, ввод, нехватка денег, доступ', 'Порядок не важен'],
          'Идём от самых «общих» к самым «специфичным»: если ввод неверный, дальше смотреть нет смысла. Так метод для одних данных всегда даёт одну ошибку.'),
        q('Когда метод должен менять баланс счёта?', 'Только после того, как все проверки пройдены', ['Сразу в начале метода', 'Перед проверкой доступа', 'Только перед исключением'],
          'Если изменить баланс, а потом найти ошибку, придётся откатывать изменения. Поэтому сначала все проверки, потом само действие.'),
        qo('Что выведет программа?', '''class BankError(Exception):
    pass


class ValidationError(BankError):
    pass


print(issubclass(ValidationError, BankError), issubclass(BankError, ValidationError))''', ['True False', 'False True', 'True True'], 'Потомок ValidationError является подклассом BankError, а родитель не является подклассом своего потомка.'),
        qo('Что выведет программа?', '''def check(mcc):
    return isinstance(mcc, str) and len(mcc) == 4 and mcc.isdigit()


print(check("5411"), check(5411), check("54"))''', ['True False False', 'True True False', 'True False True'], 'Строка "5411" подходит. Число 5411 не строка, а "54" короче четырёх символов.'),
    ])

    # ============ Задания 2 ============
    LTR = '''class BankError(Exception):
    pass


class ValidationError(BankError):
    pass


class AccessError(BankError):
    pass


def risky(code):
    if code == "1":
        raise ValidationError("плохой ввод")
    if code == "2":
        raise AccessError("нет доступа")
    if code == "3":
        raise ValueError("не число")
    return "ок"
'''
    ts2 = ts('Задания: ошибки банка', [
        task('Заведи классы исключений: BankError (наследник Exception), ValidationError и InsufficientFundsError (оба наследники BankError). Напиши функцию withdraw(balance, amount): если amount не больше нуля, она вызывает ValidationError("Сумма должна быть больше нуля"), если amount больше balance, то InsufficientFundsError("Недостаточно денег"), иначе возвращает balance - amount. Программа читает два целых числа (баланс и сумму), вызывает функцию и ловит BankError. При ошибке печатает «Ошибка: ИмяКласса: сообщение», иначе «Новый баланс: N».',
             'Классы объявляются так: class ValidationError(BankError): pass. Имя класса исключения: type(err).__name__. Сообщение лежит в самом объекте: f"{err}" или просто err в print.',
             '''class BankError(Exception):
    pass


class ValidationError(BankError):
    pass


class InsufficientFundsError(BankError):
    pass


def withdraw(balance, amount):
    if amount <= 0:
        raise ValidationError("Сумма должна быть больше нуля")
    if amount > balance:
        raise InsufficientFundsError("Недостаточно денег")
    return balance - amount


balance = int(input())
amount = int(input())
try:
    print("Новый баланс:", withdraw(balance, amount))
except BankError as err:
    print(f"Ошибка: {type(err).__name__}: {err}")''', ['100\n30', '100\n0', '100\n250', '50\n-5']),
        task('Классы ошибок BankError, ValidationError, AccessError и функция risky(code) уже написаны в заготовке (смотри ниже). Программа читает строку code и вызывает risky. Обработай результат так: ValidationError печатает «Неверные данные», любая другая ошибка банка печатает «Ошибка банка», любая вообще другая ошибка печатает «Неизвестная ошибка», а если ошибок не было, печатается результат функции. Порядок обработчиков должен идти от узких классов к широким.',
             'Поставь три except подряд: сначала except ValidationError, затем except BankError, потом except Exception. Результат функции печатай в ветке else у try.',
             LTR + '''

code = input()
try:
    result = risky(code)
except ValidationError:
    print("Неверные данные")
except BankError:
    print("Ошибка банка")
except Exception:
    print("Неизвестная ошибка")
else:
    print(result)''', ['1', '2', '3', '4'], starter=LTR),
        task('Напиши функцию check_transfer(balance, amount, same_card): она проверяет перевод. Порядок проверок строго такой: 1) если amount не число (int или float) или не больше нуля, вызови ValidationError("Некорректная сумма"); 2) если same_card равен True, вызови BusinessRuleError("Нельзя переводить самому себе"); 3) если amount больше balance, вызови InsufficientFundsError("Недостаточно денег"). Если ошибок нет, верни строку «Перевод разрешён». Классы BankError, ValidationError, BusinessRuleError и InsufficientFundsError (потомки BankError) заведи сам.',
             'Проверка типа числа: isinstance(amount, (int, float)). Порядок проверок важен: ты вызываешь первую подошедшую ошибку, поэтому после неё остальные проверки уже не выполняются.',
             '''class BankError(Exception):
    pass


class ValidationError(BankError):
    pass


class BusinessRuleError(BankError):
    pass


class InsufficientFundsError(BankError):
    pass


def check_transfer(balance, amount, same_card):
    if not isinstance(amount, (int, float)) or amount <= 0:
        raise ValidationError("Некорректная сумма")
    if same_card:
        raise BusinessRuleError("Нельзя переводить самому себе")
    if amount > balance:
        raise InsufficientFundsError("Недостаточно денег")
    return "Перевод разрешён"''',
             ['''def attempt(*args):
    try:
        print(check_transfer(*args))
    except BankError as err:
        print(type(err).__name__ + ":", err)


attempt(100, 50, False)
attempt(100, 500, False)
attempt(100, -5, False)''', '''def attempt(*args):
    try:
        print(check_transfer(*args))
    except BankError as err:
        print(type(err).__name__ + ":", err)


attempt(100, "50", False)
attempt(100, 50, True)
attempt(10, 50, True)
attempt(10, 0, True)
attempt(100.5, 100.5, False)''', '''try:
    check_transfer(1, 1, False)
    print(isinstance(BankError(), Exception))
except Exception as err:
    print("упало", type(err).__name__)
print(issubclass(ValidationError, BankError), issubclass(InsufficientFundsError, ValidationError))'''], tail=TL),
    ])

    # ============ Проект 4 ============
    p4 = pj('Банк, этап 4: правила и ошибки',
            'Банк не должен ломаться от неверных данных. Расставь в коде этапа 3 проверки и ошибки. В заготовке уже есть константы лимитов, весь каталог исключений (BankError и пять его потомков с готовыми сообщениями) и функция is_russian_name. Сообщение бери из атрибута класса: raise ValidationError(ValidationError.PIN_INVALID). Порядок проверок в каждом методе всегда такой: ValidationError, NotFoundError, AccessError, BusinessRuleError, InsufficientFundsError. Данные меняй только после всех проверок.\n'
            'Что нужно проверить:\n'
            '— User.change_pin(old_pin, new_pin): оба ПИН-кода должны быть строками из 4 символов (PIN_INVALID), только из цифр (PIN_FORMAT); старый должен совпасть с текущим (PIN_MISMATCH).\n'
            '— Bank.apply_for_card: ПИН-код проверяется как выше; фамилия и имя через is_russian_name (NAME_INVALID); платёжная система должна быть среди BINS (SYSTEM_UNKNOWN, сообщение .format(system=...)); если телефон уже у клиента с другими фамилией или именем, BusinessRuleError.PHONE_TAKEN; если у клиента уже MAX_CARDS карт, BusinessRuleError.TOO_MANY_CARDS (.format(n=MAX_CARDS)). Если ошибка случилась, ни клиент, ни счёт, ни карта не должны попасть в банк.\n'
            '— Card.get_card_info и get_balance: если у карты нет счёта (account равен None), AccessError.NO_ACCOUNT; если статус не ACTIVE (закрыта или заблокирована), AccessError.CARD_INACTIVE.\n'
            '— Card.deposit: сумма должна быть числом больше нуля (AMOUNT_INVALID); затем доступ как выше; если сумма больше DEPOSIT_LIMIT, карта становится BLOCKED и вызывается BusinessRuleError.DEPOSIT_LIMIT.\n'
            '— Card.pay: сумма (AMOUNT_INVALID), потом MCC должен быть строкой из 4 цифр (MCC_INVALID), доступ, MCC не должен быть среди FORBIDDEN_MCC (BusinessRuleError.MCC_FORBIDDEN, .format(mcc=...), карту не блокируем), сумма не больше PAY_LIMIT (иначе блокировка карты и PAY_LIMIT), хватает ли денег (InsufficientFundsError.FOR_PAY).\n'
            '— Card.transfer(to_card, amount): сумма (AMOUNT_INVALID); получатель должен быть объектом Card (NotFoundError.CARD_NOT_FOUND); доступ отправителя (NO_ACCOUNT, CARD_INACTIVE); у получателя есть счёт (AccessError.RECIPIENT_NO_ACCOUNT) и он активен (RECIPIENT_INACTIVE); нельзя переводить на ту же карту (SELF_TRANSFER); лимит TRANSFER_LIMIT (блокировка отправителя и TRANSFER_LIMIT); хватает ли денег (FOR_TRANSFER).\n'
            '— CashbackCard и SavingsCard: ставка должна быть числом больше нуля (ValidationError.RATE_INVALID) и не больше MAX_RATE (BusinessRuleError.RATE_TOO_HIGH); проверка идёт до создания карты. CashbackCard.pay проверяет всё так же, как Card.pay. SavingsCard.pay всегда вызывает BusinessRuleError.SAVINGS_PAY, а accrue_interest сначала проверяет доступ.',
            'Не повторяй одинаковые проверки: вынеси их в маленькие методы Card. Проверка доступа: _ensure_usable (счёт есть, статус ACTIVE). Проверка суммы: _check_amount (isinstance(amount, (int, float)) и amount > 0). Проверки покупки: _check_pay(amount, mcc), его же вызывает CashbackCard.pay.\n'
            'Блокировка при лимите: сначала self.status = CardStatus.BLOCKED, потом raise. Строка raise после присваивания статуса сработает, и статус останется изменённым.\n'
            'Чтобы ошибка в apply_for_card не оставила следов, создай клиента, счёт и карту как объекты, а в словари банка и списки клиента клади только в самом конце. Для классов карт со ставкой проверяй ставку в __init__ перед super().__init__(**kwargs).\n'
            'Телефон занят: найди среди customers клиента с таким же phone; если у него другие фамилия или имя, это PHONE_TAKEN. Если те же, это тот же клиент, и его число карт нужно сравнить с MAX_CARDS.\n'
            'Порядок проверок в методе строго по дереву ошибок: ввод, потом нахождение объекта, доступ, правила банка, деньги. Тест печатает тип и сообщение ошибки, поэтому тип должен совпасть.',
            _pick(4, 'sol'), SC.S4, bonus=80, tail=TL, starter=_pick(4, 'start'))

    # ============ Теория 9: страж и командная строка ============
    terms9 = [
        ('Counter', 'Класс из модуля collections, который считает, сколько раз встретилось каждое значение. Работает как словарь: обращение к отсутствующему ключу даёт 0, поэтому можно сразу писать counter[ключ] += 1.\n\nПример:\nfrom collections import Counter\n\nerrors = Counter()\nerrors["ValidationError"] += 1\nerrors["AccessError"] += 1\nerrors["ValidationError"] += 1\nprint(errors["ValidationError"], errors["NotFoundError"])\nprint(sorted(errors.items()))\nВывод:\n2 0\n[(\'AccessError\', 1), (\'ValidationError\', 2)]'),
    ]
    code_g1 = '''import sys
from collections import Counter
from functools import wraps


class BankError(Exception):
    pass


class ValidationError(BankError):
    pass


class NotFoundError(BankError):
    pass


errors = Counter()
balances = {"1": 100.0, "2": 50.0}


def guard(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BankError as err:
            errors[type(err).__name__] += 1
            return f"Ошибка ({type(err).__name__}): {err}"
    return wrapper


def number(text):
    try:
        return float(text)
    except ValueError:
        raise ValidationError("Ожидалось число")


@guard
def execute(line):
    parts = line.split()
    if len(parts) == 2 and parts[0] == "balance":
        if parts[1] not in balances:
            raise NotFoundError("Нет такой карты")
        return f"Баланс: {balances[parts[1]]:.2f}"
    if len(parts) == 3 and parts[0] == "add":
        balances[parts[1]] = balances.get(parts[1], 0) + number(parts[2])
        return "Готово"
    raise ValidationError("Неизвестная команда")


for line in sys.stdin:
    line = line.strip()
    if line == "exit":
        break
    if line:
        print(execute(line))
print(sorted(errors.items()))'''
    body9 = '''
<p>Последний этап превращает наш набор классов в «настоящую» программу. Пользователь вводит команды («пополни карту 1 на 500»), программа их выполняет, а все ошибки превращает в понятные сообщения. Падать нельзя ни при каких данных. Нужны три идеи.</p>
<h3>1. Декоратор-страж</h3>
<p>Ловить ошибки в каждой команде отдельным <code>try</code> долго и повторяется. В теме про декораторы ты узнал, как обернуть функцию. Напишем декоратор <code>guard</code>: он вызывает функцию и, если вылетела ошибка банка, возвращает её текст вместо падения. Заодно он ведёт статистику: сколько ошибок каждого вида.</p>
<p>Для подсчёта используем [[Counter|Counter]]: он сам заводит счётчик на каждое новое имя, поэтому достаточно <code>errors[имя] += 1</code>.</p>
<h3>2. Разбор команды</h3>
<p>Команда приходит строкой, например <code>"deposit 1 500"</code>. Метод <code>split()</code> режет её на слова: <code>["deposit", "1", "500"]</code>. Первое слово это команда, остальные её аргументы. Все они приходят строками, поэтому номер карты и сумму нужно преобразовать в числа, а если пользователь написал вместо числа «abc», не дать упасть <code>ValueError</code>, а вызвать нашу <code>ValidationError</code>. Для этого пригодится маленькая функция-помощник вроде <code>number(text)</code>. Неизвестную команду или неверное число аргументов тоже считаем ошибкой ввода.</p>
<h3>3. Чтение команд</h3>
<p>Команды можно читать из <code>sys.stdin</code> (как в темах про потоковый ввод): <code>for line in sys.stdin:</code>. Пустые строки пропускаем, а строка <code>exit</code> завершает работу. В конце печатаем итог: сколько всего было ошибок и сколько каждого вида.</p>
<p>Всё вместе в миниатюре (команды <code>balance</code> и <code>add</code>, свои ошибки, страж и статистика):</p>
''' + ex(code_g1, ['balance 1', 'balance 9', 'add 1 abc', 'add 1 25.5', 'balance 1', 'dance', 'exit']) + '''
<p>Посмотри на вывод. Неверные команды не прервали программу: каждая дала строку «Ошибка (...)», а потом работа продолжилась. После <code>exit</code> программа вывела статистику: <code>sorted(errors.items())</code> даёт пары «вид ошибки: сколько раз» в алфавитном порядке названий. На этапе 5 ты напишешь такой же «пульт» для настоящего банка: команды выпуска карт, пополнений, покупок, переводов и истории.</p>
'''
    th9 = th('Поддержка работы: страж и командная строка', terms9, body9)

    # ============ Проект 5 ============
    s5 = [SC.S5[2], SC.S5[0], SC.S5[1]]
    p5 = pj('Банк, этап 5: командная строка банка',
            'Финал. Сделай из банка программу, которой можно управлять командами. Код этапа 4 лежит в заготовке. Допиши в конец: программа создаёт банк Bank("Банк Кролика", "044525225"), читает команды из sys.stdin (по одной на строку, пустые строки пропускай) и выполняет их. Строка exit завершает чтение (остальные строки игнорируются). Номера карт в командах это card_id.\n'
            'Команды и ответы (каждый ответ печатается отдельной строкой, у history несколько строк):\n'
            '— apply Фамилия Имя ПИН телефон система [тип]: выпускает карту (тип simple по умолчанию, или cashback, или savings). Ответ: «Выпущена карта #N (тип), PAN ...».\n'
            '— deposit id сумма, pay id сумма mcc, transfer id_отправителя id_получателя сумма: операции. Ответ: «Готово. Карта #N: Баланс: X₽» (N это первая карта в команде).\n'
            '— balance id: «Карта #N: Баланс: X₽». info id: визитка карты (get_card_info). close id: «Карта #N закрыта». pin id старый новый: «ПИН-код изменён».\n'
            '— history id: строка «История карты #N:», а за ней строки истории или одна строка «(операций нет)».\n'
            '— accrue id: начисляет проценты на накопительной карте и отвечает «Проценты начислены. Карта #N: Баланс: X₽»; на карте другого типа вызывает BusinessRuleError.NOT_SAVINGS.\n'
            'Любая ошибка банка не останавливает программу: вместо ответа печатается «Ошибка (ИмяКласса): сообщение». Неизвестная команда или неверное число аргументов: ValidationError.BAD_COMMAND. Нечисловой номер карты или сумма: ValidationError.NOT_A_NUMBER. Карты с таким номером нет: NotFoundError.NO_SUCH_CARD (все три сообщения уже в каталоге).\n'
            'Когда ввод закончился, печатается итог: «Ошибок не было» или «Всего ошибок: N», а затем по строке вида «  ИмяКласса: число» для каждого вида ошибок (два пробела в начале, виды в алфавитном порядке).',
            'Сделай декоратор guard (functools.wraps): ловит BankError, увеличивает errors[type(err).__name__] (errors = Counter()) и возвращает строку «Ошибка (...)». Навесь его на функцию execute(bank, line), которая выполняет одну команду и возвращает ответ.\n'
            'Разбор: parts = line.split(); cmd, args = parts[0], parts[1:]. Для каждой команды проверяй и имя, и число аргументов (len(args)); в конце функции вызови ValidationError(ValidationError.BAD_COMMAND) для неизвестной.\n'
            'Помощники: number(text) превращает строку в float и при ValueError вызывает ValidationError(NOT_A_NUMBER). find_card(bank, text) делает int(text) (так же ловит ValueError) и ищет карту в bank.cards, а если её нет, вызывает NotFoundError(NO_SUCH_CARD).\n'
            'Тип карты из apply берётся из словаря {"simple": SimpleDebitCard, "cashback": CashbackCard, "savings": SavingsCard}. Остальные аргументы apply передавай в bank.apply_for_card(...) как есть: ПИН-код, телефон и система уже строки.\n'
            'accrue: проверь isinstance(card, SavingsCard), иначе вызови BusinessRuleError.NOT_SAVINGS. История пустая, если card.get_history() вернул пустой список.\n'
            'Итог: total = sum(errors.values()); для вывода по видам перебери sorted(errors.items()).',
            _pick(5, 'sol'), s5, bonus=100, starter=_pick(5, 'start'))

    return topic('Большой проект: банк', 'Enum, dataclass, связи объектов, наследование карт, иерархия ошибок, команды банка',
                 [th1, th2, th3, fl1, ts1, th4, th5, fl2, p1, th6, p2, th7, fl3, p3, th8, fl4, ts2, p4, th9, p5])
