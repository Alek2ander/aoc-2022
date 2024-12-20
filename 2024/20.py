def get_around(pos, d):
    for i in range(d):
        yield pos[0] + i, pos[1] - d + i
        yield pos[0] + d - i, pos[1] + i
        yield pos[0] - i, pos[1] + d - i
        yield pos[0] - d + i, pos[1] - i

with open('20.txt', 'r') as in_file:
    grid = []
    start = end = None
    for y, line in enumerate(in_file.readlines()):
        grid.append(l := line.strip())
        if (x := l.find('S')) != -1:
            start = (x, y)
        if (x := l.find('E')) != -1:
            end = (x, y)
path, pos, last_pos, idx = {start: 0}, start, None, 0
while pos != end:
    idx += 1
    for new_pos in get_around(pos, 1):
        if grid[new_pos[1]][new_pos[0]] != '#' and new_pos != last_pos:
            path[new_pos] = idx
            pos, last_pos = new_pos, pos
            break

count_1 = count_2 = 0
for cheat_from in path:
    for cheat_size in range(2, 21):
        for cheat_to in get_around(cheat_from, cheat_size):
            if cheat_to in path and path[cheat_to] - path[cheat_from] - cheat_size >= 100:
                if cheat_size == 2:
                    count_1 += 1
                else:
                    count_2 += 1
print(count_1)
print(count_1 + count_2)
