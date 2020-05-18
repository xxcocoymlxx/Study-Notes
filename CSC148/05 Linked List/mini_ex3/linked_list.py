class Node:
    """A node in a linked list.

    === Attributes ===
    item: object
        The data stored in this node.
    next: Node or None
        The next node in the list, or None if there are
        no more nodes in the list.
    """
    def __init__(self: 'Node', item: object, next_node: 'Node'=None) -> None:
        """Create Node self with data value and successor next.
        """

        self.item = item
        self.next = next_node # By default, this would be None

    def __repr__(self: 'Node') -> str:
        """Return a detailed str representation of Node.
        """
        if not self.next:
            return 'Node({})'.format(repr(self.item))
        else:
            return 'Node({}, {})'.format(repr(self.item), repr(self.next)) # This is recursive; take a few moments to think about how this works

class LinkedList:
    """A linked list implementation of the List ADT.

    === Private Attributes ===
    _first: Node or None
        The first node in the list, or None if the list is empty.
    """
    def __init__(self: 'LinkedList', items: list) -> None:
        """Initialize a new linked list containing the given items.

        The first node in the linked list contains the first item
        in <items>.
        """
        if len(items) == 0:  # No items, and an empty list!
            self._first = None
        else:
            self._first = Node(items[0])
            current_node = self._first
            for item in items[1:]:
                current_node.next = Node(item)
                current_node = current_node.next

    # ------------------------------------------------------------------------
    # Non-mutating methods: these methods do not change the list
    # ------------------------------------------------------------------------
    def is_empty(self: 'LinkedList') -> bool:
        """Return whether this linked list is empty.
        """
        return self._first is None

    def __str__(self: 'LinkedList'):
        """Return a string representation of this list in the form
        '[item1 -> item2 -> ... -> item-n]'.

        >>> lst = LinkedList([1, 2, 3])
        >>> str(lst)
        '[1 -> 2 -> 3]'
        """
        items = []
        curr = self._first
        while curr is not None:
            items.append(str(curr.item))
            curr = curr.next
        return '[' + ' -> '.join(items) + ']'

    def __repr__(self: 'LinkedList') -> str:
        """Return a detailed str representation of LinkedList in the form
        LinkedList(Node(value, Node(value, ...)))

        >>> lst = LinkedList([1, 2, 3])
        >>> repr(lst)
        'LinkedList(Node(1, Node(2, Node(3))))'
        """
        if self._first is None:
          return 'LinkedList()'
        else:
          return 'LinkedList(' + repr(self._first) + ')'
       
    def __getitem__(self: 'LinkedList', index: int) -> object:
        """Return the item at position <index> in this list.
        Raise IndexError if <index> is >= the length of this list.
        """
        
        curr = self._first
        curr_index = 0

        # Iterate to (index)-th node
        while curr is not None and curr_index < index:
            curr = curr.next
            curr_index += 1

        if curr is None:
            raise IndexError
        else:
            return curr.item

    def append(self, data):
        '''Add the given data into the linked list.'''
        if self._first == None:
            self._first = Node(data)
            return

        curr = self._first
        while curr.next != None:
            curr = curr.next

        curr.next = Node(data)
            
    def pop(self, index):
        '''Remove the item with given index.'''
        if self._first == None:
            raise IndexError("LinkedList index out of range")

        if index == 0:
            old = self._first
            self._first = old.next
            old.next = None
            return old.item

        parent = self._first#没进去上面那个if说明要找的就不是第一个elm
        curr = self._first.next
        curr_index = 1#index直接设为第二个elm的
        while curr != None:
            if curr_index == index:
                parent.next = curr.next#断开连接,parent是前一个,curr是后一个
                curr.next = None
                return curr.item

            parent = curr
            curr = curr.next
            curr_index += 1

        raise IndexError("LinkedList index out of range")

    
class EmptyQueueError(Exception):

    """An exception raised when attempting to dequeue from an empty queue.
    """

    pass



class Queue():#first in first out
    def __init__(self,items=[]):
        self.items = LinkedList(items)

    def enqueue(self, data):
        self.items.append(data)

    def dequeue(self):
        if self.is_empty():
            raise EmptyQueueError()
        
        return self.items.pop(0)

    def is_empty(self):
        return self.items.is_empty()

    def front(self):
        if self.is_empty():
            raise EmptyQueueError()

        return self.items._first.item



        
    
