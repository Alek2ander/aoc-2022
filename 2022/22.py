RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3
shifts = {
    RIGHT: (0, 1),
    DOWN: (1, 0),
    LEFT: (0, -1),
    UP: (-1, 0)
}
turns = {
    'L': -1,
    'R': 1,
    'X': 0
}

cube_size = 50
with open('22.txt', 'r') as in_file:
    y = 1
    max_x = 0
    walls = set()
    warps = {}
    cube_points = set()
    x_limits = {}
    y_limits = {}
    start_pos = None
    while line := in_file.readline().strip('\n'):
        for x, char in enumerate(line, start=1):
            if char == ' ':
                if x in y_limits:
                    warps[(y, x, DOWN)] = (y_limits[x], x, DOWN)
                    warps[(y_limits[x] - 1, x, UP)] = (y - 1, x, UP)
                    del y_limits[x]
                if y in x_limits:
                    warps[(y, x, RIGHT)] = (y, x_limits[y], RIGHT)
                    warps[(y, x_limits[y] - 1, LEFT)] = (y, x - 1, LEFT)
                    del x_limits[y]
            else:
                if y % cube_size == 1 and x % cube_size == 1:
                    cube_points.add((y, x))
                if y not in x_limits:
                    x_limits[y] = x
                if x not in y_limits:
                    y_limits[x] = y
                if start_pos is None:
                    start_pos = (y, x, RIGHT)
                if char == '#':
                    walls.add((y, x))
        if y in x_limits:
            warps[(y, x + 1, RIGHT)] = (y, x_limits[y], RIGHT)
            warps[(y, x_limits[y] - 1, LEFT)] = (y, x, LEFT)
        if x > max_x:
            max_x = x
        if x < max_x:
            for xx in range(x + 1, max_x + 1):
                if xx in y_limits:
                    warps[(y, xx, DOWN)] = (y_limits[xx], xx, DOWN)
                    warps[(y_limits[xx] - 1, xx, UP)] = (y - 1, xx, UP)
                    del y_limits[xx]
            max_x = x
        y += 1
    for x in y_limits:
        warps[(y, x, DOWN)] = (y_limits[x], x, DOWN)
        warps[(y_limits[x] - 1, x, UP)] = (y - 1, x, UP)
    perimeter = []
    linked_coords = []
    outer_corners = {0}
    pos = face = start_pos
    while True:
        for i in range(cube_size):
            perimeter.append((pos[0] + shifts[pos[2]][0] * i, pos[1] + shifts[pos[2]][1] * i, pos[2]))
        if (face[0] + (shifts[pos[2]][0] + shifts[(pos[2] - 1) % len(shifts)][0]) * cube_size,
                face[1] + (shifts[pos[2]][1] + shifts[(pos[2] - 1) % len(shifts)][1]) * cube_size) in cube_points:
            linked_coords.append((len(perimeter) - 1, len(perimeter)))
            face = (face[0] + (shifts[pos[2]][0] + shifts[(pos[2] - 1) % len(shifts)][0]) * cube_size,
                    face[1] + (shifts[pos[2]][1] + shifts[(pos[2] - 1) % len(shifts)][1]) * cube_size)
            pos = (pos[0] + shifts[pos[2]][0] * cube_size + shifts[(pos[2] - 1) % len(shifts)][0],
                   pos[1] + shifts[pos[2]][1] * cube_size + shifts[(pos[2] - 1) % len(shifts)][1],
                   (pos[2] - 1) % len(shifts))
        elif (face[0] + shifts[pos[2]][0] * cube_size,
                face[1] + shifts[pos[2]][1] * cube_size) in cube_points:
            face = (face[0] + shifts[pos[2]][0] * cube_size,
                    face[1] + shifts[pos[2]][1] * cube_size)
            pos = (pos[0] + shifts[pos[2]][0] * cube_size,
                   pos[1] + shifts[pos[2]][1] * cube_size,
                   pos[2])
        else:
            pos = (pos[0] + shifts[pos[2]][0] * (cube_size - 1),
                   pos[1] + shifts[pos[2]][1] * (cube_size - 1),
                   (pos[2] + 1) % len(shifts))
            outer_corners.update((len(perimeter) - 1, len(perimeter)))
        if pos == start_pos:
            break
    cube_warps = {}
    i = 0
    while True:
        new_linked_coords = []
        for c in linked_coords:
            a, b = perimeter[c[0]], perimeter[c[1]]
            if a[0] is None or b[0] is None:
                continue
            cube_warps[(a[0] + shifts[(a[2] - 1) % len(shifts)][0],
                        a[1] + shifts[(a[2] - 1) % len(shifts)][1],
                        (a[2] - 1) % len(shifts))] = (b[0], b[1], (b[2] + 1) % len(shifts))
            cube_warps[(b[0] + shifts[(b[2] - 1) % len(shifts)][0],
                        b[1] + shifts[(b[2] - 1) % len(shifts)][1],
                        (b[2] - 1) % len(shifts))] = (a[0], a[1], (a[2] + 1) % len(shifts))
            perimeter[c[0]] = (None, c[1])
            perimeter[c[1]] = (None, c[0])
            if perimeter[new_left := (c[0] - 1) % len(perimeter)][0] is None:
                new_left = (perimeter[new_left][1] - 1) % len(perimeter)
            if perimeter[new_right := (c[1] + 1) % len(perimeter)][0] is None:
                new_right = (perimeter[new_right][1] + 1) % len(perimeter)
            if all(x in outer_corners for x in (c[0], c[1], new_left, new_right)):
                if (new_right - new_left) % len(perimeter) <= (2 * cube_size) + 1:
                    continue
            new_linked_coords.append((new_left, new_right))
        if len(new_linked_coords) == 0:
            break
        else:
            linked_coords = new_linked_coords

    line = in_file.readline().strip()
    n = 0
    pos1 = start_pos
    pos2 = start_pos
    for char in line + 'X':
        if '0' <= char <= '9':
            n = n * 10 + int(char)
        else:
            blocked1 = blocked2 = False
            for i in range(1, n + 1):
                next_pos1 = (pos1[0] + shifts[pos1[2]][0], pos1[1] + shifts[pos1[2]][1], pos1[2])
                next_pos2 = (pos2[0] + shifts[pos2[2]][0], pos2[1] + shifts[pos2[2]][1], pos2[2])
                if next_pos1 in warps:
                    next_pos1 = warps[next_pos1]
                if next_pos2 in cube_warps:
                    next_pos2 = cube_warps[next_pos2]
                if not (blocked1 := ((next_pos1[0], next_pos1[1]) in walls)):
                    pos1 = next_pos1
                if not (blocked2 := ((next_pos2[0], next_pos2[1]) in walls)):
                    pos2 = next_pos2
                if blocked1 and blocked2:
                    break
            pos1 = (pos1[0], pos1[1], (pos1[2] + turns[char]) % len(shifts))
            pos2 = (pos2[0], pos2[1], (pos2[2] + turns[char]) % len(shifts))
            n = 0
    print(1000 * pos1[0] + 4 * pos1[1] + pos1[2])
    print(1000 * pos2[0] + 4 * pos2[1] + pos2[2])
