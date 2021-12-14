import numpy as np

def line_coordinates(start, end):
    x = start[0]
    y = start[1]
    yield x, y
    while x != end[0] or y != end[1]:
        if x < end[0]:
            x += 1
        elif x > end[0]:
            x -= 1
        if y < end[1]:
            y += 1
        elif y > end[1]:
            y -= 1
        yield x, y

def add_line(diagram, start, end): 
    """Adds the line (`c1` -> `c2`) to `diagram`, increasing its size if needed."""
    max_x = max(start[0], end[0], diagram.shape[1])
    max_y = max(start[1], end[1], diagram.shape[0])
    result = np.zeros((max_y + 1, max_x + 1))
    result[0:diagram.shape[0], 0:diagram.shape[1]] = diagram
    for x, y in line_coordinates(start, end):
        result[y, x] += 1
    return result

def is_horizontal(start, end):
    return start[1] == end[1]

def is_vertical(start, end):
    return start[0] == end[0]

def count_overlaps(diagram):
    return (diagram > 1).sum()

with open('05/input.txt') as input:
    diagram = np.zeros((1, 1))
    for line in input.readlines():
        coordinates = [[int(value) for value in coordinate.split(',')] for coordinate in line.split(' -> ')]
        start, end = coordinates[0], coordinates[1]
        diagram = add_line(diagram, start, end)
    print('Answer:', count_overlaps(diagram))

        
