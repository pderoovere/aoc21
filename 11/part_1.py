from pathlib import Path
import numpy as np

input = Path('11/input.txt').read_text()
input = input.strip('\n\n')
energy_levels = np.array([[int(value) for value in row] for row in input.split('\n')], dtype=int)

def valid_index(i, j, shape):
    return (0 <= i < shape[0]) and (0 <= j < shape[1])

def check_for_flash(energy_levels, flashed, nb_flashes, i, j):
    if flashed[i, j]:
        # Already flashed, continue
        return energy_levels, flashed, nb_flashes
    if energy_levels[i, j] > 9:
        # Flash              
        nb_flashes += 1
        flashed[i, j] = 1
        energy_levels[i, j] = 0
        for i_offset in [-1, 0, 1]:
            for j_offset in [-1, 0, 1]:
                new_i = i + i_offset
                new_j = j + j_offset
                if valid_index(new_i, new_j, energy_levels.shape) and not (new_i == i and new_j == j):
                    if not flashed[new_i, new_j]:
                        energy_levels[new_i, new_j] += 1
                        energy_levels, flashed, nb_flashes = check_for_flash(energy_levels, flashed, nb_flashes, new_i, new_j)
    return energy_levels, flashed, nb_flashes

def step(energy_levels, nb_flashes):
    energy_levels += 1
    flashed = np.zeros_like(energy_levels)
    for i in range(energy_levels.shape[0]):
        for j in range(energy_levels.shape[1]):
            energy_levels, flashed, nb_flashes = check_for_flash(energy_levels, flashed, nb_flashes, i, j)
    energy_levels[flashed > 0] = 0
    return energy_levels, nb_flashes

nb_flashes = 0
for i in range(100):
    energy_levels, nb_flashes = step(energy_levels, nb_flashes)

print('Answer:', nb_flashes)