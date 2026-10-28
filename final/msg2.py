from collections import Counter
from dataclasses import dataclass
from enum import Enum


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


def parse_command(line):
    if line.startswith("/"):
        parts = line[1:].split(" ", 1)
        return parts[0], parts[1].strip() if len(parts) > 1 else ""
    return "", line.strip()


def stats(messages):
    counts = Counter(m.author for m in messages if m.kind == Kind.TEXT)
    return sorted(counts.items(), key=lambda p: (-p[1], p[0]))


def post(author, text, kind=Kind.TEXT):
    msg = Message(len(messages) + 1, author, text, kind)
    messages.append(msg)
    print(msg)


def show(found, empty):
    if not found:
        print(empty)
    for msg in found:
        print(msg)


nick = "гость"
messages = []
while True:
    cmd, arg = parse_command(input())
    if cmd == "":
        if arg:
            post(nick, arg)
    elif cmd == "ник":
        if arg:
            post("*", f"{nick} теперь {arg}", Kind.SYSTEM)
            nick = arg
        else:
            print("Ник не может быть пустым")
    elif cmd == "история":
        show(messages, "Сообщений нет")
    elif cmd == "найти":
        word = arg.lower()
        show([m for m in messages if m.kind == Kind.TEXT and word in m.text.lower()], "Ничего не найдено")
    elif cmd == "упоминания":
        tag = "@" + nick.lower()
        show([m for m in messages if m.kind == Kind.TEXT and tag in m.text.lower()], "Тебя не упоминали")
    elif cmd == "стат":
        rows = stats(messages)
        if not rows:
            print("Сообщений нет")
        for author, count in rows:
            print(f"{author}: {count}")
    elif cmd == "выход":
        print(f"Пока, {nick}!")
        break
    else:
        print(f"Неизвестная команда: /{cmd}")
