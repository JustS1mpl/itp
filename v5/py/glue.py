import sys, builtins, traceback, linecache, os, types, random, hashlib, time, io
import importlib.abc, importlib.util

# ---- поправки под 64-битный CPython (в браузере сборка 32-битная) ----
sys.maxsize = 2 ** 63 - 1
_gs0 = sys.getsizeof


def _dict_size(o, w):
    if not o and w == 40:
        return 64
    k32 = w - 40
    uni = all(type(k) is str for k in o)
    for kk in range(3, 31):
        ib = 1 if kk <= 7 else 2 if kk <= 15 else 4 if kk <= 31 else 8
        idx = (1 << kk) * ib
        use = ((1 << kk) * 2) // 3
        for u in ((True, False) if uni else (False, True)):
            if 20 + idx + use * (8 if u else 12) == k32:
                return 64 + 32 + idx + use * (16 if u else 24)
    return 2 * w


def _getsizeof(o, *default):
    try:
        w = _gs0(o)
    except TypeError:
        if default:
            return default[0]
        raise
    t = type(o)
    if t is int or t is bool:
        return 24 + 4 * max(1, (abs(o).bit_length() + 29) // 30)
    if t is str:
        if o.isascii():
            return 41 + len(o)
        m = max(o)
        kind = 1 if ord(m) < 256 else 2 if ord(m) < 65536 else 4
        return 56 + (len(o) + 1) * kind
    if t is float:
        return 24
    if t is complex:
        return 32
    if t is bytes:
        return 33 + len(o)
    if t is bytearray:
        return 56 + (w - 28)
    if t is list:
        return 56 + 2 * (w - 28)
    if t is dict:
        return _dict_size(o, w)
    if t is types.GeneratorType or t is types.CoroutineType:
        return 2 * w - 8
    if t is memoryview:
        return 2 * w - 8
    return 2 * w


sys.getsizeof = _getsizeof

_EMAP = {44: 2, 20: 17, 2: 13, 31: 21, 54: 20, 63: 1, 55: 39, 28: 22, 8: 9}
_ECLS = {2: FileNotFoundError, 17: FileExistsError, 13: PermissionError, 21: IsADirectoryError, 20: NotADirectoryError, 1: PermissionError, 39: OSError, 22: OSError, 9: OSError}


def _fixos(e):
    n = getattr(e, 'errno', None)
    if n in _EMAP and type(e).__module__ == 'builtins' and not getattr(e, '_itp', False):
        ln = _EMAP[n]
        a = [ln, e.strerror, e.filename]
        if e.filename2 is not None:
            a += [None, e.filename2]
        ne = _ECLS[ln](*a)
        ne._itp = True
        return ne
    return e


import errno as _errno
_ERR0 = [getattr(_errno, _k) for _k in ('ENOENT', 'ENOTDIR', 'EBADF', 'ELOOP') if hasattr(_errno, _k)]
for _k, _v in (('ENOENT', 2), ('EEXIST', 17), ('EACCES', 13), ('EISDIR', 21), ('ENOTDIR', 20), ('EPERM', 1), ('ENOTEMPTY', 39), ('EINVAL', 22), ('EBADF', 9)):
    setattr(_errno, _k, _v)
_errno.errorcode.clear()
_errno.errorcode.update({2: 'ENOENT', 17: 'EEXIST', 13: 'EACCES', 21: 'EISDIR', 20: 'ENOTDIR', 1: 'EPERM', 39: 'ENOTEMPTY', 22: 'EINVAL', 9: 'EBADF'})
# pathlib запомнил номера ошибок до подмены: без этого Path(...).exists() для несуществующего файла падал с
# FileNotFoundError вместо False (на этом спотыкался и matplotlib)
try:
    import pathlib._abc as _pab
    _pab._IGNORED_ERRNOS = tuple(set(_ERR0) | {2, 20, 9, 40})
except Exception:
    pass


def _wrapos(f):
    def g(*a, **k):
        try:
            return f(*a, **k)
        except OSError as e:
            ne = _fixos(e)
            if ne is e:
                raise
            raise ne from None
    g.__name__ = getattr(f, '__name__', 'f')
    g.__doc__ = getattr(f, '__doc__', None)
    return g


builtins.open = io.open = _wrapos(builtins.open)
for _n in ('listdir', 'remove', 'unlink', 'mkdir', 'rmdir', 'rename', 'stat', 'makedirs', 'chdir', 'scandir', 'replace', 'lstat'):
    if hasattr(os, _n):
        setattr(os, _n, _wrapos(getattr(os, _n)))


# ---- asyncio без JSPI: обычный цикл событий, как в CPython ----
import asyncio

class _Sel:
    def select(self, timeout=None):
        t = 0.005 if timeout is None else min(timeout, 0.05)
        if t > 0:
            time.sleep(t)
        return []
    def close(self):
        pass
    def get_map(self):
        return {}

class _Loop(asyncio.BaseEventLoop):
    def __init__(self):
        super().__init__()
        self._selector = _Sel()
    def _process_events(self, event_list):
        pass
    def _write_to_self(self):
        pass
    def close(self):
        if self.is_running():
            raise RuntimeError("Cannot close a running event loop")
        super().close()
    def call_soon_threadsafe(self, callback, *args, context=None):
        return self.call_soon(callback, *args, context=context)

class _Policy(asyncio.DefaultEventLoopPolicy):
    _loop_factory = _Loop

_WL = asyncio._get_running_loop()
asyncio.set_event_loop_policy(_Policy())


# ---- hash чисел как в 64-битном CPython ----
import math as _math
_HM = (1 << 61) - 1
_hash0 = builtins.hash


def _hash_int(n):
    r = n % _HM if n >= 0 else -((-n) % _HM)
    return -2 if r == -1 else r


def _hash_float(v):
    if v != v:
        return _hash0(v)
    if v in (float('inf'), float('-inf')):
        return 314159 if v > 0 else -314159
    m, e = _math.frexp(v)
    sign = 1
    if m < 0:
        sign = -1
        m = -m
    x = 0
    while m:
        x = ((x << 28) & _HM) | (x >> (61 - 28))
        m *= 268435456.0
        e -= 28
        y = int(m)
        m -= y
        x += y
        if x >= _HM:
            x -= _HM
    e = e % 61 if e >= 0 else 61 - 1 - ((-1 - e) % 61)
    x = ((x << e) & _HM) | (x >> (61 - e))
    x *= sign
    return -2 if x == -1 else x


def hash(o):
    t = type(o)
    if t is int or t is bool:
        return _hash_int(int(o))
    if t is float:
        return _hash_float(o)
    return _hash0(o)


builtins.hash = hash
_seed0 = random.Random.seed


def _seed(self, a=None, version=2):
    if type(a) is float:
        a = abs(_hash_float(a))
    return _seed0(self, a, version)


random.Random.seed = _seed
random.seed = random._inst.seed

_BASEMODS = set(sys.modules)
_BI = dict(builtins.__dict__)
_H = os.getcwd()
_BASEFILES = set(os.listdir(_H))
_SYSK = ('stdin', 'stdout', 'stderr', 'excepthook', 'displayhook', 'argv', 'ps1', 'ps2')
_SYS0 = {k: getattr(sys, k) for k in _SYSK if hasattr(sys, k)}
_PATH0 = list(sys.path)
_RL0 = sys.getrecursionlimit()
_MAIN0 = sys.modules.get('__main__')
_urandom0 = os.urandom
_input0 = builtins.input
_mark = None  # JS-функция: _mark(длина_подсказки)
_flush = None


def _install_urandom(seed):
    state = [0]
    def urandom(n):
        out = b''
        while len(out) < n:
            state[0] += 1
            out += hashlib.sha256(('%s:%d' % (seed, state[0])).encode()).digest()
        return out[:n]
    os.urandom = urandom
    try:
        import random as _r
        _r._urandom = urandom
    except Exception:
        pass


def _marked_input(prompt=''):
    sys.stdout.flush()
    _mark(len(str(prompt)))
    return _input0(prompt)


def _clean_te(te):
    seen = set()
    def walk(t):
        if t is None or id(t) in seen:
            return
        seen.add(id(t))
        t.stack = traceback.StackSummary.from_list([f for f in t.stack if f.filename != '<itp>'])
        walk(t.__cause__)
        walk(t.__context__)
        for g in (getattr(t, 'exceptions', None) or ()):
            walk(g)
    walk(te)
    return te


def _itp_run(code, marks, seed):
    _install_urandom(seed)
    asyncio._set_running_loop(None)
    asyncio.set_event_loop(None)
    if marks:
        builtins.input = _marked_input
    mod = types.ModuleType('__main__')
    mod.__dict__.update({'__doc__': None, '__package__': None, '__loader__': None, '__spec__': None,
                         '__file__': 'main.py', '__cached__': None, '__builtins__': builtins})
    sys.modules['__main__'] = mod
    ns = mod.__dict__
    sys.argv = ['main.py']
    linecache.cache['main.py'] = (len(code), None, code.splitlines(True), 'main.py')
    res = None
    try:
        try:
            co = compile(code, 'main.py', 'exec')
        except SyntaxError as e:
            return ''.join(traceback.format_exception_only(type(e), e))
        except (ValueError, OverflowError, RecursionError, MemoryError) as e:
            return ''.join(traceback.format_exception_only(type(e), e))
        try:
            exec(co, ns)
        except SystemExit as e:
            c = e.code
            if c is not None and not isinstance(c, int):
                try:
                    sys.stderr.write(str(c) + '\n')
                except Exception:
                    pass
        except BaseException as e:
            if sys.excepthook is not _SYS0['excepthook']:
                try:
                    sys.excepthook(type(e), e, e.__traceback__.tb_next)
                except BaseException:
                    pass
            else:
                tb = e.__traceback__.tb_next if e.__traceback__ else None
                te = _clean_te(traceback.TracebackException(type(e), e, tb))
                res = ''.join(te.format())
        try:
            sys.stdout.flush()
            sys.stderr.flush()
        except Exception:
            pass
    finally:
        pass
    return res


def _itp_reset():
    try:
        for s in (sys.stdout, sys.stderr):
            try:
                s.flush()
            except Exception:
                pass
    except Exception:
        pass
    for k, v in _SYS0.items():
        try:
            setattr(sys, k, v)
        except Exception:
            pass
    sys.path[:] = _PATH0
    try:
        sys.setrecursionlimit(_RL0)
    except Exception:
        pass
    for m in list(sys.modules):
        if m not in _BASEMODS and not _itp_keep(m):
            del sys.modules[m]
    if _MAIN0 is not None:
        sys.modules['__main__'] = _MAIN0
    builtins.input = _input0
    try:
        asyncio._set_running_loop(_WL)
        asyncio.set_event_loop(None)
    except Exception:
        pass
    d = builtins.__dict__
    for k in list(d):
        if k not in _BI:
            del d[k]
    for k, v in _BI.items():
        if d.get(k) is not v:
            d[k] = v
    os.urandom = _urandom0
    try:
        os.chdir(_H)
    except Exception:
        pass
    import shutil
    for n in os.listdir(_H):
        if n not in _BASEFILES:
            p = os.path.join(_H, n)
            try:
                shutil.rmtree(p) if os.path.isdir(p) and not os.path.islink(p) else os.remove(p)
            except Exception:
                pass
    linecache.cache.pop('main.py', None)
    random.seed()

# ---- v5.4.0: модуль turtle (исходник добавляется при сборке в _TURTLE_SRC) ----
import importlib.abc, importlib.util


class _SrcLoader(importlib.abc.Loader):
    def __init__(self, name, var):
        self.name = name
        self.var = var

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        module.__file__ = '<%s>' % self.name
        exec(compile(globals()[self.var], '<%s>' % self.name, 'exec'), module.__dict__)


class _SrcFinder(importlib.abc.MetaPathFinder):
    """Свои модули ИТП, исходник которых вшит при сборке: turtle (_TURTLE_SRC), requests (_REQUESTS_SRC, учебные серверы)."""
    MODS = {'turtle': '_TURTLE_SRC', 'requests': '_REQUESTS_SRC'}

    def find_spec(self, name, path=None, target=None):
        var = self.MODS.get(name)
        if var and globals().get(var):
            return importlib.util.spec_from_loader(name, _SrcLoader(name, var))
        return None


sys.meta_path.insert(0, _SrcFinder())


# ---- v6.7.8: сторонние библиотеки (numpy, pandas, matplotlib, …) ----
# Подкачиваются с CDN Pyodide или с PyPI (micropip), когда программа их импортирует и есть интернет (worker.js).
# Загруженные пакеты лежат в site-packages и между запусками не выгружаются: модули на C (numpy) нельзя
# импортировать в одном процессе дважды, а скачивать их заново на каждый запуск долго.
_SITE = ('site-packages', 'dist-packages')


def _itp_keep(name):
    m = sys.modules.get(name)
    f = getattr(m, '__file__', None) or ''
    return any(s in f for s in _SITE)


def _itp_missing(code):
    """Модули верхнего уровня, которые программа импортирует, но которых пока нет."""
    try:
        from pyodide.code import find_imports
        names = find_imports(code)
    except Exception:
        return []
    out = []
    for n in names:
        n = n.split('.')[0]
        if not n or n in out or n == 'turtle' or n in sys.builtin_module_names:
            continue
        try:
            if importlib.util.find_spec(n) is None:
                out.append(n)
        except Exception:
            out.append(n)
    return out


_MAXSIZE_REAL = 2 ** 31 - 1


def _itp_preimport(names):
    """Первый импорт сторонних библиотек — с настоящим sys.maxsize сборки (32 бита). ИТП подменяет его на 64-битный
    ради привычных чисел в уроках, а numpy и всё, что на нём построено, при загрузке на этом спотыкаются.
    Дальше модули не выгружаются (_itp_keep), так что повторно импортировать их не нужно."""
    ms = sys.maxsize
    sys.maxsize = _MAXSIZE_REAL
    try:
        for n in names:
            try:
                __import__(n)
                if n == 'matplotlib':
                    __import__('matplotlib.pyplot')
            except Exception:
                pass
    finally:
        sys.maxsize = ms


def _itp_mpl():
    """matplotlib без окон: plt.show() отдаёт каждый рисунок картинкой PNG под выводом программы."""
    os.environ['MPLBACKEND'] = 'Agg'
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except Exception:
        return

    def _show(*a, **k):
        import base64
        for n in plt.get_fignums():
            b = io.BytesIO()
            try:
                plt.figure(n).savefig(b, format='png', dpi=110, bbox_inches='tight')
                _img(base64.b64encode(b.getvalue()).decode(), 'mpl')
            except Exception:
                pass
        plt.close('all')
    plt.show = _show
    plt._itp_show = _show


def _itp_pil():
    """Pillow: Image.show() открывает окно просмотрщика на компьютере; здесь картинка встаёт под вывод программы."""
    try:
        from PIL import Image
    except Exception:
        return
    if getattr(Image.Image.show, '_itp', False):
        return

    def show(self, title=None, **k):
        import base64
        b = io.BytesIO()
        im = self if self.mode in ('RGB', 'RGBA', 'L', 'LA', 'P', '1') else self.convert('RGBA')
        im.save(b, format='PNG')
        _img(base64.b64encode(b.getvalue()).decode(), 'pil')
    show._itp = True
    Image.Image.show = show


def _itp_mpl_flush():
    """Рисунки, которые программа построила, но не показала через plt.show(), тоже показать."""
    m = sys.modules.get('matplotlib.pyplot')
    if m is not None and getattr(m, '_itp_show', None):
        try:
            m._itp_show()
        except Exception:
            pass


def _tdump():
    m = sys.modules.get('turtle')
    if m is None:
        return None
    try:
        return m._dump()
    except Exception:
        return None
