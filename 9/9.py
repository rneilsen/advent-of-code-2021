from itertools import product
from math import prod

with open('input') as f:
    rows = [[int(ch) for ch in list(row.strip())] for row in f.readlines()]

height = len(rows)
width = len(rows[0])

def get_neighbours(i: int, j: int) -> set[tuple[int, int]]:
    neighbours = {(i-1, j), (i+1, j), (i, j-1), (i, j+1)}
    return {(x, y) for x, y in neighbours if x in range(height) and y in range(width)}

low_points = set()
for i, j in product(range(height), range(width)):
    this_height = rows[i][j]
    if this_height < min([rows[x][y] for x, y in get_neighbours(i, j)]):
        low_points.add((i, j))

print('Part 1:', sum([1 + rows[i][j] for i, j in low_points]))

basins = []
for i, j in low_points:
    basin = {(i, j)}
    checked = basin.copy()
    to_check = get_neighbours(i, j)
    
    while len(to_check) > 0:
        x, y = to_check.pop()
        if rows[x][y] < 9:
            basin.add((x,y))
            checked.add((x,y))
            to_check.update(get_neighbours(x, y) - checked)
    
    basins.append(basin)

sizes = [len(basin) for basin in basins]
sizes.sort()

print('Part 2:', prod(sizes[-3:]))
