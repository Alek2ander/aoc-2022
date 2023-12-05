from __future__ import annotations
from typing import Dict


class Node:
    parent: Node = None
    size: int
    contents: Dict[str, Node]

    def __init__(self, size: int):
        self.size = size
        self.contents = {}

    def add(self, name: str, other: Node):
        self.contents[name] = other
        other.parent = self
        self.update_size(other.size)

    def update_size(self, size):
        self.size += size
        if self.parent:
            self.parent.update_size(size)


class Dir(Node):
    def __init__(self):
        super().__init__(0)

    def solve(self, s: Solution):
        if self.size <= 100000:
            s.total_size_part1 += self.size
        if s.min_size_req <= self.size < s.min_size_part2:
            s.min_size_part2 = self.size
        for node in self.contents.values():
            if isinstance(node, Dir):
                node.solve(s)


root = Dir()
cwd = root

with open('07.txt', 'r') as in_file:
    for line in in_file.read().split('\n'):
        if len(line) == 0:
            continue
        match line.split():
            case ['$', 'cd', '/']:
                cwd = root
            case ['$', 'cd', '..']:
                cwd = cwd.parent
            case ['$', 'cd', subdir]:
                cwd = cwd.contents[subdir]
            case ['$', 'ls']:
                pass  # it's not like we care about validation
            case ['dir', name]:
                cwd.add(name, Dir())
            case [size, name]:  # once again, validation is for production code
                cwd.add(name, Node(int(size)))


class Solution:  # could have been a dict but we OOP today
    total_size_part1 = 0
    min_size_req = root.size - 40000000
    min_size_part2 = root.size


root.solve(result := Solution())
print(result.total_size_part1)
print(result.min_size_part2)
