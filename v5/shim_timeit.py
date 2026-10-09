import time

from itpshim import eval_ as eval

def _ident(x):
    return x != '' and not x[0].isdigit() and all([c.isalnum() or c == '_' for c in x])

def _mk(stmt, setup, g):
    if callable(stmt):
        return stmt
    import sys
    gg = g if g is not None else sys.modules['__main__'].__dict__
    def run():
        s = stmt.strip()
        i = s.find('=')
        if i > 0 and _ident(s[:i].strip()) and s[i + 1:i + 2] != '=':
            s = s[i + 1:]
        eval(s, gg)
    return run

def timeit(stmt='pass', setup='pass', timer=None, number=1000000, globals=None):
    f = _mk(stmt, setup, globals)
    t = time.time()
    for _ in range(number):
        f()
    return time.time() - t

def repeat(stmt='pass', setup='pass', timer=None, repeat=5, number=1000000, globals=None):
    return [timeit(stmt, setup, timer, number, globals) for _ in range(repeat)]
