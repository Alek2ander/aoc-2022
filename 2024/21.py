from functools import cache
from heapq import heappop, heappush
from itertools import pairwise

numpad = {
    '7': (0, 0), '8': (1, 0), '9': (2, 0),
    '4': (0, 1), '5': (1, 1), '6': (2, 1),
    '1': (0, 2), '2': (1, 2), '3': (2, 2),
                 '0': (1, 3), 'A': (2, 3)
}
dpad = {
                 '^': (1, 0), 'A': (2, 0),
    '<': (0, 1), 'v': (1, 1), '>': (2, 1)
}
directions = {'^': (0, -1), '<': (-1, 0), 'v': (0, 1), '>': (1, 0)}

def generate_path_cache(grid):
    result = {}
    rev_grid = {v: k for k, v in grid.items()}
    for start_key in grid:
        paths = result[start_key] = {end_key: list() for end_key in grid}
        distances = {}
        queue = [(0, '', start_key)]
        while len(queue):
            dist, path, key = heappop(queue)
            if key in distances and distances[key] < dist:
                continue
            paths[key].append(path)
            distances[key] = dist
            pos = grid[key]
            for d_symbol, (dx, dy) in directions.items():
                if (pos1 := (pos[0] + dx, pos[1] + dy)) not in rev_grid:
                    continue
                if (key1 := rev_grid[pos1]) in distances and distances[key1] <= dist:
                    continue
                heappush(queue, (dist + 1, path + d_symbol, key1))
    return result

numpad_paths = generate_path_cache(numpad)
dpad_paths = generate_path_cache(dpad)

@cache
def find_min_seq_len(src, dest, dpad_layers, is_numpad = False):
    grid_paths = numpad_paths if is_numpad else dpad_paths
    if dpad_layers == 1:
        return len(grid_paths[src][dest][0]) + 1
    min_seq_length = None
    for path in grid_paths[src][dest]:
        path_len = sum(find_min_seq_len(a, b, dpad_layers - 1) for a, b in pairwise('A' + path + 'A'))
        if min_seq_length is None or path_len < min_seq_length:
            min_seq_length = path_len
    return min_seq_length

sum_1 = sum_2 = 0
with open('21.txt', 'r') as in_file:
    for line in in_file.read().split('\n'):
        sum_1 += int(line[:-1]) * sum(find_min_seq_len(a, b, 3, True) for a, b, in pairwise('A' + line))
        sum_2 += int(line[:-1]) * sum(find_min_seq_len(a, b, 26, True) for a, b, in pairwise('A' + line))
print(sum_1)
print(sum_2)
