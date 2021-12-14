with open('03/input.txt') as input:
    one_counts = None
    nb_lines = 0
    for line in input.readlines():
        nb_lines += 1
        line = line.rstrip()
        if one_counts is None:
            one_counts = [0] * len(line)
        for i, bit in enumerate(line):
            one_counts[i] += int(bit)

    gamma_binary = ''
    epsilon_binary = ''
    for one_count in one_counts:
        if one_count > nb_lines/2:
            gamma_binary += '1'
            epsilon_binary += '0'
        else:
            gamma_binary += '0'
            epsilon_binary += '1'

    gamma = int(gamma_binary, 2)
    epsilon = int(epsilon_binary, 2)
    power_consumption = gamma * epsilon
    print('Answer:', power_consumption)