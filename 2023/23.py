directions = {
    '.': [(0, -1), (0, 1), (-1, 0), (1, 0)],
    '>': [(1, 0)],
    '<': [(-1, 0)],
    '^': [(0, -1)],
    'v': [(0, 1)]
}

with open('23.txt', 'r') as in_file:
    grid = [line.rstrip() for line in in_file]
max_y, max_x = len(grid), len(grid[0])
starting_point = (grid[0].find('.'), 0)


def find_path(ignore_slopes):
    path_cache = {starting_point: {(starting_point[0], starting_point[1] + 1): None}}
    max_dist = 0
    process = [(starting_point, {starting_point}, 0)]
    while len(process):
        node, visited, dist = process.pop()
        if node[1] == max_y - 1:
            if dist >= max_dist:
                max_dist = dist
            continue
        for step in path_cache[node]:
            if path_cache[node][step] is not None:
                end, path_dist = path_cache[node][step]
                if end is not None and end not in visited:
                    process.append((end, visited | {end}, dist + path_dist))
                continue
            x, y = step
            last_x, last_y = node
            path_dist = 1
            while True:
                check_directions = []
                for dx, dy in directions['.'] if ignore_slopes else directions[grid[y][x]]:
                    if (0 <= (nx := x + dx) < max_x and 0 <= (ny := y + dy) < max_y
                            and grid[ny][nx] != '#' and (nx != last_x or ny != last_y)):
                        check_directions.append((nx, ny))
                if not check_directions:
                    path_cache[node][step] = None, 0
                    break
                elif len(check_directions) == 1 and check_directions[0][1] != max_y - 1:
                    nx, ny = check_directions[0]
                    x, y, last_x, last_y = nx, ny, x, y
                    path_dist += 1
                elif check_directions[0][1] == max_y - 1:
                    path_cache[node][step] = check_directions[0], path_dist + 1
                    break
                else:
                    if (end := (x, y)) not in path_cache:
                        path_cache[end] = {d: None for d in check_directions + [(last_x, last_y)]}
                    path_cache[node][step] = end, path_dist
                    if ignore_slopes:
                        path_cache[end][last_x, last_y] = node, path_dist
                    if end not in visited:
                        process.append((end, visited | {end}, dist + path_dist))
                    break
    return max_dist


print(find_path(False))
print(find_path(True))
