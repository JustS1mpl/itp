import json, subprocess, html, random, hashlib, re, sys, os

PY = sys.executable
os.environ['PYTHONPATH'] = os.path.abspath('shim') + os.pathsep + os.environ.get('PYTHONPATH', '')
from c_x import XMAP
USED = set()
FILESETS = {}


def _fd(f):
    return FILESETS[f] if isinstance(f, str) else f

EX = []   # примеры из теории: для проверки в Skulpt
FL = []   # вопросы «что выведет»: для проверки в Skulpt
TK = []   # задачи: для проверки в Skulpt


def esc(s):
    return html.escape(s, quote=False)


WRAP = r'''
import sys, builtins, io
_L = %r
_lines = iter(_L)
sys.stdin = io.StringIO(''.join(x + '\n' for x in _L))
def _input(p=''):
    v = next(_lines)
    sys.stdout.write('\x03' + p + '\x04' + '\x01' + v + '\x02\n')
    return v
builtins.input = _input
exec(compile(%r, '<ex>', 'exec'), {'__name__': '__main__'})
'''


def run(code, lines=None, files=None):
    """возвращает (plain, transcript_html)"""
    import tempfile
    lines = lines or []
    d = tempfile.mkdtemp()
    for k, v in (files or {}).items():
        open(d + '/' + k, 'w', encoding='utf-8', newline='').write(v)
    r = subprocess.run([PY, '-c', WRAP % (lines, code)], capture_output=True, text=True, timeout=15, cwd=d, input=None)
    assert r.returncode == 0, (code, r.stderr)
    raw = r.stdout
    plain = re.sub(r'\x03.*?\x04', '', raw)
    plain = re.sub(r'\x01.*?\x02\n', '', plain)
    tr = esc(raw)
    tr = re.sub(r'\x03(.*?)\x04', r'\1', tr)
    tr = re.sub(r'\x01(.*?)\x02', r'<span class="ty">\1</span>', tr)
    return plain, tr


def ex(code, lines=None, files=None):
    code = code.strip('\n')
    plain, tr = run(code, lines, files)
    EX.append(dict(code=code, lines=lines or [], out=plain, files=files))
    cls = 'out con' if lines else 'out'
    return '<pre>' + code + '</pre><pre class="' + cls + '">' + tr.rstrip('\n') + '</pre>'


def tu(code, note=''):
    """пример с черепахой: код, вывод (если есть) и кнопка «Показать рисунок»"""
    code = code.strip('\n')
    plain, tr = run(code)
    EX.append(dict(code=code, lines=[], out=plain))
    h = '<pre>' + code + '</pre>'
    if plain.strip():
        h += '<pre class="out">' + tr.rstrip('\n') + '</pre>'
    return h + '<div class="tudemo"><button class="btn g" type="button" data-tu="' + html.escape(code, quote=True).replace('[', '&#91;') + '">🐢 Показать рисунок</button><span class="tumsg" role="status"></span></div>'


def exs(code, out):
    """пример без запуска (ошибка или код, который не запускается в Skulpt)"""
    return '<pre>' + code.strip('\n') + '</pre><pre class="out">' + esc(out) + '</pre>'


def exnr(code, lines, note_out=None):
    """код показываем, вывод считаем в CPython, но в Skulpt не проверяем"""
    code = code.strip('\n')
    plain, tr = run(code, lines)
    return '<pre>' + code + '</pre><pre class="out con">' + tr.rstrip('\n') + '</pre>'


def _opts(text, c, right, wrongs):
    opts = [right] + list(wrongs)
    assert len(set(opts)) == len(opts), (text, opts)
    for o in opts:
        assert len(o) <= 60, (text, o)
    rnd = random.Random(int(hashlib.md5((text + str(c) + right).encode()).hexdigest(), 16))
    pos = rnd.randrange(len(opts))
    opts.remove(right)
    opts.insert(pos, right)
    return opts, pos


def q(text, right, wrongs, e, c=None):
    opts, pos = _opts(text, c, right, wrongs)
    d = {'q': text}
    if c:
        d['c'] = c.strip('\n')
    d['o'] = opts
    d['a'] = pos
    d['e'] = e
    for k, v in XMAP.items():
        if text.startswith(k):
            code, lines = v[0].strip('\n'), v[1]
            if len(v) > 2:
                out = v[2]
            else:
                plain, _ = run(code, lines)
                out = plain.rstrip('\n')
                EX.append(dict(code=code, lines=lines, out=plain))
            d['x'] = code
            d['xo'] = out
            if lines:
                d['xi'] = lines
            USED.add(k)
            break
    return d


def qo(text, code, wrongs, e, lines=None):
    code = code.strip('\n')
    plain, _ = run(code, lines)
    right = plain.rstrip('\n')
    assert '\n' not in right, (code, right)
    t = text
    if lines:
        t += ' Пользователь вводит ' + ('по очереди: ' + ', '.join(lines) if len(lines) > 1 else lines[0]) + '.'
    FL.append(dict(code=code, lines=lines or [], right=right))
    wrongs = [w for w in wrongs if w != right]
    assert len(wrongs) >= 2, ('мало неверных вариантов', code, right, wrongs)
    return q(t, right, wrongs, e, code)


def fl(name, qs):
    assert 1 <= len(qs) <= 30
    return {'t': 'flash', 'n': name, 'q': qs}


def th(name, terms, body):
    names = [t[0] for t in terms]
    scan = re.sub(r'<pre[^>]*>[\s\S]*?</pre>', '', body)
    for pm in re.finditer(r'<pre class="out[^>]*>([\s\S]*?)</pre>', body):
        assert not re.search(r'\[\[[^\]|]+\]\]', pm.group(1)), ('вывод [[...]] принят за термин', pm.group(1)[:60])
    for m in re.finditer(r'\[\[([^\]|]+)', scan):
        assert m.group(1) in names, ('нет термина', m.group(1), name)
    d = {'t': 'theory', 'n': name}
    if terms:
        d['terms'] = [{'n': a, 'd': b} for a, b in terms]
    d['html'] = body
    return d


def _inp(s):
    return s.split('\n') if s != '' else []


def _norm_out(o, strict):
    ls = [l.rstrip() for l in o.replace('\r', '').split('\n')]
    return '\n'.join(ls).strip('\n')


def _exfmt(inputs, out):
    li = _inp(inputs)
    if len(li) <= 1 and '\n' not in out:
        return ('Вход: ' + inputs + '\n' if inputs else '') + 'Вывод: ' + out
    return ('Вход:\n' + '\n'.join(li) + '\n' if li else '') + 'Вывод:\n' + out


def _tests(sol, inputs, exp, where, files=None):
    tests = []
    for inp in inputs:
        plain, _ = run(sol, _inp(inp), files)
        out = _norm_out(plain, False)
        if exp and inp in exp:
            assert out == exp[inp], (where, inp, out, exp[inp])
        tests.append([inp, out])
    return tests


def task(q_, h, sol, inputs, strict=False, exp=None, ex_=None, files=None):
    sol = sol.strip('\n')
    tests = _tests(sol, inputs, exp, q_, _fd(files))
    TK.append(dict(where=q_, sol=sol, tests=tests, strict=strict, files=_fd(files)))
    d = {'q': q_, 'ex': ex_ if ex_ is not None else _exfmt(inputs[0], tests[0][1]), 'h': h, 'tests': tests, 'sol': sol}
    if strict:
        d['strict'] = 1
    if files:
        d['f'] = files
    return d


def ts(name, tasks):
    assert 1 <= len(tasks) <= 99
    return {'t': 'test', 'n': name, 'tasks': tasks}


def pj(name, q_, h, sol, inputs, strict=False, exp=None, bonus=None, ex_=None, files=None):
    sol = sol.strip('\n')
    tests = _tests(sol, inputs, exp, name, _fd(files))
    TK.append(dict(where=name, sol=sol, tests=tests, strict=strict, files=_fd(files)))
    d = {'t': 'project', 'n': name, 'q': q_, 'h': h, 'ex': ex_ if ex_ is not None else _exfmt(inputs[0], tests[0][1]), 'tests': tests}
    if bonus:
        d['bonus'] = bonus
    d['sol'] = sol
    if strict:
        d['strict'] = 1
    if files:
        d['f'] = files
    return d


def topic(n, s, items, intro=False):
    d = {'n': n, 's': s}
    if intro:
        d['intro'] = 1
    d['items'] = items
    return d


# ---------- сериализация в JS (одинарные кавычки) ----------
def jstr(s):
    s = s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
    s = s.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029').replace('</', '<\\/')
    return "'" + s + "'"


def js(v, ind=0, brk=False):
    if isinstance(v, str):
        return jstr(v)
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if v is None:
        return 'null'
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        if brk:
            pad = ' ' * (ind + 1)
            return '[\n' + ',\n'.join(pad + js(x, ind + 1, brk) for x in v) + ']'
        return '[' + ','.join(js(x, ind, False) for x in v) + ']'
    if isinstance(v, dict):
        parts = []
        for k, x in v.items():
            b = k in ('items', 'q', 'tasks', 'terms') and isinstance(x, list)
            kk = k if re.match(r'^[A-Za-z_$][A-Za-z0-9_$]*$', k) else jstr(k)
            parts.append(kk + ':' + js(x, ind, b))
        return '{' + ','.join(parts) + '}'
    raise TypeError(v)


def topics_js(topics):
    return 'var FILESETS=' + js(FILESETS) + ';\nvar TOPICS=[\n' + ',\n'.join(js(t, 0, False).replace('items:[\n', 'items:[\n') for t in topics) + '\n];'
