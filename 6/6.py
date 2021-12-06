DAYS = [18, 80, 256]

with open('input') as f:
    fish = [int(val) for val in f.read().split(',')]

num_fish = [fish.count(i) for i in range(8)]

for j in range(max(DAYS) + 1):
    new_num_fish = [0] * 6 + [num_fish[0]] + [0] + [num_fish[0]]
    for i in range(1, len(num_fish)):
        new_num_fish[i-1] += num_fish[i]
    num_fish = new_num_fish

    if j in DAYS:
        print(j, 'days:', sum(num_fish))
