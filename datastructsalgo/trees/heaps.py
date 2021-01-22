from datastructsalgo.utils.misc_util import _check_type, NoneType, TreeNode
from datastructsalgo.linear_data_structures.arrays import (ArrayForTrees,
     DynamicOneDimensionalArray, Array)

__all__ = [
    'BinaryHeap',
    'DHeap'
]

class Heap(object):
    """
    Abstract class for representing heaps.
    """
    pass


class DHeap(Heap):
    """
    Represents D-ary Heap.

    Parameters
    ==========

    elements : list, tuple, Array
        Optional, by default 'None'.
        list/tuple/Array of initial TreeNode in Heap.


    heap_property : str
        If the key stored in each node is
        either greater than or equal to
        the keys in the node's children
        then pass 'max'.
        If the key stored in each node is
        either less than or equal to
        the keys in the node's children
        then pass 'min'.
        By default, the heap property is
        set to 'min'.

    Examples
    ========

    >>> from datastructsalgo.trees.heaps import DHeap
    >>> min_heap = DHeap(heap_property="min", d=3)
    >>> min_heap.insert(1, 1)
    >>> min_heap.insert(5, 5)
    >>> min_heap.insert(7, 7)
    >>> min_heap.extract().key
    1
    >>> min_heap.insert(4, 4)
    >>> min_heap.extract().key
    4

    >>> max_heap = DHeap(heap_property='max', d=2)
    >>> max_heap.insert(1, 1)
    >>> max_heap.insert(5, 5)
    >>> max_heap.insert(7, 7)
    >>> max_heap.extract().key
    7
    >>> max_heap.insert(6, 6)
    >>> max_heap.extract().key
    6

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/D-ary_heap
    """
    __slots__ = ['_comp', 'heap', 'd', 'heap_property', '_last_pos_filled']

    def __new__(cls, elements=None, heap_property="min", d=4):
        obj = Heap.__new__(cls)
        obj.heap_property = heap_property
        obj.d = d
        if heap_property == "min":
            obj._comp = lambda key_parent, key_child: key_parent <= key_child
        elif heap_property == "max":
            obj._comp = lambda key_parent, key_child: key_parent >= key_child
        else:
            raise ValueError("%s is invalid heap property"%(heap_property))
        if elements is None:
            elements = DynamicOneDimensionalArray(TreeNode, 0)
        elif _check_type(elements, (list,tuple)):
            elements = DynamicOneDimensionalArray(TreeNode, len(elements), elements)
        elif _check_type(elements, Array):
            elements = DynamicOneDimensionalArray(TreeNode, len(elements), elements._data)
        else:
            raise ValueError(f'Expected a list/tuple/Array of TreeNode got {type(elements)}')
        obj.heap = elements
        obj._last_pos_filled = obj.heap._last_pos_filled
        obj._build()
        return obj

    @classmethod
    def methods(cls):
        return ['__new__', 'insert', 'extract', '__str__', 'is_empty']

    def _build(self):
        for i in range(self._last_pos_filled + 1):
            self.heap[i]._leftmost, self.heap[i]._rightmost = \
                self.d*i + 1, self.d*i + self.d
        for i in range((self._last_pos_filled + 1)//self.d, -1, -1):
            self._heapify(i)

    def _swap(self, idx1, idx2):
        idx1_key, idx1_data = \
            self.heap[idx1].key, self.heap[idx1].data
        self.heap[idx1].key, self.heap[idx1].data = \
            self.heap[idx2].key, self.heap[idx2].data
        self.heap[idx2].key, self.heap[idx2].data = \
            idx1_key, idx1_data

    def _heapify(self, i):
        while True:
            target = i
            l = self.d*i + 1
            r = self.d*i + self.d

            for j in range(l, r+1):
                if j <= self._last_pos_filled:
                    target = j if self._comp(self.heap[j].key, self.heap[target].key) \
                            else target
                else:
                    break

            if target != i:
                self._swap(target, i)
                i = target
            else:
                break

    def insert(self, key, data=None):
        """
        Insert a new element to the heap according to heap property.

        Parameters
        ==========

        key
            The key for comparison.

        data
            The data to be inserted.

        Returns
        =======

        None
        """
        new_node = TreeNode(key, data)
        self.heap.append(new_node)
        self._last_pos_filled += 1
        i = self._last_pos_filled
        self.heap[i]._leftmost, self.heap[i]._rightmost = self.d*i + 1, self.d*i + self.d

        while True:
            parent = (i - 1)//self.d
            if i == 0 or self._comp(self.heap[parent].key, self.heap[i].key):
                break
            else:
                self._swap(i, parent)
                i = parent

    def extract(self):
        """
        Extract root element of the Heap.

        Returns
        =======

        root_element : TreeNode
            The TreeNode at the root of the heap,
            if the heap is not empty.

        None
            If the heap is empty.
        """
        if self._last_pos_filled == -1:
            raise IndexError("Heap is empty.")
        else:
            element_to_be_extracted = TreeNode(self.heap[0].key, self.heap[0].data)
            self._swap(0, self._last_pos_filled)
            self.heap.delete(self._last_pos_filled)
            self._last_pos_filled -= 1
            self._heapify(0)
            return element_to_be_extracted

    def __str__(self):
        to_be_printed = ['' for i in range(self._last_pos_filled + 1)]
        for i in range(self._last_pos_filled + 1):
            node = self.heap[i]
            if node._leftmost <= self._last_pos_filled:
                if node._rightmost <= self._last_pos_filled:
                    children = list(range(node._leftmost, node._rightmost + 1))
                else:
                    children = list(range(node._leftmost, self._last_pos_filled + 1))
            else:
                children = []
            to_be_printed[i] = (node.key, node.data, children)
        return str(to_be_printed)

    @property
    def is_empty(self):
        """
        Checks if the heap is empty.
        """
        return self.heap._last_pos_filled == -1


class BinaryHeap(DHeap):
    """
    Represents Binary Heap.

    Parameters
    ==========

    elements : list, tuple
        Optional, by default 'None'.
        List/tuple of initial elements in Heap.

    heap_property : str
        If the key stored in each node is
        either greater than or equal to
        the keys in the node's children
        then pass 'max'.
        If the key stored in each node is
        either less than or equal to
        the keys in the node's children
        then pass 'min'.
        By default, the heap property is
        set to 'min'.

    Examples
    ========

    >>> from datastructsalgo.trees.heaps import BinaryHeap
    >>> min_heap = BinaryHeap(heap_property="min")
    >>> min_heap.insert(1, 1)
    >>> min_heap.insert(5, 5)
    >>> min_heap.insert(7, 7)
    >>> min_heap.extract().key
    1
    >>> min_heap.insert(4, 4)
    >>> min_heap.extract().key
    4

    >>> max_heap = BinaryHeap(heap_property='max')
    >>> max_heap.insert(1, 1)
    >>> max_heap.insert(5, 5)
    >>> max_heap.insert(7, 7)
    >>> max_heap.extract().key
    7
    >>> max_heap.insert(6, 6)
    >>> max_heap.extract().key
    6

    References
    ==========

    .. [1] https://en.m.wikipedia.org/wiki/Binary_heap
    """
    def __new__(cls, elements=None, heap_property="min"):
        obj = DHeap.__new__(cls, elements, heap_property, 2)
        return obj

    @classmethod
    def methods(cls):
        return ['__new__']
