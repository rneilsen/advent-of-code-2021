import time
from heapq import heapify, heappop, heappush

start_time = time.time()

TILES = 5
REMOVED = -1

with open('input') as f:
    map = [[int(ch) for ch in list(row.strip())] for row in f.readlines()]

def find_lowest_risk_path(map):
    height = len(map)
    width = len(map[0])
    target = (height - 1, width - 1)

    frontier = [(map[0][1], 0, 1), (map[1][0], 1, 0)]
    heapify(frontier)

    def get_neighbours(x, y):
        """Returns a set of the valid coordinate pairs of all adjacent cells
        to the given coordinates"""
        neighbours = set()
        if x > 0:
            neighbours.add((x-1, y))
        if x < height - 1:
            neighbours.add((x+1, y))
        if y > 0:
            neighbours.add((x, y-1))
        if y < width - 1:
            neighbours.add((x, y+1))
        return neighbours


    def find_in_frontier(x, y):
        """Finds a tuple of the index and current priority of the given 
        coordinate pair in the frontier, or None if the given 
        coordinate pair is not in the frontier"""
        for i in range(len(frontier)):
            fr_p, fr_x, fr_y = frontier[i]
            if fr_x == x and fr_y == y:
                return (i, fr_p)
        return None
            
   
    visited = set()

    while target not in visited:
        while True:
            cur_risk, x, y = heappop(frontier)
            if x != REMOVED:
                break
        visited.add((x, y))
        if (x, y) == target:
            return cur_risk

        neighbours = get_neighbours(x, y) - visited
        for n_x, n_y in neighbours:
            if (fif := find_in_frontier(n_x, n_y)) is not None:
                n_i, n_p = fif
                if cur_risk + map[n_x][n_y] < n_p:
                    frontier[n_i] = (n_p, REMOVED, REMOVED)
                    heappush(frontier, (cur_risk + map[n_x][n_y], n_x, n_y))
            else:
                heappush(frontier, (cur_risk + map[n_x][n_y], n_x, n_y))

print('Part 1:', find_lowest_risk_path(map), 
        f'({time.time() - start_time:0.2f} s)')
start_time = time.time()

def inc(row):
    return [(val + 1 if val < 9 else 1) for val in row]

for row in map:
    iter_row = row.copy()
    for _ in range(TILES - 1):
        iter_row = inc(iter_row)
        row.extend(iter_row)
new_rows = map.copy()
for _ in range(TILES - 1):
    new_rows = [inc(row) for row in new_rows]
    map.extend(new_rows)

print('Part 2:', find_lowest_risk_path(map), 
        f'({time.time() - start_time:0.2f} s)')
