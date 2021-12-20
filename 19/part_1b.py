from pathlib import Path
import numpy as np
from scipy.spatial.transform import Rotation as R

def parse_scanner(scanner_text):
    return [[int(v) for v in c.split(',')] for c in scanner_text.split('\n')[1:]]

lines = Path('19/test.txt').read_text().strip('\n')
scanners = [np.array(parse_scanner(scanner), dtype=int) for scanner in lines.split('\n\n')]

def transformation(rotation, translation = [0., 0., 0.]):
    result = np.eye(4)
    result[:3, :3] = rotation[:3, :3]
    result[:3, 3] = translation
    return result

rotations = []
for w in [0, 90, 180, 270]:
    for p in [0, 90, 180, 270]:
        for r in [0, 90, 180, 270]:
            rotation = transformation(R.from_euler('xyz', [w, p, r], degrees=True).as_matrix())
            if not any(np.allclose(rotation, r) for r in rotations): 
                rotations.append(rotation)

scanner_graph = {}

def arr_to_set(a):
    return set(map(tuple, a))

def set_to_arr(s):
    return np.array(list(s))

def transform_points(points, transformation):
    points = points.astype(float)
    pts_h = np.ones((points.shape[0], 4))
    pts_h[:, :3] = points
    result = (pts_h @ transformation.T)[:, :3]
    result = np.rint(result).astype(int)
    return result

def combine(t1, t2):
    return t1 @ t2

def match(reference_beacons, candidate_beacons):
    for reference_beacon in reference_beacons:
        rel_reference_beacons = arr_to_set(reference_beacons - reference_beacon)
        for candidate_beacon in candidate_beacons:
            rel_candidate_beacons = arr_to_set(candidate_beacons - candidate_beacon)
            merged_beacons = set.union(rel_reference_beacons, rel_candidate_beacons)
            if len(merged_beacons) <= len(reference_beacons) + len(candidate_beacons) - 12:
                # Match!
                return reference_beacon - candidate_beacon

for scanner_1_idx in range(len(scanners) - 1):
    for scanner_2_idx in range(scanner_1_idx + 1, len(scanners)):
        print('Matching', scanner_1_idx, scanner_2_idx)
        if (scanner_1_idx, scanner_2_idx) in scanner_graph:
            break
        for rotation in rotations:
            rotated_beacons_scanner_2 = transform_points(scanners[scanner_2_idx], rotation)
            match_translation = match(scanners[scanner_1_idx], rotated_beacons_scanner_2)
            if match_translation is not None:
                print('-Matched', scanner_1_idx, scanner_2_idx, match_translation)
                scanner_graph[(scanner_1_idx, scanner_2_idx)] = transformation(rotation, match_translation)
                break


def merge(flattened, remaining):
    if len(remaining) == 0:
        return flattened
    for ((s1, s2), T) in remaining.items():
        if s1 in flattened:
            flattened[s2] = flattened[s1] @ T
            del remaining[(s1, s2)]
            return merge(flattened,  remaining)
        elif s2 in flattened:
            flattened[s1] = flattened[s2] @ np.linalg.pinv(T)
            del remaining[(s1, s2)]
            return merge(flattened, remaining)
    if len(remaining) > 0:
        raise Exception('Something went wrong...')

flattened_transformations = merge({0: np.eye(4)}, scanner_graph)

beacons = set()
for scanner_idx, points in enumerate(scanners):
    extra = arr_to_set(transform_points(points, flattened_transformations[scanner_idx]))
    test = sorted(extra, key=lambda tup: (tup[0], tup[1], tup[2]) )
    beacons = set.union(beacons, extra)

sorted_beacons = sorted(beacons, key=lambda tup: (tup[0], tup[1], tup[2]) )

print('Nb beacons', len(sorted_beacons))