from dataclasses import dataclass, field
from enum import Enum


class Kind(Enum):
    WEAPON = "оружие"
    ARMOR = "броня"
    POTION = "зелье"


@dataclass
class Item:
    name: str
    kind: Kind
    power: int

    def __str__(self):
        return f"{self.name} ({self.kind.value}, {self.power})"


def parse_items(text):
    items = []
    for part in text.split(", "):
        if part:
            name, kind, power = part.split(":")
            items.append(Item(name, Kind(kind), int(power)))
    return items


def take(items, name):
    for item in items:
        if item.name == name:
            items.remove(item)
            return item
    return None


@dataclass
class Hero:
    name: str
    hp: int = 20
    max_hp: int = 30
    bag: list = field(default_factory=list)
    weapon: Item = None
    armor: Item = None

    @property
    def attack(self):
        return 3 + (self.weapon.power if self.weapon else 0)

    @property
    def defense(self):
        return self.armor.power if self.armor else 0

    def find(self, name):
        for item in self.bag:
            if item.name == name:
                return item
        return None


def listing(title, items, empty):
    print(title + ", ".join(str(i) for i in items) if items else empty)


def equip(hero, name):
    item = hero.find(name)
    if item is None:
        print(f"В сумке нет {name}")
    elif item.kind == Kind.WEAPON:
        hero.weapon = item
        print(f"В руках: {item.name}")
    elif item.kind == Kind.ARMOR:
        hero.armor = item
        print(f"Надето: {item.name}")
    else:
        print("Это не надеть")


def drink(hero, name):
    item = hero.find(name)
    if item is None:
        print(f"В сумке нет {name}")
    elif item.kind != Kind.POTION:
        print("Это не выпить")
    else:
        hero.hp = min(hero.max_hp, hero.hp + item.power)
        hero.bag.remove(item)
        print(f"Здоровье: {hero.hp}/{hero.max_hp}")


hero = Hero(input())
ground = parse_items(input())
while True:
    parts = input().split(" ", 1)
    cmd = parts[0]
    arg = parts[1] if len(parts) > 1 else ""
    if cmd == "выход":
        print("Игра окончена")
        break
    if cmd == "статус":
        print(f"{hero.name}: здоровье {hero.hp}/{hero.max_hp}, атака {hero.attack}, защита {hero.defense}")
    elif cmd == "осмотреться":
        listing("На земле: ", ground, "На земле пусто")
    elif cmd == "сумка":
        listing("В сумке: ", hero.bag, "Сумка пуста")
    elif cmd == "взять":
        item = take(ground, arg)
        if item is None:
            print(f"Здесь нет {arg}")
        else:
            hero.bag.append(item)
            print(f"Ты взял {item.name}")
    elif cmd == "надеть":
        equip(hero, arg)
    elif cmd == "выпить":
        drink(hero, arg)
    else:
        print(f"Не понимаю: {cmd}")
