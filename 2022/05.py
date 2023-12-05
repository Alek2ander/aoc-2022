import re
from copy import deepcopy

stacks = None
with open('05.txt', 'r') as in_file:
    while line := in_file.readline():
        if line == '\n':
            break
        crates = line[1::4]
        if not stacks:
            stacks = [[] for i in range(len(crates))]
        for stack, crate in zip(stacks, crates):
            if crate != ' ':
                stack.append(crate)
    stacks_part1 = stacks
    stacks_part2 = deepcopy(stacks_part1)
    while line := in_file.readline():
        amt, stack_from, stack_to = map(int, line.split()[1::2])
        stacks_part1[stack_from - 1], stacks_part1[stack_to - 1] = \
            stacks_part1[stack_from - 1][amt:], \
            stacks_part1[stack_from - 1][amt-1::-1] + stacks_part1[stack_to - 1]
        stacks_part2[stack_from - 1], stacks_part2[stack_to - 1] = \
            stacks_part2[stack_from - 1][amt:], \
            stacks_part2[stack_from - 1][:amt] + stacks_part2[stack_to - 1]

print(''.join(stack[0] for stack in stacks_part1))
print(''.join(stack[0] for stack in stacks_part2))
