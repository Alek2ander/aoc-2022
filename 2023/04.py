with open('04.txt', 'r') as in_file:
    sum_1 = 0
    sum_2 = 0
    stack_2 = []
    for line in in_file.read().split('\n'):
        _, data = line.split(': ')
        winning, checked = data.split(' | ')
        winning = set(num for num in winning.split(' ') if len(num))
        matches = sum(1 for num in checked.split(' ') if num in winning)
        multiplier = stack_2.pop() if len(stack_2) else 1
        if matches > 0:
            sum_1 += pow(2, matches - 1)
            stack_2 = [1 + multiplier] * (matches - len(stack_2)) + stack_2[:-matches] \
                      + [x + multiplier for x in stack_2[-matches:]]
        sum_2 += multiplier

print(sum_1)
print(sum_2)
