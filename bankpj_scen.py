S1 = [
'''bank = Bank("Demo Bank", "044452345")
card = bank.apply_for_card("Иванов", "Иван", "1234", "+79161234501", "MIR")
print(card.get_card_info())''',
'''bank = Bank("Demo Bank", "044452345")
data = [
    ("Иванов", "Иван", "1234", "+79161234501", "MIR"),
    ("Петров", "Пётр", "5678", "+79161234502", "VISA"),
    ("Смирнов", "Сергей", "1111", "+79161234505", "MASTERCARD"),
    ("Смирнов", "Сергей", "1111", "+79161234505", "VISA"),
]
for last, first, pin, phone, system in data:
    print(bank.apply_for_card(last, first, pin, phone, system).get_card_info())
print(len(bank.customers), len(bank.accounts), len(bank.cards))''',
'''bank = Bank("Банк Кролика", "044525225")
a = bank.apply_for_card("Заяц", "Захар", "0001", "+70000000001")
b = bank.apply_for_card("Заяц", "Захар", "0001", "+70000000001", "VISA")
c = bank.apply_for_card("Заяц", "Захар", "0001", "+70000000002")
print(a.account.owner is b.account.owner)
print(a.account is b.account)
print(a.account.owner is c.account.owner)
print([card.card_id for card in a.account.owner.cards])
print(list(bank.accounts))
print(a.pan, b.pan, c.pan)
print(c.expiry_date)''',
]
S2 = [
'''bank = Bank("Demo Bank", "044452345")
c1 = bank.apply_for_card("Иванов", "Иван", "1234", "+79161234501", "MIR")
c2 = bank.apply_for_card("Петров", "Пётр", "5678", "+79161234502", "VISA")
print(c1.get_balance())
c1.deposit(500)
c1.pay(120, "5411")
c1.transfer(c2, 80.5)
print(c1.get_balance())
print(c2.get_balance())''',
'''bank = Bank("Demo Bank", "044452345")
c1 = bank.apply_for_card("Иванов", "Иван", "1234", "+79161234501", "MIR")
c2 = bank.apply_for_card("Петров", "Пётр", "5678", "+79161234502", "VISA")
c1.deposit(1000)
c2.deposit(300)
c1.pay(45, "5814")
c1.transfer(c2, 150)
c2.pay(99.9, "5411")
print("История карты 1:")
for row in c1.get_history():
    print(row)
print("История карты 2:")
for row in c2.get_history():
    print(row)''',
'''bank = Bank("Demo Bank", "044452345")
c1 = bank.apply_for_card("Иванов", "Иван", "1234", "+79161234501", "MIR")
c2 = bank.apply_for_card("Петров", "Пётр", "5678", "+79161234502", "VISA")
c1.deposit(700)
c2.deposit(200)
c1.transfer(c2, 100)
user = c1.account.owner
user.change_pin("0000", "9999")
print(user.pin)
user.change_pin("1234", "4321")
print(user.pin)
print(c1.status.value)
c1.close()
print(c1.status.value, c1.status)
print(len(bank.get_global_history()), len(bank.transaction_log))
for row in bank.get_global_history():
    print(row)
print(bank.transaction_log[0].type.name, bank.transaction_log[0].type.value)''',
]
S3 = [
'''bank = Bank("Demo Bank", "044452345")
c1 = bank.apply_for_card("Иванов", "Иван", "1234", "+79161234501", "MIR", card_class=SimpleDebitCard)
c2 = bank.apply_for_card("Петров", "Пётр", "1111", "+79161234502", "MIR", card_class=SimpleDebitCard)
c1.deposit(200)
c1.pay(50, "5411")
c1.transfer(c2, 30)
print(c1.get_balance(), c2.get_balance())
print(type(c1).__name__, isinstance(c1, Card))
for row in c1.get_history() + c2.get_history():
    print(row)''',
'''bank = Bank("Demo Bank", "044452345")
base = bank.apply_for_card("Смирнов", "Андрей", "2222", "+70000000003", "MIR", card_class=CashbackCard)
custom = bank.apply_for_card("Смирнов", "Андрей", "2222", "+70000000004", "MIR", card_class=CashbackCard, cashback_rate=0.07)
base.deposit(300)
custom.deposit(300)
base.pay(120, "5814")
custom.pay(120, "5814")
base.transfer(custom, 50)
print(base.get_balance(), custom.get_balance())
print(base.account.cashback_balance, custom.account.cashback_balance)
print(base.cashback_rate, custom.cashback_rate)
for row in base.get_history() + custom.get_history():
    print(row)''',
'''bank = Bank("Demo Bank", "044452345")
a = bank.apply_for_card("Кузнецов", "Кирилл", "3333", "+70000000004", "MIR", card_class=SavingsCard)
b = bank.apply_for_card("Кузнецов", "Кирилл", "3333", "+70000000005", "VISA", card_class=SavingsCard, interest_rate=0.03)
a.deposit(1000)
b.deposit(1000)
a.accrue_interest()
b.accrue_interest()
a.pay(200, "5411")
print(a.get_balance(), b.get_balance())
print(a.interest_rate, b.interest_rate)
for row in bank.get_global_history():
    print(row)''',
'''bank = Bank("Demo Bank", "044452345")
simple = bank.apply_for_card("Орлов", "Олег", "4444", "+70000000010", "MIR", card_class=SimpleDebitCard)
cb = bank.apply_for_card("Орлов", "Олег", "4444", "+70000000010", "VISA", card_class=CashbackCard, cashback_rate=0.1)
sv = bank.apply_for_card("Орлов", "Олег", "4444", "+70000000010", "MASTERCARD", card_class=SavingsCard)
simple.deposit(1000)
simple.transfer(cb, 400)
cb.pay(250, "5411")
cb.transfer(sv, 100)
sv.accrue_interest()
print(simple.get_balance(), cb.get_balance(), sv.get_balance())
print(cb.account.cashback_balance)
print(simple.account.owner.cards == [simple, cb, sv])
print([type(c).__name__ for c in simple.account.owner.cards])
print(hasattr(simple, "cashback_rate"), hasattr(sv, "accrue_interest"))
print(issubclass(CashbackCard, Card), issubclass(SimpleDebitCard, SavingsCard))''',
]
ATT='''def attempt(action):
    try:
        print("OK:", action())
    except BankError as err:
        print(type(err).__name__ + ":", err)
'''
S4 = [
ATT+'''bank = Bank("Demo Bank", "044452345")
attempt(lambda: bank.apply_for_card("Иванов", "Иван", "12", "+79161234501").pan)
attempt(lambda: bank.apply_for_card("Иванов", "Иван", "12a4", "+79161234501").pan)
attempt(lambda: bank.apply_for_card("Ivanov", "Иван", "1234", "+79161234501").pan)
attempt(lambda: bank.apply_for_card("Иванов", "Иван", "1234", "+79161234501", "AMEX").pan)
card = bank.apply_for_card("Иванов-Петров", "Иван", "1234", "+79161234501")
attempt(lambda: bank.apply_for_card("Сидоров", "Сидор", "1234", "+79161234501").pan)
for system in ("VISA", "MIR", "MASTERCARD"):
    attempt(lambda: bank.apply_for_card("Иванов-Петров", "Иван", "1234", "+79161234501", system).card_id)
print(len(bank.customers), len(bank.accounts), len(bank.cards))''',
ATT+'''bank = Bank("Demo Bank", "044452345")
c1 = bank.apply_for_card("Иванов", "Иван", "1234", "+79161234501")
c2 = bank.apply_for_card("Петров", "Пётр", "5678", "+79161234502")
attempt(lambda: c1.deposit(-5))
attempt(lambda: c1.deposit("100"))
attempt(lambda: c1.deposit(0))
attempt(lambda: c1.deposit(100))
attempt(lambda: c1.get_balance())
attempt(lambda: c1.pay(500, "5411"))
attempt(lambda: c1.pay(10, "54"))
attempt(lambda: c1.pay(10, 5411))
attempt(lambda: c1.pay(10, "7995"))
attempt(lambda: c1.pay(30, "5411"))
attempt(lambda: c1.transfer(c2, 500))
attempt(lambda: c1.transfer(None, 10))
attempt(lambda: c1.transfer(c1, 10))
attempt(lambda: c1.transfer(c2, 10))
attempt(lambda: c2.get_balance())
c2.account = None
attempt(lambda: c1.transfer(c2, 10))
attempt(lambda: c2.get_balance())
print(c1.get_balance())''',
ATT+'''bank = Bank("Demo Bank", "044452345")
c1 = bank.apply_for_card("Иванов", "Иван", "1234", "+79161234501")
c2 = bank.apply_for_card("Петров", "Пётр", "5678", "+79161234502")
attempt(lambda: c1.deposit(500001))
print(c1.status.value)
attempt(lambda: c1.deposit(10))
attempt(lambda: c1.get_card_info())
attempt(lambda: c2.transfer(c1, 10))
c3 = bank.apply_for_card("Орлов", "Олег", "4444", "+70000000010")
c2.deposit(300000)
attempt(lambda: c2.transfer(c3, 100001))
print(c2.status.value)
c1.close()
attempt(lambda: c1.pay(1, "5411"))
c3.deposit(200000)
attempt(lambda: c3.pay(50001, "5411"))
print(c3.status.value, c3.account.balance)''',
ATT+'''bank = Bank("Demo Bank", "044452345")
cb = bank.apply_for_card("Смирнов", "Андрей", "2222", "+70000000003", "MIR", card_class=CashbackCard, cashback_rate=0.07)
sv = bank.apply_for_card("Смирнов", "Андрей", "2222", "+70000000003", "VISA", card_class=SavingsCard)
attempt(lambda: bank.apply_for_card("Смирнов", "Андрей", "2222", "+70000000009", card_class=CashbackCard, cashback_rate=-1).card_id)
attempt(lambda: bank.apply_for_card("Смирнов", "Андрей", "2222", "+70000000009", card_class=CashbackCard, cashback_rate=0.5).card_id)
attempt(lambda: bank.apply_for_card("Смирнов", "Андрей", "2222", "+70000000009", card_class=SavingsCard, interest_rate=0).card_id)
attempt(lambda: bank.apply_for_card("Смирнов", "Андрей", "2222", "+70000000009", card_class=SavingsCard, interest_rate=0.9).card_id)
print(len(bank.customers), len(bank.cards))
cb.deposit(100)
attempt(lambda: cb.pay(40, "5411"))
attempt(lambda: cb.pay(400, "5411"))
print(cb.account.cashback_balance)
sv.deposit(1000)
attempt(lambda: sv.pay(10, "5411"))
attempt(lambda: sv.accrue_interest())
attempt(lambda: sv.transfer(cb, 300))
attempt(lambda: sv.get_balance())
sv.close()
attempt(lambda: sv.accrue_interest())
user = cb.account.owner
attempt(lambda: user.change_pin("2222", "55"))
attempt(lambda: user.change_pin("2222", "55x5"))
attempt(lambda: user.change_pin(2222, "5555"))
attempt(lambda: user.change_pin("0000", "5555"))
attempt(lambda: user.change_pin("2222", "5555"))
print(user.pin)
for row in bank.get_global_history():
    print(row)''',
]

S5 = [
"""apply Иванов Иван 1234 +79161234501 MIR
apply Петров Пётр 5678 +79161234502 VISA cashback
apply Сидоров Сидор 0000 +79161234503 MASTERCARD savings
deposit 1 1000
pay 2 100 5411
transfer 1 2 300
pay 2 100 5411
balance 2
deposit 3 500
accrue 3
history 2
info 3
exit
deposit 1 99999""",
"""apply Заяц Захар 1111 +70000000001 MIR
apply Заяц Захар 1111 +70000000001 VISA
deposit 1 abc
deposit 7 100
deposit 1 -50
pay 1 10 54
pay 1 10 7995
pay 1 10 5411
transfer 1 1 5
transfer 1 9 5
fly 1 2 3
apply Волк 1234 +70000000002
apply Wolf Wolfgang 1234 +70000000002 MIR
apply Волков Валерий 1234 +70000000001 MIR
apply Заяц Захар 1111 +70000000001 MIR cashback
apply Заяц Захар 1111 +70000000001 MIR savings
apply Заяц Захар 1111 +70000000001 MIR simple
accrue 1
pin 1 1111 22
pin 1 0000 2222
pin 1 1111 2222
close 1
balance 1
history 1""",
"""apply Кроликов Роман 4321 +70000000005 VISA cashback
deposit 1 250.5
pay 1 50.5 5814
history 1
close 1
exit""",
]
