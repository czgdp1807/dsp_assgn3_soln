from pydatastructs.trees.heaps import BinaryHeap

__all__ = [
    'PriorityQueue'
]

class PriorityQueue(object):
    """
    Represents the concept of priority queue.

    Parameters
    ==========

    implementation: str
        The implementation which is to be
        used for supporting operations
        of priority queue.
        The following implementations are supported,
        'linked_list' -> Linked list implementation.
        'binary_heap' -> Binary heap implementation.
        'binomial_heap' -> Binomial heap implementation.
            Doesn't support custom comparators, minimum
            key data is extracted in every pop.
        Optional, by default, 'binary_heap' implementation
        is used.
    comp: function
        The comparator to be used while comparing priorities.
        Must return a bool object.
        By default, `lambda u, v: u < v` is used to compare
        priorities i.e., minimum priority elements are extracted
        by pop operation.

    Examples
    ========

    >>> from pydatastructs import PriorityQueue
    >>> pq = PriorityQueue()
    >>> pq.push(1, 2)
    >>> pq.push(2, 3)
    >>> pq.pop()
    1
    >>> pq2 = PriorityQueue(comp=lambda u, v: u > v)
    >>> pq2.push(1, 2)
    >>> pq2.push(2, 3)
    >>> pq2.pop()
    2

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Priority_queue
    """

    def __new__(cls, implementation='binary_heap', **kwargs):
        comp = kwargs.get("comp", lambda u, v: u < v)
        if implementation == 'binary_heap':
            return BinaryHeapPriorityQueue(comp)
        else:
            raise NotImplementedError(
                "%s implementation is not currently supported "
                "by priority queue.")

    @classmethod
    def methods(cls):
        return ['__new__']

    def push(self, value, priority):
        """
        Pushes the value to the priority queue
        according to the given priority.

        value
            Value to be pushed.
        priority
            Priority to be given to the value.
        """
        raise NotImplementedError(
                "This is an abstract method.")

    def pop(self):
        """
        Pops out the value from the priority queue.
        """
        raise NotImplementedError(
            "This is an abstract method.")

    @property
    def peek(self):
        """
        Returns the pointer to the value which will be
        popped out by `pop` method.
        """
        raise NotImplementedError(
            "This is an abstract method.")

    @property
    def is_empty(self):
        """
        Checks if the priority queue is empty.
        """
        raise NotImplementedError(
            "This is an abstract method.")

class BinaryHeapPriorityQueue(PriorityQueue):

    __slots__ = ['items']

    @classmethod
    def methods(cls):
        return ['__new__', 'push', 'pop', 'peek', 'is_empty']

    def __new__(cls, comp):
        obj = object.__new__(cls)
        obj.items = BinaryHeap()
        obj.items._comp = comp
        return obj

    def push(self, value, priority):
        self.items.insert(priority, value)

    def pop(self):
        node = self.items.extract()
        return node.data

    @property
    def peek(self):
        if self.items.is_empty:
            raise IndexError("Priority queue is empty.")
        return self.items.heap[0]

    @property
    def is_empty(self):
        return self.items.is_empty
