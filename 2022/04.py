total_count_part1 = total_count_part2 = 0
with open('04.txt', 'r') as in_file:
    for line in in_file.read().split('\n'):
        if len(line) == 0:
            continue
        l1, r1, l2, r2 = map(int, line.replace('-', ',').split(','))
        if (l1 <= l2 and r1 >= r2) or (l2 <= l1 and r2 >= r1):
            total_count_part1 += 1
        if r1 >= l2 and r2 >= l1:
            total_count_part2 += 1

print(total_count_part1)
print(total_count_part2)
