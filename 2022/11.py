import re
from operator import add, mul
from copy import deepcopy
from collections import deque

rounds_part1 = 20
rounds_part2 = 10000
operators = {
    '+': add,
    '*': mul
}
monkeys_part1 = []
monkey_business_part1 = []
monkey_business_part2 = []
lcm = 1

with open('11.txt', 'r') as in_file:
    for data in re.findall(
            r'Monkey \d+:\n'
            r'  Starting items: ([\d, ]+)\n'
            r'  Operation: new = (old|\d+) ([+*]) (old|\d+)\n'
            r'  Test: divisible by (\d+)\n'
            r'    If true: throw to monkey (\d+)\n'
            r'    If false: throw to monkey (\d+)\n',
            in_file.read()):
        startlist, op1, op, op2, div, true_dest, false_dest = data
        monkeys_part1.append(deque(int(x) for x in startlist.split(', ')))
        lcm *= (div := int(div))

        def _(x, true_dest=int(true_dest), false_dest=int(false_dest), div=div, op=operators[op], op1=op1, op2=op2):
            x = op(x if op1 == 'old' else int(op1), x if op2 == 'old' else int(op2)) // 3
            if x % div == 0:
                return true_dest, x
            else:
                return false_dest, x

        monkey_business_part1.append(_)

        def _(x, true_dest=int(true_dest), false_dest=int(false_dest), div=div, op=operators[op], op1=op1, op2=op2):
            x = op(x if op1 == 'old' else int(op1), x if op2 == 'old' else int(op2))
            if x % div == 0:
                return true_dest, x % lcm
            else:
                return false_dest, x % lcm

        monkey_business_part2.append(_)

monkeys_part2 = deepcopy(monkeys_part1)
inspections_part1 = [0] * len(monkeys_part1)
inspections_part2 = [0] * len(monkeys_part2)

for rnd in range(rounds_part1):
    for monkey_id, (monkey, business) in enumerate(zip(monkeys_part1, monkey_business_part1)):
        inspections_part1[monkey_id] += len(monkey)
        for i in range(len(monkey)):
            new_monkey, new_item = business(monkey.popleft())
            monkeys_part1[new_monkey].append(new_item)
for rnd in range(rounds_part2):
    for monkey_id, (monkey, business) in enumerate(zip(monkeys_part2, monkey_business_part2)):
        inspections_part2[monkey_id] += len(monkey)
        for i in range(len(monkey)):
            new_monkey, new_item = business(monkey.popleft())
            monkeys_part2[new_monkey].append(new_item)

print(mul(*sorted(inspections_part1, reverse=True)[:2]))
print(mul(*sorted(inspections_part2, reverse=True)[:2]))
