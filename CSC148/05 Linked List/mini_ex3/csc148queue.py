"""A simple implementation of the Queue ADT.

Authors: Francois Pitt, January 2013,
Danny Heap, September 2013
"""


class EmptyQueueError(Exception):

    """An exception raised when attempting to dequeue from an empty queue.
    """

    pass


class Queue:

    """A collection of items stored in 'first-in, first-out' (FIFO) order.
    Items can have any type.

    Supports standard operations: enqueue, dequeue, front, is_empty.
    """

    def __init__(self: 'Queue') -> None:
        """
        Initialize this queue.

        >>> q = Queue()
        >>> isinstance(q, Queue)
        True
        """

        self._items = []

    def enqueue(self: 'Queue', item: object) -> None:
        """
        Add item to the back of this queue.

        item - object to put in queue

        >>> q = Queue()
        >>> q.enqueue(5)
        >>> q.enqueue(6)
        >>> q.dequeue()
        5
        """

        self._items.append(item)

    def dequeue(self: 'Queue') -> None:
        """
        Remove and return the front item in this queue.

        >>> q = Queue()
        >>> q.enqueue(5)
        >>> q.enqueue(6)
        >>> q.dequeue()
        5
        """

        if self.is_empty():
            raise EmptyQueueError()
        return self._items.pop(0)

    def front(self: 'Queue') -> object:
        """
        Return the front item in this queue without removing it.

        >>> q = Queue()
        >>> q.enqueue(5)
        >>> q.enqueue(6)
        >>> q.front()
        5
        >>> q.dequeue()
        5
        """

        if self.is_empty():
            raise EmptyQueueError()
        return self._items[0]

    def is_empty(self: 'Queue'):
        """
        Return True iff this queue is empty.

        >>> Queue().is_empty()
        True
        """

        return self._items == []

