import numpy as np
import numpy.ma as ma
from pathlib import Path
import time

start = time.time()

input = Path('15/test.txt').read_text()
i_risk_levels = np.array([[int(v) for v in line] for line in input.strip('\n').split('\n')])
i_h, i_w = i_risk_levels.shape

nb_tiles = 5
risk_levels = np.zeros((i_h * nb_tiles, i_w * nb_tiles))
for i in range(nb_tiles):
    for j in range(nb_tiles):
        tile = (i_risk_levels + i + j - 1) % 9 + 1
        risk_levels[i*i_h:(i+1)*i_h, j*i_w:(j+1)*i_w] = tile

def valid_index(i, j):
    return ((0 <= i < risk_levels.shape[0]) and (0 <= j < risk_levels.shape[1]))

def neighbours(i, j):
    for i_offset, j_offset in [0, -1], [0, 1], [-1, 0], [1, 0]:
        n_i = i + i_offset
        n_j = j + j_offset 
        if valid_index(n_i, n_j):
            yield n_i, n_j

def calculate_heuristic(risk, location, target):
    distance = (target[0] - location[0]) + (target[1] - location[1])
    return risk - distance

def calculate_risk(location):
    return risk_levels[location[0], location[1]]

def search(start, target):
    risks = {start: 0}
    queue = {start: 0}
    visited = set()

    while len(queue) > 0:
        node = min(queue, key=queue.get)

        visited.add(node)
        risk = risks[node]

        if node == start:
            risk = 0
        del queue[node]

        for next in neighbours(*node):
            next_risk = risk + calculate_risk(next)
            if next in visited:
                continue
            if next == target:
                return next_risk
            next_cost = calculate_heuristic(next_risk, next, target)
            if next in queue.keys() and queue[next] < next_cost:
                continue
            queue[next] = next_cost
            risks[next] = next_risk

            
result = search((0, 0), (risk_levels.shape[0] - 1, risk_levels.shape[1] - 1))
print('Answer:', int(result))
