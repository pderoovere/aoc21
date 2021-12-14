with open('01/input.txt') as input:
    measurements = [int(line) for line in input.readlines()]
    window_size = 3
    previous_window = None
    nb_increases = 0
    nb_windows = len(measurements) - window_size + 1
    for i in range(nb_windows):
        new_window = sum(measurements[i:i+window_size])
        if previous_window is not None and new_window > previous_window:
            nb_increases += 1
        previous_window = new_window
    print('Answer:', nb_increases)