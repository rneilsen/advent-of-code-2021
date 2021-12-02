def count_increases(l: list) -> int:
    count = 0
    for i in range(len(l) - 1):
        if l[i+1] > l[i]:
            count += 1
    return count


with open('input') as f:
    values = [int(l.strip()) for l in f.readlines()]

sliding_sums = [sum(values[i:i+3]) for i in range(len(values) - 2)]

print(count_increases(values))
print(count_increases(sliding_sums))
