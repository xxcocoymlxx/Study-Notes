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
        if not self.next:#if not None, which means true (None represents False)
            return 'Node({})'.format(repr(self.item)) #base case
        else:
            return 'Node({}, {})'.format(repr(self.item), repr(self.next))
        # This is recursive; take a few moments to think about how this works

class LinkedList:
    """A linked list implementation of the List ADT.

    === Private Attributes ===
    _first: Node or None
        The first node in the list, or None if the list is empty.
    """
    def __init__(self: 'LinkedList', items: list) -> None: #directly turn a list into a linked list
        """Initialize a new linked list containing the given items.

        The first node in the linked list contains the first item
        in <items>.
        """
        if len(items) == 0:  # No items, and an empty list!
            self._first = None
        else:
            self._first = Node(items[0]) #creating a Node object here
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
            items.append(str(curr.item))#item is not a Node nor linked list, so it's the python built-in str
            curr = curr.next
        return '[' + ' -> '.join(items) + ']' #only for string or list with str objects

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
          return 'LinkedList(' + repr(self._first) + ')'#calling the Node Method
       
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
