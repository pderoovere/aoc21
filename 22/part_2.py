from pathlib import Path
import re
from dataclasses import dataclass

@dataclass
class Range:
    low: int
    high: int

    def diff(self, other):
        if self.high < other.low or self.low > other.high:
            return [self]
        result = []
        if self.low < other.low:
            result.append(Range(self.low, other.low - 1))
        if self.high > other.high:
            result.append(Range(other.high + 1, self.high))
        return result

    def intersect(self, other):
        low = max(self.low, other.low)
        high = min(self.high, other.high)
        if low <= high:
            return Range(low, high)
        else:
            return None

    def has_overlap(self, other):
        return not (self.high < other.low or self.low > other.high)

    def indices(self):
        return set(range(self.low, self.high + 1))

    def __len__(self):
        return self.high + 1 - self.low

@dataclass
class Box:
    value: int
    x: Range
    y: Range
    z: Range

    def total_value(self):
        return self.value * len(self.x) * len(self.y) * len(self.z)

    def has_overlap(self, other):
        return self.x.has_overlap(other.x) and self.y.has_overlap(other.y) and self.z.has_overlap(other.z)

    def diff(self, other):
        if not self.has_overlap(other):
            return [self]
        result = []
        for d_x in self.x.diff(other.x):
            result.append(Box(self.value, d_x, self.y, self.z))
        remaining_x = self.x.intersect(other.x)
        if remaining_x is None:
            return result
        for d_y in self.y.diff(other.y):
            result.append(Box(self.value, remaining_x, d_y, self.z))
        remaining_y = self.y.intersect(other.y)
        if remaining_y is None:
            return result
        for d_z in self.z.diff(other.z):
            result.append(Box(self.value, remaining_x, remaining_y, d_z))
        return result

def parse(line):
    global limit_val
    value, limits = line.split(' ')
    value = 1 if value == 'on' else 0
    limits = [int(n) for n in re.findall('[-]*[0-9]+', limits)]
    return Box(value, Range(limits[0], limits[1]), Range(limits[2], limits[3]), Range(limits[4], limits[5]))

def combine(boxes, new_box):
    new_boxes = []
    for box in boxes:
        new_boxes += box.diff(new_box)
    new_boxes.append(new_box)
    return new_boxes

result = []
lines = Path('22/input.txt').read_text().strip('\n').split('\n')
for i, line in enumerate(lines):
    box = parse(line)
    result = combine(result, box)
    print('Boxes after', i, len(result))

print('Answer: ', sum([box.total_value() for box in result]))