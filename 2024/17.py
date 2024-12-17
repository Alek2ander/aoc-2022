import re

with open('17.txt', 'r') as in_file:
    a, b, c, prog = re.match(r'Register A: (-?\d+)\nRegister B: (-?\d+)\nRegister C: (-?\d+)\n\nProgram: ([\d,]+)',
                             in_file.read()).groups()
    a, b, c = map(int, (a, b, c))
    prog = tuple(int(v) for v in prog.split(','))
ptr = 0
output = []
while ptr < len(prog) - 1:
    literal_value = combo_value = prog[ptr + 1]
    match prog[ptr + 1]:
        case 4:
            combo_value = a
        case 5:
            combo_value = b
        case 6:
            combo_value = c
    match prog[ptr]:
        case 0:  # adv
            a = a >> combo_value
        case 1:  # bxl
            b = b ^ literal_value
        case 2:  # bst
            b = combo_value & 7
        case 3:  # jnz
            if a != 0:
                ptr = literal_value
                continue
        case 4:  # bxc
            b = b ^ c
        case 5:  # out
            output.append(combo_value & 7)
        case 6:  # bdv
            b = a >> combo_value
        case 7:  # cdv
            c = a >> combo_value
    ptr += 2
print(','.join(str(v) for v in output))

# Part 2 is about reverse-engineering. This is based on my input, is not a general solution.
def reverse_program(a, i):
    if i < 0:
        return {a}
    values = set()
    for x in range(8):
        a1 = a << 3 | x
        if (x ^ 5 ^ (a1 >> (x ^ 5)) ^ 6) & 7 == prog[i]:
            values |= reverse_program(a1, i - 1)
    return values

print(min(reverse_program(0, len(prog) - 1)))
