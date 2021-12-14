with open('01/input.txt') as input:
    measurements = [int(line) for line in input.readlines()]
    previous_measurement = None
    nb_increases = 0
    for measurement in measurements:
        if previous_measurement is not None and measurement > previous_measurement:
            nb_increases += 1
        previous_measurement = measurement
    print('Answer:', nb_increases)