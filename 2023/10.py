tile_definitions = {
    '|': ((0, -1), (0, 1)),
    '-': ((1, 0), (-1, 0)),
    'L': ((0, -1), (1, 0)),
    'J': ((-1, 0), (0, -1)),
    '7': ((0, 1), (-1, 0)),
    'F': ((1, 0), (0, 1))
}

with open('10.txt', 'r') as in_file:
    grid = []
    starting_point = None
    for y, line in enumerate(in_file):
        if (x := line.find('S')) != -1:
            starting_point = (x, y)
        grid.append(line.rstrip())

prev_x, prev_y = cur_x, cur_y = starting_point
for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
    if (y := starting_point[1] + dy) < 0 or y >= len(grid):
        continue
    if (x := starting_point[0] + dx) < 0 or x >= len(grid[y]):
        continue
    if grid[y][x] not in tile_definitions:
        continue
    if (-dx, -dy) in tile_definitions[grid[y][x]]:
        cur_x, cur_y = x, y

y = area = edges = 0
while True:
    edges += 1
    area += cur_y * (cur_x - prev_x)
    if (cur_x, cur_y) == starting_point:
        break
    tile_data = tile_definitions[grid[cur_y][cur_x]]
    if (prev_x - cur_x, prev_y - cur_y) == tile_data[1]:
        next_x, next_y = cur_x + tile_data[0][0], cur_y + tile_data[0][1]
    else:
        next_x, next_y = cur_x + tile_data[1][0], cur_y + tile_data[1][1]
    cur_x, cur_y, prev_x, prev_y = next_x, next_y, cur_x, cur_y

print(edges // 2)
print(abs(area) - edges // 2 + 1)
