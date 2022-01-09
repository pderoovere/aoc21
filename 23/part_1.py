import copy

#    0 1 2 3 4 5 6 7 8 9 10
# 0  x x x x x x x x x x x
# 1      x   x   x   x
# 2      x   x   x   x


cost_factors = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

initial_state = {
    (1, 2): 'B',
    (2, 2): 'A',
    (1, 4): 'C',
    (2, 4): 'D',
    (1, 6): 'B',
    (2, 6): 'C',
    (1, 8): 'D',
    (2, 8): 'A',
}

initial_state = {
    (1, 2): 'B',
    (2, 2): 'B',
    (1, 4): 'C',
    (2, 4): 'C',
    (1, 6): 'A',
    (2, 6): 'D',
    (1, 8): 'D',
    (2, 8): 'A',
}

target_state = {
    (1, 2): 'A',
    (2, 2): 'A',
    (1, 4): 'B',
    (2, 4): 'B',
    (1, 6): 'C',
    (2, 6): 'C',
    (1, 8): 'D',
    (2, 8): 'D',
}

target_columns = {
    'A': 2,
    'B': 4,
    'C': 6,
    'D': 8,
}

valid_destinations = []
for j in range(11):
    if j not in target_columns.values():
        valid_destinations += [(0, j)]
    else:
        valid_destinations += [(1, j), (2, j)]

def is_final(pos, type, state):
    if pos[0] > 0 and pos[1] == target_columns[type]:
        for i in range(pos[0] + 1, 3):
            if (((i, pos[1]) not in state) or (state[(i, pos[1])] != type)):
                return False
        return True
    return False


def is_valid(type, pos, destination, state):

    if pos == destination:
        return False

    if is_final(pos, type, state):
        return False

    # No collisions
    i, j = pos
    if j != destination[1]:
        # Other column, always move via row 0
        while i > 0:
            i -= 1
            if (i,j) in state:
                return False
    while j != destination[1]:
        j += (1 if destination[1] > j else -1)
        if (i,j) in state:
            return False    
    while i != destination[0]:
        i += (1 if destination[0] > i else -1) 
        if (i,j) in state:
            return False

    # Other rules

    if destination[0] == 0 and pos[0] == 0:
        return False

    if destination[0] > 0 and not is_final(destination, type, state):
        return False

    return True

def next_moves(state):
    result = []
    for pos, type in state.items():
        for destination in valid_destinations:
            if is_valid(type, pos, destination, state):
                result.append(((pos, destination, type)))
    return result

def distance(pos, destination):
    if pos[1] == destination[1]:
        return abs(destination[0] - pos[0])
    else:
        return abs(0-pos[0]) + abs(destination[1] - pos[1]) + abs(0-destination[0])

def calculate_cost(pos, destination, type):
    return distance(pos, destination) * cost_factors[type]

def freeze(d):
    return frozenset(sorted(d.items()))

def unfreeze(s):
    return dict(s)

def closest(state, type, p):
    value = None
    for (pos, type) in state.items():
        if type == type:
            d = distance(pos, p)
            if value is None:
                value = d
            else:
                value = min(d, value)
    return d


def calculate_heuristic(state, cost):
    return cost
    remaining = 0
    state = unfreeze(state)
    remaining += 1000 * closest(state, 'D', (2, 8))
    remaining += 1000  * closest(state, 'D', (1, 8))
    remaining += 100 * closest(state, 'C', (2, 6))
    remaining += 100 * closest(state, 'C', (1, 6))
    remaining += 10 * closest(state, 'B', (2, 4))
    remaining += 10 * closest(state, 'B', (1, 4))
    remaining += 1 * closest(state, 'A', (2, 2))
    remaining += 1 * closest(state, 'A', (1, 2))
    return cost + 0 * remaining

lowest = None

def search(start, target):
    global lowest

    start = freeze(start)
    queue = {start: 0}
    costs = {start: 0}
    visited = set()

    print('Initial', sorted(start))

    while len(queue) > 0:
        next_state = min(queue, key=queue.get)
        
        visited.add(next_state)
        heuristic = queue[next_state]
        cost = costs[next_state]
        del queue[next_state]

        print('queue', len(queue))

        next_state = unfreeze(next_state)
        moves = next_moves(next_state)
        for pos, destination, type in moves:

            new_state = copy.deepcopy(next_state)

            del new_state[pos]
            new_state[destination] = type

            new_state = freeze(new_state)
            new_cost = cost + calculate_cost(pos, destination, type)
            new_heuristic = calculate_heuristic(new_state, new_cost)

            if new_state in visited:
                continue
            if new_state == target:
                if lowest is None:
                    lowest = new_cost
                else:
                    lowest = min(lowest, new_cost)
                continue
            if new_state in queue and queue[new_state] < new_heuristic:
                continue

            queue[new_state] = new_heuristic
            costs[new_state] = new_cost
    
    return lowest

print('Answer', search(initial_state, freeze(target_state)))

#print(is_final((1, 2), 'A', {(2, 2): 'A'}))
