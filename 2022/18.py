from collections import deque
covered_part1 = 0
cubes = {}
offsets = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]
min_coords = [float('inf')] * 3
max_coords = [float('-inf')] * 3
with open('18.txt', 'r') as in_file:
    for line in in_file.read().split('\n'):
        if len(line) == 0:
            continue
        coords = tuple(map(int, line.split((','))))
        for i in range(3):
            if coords[i] < min_coords[i]:
                min_coords[i] = coords[i]
            if coords[i] > max_coords[i]:
                max_coords[i] = coords[i]
        cubes[coords] = None
        for offset in offsets:
            if tuple(map(sum, zip(coords, offset))) in cubes:
                covered_part1 += 2
print(len(cubes) * 6 - covered_part1)
queue = deque()
start = (min_coords[0] - 1, min_coords[1] - 1, min_coords[2] - 1)
queue.append(start)
open = {start}
closed = set()
surface_part2 = 0
while len(queue):
    tile = queue.popleft()
    open.remove(tile)
    closed.add(tile)
    for offset in offsets:
        neighbor = tuple(map(sum, zip(tile, offset)))
        if neighbor in cubes:
            surface_part2 += 1
            continue
        if not all((min_coords[i] - 1 <= neighbor[i] <= max_coords[i] + 1) for i in range(3)):
            continue
        if neighbor in open or neighbor in closed:
            continue
        open.add(neighbor)
        queue.append(neighbor)
print(surface_part2)
