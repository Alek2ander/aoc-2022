def mix(seq, n, key):
    seq = [(i, x * key) for i, x in enumerate(seq)]
    s = seq
    for _ in range(n):
        for i, x in seq:
            old_i = s.index((i, x))
            new_i = (old_i + x) % (len(seq) - 1)
            if new_i > old_i:
                s = [*s[:old_i], *s[old_i + 1:new_i + 1], (i, x), *s[new_i + 1:]]
            else:
                s = [*s[:new_i], (i, x), *s[new_i:old_i], *s[old_i + 1:]]
    return s


with open('20.txt', 'r') as in_file:
    sequence = [int(x.strip()) for x in in_file if len(x) > 0]
zero = sequence.index(0)
seq_part1 = mix(sequence, 1, 1)
start = seq_part1.index((zero, 0))
print(sum(seq_part1[(start + 1000 * i) % len(seq_part1)][1] for i in range(1, 4)))
seq_part2 = mix(sequence, 10, 811589153)
start = seq_part2.index((zero, 0))
print(sum(seq_part2[(start + 1000 * i) % len(seq_part1)][1] for i in range(1, 4)))
