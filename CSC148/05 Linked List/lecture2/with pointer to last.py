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
            return 'Node({}, {})'.format(repr(self.item), repr(self.next)) 
            # This is recursive; take a few moments to think about how this works

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
            self._last = None # By adding this, we can make appending much faster!
        else:
            self._first = Node(items[0])
            current_node = self._first
            for item in items[1:]:
                current_node.next = Node(item)
                current_node = current_node.next
            self._last = current_node #set self.last为items里的最后一个elm，实时记录self.last是谁

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
        curr_index = 0 #设置一个initial index去虚拟一个linked_list其实没有的index属性

        # Iterate to (index)-th node
        while curr is not None and curr_index < index:
            curr = curr.next
            curr_index += 1

        if curr is None:
            raise IndexError
        else:
            return curr.item


    # ------------------------------------------------------------------------
    # Mutating methods: these methods do change the list
    # ------------------------------------------------------------------------

    def append(self: 'LinkedList', item: object) -> None:
        """Append Node with <item> to the end of this list.
        """

        #new_node = Node(item)
#        curr = self._first
#        if curr is None:
#            self._first = new_node
#        else:
#            while curr.next is not None:
#                curr = curr.next # THIS DOES NOT CHANGE THE LIST
#            curr.next = new_node  # THIS CHANGES THE LIST

        # WE USE SELF._LAST TO UPDATE THIS METHOD:
        #就不用每次要append new node进来都得loop一遍找到linked list里最后一个item
        #现在我们已经用新的一个attribute‘self._last’记录了linked list里的最后一个item就可以直接添加了
        new_node = Node(item)
        if self.is_empty():
            self._first = self._last = new_node #可以连等
        else:         
            self._last.next = new_node
            self._last = self._last.next            
    
    def prepend(self: 'LinkedList', item: object) -> None:
        """Prepend Node with <item> to the beginning of this list.
        """

        # WE UPDATE THIS TO TAKE SELF._LAST INTO CONSIDERATION TOO
        new_node = Node(item)
        if self.is_empty():
            self._first = self._last = new_node
        else:
            new_node.next = self._first
            self._first = new_node
        
