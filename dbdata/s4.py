import csv
import json
from datetime import datetime

def read(name):
    with open(name, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        return list(reader)

def when(text):
    return datetime.strptime(text, "%d.%m.%Y %H:%M:%S")

def percent(part, whole):
    if whole == 0:
        return 0.0
    return round(part * 100 / whole, 1)

user_id, class_id = input().split()
person = [r for r in read("user.csv") if r[0] == user_id][0]
link_id = [r[0] for r in read("class_user_link.csv") if r[1] == class_id and r[2] == user_id][0]
titles = {r[0]: r[1] for r in read("test.csv")}
correct_answer = {r[0]: r[2] for r in read("task.csv")}
attempts = {r[1]: r for r in read("test_attempt.csv")}
links = read("test_task_link.csv")
task_rows = read("task_attempt.csv")

given = [r for r in read("test_class_user_link.csv") if r[2] == link_id]
given.sort(key=lambda r: (when(r[3]), int(r[0])), reverse=True)

tests = []
completed = 0
for g in given:
    attempt = attempts.get(g[0])
    if attempt and attempt[2] == "TRUE":
        completed += 1
    answers = {}
    if attempt:
        answers = {r[1]: r for r in task_rows if r[2] == attempt[0]}
    order_list = sorted([r for r in links if r[1] == g[1]], key=lambda r: int(r[3]))
    tasks = []
    answered = right = seconds = 0
    for link in order_list:
        row = answers.get(link[2])
        if row is None or row[3] == "":
            mark = "?"
        else:
            answered += 1
            seconds += int(row[5] or 0)
            mark = "TRUE" if row[3] == correct_answer[link[2]] else "FALSE"
            right += mark == "TRUE"
        tasks.append({"order_number": int(link[3]), "task_id": int(link[2]), "is_correct": mark})
    tests.append({
        "test_id": int(g[1]),
        "title": titles[g[1]],
        "tasks": tasks,
        "progress_percent": percent(answered, len(order_list)),
        "correct_percent": percent(right, answered),
        "time": f"{seconds // 3600:02d}:{seconds % 3600 // 60:02d}:{seconds % 60:02d}",
        "date_assigned": when(g[3]).strftime("%d.%m.%y"),
    })

average = round(sum(t["correct_percent"] for t in tests) / len(tests), 1)
result = {
    "user": {"user_id": int(user_id), "full_name": person[4] + " " + person[2], "class_id": int(class_id)},
    "progress": {"tests_completed": completed, "tests_total": len(tests), "accuracy_average_percent": average},
    "tests": tests,
}
print(json.dumps(result, indent=2, ensure_ascii=False))
