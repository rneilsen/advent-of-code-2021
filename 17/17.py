import re

MAX_START_VEL = 300

with open('input') as f:
    row = f.readline().strip()

m = re.search(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)', row)
x_targ = range(int(m.group(1)), int(m.group(2))+1)
y_targ = range(int(m.group(3)), int(m.group(4))+1)

valid_trajs = {}

for start_yv in range(-MAX_START_VEL, MAX_START_VEL):
    for start_xv in range(MAX_START_VEL):
        xv, yv = start_xv, start_yv
        x, y = 0, 0
        heights = set()

        while x < max(x_targ) and (yv > 0 or y >= min(y_targ)):
            x += xv
            y += yv
            heights.add(y)
            
            if xv > 0:
                xv -= 1
            elif xv < 0:
                xv += 1
            yv -= 1

            if x in x_targ and y in y_targ:
                valid_trajs[(start_xv, start_yv)] = max(heights)

print('Part 1:', max(valid_trajs.values()))
print('Part 2:', len(valid_trajs))
