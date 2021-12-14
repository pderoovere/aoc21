from pathlib import Path

positions = [int(position) for position in Path('07/input.txt').read_text().split(',')]

# Count the occurances of each starting position and calculate the min and max position
position_counts = {}
min_position = None
max_position = None
for position in positions:
    position_counts[position] = position_counts.get(position, 0) + 1
    if min_position is None or position < min_position:
        min_position = position
    if max_position is None or position > max_position:
        max_position = position

# Calculate the total cost of each possible target position.
def count_fuel(position_counts, target_position):
    result = 0
    for position, position_count in position_counts.items():
        result += abs(position - target_position) * position_count
    return result
counts = [count_fuel(position_counts, target_position) for target_position in range(min_position, max_position+1)]

# Return the minimal total cost
print('Answer:', min(counts))