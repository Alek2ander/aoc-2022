digits = {str(i): i for i in range(0, 10)}
extended_digits = {
    **digits,
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}


def find_number(line, digits):
    indices_l = [len(line)] * 10
    indices_r = [-1] * 10
    for digit in digits:
        l_index = line.find(digit)
        if l_index != -1 and l_index < indices_l[digits[digit]]:
            indices_l[digits[digit]] = l_index
        r_index = line.rfind(digit)
        if r_index != -1 and r_index > indices_r[digits[digit]]:
            indices_r[digits[digit]] = r_index
    return indices_l.index(min(indices_l)) * 10 + indices_r.index(max(indices_r))


with open('01.txt', 'r') as in_file:
    sum_1 = 0
    sum_2 = 0
    for line in in_file.read().split('\n'):
        sum_1 += find_number(line, digits)
        sum_2 += find_number(line, extended_digits)

print(sum_1)
print(sum_2)
