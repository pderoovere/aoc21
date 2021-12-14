from functools import partial

operations = {
    'forward': lambda value, aim, h_pos, depth: (aim, h_pos + value, depth + aim * value),
    'down': lambda value, aim, h_pos, depth: (aim + value, h_pos, depth),
    'up': lambda value, aim, h_pos, depth: (aim - value, h_pos, depth)
}

def parse_line(line):
    parts = line.split()
    keyword = parts[0]
    value = int(parts[1])
    return partial(operations[keyword], value)

with open('02/input.txt') as input:
    instructions = [parse_line(line) for line in input.readlines()]
    aim = 0
    h_pos = 0
    depth = 0
    for instruction in instructions:
        aim, h_pos, depth = instruction(aim, h_pos, depth)
    print('Answer:', h_pos * depth)