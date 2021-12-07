with open('input') as f:
    positions = [int(val) for val in f.read().split(',')]

def calc_triang(n):
    return n * (n + 1) // 2

p1_fuel_reqs = []
p2_fuel_reqs = []
for possible_best in range(min(positions), max(positions)):
    p1_fuel_reqs.append(sum([abs(pos - possible_best) for pos in positions]))
    p2_fuel_reqs.append(sum([calc_triang(abs(pos - possible_best)) for pos in positions]))

print("Part 1:", min(p1_fuel_reqs))
print("Part 2:", min(p2_fuel_reqs))
