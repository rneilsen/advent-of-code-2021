from math import ceil

def freq_at_pos(char: str, strings: list[str], pos: int) -> int:
    """Determins the frequency of a given char at a given pos in a list of strings"""
    return [s[pos] for s in strings].count(char)


with open('input') as f:
    rows = [r.strip() for r in f.readlines()]

num_bits = len(rows[0])

gamma = ''.join([('1' if freq_at_pos('1', rows, i) >= (len(rows) + 1) // 2 else '0') 
        for i in range(num_bits)])
epsilon = ''.join([('0' if ch == '1' else '1') for ch in gamma])

print(f'Part 1: 0b{gamma} * 0b{epsilon} = {int(gamma, base=2) * int(epsilon, base=2)}')


def partition_by_pos(nums: list[str], pos: int) -> tuple[list[str], list[str]]:
    """Partitions the given list into two lists, one all the nums that have 0 
    at the given pos, the other all the nums with 1 at the given pos"""
    return ([s for s in nums if s[pos] == '0'], [s for s in nums if s[pos] == '1'])


def churn_list(lst: list[str], keep: int) -> str:
    """Does the weird list crunching thing until there's one number, returns that. 
    Use keep=1 for oxygen generator rating, keep=0 for CO2 scrubber rating"""
    i = 0
    while len(lst) > 1:
        part = partition_by_pos(lst, i)
        if len(part[1]) >= len(part[0]):
            lst = part[keep]
        else:
            lst = part[1 - keep]
        i += 1
    return lst[0]


og_list = rows
cs_list = rows.copy()

og_rating = churn_list(og_list, 1)
cs_rating = churn_list(cs_list, 0)

print(f'Part 2: 0b{og_rating} * 0b{cs_rating} = {int(og_rating, base=2) * int(cs_rating, base=2)}')
