galaxies_x = {}
galaxies_y = {}
with open('11.txt', 'r') as in_file:
    for y, line in enumerate(in_file):
        for x, char in enumerate(line.rstrip()):
            if char == '#':
                galaxies_x[x] = galaxies_x[x] + 1 if x in galaxies_x else 1
                galaxies_y[y] = galaxies_y[y] + 1 if y in galaxies_y else 1


def process_coord(projection, expansion_ratio):
    true_x = cur_count = result = 0
    total_count = sum(projection.values())
    for x in range(min(projection), max(projection) + 1):
        if x not in projection:
            true_x += expansion_ratio
            continue
        for _ in range(projection[x]):
            cur_count += 1
            result += true_x * (2 * cur_count - total_count - 1)
        true_x += 1
    return result


print(process_coord(galaxies_x, 2)
      + process_coord(galaxies_y, 2))
print(process_coord(galaxies_x, 1000000)
      + process_coord(galaxies_y, 1000000))
