import json
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


def parse_item(text):
    name, kind, power = text.split(":")
    return Item(name, Kind(kind), int(power))


def take(items, name):
    for item in items:
        if item.name == name:
            items.remove(item)
            return item
    return None


class GameOver(Exception):
    pass


@dataclass
class Creature:
    name: str
    hp: int
    base_attack: int
    base_defense: int = 0

    @property
    def attack(self):
        return self.base_attack

    @property
    def defense(self):
        return self.base_defense

    @property
    def alive(self):
        return self.hp > 0

    def hit(self, other):
        damage = max(1, self.attack - other.defense)
        other.hp = max(0, other.hp - damage)
        return damage


@dataclass
class Hero(Creature):
    max_hp: int = 30
    bag: list = field(default_factory=list)
    weapon: Item = None
    armor: Item = None

    @property
    def attack(self):
        return self.base_attack + (self.weapon.power if self.weapon else 0)

    @property
    def defense(self):
        return self.base_defense + (self.armor.power if self.armor else 0)

    def find(self, name):
        for item in self.bag:
            if item.name == name:
                return item
        return None


def parse_monster(text):
    name, hp, attack, defense = text.split(":")
    return Creature(name, int(hp), int(attack), int(defense))


@dataclass
class Room:
    desc: str
    exits: dict
    items: list
    monster: Creature = None


def load_dungeon(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    rooms = {}
    for name, r in data["rooms"].items():
        monster = parse_monster(r["monster"]) if r["monster"] else None
        rooms[name] = Room(r["desc"], r["exits"], [parse_item(t) for t in r["items"]], monster)
    return rooms, data["start"], data["goal"]


def look(room):
    print(room.desc)
    print("Выходы: " + ", ".join(room.exits))
    if room.items:
        print("Предметы: " + ", ".join(str(i) for i in room.items))
    if room.monster:
        print(f"Враг: {room.monster.name} ({room.monster.hp})")


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


def fight(hero, monster):
    while True:
        damage = hero.hit(monster)
        print(f"Ты бьёшь: {monster.name} -{damage}, осталось {monster.hp}")
        if not monster.alive:
            print(f"{monster.name} побеждён!")
            return
        damage = monster.hit(hero)
        print(f"{monster.name} бьёт: ты -{damage}, осталось {hero.hp}")
        if not hero.alive:
            raise GameOver


rooms, here, goal = load_dungeon("dungeon.json")
hero = Hero(input(), 20, 3)
look(rooms[here])
while True:
    parts = input().split(" ", 1)
    cmd = parts[0]
    arg = parts[1] if len(parts) > 1 else ""
    room = rooms[here]
    if cmd == "выход":
        print("Игра окончена")
        break
    if cmd == "статус":
        print(f"{hero.name}: здоровье {hero.hp}/{hero.max_hp}, атака {hero.attack}, защита {hero.defense}")
    elif cmd == "осмотреться":
        look(room)
    elif cmd == "идти":
        if room.monster:
            print(f"Путь преграждает {room.monster.name}")
        elif arg not in room.exits:
            print("Туда не пройти")
        else:
            here = room.exits[arg]
            look(rooms[here])
    elif cmd == "сумка":
        print("В сумке: " + ", ".join(str(i) for i in hero.bag) if hero.bag else "Сумка пуста")
    elif cmd == "взять":
        item = take(room.items, arg)
        if item is None:
            print(f"Здесь нет {arg}")
        else:
            hero.bag.append(item)
            print(f"Ты взял {item.name}")
    elif cmd == "надеть":
        equip(hero, arg)
    elif cmd == "выпить":
        drink(hero, arg)
    elif cmd == "бой":
        if room.monster is None:
            print("Здесь не с кем драться")
            continue
        try:
            fight(hero, room.monster)
        except GameOver:
            print("Ты погиб. Игра окончена")
            break
        room.monster = None
        if here == goal:
            print("Сокровища твои! Победа!")
            break
    else:
        print(f"Не понимаю: {cmd}")
