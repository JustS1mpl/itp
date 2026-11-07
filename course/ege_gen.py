"""ЕГЭ по информатике (7.3.0): три норы из материалов course/ege/NN.md и задачи тренажёра из course/ege/practice.json.

Материалы собраны отдельно (банк КомпЕГЭ, демоверсии ФИПИ), код решений проверен на файлах демоверсии.
Каждый номер — своя глава: два островка теории («Как устроено» и «Решаем кодом»). Первый островок любой главы открыт
сразу (правило в v5/a_ege.js), а после его прочтения задачи этого номера появляются в «Практике» (бесконечный режим).
Задачи тренажёра лежат в поле pr первого островка главы.
"""
import html, json, os, re

from dsl import th, topic

HERE = os.path.dirname(os.path.abspath(__file__))
B = chr(92)


def esc(s):
    return html.escape(s, quote=False)


def inline(s):
    """Строка Markdown → HTML: `код`, **жирный**, *курсив*, ссылки, формулы \\( \\)."""
    parts = re.split(r'(`[^`]+`)', s)
    out = []
    for p in parts:
        if p.startswith('`') and p.endswith('`') and len(p) > 1:
            out.append('<code>' + esc(p[1:-1]) + '</code>')
            continue
        p = latex_inline(p)
        p = esc(p)
        p = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)\)', lambda m: '<img class="egi" src="' + fix_img(m.group(2)) + '" alt="' + m.group(1) + '" loading="lazy">', p)
        p = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', r'<a href="\2" class="egl" target="_blank" rel="noopener">\1</a>', p)
        p = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', p)
        p = re.sub(r'(?<![*\w])\*([^*\n]+)\*(?![*\w])', r'<i>\1</i>', p)
        out.append(p)
    return ''.join(out)


def fix_img(u):
    # в части задач картинка встроена (data:), но к ней приклеен адрес сайта
    i = u.find('data:image')
    return u[i:] if i >= 0 else u


TEX = {'neg': '¬', 'to': '→', 'rightarrow': '→', 'lor': '∨', 'vee': '∨', 'land': '∧', 'wedge': '∧', 'times': '×',
       'cdot': '·', 'leq': '≤', 'le': '≤', 'geq': '≥', 'ge': '≥', 'in': '∈', 'equiv': '≡', 'neq': '≠', 'ne': '≠',
       'lt': '<', 'gt': '>', 'quad': ' ', ',': ' ', ' ': ' ', 'ldots': '…', 'dots': '…', 'notin': '∉', 'mid': '|',
       'oplus': '⊕', 'pm': '±', 'infty': '∞', 'left': '', 'right': '', 'vec': '', 'displaystyle': ''}


def group(s, i):
    """Аргумент команды: {…} или один символ. Возвращает (текст, позиция после)."""
    while i < len(s) and s[i] == ' ':
        i += 1
    if i < len(s) and s[i] == '{':
        d, j = 1, i + 1
        while j < len(s) and d:
            d += {'{': 1, '}': -1}.get(s[j], 0)
            j += 1
        return s[i + 1:j - 1], j
    return s[i:i + 1], i + 1


SUP = str.maketrans('0123456789+-=()nk', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿᵏ')
SUB = str.maketrans('0123456789+-=()', '₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎')


def tex(s):
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == B:
            m = re.match(r'\\([a-zA-Z]+|.)', s[i:])
            cmd, i = m.group(1), i + len(m.group(0))
            if cmd in ('sqrt',):
                a, i = group(s, i)
                a = tex(a)
                out.append('√' + (a if len(a) == 1 else '(' + a + ')'))
            elif cmd == 'frac':
                a, i = group(s, i)
                b, i = group(s, i)
                out.append('(' + tex(a) + ')/(' + tex(b) + ')')
            elif cmd in ('text', 'textit', 'textbf', 'mathrm', 'mathit', 'operatorname', 'mbox'):
                a, i = group(s, i)
                out.append(tex(a))
            elif cmd in ('{', '}', '%', '_', '&', '#', '$'):
                out.append(cmd)
            else:
                out.append(TEX.get(cmd, cmd))
        elif c in '^_':
            a, i = group(s, i + 1)
            a = tex(a)
            t = a.translate(SUP if c == '^' else SUB)
            if all(ch in '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿᵏ₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎' for ch in t):
                out.append(t)
            else:
                out.append(('^' if c == '^' else '_') + ('(' + a + ')' if len(a) > 1 else a))
        elif c in '{}':
            i += 1
        else:
            out.append(c)
            i += 1
    return re.sub(r' {2,}', ' ', ''.join(out)).strip()


def latex_inline(s):
    return re.sub(re.escape(B + '(') + r'([\s\S]+?)' + re.escape(B + ')'), lambda m: tex(m.group(1)), s)


def md(text):
    """Markdown глав и условий → HTML курса: заголовки h3, абзацы, списки, таблицы, блоки кода, картинки."""
    lines = text.replace('\r', '').split('\n')
    out, i, para = [], 0, []

    def flush():
        if para:
            out.append('<p>' + inline(' '.join(para)) + '</p>')
            para.clear()

    while i < len(lines):
        ln = lines[i]
        if ln.startswith('```'):
            flush()
            j = i + 1
            code = []
            while j < len(lines) and not lines[j].startswith('```'):
                code.append(lines[j])
                j += 1
            out.append('<pre>' + esc('\n'.join(code).rstrip('\n')) + '</pre>')
            i = j + 1
            continue
        if re.match(r'^#{2,4} ', ln):
            flush()
            out.append('<h3>' + inline(ln.lstrip('#').strip()) + '</h3>')
        elif ln.startswith('|'):
            flush()
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append(lines[i])
                i += 1
            cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows if not re.match(r'^\|[\s:|-]+\|?$', r.strip())]
            h = '<table><thead><tr>' + ''.join('<th>' + inline(c) + '</th>' for c in cells[0]) + '</tr></thead><tbody>'
            h += ''.join('<tr>' + ''.join('<td>' + inline(c) + '</td>' for c in r) + '</tr>' for r in cells[1:]) + '</tbody></table>'
            out.append('<div class="tw">' + h + '</div>')
            continue
        elif re.match(r'^\s*([-*]|\d+\.) ', ln):
            flush()
            tag = 'ol' if re.match(r'^\s*\d+\. ', ln) else 'ul'
            items = []
            while i < len(lines) and (re.match(r'^\s*([-*]|\d+\.) ', lines[i]) or (lines[i].startswith('  ') and items)):
                if re.match(r'^\s*([-*]|\d+\.) ', lines[i]):
                    items.append(re.sub(r'^\s*([-*]|\d+\.) ', '', lines[i]))
                else:
                    items[-1] += ' ' + lines[i].strip()
                i += 1
            out.append('<' + tag + '>' + ''.join('<li>' + inline(x) + '</li>' for x in items) + '</' + tag + '>')
            continue
        elif ln.startswith('> '):
            flush()
            out.append('<p class="egq">' + inline(ln[2:]) + '</p>')
        elif not ln.strip():
            flush()
        else:
            para.append(ln.strip())
        i += 1
    flush()
    return ''.join(out)


def sections(n):
    """Глава NN.md: название и разделы «## …» по порядку."""
    t = open(os.path.join(HERE, 'ege', '%02d.md' % n), encoding='utf-8').read()
    m = re.match(r'# Задание №(\d+) — «(.+)»', t)
    title = m.group(2)
    body = t[m.end():]
    secs = re.split(r'\n(?=## )', body)
    head, rest = secs[0], secs[1:]
    # служебные строки шапки (нора, баллы, что нужно из курса) — для черновика; на экзамене балл и время полезны
    keep = [l for l in head.strip().split('\n') if l.strip() and not l.startswith('Что нужно из курса')]
    keep = [re.sub(r'^Нора: \*\*[^*]+\*\* · ', '', l) for l in keep]
    keep = [l[0].upper() + l[1:] if l else l for l in keep]
    return title, keep, rest


def chapter(n):
    title, head, secs = sections(n)
    one, two = [], []
    for s in secs:
        name = s.split('\n', 1)[0][3:]
        (two if re.match(r'(Решение 2|Вариации|Ловушки)', name) else one).append(s)
    lead = '<p class="mu">' + '<br>'.join(inline(l) for l in head) + '</p>' if head else ''
    a = th('№%d: как устроено' % n, [], lead + md('\n'.join(one)))
    b = th('№%d: решаем кодом' % n, [], md('\n'.join(two)))
    a['ch'] = n
    b['ch'] = n
    a['cht'] = title
    a['pr'] = practice(n)
    return [a, b]


_P = None


def practice(n):
    global _P
    if _P is None:
        _P = json.load(open(os.path.join(HERE, 'ege', 'practice.json'), encoding='utf-8'))
    out = []
    for x in _P:
        if x['task'] != n:
            continue
        d = {'id': x['num'], 'src': x['source'], 'h': md(x['statement_md']), 'a': str(x['answer']).strip(), 'u': x['url'], 'tu': x['tutor']}
        if x.get('subtype') and x['subtype'] != 'основной':
            d['st'] = x['subtype']
        if x['files']:
            d['f'] = [[f['name'], f['url']] for f in x['files']]
        out.append(d)
    assert out, n
    return out


def hole(name, s, nums, after=None):
    items = []
    for n in nums:
        items += chapter(n)
    return topic(name, s, items, opt=True, after=after)
