from collections import deque

goal_1 = 64
goal_2 = 26501365
with (open('21.txt', 'r') as in_file):
    starting_point = None
    grid = [line for line in in_file.read().split('\n')]
    max_y, max_x = len(grid), len(grid[0])
    for y, line in enumerate(grid):
        if (x := line.find('S')) != -1:
            starting_point = (x, y)
    max_y, max_x = len(grid), len(grid[0])
queue = deque([starting_point])
visited = {starting_point: 0}
goals = [goal_1, max_x // 2 + max_x * 2]
zone_counts = [{(x, y): 0 for x in range(-3, 4) for y in range(-3, 4)} for _ in range(len(goals))]
while len(queue):
    x, y = queue.popleft()
    steps = visited[x, y]
    if steps > goals[-1]:
        continue
    for i, goal in enumerate(goals):
        if steps <= goal and (goal - steps) % 2 == 0:
            zone_counts[i][(x // max_x, y // max_y)] += 1
    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        if grid[ny % max_y][nx % max_x] == '#' or (nx, ny) in visited:
            continue
        visited[nx, ny] = steps + 1
        queue.append((nx, ny))

print(zone_counts[0][0, 0])

#  0      n     1     n     0
#     /     .       .    \
#  n     n-1   n^2   n-1    n
#       .    /     \    .
#  1     n^2 (n-1)^2 n^2    1
#       .    \     /    .
#  n     n-1   n^2   n-1    n
#      \    .       .    /
#  0      n     1     n     0
x = (goal_2 - (max_x // 2)) // max_x
parts = zone_counts[1]
print(parts[0, 0] * (x - 1) * (x - 1) + parts[0, 1] * x * x
      + (parts[1, 1] + parts[1, -1] + parts[-1, 1] + parts[-1, -1]) * (x - 1)
      + (parts[2, 0] + parts[-2, 0] + parts[0, 2] + parts[0, -2])
      + (parts[2, 1] + parts[2, -1] + parts[-2, 1] + parts[-2, -1]) * x
      )
