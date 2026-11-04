import re
from dsl import th, fl

def split_pair(T, ti, ith, groups, names, qsel=None, extra=None):
    """T: список тем; ti: индекс темы; ith: индекс теории в items (за ней идёт flash).
    groups: список списков номеров h3-секций; names: имена теорий; qcounts: кол-во вопросов по частям"""
    items = T[ti]['items']
    t, f = items[ith], items[ith + 1]
    assert t['t'] == 'theory' and f['t'] == 'flash'
    parts = re.split(r'(?=<h3>)', t['html'])
    intro, secs = parts[0], parts[1:]
    assert sorted(sum(groups, [])) == list(range(len(secs))), (t['n'], len(secs))
    terms = [(x['n'], x['d']) for x in t.get('terms', [])]
    newth, newfl = [], []
    qs = f['q']
    if qsel is None:
        n = len(groups); base, rest = divmod(len(qs), n); qsel = []; p0 = 0
        for i in range(n):
            c = base + (1 if i < rest else 0); qsel.append(list(range(p0, p0 + c))); p0 += c
    assert sorted(sum(qsel, [])) == list(range(len(qs))), (t['n'], qsel, len(qs))
    for gi, g in enumerate(groups):
        body = (intro if gi == 0 else '') + ''.join(secs[k] for k in g)
        used = set(re.findall(r'\[\[([^\]|]+)', re.sub(r'<pre[^>]*>[\s\S]*?</pre>', '', body)))
        tl = [x for x in terms if x[0] in used]
        if gi == 0:
            tl += [x for x in terms if x[0] not in used and not any(x[0] in re.findall(r'\[\[([^\]|]+)', re.sub(r'<pre[^>]*>[\s\S]*?</pre>', '', ''.join(secs))) for _ in [0])]
        d = {'t': 'theory', 'n': names[gi]}
        if tl:
            d['terms'] = [{'n': a, 'd': b} for a, b in tl]
        d['html'] = body
        newth.append(d)
        newfl.append({'t': 'flash', 'n': f['n'] + (' (%d)' % (gi + 1) if len(groups) > 1 else ''), 'q': [qs[k] for k in qsel[gi]] + list((extra or {}).get(gi, []))})
    out = []
    for a, b in zip(newth, newfl):
        out += [a, b]
    items[ith:ith + 2] = out

def show(T, ti):
    for x in T[ti]['items']:
        if x['t'] == 'flash':
            print('FL', x['n'])
            for q in x['q']:
                print('   ', q['q'][:50], '|', (q.get('c') or '').replace('\n', ' / ')[:90])
        elif x['t'] == 'theory':
            print('TH', x['n'], re.findall(r'<h3>(.*?)</h3>', x['html']))
