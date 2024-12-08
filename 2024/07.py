from operator import add, mul, sub
from math import log10, floor

def concat(x, y):
    return x * 10 ** (floor(log10(y)) + 1) + y

def r_mul(x, y):
    return x // y if x % y == 0 else None

def r_concat(x, y):
    return x // size if x % (size := 10 ** (floor(log10(y)) + 1)) == y else None

def apply_operators(set_x, y, operators):
    new_x = set()
    for x in set_x:
        for op in operators:
            if (v := op(x, y)) is not None:
                new_x.add(v)
    return new_x

def check_reachable(left, middle, right, operators_l, operators_r):
    reachable_l, reachable_r = {left}, {right}
    i_l, i_r = 0, len(middle)
    while i_l < i_r:
        if len(reachable_l) < len(reachable_r):
            reachable_l = apply_operators(reachable_l, middle[i_l], operators_l)
            i_l += 1
        else:
            reachable_r = apply_operators(reachable_r, middle[i_r - 1], operators_r)
            i_r -= 1
    return len(reachable_l & reachable_r) > 0

with open('07.txt', 'r') as in_file:
    sum_1 = sum_2 = 0
    for line in in_file.readlines():
        result, operand_line = line.split(': ')
        (left, *middle), right = map(int, operand_line.split()), int(result)
        if check_reachable(left, middle, right, (add, mul), (sub, r_mul)):
            sum_1 += right
        elif check_reachable(left, middle, right, (add, mul, concat), (sub, r_mul, r_concat)):
            sum_2 += right

print(sum_1)
print(sum_1 + sum_2)
