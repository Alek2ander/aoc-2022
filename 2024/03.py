import re

with open('03.txt', 'r') as in_file:
    sum_do = sum_dont = 0
    for section in in_file.read().split('do()'):
        do_this, *dont_this = section.split('don\'t()')
        sum_do += sum(int(op1) * int(op2) for op1, op2 in re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', do_this))
        sum_dont += sum(int(op1) * int(op2) for op1, op2 in re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', ''.join(dont_this)))

print(sum_do + sum_dont)
print(sum_do)
