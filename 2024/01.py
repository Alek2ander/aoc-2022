from sortedcontainers import SortedList

with open('01.txt', 'r') as in_file:
    left_list = SortedList()
    right_list = SortedList()
    for line in in_file.read().split('\n'):
        n_left, n_right = map(int, line.split())
        left_list.add(n_left)
        right_list.add(n_right)

sum_1 = sum_2 = i_right = 0
for i_left, n_left in enumerate(left_list):
    c = 0
    sum_1 += abs(n_left - right_list[i_left])
    while i_right < len(right_list) and right_list[i_right] < n_left:
        i_right += 1
    while i_right < len(right_list) and right_list[i_right] == n_left:
        c += 1
        i_right += 1
    sum_2 += n_left * c

print(sum_1)
print(sum_2)
