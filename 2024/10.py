with open('10.txt', 'r') as in_file:
    grid = [line.strip() for line in in_file.readlines()]
    max_y, max_x = len(grid), len(grid[0])

def find_paths(x, y):
    found_1, found_2 = set(), 0
    if grid[y][x] == '9':
        return {(x, y)}, 1
    for x1, y1 in ((x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)):
        if 0 <= x1 < max_x and 0 <= y1 < max_y and ord(grid[y1][x1]) == ord(grid[y][x]) + 1:
            found_set, found_count = find_paths(x1, y1)
            found_1 |= found_set
            found_2 += found_count
    return found_1, found_2

sum_1 = sum_2 = 0
for y in range(max_y):
    for x in range(max_x):
        if grid[y][x] == '0':
            found_set, found_count = find_paths(x, y)
            sum_1 += len(found_set)
            sum_2 += found_count

print(sum_1)
print(sum_2)
