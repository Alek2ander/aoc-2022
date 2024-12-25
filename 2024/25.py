keys, locks = [], []
sum_1 = 0
with open('25.txt', 'r') as in_file:
    cur, is_key = [0] * 5, None
    while True:
        line = in_file.readline()
        if not line and is_key is None:
            break
        if not (line := line.strip()):
            if is_key:
                sum_1 += sum(1 for vs in locks if all(vs[i] <= cur[i] for i in range(len(cur))))
                keys.append(cur)
            else:
                sum_1 += sum(1 for vs in keys if all(vs[i] >= cur[i] for i in range(len(cur))))
                locks.append(cur)
            cur, is_key = [0] * 5, None
            continue
        if is_key is None:
            is_key = (line == '.....')
            continue
        for i, c in enumerate(line):
            cur[i] += 1 if c == ('.' if is_key else '#') else 0
print(sum_1)
