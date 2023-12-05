from operator import add, sub, mul, truediv
from sympy import solve
from sympy.abc import x
from copy import deepcopy

operators = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv
}
with open('21.txt', 'r') as in_file:
    monkeys1 = {s[0]: tuple(s[1].split(' ')) for line in in_file if len(s := line.strip().split(': ')) == 2}
monkeys2 = deepcopy(monkeys1)


def monkey_business_part1(key, m):
    match m[key]:
        case int(_):
            pass
        case (m1, op, m2):
            m[key] = operators[op](monkey_business_part1(m1, m), monkey_business_part1(m2, m))
        case (istr,):
            m[key] = int(istr)
    return m[key]


def monkey_business_part2(key, m):
    match key, m[key]:
        case 'humn', _:
            m[key] = x
        case 'root', (m1, _, m2):
            return monkey_business_part2(m1, m) - monkey_business_part2(m2, m)
        case _, int(_):
            return m[key]
        case _, (m1, op, m2):
            m[key] = operators[op](monkey_business_part2(m1, m), monkey_business_part2(m2, m))
        case _, (istr,):
            m[key] = int(istr)
    return m[key]


print(round(monkey_business_part1('root', monkeys1)))
print(round(solve(monkey_business_part2('root', monkeys2))[0]))
