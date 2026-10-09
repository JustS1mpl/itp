# -*- coding: utf-8 -*-
"""Логика №5: правила-автоматы, формы вопросов, ловушки. f(n) всегда берётся из ТЕКСТА кода (exec),
тот же текст попадает в разбор — поэтому сниппет и ответ не могут разойтись."""
import random

LIMIT = 200000


def bits(n):
    return bin(n)[2:]


def inv(s):
    return ''.join('1' if c == '0' else '0' for c in s)


class Rule:
    def __init__(self, kind, text, code, trace_fn, domain=None, short=""):
        self.kind, self.text, self.code, self.trace_fn, self.domain, self.short = kind, text, code, trace_fn, domain, short
        ns = {}
        exec(code, ns)
        self.f = ns['f']

    def trace(self, n):
        t = self.trace_fn(n)
        assert t['R'] == self.f(n), (self.kind, n, t, self.f(n))
        return t


def quote(s):
    return "«%s»" % s


def clause_side(left, right):
    parts = []
    if left:
        parts.append("слева дописывается %s" % quote(left))
    if right:
        parts.append("справа дописывается %s" % quote(right))
    return ", а ".join(parts) if len(parts) == 2 else parts[0]


# ----------------------------------------------------------------------------------------
def rule_A(el, er, ol, orr):
    """5.1 Дописывание цифр слева/справа в зависимости от чётности N."""
    text = ("Алгоритм получает на вход натуральное число N и строит новое число R следующим образом.\n"
            "1. Строится двоичная запись числа N.\n"
            "2. Если N чётное, то в этой записи %s; если N нечётное, то %s.\n"
            "3. Полученная запись является двоичной записью искомого числа R.") % (clause_side(el, er), clause_side(ol, orr))
    code = ("def f(n):\n    b = bin(n)[2:]                       # двоичная запись N\n"
            "    if n %% 2 == 0:\n        s = %r + b + %r\n    else:\n        s = %r + b + %r\n"
            "    return int(s, 2)                     # R в десятичной системе\n") % (el, er, ol, orr)

    def tr(n):
        b = bits(n)
        s = (el + b + er) if n % 2 == 0 else (ol + b + orr)
        return dict(bin=b, branch="чётное" if n % 2 == 0 else "нечётное", step=s, R=int(s, 2))
    return Rule('A', text, code, tr, short="дописывание по чётности")


def rule_B(em, om):
    """5.2 Замена цифр двоичной записи по чётности N."""
    def cl(m):
        return ", ".join("каждая цифра %s заменяется на %s" % (quote(k), quote(v)) for k, v in m.items())
    text = ("Алгоритм получает на вход натуральное число N и строит новое число R следующим образом.\n"
            "1. Строится двоичная запись числа N.\n"
            "2. Если N чётное, то в записи %s; если N нечётное, то %s.\n"
            "3. Полученная запись является двоичной записью искомого числа R.") % (cl(em), cl(om))
    code = ("def f(n):\n    b = bin(n)[2:]\n    m = %r if n %% 2 == 0 else %r      # какая замена действует\n"
            "    s = ''.join(m.get(c, c) for c in b)    # цифры, которых нет в m, остаются\n    return int(s, 2)\n") % (em, om)

    def tr(n):
        b = bits(n)
        m = em if n % 2 == 0 else om
        s = ''.join(m.get(c, c) for c in b)
        return dict(bin=b, branch="чётное" if n % 2 == 0 else "нечётное", step=s, R=int(s, 2))
    return Rule('B', text, code, tr, short="замена цифр")


def rule_C(side, times, flip):
    """5.3 Бит чётности (контрольный разряд), times раз."""
    what = ("единицы 1, если число единиц в записи нечётно, иначе 0" if not flip else
            "0, если число единиц в записи нечётно, иначе 1")
    where = "справа" if side == 'r' else "слева"
    rep = {1: "", 2: " Затем те же действия выполняются ещё раз для полученной записи.", 3: " Затем те же действия выполняются ещё два раза (для каждой новой записи)."}[times]
    text = ("Алгоритм получает на вход натуральное число N и строит новое число R следующим образом.\n"
            "1. Строится двоичная запись числа N.\n"
            "2. %s к записи дописывается контрольный разряд: %s.%s\n"
            "3. Полученная запись является двоичной записью искомого числа R.") % (where.capitalize(), what, rep)
    code = ("def f(n):\n    s = bin(n)[2:]\n    for _ in range(%d):\n        p = str(s.count('1') %% 2)%s\n        s = %s\n    return int(s, 2)\n") % (
        times, "" if not flip else "\n        p = '1' if p == '0' else '0'    # контрольный разряд инвертирован", "s + p" if side == 'r' else "p + s")

    def tr(n):
        s = bits(n)
        b0 = s
        seq = []
        for _ in range(times):
            p = str(s.count('1') % 2)
            if flip:
                p = '1' if p == '0' else '0'
            s = (s + p) if side == 'r' else (p + s)
            seq.append(s)
        return dict(bin=b0, branch="", step=" → ".join(seq), R=int(s, 2))
    return Rule('C', text, code, tr, short="контрольный разряд")


def rule_D(k, side, times):
    """5.4 Дописывание остатка от деления на k."""
    where = "справа" if side == 'r' else "слева"
    rep = {1: "", 2: " Затем с полученным числом выполняются те же действия ещё раз."}[times]
    text = ("Алгоритм получает на вход натуральное число N и строит новое число R следующим образом.\n"
            "1. Строится двоичная запись числа N.\n"
            "2. %s к записи дописывается двоичная запись остатка от деления N на %d.%s\n"
            "3. Полученная запись является двоичной записью искомого числа R.") % (where.capitalize(), k, rep)
    if times == 1:
        code = ("def f(n):\n    s = bin(n)[2:]\n    r = bin(n %% %d)[2:]                 # остаток в двоичной записи\n    s = %s\n    return int(s, 2)\n") % (
            k, "s + r" if side == 'r' else "r + s")
    else:
        code = ("def f(n):\n    for _ in range(2):\n        r = bin(n %% %d)[2:]            # остаток от деления текущего числа\n"
                "        s = bin(n)[2:]\n        s = %s\n        n = int(s, 2)\n    return n\n") % (k, "s + r" if side == 'r' else "r + s")

    def tr(n):
        seq = []
        cur = n
        b0 = bits(n)
        for _ in range(times):
            r = bits(cur % k)
            s = bits(cur)
            s = (s + r) if side == 'r' else (r + s)
            seq.append("%s (ост. %d)" % (s, cur % k))
            cur = int(s, 2)
        return dict(bin=b0, branch="остаток %d" % (n % k), step=" → ".join(seq), R=cur)
    return Rule('D', text, code, tr, short="остаток от деления")


def rule_E(es, os_, oextra):
    """5.5 Инверсия записи."""
    def side(x):
        return "справа" if x == 'r' else "слева"
    text = ("Алгоритм получает на вход натуральное число N и строит новое число R следующим образом.\n"
            "1. Строится двоичная запись числа N.\n"
            "2. Строится инверсия этой записи (все нули заменяются единицами, а единицы — нулями).\n"
            "3. Если N чётное, то инверсия дописывается к исходной записи %s; если N нечётное, то %s.\n"
            "4. Полученная запись является двоичной записью искомого числа R.") % (
        side(es), ("в начало записи инверсии добавляется «%s», после чего она дописывается %s" % (oextra, side(os_))) if oextra else ("инверсия дописывается %s" % side(os_)))
    code = ("def f(n):\n    b = bin(n)[2:]\n    c = ''.join('1' if x == '0' else '0' for x in b)   # инверсия\n"
            "    if n %% 2 == 0:\n        s = %s\n    else:\n        c = %r + c\n        s = %s\n    return int(s, 2)\n") % (
        "b + c" if es == 'r' else "c + b", oextra, "b + c" if os_ == 'r' else "c + b")

    def tr(n):
        b = bits(n)
        c = inv(b)
        if n % 2 == 0:
            s = (b + c) if es == 'r' else (c + b)
        else:
            c = oextra + c
            s = (b + c) if os_ == 'r' else (c + b)
        return dict(bin=b, branch="чётное" if n % 2 == 0 else "нечётное", step="инверсия " + (inv(b) if n % 2 == 0 else c) + " → " + s, R=int(s, 2))
    return Rule('E', text, code, tr, short="инверсия")


def rule_F(d, order):
    """5.6 Суммы цифр десятичного числа."""
    pairs = {3: [(0, 1), (1, 2)], 4: [(0, 1), (2, 3)], -4: [(0, 1), (1, 2), (2, 3)]}[d]
    dd = abs(d)
    names = ["первой", "второй", "третьей", "четвёртой"]
    sums = "; ".join("сумма %s и %s цифр" % (names[i], names[j]) for i, j in pairs)
    od = "неубывания" if order == 'asc' else "невозрастания"
    ex_n = {3: 678, 4: 3678, -4: 3678}[d]
    dg = [int(c) for c in str(ex_n)]
    sv = sorted([dg[i] + dg[j] for i, j in pairs], reverse=(order == 'desc'))
    text = ("Автомат получает на вход %d-значное десятичное число N. По нему строится новое число R:\n"
            "1. Вычисляются суммы: %s.\n"
            "2. Полученные числа записываются друг за другом (без разделителей) в порядке %s.\n"
            "Пример. Для N = %d вычисляются суммы %s; в порядке %s получается R = %s.") % (
        dd, sums, od, ex_n, ", ".join(str(dg[i] + dg[j]) for i, j in pairs), od, ''.join(map(str, sv)))
    code = ("def f(n):\n    d = [int(c) for c in str(n)]          # цифры числа\n    s = [%s]   # суммы\n"
            "    s.sort(reverse=%s)                    # %s\n    return int(''.join(map(str, s)))\n") % (
        ", ".join("d[%d] + d[%d]" % p for p in pairs), order == 'desc', "по невозрастанию" if order == 'desc' else "по неубыванию")

    def tr(n):
        dg = [int(c) for c in str(n)]
        sm = [dg[i] + dg[j] for i, j in pairs]
        sv = sorted(sm, reverse=(order == 'desc'))
        return dict(bin=str(n), branch="", step="суммы " + ", ".join(map(str, sm)) + " → " + ''.join(map(str, sv)), R=int(''.join(map(str, sv))))
    return Rule('F', text, code, tr, domain=(10 ** (dd - 1), 10 ** dd - 1), short="суммы цифр")


def make_rule(kind, **p):
    return {'A': rule_A, 'B': rule_B, 'C': rule_C, 'D': rule_D, 'E': rule_E, 'F': rule_F}[kind](**p)


# ----------------------------------------------------------------------------------------
def dom(rule):
    return rule.domain if rule.domain else (1, LIMIT)


def values(rule, lo, hi):
    return {n: rule.f(n) for n in range(lo, hi + 1)}


def solve(rule, form, q):
    f = rule.f
    lo, hi = dom(rule)
    if form == 'min_gt':
        return next(n for n in range(max(lo, 1), hi + 1) if f(n) > q['X'])
    if form == 'min_ge':
        return next(n for n in range(max(lo, 1), hi + 1) if f(n) >= q['X'])
    if form == 'max_le':
        return max(f(n) for n in range(max(lo, 1), q['M'] + 1))
    if form == 'min_eq':
        return next(n for n in range(max(lo, 1), hi + 1) if f(n) == q['X'])
    if form == 'max_eq':
        return max(n for n in range(lo, hi + 1) if f(n) == q['X'])
    if form == 'count':
        return len({f(n) for n in range(q['a'], q['b'] + 1)})
    if form == 'count_n':
        return sum(1 for n in range(lo, hi + 1) if f(n) == q['X'])
    raise ValueError(form)


def trap(rule, form, q, ans):
    """Типичная ошибка: (неверный ответ, пояснение) или None. Должен отличаться от ans."""
    f = rule.f
    lo, hi = dom(rule)
    lo = max(lo, 1)
    t = None
    if form == 'min_gt':
        t = (next(n for n in range(lo, hi + 1) if f(n) >= q['X']), "нестрогое неравенство вместо строгого: взяли N, для которого R = %d (а нужно R > %d)" % (q['X'], q['X']))
    elif form == 'min_ge':
        t = (next(n for n in range(lo, hi + 1) if f(n) > q['X']), "строгое неравенство вместо нестрогого: пропустили N, для которого R = %d" % q['X'])
    elif form == 'max_le':
        t = (f(q['M']), "решили, что наибольшее R получается у наибольшего N = %d (R = %d), не проверив остальные N" % (q['M'], f(q['M'])))
    elif form == 'min_eq':
        sols = [n for n in range(lo, min(hi, 3000) + 1) if f(n) == q['X']]
        other = [n for n in sols if n % 2 != sols[0] % 2] if rule.kind != 'F' else []
        if other:
            t = (other[0], "нашли решение только в одной ветке (по чётности N = %d), не проверив другую" % other[0])
        elif len(sols) > 1:
            t = (sols[-1], "взяли не наименьшее из подходящих N")
    elif form == 'max_eq':
        t = (min(n for n in range(lo, hi + 1) if f(n) == q['X']), "взяли наименьшее подходящее N вместо наибольшего")
    elif form == 'count':
        t = (q['b'] - q['a'] + 1, "посчитали количество чисел N (%d), а не количество различных R" % (q['b'] - q['a'] + 1))
    elif form == 'count_n':
        t = (len({f(n) for n in range(lo, hi + 1)}), "посчитали не N с R = %d, а различные R" % q['X']) if False else None
    if t and t[0] != ans:
        return t
    return None


def pick_params(rule, form, rng, level):
    """Подбор числовых параметров: ответ существует, ловушка даёт другой ответ."""
    lo, hi = dom(rule)
    for _ in range(4000):
        if rule.kind == 'F':
            if form in ('min_eq', 'max_eq', 'count_n'):
                n0 = rng.randint(lo, hi)
                q = {'X': rule.f(n0)}
            elif form == 'min_gt':
                n0 = rng.randint(lo, hi)
                q = {'X': rule.f(n0) - rng.choice([0, 1, 2])}
            else:
                continue
        elif form in ('min_gt', 'min_ge'):
            n0 = rng.randint(6 + level * 4, 20 + level * 25)
            q = {'X': rule.f(n0) - (rng.choice([0, 1, 2]) if form == 'min_gt' else rng.choice([0, 0, 1]))}
            if form == 'min_ge':
                q = {'X': rule.f(n0)}
        elif form == 'max_le':
            q = {'M': rng.randint(8 + level * 2, 14 + level * 4)}
        elif form == 'min_eq':
            n0 = rng.randint(5, 40 + level * 40)
            q = {'X': rule.f(n0)}
        elif form == 'count':
            a = rng.randint(1, 6)
            q = {'a': a, 'b': a + rng.randint(9, 13 + level * 3)}
        else:
            continue
        try:
            ans = solve(rule, form, q)
        except StopIteration:
            continue
        if form.startswith('min') and rule.kind != 'F' and ans > 400:
            continue
        tr_ = trap(rule, form, q, ans)
        if tr_ is None and form not in ('count_n', 'min_eq'):
            continue
        return q, ans, tr_
    raise RuntimeError("не удалось подобрать параметры: %s %s" % (rule.kind, form))


def question_text(rule, form, q):
    if rule.kind == 'F':
        t = {'min_eq': "Укажите наименьшее число N, при вводе которого автомат выдаёт число R = %d." % q.get('X', 0),
             'max_eq': "Укажите наибольшее число N, при вводе которого автомат выдаёт число R = %d." % q.get('X', 0),
             'count_n': "Сколько существует чисел N, при вводе которых автомат выдаёт число R = %d?" % q.get('X', 0),
             'min_gt': "Укажите наименьшее число N, при вводе которого автомат выдаёт число R, большее %d." % q.get('X', 0)}[form]
        return t + " В ответе запишите число."
    return {'min_gt': "Укажите минимальное число N, после обработки которого с помощью этого алгоритма получится число R, большее %d. В ответе запишите это число N в десятичной системе счисления." % q.get('X', 0),
            'min_ge': "Укажите минимальное число N, после обработки которого с помощью этого алгоритма получится число R, не меньшее %d. В ответе запишите это число N в десятичной системе счисления." % q.get('X', 0),
            'max_le': "Укажите максимальное число R, которое может получиться в результате работы алгоритма, если N не превосходит %d. В ответе запишите число R в десятичной системе счисления." % q.get('M', 0),
            'min_eq': "Укажите наименьшее число N, при котором в результате работы алгоритма получается R = %d. В ответе запишите число N в десятичной системе счисления." % q.get('X', 0),
            'count': "Сколько различных значений R может получиться, если N — натуральное число от %d до %d включительно? В ответе запишите количество." % (q.get('a', 0), q.get('b', 0))}[form]


def snippet(rule, form, q):
    lo, hi = dom(rule)
    c = rule.code + "\n"
    if rule.kind == 'F':
        rng_ = "range(%d, %d)" % (lo, hi + 1)
        c += {'min_eq': "print(min(n for n in %s if f(n) == %d))" % (rng_, q.get('X', 0)),
              'max_eq': "print(max(n for n in %s if f(n) == %d))" % (rng_, q.get('X', 0)),
              'count_n': "print(sum(1 for n in %s if f(n) == %d))" % (rng_, q.get('X', 0)),
              'min_gt': "print(min(n for n in %s if f(n) > %d))" % (rng_, q.get('X', 0))}[form]
        return c
    c += {'min_gt': "n = 1\nwhile f(n) <= %d:      # пока R не больше X — берём следующее N\n    n += 1\nprint(n)" % q.get('X', 0),
          'min_ge': "n = 1\nwhile f(n) < %d:       # пока R меньше X — берём следующее N\n    n += 1\nprint(n)" % q.get('X', 0),
          'max_le': "print(max(f(n) for n in range(1, %d + 1)))" % q.get('M', 0),
          'min_eq': "n = 1\nwhile f(n) != %d:\n    n += 1\nprint(n)" % q.get('X', 0),
          'count': "print(len({f(n) for n in range(%d, %d + 1)}))      # множество — без повторов" % (q.get('a', 0), q.get('b', 0))}[form]
    return c


def run_snippet(code):
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(code, {})
    return buf.getvalue().strip()


if __name__ == "__main__":
    r = make_rule('A', el='10', er='', ol='1', orr='01')
    print(r.f(12), solve(r, 'max_le', {'M': 12}), solve(r, 'min_gt', {'X': 516}))
    rng = random.Random(1)
    for k, p, fm in [('B', dict(em={'1': '11'}, om={'0': '00'}), 'min_gt'), ('C', dict(side='r', times=2, flip=False), 'min_gt'), ('D', dict(k=3, side='r', times=1), 'min_eq'),
                     ('E', dict(es='r', os_='l', oextra=''), 'count'), ('F', dict(d=4, order='desc'), 'min_eq')]:
        r = make_rule(k, **p)
        q, a, t = pick_params(r, fm, rng, 1)
        print(k, fm, q, a, t)
        assert run_snippet(snippet(r, fm, q)) == str(a)
