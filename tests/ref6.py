# Независимый эталон №6 (порт решения из комплекта ege_task06)
from math import cos, sin, radians, gcd

def flat(prog):
    for c in prog:
        if c[0] == 'rep':
            for _ in range(c[1]):
                yield from flat(c[2])
        else:
            yield c

def lines_of(prog):
    x, y, ang, down = 0.0, 0.0, 90, True
    lines = [[(x, y)]]
    for c in flat(prog):
        if c[0] == 'F':
            x += c[1] * cos(radians(ang)); y += c[1] * sin(radians(ang))
            if down: lines[-1].append((x, y))
        elif c[0] == 'R': ang -= c[1]
        elif c[0] == 'L': ang += c[1]
        elif c[0] == 'up': down = False
        else:
            down = True; lines.append([(x, y)])
    return lines

def polygon(line):
    for i in range(1, len(line)):
        if abs(line[i][0] - line[0][0]) < 1e-7 and abs(line[i][1] - line[0][1]) < 1e-7:
            return line[:i]

def on_edge(px, py, poly):
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
        dx, dy = x2 - x1, y2 - y1
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
        if (px - x1 - t * dx) ** 2 + (py - y1 - t * dy) ** 2 < 1e-12: return True
    return False

def inside(px, py, poly):
    res = False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
        if (y1 > py) != (y2 > py) and px < x1 + (py - y1) * (x2 - x1) / (y2 - y1): res = not res
    return res

def solve(Q):
    k = Q['kind']; f = Q['form']
    if k == 'T':
        polys = [polygon(l) for l in lines_of(Q['prog']) if len(l) > 2]
        strict = f.endswith('strict') or f == 'strict'
        mem = (lambda X, Y, p: inside(X, Y, p) and not on_edge(X, Y, p)) if strict else (lambda X, Y, p: inside(X, Y, p) or on_edge(X, Y, p))
        agg = any if f.startswith('union') else all
        return sum(1 for X in range(-80, 81) for Y in range(-80, 81) if agg(mem(X, Y, p) for p in (polys if f[0] in 'ui' else polys[:1])))
    if k == 'R':
        L = lines_of(Q['prog'])
        def box(line):
            xs = [round(p[0]) for p in line]; ys = [round(p[1]) for p in line]
            return min(xs), max(xs), min(ys), max(ys)
        (a1, b1, c1, d1), (a2, b2, c2, d2) = box(L[0]), box(L[1])
        w = min(b1, b2) - max(a1, a2); h = min(d1, d2) - max(c1, c2)
        return 2 * (w + h) if f == 'perim' else w * h
    moves, kk = Q['moves'], Q['k']
    if f == 'traj':
        x = y = 0; pts = {(0, 0)}
        for _ in range(kk):
            for a, b in moves:
                g = gcd(abs(a), abs(b))
                for t in range(1, g + 1): pts.add((x + a * t // g, y + b * t // g))
                x, y = x + a, y + b
        return len(pts)
    P = [(0, 0)]; x = y = 0
    for a, b in moves[:-1]:
        x += a; y += b; P.append((x, y))
    S2 = abs(sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P))))
    B = sum(gcd(abs(a), abs(b)) for a, b in moves)
    return (S2 - B + 2) // 2

if __name__ == '__main__':
    import json
    cs = json.load(open('t6_cases.json')); bad = 0
    for c in cs:
        # конвертируем списки в формат (кортежи не нужны)
        r = solve(c['query'])
        if str(r) != c['a']:
            bad += 1; print('BAD', c['type'], c['query'], r, c['a'])
    print('cases', len(cs), 'bad', bad)
