import sys
import time

__all__ = ['open', 'OSError', 'FileNotFoundError', 'FileExistsError', 'eval_', 'input', 'IOError', 'zip_', 'bytearray', '__itp_ifb']
_bi = input

class OSError(Exception):
    pass

IOError = OSError

class FileNotFoundError(OSError):
    pass

class FileExistsError(OSError):
    pass

_FS = __itp_files__

class _File:
    def __init__(self, name, mode, newline=None):
        self.nl = newline
        self.name = name
        self.mode = mode
        self.closed = False
        self._i = 0
        self._r = 'r' in mode or '+' in mode
        self._w = 'w' in mode or 'a' in mode or 'x' in mode or '+' in mode
        if 'r' in mode:
            if name not in _FS:
                raise FileNotFoundError("[Errno 2] No such file or directory: " + repr(name))
        elif 'w' in mode:
            _FS[name] = ''
        elif 'x' in mode:
            if name in _FS:
                raise FileExistsError("[Errno 17] File exists: " + repr(name))
            _FS[name] = ''
        elif 'a' in mode:
            if name not in _FS:
                _FS[name] = ''
            self._i = len(_FS[name])

    def _chk(self):
        if self.closed:
            raise ValueError('I/O operation on closed file.')

    def _t(self):
        t = _FS[self.name]
        if isinstance(t, bytes):
            t = t.decode('utf-8')
            _FS[self.name] = t
        if self.nl is None and '\r' in t:
            t = t.replace('\r\n', '\n').replace('\r', '\n')
        return t

    def read(self, n=-1):
        self._chk()
        if not self._r:
            raise OSError('not readable')
        t = self._t()
        if n is None or n < 0:
            r = t[self._i:]
        else:
            r = t[self._i:self._i + n]
        self._i += len(r)
        return r

    def readline(self, n=-1):
        self._chk()
        if not self._r:
            raise OSError('not readable')
        t = self._t()
        if self._i >= len(t):
            return ''
        j = t.find('\n', self._i)
        j = len(t) if j < 0 else j + 1
        r = t[self._i:j]
        self._i = j
        return r

    def readlines(self, hint=-1):
        r = []
        while True:
            l = self.readline()
            if l == '':
                return r
            r.append(l)

    def __iter__(self):
        self._chk()
        return self

    def __next__(self):
        l = self.readline()
        if l == '':
            raise StopIteration
        return l

    next = __next__

    def write(self, s):
        self._chk()
        if not self._w:
            raise OSError('not writable')
        if not isinstance(s, str):
            raise TypeError('write() argument must be str, not ' + type(s).__name__)
        t = _FS[self.name]
        if isinstance(t, bytes):
            t = t.decode('utf-8')
        if 'a' in self.mode:
            self._i = len(t)
        _FS[self.name] = t[:self._i] + s + t[self._i + len(s):]
        self._i += len(s)
        return len(s)

    def writelines(self, lines):
        for l in lines:
            self.write(l)

    def seek(self, pos, whence=0):
        self._i = pos if whence == 0 else (self._i + pos if whence == 1 else len(_FS[self.name]) + pos)
        return self._i

    def tell(self):
        return self._i

    def flush(self):
        pass

    def readable(self):
        return self._r

    def writable(self):
        return self._w

    def close(self):
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        self.close()
        return False

class bytearray:
    def __init__(self, src=b'', encoding=None):
        if isinstance(src, int):
            self._l = [0] * src
        elif isinstance(src, str):
            self._l = list(src.encode(encoding or 'utf-8'))
        else:
            self._l = list(src)

    def __len__(self):
        return len(self._l)

    def __iter__(self):
        return iter(self._l)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return bytearray(self._l[i])
        return self._l[i]

    def __setitem__(self, i, v):
        if isinstance(i, slice):
            self._l[i] = list(v)
        else:
            if not 0 <= v < 256:
                raise ValueError('byte must be in range(0, 256)')
            self._l[i] = v

    def __delitem__(self, i):
        del self._l[i]

    def append(self, v):
        if not 0 <= v < 256:
            raise ValueError('byte must be in range(0, 256)')
        self._l.append(v)

    def extend(self, it):
        for v in it:
            self.append(v)

    def pop(self, i=-1):
        return self._l.pop(i)

    def __add__(self, o):
        return bytearray(self._l + list(o))

    def __iadd__(self, o):
        self.extend(o)
        return self

    def __eq__(self, o):
        return list(self._l) == list(o)

    def decode(self, enc='utf-8'):
        return bytes(self._l).decode(enc)

    def hex(self):
        return bytes(self._l).hex()

    def __bytes__(self):
        return bytes(self._l)

    def __repr__(self):
        return 'bytearray(' + repr(bytes(self._l)) + ')'


def _tob(v):
    if isinstance(v, bytearray):
        return bytes(v._l)
    if isinstance(v, bytes):
        return v
    raise TypeError("a bytes-like object is required, not '" + type(v).__name__ + "'")


def __itp_ifb(b, byteorder='big', signed=False):
    l = list(_tob(b)) if not isinstance(b, (list, tuple)) else list(b)
    if byteorder == 'little':
        l = l[::-1]
    elif byteorder != 'big':
        raise ValueError("byteorder must be either 'little' or 'big'")
    v = 0
    for x in l:
        v = v * 256 + x
    if signed and l and l[0] >= 128:
        v -= 256 ** len(l)
    return v


class _BFile:
    def __init__(self, name, mode):
        self.name = name
        self.mode = mode
        self.closed = False
        self._i = 0
        self._r = 'r' in mode or '+' in mode
        self._w = 'w' in mode or 'a' in mode or 'x' in mode or '+' in mode
        if 'r' in mode:
            if name not in _FS:
                raise FileNotFoundError("[Errno 2] No such file or directory: " + repr(name))
        elif 'w' in mode:
            _FS[name] = b''
        elif 'x' in mode:
            if name in _FS:
                raise FileExistsError("[Errno 17] File exists: " + repr(name))
            _FS[name] = b''
        elif 'a' in mode:
            if name not in _FS:
                _FS[name] = b''
            self._i = len(self._d())

    def _chk(self):
        if self.closed:
            raise ValueError('I/O operation on closed file.')

    def _d(self):
        v = _FS[self.name]
        if isinstance(v, str):
            v = v.encode('utf-8')
        return v

    def read(self, n=-1):
        self._chk()
        if not self._r:
            raise OSError('not readable')
        d = self._d()
        r = d[self._i:] if n is None or n < 0 else d[self._i:self._i + n]
        self._i += len(r)
        return r

    def readline(self):
        self._chk()
        d = self._d()
        j = d.find(b'\n', self._i)
        r = d[self._i:] if j < 0 else d[self._i:j + 1]
        self._i += len(r)
        return r

    def readlines(self):
        r = []
        while True:
            l = self.readline()
            if not l:
                return r
            r.append(l)

    def __iter__(self):
        return self

    def __next__(self):
        l = self.readline()
        if not l:
            raise StopIteration
        return l

    next = __next__

    def write(self, b):
        self._chk()
        if not self._w:
            raise OSError('not writable')
        if isinstance(b, str):
            raise TypeError("a bytes-like object is required, not 'str'")
        b = _tob(b)
        d = self._d()
        if 'a' in self.mode:
            self._i = len(d)
        _FS[self.name] = d[:self._i] + b + d[self._i + len(b):]
        self._i += len(b)
        return len(b)

    def seek(self, pos, whence=0):
        self._i = pos if whence == 0 else (self._i + pos if whence == 1 else len(self._d()) + pos)
        return self._i

    def tell(self):
        return self._i

    def flush(self):
        pass

    def readable(self):
        return self._r

    def writable(self):
        return self._w

    def close(self):
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        self.close()
        return False


def open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None):
    if 'b' in mode:
        if encoding is not None:
            raise ValueError("binary mode doesn't take an encoding argument")
        return _BFile(file, mode)
    return _File(file, mode, newline)

# ---------- ввод ----------
class _Stdin:
    name = '<stdin>'

    def _line(self):
        sys.stdin = _so
        try:
            v = _bi('\x05')
        finally:
            sys.stdin = _me
        if v == '\x05EOF':
            return None
        return v + '\n'

    def readline(self, n=-1):
        l = self._line()
        return '' if l is None else l

    def readlines(self, hint=-1):
        r = []
        while True:
            l = self._line()
            if l is None:
                return r
            r.append(l)

    def read(self, n=-1):
        return ''.join(self.readlines())

    def __iter__(self):
        return self

    def __next__(self):
        l = self._line()
        if l is None:
            raise StopIteration
        return l

    next = __next__

_so = sys.stdin
_me = _Stdin()
if __itp_stdin__:
    sys.stdin = _me

def input(prompt=''):
    sys.stdin = _so
    try:
        return _bi(prompt)
    finally:
        if __itp_stdin__:
            sys.stdin = _me


# ---------- прочее ----------
def _gsz(o):
    n = type(o).__name__
    if n == 'bool':
        return 28
    if n == 'int':
        k = 0
        x = abs(o)
        while x:
            k += 1
            x >>= 30
        return 24 + 4 * max(k, 1) if o else 24
    if n == 'float':
        return 24
    if n == 'NoneType':
        return 16
    if n == 'str':
        w = 1
        for ch in o:
            if ord(ch) > 65535:
                w = 4
                break
            if ord(ch) > 255 and w < 2:
                w = 2
        return (41 if w == 1 and o.isascii() else 58 if w == 1 else 74 if w == 2 else 76) + w * len(o)
    if n == 'list':
        return 56 + 8 * len(o)
    if n == 'tuple':
        return 40 + 8 * len(o)
    if n == 'set':
        return 216 if len(o) < 5 else 728
    if n == 'dict':
        return 64 + 8 * len(o) * 3 if len(o) else 64
    if n == 'generator':
        return 112
    if n == 'range':
        return 48
    return 48

sys.getsizeof = _gsz
time.perf_counter = time.time
time.perf_counter_ns = lambda: int(time.time() * 1000000000)
time.monotonic = time.time

# ---------- eval (подмножество выражений) ----------
_TOK = None

def _tokenize(s):
    t = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c in ' \t\n':
            i += 1
        elif c.isdigit() or (c == '.' and i + 1 < n and s[i + 1].isdigit()):
            j = i
            while j < n and (s[j].isdigit() or s[j] == '.' or s[j] in 'eE' or (s[j] in '+-' and s[j - 1] in 'eE')):
                j += 1
            t.append(('n', s[i:j]))
            i = j
        elif c.isalpha() or c == '_':
            j = i
            while j < n and (s[j].isalnum() or s[j] == '_'):
                j += 1
            t.append(('w', s[i:j]))
            i = j
        elif c in '"\'':
            j = i + 1
            o = ''
            while j < n and s[j] != c:
                if s[j] == '\\' and j + 1 < n:
                    j += 1
                    o += {'n': '\n', 't': '\t'}.get(s[j], s[j])
                else:
                    o += s[j]
                j += 1
            t.append(('s', o))
            i = j + 1
        else:
            two = s[i:i + 2]
            three = s[i:i + 3]
            if two in ('==', '!=', '<=', '>=', '//', '**') :
                t.append(('o', two))
                i += 2
            else:
                t.append(('o', c))
                i += 1
    t.append(('e', ''))
    return t

class _Ev:
    def __init__(self, s, g, l):
        self.t = _tokenize(s)
        self.p = 0
        self.g = g
        self.l = l

    def peek(self):
        return self.t[self.p]

    def nxt(self):
        x = self.t[self.p]
        self.p += 1
        return x

    def isop(self, v):
        x = self.t[self.p]
        return x[0] in 'ow' and x[1] == v and x[0] != 's'

    def eat(self, v):
        if self.isop(v):
            self.p += 1
            return True
        return False

    def need(self, v):
        if not self.eat(v):
            raise SyntaxError('invalid syntax')

    def name(self, w):
        if w in self.l:
            return self.l[w]
        if w in self.g:
            return self.g[w]
        b = {'abs': abs, 'max': max, 'min': min, 'sum': sum, 'len': len, 'int': int, 'float': float, 'str': str, 'bool': bool, 'list': list, 'tuple': tuple, 'set': set, 'dict': dict, 'round': round, 'sorted': sorted, 'range': range, 'pow': pow, 'divmod': divmod, 'ord': ord, 'chr': chr, 'any': any, 'all': all, 'map': map, 'zip': zip, 'enumerate': enumerate, 'reversed': reversed, 'repr': repr, 'True': True, 'False': False, 'None': None}
        if w in b:
            return b[w]
        raise NameError("name '" + w + "' is not defined")

    def run(self):
        v = self.ternary()
        if self.peek()[0] != 'e':
            raise SyntaxError('invalid syntax')
        return v

    def ternary(self):
        v = self.orx()
        if self.isop('if'):
            self.p += 1
            c = self.orx()
            self.need('else')
            e = self.ternary()
            return v if c else e
        return v

    def orx(self):
        v = self.andx()
        while self.isop('or'):
            self.p += 1
            r = self.andx()
            v = v or r
        return v

    def andx(self):
        v = self.notx()
        while self.isop('and'):
            self.p += 1
            r = self.notx()
            v = v and r
        return v

    def notx(self):
        if self.isop('not'):
            self.p += 1
            return not self.notx()
        return self.cmp()

    def cmp(self):
        a = self.arith()
        res = True
        first = True
        while True:
            op = None
            x = self.peek()
            if x[0] == 'o' and x[1] in ('==', '!=', '<', '>', '<=', '>='):
                op = x[1]
                self.p += 1
            elif x[0] == 'w' and x[1] == 'in':
                op = 'in'
                self.p += 1
            elif x[0] == 'w' and x[1] == 'not' and self.t[self.p + 1][1] == 'in':
                op = 'not in'
                self.p += 2
            elif x[0] == 'w' and x[1] == 'is':
                self.p += 1
                if self.isop('not'):
                    self.p += 1
                    op = 'is not'
                else:
                    op = 'is'
            if op is None:
                return a if first else res
            b = self.arith()
            first = False
            if op == '==':
                r = a == b
            elif op == '!=':
                r = a != b
            elif op == '<':
                r = a < b
            elif op == '>':
                r = a > b
            elif op == '<=':
                r = a <= b
            elif op == '>=':
                r = a >= b
            elif op == 'in':
                r = a in b
            elif op == 'not in':
                r = a not in b
            elif op == 'is':
                r = a is b
            else:
                r = a is not b
            res = res and r
            a = b

    def arith(self):
        v = self.term()
        while self.peek()[0] == 'o' and self.peek()[1] in ('+', '-'):
            o = self.nxt()[1]
            r = self.term()
            v = v + r if o == '+' else v - r
        return v

    def term(self):
        v = self.unary()
        while self.peek()[0] == 'o' and self.peek()[1] in ('*', '/', '//', '%'):
            o = self.nxt()[1]
            r = self.unary()
            if o == '*':
                v = v * r
            elif o == '/':
                v = v / r
            elif o == '//':
                v = v // r
            else:
                v = v % r
        return v

    def unary(self):
        if self.peek()[0] == 'o' and self.peek()[1] in ('-', '+'):
            o = self.nxt()[1]
            v = self.unary()
            return -v if o == '-' else +v
        return self.power()

    def power(self):
        v = self.post()
        if self.peek()[0] == 'o' and self.peek()[1] == '**':
            self.p += 1
            return v ** self.unary()
        return v

    def post(self):
        v = self.atom()
        while True:
            x = self.peek()
            if x[0] == 'o' and x[1] == '(':
                self.p += 1
                a = []
                k = {}
                while not self.isop(')'):
                    if self.peek()[0] == 'w' and self.t[self.p + 1][1] == '=' and self.t[self.p + 2][1] != '=':
                        nm = self.nxt()[1]
                        self.p += 1
                        k[nm] = self.ternary()
                    else:
                        a.append(self.ternary())
                    if not self.eat(','):
                        break
                self.need(')')
                v = v(*a, **k)
            elif x[0] == 'o' and x[1] == '[':
                self.p += 1
                lo = None
                if not self.isop(':'):
                    lo = self.ternary()
                if self.eat(':'):
                    hi = None
                    st = None
                    if not self.isop(']') and not self.isop(':'):
                        hi = self.ternary()
                    if self.eat(':'):
                        if not self.isop(']'):
                            st = self.ternary()
                    self.need(']')
                    v = v[lo:hi:st] if st is not None else v[lo:hi]
                else:
                    self.need(']')
                    v = v[lo]
            elif x[0] == 'o' and x[1] == '.':
                self.p += 1
                v = getattr(v, self.nxt()[1])
            else:
                return v

    def atom(self):
        x = self.nxt()
        if x[0] == 'n':
            return float(x[1]) if ('.' in x[1] or 'e' in x[1] or 'E' in x[1]) else int(x[1])
        if x[0] == 's':
            s = x[1]
            while self.peek()[0] == 's':
                s += self.nxt()[1]
            return s
        if x[0] == 'w':
            return self.name(x[1])
        if x[1] == '(':
            if self.eat(')'):
                return ()
            v = self.ternary()
            if self.isop(','):
                r = [v]
                while self.eat(','):
                    if self.isop(')'):
                        break
                    r.append(self.ternary())
                self.need(')')
                return tuple(r)
            self.need(')')
            return v
        if x[1] == '[':
            r = []
            while not self.isop(']'):
                r.append(self.ternary())
                if not self.eat(','):
                    break
            self.need(']')
            return r
        if x[1] == '{':
            if self.eat('}'):
                return {}
            first = self.ternary()
            if self.eat(':'):
                d = {first: self.ternary()}
                while self.eat(','):
                    if self.isop('}'):
                        break
                    k = self.ternary()
                    self.need(':')
                    d[k] = self.ternary()
                self.need('}')
                return d
            s = {first}
            while self.eat(','):
                if self.isop('}'):
                    break
                s.add(self.ternary())
            self.need('}')
            return s
        raise SyntaxError('invalid syntax')

def _ev(source, globals=None, locals=None):
    g = globals
    if g is None:
        g = sys.modules['__main__'].__dict__
    l = locals if locals is not None else {}
    return _Ev(source.strip(), g, l).run()

eval_ = _ev


def _zg(iters, strict):
    while True:
        row = []
        for k in range(len(iters)):
            try:
                row.append(next(iters[k]))
            except StopIteration:
                if strict:
                    if k > 0:
                        raise ValueError('zip() argument ' + str(k + 1) + ' is shorter than argument 1')
                    for j in range(1, len(iters)):
                        try:
                            next(iters[j])
                        except StopIteration:
                            continue
                        raise ValueError('zip() argument ' + str(j + 1) + ' is longer than argument 1')
                return
        yield tuple(row)

def zip_(*its, strict=False):
    iters = [iter(x) for x in its]
    if not iters:
        return iter([])
    return _zg(iters, strict)
