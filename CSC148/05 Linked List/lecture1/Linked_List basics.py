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
        self.next = next_node #By default, this would be None

    def __repr__(self: 'Node') -> str:
        """Return a detailed str representation of Node.
        Node(value, Node(value, ...))
        This method is used when printing Linked_list.
        
        >>> lst = LinkedList([1, 2, 3])
        >>> repr(lst)
        'Node(1, Node(2, Node(3)))'
        """
        if not self.next:#if self.next is None
            return 'Node({})'.format(repr(self.item))#return self.item
        else:
            return 'Node({}, {})'.format(repr(self.item), repr(self.next))
        # This is recursive; take a few moments to think about how this works
        #return 'Node({}, {})'.format(self.item, repr(剩下所有node.item))

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
            self._first = None # base case
        else:
            self._first = Node(items[0])
            current_node = self._first
            for item in items[1:]:
                current_node.next = Node(item)
                current_node = current_node.next

        #format:
        #current_node = self.first
        #do something with current_node
        #current_node = cerrent_node.next

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
            items.append(str(curr.item))#这里只是string化item这个object
            curr = curr.next
        return '[' + ' -> '.join(items) + ']'
    #join method can be used for strings or list with str objects
    #用‘->’把string/list里每个item连接起来
    

    def __repr__(self: 'LinkedList') -> str:
        """Return a detailed str representation of LinkedList in the form
        LinkedList(Node(value, Node(value, ...)))

        >>> lst = LinkedList([1, 2, 3])
        >>> repr(lst)
        'LinkedList(Node(1, Node(2, Node(3))))'
        
        note: class Node also has a method called __repr__
        """
        if self._first is None:
          return 'LinkedList()'# base case
        else:
          return 'LinkedList(' + repr(self._first) + ')'
        #self.first是个Node，这里call的repr是class Node的method
        #给了他一个node他会自己完成print剩下所有self.next的node的
       
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

        #从上面那个loop里出来就只有两种可能
        if curr is None:#curr已经是None了但curr_index还小于index，<index> is >= the length of this list
            raise IndexError
        else:#curr_index = index
            return curr.item
