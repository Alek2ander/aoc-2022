from itertools import combinations

network = {}
complete_networks = []

def bors_kerbosch(complete, process, exclude):
    if not process and not exclude:
        if len(complete) > 2:
            complete_networks.append(complete)
        return
    _, pivot = max((len(network[c]), c) for c in process | exclude)
    for c in process - network[pivot]:
        bors_kerbosch(complete | {c}, process & network[c], exclude & network[c])
        process.remove(c)
        exclude.add(c)
    return

with open('23.txt', 'r') as in_file:
    for line in in_file.readlines():
        ca, cb = line.strip().split('-')
        if ca not in network:
            network[ca] = set()
        if cb not in network:
            network[cb] = set()
        network[ca].add(cb)
        network[cb].add(ca)
count_1 = 0
for i in range(26):
    ca = 't' + chr(ord('a') + i)
    if ca not in network or len(network[ca]) < 2:
        continue
    for (cb, cc) in combinations(network[ca], 2):
        if (cb.startswith('t') and cb < ca) or (cc.startswith('t') and cc < ca):
            continue
        if cb in network[cc]:
            count_1 += 1
bors_kerbosch(set(), set(network.keys()), set())
_, max_complete_network = max((len(s), s) for s in complete_networks)
print(count_1)
print(','.join(sorted(max_complete_network)))
