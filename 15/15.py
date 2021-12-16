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
        """Returns a tuple of the index and current priority (risk) of the 
        given coordinate pair in the frontier, or None if the given coordinate
        pair is not in the frontier"""
        for i in range(len(frontier)):
            fr_p, fr_x, fr_y = frontier[i]
            if fr_x == x and fr_y == y:
                return (i, fr_p)
        return None

   
    visited = {(0,0)}

    while True:
        while True:
            # find next (non-removed) cell to visit in the frontier
            cur_risk, x, y = heappop(frontier)
            if x != REMOVED:
                break

        if (x, y) == target:
            return cur_risk
        visited.add((x, y))

        neighbours = get_neighbours(x, y) - visited
        for n_x, n_y in neighbours:
            new_risk = cur_risk + map[n_x][n_y]
            if (fif := find_in_frontier(n_x, n_y)) is not None:
                # this neighbour is already in the frontier, update it if req'd
                n_i, n_r = fif
                if new_risk < n_r:
                    frontier[n_i] = (n_r, REMOVED, REMOVED)
                    heappush(frontier, (new_risk, n_x, n_y))
            else:
                # this neighbour is new, add it to the frontier
                heappush(frontier, (new_risk, n_x, n_y))

print('Part 1:', find_lowest_risk_path(map), 
        f'({time.time() - start_time:0.2f} s)')
start_time = time.time()

# Tile the map for part 2
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
