from pathlib import Path
import numpy as np
import re

def parse_step(line):
    global limit_val
    value, ranges = line.split(' ')
    value = 1 if value == 'on' else 0
    ranges = [int(n) for n in re.findall('[-]*[0-9]+', ranges)]
    return value, ranges

def find_limit(steps):
    limit_val = 0
    for _, ranges in steps:
        limit_val = max(limit_val, max([abs(n) for n in ranges]))
    return limit_val

lines = Path('22/input.txt').read_text().strip('\n').split('\n')
steps = [parse_step(line) for line in lines]
limit = 50

result = np.zeros((limit * 2 + 1, limit * 2 + 1, limit * 2 + 1))

def valid_ranges(ranges):
    return all(-limit <= n <= limit for n in ranges)

def convert_ranges(ranges):
    result = []
    for i, n in enumerate(ranges):
        n += limit
        if i % 2 != 0:
            n += 1 # Increase maximum indices 1 more
        result.append(n)
    return result


for value, ranges in steps:
    if valid_ranges(ranges):
        r = convert_ranges(ranges)
        result[r[0]:r[1], r[2]:r[3], r[4]:r[5]] = value

print('Answer', int(np.sum(result)))