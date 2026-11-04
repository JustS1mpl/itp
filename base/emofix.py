"""Чистка встроенных смайликов (assets/emoji_pack.b64) перед встраиванием, U2-6.

Смайлики в пакете — объёмные SVG, у которых при упаковке пропали фильтры (внутренние тени). Без них
мелкие «подкрашивающие» слои по краям фигуры — та же форма ещё раз, залитая крошечным радиальным
градиентом, который тут же уходит в прозрачность (тёмная капля на кончике луча звезды, рыжая у ножки) —
видны как грязные пятна. Убираем именно такие слои: путь повторяет уже нарисованную форму, градиент
радиальный, радиус не больше RMAX единиц из 32 и последний цвет прозрачный. Основные заливки, блики глаз
и прочие детали (у них свои формы) не трогаются. Неиспользуемые после этого градиенты тоже удаляются.
"""
import re

RMAX = 4.5
_RG = re.compile(r'<radialGradient id="([^"]+)"[^>]*>.*?</radialGradient>', re.S)
_PATH = re.compile(r'<path d="([^"]+)"([^>]*)/>')


def _tiny(g):
    m = re.search(r'scale\(([\d.]+)(?:[ ,]+([\d.]+))?\)', g)
    if not m or 'stop-opacity="0"' not in g:
        return False
    return max(float(m.group(1)), float(m.group(2) or m.group(1))) <= RMAX


def emo_svg(v):
    """Вернуть (svg, сколько слоёв убрано)."""
    grads = {m.group(1): m.group(0) for m in _RG.finditer(v)}
    seen, out, n, pos = set(), [], 0, 0
    for m in _PATH.finditer(v):
        d, rest = m.group(1), m.group(2)
        f = re.search(r'fill="url\(#([^)]+)\)"', rest)
        drop = d in seen and f and f.group(1) in grads and _tiny(grads[f.group(1)])
        seen.add(d)
        if drop:
            out.append(v[pos:m.start()])
            pos = m.end()
            n += 1
    out.append(v[pos:])
    v = ''.join(out)
    if n:
        for gid, g in grads.items():
            if 'url(#%s)' % gid not in v:
                v = v.replace(g, '')
    return v, n


def emo_clean(pack):
    """pack: {код: svg}. Возвращает (чистый пакет, (слоёв, смайликов))."""
    tot = ems = 0
    for k in list(pack):
        pack[k], n = emo_svg(pack[k])
        if n:
            tot += n
            ems += 1
    return pack, (tot, ems)
