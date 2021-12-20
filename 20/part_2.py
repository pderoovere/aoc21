from pathlib import Path
import numpy as np

lines = Path('20/input.txt').read_text().strip('\n')
lines = lines.replace('.', '0')
lines = lines.replace('#', '1')

algorithm, img = lines.split('\n\n')
algorithm = np.array([int(c) for c in algorithm])
img = np.array([[int(c) for c in line] for line in img.split('\n')])

def value(key):
    key = int(''.join([str(c) for c in key.flatten()]), 2)
    return algorithm[key]

def enhance(img, c=0):
    img = np.pad(img, 3, 'constant', constant_values=c)
    result = np.zeros((img.shape[0] - 2, img.shape[0] - 2), dtype=int)
    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            result[i, j] = value(img[i:i+3, j:j+3])
    return result

for i in range(50):
    print('Enhancing', i)
    if i == 0: 
        img = enhance(img, 0)
    elif i % 2 == 0:
        img = enhance(img, algorithm[algorithm[0]])
    else:
        img = enhance(img, algorithm[0])

print('Answer', np.sum(img))