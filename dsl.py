import json, subprocess, html, random, hashlib, re, sys, os

PY = sys.executable
# модуль turtle для проверки примеров: tkinter в среде сборки нет, поэтому берём тот же файл, что работает в приложении
import shutil
_TS = os.path.abspath('.turtle_shim')
os.makedirs(_TS, exist_ok=True)
shutil.copy('v5/py/turtle_shim.py', _TS + '/turtle.py')
shutil.copy('v5/py/miniweb_shim.py', _TS + '/miniweb.py')  # учебный веб-фреймворк (нора «Веб-сервер»)
shutil.copy('v5/py/requests_shim.py', _TS + '/requests.py')  # учебный requests с виртуальными серверами: тот же файл, что в приложении
os.environ['PYTHONPATH'] = _TS + os.pathsep + os.path.abspath('shim') + os.pathsep + os.environ.get('PYTHONPATH', '')
XMAP = {}  # примеры к объяснениям вопросов: ключ = начало текста вопроса, значение = (код, ввод[, вывод])
USED = set()
FILESETS = {}


def _fd(f):
    return FILESETS[f] if isinstance(f, str) else f

# скрытый «хвост» задач на функции: проверка вызывает функцию кодом из теста (тест = вызов, который читается из stdin)
TL = "exec(__import__('sys').stdin.read(), globals())"

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


# ---------- код с numpy / pandas / matplotlib: вывод берём у настоящего движка курса ----------
# Обычный CPython сборки даёт другой вывод (numpy на wasm32 считает целые как int32, версии pandas отличаются),
# поэтому такие программы запускаются в Pyodide из уже собранного out5.html. Результаты лежат в pyo_cache.json,
# чтобы пересборка была быстрой и повторяемой. Пакеты Pyodide берутся из PYODIDE_PKGS (tests/h.py).
PYO_RE = re.compile(r'^\s*(import|from)\s+(numpy|pandas|matplotlib|bs4|PIL)\b', re.M)
_PYO = {}


def _pyo_run(code, lines, files):
    cf = 'pyo_cache.json'
    if 'cache' not in _PYO:
        _PYO['cache'] = json.load(open(cf, encoding='utf-8')) if os.path.exists(cf) else {}
    key = hashlib.sha1(json.dumps([code, lines, files or {}], ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    c = _PYO['cache']
    if key not in c:
        if 'pg' not in _PYO:
            sys.path.insert(0, os.path.abspath('tests'))
            from h import open_page
            from playwright.sync_api import sync_playwright
            pw = sync_playwright().start()
            b, ctx, pg, logs = open_page(pw, os.path.abspath('out5.html'))
            pg.evaluate('skReady()')
            _PYO.update(pw=pw, b=b, pg=pg)
        r = _PYO['pg'].evaluate('async (a)=>{const r=await exec(a[0],{lines:a[1],files:a[2]});return [r.out,r.err]}', [code, lines, files or {}])
        assert not r[1], ('ошибка в Pyodide', code, r[1])
        c[key] = r[0]
        json.dump(c, open(cf, 'w', encoding='utf-8'), ensure_ascii=False, indent=0, sort_keys=True)
    return c[key]


def run(code, lines=None, files=None):
    """возвращает (plain, transcript_html)"""
    import tempfile
    lines = lines or []
    if PYO_RE.search(code):
        plain = _pyo_run(code, lines, files)
        return plain, esc(plain)
    d = tempfile.mkdtemp()
    for k, v in (files or {}).items():
        os.makedirs(os.path.dirname(d + '/' + k), exist_ok=True)  # файлы задачи могут лежать в папках: «Загрузки/фото.jpg»
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


ER = []   # примеры с намеренной ошибкой: tests/xc5.py сверяет вывод и текст ошибки с движком приложения


def exerr(code):
    """Пример с ошибкой: код и то, что увидит ученик (вывод до ошибки + текст ошибки), как в приложении.
    Запускается настоящим Python как файл main.py (так называется программа ученика в приложении)."""
    import tempfile
    code = code.strip('\n')
    d = tempfile.mkdtemp()
    open(d + '/main.py', 'w', encoding='utf-8').write(code + '\n')
    r = subprocess.run([PY, 'main.py'], capture_output=True, text=True, timeout=15, cwd=d,
                       env=dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1'))
    assert r.returncode != 0, ('пример должен падать с ошибкой', code)
    err = re.sub(r'File "[^"]*main\.py"', 'File "main.py"', r.stderr.rstrip('\n'))  # в приложении путь просто main.py
    ER.append(dict(code=code, out=r.stdout, err=err))
    shown = (r.stdout + err).rstrip('\n')
    return '<pre>' + code + '</pre><pre class="out oerr">' + esc(shown) + '</pre>'


def ex(code, lines=None, files=None):
    code = code.strip('\n')
    plain, tr = run(code, lines, files)
    EX.append(dict(code=code, lines=lines or [], out=plain, files=files))
    cls = 'out con' if lines else 'out'
    return '<pre>' + code + '</pre><pre class="' + cls + '">' + tr.rstrip('\n') + '</pre>'


def run_tu(code, lines=None):
    """запуск с модулем turtle из v5/py/turtle_shim.py: (plain, transcript_html, json_рисунка)"""
    import tempfile, shutil
    lines = lines or []
    d = tempfile.mkdtemp()
    shutil.copy('v5/py/turtle_shim.py', d + '/turtle.py')
    prog = WRAP % (lines, code) + "\nimport turtle as _t\nopen('__dump.json', 'w', encoding='utf-8').write(_t._dump() or '')\n"
    r = subprocess.run([PY, '-c', prog], capture_output=True, text=True, timeout=20, cwd=d)
    assert r.returncode == 0, (code, r.stderr)
    raw = r.stdout
    plain = re.sub(r'\x03.*?\x04', '', raw)
    plain = re.sub(r'\x01.*?\x02\n', '', plain)
    tr = esc(raw)
    tr = re.sub(r'\x03(.*?)\x04', r'\1', tr)
    tr = re.sub(r'\x01(.*?)\x02', r'<span class="ty">\1</span>', tr)
    dump = open(d + '/__dump.json', encoding='utf-8').read()
    assert dump, ('программа ничего не нарисовала', code)
    return plain, tr, dump


def tu(code, lines=None):
    """пример с черепахой: код, вывод (если есть) и готовый рисунок под ним (рисуется в приложении на холсте)"""
    code = code.strip('\n')
    plain, tr, dump = run_tu(code, lines)
    EX.append(dict(code=code, lines=lines or [], out=plain))
    h = '<pre>' + code + '</pre>'
    if plain.strip():
        h += '<pre class="out' + (' con' if lines else '') + '">' + tr.rstrip('\n') + '</pre>'
    return h + '<div class="tuf" data-td="' + html.escape(dump, quote=True).replace('[', '&#91;') + '"></div>'


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


def q(text, right, wrongs, e, c=None, bad=False):
    """bad=True: код c намеренно с ошибкой (coverage_check его не проверяет)"""
    opts, pos = _opts(text, c, right, wrongs)
    d = {'q': text}
    if c:
        d['c'] = c.strip('\n')
    if bad:
        d['cb'] = 1
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
    # примеры в описаниях терминов: «Пример:\nкод\nВывод:\nтекст» — запускаем код и сверяем, что текст начинается с настоящего вывода
    for tn, td in terms:
        m = re.search(r'Пример:\n([\s\S]*?)\nВывод:\n([\s\S]*)$', td)
        if m and 'input(' not in m.group(1):
            plain, _ = run(m.group(1))
            out = _norm_out(plain, False)
            shown = _norm_out(m.group(2), False)
            assert shown.startswith(out), ('вывод в примере термина не совпадает', tn, out, m.group(2)[:120])
            # в основном курсе после вывода ничего постороннего («Частая ошибка: …» — в тексте термина выше примера)
            if not os.path.basename(sys._getframe(1).f_code.co_filename).startswith('c_h_'):
                if os.environ.get('KCOLLECT') and shown != out:
                    print('TAIL', tn, '|', shown[len(out):].strip().replace('\n', ' / ')[:150])
                    continue
                assert shown == out, ('после вывода в примере термина лишний текст — перенеси его выше «Пример:»', tn, shown[len(out):][:120])
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


def _exfmt(inputs, out, tail=False):
    if tail:
        return 'Проверка запустит:\n' + inputs + '\nВывод:\n' + out
    li = _inp(inputs)
    if len(li) <= 1 and '\n' not in out:
        return ('Вход: ' + inputs + '\n' if inputs else '') + 'Вывод: ' + out
    return ('Вход:\n' + '\n'.join(li) + '\n' if li else '') + 'Вывод:\n' + out


def _tests(sol, inputs, exp, where, files=None, tail=None):
    tests = []
    full = sol + '\n' + tail if tail else sol
    for inp in inputs:
        plain, _ = run(full, _inp(inp), files)
        out = _norm_out(plain, False)
        if exp and inp in exp:
            assert out == exp[inp], (where, inp, out, exp[inp])
        tests.append([inp, out])
    return tests


def task(q_, h, sol, inputs, strict=False, exp=None, ex_=None, files=None, tail=None, starter=None, fix=False):
    """fix=True: задача «исправь ошибку», шаблон starter намеренно с ошибками (coverage_check его не проверяет)"""
    sol = sol.strip('\n')
    tests = _tests(sol, inputs, exp, q_, _fd(files), tail)
    TK.append(dict(where=q_, sol=sol, tests=tests, strict=strict, files=_fd(files), tail=tail))
    d = {'q': q_, 'ex': ex_ if ex_ is not None else _exfmt(inputs[0], tests[0][1], bool(tail)), 'h': h, 'tests': tests, 'sol': sol}
    if fix:
        assert starter, 'у задачи «исправь ошибку» нужен шаблон с ошибками'
        d['fix'] = 1
    if strict:
        d['strict'] = 1
    if files:
        d['f'] = files
    if tail:
        d['tail'] = tail
    if starter:
        d['starter'] = starter.strip('\n') + '\n'
    return d


def ts(name, tasks):
    assert 1 <= len(tasks) <= 99
    return {'t': 'test', 'n': name, 'tasks': tasks}


def pj(name, q_, h, sol, inputs, strict=False, exp=None, bonus=None, ex_=None, files=None, tail=None, starter=None):
    sol = sol.strip('\n')
    tests = _tests(sol, inputs, exp, name, _fd(files), tail)
    TK.append(dict(where=name, sol=sol, tests=tests, strict=strict, files=_fd(files), tail=tail))
    d = {'t': 'project', 'n': name, 'q': q_, 'h': h, 'ex': ex_ if ex_ is not None else _exfmt(inputs[0], tests[0][1], bool(tail)), 'tests': tests}
    if bonus:
        d['bonus'] = bonus
    d['sol'] = sol
    if strict:
        d['strict'] = 1
    if files:
        d['f'] = files
    if tail:
        d['tail'] = tail
    if starter:
        d['starter'] = starter.strip('\n') + '\n'
    return d


# opt — доп. глава (кроличья нора); after — номер островка темы перед ней (с 0), после которого глава открывается и рядом с которым стоит нора
def topic(n, s, items, intro=False, opt=False, after=None):
    d = {'n': n, 's': s}
    if intro:
        d['intro'] = 1
    if opt:
        d['opt'] = 1
    if after is not None:
        d['after'] = after
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
