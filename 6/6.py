NUM_DAYS = 80

with open('test1') as f:
    fish = [int(val) for val in f.read().split(',')]

for _ in range(NUM_DAYS):
    new_fish = 0
    for i in range(len(fish)):
        if fish[i] == 0:
            fish[i] = 6
            new_fish += 1
        else:
            fish[i] -= 1
    fish += [8] * new_fish

print(len(fish))