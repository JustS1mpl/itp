class StatisticsError(ValueError):
    pass

def _chk(d):
    d = list(d)
    if not d:
        raise StatisticsError('no data points' if False else 'mean requires at least one data point')
    return d

def mean(data):
    d = _chk(data)
    s = sum(d)
    n = len(d)
    if all([isinstance(x, int) for x in d]):
        if s % n == 0:
            return s // n
        return s / n
    return s / n

def fmean(data, weights=None):
    d = _chk(data)
    return sum(d) / len(d)

def median(data):
    d = sorted(_chk(data))
    n = len(d)
    if n % 2:
        return d[n // 2]
    a = d[n // 2 - 1]
    b = d[n // 2]
    return (a + b) / 2

def median_low(data):
    d = sorted(_chk(data))
    n = len(d)
    return d[n // 2] if n % 2 else d[n // 2 - 1]

def median_high(data):
    d = sorted(_chk(data))
    return d[len(d) // 2]

def multimode(data):
    d = list(data)
    c = {}
    for x in d:
        c[x] = c.get(x, 0) + 1
    if not c:
        return []
    m = max(c.values())
    return [k for k in c if c[k] == m]

def mode(data):
    r = multimode(data)
    if not r:
        raise StatisticsError('no mode for empty data')
    return r[0]

def _ss(d, c):
    return sum([(x - c) ** 2 for x in d])

def pvariance(data, mu=None):
    d = _chk(data)
    c = sum(d) / len(d) if mu is None else mu
    return _ss(d, c) / len(d)

def variance(data, xbar=None):
    d = list(data)
    if len(d) < 2:
        raise StatisticsError('variance requires at least two data points')
    c = sum(d) / len(d) if xbar is None else xbar
    return _ss(d, c) / (len(d) - 1)

def pstdev(data, mu=None):
    return pvariance(data, mu) ** 0.5

def stdev(data, xbar=None):
    return variance(data, xbar) ** 0.5
