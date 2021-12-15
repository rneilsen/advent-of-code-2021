from collections import Counter

NUM_STEPS = 10
PRINT_STEPS = [0, 1, 2, 3, 4]

with open('input') as f:
    polymer = f.readline().strip()
    f.readline()
    rows = [row.strip().split(' -> ') for row in f.readlines()]

rules = {pair: addition for pair, addition in rows}

n = 0
while n < NUM_STEPS:
    if n in PRINT_STEPS:
        print(f'After step {n}: {polymer}')
    n += 1

    new_polymer = ''
    for i in range(len(polymer) - 1):
        new_polymer += polymer[i] + rules[polymer[i] + polymer[i+1]]
    new_polymer += polymer[-1]
    
    polymer = new_polymer

counts = Counter(polymer).most_common()
print('Part 1:', counts[0][1] - counts[-1][1])