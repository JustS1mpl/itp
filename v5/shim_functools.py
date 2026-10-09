def reduce(function, iterable, *initial):
    it = iter(iterable)
    if initial:
        v = initial[0]
    else:
        try:
            v = next(it)
        except StopIteration:
            raise TypeError('reduce() of empty iterable with no initial value')
    for x in it:
        v = function(v, x)
    return v

class partial:
    def __init__(self, func, *args, **kw):
        self.func = func
        self.args = args
        self.keywords = kw

    def __call__(self, *a, **k):
        kw = dict(self.keywords)
        kw.update(k)
        return self.func(*(self.args + a), **kw)

def wraps(wrapped, assigned=None, updated=None):
    def deco(f):
        return f
    return deco

def lru_cache(maxsize=128, typed=False):
    def deco(f):
        cache = {}
        def w(*a):
            if a not in cache:
                cache[a] = f(*a)
            return cache[a]
        return w
    if callable(maxsize):
        return deco(maxsize)
    return deco

def cache(f):
    return lru_cache()(f)

def cmp_to_key(mycmp):
    class K:
        def __init__(self, obj):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
    return K
