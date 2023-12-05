def get_priority(i):
    if ord('a') <= ord(i) <= ord('z'):
        return ord(i) - ord('a') + 1
    else:
        return ord(i) - ord('A') + 27


total_priority_part1 = total_priority_part2 = 0
with open('03.txt', 'r') as in_file:
    for index, line in enumerate(in_file.read().split('\n')):
        mid = len(line) // 2
        rucksack_1, rucksack_2 = set(line[:mid]), set(line[mid:])
        total_priority_part1 += sum(get_priority(i) for i in rucksack_1 & rucksack_2)
        if index % 3 == 0:
            group_rucksack = rucksack_1 | rucksack_2
        else:
            group_rucksack &= rucksack_1 | rucksack_2
            if index % 3 == 2:
                total_priority_part2 += sum(get_priority(i) for i in group_rucksack)

print(total_priority_part1)
print(total_priority_part2)
