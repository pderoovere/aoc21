def parse_line(line):
    parts = line.replace('|', '').split()
    patterns = parts[:10]
    output = parts[10:]
    return patterns, output

def count_unique_numbers(output):
    return len([digit for digit in output if len(digit) in [2, 3, 4, 7]])

with open('08/input.txt') as input:
    count = 0
    for line in input.readlines():
        _, output = parse_line(line) 
        count += count_unique_numbers(output)
    print('Answer:', count)