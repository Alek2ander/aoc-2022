import math

# i * (t - i) > r
# ⇓
# ⌈ t² - 4r > 0 ⇒ i ∈ (t - sqrt(t^2 - 4r) / 2; t + sqrt(t^2 - 4r) / 2)
# ⌊ t² - 4r ≤ 0 ⇒ i ∈ ∅

with open('06.txt', 'r') as in_file:
    times_line = in_file.readline().split(':')[1]
    times = [int(''.join(filter(str.isdigit, times_line)))]
    times += [int(i) for i in times_line.split() if i]
    records_line = in_file.readline().split(':')[1]
    records = [int(''.join(filter(str.isdigit, records_line)))]
    records += [int(i) for i in records_line.split() if i]
    product_1 = 1
    result_2 = 0
    for i, (t, r) in enumerate(zip(times, records)):
        if (d := t ** 2 - 4 * r) > 0:
            result = math.ceil(t / 2 + (rt := math.sqrt(d)) / 2) - math.floor(t / 2 - rt / 2) - 1
            if i == 0:
                result_2 = result
            else:
                product_1 *= result
        elif i > 0:
            product_1 = 0
            break

print(product_1)
print(result_2)
