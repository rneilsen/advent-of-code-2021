with open('input') as f:
    rows = [tuple(row.strip().split('-')) for row in f.readlines()]

links_from = {}
small_caves = set()
for orig, term in rows:
    for cave in (orig, term):
        if cave.lower() == cave:
            small_caves.add(cave)
        if cave not in links_from:
            links_from[cave] = set()
    
    if orig != 'end' and term != 'start':
        links_from[orig].add(term)
    if orig != 'start' and term != 'end':
        links_from[term].add(orig)


def allowed_no_dup(path: list[str]) -> bool:
    """Returns True if no small cave is visited multiple times,
    and False otherwise."""
    for cave in small_caves:
        if path.count(cave) > 1:
            return False
    return True


def allowed_one_dup(path: list[str]) -> bool:
    """Returns True if at most one cave is visited multiple times,
    and twice at most. Returns False otherwise."""
    small_cave_dup = False
    for cave in small_caves:
        count = path.count(cave)
        if count > 2:
            return False
        if count > 1:
            if small_cave_dup:
                return False
            small_cave_dup = True
    return True

parts = ((1, allowed_no_dup), (2, allowed_one_dup))

for (part_num, allow_func) in parts:
    explore_queue = [['start', term] for term in links_from['start']]
    complete_paths = []
    while explore_queue:
        current_path = explore_queue.pop()
        current_term = current_path[-1]
        if current_term == 'end':
            complete_paths.append(current_path)
        else:
            for term in links_from[current_term]:
                if allow_func(current_path + [term]):
                    explore_queue.append(current_path + [term])

    print(f'Part {part_num}: {len(complete_paths)}')
