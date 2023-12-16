N, E, S, W = 0, 1, 2, 3
redirects = {
    '.': {N: [(0, -1, N)], E: [(1, 0, E)], S: [(0, 1, S)], W: [(-1, 0, W)]},
    '/': {N: [(1, 0, E)], E: [(0, -1, N)], S: [(-1, 0, W)], W: [(0, 1, S)]},
    '\\': {N: [(-1, 0, W)], E: [(0, 1, S)], S: [(1, 0, E)], W: [(0, -1, N)]},
    '|': {N: [(0, -1, N)], E: [(0, -1, N), (0, 1, S)], S: [(0, 1, S)], W: [(0, -1, N), (0, 1, S)]},
    '-': {N: [(1, 0, E), (-1, 0, W)], E: [(1, 0, E)], S: [(1, 0, E), (-1, 0, W)], W: [(-1, 0, W)]}
}

with open('16.txt', 'r') as in_file:
    lines = in_file.read().split('\n')
    max_y, max_x = len(lines), len(lines[0])
counter_1 = 0
counter_2 = 0
starting_points = [
    *[(x, 0, S) for x in range(max_x)],
    *[(x, max_y - 1, N) for x in range(max_x)],
    *[(0, y, E) for y in range(max_y)],
    *[(max_x - 1, y, W) for y in range(max_y)],
]
for starting_point in starting_points:
    beams = [starting_point]
    visited_tiles = set()
    visited_beams = set()
    counter_1 = 0
    while len(beams):
        x, y, d = beams.pop()
        visited_beams.add((x, y, d))
        visited_tiles.add((x, y))
        for dx, dy, new_dir in redirects[lines[y][x]][d]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < max_x and 0 <= new_y < max_y and (new_x, new_y, new_dir) not in visited_beams:
                beams.append((new_x, new_y, new_dir))
    if (counter_1 := len(visited_tiles)) > counter_2:
        counter_2 = counter_1
    if starting_point == (0, 0, E):
        print(counter_1)
print(counter_2)
