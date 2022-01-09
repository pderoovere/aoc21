from pathlib import Path

lines = Path('25/input.txt').read_text().strip('\n').split('\n')

hor = set()
vert = set()
vert_len = len(lines)
hor_len = len(lines[0])

for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == 'v':
            vert.add((i, j))
        elif c == '>':
            hor.add((i, j))

def print_state():
    for i in range(vert_len):
        for j in range(hor_len):
            if (i, j) in hor:
                print('>', end='')
            elif (i, j) in vert:
                print('v', end='')
            else:
                print('.', end='')
        print('')

def step(hor, vert):
    new_hor = set()
    did_move = False
    for (i, j) in hor:
        new_j = (j + 1) % hor_len
        if (i, new_j) in hor or (i, new_j) in vert:
            new_hor.add((i, j))
        else:
            new_hor.add((i, new_j))
            did_move = True
    new_vert = set()
    for (i, j) in vert:
        new_i = (i + 1) % vert_len
        if (new_i, j) in new_hor or (new_i, j) in vert:
            new_vert.add((i, j))
        else:
            new_vert.add((new_i, j))
            did_move = True
    return new_hor, new_vert, did_move


did_move = True
count = 0
while did_move:
    hor, vert, did_move = step(hor, vert)
    count += 1

print('Count', count)