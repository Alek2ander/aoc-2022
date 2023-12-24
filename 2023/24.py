from itertools import combinations
from sympy import symbols, solve_poly_system

xy_min = 200000000000000
xy_max = 400000000000000
lines = []
with open('24.txt', 'r') as in_file:
    for line in in_file:
        coords, speed = line.rstrip().split(' @ ')
        lines.append(tuple(map(int, (*coords.split(', '), *speed.split(', ')))))

part1_count = 0
for line1, line2 in combinations(lines, 2):
    x1, y1, _, dx1, dy1, _ = line1
    x2, y2, _, dx2, dy2, _ = line2
    div = dx1 * dy2 - dy1 * dx2
    if div == 0:
        continue
    t1 = dy2 * (x2 - x1) - dx2 * (y2 - y1)
    t2 = dy1 * (x2 - x1) - dx1 * (y2 - y1)
    if ((t1 > 0) == (div > 0) and (t2 > 0) == (div > 0)
            and xy_min <= x1 + t1 / div * dx1 <= xy_max and xy_min <= y1 + t1 / div * dy1 <= xy_max):
        part1_count += 1
print(part1_count)

x1, y1, z1, dx1, dy1, dz1 = lines[0]
x2, y2, z2, dx2, dy2, dz2 = lines[1]
x3, y3, z3, dx3, dy3, dz3 = lines[2]
x0, y0, z0, dx0, dy0, dz0, t1, t2, t3 = symbols('x0,y0,z0,dx0,dy0,dz0,t1,t2,t3')
x0, y0, z0, dx0, dy0, dz0, t1, t2, t3 = solve_poly_system((
        x0 + t1 * dx0 - x1 + t1 * dx1,
        y0 + t1 * dy0 - y1 + t1 * dy1,
        z0 + t1 * dz0 - z1 + t1 * dz1,
        x0 + t2 * dx0 - x2 + t2 * dx2,
        y0 + t2 * dy0 - y2 + t2 * dy2,
        z0 + t2 * dz0 - z2 + t2 * dz2,
        x0 + t3 * dx0 - x3 + t3 * dx3,
        y0 + t3 * dy0 - y3 + t3 * dy3,
        z0 + t3 * dz0 - z3 + t3 * dz3
    ), symbols=(x0, y0, z0, dx0, dy0, dz0, t1, t2, t3))[0]
print(x0 + y0 + z0)
