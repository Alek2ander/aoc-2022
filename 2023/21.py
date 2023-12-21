from collections import deque

goal_1 = 64
goal_2 = 26501365
with (open('21.txt', 'r') as in_file):
    starting_point = None
    grid = [line for line in in_file.read().split('\n')]
    max_y, max_x = len(grid), len(grid[0])
    even_full = odd_full = 0
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c != '#':
                if (x + y) % 2 == 0:
                    even_full += 1
                else:
                    odd_full += 1
        if (x := line.find('S')) != -1:
            starting_point = (x, y)
    max_y, max_x = len(grid), len(grid[0])
queue = deque([starting_point])
visited = {starting_point: 0}
goals = [goal_1, max_x // 2, max_x // 2 + max_x]
counts = [0, 0, 0]
while len(queue):
    x, y = queue.popleft()
    steps = visited[x, y]
    if steps > goals[-1]:
        continue
    for i, goal in enumerate(goals):
        if steps <= goal and (goal - steps) % 2 == 0:
            counts[i] += 1
    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        if grid[ny % max_y][nx % max_x] == '#' or (nx, ny) in visited:
            continue
        visited[nx, ny] = steps + 1
        queue.append((nx, ny))

result_1, odd_inner, fx1 = tuple(counts)
print(result_1)
even_outer = fx1 - 2 * odd_full - 2 * odd_inner - even_full
x = (goal_2 - (max_x // 2)) // max_x
result_2 = (x + 1) * x * odd_full + (x + 1) * odd_inner + x * x * even_full + x * even_outer - x * (x - 1)
print(result_2)
