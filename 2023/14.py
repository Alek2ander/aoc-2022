from sortedcontainers import SortedList

with open('14.txt', 'r') as in_file:
    lines = in_file.read().split('\n')
    max_y, max_x = len(lines), len(lines[0])
    row_blockers = [SortedList((-1, max_x)) for y in range(max_y)]
    col_blockers = [SortedList((-1, max_y)) for x in range(max_x)]
    segments_internal = {}
    segments_n = {(x, -1): 0 for x in range(max_x)}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            match c:
                case 'O':
                    section_y = col_blockers[x][-2]
                    segments_n[(x, section_y)] += 1
                case '#':
                    col_blockers[x].add(y)
                    row_blockers[y].add(x)
                    segments_internal[(x, y)] = 0
                    segments_n[(x, y)] = 0
                case '.':
                    pass

sum_1 = sum_2 = cycle = 0
target_cycle = 1000000000
last_cycles = []
last_cycles_map = {}
while True:
    segments_w = {(-1, y): 0 for y in range(max_y)} | segments_internal
    for (x, y), n in segments_n.items():
        for i in range(n):
            blocker_w = row_blockers[y + i + 1][row_blockers[y + i + 1].bisect_right(x) - 1]
            segments_w[(blocker_w, y + i + 1)] += 1
            if not len(last_cycles):
                sum_1 += max_y - y - i - 1
    segments_s = {(x, max_y): 0 for x in range(max_x)} | segments_internal
    for (x, y), n in segments_w.items():
        for i in range(n):
            blocker_s = col_blockers[x + i + 1][col_blockers[x + i + 1].bisect_right(y)]
            segments_s[(x + i + 1, blocker_s)] += 1
    cycle_result = 0
    segments_e = {(max_x, y): 0 for y in range(max_y)} | segments_internal
    for (x, y), n in segments_s.items():
        for i in range(n):
            blocker_e = row_blockers[y - i - 1][row_blockers[y - i - 1].bisect_right(x)]
            segments_e[(blocker_e, y - i - 1)] += 1
            cycle_result += max_y - y + i + 1
    if (s := tuple(segments_e.values())) in last_cycles_map:
        loop_start = last_cycles_map[s]
        loop_len = cycle - loop_start
        sum_2 = last_cycles[(target_cycle - loop_start - 1) % loop_len + loop_start]
        break
    last_cycles.append(cycle_result)
    last_cycles_map[s] = cycle
    segments_n = {(x, -1): 0 for x in range(max_x)} | segments_internal
    for (x, y), n in segments_e.items():
        for i in range(n):
            blocker_n = col_blockers[x - i - 1][col_blockers[x - i - 1].bisect_right(y) - 1]
            segments_n[(x - i - 1, blocker_n)] += 1
    cycle += 1

print(sum_1)
print(sum_2)
