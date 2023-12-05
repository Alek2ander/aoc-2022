directions = {
    'X': (0, 0),
    '>': (0, 1),
    '<': (0, -1),
    '^': (-1, 0),
    'v': (1, 0)
}
blizzards = []
first_pos = None
last_pos = None

with open('24.txt', 'r') as in_file:
    lines = [line.strip() for line in in_file.readlines() if len(line) > 0]
    height = len(lines) - 2
    width = len(lines[0]) - 2
    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            match char:
                case '#':
                    continue
                case '.':
                    if y == 0:
                        first_pos = (y, x)
                    if y == height + 1:
                        last_pos = (y, x)
                case b:
                    blizzards.append([(y, x), directions[b]])


def find_path(start, goal, blizzards):
    last_turn = {start}
    t = 0
    while True:
        t += 1
        blocked = set()
        for blizzard in blizzards:
            new_y, new_x = blizzard[0][0] + blizzard[1][0], blizzard[0][1] + blizzard[1][1]
            if new_y == 0:
                new_y = height
            elif new_y == height + 1:
                new_y = 1
            if new_x == 0:
                new_x = width
            elif new_x == width + 1:
                new_x = 1
            blizzard[0] = (new_y, new_x)
            blocked.add((new_y, new_x))
        if goal in last_turn:
            break
        turn = {start}
        for y in range(1, height + 1):
            for x in range(1, width + 1):
                if (y, x) in blocked:
                    continue
                for direction in directions.values():
                    if (y + direction[0], x + direction[1]) in last_turn:
                        turn.add((y, x))
                        break
        last_turn = turn
    return t, blizzards


t1, blizzards = find_path(first_pos, (last_pos[0] - 1, last_pos[1]), blizzards)
print(t1)
t2, blizzards = find_path(last_pos, (first_pos[0] + 1, first_pos[1]), blizzards)
t3, blizzards = find_path(first_pos, (last_pos[0] - 1, last_pos[1]), blizzards)
print(t1 + t2 + t3)
