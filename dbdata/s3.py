import csv
from datetime import datetime

def read(name):
    with open(name, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        return list(reader)

def when(text):
    return datetime.strptime(text, "%d.%m.%Y %H:%M:%S")

def percent(part, whole):
    return round(part * 100 / whole, 1)

user_id, class_id = input().split()
link_id = [r[0] for r in read("class_user_link.csv") if r[1] == class_id and r[2] == user_id][0]
given = [r for r in read("test_class_user_link.csv") if r[2] == link_id]
last = max(given, key=lambda r: (when(r[3]), int(r[0])))
attempt_id = [r[0] for r in read("test_attempt.csv") if r[1] == last[0]][0]
tasks = sorted([r for r in read("test_task_link.csv") if r[1] == last[1]], key=lambda r: int(r[3]))
correct_answer = {r[0]: r[2] for r in read("task.csv")}
answers = {r[1]: r for r in read("task_attempt.csv") if r[2] == attempt_id}

answered = 0
right = 0
seconds = 0
lines = []
for link in tasks:
    order, task_id = link[3], link[2]
    row = answers.get(task_id)
    if row is None or row[3] == "":
        lines.append(f"{order} ? {task_id}")
        continue
    answered += 1
    seconds += int(row[5] or 0)
    ok = row[3] == correct_answer[task_id]
    right += ok
    lines.append(f"{order} {'TRUE' if ok else 'FALSE'} {task_id}")

print(f"{percent(answered, len(tasks)):.1f}% {percent(right, answered):.1f}%")
for line in lines:
    print(line)
print(f"{seconds // 3600:02d}:{seconds % 3600 // 60:02d}:{seconds % 60:02d}")
