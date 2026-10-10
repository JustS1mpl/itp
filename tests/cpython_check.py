"""Сверка всех примеров из теории, ответов вопросов и эталонных решений с настоящим CPython.

Запуск из корня репозитория после сборки (нужен checks.json, его делает build.py):
    python3 tests/cpython_check.py
Тексты в input("...") в проверку не входят, как и в приложении. Примеры с turtle пропускаются:
им нужен tkinter, который есть не везде. Код выхода 1, если есть расхождения.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRE = 'import builtins as _b\n_i = _b.input\n_b.input = lambda p="": _i()\n'


def norm(s, strict):
    rows = s.replace('\r', '').split('\n')
    if strict:
        return '\n'.join(r.rstrip() for r in rows).strip('\n')
    return '\n'.join(re.sub(r'\s+', ' ', r.strip()) for r in rows).strip()


def run(code, lines, files):
    with tempfile.TemporaryDirectory() as d:
        for name, text in (files or {}).items():
            path = os.path.join(d, name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8', newline='') as f:
                f.write(text)
        with open(os.path.join(d, 'main.py'), 'w', encoding='utf-8') as f:
            f.write(PRE + code)
        try:
            r = subprocess.run([sys.executable, '-I', 'main.py'], cwd=d, input='\n'.join(lines) + '\n' if lines else '',
                               capture_output=True, text=True, timeout=10, encoding='utf-8')
            return r.stdout, r.stderr
        except subprocess.TimeoutExpired:
            return '', 'TIMEOUT'


def main():
    ch = json.load(open(os.path.join(ROOT, 'checks.json'), encoding='utf-8'))
    jobs = []
    for n, e in enumerate(ch['EX']):
        jobs.append(('EX', n, e['code'], e['lines'], e.get('files'), e['out'], True))
    for n, e in enumerate(ch['FL']):
        jobs.append(('FL', n, e['code'], e['lines'], e.get('files'), e['right'], True))
    for n, t in enumerate(ch['TK']):
        for k, (i, o) in enumerate(t['tests']):
            jobs.append(('TK', f'{n}.{k}', t['sol'], [] if i == '' else i.split('\n'), t.get('files'), o, bool(t.get('strict'))))
    skipped = [j for j in jobs if 'turtle' in j[2]]
    jobs = [j for j in jobs if 'turtle' not in j[2]]

    def work(j):
        kind, n, code, lines, files, exp, strict = j
        out, err = run(code, lines, files)
        return (kind, n, norm(out, strict) == norm(exp, strict), code, exp, out, err)

    with ThreadPoolExecutor(8) as ex:
        bad = [r for r in ex.map(work, jobs) if not r[2]]
    print(f'проверено {len(jobs)}, пропущено (turtle) {len(skipped)}, расхождений {len(bad)}')
    for kind, n, _, code, exp, out, err in bad[:20]:
        print('-' * 60, kind, n)
        print(code[:300])
        print('ожидалось:', repr(exp[:200]))
        print('получено :', repr(out[:200]), err.strip().split('\n')[-1][:150] if err else '')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
