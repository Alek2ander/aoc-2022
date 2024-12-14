import curses
import math
import re

max_x, max_y = 101, 103
robots = []
steps = 100
pattern = [0] * 4
with open('14.txt', 'r') as in_file:
    for robot in re.findall(
            r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)',
            in_file.read()):
        x0, y0, dx, dy = map(int, robot)
        x1, y1 = (x0 + dx * (steps % (max_x * max_y))) % max_x, (y0 + dy * (steps % (max_x * max_y))) % max_y
        if x1 < max_x // 2 and y1 < max_y // 2:
            pattern[0] += 1
        elif x1 > max_x // 2 and y1 < max_y // 2:
            pattern[1] += 1
        elif x1 < max_x // 2 and y1 > max_y // 2:
            pattern[2] += 1
        elif x1 > max_x // 2 and y1 > max_y // 2:
            pattern[3] += 1
        robots.append(([x0, y0], (dx, dy)))

print(math.prod(pattern))

# Time to look for anomalies.
# On my input, I found 2 anomalies repeating with max_x and max_y intervals.
# Using the Chinese Remainder Theorem, you can find where the anomalies meet.
# 
# i = 0
# while i < max_x * max_y:
#     i += 1
#     lines = [[' ' for __ in range(max_x)] for _ in range(max_y)]
#     for robot in robots:
#         x = robot[0][0] = (robot[0][0] + robot[1][0]) % max_x
#         y = robot[0][1] = (robot[0][1] + robot[1][1]) % max_y
#         lines[y][x] = '█'
#     print(i)
#     print('\n'.join(''.join(line) for line in lines))
#     if (s := input()) == 'q':
#         break

anomaly_x = 7
anomaly_y = 53

def extended_euclid(m, n):
    u, u1, v, v1 = 1, 0, 0, 1
    while n != 0:
        q, m, n = m // n, n, m % n
        u, u1 = u1, u - q * u1
        v, v1 = v1, v - q * v1
    return m, u, v

def find_common_target(loops, targets):
    m = loops[0]
    a = targets[0] % m
    for loop_len, target in zip(loops[1:], targets[1:]):
        b, n = target % loop_len, loop_len
        gcd, u, v = extended_euclid(m, n)
        d, check_mod = divmod(a - b, gcd)
        if check_mod != 0:
            return None
        m = m // gcd * n
        a = (b + n * v * d) % m
    return a

print(target := find_common_target((max_x, max_y), (anomaly_x, anomaly_y)))
lines = [[' ' for __ in range(max_x)] for _ in range(max_y)]
for robot in robots:
    x = robot[0][0] = (robot[0][0] + robot[1][0] * target) % max_x
    y = robot[0][1] = (robot[0][1] + robot[1][1] * target) % max_y
    lines[y][x] = '█'
print('\n'.join(''.join(line) for line in lines))
