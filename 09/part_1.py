from pathlib import Path
import numpy as np

input = Path('09/input.txt').read_text()
input = input.strip('\n\n')
heightmap = np.array([[int(value) for value in row] for row in input.split('\n')], dtype=int)
heightmap = np.pad(heightmap, ((1, 1), (1, 1)), 'constant', constant_values=9)

minima = np.array([], dtype=int)
nb_rows, nb_columns = heightmap.shape
for i in range(1, nb_rows-1):
    for j in range(1, nb_columns-1):
        height = heightmap[i, j]
        if np.all(heightmap[[i-1, i, i, i+1], [j, j-1, j+1, j]] > height):
            minima = np.append(minima, height)

risk = np.sum(minima + 1)
print('Answer:', risk)