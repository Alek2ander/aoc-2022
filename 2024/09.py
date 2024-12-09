with open('09.txt', 'r') as in_file:
    fs_1, fs_2, size_lookup = [], [], {k: [] for k in range(1, 10)}
    for i, c in enumerate(in_file.read().strip()):
        n = int(c)
        fs_1.append(n)
        fs_2.append(n)
        if i % 2 == 0:
            size_lookup[n].append(i)

i_l = fs_index_1 = fs_index_2 = sum_1 = sum_2 = 0
r_index_1, counted_2 = len(fs_1) - 1 if len(fs_1) % 2 == 1 else len(fs_1) - 2, set()
while i_l < len(fs_1):
    if i_l % 2 == 0:
        block_len_1, block_len_2 = fs_1[i_l], fs_2[i_l]
        if block_len_1:
            sum_1 += i_l * (2 * fs_index_1 + block_len_1 - 1) * block_len_1 // 4
        if i_l not in counted_2:
            sum_2 += i_l * (2 * fs_index_2 + block_len_2 - 1) * block_len_2 // 4
            counted_2.add(i_l)
        fs_index_1, fs_index_2 = fs_index_1 + block_len_1, fs_index_2 + block_len_2
    else:
        while (hole := fs_1[i_l]) > 0:  # Part 1
            if r_index_1 < i_l:
                fs_index_1 = fs_index_1 + hole
                break
            fill = fs_1[r_index_1]
            block_len = min(hole, fill)
            sum_1 += r_index_1 * (2 * fs_index_1 + block_len - 1) * block_len // 4
            fs_1[i_l], fs_1[r_index_1], fs_index_1 = hole - block_len, fill - block_len, fs_index_1 + block_len
            if fill == block_len:
                r_index_1 -= 2
        while (hole := fs_2[i_l]) > 0:  # Part 2
            block_len = index_moved = 0
            for fill in range(hole, 0, -1):
                if not size_lookup[fill]:
                    continue
                if size_lookup[fill][-1] in counted_2:
                    size_lookup[fill] = []
                    continue
                if size_lookup[fill][-1] > index_moved:
                    block_len, index_moved = fill, size_lookup[fill][-1]
            if block_len == 0:
                fs_index_2 = fs_index_2 + hole
                break
            size_lookup[block_len].pop()
            sum_2 += index_moved * (2 * fs_index_2 + block_len - 1) * block_len // 4
            counted_2.add(index_moved)
            fs_2[i_l], fs_index_2 = hole - block_len, fs_index_2 + block_len
    i_l += 1

print(sum_1)
print(sum_2)
