with open('input') as f:
    instrs = [l.split() for l in f.readlines()]

p1depth, p1pos = 0, 0
p2depth, p2pos, p2aim = 0, 0, 0

for (instr, val) in instrs:
    val = int(val)
    match instr:
        case 'forward':
            p1pos += val
            p2pos += val
            p2depth += p2aim * val
        case 'down':
            p1depth += val
            p2aim += val
        case 'up':
            p1depth -= val
            p2aim -= val

print(f'Part 1: depth = {p1depth}, pos = {p1pos}, product = {p1depth * p1pos}')
print(f'Part 2: depth = {p2depth}, pos = {p2pos}, product = {p2depth * p2pos}')
