
segments = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
numbers = [
    'abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf', 'abcdefg', 'abcdfg']

def parse_line(line):
    parts = line.replace('|', '').split()
    patterns = parts[:10]
    outputs = parts[10:]
    return [list(pattern) for pattern in patterns], [list(output) for output in outputs]

def calc_segments_by_occurances(patterns):
    segment_counts = {segment: 0 for segment in segments}    
    for pattern in patterns:
        for segment in pattern:
            segment_counts[segment] += 1
    counts = {}
    for count in range(len(patterns) + 1):
        counts[count] = [s for s, c in segment_counts.items() if c == count]
    return counts

def calc_constraints(length, patterns):
    segments_by_occurances = calc_segments_by_occurances(patterns)
    if length == 2: # 1, single match
        return [(['c', 'f'], segments_by_occurances[1])]
    elif length == 3: # 7, single match
        return [(['a', 'c', 'f'], segments_by_occurances[1])]
    elif length == 4: # 4, single match
        return [(['b', 'c', 'd', 'f'], segments_by_occurances[1])]
    elif length == 7: # 8, no constraints
        return []
    elif length == 5: # 2, 3 or 5
        return [(['a', 'd', 'g'], segments_by_occurances[3]), (['c', 'f'], segments_by_occurances[2]), (['b', 'e'], segments_by_occurances[1])]
    elif length == 6: # 6, 9, 0
        return [(['a', 'b', 'f', 'g'], segments_by_occurances[3]), (['c', 'd', 'e'], segments_by_occurances[2])]

def apply_constraint(segment_options, constraint):
    for segment in segments:
        if segment in constraint[0]:
            segment_options[segment] = [option for option in segment_options[segment] if option in constraint[1]]
        else:
            segment_options[segment] = [option for option in segment_options[segment] if option not in constraint[1]]
        if len(segment_options[segment]) == 1:
            segment_options[segment] = segment_options[segment][0]
    return segment_options

def resolve_patterns(patterns):
    patterns_by_length = dict()
    for pattern in patterns:
        length = len(pattern)
        patterns_by_length[length] = patterns_by_length.get(length, []) + [pattern]
    segment_options = {segment: segments.copy() for segment in segments}
    for length, p in patterns_by_length.items():
        constraints = calc_constraints(length, p)
        for constraint in constraints:
            segment_options = apply_constraint(segment_options, constraint)
    return segment_options

def translate_digit(dictionary, digit):
    active_segments = [dictionary[d] for d in digit]
    return numbers.index(''.join(sorted(active_segments)))

def translate_output(dictionary, output):
    return int(''.join([str(translate_digit(dictionary, digit)) for digit in output]))

with open('08/input.txt') as input:
    overall_sum = 0
    for line in input.readlines():
        patterns, output = parse_line(line)     
        dictionary = resolve_patterns(patterns)
        dictionary = {v: k for k, v in dictionary.items()}
        number = translate_output(dictionary, output)
        overall_sum += number
    print('Answer:', overall_sum)
