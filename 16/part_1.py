from pathlib import Path
input = Path('16/input.txt').read_text().strip('\n')
input = list(''.join([bin(int(c, 16))[2:].zfill(4) for c in input])) # 16 = hex, 4 bits

def pop(data, size):
    part = data[:size]
    del data[:size]
    return part

def binary_to_int(data):
    return int(''.join(data), 2)

def pop_version(data):
    return binary_to_int(pop(data, 3))

def pop_type_id(data):
    return binary_to_int(pop(data, 3))    

def pop_literal(data):
    parts = []
    while True:
        part = pop(data, 5)
        parts += part[1:]
        if part[0] == '0':
            return binary_to_int(parts)

def pop_operator(data):
    subpackets = []
    length_type_id = pop(data, 1)[0]
    if length_type_id == '0':
        subpackets_length = binary_to_int(pop(data, 15))
        subpackets_data = pop(data, subpackets_length)
        while len(subpackets_data) > 0 and binary_to_int(subpackets_data) > 0:
            subpackets.append(pop_package(subpackets_data))
    else:
        nb_subpackets = binary_to_int(pop(data, 11))
        for _ in range(nb_subpackets):
            subpackets.append(pop_package(data))
    return subpackets

def pop_package(data):
    version = pop_version(data)
    type_id = pop_type_id(data)
    if type_id == 4:
        content = pop_literal(data)
    else:
        content = pop_operator(data)
    return {
        'version': version,
        'type_id': type_id,
        'content': content
    }

package = pop_package(input)

def count_versions(package):
    count = package['version']
    if package['type_id'] != 4:
        for p in package['content']:
            count += count_versions(p)
    return count

print('Answer', count_versions(package))