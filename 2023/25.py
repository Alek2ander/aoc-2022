import math
import random
from copy import deepcopy
from itertools import count


def contract(vertices, edges, max_vertices, index_iter):
    while len(vertices) > max_vertices:
        edge = random.choices(list(edges.keys()), edges.values())[0]
        v1, v2 = edge
        new_v = next(index_iter)
        del edges[edge]
        vertices[new_v] = {'weight': vertices[v1]['weight'] + vertices[v2]['weight'], 'edges': {}}
        for source_v in (v1, v2):
            for other_v, other_e in vertices[source_v]['edges'].items():
                if other_e == edge:
                    continue
                new_edge = frozenset((new_v, other_v))
                vertices[new_v]['edges'][other_v] = new_edge
                vertices[other_v]['edges'][new_v] = new_edge
                if new_edge not in edges:
                    edges[new_edge] = 0
                edges[new_edge] += edges[other_e]
                del vertices[other_v]['edges'][source_v]
                del edges[other_e]
            del vertices[source_v]
    return vertices, edges


def min_cut(vertices, edges, index_iter):
    if len(vertices) <= 6:
        vertices, edges = contract(vertices, edges, 2, index_iter)
        return edges.popitem()[1], vertices.popitem()[1]['weight'] * vertices.popitem()[1]['weight']
    else:
        t = math.ceil(1 + len(vertices) / math.sqrt(2))
        min_edge_count_1, result_1 = min_cut(*contract(deepcopy(vertices), deepcopy(edges), t, index_iter), index_iter)
        if min_edge_count_1 == 3:
            return min_edge_count_1, result_1
        min_edge_count_2, result_2 = min_cut(*contract(deepcopy(vertices), deepcopy(edges), t, index_iter), index_iter)
        return min_edge_count_2, result_2


vertices = {}
edges = {}
with open('25.txt', 'r') as in_file:
    for line in in_file:
        left, right = line.rstrip().split(': ')
        if left not in vertices:
            vertices[left] = {'weight': 1, 'edges': {}}
        for vertex in right.split():
            if vertex not in vertices:
                vertices[vertex] = {'weight': 1, 'edges': {}}
            edge = frozenset((left, vertex))
            edges[edge] = 1
            vertices[left]['edges'][vertex] = edge
            vertices[vertex]['edges'][left] = edge
min_edge_count, result = len(edges), 0
while min_edge_count > 3:
    min_edge_count, result = min_cut(deepcopy(vertices), deepcopy(edges), count(0))
print(result)
