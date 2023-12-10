tile_definitions = {
    '|': {'connections': [(0, -1), (0, 1)], 'neighbors': [[(-1, 0)], [(1, 0)]], 'rotation': 0},
    '-': {'connections': [(1, 0), (-1, 0)], 'neighbors': [[(0, -1)], [(1, 0)]], 'rotation': 0},
    'L': {'connections': [(0, -1), (1, 0)], 'neighbors': [[(-1, 0), (0, 1), (-1, 1)], []], 'rotation': 1},
    'J': {'connections': [(-1, 0), (0, -1)], 'neighbors': [[(1, 0), (0, 1), (1, 1)], []], 'rotation': 1},
    '7': {'connections': [(0, 1), (-1, 0)], 'neighbors': [[(1, 0), (0, -1), (1, -1)], []], 'rotation': 1},
    'F': {'connections': [(1, 0), (0, 1)], 'neighbors': [[(-1, 0), (0, -1), (-1, -1)], []], 'rotation': 1}
}

with open('10.txt', 'r') as in_file:
    grid = []
    starting_point = None
    for y, line in enumerate(in_file):
        if (x := line.find('S')) != -1:
            starting_point = (x, y)
        grid.append(line.rstrip())

prev_x, prev_y = cur_x, cur_y = starting_point
starting_connections = []
for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
    if (y := starting_point[1] + dy) < 0 or y >= len(grid):
        continue
    if (x := starting_point[0] + dx) < 0 or x >= len(grid[y]):
        continue
    if grid[y][x] not in tile_definitions:
        continue
    if (-dx, -dy) in tile_definitions[grid[y][x]]['connections']:
        starting_connections.append((dx, dy))
        prev_x, prev_y = cur_x + dx, cur_y + dy
for tile, data in tile_definitions.items():
    if data['connections'] == starting_connections or data['connections'] == starting_connections[::-1]:
        grid[cur_y] = ''.join((grid[cur_y][:cur_x], tile, grid[cur_y][cur_x + 1:]))
        break

loop = set()
neighbors_left = set()
neighbors_right = set()
rotation = 0
while True:
    loop.add((cur_x, cur_y))
    tile_data = tile_definitions[grid[cur_y][cur_x]]
    if (prev_x - cur_x, prev_y - cur_y) == tile_data['connections'][1]:
        neighbors_left |= set((cur_x + dx, cur_y + dy) for dx, dy in tile_data['neighbors'][0])
        neighbors_right |= set((cur_x + dx, cur_y + dy) for dx, dy in tile_data['neighbors'][1])
        rotation += tile_data['rotation']
        next_x, next_y = cur_x + tile_data['connections'][0][0], cur_y + tile_data['connections'][0][1]
    else:
        neighbors_left |= set((cur_x + dx, cur_y + dy) for dx, dy in tile_data['neighbors'][1])
        neighbors_right |= set((cur_x + dx, cur_y + dy) for dx, dy in tile_data['neighbors'][0])
        rotation -= tile_data['rotation']
        next_x, next_y = cur_x + tile_data['connections'][1][0], cur_y + tile_data['connections'][1][1]
    cur_x, cur_y, prev_x, prev_y = next_x, next_y, cur_x, cur_y
    if (cur_x, cur_y) == starting_point:
        break
print(len(loop) // 2)

in_loop_done = set()
if rotation == 4:
    in_loop = neighbors_right - loop
else:
    in_loop = neighbors_left - loop
while len(in_loop):
    point = in_loop.pop()
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if (p := (point[0] + dx, point[1] + dy)) in loop or p in in_loop or p in in_loop_done:
            continue
        in_loop.add(p)
    in_loop_done.add(point)
print(len(in_loop_done))
