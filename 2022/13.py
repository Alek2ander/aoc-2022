import json
from functools import cmp_to_key


def cmp(l, r):
    match l, r:
        case int(a), int(b):
            return (a > b) - (a < b)
        case int(a), [*b]:
            return cmp([a], [*b])
        case [*a], int(b):
            return cmp([*a], [b])
        case [*a], [*b]:
            for aa, bb in zip(a, b):
                if x := cmp(aa, bb):
                    return x
            return (len(a) > len(b)) - (len(a) < len(b))


total_part1 = 0
dividers = [[2]], [[6]]
all_entries = [*dividers]
with open('13.txt', 'r') as in_file:
    for i, (first, second) in enumerate(zip((lines := in_file.readlines())[::3], lines[1::3]), start=1):
        l, r = map(json.loads, (first, second))
        if (x := cmp(l, r)) == -1:
            total_part1 += i
        all_entries += (l, r)
all_entries.sort(key=cmp_to_key(cmp))
prod_part2 = (all_entries.index(dividers[0]) + 1) * (all_entries.index(dividers[1]) + 1)

print(total_part1)
print(prod_part2)
