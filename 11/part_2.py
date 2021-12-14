from pathlib import Path
import numpy as np

input = Path('11/input.txt').read_text()
input = input.strip('\n\n')
energy_levels = np.array([[int(value) for value in row] for row in input.split('\n')], dtype=int)

def valid_index(i, j, shape):
    return (0 <= i < shape[0]) and (0 <= j < shape[1])

def check_for_flash(energy_levels, flashed, i, j):
    if flashed[i, j]:
        # Already flashed, continue
        return energy_levels, flashed
    if energy_levels[i, j] > 9:
        # Flash        
        flashed[i, j] = 1
        energy_levels[i, j] = 0
        for i_offset in [-1, 0, 1]:
            for j_offset in [-1, 0, 1]:
                new_i = i + i_offset
                new_j = j + j_offset
                if valid_index(new_i, new_j, energy_levels.shape) and not (new_i == i and new_j == j):
                    if not flashed[new_i, new_j]:
                        energy_levels[new_i, new_j] += 1
                        energy_levels, flashed = check_for_flash(energy_levels, flashed, new_i, new_j)
    return energy_levels, flashed 

def step(energy_levels):
    energy_levels += 1
    flashed = np.zeros_like(energy_levels)
    for i in range(energy_levels.shape[0]):
        for j in range(energy_levels.shape[1]):
            energy_levels, flashed = check_for_flash(energy_levels, flashed, i, j)
    energy_levels[flashed > 0] = 0
    return energy_levels


s = 0
while True:
    energy_levels = step(energy_levels)
    s += 1
    if np.all(energy_levels == 0):
        print('Answer', s)
        exit()