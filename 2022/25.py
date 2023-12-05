digits = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2
}
reverse = {
    0: ('0', 0),
    1: ('1', 1),
    2: ('2', 2),
    3: ('=', -2),
    4: ('-', -1)
}
base = 5
s = 0
with open('25.txt', 'r') as in_file:
    for line in in_file:
        if len(line) == 0:
            continue
        for i, d in enumerate(line.strip()[::-1]):
            s += pow(base, i) * digits[d]
snafu = ''
i = 0
while s != 0:
    digit, add = reverse[(s // pow(base, i)) % base]
    snafu = digit + snafu
    s -= pow(base, i) * add
    i += 1
print(snafu)
