"""Учебные таблицы для тем про numpy и pandas. Запуск из корня: python3 npdata/make.py
students.csv: 1000 вымышленных учеников. Гистограмма баллов по математике (10 корзин по 10 баллов) задана руками,
чтобы совпадать с рисунком в теории.
data.csv: каждая 8-я строка присланного набора выстрелов (433 787 строк -> ~54 тыс.), чтобы не раздувать приложение."""
import csv, random, os
R = random.Random(2026)
HIST = [2, 2, 10, 26, 95, 188, 268, 216, 135, 58]
math = []
for i, n in enumerate(HIST):
    lo, hi = i * 10, i * 10 + 9
    if i == 9:
        hi = 100
    math += [R.randint(lo, hi) for _ in range(n)]
math[0] = 0
math[-1] = 100
R.shuffle(math)
rows = []
EDU = ['some high school', 'high school', 'some college', "associate's degree", "bachelor's degree", "master's degree"]
EW = [0.18, 0.20, 0.23, 0.22, 0.12, 0.05]
for m in math:
    g = 'female' if R.random() < 0.52 else 'male'
    grp = R.choices(['group A', 'group B', 'group C', 'group D', 'group E'], [0.09, 0.19, 0.32, 0.26, 0.14])[0]
    edu = R.choices(EDU, EW)[0]
    lunch = 'standard' if R.random() < 0.35 + 0.5 * m / 100 else 'free/reduced'
    prep = 'completed' if R.random() < 0.22 + 0.3 * m / 100 else 'none'
    rd = max(0, min(100, round(m + (4 if g == 'female' else -3) + R.gauss(0, 8))))
    wr = max(0, min(100, round(rd - 2 + R.gauss(0, 6) + (3 if prep == 'completed' else 0))))
    rows.append([g, grp, edu, lunch, prep, m, rd, wr])
here = os.path.dirname(os.path.abspath(__file__))
with open(here + '/students.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course', 'math score', 'reading score', 'writing score'])
    w.writerows(rows)
src = '/tmp/shots_full.csv'
if os.path.exists(src):
    L = open(src, encoding='utf-8').read().split('\n')
    out = [L[0]] + [x for i, x in enumerate(L[1:]) if x and i % 8 == 0]
    open(here + '/data.csv', 'w', encoding='utf-8', newline='').write('\n'.join(out) + '\n')
