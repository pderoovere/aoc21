from pathlib import Path
import math
import sys

sys.setrecursionlimit(10_000)

lines = Path('18/input.txt').read_text().strip('\n').split('\n')

def parse_line(line):
    result = []
    buffer = ''
    for c in line:
        if c.isdigit():
            buffer += c
        else:
            if len(buffer) > 0:
                result.append(int(buffer))
                buffer = ''
            result.append(c)
    return result

pairs = [parse_line(line) for line in lines]

def to_str(pair):
    return ''.join([str(c) for c in pair])

def add_left(seq, number):
    seq_lenth = len(seq)
    for i in range(seq_lenth):
        idx = seq_lenth - 1 - i
        if isinstance(seq[idx], int):
            seq[idx] += number
            break
    return seq

def add_right(seq, number):
    for i in range(len(seq)):
        if isinstance(seq[i], int):
            seq[i] += number
            break
    return seq

def explode_at(pair, i):
    left_side = pair[:i-1] # Without the number at i and the '[' before
    n_1 = pair[i]
    right_side = pair[i+4:] # Without the ',', number and ']' after i
    n_2 = pair[i+2]
    left_side = add_left(left_side, n_1)
    right_side = add_right(right_side, n_2)
    return reduce(left_side + [0] + right_side)

def split_at(pair, i):
    left_side = pair[:i]
    right_side = pair[i+1:]
    n = pair[i]
    return reduce(left_side + ['[', math.floor(n/2), ',', math.ceil(n/2), ']'] + right_side)

def process(pair, condition, operation):
    nesting_level = 0
    for i, c in enumerate(pair):
        if c == '[':
            nesting_level += 1
        elif c == ']':
            nesting_level -= 1
        elif isinstance(c, int) and condition(nesting_level, pair, i):
            return operation(pair, i)
    return pair

def no_sublevels(nesting_level, pair, i):
    return i < len(pair) - 3 and pair[i+1] == ',' and isinstance(pair[i+2], int)

def should_explode(nesting_level, pair, i):
    return nesting_level >= 5 and pair[i+1] == ','

def should_split(nesting_level, pair, i):
    return pair[i] >= 10

def reduce(pair):
    pair = process(pair, should_explode, explode_at)
    pair = process(pair, should_split, split_at)
    return pair

def add(pair_1, pair_2):
    result = reduce(['['] + pair_1 + [','] + pair_2 + [']'])
    return result

def magnitude_at(pair, i):
    left_side = pair[:i-1] # Without the number at i and the '[' before
    n_left = pair[i]
    right_side = pair[i+4:] # Without the ',', number and ']' after i
    n_right = pair[i+2]
    return magnitude(left_side + [(3*n_left + 2*n_right)] + right_side)

def magnitude(pair):
    return process(pair, no_sublevels, magnitude_at)

result = pairs[0]
for pair in pairs[1:]:
    result = add(result, pair)

m = magnitude(result)

print('Answer:', m)