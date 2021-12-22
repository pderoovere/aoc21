from pathlib import Path
import re
from dataclasses import dataclass

@dataclass
class Range:
    low: int
    high: int

    def intersection(self, other):
        low = max(self.low, other.low)
        high = min(self.high, other.high)
        return Range(low, high) if low <= high else None

    def has_overlap(self, other):
        return self.intersection(other) is not None

    def differences(self, other):
        if not self.has_overlap(other):
            return [self]
        result = []
        if self.low < other.low:
            result.append(Range(self.low, other.low - 1))
        if self.high > other.high:
            result.append(Range(other.high + 1, self.high))
        return result

    def __len__(self):
        return self.high + 1 - self.low

@dataclass
class Cuboid:
    value: int
    x: Range
    y: Range
    z: Range

    def has_overlap(self, other):
        return self.x.has_overlap(other.x) and self.y.has_overlap(other.y) and self.z.has_overlap(other.z)

    def differences(self, other):
        if not self.has_overlap(other):
            return [self]
        result = []
        for d_x in self.x.differences(other.x):
            result.append(Cuboid(self.value, d_x, self.y, self.z))
        remaining_x = self.x.intersection(other.x)
        for d_y in self.y.differences(other.y):
            result.append(Cuboid(self.value, remaining_x, d_y, self.z))
        remaining_y = self.y.intersection(other.y)
        for d_z in self.z.differences(other.z):
            result.append(Cuboid(self.value, remaining_x, remaining_y, d_z))
        return result

    def total_value(self):
        return self.value * len(self.x) * len(self.y) * len(self.z)

def combine(cuboids, new_cuboid):
    remaining_cuboids = []
    for cuboid in cuboids:
        remaining_cuboids += cuboid.differences(new_cuboid)
    return remaining_cuboids + [new_cuboid]

def parse(line):
    value, limits = line.split(' ')
    value = 1 if value == 'on' else 0
    limits = [int(n) for n in re.findall('[-]*[0-9]+', limits)]
    return Cuboid(value, Range(limits[0], limits[1]), Range(limits[2], limits[3]), Range(limits[4], limits[5]))

lines = Path('22/input.txt').read_text().strip('\n').split('\n')

cuboids = []
for i, line in enumerate(lines):
    cuboid = parse(line)
    cuboids = combine(cuboids, cuboid)

print('Answer: ', sum([cuboid.total_value() for cuboid in cuboids]))