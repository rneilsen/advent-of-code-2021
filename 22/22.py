import re

with open('test2') as f:
    rows = [row.strip() for row in f.readlines()]

class Cuboid:
    def __init__(self, *args):
        self.ranges = []
        for coord_range in args:
            if isinstance(coord_range, range):
                self.ranges.append(coord_range)
            else:
                vals = [int(val) for val in coord_range]
                self.ranges.append(range(min(vals), max(vals) + 1))
    
    def __str__(self):
        return 'Cuboid(' + ','.join([f'({min(r)},{max(r)})' for r in self.ranges]) + ')'

    def __repr__(self):
        return self.__str__()

def intersect(a: Cuboid, b: Cuboid) -> tuple[list[Cuboid], Cuboid, list[Cuboid]]:
    """Returns a tuple of a list of cuboids, a cuboid, and a list of cuboids,
    where the first list is a excluding b decomposed into a list of cuboids,
    the second list is b excluding a decomposed into a list of cuboids, and
    the cuboid between then is the intersection cuboid of a and b"""
    if len(a.ranges) != len(b.ranges):
        return ValueError
    
    num_dims = len(a.ranges)
    if num_dims == 0:
        return ([a], None, [b])

    for i in range(num_dims):
        # if any dimension has zero overlap, the cuboids do not intersect at all
        if min(a.ranges[i]) > max(b.ranges[i]) or max(a.ranges[i]) < min(b.ranges[i]):
            return ([], a, [])
    
    a_rem = []
    b_rem = []

    a_min, a_max = min(a.ranges[0]), max(a.ranges[0])
    b_min, b_max = min(b.ranges[0]), max(b.ranges[0])

    if a_min < b_min:
        a_rem.append(Cuboid((a_min, b_min - 1), *a.ranges[1:]))
        a_min = b_min
        a = Cuboid((a_min, a_max), *a.ranges[1:])
    elif b_min < a_min:
        b_rem.append(Cuboid((b_min, a_min - 1), *b.ranges[1:]))
        b_min = a_min
        b = Cuboid((b_min, b_max), *b.ranges[1:])
    
    if a_max > b_max:
        a_rem.append(Cuboid((b_max + 1, a_max), *a.ranges[1:]))
        a_max = b_max
        a = Cuboid((a_min, a_max), *a.ranges[1:])
    elif b_max > a_max:
        b_rem.append(Cuboid((a_max + 1, b_max), *b.ranges[1:]))
        b_max = a_max
        b = Cuboid((b_min, b_max), *b.ranges[1:])
    
    if num_dims == 1:
        return (a_rem, a, b_rem)
    
    a_subrems, intersection, b_subrems = intersect(Cuboid(*a.ranges[1:]), Cuboid(*b.ranges[1:]))
    a_rem += [Cuboid((a_min, a_max), *c.ranges) for c in a_subrems]
    b_rem += [Cuboid((b_min, b_max), *c.ranges) for c in b_subrems]
    intersection = Cuboid((a_min, a_max), *intersection.ranges)
    
    return (a_rem, intersection, b_rem)


blocks = []
for row in rows:
    mode, coords = row.split(' ')
    raw_ranges = coords.split(',')
    ranges = []
    for r in raw_ranges:
        m = re.match(r'\w=([-\d]+)..([-\d]+)', r)
        ranges.append(m.groups())
    blocks.append(((1 if mode == 'on' else 0), *ranges))

print(blocks)