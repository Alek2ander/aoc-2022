cache = {}


def count_arrangements(data, i, running_count, span_i):
    if (cache_index := (data['seq'][i:], data['spans'][span_i:])) in cache and running_count == 0:
        return cache[cache_index]
    cur_span = data['spans'][span_i] if span_i < len(data['spans']) else 0
    if i >= len(data['seq']):
        if span_i >= len(data['spans']) or (span_i == len(data['spans']) - 1 and running_count == cur_span):
            return 1
        else:
            return 0
    if running_count > cur_span:
        return 0
    elif running_count == cur_span:
        match data['seq'][i]:
            case '#':
                result = 0
            case '.' | '?':
                result = count_arrangements(data, i + 1, 0, span_i + 1)
        if running_count == 0:
            cache[cache_index] = result
        return result
    elif 0 < running_count < cur_span:
        match data['seq'][i]:
            case '.':
                return 0
            case '#' | '?':
                return count_arrangements(data, i + 1, running_count + 1, span_i)
    else:
        match data['seq'][i]:
            case '#':
                cache[cache_index] = count_arrangements(data, i + 1, 1, span_i)
                return cache[cache_index]
            case '.':
                cache[cache_index] = count_arrangements(data, i + 1, 0, span_i)
                return cache[cache_index]
            case '?':
                if_broken = count_arrangements(data, i + 1, 1, span_i)
                if_good = count_arrangements(data, i + 1, 0, span_i)
                cache[cache_index] = if_broken + if_good
                return cache[cache_index]


sum_1 = sum_2 = 0
with open('12.txt', 'r') as in_file:
    for line in in_file:
        seq, spans = line.rstrip().split()
        spans = tuple(int(x) for x in spans.split(','))
        sum_1 += count_arrangements({'seq': seq, 'spans': spans}, 0, 0, 0)
        sum_2 += count_arrangements({'seq': '?'.join([seq] * 5), 'spans': spans * 5}, 0, 0, 0)
print(sum_1)
print(sum_2)
