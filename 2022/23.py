elves = {}
directions = (
    ((-1, 0), ((-1, 0), (-1, -1), (-1, 1))),
    ((1, 0), ((1, 0), (1, -1), (1, 1))),
    ((0, -1), ((0, -1), (-1, -1), (1, -1))),
    ((0, 1), ((0, 1), (-1, 1), (1, 1)))
)
part1_rounds = 10


with open('23.txt', 'r') as in_file:
    for y, line in enumerate(in_file):
        if len(line) == 0:
            continue
        for x, char in enumerate(line.strip()):
            if char == '#':
                elves[(y, x)] = None

min_x = min_y = float('inf')
max_x = max_y = float('-inf')
i = 0
moving = True
while moving:
    moving = False
    desired_moves = {}
    for elf in elves:
        adjacency = {(x, y): ((elf[0] + x, elf[1] + y) not in elves)
                     for x in range(-1, 2) for y in range(-1, 2)
                     if x != 0 or y != 0}
        if all(adjacency.values()):
            continue
        for d in range(len(directions)):
            direction, checks = directions[(i + d) % len(directions)]
            if all(adjacency[c] for c in checks):
                move = (elf[0] + direction[0], elf[1] + direction[1])
                elves[elf] = move
                if move not in desired_moves:
                    desired_moves[move] = True
                else:
                    desired_moves[move] = False
                break
    new_elves = {}
    for elf, move in elves.items():
        if move is not None and desired_moves[move]:
            new_elves[move] = None
            moving = True
        else:
            move = elf
            new_elves[move] = None
        if i == part1_rounds - 1:
            if move[0] > max_y:
                max_y = move[0]
            if move[0] < min_y:
                min_y = move[0]
            if move[1] > max_x:
                max_x = move[1]
            if move[1] < min_x:
                min_x = move[1]
    elves = new_elves
    i += 1
print((max_y - min_y + 1) * (max_x - min_x + 1) - len(elves))
print(i)
