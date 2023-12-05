rocks = [
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    ((0, 1), (1, 0), (1, 1), (1, 2), (2, 1)),
    ((0, 0), (0, 1), (0, 2), (1, 2), (2, 2)),
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((0, 0), (0, 1), (1, 0), (1, 1))
]
buffer_ratio = 2
buffer_size = len(rocks) * buffer_ratio

with open('17.txt', 'r') as in_file:
    sequence = in_file.read().strip()


def toss_rocks(total):
    movement = cycle_lines = 0
    remaining = total
    position_buffers = [[None] * buffer_size for _ in range(buffer_ratio)]
    rel_y = [0] * buffer_ratio
    end_states = {}
    tower = [127]
    while remaining:
        rock_idx = (total - remaining) % len(rocks)
        buffer_index = (total - remaining) % buffer_size
        primary_buffer = buffer_index // len(rocks)
        buffer_idx = [(buffer_index + len(rocks) * i) % buffer_size for i in range(buffer_ratio)]
        rock = rocks[rock_idx]
        position = [len(tower) + 3, 2]
        while True:
            match sequence[movement]:
                case '>':
                    shift = (0, 1)
                case '<':
                    shift = (0, -1)
                case _:
                    raise Exception('what?')
            valid_move = True
            for tile in rock:
                y, x = map(sum, zip(position, tile, shift))
                if x < 0 or x >= 7 or (y < len(tower) and tower[y] & (1 << x)):
                    valid_move = False
            if valid_move:
                position = [x for x in map(sum, zip(position, shift))]
            movement = (movement + 1) % len(sequence)
            shift = (-1, 0)
            valid_move = True
            for tile in rock:
                y, x = map(sum, zip(position, tile, shift))
                if y < len(tower) and tower[y] & (1 << x):
                    valid_move = False
            if valid_move:
                position = [x for x in map(sum, zip(position, shift))]
            else:
                for tile in rock:
                    y, x = map(sum, zip(position, tile))
                    while y >= len(tower):
                        tower.append(0)
                    tower[y] |= 1 << x
                break
        for i, position_buffer in enumerate(position_buffers):
            position_buffer[buffer_idx[i]] = tuple(map(sum, zip(position, (-rel_y[i], 0))))
        if rock_idx == len(rocks) - 1:
            rel_y[primary_buffer] = len(tower) - 1
            key = (movement, tuple(position_buffers[primary_buffer]))
            if key in end_states:
                blocks = total - remaining - end_states[key][0]
                lines = rel_y[primary_buffer] - end_states[key][1]
                cycles = remaining // (total - remaining - end_states[key][0])
                remaining -= cycles * blocks
                total -= cycles * blocks
                cycle_lines += cycles * lines
            else:
                end_states[key] = (total - remaining, rel_y[primary_buffer])
        remaining -= 1
    return len(tower) - 1 + cycle_lines


print(toss_rocks(2022))
print(toss_rocks(1000000000000))
