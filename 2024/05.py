with open('05.txt', 'r') as in_file:
    prereqs = {}
    sum_good_middle = sum_bad_middle = 0
    while line := in_file.readline().strip():
        before, after = line.split('|')
        if after not in prereqs:
            prereqs[after] = {before}
        else:
            prereqs[after].add(before)
    while line := in_file.readline().strip():
        values = list(line.split(','))
        remaining = set(values)
        good_order = True
        for v in values:
            if v in prereqs and (prereqs[v] & remaining):
                good_order = False
                break
            remaining.remove(v)
        if good_order:
            sum_good_middle += int(values[len(values) // 2])
            continue
        remaining = set(values)
        while len(remaining) > len(values) // 2:  # No need to sort further than the middle because we only need the middle value
            found_next = False
            for v in remaining:
                if v in prereqs and (prereqs[v] & remaining):
                    continue
                found_next = True
                remaining.remove(v)
                if len(remaining) == len(values) // 2:
                    sum_bad_middle += int(v)
                break
            if not found_next:
                raise ValueError('Sequence cannot be ordered due to a dependency loop.')

print(sum_good_middle)
print(sum_bad_middle)
