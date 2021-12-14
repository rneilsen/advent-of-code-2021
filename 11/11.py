from itertools import product
from functools import reduce

NUM_STEPS = [0, 100]


with open('input') as f:
    energy = [[int(ch) for ch in row.strip()] for row in f.readlines()]


height = len(energy)
width = len(energy[0])
valid_coords = set(product(range(height), range(width)))


def get_neighbours(x, y):
    return (set(product(range(x-1, x+2), range(y-1, y+2))) - {(x, y)}).intersection(valid_coords)


n = 0
total_flashed = 0
all_flashed = False
while n <= max(NUM_STEPS) or not all_flashed:
    if n in NUM_STEPS:
        print(f'\nAfter step {n} ({total_flashed} flashes total):')
        for row in energy:
            print(''.join([str(e) for e in row]))
    n += 1

    # step 1: increase all octopi energy by 1
    for i, j in valid_coords:
            energy[i][j] += 1

    # step 2: all octopi with energy greater than 9 flash
    to_check = valid_coords.copy()
    flashed = set()

    while to_check:
        i, j = to_check.pop()
        if (i, j) not in flashed and energy[i][j] > 9:
            flashed.add((i, j))
            total_flashed += 1
            neighbours = get_neighbours(i, j)
            for p, q in neighbours:
                energy[p][q] += 1
            to_check.update(neighbours)
    
    # step 3: all flashed octopi reset to 0
    for i, j in flashed:
        energy[i][j] = 0
    
    if flashed == valid_coords:
        all_flashed = True
        print(f'All flashed on step {n}')
