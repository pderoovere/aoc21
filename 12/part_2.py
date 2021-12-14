from pathlib import Path
import collections

input = Path('12/input.txt').read_text()
input = input.strip('\n\n')

graph = collections.defaultdict(list)
for line in input.split('\n'):
    c1, c2 = line.split('-')
    graph[c1].append(c2)
    graph[c2].append(c1)

def visited_small_cave_twice(current_path):
    for node in set(current_path):
        if node.islower() and current_path.count(node) == 2:
            return True
    return False

def can_visit(node, current_path):
    return (
        node.isupper() or 
        node not in current_path or
        (node != 'start' and (not visited_small_cave_twice(current_path)))
    )

def travel(paths, current_path, graph, current_node, end_node):
    if can_visit(current_node, current_path):
        current_path.append(current_node)
        if current_node == end_node:
            paths.append(current_path)
        else:
            for node in graph[current_node]:
                travel(paths, current_path.copy(), graph, node, end_node)

paths = []
travel(paths, [], graph, 'start', 'end')

print('Answer:', len(paths))