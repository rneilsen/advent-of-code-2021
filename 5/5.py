Terminus = tuple[int, int]

class Vent:
    def __init__(self, start: Terminus, end: Terminus):
        self.start_x, self.start_y = int(start[0]), int(start[1])
        self.end_x, self.end_y = int(end[0]), int(end[1])
    
    def __repr__(self):
        return f'({self.start_x}, {self.start_y}) -> ({self.end_x}, {self.end_y})'

with open('input') as f:
    rows = list(filter(None, [row.strip() for row in f.readlines()]))

vents = []
for row in rows:
    start, end = row.split(' -> ')
    vents.append(Vent(start.split(',')[::-1], end.split(',')[::-1]))


def find_crossings(vents: list[Vent], count_diags=False):
    num_rows = max([max(vent.start_x, vent.end_y) for vent in vents]) + 1
    num_cols = max([max(vent.start_y, vent.end_y) for vent in vents]) + 1
    
    crossings = [[0 for _ in range(num_cols)] for _ in range(num_rows)]
    calc_step = lambda x, y: (0 if x == y else (1 if x > y else -1))

    for vent in vents:
        if not count_diags and vent.start_x != vent.end_x and vent.start_y != vent.end_y:
            continue

        x, y = vent.start_x, vent.start_y
        x_step = calc_step(vent.end_x, vent.start_x)
        y_step = calc_step(vent.end_y, vent.start_y)
        x_range = range(min(vent.start_x, vent.end_x), max(vent.start_x, vent.end_x) + 1)
        y_range = range(min(vent.start_y, vent.end_y), max(vent.start_y, vent.end_y) + 1)

        while x in x_range and y in y_range:
            crossings[x][y] += 1
            x += x_step
            y += y_step
    
    return sum([len([x for x in row if x > 1]) for row in crossings])


print(f'Part 1: {find_crossings(vents)} crossings')
print(f'Part 2: {find_crossings(vents, count_diags=True)} crossings')