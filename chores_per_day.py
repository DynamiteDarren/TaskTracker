import os 
from rainbow_habit_tracker import read_entries

dir_path = os.path.dirname(os.path.realpath(__file__))

files = os.listdir()
chore_files = []

for file in files:
    if file.endswith('.txt'):
        chore_files.append(file)
print("Chore files: {0}".format(chore_files))
count = 0
for file_name in chore_files:
    file = open(file_name, "r")

    lines = file.readlines()
    entries = read_entries(lines)
    for e in entries:
        count += e[1]


print("total: " + str(count))

days = 30

per_day = count / days

print("Per day: {0}".format(per_day))

