with open('03.txt', 'r') as in_file:
    symbols_1 = set()
    gears_2 = {}
    for y, line in enumerate(data := in_file.read().split('\n')):
        for x, character in enumerate(line):
            if not character.isdigit() and character != '.':
                symbols_1.add((x, y))
            if character == '*':
                gears_2[(x, y)] = []

    def close_number(number, start, end, y):
        coords_list = {(i, y + j) for i in range(start - 1, end + 1) for j in (1, -1)} | {(start - 1, y), (end, y)}
        for gear in coords_list & set(gears_2.keys()):
            gears_2[gear].append(number)
        return len(coords_list & symbols_1) > 0

    sum_1 = 0
    for y, line in enumerate(data):
        cur_number = 0
        start = -1
        for x, character in enumerate(line):
            if character.isdigit():
                if start == -1:
                    start = x
                cur_number = cur_number * 10 + int(character)
            elif start != -1:
                if close_number(cur_number, start, x, y):
                    sum_1 += cur_number
                cur_number = 0
                start = -1
        if start != -1:
            if close_number(cur_number, start, len(line), y):
                sum_1 += cur_number

    sum_2 = 0
    for gear in gears_2.values():
        if len(gear) == 2:
            sum_2 += gear[0] * gear[1]

print(sum_1)
print(sum_2)
