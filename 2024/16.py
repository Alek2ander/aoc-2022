from heapq import heappop, heappush

directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
obstacles = set()
step_cost, turn_cost = 1, 1000
start = goal = None
with open('16.txt', 'r') as in_file:
    for y, line in enumerate(in_file.readlines()):
        for x, c in enumerate(line.strip()):
            match c:
                case '#':
                    obstacles.add((x, y))
                case 'S':
                    start = (x, y)
                case 'E':
                    goal = (x, y)

queue = [(0, start[0], start[1], 0, (start[0], start[1], 0))]
done = {}
while len(queue):
    points, x, y, d, prev_idx = heappop(queue)
    if (idx := (x, y, d)) in done:
        if done[idx][0] == points:
            done[idx][1].add(prev_idx)
        continue
    done[idx] = (points, {prev_idx})
    if (x1 := x, y1 := y, d1 := (d + 1) % len(directions)) not in done:
        heappush(queue, (points + turn_cost, x1, y1, d1, idx))
    if (x1 := x, y1 := y, d1 := (d - 1) % len(directions)) not in done:
        heappush(queue, (points + turn_cost, x1, y1, d1, idx))
    if (x1 := x + directions[d][0], y1 := y + directions[d][1], d1 := d) not in done and (x1, y1) not in obstacles:
        heappush(queue, (points + step_cost, x1, y1, d1, idx))
min_goal_points = min(done[(goal[0], goal[1], d)][0] for d in range(len(directions)))
min_path_set, min_path_backtrace_process, min_path_backtrace_done = set(), set(), set()
for d in range(len(directions)):
    if done[(goal[0], goal[1], d)][0] == min_goal_points:
        min_path_backtrace_process.add((goal[0], goal[1], d))
while len(min_path_backtrace_process):
    idx = min_path_backtrace_process.pop()
    min_path_backtrace_done.add(idx)
    min_path_set.add((idx[0], idx[1]))
    for parent in done[idx][1]:
        if parent in min_path_backtrace_done:
            continue
        min_path_backtrace_process.add(parent)

print(min_goal_points)
print(len(min_path_set))
