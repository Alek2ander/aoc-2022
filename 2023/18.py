directions = {
    'R': 0,
    'D': 1,
    'L': 2,
    'U': 3
}


def get_area(instructions):
    y = area = edges = 0
    for d, n in instructions:
        edges += n
        match d:
            case 0:
                area += y * n
            case 1:
                y -= n
            case 2:
                area -= y * n
            case 3:
                y += n
    return abs(area) + edges // 2 + 1


instructions_1 = []
instructions_2 = []
with open('18.txt', 'r') as in_file:
    for line in in_file:
        d, n, c = line.rstrip().split()
        instructions_1.append((directions[d], int(n)))
        instructions_2.append((int(c[7]), int(c[2:7], 16)))

print(get_area(instructions_1))
print(get_area(instructions_2))
