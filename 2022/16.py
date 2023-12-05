import re
from itertools import product

caves = {}
start = 'AA'
with open('16.txt', 'r') as in_file:
    for data in re.findall(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([\w, ]+)',
                                   in_file.read()):
        valve_id, flow, neighbors = data
        caves[valve_id] = (int(flow), set(c for c in neighbors.split(', ')))
distance_matrix = {c1: {c2: len(caves) for c2 in caves} for c1 in caves}
for c in caves:
    distance_matrix[c][c] = 0
    for n in caves[c][1]:
        distance_matrix[c][n] = 1
for k, i, j in product(caves, caves, caves):
    if distance_matrix[i][j] > distance_matrix[i][k] + distance_matrix[k][j]:
        distance_matrix[i][j] = distance_matrix[i][k] + distance_matrix[k][j]
caves = {c: f for c, (f, _) in caves.items() if f > 0 or c == start}
distance_matrix = {c1: {c2: d + 1 for c2, d in row.items() if c2 in caves}
                   for c1, row in distance_matrix.items() if c1 in caves}


def release_pressure(workers, steps):
    dynamic = [{k: (None,) * workers for k in product(*((caves,) * workers))}]
    dynamic[0][(start,) * workers] = tuple((0, 0, frozenset()) for _ in range(workers))
    step_estimates = []
    for i in range(1, steps + 1):
        step = {}
        best_best_estimate = 0
        for cur_caves in dynamic[-1]:
            valves_here = set(cur_caves)
            if cur_caves != (start,) * workers and len(valves_here) < workers:
                continue
            candidates = []
            for w in range(workers):
                worker_candidates = {}
                if caves[cur_caves[w]] == 0:
                    if (this_cave := dynamic[-1][cur_caves][w]) is None:
                        worker_candidates[frozenset()] = (None, 0)
                    else:
                        prev_flow, prev_total, prev_valves = this_cave
                        flow = prev_flow
                        total = prev_total + prev_flow
                        valves = prev_valves
                        estimate = total + flow * (steps - i)
                        worker_candidates[valves] = ((flow, total, valves), estimate)
                else:
                    for prev_caves in dynamic[-1]:
                        d = distance_matrix[prev_caves[w]][cur_caves[w]]
                        if d > i or dynamic[i - d][prev_caves][w] is None:
                            continue
                        prev_flow, prev_total, prev_valves = dynamic[i - d][prev_caves][w]
                        if len(intersect := valves_here & prev_valves) > 1 \
                                or (len(intersect) == 1 and prev_caves[w] != cur_caves[w]):
                            continue
                        elif len(intersect) == 1:
                            flow = prev_flow
                            total = prev_total + prev_flow
                            valves = prev_valves
                            estimate = total + flow * (steps - i)
                            worker_candidates[valves] = ((flow, total, valves), estimate)
                        else:
                            flow = prev_flow + caves[cur_caves[w]]
                            total = prev_total + prev_flow * d
                            valves = frozenset(prev_valves | {cur_caves[w]})
                            estimate = total + flow * (steps - i)
                        if valves in worker_candidates and worker_candidates[valves][1] >= estimate:
                            continue
                        worker_candidates[valves] = ((flow, total, valves), estimate)
                candidates.append([(v[0], v[1], k) for k, v in worker_candidates.items()])
            best_estimate = None
            best = (None,) * workers
            for combination in product(*candidates):
                valves = set()
                valve_counter = 0
                for c in combination:
                    valves |= c[2]
                    valve_counter += len(c[2])
                if len(valves) < valve_counter:
                    continue
                estimate = sum(c[1] for c in combination)
                if best_estimate is None or estimate > best_estimate:
                    best_estimate = estimate
                    best = tuple(c[0] for c in combination)
            step[cur_caves] = best
            if best_estimate is not None and best_estimate > best_best_estimate:
                best_best_estimate = best_estimate
        dynamic.append(step)
        step_estimates.append(best_best_estimate)
    return step_estimates


step_estimates = release_pressure(1, 30)
print(step_estimates[-1])
step_estimates = release_pressure(2, 26)
print(step_estimates[-1])
