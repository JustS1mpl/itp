from collections import Counter
from dataclasses import dataclass
from enum import Enum

import requests

BASE = "http://chat.itp/messages"


class Kind(Enum):
    TEXT = "TEXT"
    SYSTEM = "SYSTEM"


@dataclass
class Message:
    id: int
    author: str
    text: str
    kind: Kind = Kind.TEXT

    def __str__(self):
        if self.kind == Kind.SYSTEM:
            return f"[{self.id}] * {self.text}"
        return f"[{self.id}] {self.author}: {self.text}"


class ChatError(Exception):
    pass


def parse_command(line):
    if line.startswith("/"):
        parts = line[1:].split(" ", 1)
        return parts[0], parts[1].strip() if len(parts) > 1 else ""
    return "", line.strip()


def stats(messages):
    counts = Counter(m.author for m in messages if m.kind == Kind.TEXT)
    return sorted(counts.items(), key=lambda p: (-p[1], p[0]))


def to_message(d):
    return Message(d["id"], d["author"], d["text"], Kind(d["kind"]))


def load():
    return [to_message(d) for d in requests.get(BASE).json()]


def post(author, text, kind=Kind.TEXT):
    msg = to_message(requests.post(BASE, json={"author": author, "text": text, "kind": kind.value}).json())
    print(msg)
    return msg


def show(found, empty):
    if not found:
        print(empty)
    for msg in found:
        print(msg)


def delete(arg):
    if not arg.isdigit():
        raise ChatError("Укажи номер сообщения")
    r = requests.get(f"{BASE}/{arg}")
    if r.status_code == 404:
        raise ChatError(f"Нет сообщения {arg}")
    if r.json()["author"] != nick:
        raise ChatError("Можно удалять только свои сообщения")
    requests.delete(f"{BASE}/{arg}")
    print(f"Сообщение {arg} удалено")


def handle(line):
    global nick, seen
    cmd, arg = parse_command(line)
    if cmd == "":
        if arg:
            seen = max(seen, post(nick, arg).id)
    elif cmd == "ник":
        if not arg:
            raise ChatError("Ник не может быть пустым")
        seen = max(seen, post("*", f"{nick} теперь {arg}", Kind.SYSTEM).id)
        nick = arg
    elif cmd == "обновить":
        new = [m for m in load() if m.id > seen]
        show(new, "Новых сообщений нет")
        seen = max([seen] + [m.id for m in new])
    elif cmd == "история":
        show(load(), "Сообщений нет")
    elif cmd == "найти":
        word = arg.lower()
        show([m for m in load() if m.kind == Kind.TEXT and word in m.text.lower()], "Ничего не найдено")
    elif cmd == "упоминания":
        tag = "@" + nick.lower()
        show([m for m in load() if m.kind == Kind.TEXT and tag in m.text.lower()], "Тебя не упоминали")
    elif cmd == "стат":
        rows = stats(load())
        if not rows:
            print("Сообщений нет")
        for author, count in rows:
            print(f"{author}: {count}")
    elif cmd == "удалить":
        delete(arg)
    elif cmd == "выход":
        print(f"Пока, {nick}!")
        return False
    else:
        raise ChatError(f"Неизвестная команда: /{cmd}")
    return True


nick = "гость"
seen = 0
print("Подключено к серверу")
while True:
    try:
        if not handle(input()):
            break
    except ChatError as e:
        print(e)
