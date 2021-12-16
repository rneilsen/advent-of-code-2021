import time

start_time = time.time()

with open('input') as f:
    map = [[int(ch) for ch in list(row.strip())] for row in f.readlines()]

TILES = 5

def find_best_path(map):
    height = len(map)
    width = len(map[0])
    target = (height - 1, width - 1)

    unvisited = {(i, j) for i in range(height) for j in range(width)}
    visited = set()
    best_distance = {node: float('inf') for node in unvisited}
    best_distance[(0,0)] = 0


    def get_neighbours(i, j):
        neighbours = set()
        if i > 0:
            neighbours.add((i-1, j))
        if i < height - 1:
            neighbours.add((i+1, j))
        if j > 0:
            neighbours.add((i, j-1))
        if j < width - 1:
            neighbours.add((i, j+1))
        return neighbours


    def get_min_distance(node_set):
        min_distance = float('inf')
        for node in node_set:
            if best_distance[node] < min_distance:
                min_distance = best_distance[node]
                best_node = node
        return best_node


    current_node = (0,0)
    while best_distance[target] == float('inf'):
        for i, j in get_neighbours(*current_node) - visited:
            best_distance[(i, j)] = min(best_distance[(i, j)], best_distance[current_node] + map[i][j])
        visited.add(current_node)
        unvisited.remove(current_node)
        current_node = get_min_distance(unvisited)

    return best_distance[target]

print('Part 1:', find_best_path(map), f'in {time.time() - start_time:0.2}s')

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

# print('Part 2:', find_best_path(map))