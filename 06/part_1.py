from pathlib import Path

ages = [int(age) for age in Path('06/test.txt').read_text().split(',')]

nb_days = 256
for _ in range(nb_days):
    new_state = ages.copy()
    for i, age in enumerate(ages):
        age -= 1
        if age < 0:
            new_state.append(8)
            age = 6
        new_state[i] = age
    ages = new_state

print('Answer:', len(ages))