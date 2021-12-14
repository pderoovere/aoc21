error_points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

brackets = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

with open('10/input.txt') as input:
    error = 0
    for line in input.readlines():
        stack = []
        for c in line.rstrip('\n'):
            if c in brackets.keys():
                # Opening bracket
                stack.append(brackets[c])
            else:
                # Closing bracket
                expected = stack.pop()
                if c is not expected:
                    error += error_points[c]
                    break
    print('Answer:', error)

