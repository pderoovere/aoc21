def bits_to_number(bits):
    result = ''
    for bit in bits:
        result += str(bit)
    return int(result, 2)


def count_ones_at_index(candidates, index):
    return sum([candidate[index] for candidate in candidates])


def find_match(candidates, index, value):
    candidates = list(filter(lambda candidate: candidate[index] == value, candidates))
    match = None
    if len(candidates) == 1:
        match = bits_to_number(candidates[0])
    return match, candidates


with open('03/input.txt') as input:
    bits_by_lines = [[int(bit) for bit in list(line.rstrip())] for line in input]
    nb_bits = len(bits_by_lines[0])
    oxygen_generator_candidates = bits_by_lines.copy()
    co2_scrubber_candidates = bits_by_lines.copy()
    oxygen_generator = None
    co2_scrubber = None
    for i in range(nb_bits):
        if oxygen_generator is None:
            nb_ones_at_current_index = count_ones_at_index(oxygen_generator_candidates, i)
            most_common = 1 if nb_ones_at_current_index >= len(oxygen_generator_candidates)/2 else 0
            oxygen_generator, oxygen_generator_candidates = find_match(oxygen_generator_candidates, i, most_common)
        if co2_scrubber is None:
            nb_ones_at_current_index = count_ones_at_index(co2_scrubber_candidates, i)
            least_common = 0 if nb_ones_at_current_index >= len(co2_scrubber_candidates)/2 else 1
            co2_scrubber, co2_scrubber_candidates = find_match(co2_scrubber_candidates, i, least_common)
        if oxygen_generator is not None and co2_scrubber is not None:
            print('Answer', oxygen_generator * co2_scrubber)
            break

