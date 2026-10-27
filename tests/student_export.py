"""Выгружает темы из topics.json в простой текст для проверки «учеником» (суб-агентом, который не видел, как писалась тема).
Ответов на вопросы, пояснений и эталонных решений в выгрузке нет — только то, что видит ученик.
Запуск из корня после сборки: py tests/student_export.py файл.txt [название темы ...] (без названий — все темы)."""
import html, json, re, sys

d = json.load(open('topics.json', encoding='utf-8'))
only = set(sys.argv[2:])


def txt(h):
    # код в <pre> не экранирован (в нём бывают < и >), поэтому блоки кода и вывода прячем до удаления тегов
    keep = []

    def hold(text):
        keep.append(text)
        return f'\x00{len(keep) - 1}\x00'
    h = re.sub(r'<pre class="out[^"]*">([\s\S]*?)</pre>', lambda m: hold('\n[ВЫВОД]\n' + html.unescape(m.group(1)) + '\n[/ВЫВОД]\n'), h)
    h = re.sub(r'<pre>([\s\S]*?)</pre>', lambda m: hold('\n[КОД]\n' + m.group(1) + '\n[/КОД]\n'), h)
    h = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', h)
    h = re.sub(r'\[\[([^\]]+)\]\]', r'\1', h)
    h = re.sub(r'<li>', '\n- ', h)
    h = re.sub(r'<h3>', '\n\n## ', h)
    h = re.sub(r'</?p>|</tr>', '\n', h)
    h = re.sub(r'</t[dh]>', ' | ', h)
    h = html.unescape(re.sub(r'<[^>]+>', '', h))
    return re.sub(r'\x00(\d+)\x00', lambda m: keep[int(m.group(1))], h)


o = []
for T in d['topics']:
    if only and T['n'] not in only:
        continue
    o.append(f'# ТЕМА: {T["n"]} ({T["s"]})')
    for it in T['items']:
        if it['t'] == 'theory':
            o.append(f'\n=== ТЕОРИЯ: {it["n"]} ===\n' + txt(it['html']))
            for t in it.get('terms', []):
                o.append(f'[ТЕРМИН — открывается по нажатию на слово «{t["n"]}»]\n{t["d"]}\n')
        elif it['t'] == 'flash':
            o.append(f'\n=== ВОПРОСЫ: {it["n"]} ===')
            for i, q in enumerate(it['q'], 1):
                o.append(f'Вопрос {i}. {q["q"]}' + (f'\n[КОД]\n{q["c"]}\n[/КОД]' if q.get('c') else '')
                         + '\nВарианты: ' + ' | '.join(f'({chr(1072 + k)}) {v}' for k, v in enumerate(q['o'])))
        else:
            o.append(f'\n=== {it["n"].upper()} ===')
            for i, t in enumerate(it.get('tasks', [it]), 1):
                o.append(f'Задача {i}. {t["q"]}\nПример: {t["ex"]}'
                         + (f'\n[В РЕДАКТОРЕ УЖЕ ЕСТЬ КОД]\n{t["starter"]}[/КОД]' if t.get('starter') else '')
                         + f'\n[ПОДСКАЗКА — открывается по кнопке, опыт уменьшается вдвое]\n{t["h"]}\n')
open(sys.argv[1], 'w', encoding='utf-8').write('\n'.join(o))
print('знаков', len('\n'.join(o)))
