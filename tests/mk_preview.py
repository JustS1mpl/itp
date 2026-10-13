"""Собирает sounds-preview.html из v5/a_sound.js: страница для прослушивания и оценки звуков (только для проверки).
Код движка копируется между маркерами ENGINE:BEGIN / ENGINE:END, поэтому страница всегда играет ровно то, что в приложении.
Запуск из корня репозитория: python3 tests/mk_preview.py          — записать sounds-preview.html
                             python3 tests/mk_preview.py --check  — проверить, что страница не отстала от a_sound.js"""
import re, sys, os
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(W, 'v5/a_sound.js'), encoding='utf-8').read()
head = re.search(r'^var SX=\{.*?\};$', src, re.M).group(0)
eng = re.search(r'/\*==== ENGINE:BEGIN.*?\*/\n(.*?)/\*==== ENGINE:END ====\*/', src, re.S).group(1)
TPL = open(os.path.join(W, 'tests/preview_tpl.html'), encoding='utf-8').read()
out = TPL.replace('/*@ENGINE@*/', head + '\n' + eng)
path = os.path.join(W, 'sounds-preview.html')
if '--check' in sys.argv:
    cur = open(path, encoding='utf-8').read()
    print('OK: страница совпадает с a_sound.js' if cur == out else 'УСТАРЕЛА: запусти python3 tests/mk_preview.py')
    sys.exit(0 if cur == out else 1)
open(path, 'w', encoding='utf-8').write(out)
print('записано', path, len(out), 'байт')
