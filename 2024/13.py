import re
from math import floor, ceil
from sympy import Integer, Matrix, Interval, solve_linear_system, symbols, diophantine, minimum, N
from sympy.core.numbers import Infinity, NegativeInfinity

def solve(ax, ay, bx, by, x, y, cost_a, cost_b):
    a, b = symbols('a, b', integer=True)
    solution = solve_linear_system(Matrix(((ax, bx, x), (ay, by, y))), a, b)
    if solution is None:
        return 0
    if a in solution and isinstance(an := solution[a], Integer) \
            and b in solution and isinstance(bn := solution[b], Integer):
        return an * cost_a + bn * cost_b
    elif a in solution and b not in solution:
        # For the sake of completeness, solve the linear-dependent case.
        # (not actually necessary because there's none in the real input)
        # Also, there's probably a more optimal solution than general solvers,
        # but I don't have the time on a working friday.
        int_solution = diophantine(solution[a] - a)
        if not int_solution:
            return 0
        f_a, f_b = int_solution.pop()
        t_0 = symbols('t_0', integer=True)
        flipped = (f_a == -t_0 or f_b == -t_0)
        if flipped:
            min_t = -minimum(f_a * cost_a + f_b * cost_b, t_0, Interval(NegativeInfinity, 0))
        else:
            min_t = minimum(f_a * cost_a + f_b * cost_b, t_0, Interval(0, Infinity))
        if isinstance(min_t, Integer):
            return f_a.subs(t_0, min_t) * cost_a + f_b.subs(t_0, min_t) * cost_b
        else:
            return min(
                f_a.subs(t_0, floor(min_t)) * cost_a + f_b.subs(t_0, floor(min_t)) * cost_b,
                f_a.subs(t_0, ceil(min_t)) * cost_a + f_b.subs(t_0, ceil(min_t)) * cost_b)
    else:
        return 0

sum_1 = sum_2 = 0
cost_a, cost_b = 3, 1
with open('13.txt', 'r') as in_file:
    for claw in re.findall(
            r'Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)',
            in_file.read()):
        ax, ay, bx, by, x, y = map(int, claw)
        sum_1 += solve(ax, ay, bx, by, x, y, cost_a, cost_b)
        sum_2 += solve(ax, ay, bx, by, x + 10000000000000, y + 10000000000000, cost_a, cost_b)

print(sum_1)
print(sum_2)
