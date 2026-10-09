import re

_MON = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
_DAY = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def _strptime(data_string, format):
    pat = ''
    keys = []
    i = 0
    while i < len(format):
        c = format[i]
        if c == '%' and i + 1 < len(format):
            d = format[i + 1]
            i += 2
            if d == '%':
                pat += '%'
            elif d in 'YymdHMSIjf':
                w = {'Y': '(\\d{4})', 'y': '(\\d{2})', 'm': '(\\d{1,2})', 'd': '(\\d{1,2})', 'H': '(\\d{1,2})', 'M': '(\\d{1,2})', 'S': '(\\d{1,2})', 'I': '(\\d{1,2})', 'j': '(\\d{1,3})', 'f': '(\\d{1,6})'}[d]
                pat += w
                keys.append(d)
            elif d in 'bBaApZ':
                pat += '([A-Za-z]+)' if d != 'p' else '([AaPp][Mm])'
                keys.append(d)
            else:
                raise ValueError("'" + d + "' is a bad directive in format '" + format + "'")
        elif c == ' ':
            pat += '\\s+'
            i += 1
        else:
            pat += ('\\' + c) if c in '.^$*+?{}[]\\|()' else c
            i += 1
    m = re.match('^' + pat + '$', data_string)
    if not m:
        raise ValueError("time data '" + data_string + "' does not match format '" + format + "'")
    y, mo, d, H, M, S, us = 1900, 1, 1, 0, 0, 0, 0
    pm = None
    for k, v in zip(keys, m.groups()):
        if k == 'Y':
            y = int(v)
        elif k == 'y':
            y = int(v) + (2000 if int(v) < 69 else 1900)
        elif k == 'm':
            mo = int(v)
        elif k == 'd':
            d = int(v)
        elif k in 'HI':
            H = int(v)
        elif k == 'M':
            M = int(v)
        elif k == 'S':
            S = int(v)
        elif k == 'f':
            us = int((v + '000000')[:6])
        elif k == 'p':
            pm = v.lower() == 'pm'
        elif k == 'B' or k == 'b':
            n = v.lower()
            for idx in range(12):
                if _MON[idx] == n or _MON[idx][:3] == n:
                    mo = idx + 1
                    break
            else:
                raise ValueError("time data '" + data_string + "' does not match format '" + format + "'")
    if pm is not None:
        if pm and H < 12:
            H += 12
        if not pm and H == 12:
            H = 0
    if not (1 <= mo <= 12) or not (1 <= d <= 31) or H > 23 or M > 59 or S > 61:
        raise ValueError('unconverted data remains or value out of range')
    return (y, mo, d, H, M, S, 0, 1, -1), us
