from dsl import *

# Нора после «Наследование»: окна на tkinter. В браузере окна не открываются: код окна показан для компьютера (<pre class="pc">),
# а в приложении — вопросы «что произойдёт» и задачи на логику, которую окно вызывает (калькулятор, заметки, трекер привычек).
# Две теории: окно и виджеты; события и обработчики (логика отдельно от окна). Мини-проект — трекер привычек.

WINDOW = ('import tkinter as tk\n\nroot = tk.Tk()\nroot.title("Привет")\nroot.geometry("300x150")\n\nlabel = tk.Label(root, text="Как тебя зовут?")\nlabel.pack(pady=5)\n'
          'entry = tk.Entry(root)\nentry.pack()\n\n\ndef greet():\n    label.config(text=f"Привет, {entry.get()}!")\n\n\ntk.Button(root, text="Поздороваться", command=greet).pack(pady=5)\n'
          'root.mainloop()')
CALC = ('import tkinter as tk\nfrom calc_logic import Calculator   # класс из задачи ниже — в отдельном файле\n\ncalc = Calculator()\nroot = tk.Tk()\n'
        'display = tk.Label(root, text="0", font=("Arial", 24), anchor="e", width=12)\ndisplay.grid(row=0, column=0, columnspan=4)\n\n\ndef click(key):\n'
        '    display.config(text=calc.press(key))\n\n\nfor i, key in enumerate("789/456*123-0C=+"):\n    tk.Button(root, text=key, width=4, command=lambda k=key: click(k)).grid(row=1 + i // 4, column=i % 4)\n'
        'root.mainloop()')


def th_window():
    terms = [
        ('tkinter', 'Встроенная в Python библиотека окон: кнопки, поля, надписи. На компьютере работает без установки, в браузере — нет.'),
        ('виджет', 'Элемент окна: Label — надпись, Entry — поле ввода, Button — кнопка, Listbox — список. Виджет создают и размещают в окне через pack или grid.'),
        ('mainloop', 'root.mainloop() — запустить цикл событий окна: программа ждёт нажатий и вызывает обработчики, пока окно не закроют.'),
    ]
    body = (
        '<p>Программы с окнами и кнопками на Python делают модулем [[tkinter]] — он встроен в Python и на компьютере работает сразу. В браузере ИТП '
        'окна не открываются, поэтому код окна — для компьютера, а в задачах будем писать логику, которую окно вызывает.</p>'
        '<pre class="pc">' + WINDOW + '</pre>'
        '<p>Окно состоит из [[виджет]]ов: надпись Label, поле Entry, кнопка Button. Каждый создают, указав окно-родителя, и размещают: '
        '<code>pack()</code> ставит виджеты друг под другом, <code>grid(row=…, column=…)</code> — в клетки таблицы. Последняя строка — [[mainloop]]: '
        'с неё окно начинает жить и отвечать на нажатия.</p>'
        '<p>Код после <code>mainloop()</code> выполнится только когда окно закроют, поэтому всё, что должно работать, настраивают до него.</p>'
    )
    return th('Окно и виджеты', terms, body)


def fl_window():
    return fl('Окно и виджеты', [
        q('Что делает root.mainloop()?', 'Запускает цикл событий: окно ждёт нажатий до закрытия', ['Закрывает окно', 'Рисует все виджеты заново'],
          'Код после него выполнится после закрытия окна.'),
        q('Какой виджет нужен, чтобы пользователь ввёл своё имя?', 'Entry', ['Label', 'Button'], 'Label только показывает текст.'),
        q('Чем grid отличается от pack?', 'grid ставит виджеты в клетки таблицы, pack — друг за другом', ['Ничем', 'grid работает только с кнопками'],
          'Калькулятор удобно делать на grid.'),
    ])


def th_events():
    terms = [
        ('обработчик', 'Функция, которую окно вызывает при событии: Button(..., command=функция) — при нажатии. Передают саму функцию, без скобок.'),
        ('событие', 'То, на что программа реагирует: нажатие кнопки, клавиши, движение мыши. Программа с окном не идёт по строкам сверху вниз, '
                    'а ждёт событий.'),
    ]
    body = (
        '<p>Программа с окном живёт [[событие]]м: нажали кнопку — вызвалась функция-[[обработчик]]. Её передают в <code>command</code> без скобок: '
        '<code>command=greet</code>. Со скобками <code>command=greet()</code> функция вызовется сразу при создании кнопки, а кнопка '
        'получит её результат — частая ошибка.</p>'
        '<p>Когда кнопок много и обработчик у них общий, нужный аргумент передают через lambda: <code>command=lambda k=key: click(k)</code>. '
        '<code>k=key</code> запоминает значение в момент создания кнопки — без него все кнопки взяли бы последнее значение цикла.</p>'
        '<p>Главный приём — держать логику отдельно от окна. Окно калькулятора только показывает кнопки и передаёт нажатия в объект, а '
        'считает класс без tkinter — его можно проверить в ИТП:</p>'
        '<pre class="pc">' + CALC + '</pre>'
        '<p>Такую логику проверяют, «нажимая кнопки» кодом:</p>'
        + ex('class Counter:\n    def __init__(self):\n        self.value = 0\n\n    def press(self, key):\n        if key == "+":\n            self.value += 1\n'
             '        elif key == "-":\n            self.value -= 1\n        elif key == "сброс":\n            self.value = 0\n        return str(self.value)\n\n\n'
             'c = Counter()\nfor key in ["+", "+", "-", "+", "сброс", "-"]:\n    print(key, "→", c.press(key))')
    )
    return th('События и обработчики', terms, body)


def fl_events():
    return fl('События и обработчики', [
        q('Что не так в Button(root, text="Ок", command=save())?', 'save вызовется сразу, а не при нажатии', ['Нужно писать commands', 'Кнопке нельзя давать функцию'],
          'Передают саму функцию: command=save.'),
        q('Зачем в lambda k=key: click(k) пишут k=key?', 'Чтобы запомнить значение key в момент создания кнопки',
          ['Без этого lambda не скомпилируется', 'Чтобы кнопка стала круглой'], 'Иначе все кнопки получат последнее key из цикла.'),
        q('Зачем логику калькулятора писать отдельным классом без tkinter?', 'Её можно проверить без окна, а окно менять отдельно',
          ['tkinter не умеет складывать числа', 'Так окно открывается быстрее'], 'Окно только передаёт нажатия.'),
    ])


def code_events():
    return ts('События и обработчики', [
        task('Логика калькулятора. Напиши класс Calculator с методом press(key), который возвращает строку для экрана. Кнопки: цифры, «+», «-», «*», «/», '
             '«=» и «C». Цифры дописываются к текущему числу (экран показывает его; ведущий 0 заменяется). Операция запоминает число и операцию и '
             'начинает новое число; «=» считает результат и показывает его (целое — без «.0»; деление на ноль — «Ошибка»). «C» сбрасывает всё в «0». '
             'Если перед операцией уже была операция, сначала считается она.',
             'Храни: current — строка набираемого числа, stored — запомненное число, op — операция. compute(): по op из stored и current.\n'
             'Целое без .0: int(r) if r == int(r) else r.',
             'class Calculator:\n    def __init__(self):\n        self.current = "0"\n        self.stored = None\n        self.op = None\n\n    def compute(self):\n'
             '        a, b = self.stored, float(self.current)\n        if self.op == "+":\n            r = a + b\n        elif self.op == "-":\n            r = a - b\n'
             '        elif self.op == "*":\n            r = a * b\n        else:\n            if b == 0:\n                return None\n            r = a / b\n'
             '        return int(r) if r == int(r) else r\n\n    def press(self, key):\n        if key == "C":\n            self.__init__()\n        elif key.isdigit():\n'
             '            self.current = key if self.current == "0" else self.current + key\n        elif key in "+-*/":\n            if self.op is not None:\n'
             '                r = self.compute()\n                if r is None:\n                    self.__init__()\n                    return "Ошибка"\n                self.current = str(r)\n'
             '            self.stored = float(self.current)\n            self.op = key\n            self.current = "0"\n            return str(self.stored if self.stored != int(self.stored) else int(self.stored))\n'
             '        elif key == "=" and self.op is not None:\n            r = self.compute()\n            self.__init__()\n            if r is None:\n                return "Ошибка"\n'
             '            self.current = str(r)\n        return self.current\n',
             ['c = Calculator()\nfor k in "12+30=":\n    print(c.press(k))', 'c = Calculator()\nprint(" ".join(c.press(k) for k in "7/2="))\nprint(" ".join(c.press(k) for k in "C5*4-6="))',
              'c = Calculator()\nprint(" ".join(c.press(k) for k in "9/0="))\nprint(" ".join(c.press(k) for k in "007+1="))'], tail=TL),
        task('Логика заметок. Окно заметок вызывает методы класса Notes: add(text) — добавить (пустой текст или только пробелы — не добавлять, вернуть False), '
             'delete(i) — удалить заметку с номером i (с 1; вернуть False, если такой нет), find(word) — список заметок, где есть слово без учёта регистра, '
             'listing() — строки «N. ТЕКСТ» для списка в окне. Напиши класс.',
             'Храни заметки списком. listing: [f"{i}. {t}" for i, t in enumerate(self.items, 1)].',
             'class Notes:\n    def __init__(self):\n        self.items = []\n\n    def add(self, text):\n        if not text.strip():\n            return False\n'
             '        self.items.append(text.strip())\n        return True\n\n    def delete(self, i):\n        if not 1 <= i <= len(self.items):\n            return False\n'
             '        self.items.pop(i - 1)\n        return True\n\n    def find(self, word):\n        return [t for t in self.items if word.lower() in t.lower()]\n\n'
             '    def listing(self):\n        return [f"{i}. {t}" for i, t in enumerate(self.items, 1)]\n',
             ['n = Notes()\nprint(n.add("Купить хлеб"), n.add("   "), n.add("Позвонить бабушке"))\nprint(n.listing())',
              'n = Notes()\nfor t in ["ДЗ по алгебре", "хлеб", "алгебра: №112"]:\n    n.add(t)\nprint(n.find("АЛГЕБР"))\nprint(n.delete(2), n.delete(5))\nprint(n.listing())'], tail=TL),
    ])


def project():
    return pj('Трекер привычек',
              'Окно трекера будет вызывать класс Tracker, а пока проверим его командами. Привычку отмечают по дням (номер дня — целое, начиная с 1). '
              'На вход подаются команды, последняя — «стоп»:\n— «добавить ПРИВЫЧКА» → «Добавлено: ПРИВЫЧКА» или «Уже есть: ПРИВЫЧКА»;\n'
              '— «отметить ПРИВЫЧКА ДЕНЬ» → «ПРИВЫЧКА: день ДЕНЬ отмечен» (повторная отметка ничего не меняет и пишет то же); нет привычки — «Нет привычки: ПРИВЫЧКА»;\n'
              '— «серия ПРИВЫЧКА ДЕНЬ» → «ПРИВЫЧКА: серия N» — сколько дней подряд отмечено, заканчивая этим днём (если этот день не отмечен — 0);\n'
              '— «итоги» → по привычкам в алфавитном порядке «ПРИВЫЧКА: дней D, лучшая серия B», или «Привычек нет».\n'
              'Названия привычек — одно слово. У привычки без отметок лучшая серия — 0.',
              'В Tracker словарь «привычка → множество отмеченных дней»\nСерия до дня d: пока d в множестве — считать и уменьшать d\n'
              'Лучшая серия: для каждого дня, после которого следующий не отмечен, посчитать серию до него и взять максимум',
              'class Tracker:\n    def __init__(self):\n        self.days = {}\n\n    def add(self, name):\n        if name in self.days:\n            return f"Уже есть: {name}"\n'
              '        self.days[name] = set()\n        return f"Добавлено: {name}"\n\n    def mark(self, name, day):\n        if name not in self.days:\n            return f"Нет привычки: {name}"\n'
              '        self.days[name].add(day)\n        return f"{name}: день {day} отмечен"\n\n    def streak(self, name, day):\n        n = 0\n        while day in self.days[name]:\n'
              '            n += 1\n            day -= 1\n        return n\n\n    def best(self, name):\n        return max((self.streak(name, d) for d in self.days[name]), default=0)\n\n\n'
              'tracker = Tracker()\nwhile True:\n    words = input().split()\n    if words == ["стоп"]:\n        break\n    cmd = words[0]\n    if cmd == "добавить":\n'
              '        print(tracker.add(words[1]))\n    elif cmd == "отметить":\n        print(tracker.mark(words[1], int(words[2])))\n    elif cmd == "серия":\n'
              '        if words[1] not in tracker.days:\n            print(f"Нет привычки: {words[1]}")\n        else:\n            print(f"{words[1]}: серия {tracker.streak(words[1], int(words[2]))}")\n'
              '    else:\n        if not tracker.days:\n            print("Привычек нет")\n        for name in sorted(tracker.days):\n'
              '            print(f"{name}: дней {len(tracker.days[name])}, лучшая серия {tracker.best(name)}")',
              ['добавить зарядка\nдобавить чтение\nотметить зарядка 1\nотметить зарядка 2\nотметить зарядка 4\nотметить зарядка 5\nотметить зарядка 6\n'
               'отметить чтение 2\nсерия зарядка 6\nсерия зарядка 3\nитоги\nстоп', 'итоги\nотметить бег 1\nдобавить бег\nдобавить бег\nотметить бег 1\nотметить бег 1\nитоги\nстоп'])


def build():
    return topic('Tkinter: окна и кнопки', 'окно, виджеты, события', [
        th_window(), fl_window(),
        th_events(), fl_events(), code_events(),
        project(),
    ], opt=True)
