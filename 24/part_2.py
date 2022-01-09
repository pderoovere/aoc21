from functools import lru_cache

@lru_cache(maxsize=None)
def sub_program(z, input, p1, p2, p3):
    w = input
    x = z % 26
    z = z // p1
    x += p2
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y = 25 * x + 1
    z *= y
    y = w + p3
    y *= x
    z += y
    return z

parameters = [
    (1, 13, 14),
    (1, 12, 8),
    (1, 11, 5),
    (26, 0, 4),
    (1, 15, 10),
    (26, -13, 13),
    (1, 10, 16),
    (26, -9, 5),
    (1, 11, 6),
    (1, 13, 13),
    (26, -14, 6),
    (26, -3, 7),
    (26, -2, 13),
    (26, -14, 3)
]

def find_valid_zs(target_zs, index):
    result = set()
    p1, p2, p3 = parameters[index]
    for z in range(1_000_000):
        for i in range(1, 10):
            if sub_program(z, i, p1, p2, p3) in target_zs:
                result.add(z)
    return result

# Find the valid z's for each index
valid_zs = [{0}]
for i in range(13, 0, -1):
    target_zs = [0] if len(valid_zs) == 0 else valid_zs[0]
    valid_zs.insert(0, find_valid_zs(target_zs, i))

# Find the value of each index that produces a valid z
z = 0
result = []
for idx in range(14):
    p1, p2, p3 = parameters[idx]
    for i in range(1, 10):
        new_z = sub_program(z, i, p1, p2, p3)
        if new_z in valid_zs[idx]:
            z = new_z
            result.append(i)
            break

print('Answer', ''.join([str(d) for d in result]))