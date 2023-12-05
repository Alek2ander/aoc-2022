source = (500, 0)
max_y = 0
walls = set()
sand = set()


def sand_fall(source, part1):
    if source[1] == max_y + 1:
        if not part1:
            sand.add(source)
        return True
    if (down := (source[0], source[1] + 1)) not in walls and down not in sand:
        if sand_fall(down, part1) and part1:
            return True
    if (downleft := (source[0] - 1, source[1] + 1)) not in walls and downleft not in sand:
        if sand_fall(downleft, part1) and part1:
            return True
    if (downright := (source[0] + 1, source[1] + 1)) not in walls and downright not in sand:
        if sand_fall(downright, part1) and part1:
            return True
    sand.add(source)
    return False


with open('14.txt', 'r') as in_file:
    for line in in_file.read().split('\n'):
        if len(line) == 0:
            continue
        for i, segment in enumerate(line.split(' -> ')):
            x, y = map(int, segment.split(','))
            if y > max_y:
                max_y = y
            if i > 0:
                if x == prev_x:
                    walls.update((x, y) for y in range(min(y, prev_y), max(y, prev_y) + 1))
                else:
                    walls.update((x, y) for x in range(min(x, prev_x), max(x, prev_x) + 1))
            prev_x, prev_y = x, y
sand_fall(source, True)
print(len(sand))
sand_fall(source, False)
print(len(sand))
