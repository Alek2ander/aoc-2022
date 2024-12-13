from collections import deque

with open('12.txt', 'r') as in_file:
    grid = [line.strip() for line in in_file.readlines()]
    max_x = len(grid[0])
    max_y = len(grid)

def get_region(x, y):
    symbol = grid[y][x]
    area, perimeter, sides = 1, 4, 0
    region = {(x, y)}
    queue = deque(region)
    edges = [{}, {}, {}, {}]
    while queue:
        x, y = queue.popleft()
        for i, (x1, y1) in enumerate(((x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y))):
            if 0 <= x1 < max_x and 0 <= y1 < max_y and grid[y1][x1] == symbol:
                    perimeter -= 1
                    if (x1, y1) not in region:
                        region.add((x1, y1))
                        queue.append((x1, y1))
                        area += 1
                        perimeter += 4
            else:
                level, value = (y, x) if i % 2 == 0 else (x, y)
                if level not in edges[i]:
                    edges[i][level] = []
                edges[i][level].append(value)
    for edge_type in edges:
        for level in edge_type:
            sides += 1
            last_value = None
            for value in sorted(edge_type[level]):
                if last_value is not None and value != last_value + 1:
                    sides += 1
                last_value = value
    return region, area * perimeter, area * sides

visited = set()
sum_1 = sum_2 = 0
for y in range(max_y):
    for x in range(max_x):
        if (x, y) in visited:
            continue
        region, value_1, value_2 = get_region(x, y)
        visited |= region
        sum_1 += value_1
        sum_2 += value_2

print(sum_1)
print(sum_2)
