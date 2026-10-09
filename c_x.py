# Примеры кода к объяснениям вопросов: ключ = начало текста вопроса
XMAP = {
 'Строка «Итого:» занимает 6': ('''line = "Итого:"
print(len(line))
print(f"{line}{'6руб':>29}")
print(len(f"{line}{'6руб':>29}"))''', []),
 'Как выровнять значение, которое собрано': ('''weight = 3
price = 2
detail = f"{weight}кг * {price}руб/кг"
print(f"Цена:{detail:>30}")
print(f"Цена:{weight}кг * {price}руб/кг:>30")''', []),
 'В каком порядке записываются части формата': ('''print(f"[{'a':.^7}]")
print(f"[{'a':*<7}]")
print(f"[{'a':#>7}]")''', []),
 'Какой тип будет у значения, которое вернул input': ('''x = input()
print(x, type(x))
print(int(x) + 1)''', ['25']),
 'Как правильно прочитать дробное число': ('''x = float(input())
print(x * 2)''', ['2.5']),
 'Как проверить, что число n чётное': ('''for n in 6, 7:
    print(n, n % 2 == 0)''', []),
 'Как проверить, что x равен 10': ('''x = 10
print(x == 10)
x = 5
print(x == 10)''', []),
 'Сколько веток выполнится в цепочке': ('''n = 15
if n > 10:
    print("больше 10")
elif n > 5:
    print("больше 5")
else:
    print("мало")''', []),
 'Как правильно проверить, что grade равен 4 или 5': ('''grade = 3
print(grade == 4 or grade == 5)
print(grade == 4 or 5)''', []),
 'Какая запись равна условию x >= 0 and x < 100': ('''for x in -1, 50, 100:
    print(x, 0 <= x < 100)''', []),
 'Как сравнить два слова a и b без учёта регистра': ('''a = "Python"
b = "PYTHON"
print(a == b)
print(a.lower() == b.lower())''', []),
 'Что делает запись count += 1': ('''count = 4
count += 1
print(count)
count += 1
print(count)''', []),
 'Как напечатать числа от 1 до 10': ('''for i in range(1, 11):
    print(i, end=" ")
print()
for i in range(10):
    print(i, end=" ")''', []),
 'Какое выражение даёт, сколько процентов': ('''a = 3
b = 8
print(a * 100 / b)
print(a / b * 100)''', []),
 'Что делает map(int, строка.split())': ('''parts = input().split()
nums = list(map(int, parts))
print(parts)
print(nums)
print(sum(nums))''', ['4 7 10']),
 'Как записать ширину поля, которая хранится': ('''text = "кот"
width = 9
print(f"[{text:^{width}}]")
width = 5
print(f"[{text:^{width}}]")''', []),
 'Какой индекс имеет самый первый символ': ('''word = "Питон"
print(word[0])
print(word[1])''', []),
 'Строка состоит из 7 символов': ('''word = "ракушка"
print(len(word))
print(word[6])
print(word[len(word) - 1])''', []),
 'Какой отрицательный индекс у последнего': ('''for word in "кот", "самолёт":
    print(word[-1])''', []),
 'Какой цикл подходит, если нужны и номер': ('''text = "abc"
for i, ch in enumerate(text):
    print(i, ch)''', []),
 'Какой срез даёт первые пять символов': ('''text = "программа"
print(text[:5])
print(text[5])
print(text[:4])''', []),
 'Что делают методы строк с самой строкой': ('''s = "привет"
t = s.upper()
print(s)
print(t)''', []),
 'Какой метод безопаснее, если подстроки': ('''s = "привет"
print(s.find("з"))
print(s.index("з"))''', [], '-1\nValueError: substring not found'),
 'Чем remove отличается от pop': ('''a = [5, 7, 5, 9]
a.remove(5)
print(a)
x = a.pop(0)
print(x, a)''', []),
 'Как сделать копию списка a': ('''a = [1, 2]
b = a
c = a.copy()
a.append(3)
print(b)
print(c)''', []),
 'Какой функцией собрать строку из списка букв': ('''letters = ["п", "и", "т"]
print(str(letters))
print("".join(letters))''', []),
 'Какой элемент стека снимается первым': ('''stack = [1, 2, 3]
stack.append(4)
print(stack.pop())
print(stack)''', []),
 'Как создать пустое множество': ('''a = {}
b = set()
print(type(a))
print(type(b))''', []),
 'Почему перед выводом множества часто': ('''s = {3, 1, 2, 3}
print(sorted(s))
print(len(s))''', []),
 'Какой знак находит общие элементы': ('''a = {1, 2, 3}
b = {2, 3, 4}
print(sorted(a | b))
print(sorted(a & b))
print(sorted(a - b))
print(sorted(a ^ b))''', []),
 'Какая операция оставляет элементы, которые есть ровно': ('''a = {1, 2, 3}
b = {3, 4}
print(sorted(a ^ b))''', []),
 'Что проверяет выражение a <= b для множеств': ('''a = {1, 2}
b = {1, 2, 3}
print(a <= b)
print(b <= a)''', []),
 'Чем remove отличается от discard': ('''s = {1, 2}
s.discard(5)
print(s)
s.remove(5)''', [], '{1, 2}\nKeyError: 5'),
 'Что может быть ключом словаря': ('''d = {}
d["a"] = 1
d[(1, 2)] = 2
print(d)
d[[1, 2]] = 3''', [], "{'a': 1, (1, 2): 2}\nTypeError: unhashable type: 'list'"),
 'Что получает переменная x в цикле for x in d': ('''d = {"a": 1, "b": 2}
for x in d:
    print(x)
for x in d.values():
    print(x)''', []),
 'Как посчитать, сколько раз встретилось слово w': ('''counts = {}
for w in "a b a".split():
    counts[w] = counts.get(w, 0) + 1
print(counts)''', []),
 'Что будет, если оставить тело цикла совсем пустым': ('''for i in range(3):
    pass
print("готово")''', []),
 'Почему rating = 0 пишут внутри': ('''for pupil in 1, 2:
    rating = 0
    for score in 4, 5:
        rating += score
    print(rating)''', []),
 'Чем список отличается от строки': ('''s = "кот"
a = ["к", "о", "т"]
a[0] = "р"
print(a)
s[0] = "р"''', [], "['р', 'о', 'т']\nTypeError: 'str' object does not support item assignment"),
}
