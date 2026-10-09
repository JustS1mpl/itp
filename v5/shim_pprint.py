def _r(o, sd):
    if isinstance(o, dict):
        ks = sorted(o.keys()) if sd else list(o.keys())
        return '{' + ', '.join([_r(k, sd) + ': ' + _r(o[k], sd) for k in ks]) + '}'
    if isinstance(o, list):
        return '[' + ', '.join([_r(v, sd) for v in o]) + ']'
    if isinstance(o, tuple):
        if len(o) == 1:
            return '(' + _r(o[0], sd) + ',)'
        return '(' + ', '.join([_r(v, sd) for v in o]) + ')'
    if isinstance(o, (set, frozenset)):
        if not o:
            return 'set()'
        return '{' + ', '.join([_r(v, sd) for v in sorted(o)]) + '}'
    return repr(o)

def _f(o, ind, w, col, sd):
    r = _r(o, sd)
    if len(r) + col <= w:
        return r
    pad = ',\n' + ' ' * (col + ind)
    if isinstance(o, dict):
        ks = sorted(o.keys()) if sd else list(o.keys())
        parts = []
        for k in ks:
            kr = _r(k, sd)
            parts.append(kr + ': ' + _f(o[k], ind, w, col + ind + len(kr) + 2, sd))
        return '{' + ' ' * (ind - 1) + pad.join(parts) + '}'
    if isinstance(o, list):
        return '[' + ' ' * (ind - 1) + pad.join([_f(v, ind, w, col + ind, sd) for v in o]) + ']'
    if isinstance(o, tuple):
        return '(' + ' ' * (ind - 1) + pad.join([_f(v, ind, w, col + ind, sd) for v in o]) + (',)' if len(o) == 1 else ')')
    if isinstance(o, (set, frozenset)):
        return '{' + ' ' * (ind - 1) + pad.join([_f(v, ind, w, col + ind, sd) for v in sorted(o)]) + '}'
    return r

def pformat(obj, indent=1, width=80, depth=None, compact=False, sort_dicts=True):
    return _f(obj, indent, width, 0, sort_dicts)

def pprint(obj, stream=None, indent=1, width=80, depth=None, compact=False, sort_dicts=True):
    s = pformat(obj, indent, width, depth, compact, sort_dicts)
    if stream is None:
        print(s)
    else:
        stream.write(s + '\n')

PrettyPrinter = None
