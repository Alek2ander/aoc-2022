directions = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))

with open('04.txt', 'r') as in_file:
    count_xmas = 0
    count_x_mas = 0
    arr = list(in_file.read().split('\n'))
    max_y = len(arr)
    max_x = len(arr[0])
    placeholder = '.' * (max_x + 4)
    arr = [placeholder, placeholder, *('..' + line + '..' for line in arr), placeholder, placeholder]
    for y in range(2, max_y + 2):
        for x in range(2, max_x + 2):
            if arr[y][x] != 'A':
                continue
            mas_directions = 0
            for d in directions:
                if          arr[y - 2 * d[0]][x - 2 * d[1]] == 'X' \
                        and arr[y - 1 * d[0]][x - 1 * d[1]] == 'M' \
                        and arr[y + 1 * d[0]][x + 1 * d[1]] == 'S':
                    count_xmas += 1
                if d[0] != 0 and d[1] != 0 \
                        and arr[y - 1 * d[0]][x - 1 * d[1]] == 'M' \
                        and arr[y + 1 * d[0]][x + 1 * d[1]] == 'S':
                    mas_directions += 1
            if mas_directions == 2:
                count_x_mas += 1

print(count_xmas)
print(count_x_mas)
