from sortedcontainers import SortedDict
from functools import reduce


def add_range(ranges, new_range):
    cur_start, cur_length = new_range
    if cur_length == 0:
        return ranges
    i = ranges.bisect_right(cur_start)
    if i > 0:
        prev_start, prev_length = ranges.peekitem(i - 1)
        if prev_start + prev_length == cur_start:
            ranges[prev_start] += cur_length
            return ranges
    if i < len(ranges):
        next_start, next_length = ranges.peekitem(i)
        if next_start == cur_start + cur_length:
            ranges[cur_start] = cur_length + next_length
            del ranges[next_start]
            return ranges
    ranges[cur_start] = cur_length
    return ranges


def convert_ranges(conv, ranges):
    new_ranges = SortedDict()
    cur_start, cur_length = ranges.popitem()
    while True:
        new_length = 0
        i = conv.bisect_right(cur_start)
        if i > 0:
            prev_start, (prev_dest, prev_length) = conv.peekitem(i - 1)
            valid_length = prev_start - cur_start + prev_length
            if valid_length > 0:
                add_range(new_ranges, (prev_dest + cur_start - prev_start,
                                       new_length := min(cur_length, valid_length)))
        if new_length == 0:
            if i < len(conv):
                next_start, _ = conv.peekitem(i)
                valid_length = next_start - cur_start
            else:
                valid_length = cur_length
            add_range(new_ranges, (cur_start,
                                   new_length := min(cur_length, valid_length)))
        cur_start += new_length
        cur_length -= new_length
        if cur_length <= 0:
            if len(ranges):
                cur_start, cur_length = ranges.popitem()
            else:
                return new_ranges


with open('05.txt', 'r') as in_file:
    _, data = in_file.readline().rstrip().split(': ')
    seeds = [int(seed) for seed in data.split(' ')]
    ranges_1 = reduce(add_range, ((seed, 1) for seed in seeds), SortedDict())
    ranges_2 = reduce(add_range, (rng for rng in zip(seeds[::2], seeds[1::2])), SortedDict())
    in_file.readline()
    in_file.readline()
    conv = SortedDict()
    while True:
        line = in_file.readline().rstrip()
        if len(line):
            dest, source, length = map(int, line.split(' '))
            conv[source] = (dest, length)
        else:
            ranges_1 = convert_ranges(conv, ranges_1)
            ranges_2 = convert_ranges(conv, ranges_2)
            if len(in_file.readline()):
                conv = SortedDict()
            else:
                break

print(ranges_1.peekitem(0)[0])
print(ranges_2.peekitem(0)[0])
