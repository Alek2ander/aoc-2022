from functools import cache

with open('19.txt', 'r') as in_file:
    towel_trie = {}
    for towel in in_file.readline().strip().split(', '):
        ptr = towel_trie
        for c in towel:
            if c not in ptr:
                ptr[c] = {}
            ptr = ptr[c]
        ptr[None] = None

    @cache
    def arrange_towels(line):
        if not line:
            return 1
        arrangements = 0
        ptr = towel_trie
        for i, c in enumerate(line):
            if c not in ptr:
                return arrangements
            ptr = ptr[c]
            if None in ptr:
                arrangements += arrange_towels(line[i + 1:])
        return arrangements

    results = tuple(arrange_towels(l) for line in in_file.readlines() if (l := line.strip()))

print(sum(1 for v in results if v > 0))
print(sum(results))
