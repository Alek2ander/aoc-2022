dirs = ((0, -1), (1, 0), (0, 1), (-1, 0))

starting_position = None
obstacles = set()
with open('06.txt', 'r') as in_file:
    for y, line in enumerate(in_file.readlines()):
        for x, c in enumerate(line.strip()):
            match c:
                case '#':
                    obstacles.add((x, y))
                case '^':
                    starting_position = (x, y)
    max_x, max_y = x, y

def check_path_outer(pos, d):
    path = {}
    extra_obstacle_positions = set()
    while pos not in path or d not in path[pos]:
        if pos not in path:
            path[pos] = set()
        path[pos].add(d)
        next_pos = (pos[0] + dirs[d][0], pos[1] + dirs[d][1])
        if next_pos in obstacles:
            d = (d + 1) % len(dirs)
        elif next_pos[0] < 0 or next_pos[0] > max_x or next_pos[1] < 0 or next_pos[1] > max_y:
            return len(path), len(extra_obstacle_positions)
        else:
            if next_pos not in extra_obstacle_positions and next_pos not in path and check_path_inner(path, pos, (d + 1) % len(dirs), next_pos):
                extra_obstacle_positions.add(next_pos)
            pos = next_pos
    return len(path), len(extra_obstacle_positions)

def check_path_inner(pre_visited, pos, d, extra_obstacle):
    visited = {}
    while (pos not in pre_visited or d not in pre_visited[pos]) and (pos not in visited or d not in visited[pos]):
        if pos not in visited:
            visited[pos] = set()
        visited[pos].add(d)
        next_pos = (pos[0] + dirs[d][0], pos[1] + dirs[d][1])
        if next_pos in obstacles or next_pos == extra_obstacle:
            d = (d + 1) % len(dirs)
        elif next_pos[0] < 0 or next_pos[0] > max_x or next_pos[1] < 0 or next_pos[1] > max_y:
            return False
        else:
            pos = next_pos
    return True

part_1, part_2 = check_path_outer(starting_position, 0)
print(part_1)
print(part_2)
