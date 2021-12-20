import numpy as np
from collections import deque
from itertools import combinations
from functools import lru_cache
import time

start_time = time.time()

np.set_printoptions(edgeitems=30, linewidth=100000)

SCANNER_RANGE = 1000
COMMON_THRESHOLD = 12

IDENT = np.array([  [1, 0, 0],
                    [0, 1, 0],
                    [0, 0, 1]])
ROT_X = np.array([  [1, 0, 0],
                    [0, 0, -1],
                    [0, 1, 0]])
ROT_Y = np.array([  [0, 0, 1],
                    [0, 1, 0],
                    [-1, 0, 0]])
ROT_Z = np.array([  [0, -1, 0],
                    [1, 0, 0],
                    [0, 0, 1]])

def rotator_generator():
    """Yields the 24 distinct combined 90-degree rotation matrices"""
    
    def roll(m): 
        """Rotates the given matrix 90 degrees about the z-axis"""
        return np.matmul(ROT_Z, m)

    def turn(m): 
        """Rotates the given matrix 90 degrees about the x-axis"""
        return np.matmul(ROT_X, m)

    m = IDENT
    for _ in range(2):
        for _ in range(3):
            m = roll(m)
            yield(m)
            for i in range(3):
                m = turn(m)
                yield(m)
        m = roll(turn(roll(m)))

ROTATORS = list(rotator_generator())

def rotations(beacon_set):
    """Yields the given map (beacon set) in all 24 of its rotated versions"""
    for rotator in ROTATORS:
        yield np.matmul(rotator, beacon_set)

def translator_to(from_v, to_v):
    """Returns the translation vector to translate one point to another"""
    return (to_v - from_v).reshape((3,1))

def check_match(a, b):
    """Counts the number of common columns between two matrices, and returns
    True if it is at least COMMON_THRESHOLD, False if not"""
    if len(set(a[0]) & set(b[0])) < COMMON_THRESHOLD:
        # quick check on first row to discard obvious non-matches
        return False

    a_set = {tuple(col) for col in a.T.tolist()}
    b_set = {tuple(col) for col in b.T.tolist()}
    return len(a_set & b_set) >= COMMON_THRESHOLD

def attempt_match(free_map: np.ndarray, fixed_map: np.ndarray):
    """Rotates and translated free_map through every matchup with fixed_map. 
    Returns the scanner's position (relative to scanner 0) and the correctly
    rotated and translated version of free_map if found, or None if not."""
    for rot_free_map in rotations(free_map):
        for handle in rot_free_map.T[:-12]:
            for fixed_point in fixed_map.T:
                translator = translator_to(handle, fixed_point)
                shifted_free_map = rot_free_map + translator
                if check_match(fixed_map, shifted_free_map):
                    return (translator, shifted_free_map)
    return None

def manhattan_dist(point_a, point_b):
    """Returns the manhattan distance between two points"""
    return sum([abs(a - b) for a, b in zip(point_a, point_b)])

free_maps = deque()
attempted = {}
with open('input') as f:
    while line := f.readline().strip():
        if line == '':
            continue
        if line.startswith('---'):
            scanner_num = int(line[12:-4])
        raw_beacons = []
        while (line := f.readline().strip()) != '':
            raw_beacons.append([int(val) for val in line.split(',')])
        
        free_maps.append((scanner_num, np.array(raw_beacons).transpose()))
        attempted[scanner_num] = set()

fixed_maps = {0: free_maps.popleft()[1]}
centres = set()
while free_maps:
    free_num, free_map = free_maps[0]
    print(f'Attempting to align {free_num}...', end='')
    for fixed_num, fixed_map in fixed_maps.items():
        if free_num in attempted[fixed_num]:
            continue
        if (result := attempt_match(free_map, fixed_map)) is not None:
            centre = tuple(result[0].reshape(3))
            centres.add(centre)
            fixed_maps[free_num] = result[1]
            free_maps.popleft()
            print(f'aligned to {fixed_num}! Centre at {centre}. {len(free_maps)} remaining.')
            break
        attempted[fixed_num].add(free_num)
    else:
        print('no match yet.')
    free_maps.rotate(-1)

beacons = set()
for fixed_map in fixed_maps.values():
    for row in fixed_map.T:
        beacons.add(tuple(row))
print(f'Part 1: {len(beacons)} ({time.time() - start_time:0.2f} s)')
start_time = time.time()

max_dist = max([manhattan_dist(a, b) for a, b in combinations(centres, 2)])
print(f'Part 2: {max_dist} ({time.time() - start_time:0.2f} s)')
