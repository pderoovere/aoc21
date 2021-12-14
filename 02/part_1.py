from functools import partial

operations = {
    'forward': lambda value, h_pos, depth: (h_pos + value, depth),
    'down': lambda value, h_pos, depth: (h_pos, depth + value),
    'up': lambda value, h_pos, depth: (h_pos, depth - value)
}

def parse_line(line):
    parts = line.split()
    keyword = parts[0]
    value = int(parts[1])
    return partial(operations[keyword], value)

with open('02/input.txt') as input:
    instructions = [parse_line(line) for line in input.readlines()]
    h_pos = 0
    depth = 0
    for instruction in instructions:
        h_pos, depth = instruction(h_pos, depth)
    print('Answer:', h_pos * depth)