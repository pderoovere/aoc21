from pathlib import Path

ages = [int(age) for age in Path('06/input.txt').read_text().split(',')]
age_counts = {}
for i in range(9):
    age_counts[i] = ages.count(i)

days = 256
for _ in range(days):
    new_age_counts = {}
    for i in reversed(sorted(age_counts.keys())):
        if i == 0:
            new_age_counts[8] = age_counts[0]
            new_age_counts[6] += age_counts[0]
        else:
            new_age_counts[i-1] = age_counts[i]
    age_counts = new_age_counts.copy()

print('Answer:', sum(age_counts.values()))