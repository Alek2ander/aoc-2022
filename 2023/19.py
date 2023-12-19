import re
from math import prod


def find_accepted_values(workflow, bounds, visited, results):
    if workflow == 'R' or workflow in visited:
        return
    elif workflow == 'A':
        results.append(bounds)
        return
    for step in workflows[workflow]:
        match step['op']:
            case '>':
                b_true = {'min': max(bounds[step['key']]['min'], step['val'] + 1), 'max': bounds[step['key']]['max']}
                b_false = {'min': bounds[step['key']]['min'], 'max': min(bounds[step['key']]['max'], step['val'] + 1)}
                if b_true['min'] < b_true['max']:
                    new_bounds = {**bounds, step['key']: b_true}
                    find_accepted_values(step['dest'], new_bounds, visited | {workflow}, results)
                if b_false['min'] < b_false['max']:
                    bounds[step['key']] = b_false
                else:
                    return
            case '<':
                b_true = {'min': bounds[step['key']]['min'], 'max': min(bounds[step['key']]['max'], step['val'])}
                b_false = {'min': max(bounds[step['key']]['min'], step['val']), 'max': bounds[step['key']]['max']}
                if b_true['min'] < b_true['max']:
                    new_bounds = {**bounds, step['key']: b_true}
                    find_accepted_values(step['dest'], new_bounds, visited | {workflow}, results)
                if b_false['min'] < b_false['max']:
                    bounds[step['key']] = b_false
                else:
                    return
            case '':
                find_accepted_values(step['dest'], bounds, visited | {workflow}, results)
                return
            case s:
                print(f'Unexpected operator: {s}')


workflows = {}
sum_1 = 0
with open('19.txt', 'r') as in_file:
    while line := in_file.readline().rstrip():
        label, data = line.split('{')
        steps = re.findall(r'(?:(\w)(.)(\d+):)?(\w+)[,}]', data)
        workflows[label] = [{'key': step[0], 'op': step[1],
                             'val': int(step[2]) if step[2] else 0, 'dest': step[3]}
                            for step in steps]
    accepted = []
    find_accepted_values('in', {k: {'min': 1, 'max': 4001} for k in 'xmas'}, set(), accepted)
    while line := in_file.readline().rstrip():
        params = re.findall(r'(\w)=(\d+)[,}]', line)
        part = {k: int(v) for k, v in params}
        for prism in accepted:
            in_prism = True
            for key in 'xmas':
                if part[key] < prism[key]['min'] or part[key] >= prism[key]['max']:
                    in_prism = False
                    break
            if in_prism:
                sum_1 += sum(part.values())
                break

print(sum_1)
print(sum(prod(edge['max'] - edge['min'] for edge in prism.values()) for prism in accepted))
