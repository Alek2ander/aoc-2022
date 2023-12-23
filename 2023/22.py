from heapq import heappush, heappop
from itertools import product

bricks = []
with open('22.txt', 'r') as in_file:
    for i, line in enumerate(in_file):
        left, right = line.rstrip().split('~')
        x1, y1, z1 = map(int, left.split(','))
        x2, y2, z2 = map(int, right.split(','))
        heappush(bricks, (z1, i, (x1, y1, z1), (x2, y2, z2)))

projection = {}
below = {}
above = {}
while len(bricks):
    _, i, (x1, y1, z1), (x2, y2, z2) = heappop(bricks)
    cur_support_height = 0
    cur_supports = set()
    for x, y in product(range(x1, x2 + 1), range(y1, y2 + 1)):
        if (x, y) in projection:
            if projection[x, y][0] == cur_support_height:
                cur_supports.add(projection[x, y][1])
            elif projection[x, y][0] > cur_support_height:
                cur_support_height = projection[x, y][0]
                cur_supports = {projection[x, y][1]}
    for x, y in product(range(x1, x2 + 1), range(y1, y2 + 1)):
        projection[x, y] = (cur_support_height + z2 - z1 + 1, i)
    check_below = cur_supports.copy()
    while len(check_below):
        below_i = check_below.pop()
        if all(support in above[below_i] for support in cur_supports):
            above[below_i].add(i)
        check_below |= below[below_i]
    below[i] = cur_supports
    above[i] = {i}
print(sum(1 for s in above.values() if len(s) == 1))
print(sum(len(s) - 1 for s in above.values()))
