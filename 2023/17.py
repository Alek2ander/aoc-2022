from heapq import heappop, heappush

directions = {
    0: (0, -1),  # North
    1: (1, 0),   # East
    2: (0, 1),   # South
    3: (-1, 0)   # West
}

with open('17.txt', 'r') as in_file:
    lines = in_file.read().split('\n')
    max_y, max_x = len(lines), len(lines[0])
    max_heat = max_y * max_x * 10
loss = [[int(c) for c in line] for line in lines]


def find_path(goal, min_to_turn, max_to_turn):
    grid = [[[max_heat] * len(directions) for __ in range(max_x)] for _ in range(max_y)]
    grid_visited = [[[False] * len(directions) for __ in range(max_x)] for _ in range(max_y)]
    grid[0][0] = [0] * len(directions)
    process = [(0, 0, 0, 1), (0, 0, 0, 2)]
    while len(process):
        dist, x, y, d = heappop(process)
        if (x, y) == goal:
            return dist
        if grid_visited[y][x][d]:
            continue
        else:
            grid_visited[y][x][d] = True
        dx, dy = directions[d]
        for n in range(1, max_to_turn + 1):
            if (nx := x + n * dx) < 0 or nx >= max_x or (ny := y + n * dy) < 0 or ny >= max_y:
                break
            dist += loss[ny][nx]
            if n < min_to_turn:
                continue
            for nd in ((d - 1) % 4, (d + 1) % 4):
                if dist < grid[ny][nx][nd]:
                    grid[ny][nx][nd] = dist
                    heappush(process, (dist, nx, ny, nd))


print(find_path((max_x - 1, max_y - 1), 1, 3))
print(find_path((max_x - 1, max_y - 1), 4, 10))
