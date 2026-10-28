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


def parse_monsters(text):
    monsters = []
    for part in text.split(", "):
        if part:
            name, hp, attack, defense = part.split(":")
            monsters.append(Creature(name, int(hp), int(attack), int(defense)))
    return monsters


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


hero = Hero(input(), 20, 3)
ground = parse_items(input())
monsters = parse_monsters(input())
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
    elif cmd == "враги":
        print("Враги: " + ", ".join(f"{m.name} ({m.hp})" for m in monsters) if monsters else "Врагов нет")
    elif cmd == "бой":
        monster = take(monsters, arg)
        if monster is None:
            print(f"Здесь нет {arg}")
            continue
        try:
            fight(hero, monster)
        except GameOver:
            print("Ты погиб. Игра окончена")
            break
    else:
        print(f"Не понимаю: {cmd}")
