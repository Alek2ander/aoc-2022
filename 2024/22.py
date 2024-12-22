sum_1, sales_2 = 0, {}
with open('22.txt', 'r') as in_file:
    for n in map(int, in_file.read().split('\n')):
        changes = tuple()
        sold = set()
        for i in range(2000):
            next_n = n ^ (n << 6) & 16777215
            next_n = next_n ^ (next_n >> 5) & 16777215
            next_n = next_n ^ (next_n << 11) & 16777215
            changes = (*changes[-3:], next_n % 10 - n % 10)
            if len(changes) == 4 and changes not in sold:
                sales_2[changes] = next_n % 10 + sales_2.get(changes, 0)
                sold.add(changes)
            n = next_n
        sum_1 += n
print(sum_1)
print(max(sales_2.values()))
