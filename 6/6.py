DAYS = [18, 80, 256]

with open('input') as f:
    fish = [int(val) for val in f.read().split(',')]

num_fish = [fish.count(i) for i in range(9)]

for j in range(max(DAYS) + 1):
    if j in DAYS:
        print(j, 'days:', sum(num_fish))
    
    num_breeding = num_fish.pop(0)
    num_fish.append(num_breeding)
    num_fish[6] += num_breeding
