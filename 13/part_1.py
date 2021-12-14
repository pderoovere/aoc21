from pathlib import Path
import numpy as np

input = Path('13/input.txt').read_text()
s_coordinates, s_folds = input.split('\n\n')[:2]

width, height = 0, 0
coordinates = []
for c in s_coordinates.split('\n'):
    c = c.split(',')
    x, y = int(c[0]), int(c[1])
    coordinates.append((x, y))
    width = max(x + 1, width)
    height = max(y + 1, height)

paper = np.zeros((height, width))
for x, y in coordinates:
    paper[y, x] = 1

def create_part(orig, shape, pad_before):
    orig_h, orig_w = orig.shape
    h, w = shape
    result = np.zeros(shape)
    x_start = 0
    y_start = 0
    if pad_before:
        x_start = w - orig_w
        y_start = h - orig_h
    result[x_start:x_start+orig_h, y_start:y_start+orig_w] = orig
    return result

def fold(paper, axis, location):
    height, width = paper.shape
    if axis == 'x':
        new_width = max(location, width - location - 1)
        part1 = create_part(paper[:, :location], (height, new_width), True)
        part2 = create_part(paper[:, location+1:], (height, new_width), False)
        part2 = np.flip(part2, axis=1)
        return part1 + part2
    elif axis == 'y':
        new_height = max(location, height - location - 1)
        part1 = create_part(paper[:location, :], (new_height, width), True)
        part2 = create_part(paper[location+1:, :], (new_height, width), False)
        part2 = np.flip(part2, axis=0)
        return part1 + part2

for f in s_folds.split('\n'):
    f = f.strip('fold along ').split('=')
    axis = f[0]
    location = int(f[1])
    paper = fold(paper, axis, location)
    break

paper = np.clip(paper, 0, 1)

print('Answer:', int(np.sum(paper)))