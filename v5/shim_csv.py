QUOTE_MINIMAL = 0
QUOTE_ALL = 1
QUOTE_NONNUMERIC = 2
QUOTE_NONE = 3

class Error(Exception):
    pass

def _split(line, d, q):
    row = []
    cur = []
    inq = False
    fresh = True
    i = 0
    n = len(line)
    while i < n:
        c = line[i]
        if inq:
            if c == q:
                if i + 1 < n and line[i + 1] == q:
                    cur.append(q)
                    i += 1
                else:
                    inq = False
            else:
                cur.append(c)
        else:
            if c == q and fresh:
                inq = True
                fresh = False
            elif c == d:
                row.append(''.join(cur))
                cur = []
                fresh = True
            else:
                cur.append(c)
                fresh = False
        i += 1
    return row + [''.join(cur)], inq

class reader:
    def __init__(self, f, delimiter=',', quotechar='"', **kw):
        self.f = iter(f)
        self.d = delimiter
        self.q = quotechar
        self.line_num = 0

    def __iter__(self):
        return self

    def __next__(self):
        line = next(self.f)
        self.line_num += 1
        line = line.rstrip('\r\n') if line.endswith('\n') or line.endswith('\r') else line
        row, inq = _split(line, self.d, self.q)
        while inq:
            try:
                nxt = next(self.f)
            except StopIteration:
                break
            self.line_num += 1
            line = line + '\n' + nxt.rstrip('\r\n')
            row, inq = _split(line, self.d, self.q)
        if line == '':
            return []
        return row

    next = __next__

class DictReader:
    def __init__(self, f, fieldnames=None, restkey=None, restval=None, delimiter=',', quotechar='"', **kw):
        self.reader = reader(f, delimiter, quotechar)
        self._fn = fieldnames
        self.restkey = restkey
        self.restval = restval

    @property
    def fieldnames(self):
        if self._fn is None:
            try:
                self._fn = next(self.reader)
            except StopIteration:
                pass
        return self._fn

    def __iter__(self):
        return self

    def __next__(self):
        fn = self.fieldnames
        row = next(self.reader)
        while row == []:
            row = next(self.reader)
        d = {}
        for i in range(len(fn)):
            d[fn[i]] = row[i] if i < len(row) else self.restval
        if len(row) > len(fn):
            d[self.restkey] = row[len(fn):]
        return d

def _cell(v, d, q, quoting):
    if v is None:
        v = ''
    s = v if isinstance(v, str) else str(v)
    need = quoting == QUOTE_ALL or (quoting == QUOTE_NONNUMERIC and isinstance(v, str))
    if not need and quoting != QUOTE_NONE:
        need = d in s or q in s or '\n' in s or '\r' in s or (s == '' and False)
    if need:
        s = q + s.replace(q, q + q) + q
    return s

class writer:
    def __init__(self, f, delimiter=',', quotechar='"', lineterminator='\r\n', quoting=QUOTE_MINIMAL, **kw):
        self.f = f
        self.d = delimiter
        self.q = quotechar
        self.lt = lineterminator
        self.quoting = quoting

    def writerow(self, row):
        row = list(row)
        if len(row) == 1 and (row[0] is None or row[0] == ''):
            s = self.q + self.q
        else:
            s = self.d.join([_cell(v, self.d, self.q, self.quoting) for v in row])
        return self.f.write(s + self.lt)

    def writerows(self, rows):
        for r in rows:
            self.writerow(r)

class DictWriter:
    def __init__(self, f, fieldnames, restval='', extrasaction='raise', **kw):
        self.fieldnames = list(fieldnames)
        self.restval = restval
        self.extrasaction = extrasaction
        self.w = writer(f, **kw)

    def writeheader(self):
        return self.w.writerow(self.fieldnames)

    def writerow(self, d):
        if self.extrasaction == 'raise':
            extra = [k for k in d if k not in self.fieldnames]
            if extra:
                raise ValueError('dict contains fields not in fieldnames: ' + ', '.join([repr(k) for k in extra]))
        return self.w.writerow([d.get(k, self.restval) for k in self.fieldnames])

    def writerows(self, rows):
        for r in rows:
            self.writerow(r)
