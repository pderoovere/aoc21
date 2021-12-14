from pathlib import Path

input = Path('14/input.txt').read_text()
template, s_rules = input.split('\n\n')[:2]
rules = {}
for rule in s_rules.split('\n'):
    pair, new_char = rule.strip('\n').split(' -> ')
    rules[pair] = new_char

template_pair_count = {}
for i in range(len(template) - 1):
    pair = input[i:i+2]
    template_pair_count[pair] = template_pair_count.get(pair, 0) + 1

for _ in range(10):
    new_template_pair_count = {}
    for (pair, count) in template_pair_count.items():
        if pair in rules:
            new_char = rules[pair]
            new_pair1 = pair[0] + new_char
            new_pair2 = new_char + pair[1]
            new_template_pair_count[new_pair1] = new_template_pair_count.get(new_pair1, 0) + count
            new_template_pair_count[new_pair2] = new_template_pair_count.get(new_pair2, 0) + count
        else:
            new_template_pair_count[pair] = count
    template_pair_count = new_template_pair_count

sum = 0
counts = {
    'N': 1 # Because last char
}
for pair, count in template_pair_count.items():
    char1 = pair[0]
    counts[char1] = counts.get(char1, 0) + count
    sum += count

least = None
most = None
for _, count in counts.items():
    if least is None or count < least:
        least = count
    if most is None or count > most:
        most = count

print('Answer:', most - least)