import importlib, json, os


def build():
    # Темы идут в порядке curriculum.json: модуль темы называется c_<id>.py, модуль норы — c_h_<id>.py.
    # Нора встаёт сразу за темой, к которой привязана (поле after в curriculum.json).
    # Темы, которые ещё не написаны (нет файла), пропускаются.
    cur = json.load(open('curriculum.json', encoding='utf-8'))
    out = []
    for t in cur['topics']:
        if os.path.exists('c_%s.py' % t['id']):
            out.append(importlib.import_module('c_' + t['id']).build())
            for h in cur['holes']:
                if h['after'] == t['id'] and os.path.exists('c_h_%s.py' % h['id']):
                    out.append(importlib.import_module('c_h_' + h['id']).build())
    return out
