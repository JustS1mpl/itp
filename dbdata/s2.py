import csv
from datetime import datetime

def read(name):
    with open(name, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        return list(reader)

user_id, class_id = input().split()
links = read("class_user_link.csv")
link_id = [r[0] for r in links if r[1] == class_id and r[2] == user_id][0]
titles = {r[0]: r[1] for r in read("test.csv")}
finished = {r[1]: r[2] for r in read("test_attempt.csv")}
given = [r for r in read("test_class_user_link.csv") if r[2] == link_id]
given.sort(key=lambda r: (datetime.strptime(r[3], "%d.%m.%Y %H:%M:%S"), int(r[0])), reverse=True)
done = sum(1 for r in given if finished.get(r[0]) == "TRUE")
print(f"{done}/{len(given)}")
for r in given:
    date = datetime.strptime(r[3], "%d.%m.%Y %H:%M:%S").strftime("%d.%m.%y")
    print(titles[r[1]], date, finished.get(r[0]) == "TRUE" and "TRUE" or "FALSE")
