"""Run some timing experiments on class Queue operations.

Authors: Francois Pitt, January 2013,
        Danny Heap, September 2013, February 2014
"""
#from csc148queue import Queue
from linked_list import Queue
import time


def enqueue_dequeue(q: Queue, howmany: int):

    """Enqueue and dequeue 'howmany' items to/from Queue 'q'.
    """

    for i in range(howmany):
        q.enqueue(42)
        q.dequeue()


def time_queue(m: int, n: int):

    """Return how long it takes to enqueue and dequeue 'm' items to/from a
    Queue with 'n' items already in it.
    """

    q = Queue()
    for i in range(n):
        q.enqueue(1)

    start = time.time()
    enqueue_dequeue(q, m)
    end = time.time()

    return end - start

if __name__ == '__main__':
    for n in [i * 10000 for i in range(1, 11)]:
        print('Inserting and removing 20000 items with', n, 'items already '
              'in queue:', time_queue(20000, n))
