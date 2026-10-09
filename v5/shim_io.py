class StringIO:
    def __init__(self, initial_value='', newline=None):
        self._s = initial_value
        self._i = 0
        self.closed = False

    def write(self, s):
        self._s = self._s[:self._i] + s + self._s[self._i + len(s):]
        self._i += len(s)
        return len(s)

    def writelines(self, ls):
        for l in ls:
            self.write(l)

    def getvalue(self):
        return self._s

    def read(self, n=-1):
        r = self._s[self._i:] if n is None or n < 0 else self._s[self._i:self._i + n]
        self._i += len(r)
        return r

    def readline(self):
        if self._i >= len(self._s):
            return ''
        j = self._s.find('\n', self._i)
        j = len(self._s) if j < 0 else j + 1
        r = self._s[self._i:j]
        self._i = j
        return r

    def readlines(self):
        r = []
        while True:
            l = self.readline()
            if l == '':
                return r
            r.append(l)

    def seek(self, p, w=0):
        self._i = p
        return p

    def tell(self):
        return self._i

    def truncate(self, size=None):
        self._s = self._s[:self._i if size is None else size]

    def close(self):
        self.closed = True

    def __iter__(self):
        return self

    def __next__(self):
        l = self.readline()
        if l == '':
            raise StopIteration
        return l

    next = __next__

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        return False
