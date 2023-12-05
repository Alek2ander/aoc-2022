def check_counter(cycle, x, s):
    s['part2'] += '#' if abs(cycle % 40 - x) <= 1 else '.'
    if cycle % 40 == 19:
        s['part1'] += (cycle + 1) * x


cycle, x = -1, 1
solution = {
    'part1': 0,
    'part2': ''
}

with open('10.txt', 'r') as in_file:
    for line in in_file.read().split('\n'):
        if len(line) == 0:
            continue
        match line.split():
            case ['noop']:
                check_counter(cycle := cycle + 1, x, solution)
            case ['addx', v]:
                check_counter(cycle := cycle + 1, x, solution)
                check_counter(cycle := cycle + 1, x, solution)
                x += int(v)

print(solution['part1'])
print('\n'.join(solution['part2'][p:p + 40] for p in range(0, len(solution['part2']), 40)))
