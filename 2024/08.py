from itertools import combinations

frequencies = {}
with open('08.txt', 'r') as in_file:
    for y, line in enumerate(in_file.readlines()):
        for x, c in enumerate(line.strip()):
            if c == '.':
                continue
            if c not in frequencies:
                frequencies[c] = []
            frequencies[c].append((x, y))
    max_x, max_y = x, y

antinodes_1 = set()
antinodes_all = set()
for antennas in frequencies.values():
    for a1, a2 in combinations(antennas, 2):
        an, i = a1, 0
        while 0 <= an[0] <= max_x and 0 <= an[1] <= max_y:
            if i == 1:
                antinodes_1.add(an)
            antinodes_all.add(an)
            an, i = (an[0] - a2[0] + a1[0], an[1] - a2[1] + a1[1]), i + 1
        an, i = a2, 0
        while 0 <= an[0] <= max_x and 0 <= an[1] <= max_y:
            if i == 1:
                antinodes_1.add(an)
            antinodes_all.add(an)
            an, i = (an[0] + a2[0] - a1[0], an[1] + a2[1] - a1[1]), i + 1

print(len(antinodes_1))
print(len(antinodes_all))
