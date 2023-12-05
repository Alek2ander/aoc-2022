import math

reqs_1 = {'red': 12, 'green': 13, 'blue': 14}

with open('02.txt', 'r') as in_file:
    sum_1 = 0
    sum_2 = 0
    for line in in_file.read().split('\n'):
        label, data = line.split(': ')
        game_id = int(label.split(' ')[1])
        valid_1 = True
        min_cubes_2 = {'red': 0, 'green': 0, 'blue': 0}
        for cube_set in data.split('; '):
            for cube_info in cube_set.split(', '):
                amt, color = int((info := cube_info.split(' '))[0]), info[1]
                if amt > reqs_1[color]:
                    valid_1 = False
                if amt > min_cubes_2[color]:
                    min_cubes_2[color] = amt
        if valid_1:
            sum_1 += game_id
        sum_2 += math.prod(min_cubes_2.values())

print(sum_1)
print(sum_2)
