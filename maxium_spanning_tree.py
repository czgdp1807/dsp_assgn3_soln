from datastructsalgo import Graph, AdjacencyListGraphNode, minimum_spanning_tree
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
    u, v, c = read(str)
    graph.add_edge(u, v, -int(c))
    graph.add_edge(v, u, -int(c))

mst = minimum_spanning_tree(graph, 'prim')
for edge in mst.edge_weights.keys():
    u, v = edge.split("_")
    if int(u) <= int(v):
        print(u, v)
