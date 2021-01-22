"""
Contains algorithms associated with graph
data structure.
"""
from collections import deque
from datastructsalgo.miscellaneous_data_structures import PriorityQueue
from datastructsalgo.graphs.graph import Graph

__all__ = [
    'minimum_spanning_tree',
    'shortest_paths'
]

Stack = Queue = deque

def _generate_mst_object(graph):
    mst = Graph(*[getattr(graph, str(v)) for v in graph.vertices])
    return mst

def _sort_edges(graph, num_threads=None):
    edges = list(graph.edge_weights.items())
    if num_threads is None:
        sort_key = lambda item: item[1].value
        return sorted(edges, key=sort_key)

    merge_sort_parallel(edges, num_threads,
                        comp=lambda u,v: u[1].value <= v[1].value)
    return edges

def _minimum_spanning_tree_prim_adjacency_list(graph):
    q = PriorityQueue(implementation='binary_heap')
    e = {}
    mst = Graph(implementation='adjacency_list')
    q.push(next(iter(graph.vertices)), 0)
    while not q.is_empty:
        v = q.pop()
        if not hasattr(mst, v):
            mst.add_vertex(graph.__getattribute__(v))
            if e.get(v, None) is not None:
                edge = e[v]
                mst.add_vertex(edge.target)
                mst.add_edge(edge.source.name, edge.target.name, edge.value)
                mst.add_edge(edge.target.name, edge.source.name, edge.value)
            for w_node in graph.neighbors(v):
                w = w_node.name
                vw = graph.edge_weights[v + '_' + w]
                q.push(w, vw.value)
                if e.get(w, None) is None or \
                    e[w].value > vw.value:
                    e[w] = vw
    return mst

def minimum_spanning_tree(graph, algorithm):
    """
    Computes a minimum spanning tree for the given
    graph and algorithm.

    Parameters
    ==========

    graph: Graph
        The graph whose minimum spanning tree
        has to be computed.
    algorithm: str
        The algorithm which should be used for
        computing a minimum spanning tree.
        Currently the following algorithms are
        supported,
        'kruskal' -> Kruskal's algorithm as given in
                     [1].
        'prim' -> Prim's algorithm as given in [2].

    Returns
    =======

    mst: Graph
        A minimum spanning tree using the implementation
        same as the graph provided in the input.

    Examples
    ========

    >>> from datastructsalgo import Graph, AdjacencyListGraphNode
    >>> from datastructsalgo import minimum_spanning_tree
    >>> u = AdjacencyListGraphNode('u')
    >>> v = AdjacencyListGraphNode('v')
    >>> G = Graph(u, v)
    >>> G.add_edge(u.name, v.name, 3)
    >>> mst = minimum_spanning_tree(G, 'kruskal')
    >>> u_n = mst.neighbors(u.name)
    >>> mst.get_edge(u.name, u_n[0].name).value
    3

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Kruskal%27s_algorithm
    .. [2] https://en.wikipedia.org/wiki/Prim%27s_algorithm

    Note
    ====

    The concept of minimum spanning tree is valid only for
    connected and undirected graphs. So, this function
    should be used only for such graphs. Using with other
    types of graphs may lead to unwanted results.
    """
    import datastructsalgo.graphs.algorithms as algorithms
    func = "_minimum_spanning_tree_" + algorithm + "_" + graph._impl
    if not hasattr(algorithms, func):
        raise NotImplementedError(
        "Currently %s algoithm for %s implementation of graphs "
        "isn't implemented for finding minimum spanning trees."
        %(algorithm, graph._impl))
    return getattr(algorithms, func)(graph)

def shortest_paths(graph: Graph, algorithm: str,
                   source: str, target: str="") -> tuple:
    """
    Finds shortest paths in the given graph from a given source.

    Parameters
    ==========

    graph: Graph
        The graph under consideration.
    algorithm: str
        The algorithm to be used. Currently, the following algorithms
        are implemented,
        'bellman_ford' -> Bellman-Ford algorithm as given in [1].
        'dijkstra' -> Dijkstra algorithm as given in [2].
    source: str
        The name of the source the node.
    target: str
        The name of the target node.
        Optional, by default, all pair shortest paths
        are returned.

    Returns
    =======

    (distances, predecessors): (dict, dict)
        If target is not provided and algorithm used
        is 'bellman_ford'/'dijkstra'.
    (distances[target], predecessors): (float, dict)
        If target is provided and algorithm used is
        'bellman_ford'/'dijkstra'.

    Examples
    ========

    >>> from datastructsalgo import Graph, AdjacencyListGraphNode
    >>> from datastructsalgo import shortest_paths
    >>> V1 = AdjacencyListGraphNode("V1")
    >>> V2 = AdjacencyListGraphNode("V2")
    >>> V3 = AdjacencyListGraphNode("V3")
    >>> G = Graph(V1, V2, V3)
    >>> G.add_edge('V2', 'V3', 10)
    >>> G.add_edge('V1', 'V2', 11)
    >>> shortest_paths(G, 'bellman_ford', 'V1')
    ({'V1': 0, 'V2': 11, 'V3': 21}, {'V1': None, 'V2': 'V1', 'V3': 'V2'})
    >>> shortest_paths(G, 'dijkstra', 'V1')
    ({'V2': 11, 'V3': 21, 'V1': 0}, {'V1': None, 'V2': 'V1', 'V3': 'V2'})

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm
    .. [2] https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    """
    import datastructsalgo.graphs.algorithms as algorithms
    func = "_" + algorithm + "_" + graph._impl
    if not hasattr(algorithms, func):
        raise NotImplementedError(
        "Currently %s algorithm isn't implemented for "
        "finding shortest paths in graphs."%(algorithm))
    return getattr(algorithms, func)(graph, source, target)

def _dijkstra_adjacency_list(graph: Graph, start: str, target: str):
    V = len(graph.vertices)
    visited, dist, pred = {}, {}, {}
    for v in graph.vertices:
        visited[v] = False
        pred[v] = None
        if v != start:
            dist[v] = float('inf')
    dist[start] = 0
    pq = PriorityQueue(implementation='binary_heap')
    for vertex in dist:
        pq.push(vertex, dist[vertex])
    for _ in range(V):
        u = pq.pop()
        visited[u] = True
        for v in graph.vertices:
            edge_str = u + '_' + v
            if (edge_str in graph.edge_weights and graph.edge_weights[edge_str].value > 0 and
                visited[v] is False and dist[v] > dist[u] + graph.edge_weights[edge_str].value):
                dist[v] = dist[u] + graph.edge_weights[edge_str].value
                pred[v] = u
                pq.push(v, dist[v])

    if target != "":
        return (dist[target], pred)
    return dist, pred

_dijkstra_adjacency_matrix = _dijkstra_adjacency_list
