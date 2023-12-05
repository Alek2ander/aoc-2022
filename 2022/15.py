import re

segments = []
scanned_y = 2000000
x_mult = max_bound = 4000000
slopes_ur = []
slopes_dr = []
with open('15.txt', 'r') as in_file:
    for data in re.findall(r'Sensor at x=([\d-]+), y=([\d-]+): closest beacon is at x=([\d-]+), y=([\d-]+)',
                                   in_file.read()):
        x, y, bx, by = map(int, data)
        if (proj := (dist := abs(bx - x) + abs(by - y)) - abs(scanned_y - y)) >= 0:
            segments.append((x - proj, x + proj, 1))
        if by == scanned_y:
            segments.append((bx, bx, -1))
        slopes_ur.append((a := y - dist - x - 1, max(x, 0, -a), min(x + dist + 1, max_bound, max_bound - a), True))
        slopes_ur.append((a := y + dist - x + 1, max(x - dist - 1, 0, -a), min(x, max_bound, max_bound - a), False))
        slopes_dr.append((a := y - dist + x - 1, max(x - dist - 1, 0, a - max_bound), min(x, max_bound, a), True))
        slopes_dr.append((a := y + dist + x + 1, max(x, 0, a - max_bound), min(x + dist + 1, max_bound, a), False))

counter_part1 = 0
curr_l = curr_r = float("-inf")
for segment in sorted(segments):
    if segment[0] > curr_r and segment[2] == 1:
        curr_r = segment[1]
        counter_part1 += curr_r - segment[0] + 1
    elif segment[1] > curr_r and segment[2] == 1:
        counter_part1 += segment[1] - curr_r
        curr_r = segment[1]
    elif segment[0] > curr_l and segment[2] == -1:
        curr_l = segment[0]
        counter_part1 -= 1


def merge_and_find_candidates(slopes):
    merged = {}
    for slope in slopes:
        if slope[0] not in merged:
            merged[slope[0]] = {True: [], False: []}
        merged[slope[0]][slope[3]].append((slope[1], slope[2]))
    for k, v in merged.items():
        candidates = set()
        for l1, r1 in v[True]:
            for l2, r2 in v[False]:
                if (min_x := max(l1, l2)) <= (max_x := min(r1, r2)):
                    candidates.update(x for x in range(min_x, max_x + 1))
        for x in candidates:
            yield k, x


candidates_ur = set((x, a + x) for a, x in merge_and_find_candidates(slopes_ur))
candidates_dr = set((x, a - x) for a, x in merge_and_find_candidates(slopes_dr))
beacon_part2 = (candidates_ur & candidates_dr).pop()

print(counter_part1)
print(beacon_part2[0] * x_mult + beacon_part2[1])
