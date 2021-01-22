from datastructsalgo import Graph, AdjacencyListGraphNode
from datastructsalgo.graphs.algorithms import shortest_paths
import sys

def read(data_type):
    return list(map(data_type, sys.stdin.readline().strip().split()))

N = int(input())
E = int(input())

nodes = []
for n in range(N):
    nodes.append(AdjacencyListGraphNode(str(n + 1)))

graph = Graph(*nodes)
for _ in range(E):
    u, v, t = read(str)
    graph.add_edge(u, v, int(t))
    graph.add_edge(v, u, int(t))

K = int(input())
cache = {}
for _ in range(K):
    u, v = read(str)
    if u not in cache:
        costs = shortest_paths(graph, 'dijkstra', u)[0]
        cache[u] = costs
    print(cache[u][v])
