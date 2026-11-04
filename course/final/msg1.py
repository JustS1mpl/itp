from dataclasses import dataclass


@dataclass
class Message:
    id: int
    author: str
    text: str

    def __str__(self):
        return f"[{self.id}] {self.author}: {self.text}"


def parse_command(line):
    if line.startswith("/"):
        parts = line[1:].split(" ", 1)
        return parts[0], parts[1].strip() if len(parts) > 1 else ""
    return "", line.strip()


nick = "гость"
messages = []
while True:
    cmd, arg = parse_command(input())
    if cmd == "":
        if arg:
            msg = Message(len(messages) + 1, nick, arg)
            messages.append(msg)
            print(msg)
    elif cmd == "ник":
        if arg:
            nick = arg
            print(f"Теперь ты {nick}")
        else:
            print("Ник не может быть пустым")
    elif cmd == "история":
        if not messages:
            print("Сообщений нет")
        for msg in messages:
            print(msg)
    elif cmd == "выход":
        print(f"Пока, {nick}!")
        break
    else:
        print(f"Неизвестная команда: /{cmd}")
