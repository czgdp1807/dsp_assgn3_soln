__all__ = [
    'TreeNode',
    'AdjacencyListGraphNode',
    'GraphEdge'
]

_check_type = lambda a, t: isinstance(a, t)
NoneType = type(None)

class Node(object):
    """
    Abstract class representing a node.
    """
    pass

class TreeNode(Node):
    """
    Represents node in trees.

    Parameters
    ==========

    key
        Required for comparison operations.
    data
        Any valid data to be stored in the node.
    left: int
        Optional, index of the left child node.
    right: int
        Optional, index of the right child node.
    """

    __slots__ = ['key', 'data', 'left', 'right', 'is_root',
                 'height', 'parent', 'size']

    @classmethod
    def methods(cls):
        return ['__new__', '__str__']

    def __new__(cls, key, data=None):
        obj = Node.__new__(cls)
        obj.data, obj.key = data, key
        obj.left, obj.right, obj.parent, obj.height, obj.size = \
            None, None, None, 0, 1
        obj.is_root = False
        return obj

    def __str__(self):
        """
        Used for printing.
        """
        return str((self.left, self.key, self.data, self.right))

class GraphNode(Node):
    """
    Abastract class for graph nodes/vertices.
    """
    def __str__(self):
        return str((self.name, self.data))

class AdjacencyListGraphNode(GraphNode):
    """
    Represents nodes for adjacency list implementation
    of graphs.

    Parameters
    ==========

    name: str
        The name of the node by which it is identified
        in the graph. Must be unique.
    data
        The data to be stored at each graph node.
    adjacency_list: list
        Any valid iterator to initialize the adjacent
        nodes of the current node.
        Optional, by default, None
    """
    @classmethod
    def methods(cls):
        return ['__new__', 'add_adjacent_node',
                'remove_adjacent_node']

    def __new__(cls, name, data=None, adjacency_list=None):
        obj = GraphNode.__new__(cls)
        obj.name, obj.data = str(name), data
        obj._impl = 'adjacency_list'
        if adjacency_list is not None:
            for node in adjacency_list:
                obj.__setattr__(node.name, node)
        obj.adjacent = adjacency_list if adjacency_list is not None \
                       else []
        return obj

    def add_adjacent_node(self, name, data=None):
        """
        Adds adjacent node to the current node's
        adjacency list with given name and data.
        """
        if hasattr(self, name):
            getattr(self, name).data = data
        else:
            new_node = AdjacencyListGraphNode(name, data)
            self.__setattr__(new_node.name, new_node)
            self.adjacent.append(new_node.name)

    def remove_adjacent_node(self, name):
        """
        Removes node with given name from
        adjacency list.
        """
        if not hasattr(self, name):
            raise ValueError("%s is not adjacent to %s"%(name, self.name))
        self.adjacent.remove(name)
        delattr(self, name)

class GraphEdge(object):
    """
    Represents the concept of edges in graphs.

    Parameters
    ==========

    node1: GraphNode or it's child classes
        The source node of the edge.
    node2: GraphNode or it's child classes
        The target node of the edge.
    """
    @classmethod
    def methods(cls):
        return ['__new__', '__str__']

    def __new__(cls, node1, node2, value=None):
        obj = object.__new__(cls)
        obj.source, obj.target = node1, node2
        obj.value = value
        return obj

    def __str__(self):
        return str((self.source.name, self.target.name))
