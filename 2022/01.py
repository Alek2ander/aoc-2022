import heapq


def get_elves():
    cur_cal = 0
    with open('01.txt', 'r') as in_file:
        for line in in_file.read().split('\n'):
            if line == '':
                yield cur_cal
                cur_cal = 0
            else:
                cur_cal += int(line)
    yield cur_cal


top3 = heapq.nlargest(3, get_elves())  # using builtins is pythonic :^)
print(top3[0])
print(sum(top3))
