from dataclasses import dataclass
from heapq import heappush, heappop, heapify


@dataclass(order=True)
class MapNode:
    cost: int
    cost_from_start: int
    cost_to_finish: int
    x: int
    y: int

    def get_cost(self, x, y):
        return abs(self.x - x) + abs(self.y - y)


terrain = []
adjacent = ((-1, 0), (1, 0), (0, -1), (0, 1))
start = end = None
with open('12.txt', 'r') as in_file:
    for y, line in enumerate(in_file.read().split('\n')):
        if len(line) == 0:
            continue
        if (x := line.find('S')) > -1:
            end = MapNode(0, 0, 0, x, y)
            line = line[:x] + 'a' + line[x + 1:]
        if (x := line.find('E')) > -1:
            start = MapNode(0, 0, 0, x, y)
            line = line[:x] + 'z' + line[x + 1:]
        terrain.append(line)

start.cost_to_finish = start.cost = start.get_cost(end.x, end.y)
queue = []
done = {}
visited = {(start.x, start.y): start}
heappush(queue, start)
part2_dist = part1_dist = len(terrain) * len(terrain[0])
while len(queue):
    cur_node = heappop(queue)
    if cur_node.x == end.x and cur_node.y == end.y:
        part1_dist = cur_node.cost_from_start
    if terrain[cur_node.y][cur_node.x] == 'a' and cur_node.cost_from_start < part2_dist:
        part2_dist = cur_node.cost_from_start
    del visited[(cur_node.x, cur_node.y)]
    done[(cur_node.x, cur_node.y)] = cur_node
    for shift in adjacent:
        if (yy := cur_node.y + shift[0]) < 0 or yy >= len(terrain):
            continue
        if (xx := cur_node.x + shift[1]) < 0 or xx >= len(terrain[0]):
            continue
        if (xx, yy) in done:
            continue
        if terrain[cur_node.y][cur_node.x] > chr(ord(terrain[yy][xx]) + 1):
            continue
        cost_from_start, cost_to_finish = cur_node.cost_from_start + 1, end.get_cost(xx, yy)
        if (xx, yy) in visited:
            visited[(xx, yy)].cost_from_start = cost_from_start
            visited[(xx, yy)].cost = cost_from_start + cost_to_finish
            heapify(queue)
        else:
            heappush(queue, node := MapNode(cost_from_start + cost_to_finish, cost_from_start, cost_to_finish, xx, yy))
            visited[(xx, yy)] = node
print(part1_dist)
print(part2_dist)
