"""Проверка курса после build.py: структура данных и правило «всё, что используется, введено раньше».
Запуск из корня репозитория после сборки: py tests/coverage_check.py
Читает topics.json (его пишет build.py) и curriculum.json. Любое нарушение — код выхода 1.

Что считается введённым к моменту островка:
- всё из curriculum.json у предыдущих тем основного пути (для норы — до темы after включительно);
- в текущей теме — то, что уже описано в terms её теорий выше по порядку (теория может использовать свои terms).
Функции и методы сверяются по последней части имени (math.sqrt → sqrt), конструкции — по ключам ниже.
Имена, которые код определяет сам (переменные, def, class, параметры, import as), не проверяются."""
import ast, builtins, html, io, json, re, subprocess, sys, os, tokenize

sys.path.insert(0, os.getcwd())
CUR = json.load(open('curriculum.json', encoding='utf-8'))
DATA = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'topics.json', encoding='utf-8'))
TOPICS, FILESETS = DATA['topics'], DATA['filesets']
TL = "exec(__import__('sys').stdin.read(), globals())"   # скрытый хвост задач на функции (dsl.TL)

# конструкция → названия терминов, которые её объясняют (термин обязателен в теме, которая её вводит)
KTERM = {
    'if': ['if'], 'elif': ['elif'], 'else': ['else'], 'while': ['while'], 'for': ['for'], 'break': ['break'],
    'continue': ['continue'], 'def': ['def'], 'return': ['return'], 'None': ['None'], 'global': ['global'],
    'nonlocal': ['nonlocal'], 'lambda': ['lambda'], 'try': ['try'], 'except': ['except'], 'finally': ['finally'],
    'raise': ['raise'], 'assert': ['assert'], 'with': ['with'], 'class': ['class'], 'yield': ['yield'],
    'yield from': ['yield from'], 'import': ['import'], 'from-import': ['from'], 'import-as': ['as'],
    'match': ['match'], 'is': ['is'], 'in': ['in'], 'not': ['not'], 'and/or': ['and', 'or'], 'del': ['del'],
    'f-string': ['f-строка'], 'slice': ['срез'], 'listcomp': ['списочное выражение'],
    'dictcomp': ['словарное выражение'], 'setcomp': ['множественное выражение'], 'genexp': ['выражение-генератор'],
    'ternary': ['условное выражение'], 'for-else': ['else у цикла'], '//': ['//'], '%': ['%'], '**': ['**'],
    '+=': ['+='], 'comment': ['#'], '*args': ['*args'], '**kwargs': ['**kwargs'], 'annotation': ['подсказка типа'],
    'decorator-use': ['декоратор'], 'format-spec': ['формат в f-строке'],
}
OPS = {ast.FloorDiv: '//', ast.Mod: '%', ast.Pow: '**'}


def norm(name):
    return re.sub(r'\(.*\)$', '', name.strip()).split('.')[-1].strip()


# ---------- что использует код ----------
def scan(code):
    """→ (функции и методы, конструкции, модули, ошибки) или None, если код не разбирается"""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None
    own, mods, calls, ks, errs, imported = set(), set(), set(), set(), set(), set()
    for n in ast.walk(tree):                                  # что код определяет сам
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            own.add(n.name)
        elif isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
            own.add(n.id)
        elif isinstance(n, ast.arg):
            own.add(n.arg)
        elif isinstance(n, (ast.Import, ast.ImportFrom)):
            for a in n.names:
                if isinstance(n, ast.Import):
                    mods.add(a.name)
                own.add(a.asname or a.name.split('.')[0])
            if isinstance(n, ast.ImportFrom) and n.module:
                mods.add(n.module)
                imported |= {a.name for a in n.names if a.name != '*'}   # from math import sqrt → проверяем sqrt
        elif isinstance(n, ast.ExceptHandler) and n.name:
            own.add(n.name)
    modnames = {m.split('.')[0] for m in mods}
    for n in ast.walk(tree):
        t = type(n)
        if t is ast.Call:
            f = n.func
            if isinstance(f, ast.Name) and f.id not in own:
                calls.add(f.id)
            elif isinstance(f, ast.Attribute) and f.attr not in own:
                calls.add(f.attr)
        elif t is ast.Name and isinstance(n.ctx, ast.Load) and n.id not in own and n.id not in ('True', 'False', 'None'):
            if callable(getattr(builtins, n.id, None)) and not (isinstance(getattr(builtins, n.id), type) and issubclass(getattr(builtins, n.id), BaseException)):
                calls.add(n.id)
            elif isinstance(getattr(builtins, n.id, None), type):
                errs.add(n.id)                                 # встроенные исключения: ValueError и т.д.
        elif t is ast.Attribute and isinstance(n.value, ast.Name) and n.value.id in modnames:
            calls.add(n.attr)                                  # math.pi, sys.stdin
        elif t in (ast.FunctionDef, ast.AsyncFunctionDef):
            ks.add('def')
            if n.name.startswith('__') and n.name.endswith('__'):
                calls.add(n.name)                              # магические методы вводятся как термины
            if n.decorator_list:
                ks.add('decorator-use')
            if n.args.vararg:
                ks.add('*args')
            if n.args.kwarg:
                ks.add('**kwargs')
            if n.returns or any(a.annotation for a in n.args.args):
                ks.add('annotation')
            if any(isinstance(b, (ast.FunctionDef, ast.AsyncFunctionDef)) for b in ast.walk(n) if b is not n):
                ks.add('nested-def')
        elif t in (ast.For, ast.While):
            ks.add('for' if t is ast.For else 'while')
            if n.orelse:
                ks.add('for-else')
        elif t is ast.If:
            ks.add('if')
        elif t is ast.BinOp and type(n.op) in OPS:
            ks.add(OPS[type(n.op)])
        elif t is ast.AugAssign:
            ks.add('+=')
        elif t is ast.Compare:
            for op in n.ops:
                if isinstance(op, (ast.In, ast.NotIn)):
                    ks.add('in')
                if isinstance(op, (ast.Is, ast.IsNot)):
                    ks.add('is')
        elif t is ast.BoolOp:
            ks.add('and/or')
        elif t is ast.UnaryOp and isinstance(n.op, ast.Not):
            ks.add('not')
        elif t is ast.ImportFrom:
            ks.add('from-import')
        elif t is ast.Import:
            ks.add('import')
            if any(a.asname for a in n.names):
                ks.add('import-as')
        elif t is ast.Return and n.value is not None:
            ks.add('return')
        elif t is ast.JoinedStr:
            ks.add('f-string')
            if any(isinstance(v, ast.FormattedValue) and v.format_spec for v in n.values):
                ks.add('format-spec')
        elif t is ast.Constant and n.value is None:
            ks.add('None')
        else:
            simple = {ast.With: 'with', ast.Lambda: 'lambda', ast.Try: 'try', ast.Raise: 'raise', ast.ClassDef: 'class',
                      ast.Yield: 'yield', ast.YieldFrom: 'yield from', ast.Global: 'global', ast.Nonlocal: 'nonlocal',
                      ast.ListComp: 'listcomp', ast.DictComp: 'dictcomp', ast.SetComp: 'setcomp', ast.GeneratorExp: 'genexp',
                      ast.Slice: 'slice', ast.NamedExpr: ':=', ast.Match: 'match', ast.Assert: 'assert', ast.Break: 'break',
                      ast.Continue: 'continue', ast.IfExp: 'ternary', ast.Delete: 'del', ast.AsyncFunctionDef: 'async def',
                      ast.Await: 'await', ast.List: 'list-literal', ast.Dict: 'dict-literal', ast.Set: 'set-literal'}
            if t in simple:
                ks.add(simple[t])
        if t is ast.ExceptHandler:
            ks.add('except')
            for e in ast.walk(n.type) if n.type else []:
                if isinstance(e, ast.Name) and e.id not in own:
                    errs.add(e.id)
        if t is ast.Try and n.finalbody:
            ks.add('finally')
    try:
        if any(tok.type == tokenize.COMMENT for tok in tokenize.generate_tokens(io.StringIO(code).readline)):
            ks.add('comment')
    except (tokenize.TokenError, IndentationError):
        pass
    return calls | imported, ks, mods, errs


def pre_codes(h):
    """код примеров из html теории: <pre> без класса; пример с намеренной ошибкой (exerr, за ним pre.oerr) пропускается"""
    return [html.unescape(m.group(1)) for m in re.finditer(r'<pre>([\s\S]*?)</pre>(?!\s*<pre class="out oerr">)', h)]


# ---------- реестр ----------
def intro_sets(entry):
    i = entry.get('introduces', {})
    fm = {norm(x) for x in i.get('f', []) + i.get('m', [])}
    return fm, set(i.get('k', [])), {m for m in i.get('mod', [])}, set(i.get('err', []))


ERR = []


def err(where, msg):
    ERR.append(f'{where}: {msg}')


def main():
    cur_main, cur_holes = CUR['topics'], {h['n']: h for h in CUR['holes']}
    by_name = {t['n']: (k, t) for k, t in enumerate(cur_main)}
    main_seen = []
    acc = {}                                   # id темы → (fm, k, mod, err) накопленное до неё включительно
    tot_fm, tot_k, tot_mod, tot_err = set(), set(), set(), set()
    for t in cur_main:
        fm, k, mod, er = intro_sets(t)
        tot_fm |= fm; tot_k |= k; tot_mod |= mod; tot_err |= er
        acc[t['id']] = (set(tot_fm), set(tot_k), set(tot_mod), set(tot_err))
    prev = {}                                  # id → накопленное ДО темы
    p = (set(), set(), set(), set())
    for t in cur_main:
        prev[t['id']] = p
        p = acc[t['id']]
    all_fm = set().union(*(intro_sets(e)[0] for e in cur_main + CUR['holes']))
    all_k = set().union(*(intro_sets(e)[1] for e in cur_main + CUR['holes']))

    for ti, T in enumerate(TOPICS):
        where_t = f'тема «{T.get("n")}»'
        if not T.get('n') or not T.get('s'):
            err(where_t, 'нет n или s')
        if T.get('opt'):
            ent = cur_holes.get(T['n'])
            if not ent:
                err(where_t, 'нора не найдена в curriculum.json (holes)')
                continue
            base = acc[ent['after']]
        else:
            if T['n'] not in by_name:
                err(where_t, 'тема не найдена в curriculum.json')
                continue
            k, ent = by_name[T['n']]
            main_seen.append(k)
            if T['s'] != ent['s']:
                err(where_t, f'подзаголовок s не совпадает с curriculum.json: «{ent["s"]}»')
            if bool(T.get('intro')) != bool(ent.get('intro')):
                err(where_t, 'признак intro не совпадает с curriculum.json')
            if T.get('intro') and [i['t'] for i in T['items']] != ['theory']:
                err(where_t, 'тема-знакомство должна состоять из одного островка теории')
            base = prev[ent['id']]
        own_fm, own_k, own_mod, own_err = intro_sets(ent)
        b_fm, b_k, b_mod, b_err = base
        terms_here = set()                     # нормализованные имена терминов теорий выше по порядку
        theories = []
        for ii, it in enumerate(T['items']):
            ty = it.get('t')
            where = f'{where_t}, островок {ii + 1} «{it.get("n")}»'
            if not it.get('n'):
                err(where, 'нет названия')
            if ty == 'theory':
                if re.fullmatch(r'\s*теория\s*', it.get('n', ''), re.I):
                    err(where, 'название теории не должно быть просто «Теория»')
                names = [x['n'] for x in it.get('terms', [])]
                terms_here |= {norm(x) for x in names}
                theories.append(it.get('n'))
                codes = [('пример', c) for c in pre_codes(it.get('html', ''))]
                for x in it.get('terms', []):
                    if not x.get('d'):
                        err(where, f'пустое описание термина {x["n"]}')
                    for m in re.finditer(r'Пример:\n([\s\S]*?)(?:\nВывод:|$)', x.get('d', '')):
                        codes.append((f'термин {x["n"]}', m.group(1)))
            elif ty == 'flash':
                if it.get('n') not in theories:
                    err(where, 'название вопросов должно совпадать с названием теории выше в этой теме')
                qs = it.get('q', [])
                if not 1 <= len(qs) <= 30:
                    err(where, f'вопросов {len(qs)}, нужно 1–30')
                codes = []
                for qi, q in enumerate(qs):
                    o = q.get('o', [])
                    if not isinstance(q.get('a'), int) or not 0 <= q['a'] < len(o):
                        err(where, f'вопрос {qi + 1}: a вне вариантов')
                    if not 3 <= len(o) <= 4:
                        err(where, f'вопрос {qi + 1}: вариантов {len(o)}, нужно 3–4')
                    if len(set(o)) != len(o):
                        err(where, f'вопрос {qi + 1}: повторяются варианты')
                    if any(len(v) > 60 for v in o):
                        err(where, f'вопрос {qi + 1}: вариант длиннее 60 знаков')
                    if not q.get('e'):
                        err(where, f'вопрос {qi + 1}: нет пояснения e')
                    for key in ('c', 'x'):
                        if q.get(key) and not (key == 'c' and q.get('cb')):
                            codes.append((f'вопрос {qi + 1}', q[key]))
            elif ty in ('test', 'project'):
                if ty == 'test' and it.get('n') not in theories and it.get('n') != 'Задачи: испытание':
                    err(where, 'островок «Код» называется как теория выше, к которой он относится, или «Задачи: испытание»')
                if ty == 'project' and re.match(r'\s*(мини-)?проект', it.get('n', ''), re.I):
                    err(where, 'проект называется тем, что строим, без слова «проект»')
                tasks = it['tasks'] if ty == 'test' else [it]
                codes = []
                for ki, tk in enumerate(tasks):
                    wk = f'задача {ki + 1}' if ty == 'test' else 'проект'
                    for key in ('q', 'h', 'sol'):
                        if not tk.get(key):
                            err(where, f'{wk}: нет поля {key}')
                    if not tk.get('tests'):
                        err(where, f'{wk}: нет тестов')
                    zzz(where + ', ' + wk, tk)
                    full = tk['sol'] + ('\n' + tk['tail'] if tk.get('tail') and tk['tail'] != TL else '')
                    if scan(full) is None:
                        err(where, f'{wk}: эталон не разбирается Python')
                    codes.append((wk, full))
                    if tk.get('starter') and not tk.get('fix'):
                        codes.append((wk + ', шаблон', tk['starter']))
            else:
                err(where, f'неизвестный тип островка {ty}')
                continue
            # правило «введено раньше»
            ok_fm = b_fm | (own_fm & terms_here)
            ok_k = b_k | {k for k in own_k if k not in KTERM or any(norm(a) in terms_here for a in KTERM[k])}
            ok_mod, ok_err = b_mod | own_mod, b_err | (own_err & terms_here)
            for label, code in codes:
                r = scan(code)
                if r is None:
                    continue                           # пример с намеренной синтаксической ошибкой
                calls, ks, mods, errs = r
                for x in sorted(calls - ok_fm):
                    err(where, f'{label}: «{x}» ещё не введено' + ('' if x in all_fm else ' (нет в curriculum.json)'))
                for x in sorted(ks - ok_k):
                    if x in all_k or x in KTERM or x in (':=', 'async def', 'await'):
                        err(where, f'{label}: конструкция «{x}» ещё не введена' + ('' if x in all_k else ' (нет в curriculum.json)'))
                for x in sorted({m.split('.')[0] for m in mods} - {m.split('.')[0] for m in ok_mod}):
                    err(where, f'{label}: модуль «{x}» ещё не введён')
                for x in sorted(errs - ok_err):
                    err(where, f'{label}: ошибка «{x}» ещё не введена')
        # правило владельца: у каждой теории свои вопросы; островок «Код» (минимум 3 задачи) идёт после каждой теории
        # или после пары теорий (тогда задачи сочетают обе) и называется по последней теории перед ним
        if not T.get('intro'):
            for name in theories:
                if not any(i.get('t') == 'flash' and i.get('n') == name for i in T['items']):
                    err(where_t, f'у теории «{name}» нет островка вопросов с тем же названием')
            pending = []
            for it in T['items']:
                if it.get('t') == 'theory':
                    pending.append(it.get('n'))
                elif it.get('t') == 'test' and it.get('n') != 'Задачи: испытание':
                    if len(it.get('tasks', [])) < 3:
                        err(where_t, f'в островке «Код» «{it.get("n")}» меньше трёх задач')
                    if pending and it.get('n') != pending[-1]:
                        err(where_t, f'островок «Код» «{it.get("n")}» должен называться по последней теории перед ним: «{pending[-1]}»')
                    if len(pending) > 2:
                        err(where_t, f'перед островком «Код» «{it.get("n")}» больше двух теорий без своих задач')
                    pending = []
                if len(pending) > 2:
                    err(where_t, f'теории {pending[:-1]} остались без островка «Код»')
                    pending = pending[-1:]
            if pending:
                err(where_t, f'после теорий {pending} нет островка «Код»')
        # каждый вводимый в теме объект описан термином
        need = set(own_fm) | own_err | {m.split('.')[0] for m in own_mod}
        for k in own_k:
            if k in KTERM and not any(norm(a) in terms_here for a in KTERM[k]):
                err(where_t, f'нет термина для конструкции «{k}» (ожидается {" / ".join(KTERM[k])})')
        for x in sorted(need - terms_here):
            err(where_t, f'нет термина для «{x}», хотя тема его вводит')
    if main_seen != sorted(main_seen):
        err('порядок', 'основные темы идут не в порядке curriculum.json')


def zzz(where, tk):
    """пустая программа и print("zzz") не должны проходить ни одного теста"""
    tail = tk.get('tail')
    for inp, out in tk.get('tests', []):
        for fake in ('', 'print("zzz")'):
            if not tail:
                got = 'zzz' if fake else ''
            else:
                got = run(fake + '\n' + tail, inp, tk.get('f'))
            if got.strip() == out.strip():
                err(where, f'тест {inp!r} проходит программа {fake or "(пустая)"}')
                return


def run(code, inp, files):
    import dsl, tempfile
    fs = FILESETS.get(files) if isinstance(files, str) else files
    d = tempfile.mkdtemp()
    for k, v in (fs or {}).items():
        open(os.path.join(d, k), 'w', encoding='utf-8', newline='').write(v)
    lines = inp.split('\n') if inp else []
    r = subprocess.run([sys.executable, '-c', dsl.WRAP % (lines, code)], capture_output=True, text=True, timeout=15, cwd=d)
    out = re.sub(r'\x03.*?\x04', '', r.stdout)
    return re.sub(r'\x01.*?\x02\n', '', out) if r.returncode == 0 else '\x00ошибка'


if __name__ == '__main__':
    main()
    print('тем', len(TOPICS), 'нарушений', len(ERR))
    for x in ERR:
        print(' -', x)
    sys.exit(1 if ERR else 0)
