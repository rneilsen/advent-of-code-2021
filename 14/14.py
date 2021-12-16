from collections import Counter

PRINT_STEPS = (10, 40)

with open('input') as f:
    polymer = f.readline().strip()
    f.readline()
    rows = [row.strip().split(' -> ') for row in f.readlines()]

# 'CH -> B' translates to rules dict as {'CH': ('CB', 'BH')}
rules = {pair: (pair[0] + addition, addition + pair[1]) for pair, addition in rows}

pair_counts = Counter([polymer[i:i+2] for i in range(len(polymer) - 1)])

n = 0
while n < max(PRINT_STEPS):
    n += 1

    new_pair_counts = Counter()
    for pair, count in pair_counts.items():
        for result in rules[pair]:
            new_pair_counts[result] += count

    pair_counts = new_pair_counts

    if n in PRINT_STEPS:
        letter_counts = Counter()
        for pair, count in pair_counts.items():
            for letter in pair:
                letter_counts[letter] += count

        # all letters are doublecounted since they're counted in every pair
        for letter in letter_counts:
            letter_counts[letter] //= 2
        
        # adjust first and last letters since they're only counted in one pair
        letter_counts[polymer[0]] += 1
        letter_counts[polymer[-1]] += 1

        common = letter_counts.most_common()
        print(f'After {n} steps:', common[0][1] - common[-1][1])
