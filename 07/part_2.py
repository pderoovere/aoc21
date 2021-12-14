from pathlib import Path
import tqdm

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

# Calculate the cost of each possible displacement
costs = {}
for distance in range(max_position - min_position + 1):
    cost = 0
    extra_cost = 1
    for i in range(distance):
        cost += extra_cost
        extra_cost += 1
    costs[distance] = cost

# Calculate the total cost of each possible target position
counts = []
for target_position in tqdm.tqdm(range(min_position, max_position+1)):
    total_cost = 0
    for position, position_count in position_counts.items():
        total_cost += position_count * costs[abs(position - target_position)]
    counts.append(total_cost)

# Return the minimal total cost
print('Answer:', min(counts))