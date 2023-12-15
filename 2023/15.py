def deer_hash(s):
    h = 0
    for c in s:
        h = ((h + ord(c)) * 17) % 256
    return h


sum_1 = sum_2 = 0
hashmap = {}
with open('15.txt', 'r') as in_file:
    for line in in_file.read().split(','):
        sum_1 += deer_hash(line)
        if line[-1] == '-':
            hashmap.pop(line[:-1], 0)
        else:
            label, lens = line.split('=')
            hashmap[label] = int(lens)

counters = [0] * 256
for label, lens in hashmap.items():
    box = deer_hash(label)
    counters[box] = i = counters[box] + 1
    sum_2 += (box + 1) * i * lens

print(sum_1)
print(sum_2)
