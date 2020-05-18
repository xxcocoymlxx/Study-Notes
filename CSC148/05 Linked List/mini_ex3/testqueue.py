"""Test module Queue.

Authors: Francois Pitt, January 2013,
         Danny Heap, September 2013, February 2014
"""
import unittest
from linked_list import Queue


class EmptyTestCase(unittest.TestCase):

    """Test behaviour of an empty Queue.
    """

    def setUp(self):
        """Set up an empty queue.
        """

        self.queue = Queue()

    def tearDown(self):
        """Clean up.
        """

        self.queue = None

    def testIsEmpty(self):
        """Test is_empty() on empty Queue.
        """
        self.assertTrue(
            self.queue.is_empty(),
            'is_empty returned False on an empty Queue!')

class SingletonTestCase(unittest.TestCase):

    """Check whether enqueueing a single item makes it appear at the front.
    """

    def setUp(self):
        """Set up a queue with a single element.
        """

        self.queue = Queue()
        self.queue.enqueue('a')

    def tearDown(self):
        """Clean up.
        """

        self.queue = None

    def testIsEmpty(self):
        """Test is_empty() on non-empty Queue.
        """

        self.assertFalse(
            self.queue.is_empty(),
            'is_empty returned True on non-empty Queue!')

    def testFront(self):
        """Test front() on a non-empty Queue.
        """

        front = self.queue.front()
        self.assertEqual(
            front, 'a',
            'The item at the front should have been "a" but was ' +
            front + '.')

    def testDequeue(self):
        """Test dequeue() on a non-empty Queue.
        """

        front = self.queue.dequeue()
        self.assertEqual(
            front, 'a',
            'The item at the front should have been "a" but was ' +
            front + '.')
        self.assertTrue(
            self.queue.is_empty(),
            'Queue with one element not empty after dequeue().')


class TypicalTestCase(unittest.TestCase):

    """A comprehensive tester of typical behaviour of Queue.
    """

    def setUp(self):
        """Set up an empty queue.
        """

        self.queue = Queue()

    def tearDown(self):
        """Clean up.
        """

        self.queue = None

    def testAll(self):
        """Check enqueueing and dequeueing several items.
        """

        for item in range(20):
            self.queue.enqueue(item)
            self.assertFalse(
                self.queue.is_empty(),
                'Queue should not be empty after adding item ' +
                str(item))
        item = 0
        while not self.queue.is_empty():
            front = self.queue.dequeue()
            self.assertEqual(
                front, item,
                'Wrong item at the front of the Queue. Found ' +
                str(front) + ' but expected ' + str(item))
            item += 1


class MutableTestCase(unittest.TestCase):

    """Test adding a mutable object. Make sure the Queue adds the object,
    and does not make a copy.
    """

    def setUp(self):
        """Set up an empty queue.
        """

        self.queue = Queue()

    def tearDown(self):
        """Clean up.
        """

        self.queue = None

    def testMutable(self):
        """Test with a list.
        """

        item = [1, 2, 3]
        self.queue.enqueue(item)
        item.append(42)
        self.assertEqual(self.queue.front(), item,
                         'mutable item did not change!')
        self.assertEqual(self.queue.dequeue(), item,
                         'mutable item did not change!')

if __name__ == '__main__':
    unittest.main(exit=False)
