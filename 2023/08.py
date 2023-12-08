import itertools
import re

with open('08.txt', 'r') as in_file:
    directions = in_file.readline().rstrip()
    connections = {}
    nodes = {}
    for node in re.findall(r'(.+) = \((.+), (.+)\)', in_file.read()):
        source, l_dest, r_dest = node
        connections[source] = {'L': l_dest, 'R': r_dest}
        if source.endswith('A'):
            nodes[source] = {'states': {(0, source): 0}, 'targets': []}

cur_node = 'AAA'
i = c = 0
while cur_node != 'ZZZ':
    cur_node = connections[cur_node][directions[i]]
    c += 1
    i += 1
    if i == len(directions):
        i = 0
print(c)

for source, data in nodes.items():
    cur_node = source
    i = c = 0
    while True:
        cur_node = connections[cur_node][directions[i]]
        c += 1
        i += 1
        if i == len(directions):
            i = 0
        if cur_node.endswith('Z'):
            data['targets'].append(c)
        if (state := (i, cur_node)) in data['states']:
            data['loop'] = (start := data['states'][state], c - start)
            del data['states']
            break
        else:
            data['states'][state] = c


def extended_euclid(m, n):
    u, u1, v, v1 = 1, 0, 0, 1
    while n != 0:
        q, m, n = m // n, n, m % n
        u, u1 = u1, u - q * u1
        v, v1 = v1, v - q * v1
    return m, u, v


def check_fixed_target(loops, targets):
    fixed_target = None
    for (loop_start, loop_len), target in zip(loops, targets):
        if target < loop_start:
            if fixed_target is None:
                fixed_target = target
            if fixed_target != target:
                return None
    if fixed_target is None:
        return None
    for (loop_start, loop_len), target in zip(loops, targets):
        if target < loop_start:
            continue
        if target > fixed_target:
            return None
        if (fixed_target - target) % loop_len != 0:
            return None
    return fixed_target


def find_common_target(loops, targets, max_loop_start):
    m = loops[0][1]
    a = (targets[0] - max_loop_start) % m
    for (loop_start, loop_len), target in zip(loops[1:], targets[1:]):
        b, n = (target - max_loop_start) % loop_len, loop_len
        gcd, u, v = extended_euclid(m, n)
        d, check_mod = divmod(a - b, gcd)
        if check_mod != 0:
            return None
        m = m // gcd * n
        a = (b + n * v * d) % m
    return max_loop_start + a


min_result = None
loops = tuple(data['loop'] for data in nodes.values())
max_loop_start = max(loop[0] for loop in loops)
for targets in itertools.product(*(data['targets'] for data in nodes.values())):
    result = check_fixed_target(loops, targets)
    if result is None:
        result = find_common_target(loops, targets, max_loop_start)
    if result is None:
        continue
    if min_result is None or result < min_result:
        min_result = result

print(min_result)
