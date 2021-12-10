from numpy import median

MATCH =         {'(': ')',  '[': ']',   '{': '}',   '<': '>'}
ERR_SCORES =    {')': 3,    ']': 57,    '}': 1197,  '>': 25137}
FIX_SCORES =    {')': 1,    ']': 2,     '}': 3,     '>': 4}

with open('input') as f:
    rows = [row.strip() for row in f.readlines()]

err_total = 0
fix_scores = []

for row in rows:
    expected = []
    invalid = False
    for ch in row:
        if ch in MATCH.keys():
            expected.append(MATCH[ch])
        else:
            if ch != expected.pop():
                err_total += ERR_SCORES[ch]
                invalid = True
                break
    if invalid:
        continue

    row_score = 0
    expected.reverse()
    for ch in expected:
        row_score *= 5
        row_score += FIX_SCORES[ch]
    fix_scores.append(row_score)

print('Part 1:', err_total)
print('Part 2:', int(median(fix_scores)))
