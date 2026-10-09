class JSONDecodeError(ValueError):
    pass

_ESC = {'"': '\\"', '\\': '\\\\', '\n': '\\n', '\r': '\\r', '\t': '\\t', '\b': '\\b', '\f': '\\f'}

def _hex4(n):
    return '\\u' + ('0000' + '%x' % n)[-4:]

def _str(s, ea):
    o = ['"']
    for ch in s:
        if ch in _ESC:
            o.append(_ESC[ch])
            continue
        n = ord(ch)
        if n < 32:
            o.append(_hex4(n))
        elif n > 126 and ea:
            if n > 65535:
                n -= 65536
                o.append(_hex4(55296 + (n >> 10)) + _hex4(56320 + (n & 1023)))
            else:
                o.append(_hex4(n))
        elif n == 127 and ea:
            o.append(ch)
        else:
            o.append(ch)
    o.append('"')
    return ''.join(o)

def _key(k):
    if isinstance(k, str):
        return k
    if k is True:
        return 'true'
    if k is False:
        return 'false'
    if k is None:
        return 'null'
    if isinstance(k, (int, float)):
        return _num(k)
    raise TypeError('keys must be str, int, float, bool or None, not ' + type(k).__name__)

def _num(x):
    if isinstance(x, float):
        if x != x:
            return 'NaN'
        if x == float('inf'):
            return 'Infinity'
        if x == -float('inf'):
            return '-Infinity'
        return repr(x)
    return str(int(x))

def _enc(o, ea, ind, sk, isep, ksep, dflt, lvl):
    if o is None:
        return 'null'
    if o is True:
        return 'true'
    if o is False:
        return 'false'
    if isinstance(o, str):
        return _str(o, ea)
    if isinstance(o, (int, float)):
        return _num(o)
    if isinstance(o, (list, tuple)):
        if not o:
            return '[]'
        items = [_enc(v, ea, ind, sk, isep, ksep, dflt, lvl + 1) for v in o]
        if ind is None:
            return '[' + isep.join(items) + ']'
        pad = '\n' + ind * (lvl + 1)
        return '[' + pad + (isep.rstrip() + pad).join(items) + '\n' + ind * lvl + ']'
    if isinstance(o, dict):
        if not o:
            return '{}'
        ks = list(o.keys())
        if sk:
            ks = sorted(ks)
        items = [_str(_key(k), ea) + ksep + _enc(o[k], ea, ind, sk, isep, ksep, dflt, lvl + 1) for k in ks]
        if ind is None:
            return '{' + isep.join(items) + '}'
        pad = '\n' + ind * (lvl + 1)
        return '{' + pad + (isep.rstrip() + pad).join(items) + '\n' + ind * lvl + '}'
    if dflt is not None:
        return _enc(dflt(o), ea, ind, sk, isep, ksep, dflt, lvl)
    raise TypeError('Object of type ' + type(o).__name__ + ' is not JSON serializable')

def dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False):
    if indent is not None and not isinstance(indent, str):
        indent = ' ' * indent
    if separators is None:
        isep, ksep = (', ', ': ') if indent is None else (',', ': ')
    else:
        isep, ksep = separators
    return _enc(obj, ensure_ascii, indent, sort_keys, isep, ksep, default, 0)

def dump(obj, fp, **kw):
    fp.write(dumps(obj, **kw))

class _P:
    def __init__(self, s):
        self.s = s
        self.i = 0

    def err(self, msg):
        raise JSONDecodeError(msg + ': line 1 column ' + str(self.i + 1) + ' (char ' + str(self.i) + ')')

    def ws(self):
        s = self.s
        while self.i < len(s) and s[self.i] in ' \t\n\r':
            self.i += 1

    def val(self):
        self.ws()
        s = self.s
        if self.i >= len(s):
            self.err('Expecting value')
        c = s[self.i]
        if c == '{':
            self.i += 1
            d = {}
            self.ws()
            if self.i < len(s) and s[self.i] == '}':
                self.i += 1
                return d
            while True:
                self.ws()
                if self.i >= len(s) or s[self.i] != '"':
                    self.err('Expecting property name enclosed in double quotes')
                k = self.string()
                self.ws()
                if self.i >= len(s) or s[self.i] != ':':
                    self.err("Expecting ':' delimiter")
                self.i += 1
                d[k] = self.val()
                self.ws()
                if self.i < len(s) and s[self.i] == ',':
                    self.i += 1
                    continue
                if self.i < len(s) and s[self.i] == '}':
                    self.i += 1
                    return d
                self.err("Expecting ',' delimiter")
        if c == '[':
            self.i += 1
            a = []
            self.ws()
            if self.i < len(s) and s[self.i] == ']':
                self.i += 1
                return a
            while True:
                a.append(self.val())
                self.ws()
                if self.i < len(s) and s[self.i] == ',':
                    self.i += 1
                    continue
                if self.i < len(s) and s[self.i] == ']':
                    self.i += 1
                    return a
                self.err("Expecting ',' delimiter")
        if c == '"':
            return self.string()
        for w, v in (('true', True), ('false', False), ('null', None), ('NaN', float('nan')), ('Infinity', float('inf')), ('-Infinity', -float('inf'))):
            if s.startswith(w, self.i):
                self.i += len(w)
                return v
        j = self.i
        if j < len(s) and s[j] == '-':
            j += 1
        st = j
        while j < len(s) and s[j] in '0123456789':
            j += 1
        if j == st:
            self.err('Expecting value')
        fl = False
        if j < len(s) and s[j] == '.':
            k = j + 1
            while k < len(s) and s[k] in '0123456789':
                k += 1
            if k > j + 1:
                fl = True
                j = k
        if j < len(s) and s[j] in 'eE':
            k = j + 1
            if k < len(s) and s[k] in '+-':
                k += 1
            m = k
            while k < len(s) and s[k] in '0123456789':
                k += 1
            if k > m:
                fl = True
                j = k
        t = s[self.i:j]
        self.i = j
        return float(t) if fl else int(t)

    def string(self):
        s = self.s
        self.i += 1
        o = []
        while True:
            if self.i >= len(s):
                self.err('Unterminated string starting at')
            c = s[self.i]
            if c == '"':
                self.i += 1
                return ''.join(o)
            if c == '\\':
                self.i += 1
                e = s[self.i:self.i + 1]
                if e == 'u':
                    n = int(s[self.i + 1:self.i + 5], 16)
                    self.i += 5
                    if 55296 <= n < 56320 and s[self.i:self.i + 2] == '\\u':
                        n2 = int(s[self.i + 2:self.i + 6], 16)
                        if 56320 <= n2 < 57344:
                            n = 65536 + ((n - 55296) << 10) + (n2 - 56320)
                            self.i += 6
                    o.append(chr(n))
                    continue
                m = {'n': '\n', 't': '\t', 'r': '\r', 'b': '\b', 'f': '\f', '"': '"', '\\': '\\', '/': '/'}
                if e not in m:
                    self.err('Invalid \\escape')
                o.append(m[e])
                self.i += 1
                continue
            if ord(c) < 32:
                self.err('Invalid control character at')
            o.append(c)
            self.i += 1

def loads(s, **kw):
    p = _P(s)
    v = p.val()
    p.ws()
    if p.i < len(s):
        p.err('Extra data')
    return v

def load(fp, **kw):
    return loads(fp.read())
