#带壳的
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
            return 'Node({})'.format(repr(self.item))#这里的repr其实不需要，这就是base case
        else:
            return 'Node({}, {})'.format(repr(self.item), repr(self.next)) 
            # This is recursive; take a few moments to think about how this works
            #Node({当前的}, {余下的所有}会自己一层一层的叠代完)
            #这里的第一个repr其实也不需要,没有进行叠代，只有self.next需要叠代

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
            items.append(str(curr.item))#把curr.item string化
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
          return 'LinkedList(' + repr(self._first) + ')'#calling the Node method
          #给他第一个node就会把剩下的按照Node(1, Node(2, Node(3)))呈现出来

       
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

    # ------------------------------------------------------------------------
    # Mutating methods: these methods do change the list
    # ------------------------------------------------------------------------
    def append(self: 'LinkedList', item: object) -> None:
        """Append Node with <item> to the end of this list.
        """
        # The runtime of this method is LINEAR or O(n) because
        # the number of times the loop iterates is equal to
        # the number of items in the list. So, as the list grows,
        # the steps this method takes also grows at linear pace.
        
        new_node = Node(item)
        
        curr = self._first
        # what do we have access to?
        ## to get first node: self._first
        ## each node has: .item, .next (last node in list has .next=None)

        if curr is None:
            self._first = new_node
        else:
            while curr.next is not None:
                curr = curr.next # this is not changing the list
                #这里loop完了以后curr就是最后一个node
            curr.next = new_node # this changes the list
        
    def prepend(self: 'LinkedList', item: object) -> None:
        """Prepend Node with <item> to the beginning of this list.
        """
        # The runtime of this method is CONSTANT or O(1) because
        # no matter how big my list gets, the number of steps this method
        # takes will stay the same. So, prepending is faster than appending
        # for this implementation of the linked list.
        # See linked_list_v2.py for an implementation where appending is also
        # constant time.

        new_node = Node(item)

        # first attempt:
        # self._first = new_node
        # this is WRONG. it will DELETE ALL THE ORIGINAL LIST ITEMS.
        
        new_node.next = self._first
        self._first = new_node
    
        # alternative to all of the above:
        # self._first = Node(item, self._first)





