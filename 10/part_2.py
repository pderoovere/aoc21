score_points = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

brackets = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

with open('10/input.txt') as input:
    scores = []
    for line in input.readlines():
        stack = []
        for c in line:
            if c == '\n' and len(stack) > 0:
                # End of and incomplete string
                score = 0
                for s in reversed(stack):
                    score = score * 5 + score_points[s]
                scores.append(score)
            elif c in brackets.keys():
                # Opening bracket
                stack.append(brackets[c])
            else:
                # Closing bracket
                expected = stack.pop()
                if c is not expected:
                    # Corrupt line, ignore and continue
                    break
    print('Answer:', sorted(scores)[int((len(scores) - 1) / 2)])

