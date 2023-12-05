def sign(x):
    return (x > 0) - (x < 0)


rope = [(0, 0) for i in range(10)]
visited_part1 = {(0, 0)}
visited_part2 = {(0, 0)}
directions = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

with open('09.txt', 'r') as in_file:
    for line in in_file.read().split('\n'):
        if len(line) == 0:
            continue
        d, dist = line.split()
        for i in range(int(dist)):
            rope[0] = (rope[0][0] + directions[d][0], rope[0][1] + directions[d][1])
            for i in range(1, len(rope)):
                if abs(rope[i][0] - rope[i - 1][0]) == 2 or abs(rope[i][1] - rope[i - 1][1]) == 2:
                    rope[i] = (rope[i][0] if rope[i][0] == rope[i - 1][0] else
                               rope[i][0] + sign(rope[i - 1][0] - rope[i][0]),
                               rope[i][1] if rope[i][1] == rope[i - 1][1] else
                               rope[i][1] + sign(rope[i - 1][1] - rope[i][1]))
            visited_part1.add(rope[1])
            visited_part2.add(rope[9])

print(len(visited_part1))
print(len(visited_part2))
