from math import log10, floor
from functools import cache

with open('11.txt', 'r') as in_file:
    stones = [int(n) for n in in_file.read().strip().split()]

@cache
def blink(n, i):
    if i == 0:
        return 1
    if n == 0:
        return blink(1, i - 1)
    elif (size := floor(log10(n)) + 1) % 2 == 0:
        return blink(n // 10 ** (size // 2), i - 1) + blink(n % 10 ** (size // 2), i - 1)
    else:
        return blink(n * 2024, i - 1)

print(sum(blink(n, 25) for n in stones))
print(sum(blink(n, 75) for n in stones))
