def find_symmetries(data, errors, stop):
    if len(data) < 2:
        return 0
    for i in range(1, len(data)):
        visible = min(i, len(data) - i)
        differences = 0
        for j in range(visible):
            for x, y in zip(data[i - j - 1], data[i + j]):
                if x != y:
                    differences += 1
                if differences > errors:
                    break
            if differences > errors:
                break
        if differences == errors:
            yield i
            if stop:
                break


sum_1 = sum_2 = 0
with open('13.txt', 'r') as in_file:
    rows = []
    cols = []
    for line in in_file:
        if line := line.rstrip():
            rows.append(line)
            for i in range(len(line)):
                if i >= len(cols):
                    cols.append([])
                cols[i].append(line[i])
        else:
            sum_1 += sum(find_symmetries(cols, 0, False)) + 100 * sum(find_symmetries(rows, 0, False))
            sum_2 += sum(find_symmetries(cols, 1, True)) + 100 * sum(find_symmetries(rows, 1, True))
            rows = []
            cols = []
    sum_1 += sum(find_symmetries(cols, 0, False)) + 100 * sum(find_symmetries(rows, 0, False))
    sum_2 += sum(find_symmetries(cols, 1, True)) + 100 * sum(find_symmetries(rows, 1, True))
print(sum_1)
print(sum_2)
