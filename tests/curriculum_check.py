"""Проверяет учебный план curriculum.json и перестраивает таблицы в docs/CURRICULUM.md.
Запуск из корня репозитория: py tests/curriculum_check.py
Правила стиля названий описаны в docs/CURRICULUM.md («Единый стиль названий»)."""
import json, re, sys

c = json.load(open('course/curriculum.json', encoding='utf-8'))
T, H = c['topics'], c['holes']
ids = [t['id'] for t in T]
bad = []
LAT = re.compile(r'[A-Za-z]')

for i, t in enumerate(T):
    w = t['id']
    for p in t['pre']:
        if p not in ids or ids.index(p) >= i:
            bad.append(f'{w}: пререквизит {p} не раньше темы')
    n, s = t['n'], t['s']
    if LAT.search(n) or ':' in n or n.endswith('.') or n[0] != n[0].upper():
        bad.append(f'{w}: название «{n}»: русские слова, без двоеточия и точки, с заглавной')
    if len(n.split()) > 4:
        bad.append(f'{w}: название длиннее 4 слов')
    if not s or len(s) > 60 or s.endswith('.') or re.match(r'[А-ЯЁ]', s):
        bad.append(f'{w}: подзаголовок «{s}»: до 60 знаков, русское слово со строчной, без точки')
for h in H:
    n = h['n']
    if h['after'] not in ids:
        bad.append(f'нора {h["id"]}: нет темы {h["after"]}')
    if n.count(':') != 1 or len(n.split(':')[0].split()) > 2 or n.endswith('.'):
        bad.append(f'нора {h["id"]}: «{n}» — нужно «Короткое имя: что делаем», имя 1–2 слова')

seen = {}
for t in T + H:
    for kind, names in t.get('introduces', {}).items():
        for x in names:
            if (kind, x) in seen:
                bad.append(f'{x} ({kind}) вводится дважды: {seen[(kind, x)]} и {t["id"]}')
            seen[(kind, x)] = t['id']

# таблицы для docs/CURRICULUM.md
num = {t['id']: k for k, t in enumerate(T)}
rows = ['| № | Тема | Подзаголовок | Мин | Опирается на | Проект |', '|---|------|--------------|----:|--------------|--------|']
for k, t in enumerate(T):
    pre = ', '.join(str(num[p]) for p in t['pre']) or '—'
    rows.append(f"| {k} | {t['n']} | {t['s']} | {t['min']} | {pre} | {t.get('project', '')} |")
tot = sum(t['min'] for t in T)
rows.append('')
rows.append(f'Всего {len(T)} тем, ≈{tot / 60:.0f} ч основного пути.')
holes = ['| Нора | После темы | Как запускается | Мин |', '|------|-----------|-----------------|----:|']
RUN = {'native': 'обычный Python', 'native-vfs': 'виртуальная ФС Pyodide', 'shim': 'учебная имитация',
       'pyodide-package': 'пакет Pyodide (нужен интернет)', 'read-only': 'код для ПК + проверяемые задачи',
       'read-only+native': 'частично в приложении, частично код для ПК', 'shim+pyodide-package': 'учебная имитация + пакет Pyodide',
       'shim+read-only': 'учебная имитация + код для ПК', 'native+read-only': 'частично в приложении, частично код для ПК'}
for h in H:
    holes.append(f"| {h['n']} | {num[h['after']]} {T[num[h['after']]]['n']} | {RUN[h['run']]} | {h['min']} |")

md = old_md = open('docs/CURRICULUM.md', encoding='utf-8').read()
for tag, body in (('TOPICS', rows), ('HOLES', holes)):
    a, b = f'<!-- {tag}:начало -->', f'<!-- {tag}:конец -->'
    if a not in md:
        bad.append(f'в docs/CURRICULUM.md нет метки {a}')
        continue
    md = md[:md.index(a) + len(a)] + '\n' + '\n'.join(body) + '\n' + md[md.index(b):]
if md != old_md:  # перезаписываем, только если таблицы изменились (файл может быть открыт в редакторе)
    open('docs/CURRICULUM.md', 'w', encoding='utf-8', newline='\n').write(md)

print('тем', len(T), 'нор', len(H), 'минут', tot, 'нарушений', len(bad))
for x in bad:
    print(' -', x)
sys.exit(1 if bad else 0)
