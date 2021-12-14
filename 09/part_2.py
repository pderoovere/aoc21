from pathlib import Path
import numpy as np

input = Path('09/input.txt').read_text()
input = input.strip('\n\n')
height_map = np.array([[int(value) for value in row] for row in input.split('\n')], dtype=int)
height_map = np.pad(height_map, ((1, 1), (1, 1)), 'constant', constant_values=9)

minima_indices = []
nb_rows, nb_columns = height_map.shape
for i in range(1, nb_rows-1):
    for j in range(1, nb_columns-1):
        height = height_map[i, j]
        if np.all(height_map[[i-1, i, i, i+1], [j, j-1, j+1, j]] > height):
            minima_indices.append((i, j))

visited_map = np.zeros_like(height_map)

def expand(index, basin):
    i, j = index
    height = height_map[i, j] 
    basin.append(height)
    visited_map[i, j] = 1
    for new_i, new_j in zip([i-1, i, i, i+1], [j, j-1, j+1, j]):
        neighbouring_height = height_map[new_i, new_j]
        if neighbouring_height != 9 and neighbouring_height > height and visited_map[new_i, new_j] == 0:
            expand((new_i, new_j), basin)
    return basin
    
basins = [expand(minima_index, []) for minima_index in minima_indices]
basin_sizes = sorted([len(basin) for basin in basins], reverse=True)

print('Answer:', basin_sizes[0] * basin_sizes[1] * basin_sizes[2])