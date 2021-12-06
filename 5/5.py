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

print(vents)

def find_crossings(vents: list[Vent]):
    num_rows = max([max(vent.start_x, vent.end_y) for vent in vents]) + 1
    num_cols = max([max(vent.start_y, vent.end_y) for vent in vents]) + 1
    
    crossings = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    for vent in vents:
        x_terms = {vent.start_x, vent.end_x}
        y_terms = {vent.start_y, vent.end_y}
        if vent.start_x == vent.end_x:
            i = vent.start_x
            for j in range(min(y_terms), max(y_terms) + 1):
                crossings[i][j] += 1
        elif vent.start_y == vent.end_y:
            j = vent.start_y
            for i in range(min(x_terms), max(x_terms) + 1):
                crossings[i][j] += 1
    
    return sum([len([x for x in row if x > 1]) for row in crossings])

print(f'Part 1: {find_crossings(vents)} crossings')