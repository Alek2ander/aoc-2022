directions = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}
shape_1, shape_2 = ((0, 0),), ((0, 0), (1, 0))
walls_1, walls_2 = set(), set()
boxes_1, boxes_2 = set(), set()
position_1 = position_2 = None
with open('15.txt', 'r') as in_file:
    y = 0
    while line := in_file.readline().strip():
        for x, c in enumerate(line):
            match c:
                case '.':
                    continue
                case '#':
                    walls_1.add((x, y))
                    walls_2.add((x * 2, y))
                    walls_2.add((x * 2 + 1, y))
                case 'O':
                    boxes_1.add((x, y))
                    boxes_2.add((x * 2, y))
                case '@':
                    position_1 = (x, y)
                    position_2 = (x * 2, y)
        y += 1
    movements = in_file.read()

def try_move(pos, d, walls, boxes, self_shape, box_shape, active_mover):
    new_pos = (pos[0] + directions[d][0], pos[1] + directions[d][1])
    to_move, obstacles = set(), set()
    for tile in self_shape:
        if (new_pos[0] + tile[0], new_pos[1] + tile[1]) in walls:
            return pos, to_move
        for box_tile in box_shape:
            if (box := (new_pos[0] + tile[0] - box_tile[0], new_pos[1] + tile[1] - box_tile[1])) in boxes:
                if box == pos:
                    continue
                obstacles.add(box)
    for box in obstacles:
        dest, more_to_move = try_move(box, d, walls, boxes, box_shape, box_shape, False)
        if dest == box:
            return pos, to_move
        else:
            to_move |= more_to_move
    if active_mover:
        destinations = {(box[0] + directions[d][0], box[1] + directions[d][1]) for box in to_move}
        for box in destinations - to_move:
            boxes.add(box)
        for box in to_move - destinations:
            boxes.remove(box)
    else:
        to_move.add(pos)
    return new_pos, to_move

for d in movements:
    if d not in directions:
        continue
    position_1, _ = try_move(position_1, d, walls_1, boxes_1, shape_1, shape_1, True)
    position_2, _ = try_move(position_2, d, walls_2, boxes_2, shape_1, shape_2, True)

print(sum(x + 100 * y for x, y in boxes_1))
print(sum(x + 100 * y for x, y in boxes_2))
