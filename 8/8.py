from itertools import permutations

DIGITS_STANDARD = { 0: 'abcefg', 1: 'cf', 2: 'acdeg', 3: 'acdfg', 4: 'bcdf',
                    5: 'abdfg', 6: 'abdefg', 7: 'acf', 8: 'abcdefg', 9: 'abcdfg'}
DIGITS_LOOKUP = {val: str(key) for key, val in DIGITS_STANDARD.items()}

STANDARD_STRING = ' '.join(DIGITS_STANDARD.values())
STANDARD_SET = set(DIGITS_STANDARD.values())
LETTERS = 'abcdefg'

def strsort(s):
    return ''.join(sorted(list(s)))

with open('input') as f:
    rows = [row.strip() for row in f.readlines()]

entries = []
for row in rows:
    (digits, output) = row.split(' | ')
    entries.append(({strsort(digit) for digit in digits.split(' ')}, output.split(' ')))

total = 0
for digits, output in entries:
    total += len([out for out in output if len(out) in [2, 3, 4, 7]])

print('Part 1:', total)

total = 0
for digits, output in entries:    
    for perm in permutations(LETTERS):
        trans = str.maketrans(LETTERS, ''.join(perm))
        if {strsort(digit.translate(trans)) for digit in STANDARD_SET} == digits:
            break
    trans = str.maketrans(''.join(perm), LETTERS)
    
    total += int(''.join([DIGITS_LOOKUP[strsort(out_dig.translate(trans))] for out_dig in output]))

print('Part 2:', total)
