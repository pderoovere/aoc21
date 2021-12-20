from pathlib import Path
import re

input = Path('17/input.txt').read_text().strip('\n')
ranges = [(int(v)) for v in re.findall("[0-9|-]+", input)]

x_min, x_max = ranges[:2]
y_min, y_max = ranges[2:]

def is_hit(x, y):
    return (x_min <= x <= x_max) and (y_min <= y <= y_max)

def should_continue(x, y, xv, yv):
    if (yv < 0 and y < y_min):
        return False
    if (xv == 0 and (x < x_min or x > x_max)):
        return False
    if (xv > 0 and x > x_max):
        return False
    return True

def step(x, y, xv, yv):
    x += xv
    y += yv
    xv += (1 if xv < 0 else -1 if xv > 0 else 0)
    yv -= 1
    return x, y, xv, yv

def simulate(x, y, xv, yv):
    while (should_continue(x, y, xv, yv)):
        x, y, xv, yv = step(x, y, xv, yv)
        if (is_hit(x, y)):
            return True
    return False

count = 0
for xv in range(300):
    for yv in range(-100, 400):
        if simulate(0, 0, xv, yv):
            count += 1

print('Answer', count)