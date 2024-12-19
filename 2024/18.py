from heapq import heappop, heappush

max_x = max_y = 70
start, goal = (0, 0), (max_x, max_y)
with open('18.txt', 'r') as in_file:
    blocks = [tuple(map(int, line.strip().split(','))) for line in in_file.readlines()]

def a_star(a, b, obstacles):
    queue = [(abs(a[0] - b[0]) + abs(a[1] - b[1]), 0, a)]
    done = set()
    while len(queue):
        _, steps, pos = heappop(queue)
        if pos == b:
            return steps
        if pos in done:
            continue
        done.add(pos)
        for x1, y1 in ((pos[0], pos[1] - 1), (pos[0] + 1, pos[1]), (pos[0], pos[1] + 1), (pos[0] - 1, pos[1])):
            if x1 < 0 or x1 > max_x or y1 < 0 or y1 > max_y or (pos1 := (x1, y1)) in done or pos1 in obstacles:
                continue
            heappush(queue, (steps + 1 + abs(pos1[0] - b[0]) + abs(pos1[1] - b[1]), steps + 1, pos1))
    return None

print(a_star(start, goal, {x for x in blocks[:1024]}))
l, r = 1024, len(blocks)
while r > l + 1:
    m = (l + r) // 2
    if a_star(start, goal, {x for x in blocks[:m + 1]}) is None:
        r = m
    else:
        l = m
print(','.join(map(str, blocks[r])))
