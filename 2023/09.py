with open('09.txt', 'r') as in_file:
    sum_1 = sum_2 = 0
    for line in in_file:
        derivs = []
        for i, x in enumerate(line.rstrip().split()):
            cur_deriv = int(x)
            if not derivs:
                derivs.append(cur_deriv)
                sum_2 += cur_deriv
                continue
            for j in range(len(derivs)):
                cur_deriv, derivs[j] = cur_deriv - derivs[j], cur_deriv
            derivs.append(cur_deriv)
            sum_2 += cur_deriv if i % 2 == 0 else -cur_deriv
        sum_1 += sum(derivs)

print(sum_1)
print(sum_2)

# But hey this also works
#
# from numpy.polynomial import Polynomial
#
# with open('09.txt', 'r') as in_file:
#     sum_1 = sum_2 = 0
#     for line in in_file:
#         values = [int(x) for x in line.rstrip().split()]
#         poly = Polynomial.fit(range(len(values)), values, len(values) - 1)
#         sum_1, sum_2 = sum_1 + round(poly(len(values))), sum_2 + round(poly(-1))
#
# print(sum_1)
# print(sum_2)
