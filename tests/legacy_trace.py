"""Ищет в собранном файле следы старого учебного материала (ветка legacy-do-not-read).
Запуск из корня репозитория: py tests/legacy_trace.py [файл.html]
Берёт из старых c_*.py и post.py все строки с русским текстом длиной от 30 знаков и проверяет, нет ли их в сборке."""
import json, re, subprocess, sys

F = sys.argv[1] if len(sys.argv) > 1 else 'out5.html'
REF = 'legacy-do-not-read'


def git(*a):
    return subprocess.run(['git', *a], capture_output=True, encoding='utf-8', check=True).stdout


files = [f for f in git('ls-tree', '--name-only', REF).split('\n') if re.fullmatch(r'c_\w+\.py|post\.py', f)]
phr = set()
for f in files:
    for m in re.finditer(r"[А-Яа-яЁё][^'\"\\\n<>]{29,}", git('show', REF + ':' + f)):
        phr.add(m.group(0).strip())
out = open(F, encoding='utf-8').read()
# общеизвестные строки, которые совпадают с чем угодно и заимствованием не являются
ALLOW = {'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'}
# названия тем и нор — из учебного плана владельца (curriculum.json), совпадение со старым курсом здесь не заимствование
_cur = json.load(open('course/curriculum.json', encoding='utf-8'))
ALLOW |= {e['n'] for e in _cur['topics'] + _cur['holes']}
hit = sorted(p for p in phr if p in out and p not in ALLOW)
print('файлов', len(files), 'фраз', len(phr), 'найдено в сборке', len(hit))
for p in hit[:40]:
    print(' -', p[:120])
sys.exit(1 if hit else 0)
