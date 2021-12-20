from pathlib import Path
import numpy as np
from scipy.spatial.transform import Rotation as R

def parse_scanner(scanner_text):
    return [[int(v) for v in c.split(',')] for c in scanner_text.split('\n')[1:]]

lines = Path('19/test.txt').read_text().strip('\n')
scanners = [np.array(parse_scanner(scanner)) for scanner in lines.split('\n\n')]

rotations = []
for w in [0, 90, 180, 270]:
    for p in [0, 90, 180, 270]:
        for r in [0, 90, 180, 270]:
            rotation = R.from_euler('xyz', [w, p, r], degrees=True).as_matrix()
            if not any(np.allclose(rotation, r) for r in rotations): 
                rotations.append(rotation)
rotations = np.stack(rotations)

def transform_pts(points):
    points = points.astype(float)
    result = np.einsum('vij, nj -> vni', rotations, points)
    result = np.rint(result).astype(int)
    return result

scanners = [transform_pts(pts) for pts in scanners]

def to_set(arr):
    return set(map(tuple, arr))

def to_arr(set):
    return np.array(list(set))

def match_pts(ref, pts):
    for pts_pt in pts:
        pts_set = to_set(pts - pts_pt)
        for ref_pt in ref:
            ref_set = to_set(ref - ref_pt)
            merged_set = set.union(ref_set, pts_set)
            if len(merged_set) <= len(ref_set) + len(pts_set) - 12:
                return to_arr(merged_set) + ref_pt

def match_scanners(s1, s2):
    ref_orientation = s1[0]
    for test_orientation in s2:
        match = match_pts(ref_orientation, test_orientation)
        if match is not None:
            return transform_pts(match)

def try_to_merge(scanners):
    if len(scanners) == 1: 
        return scanners
    ref = scanners[0]
    for scanner in range(1, len(scanners)):
        match = match_scanners(ref, scanners[scanner])
        if match is not None:
            scanners.pop(scanner)
            scanners.pop(0)
            scanners.append(match)
            return try_to_merge(scanners)
    print('Weird, could not find a match, add it to the back to try again later...')
    scanners.pop(0)
    scanners.append(ref)
    return try_to_merge(scanners)

ref = scanners[0]
result = try_to_merge(scanners)
result = match_scanners(ref, result[0])[0]

print('Answer:', len(result))
