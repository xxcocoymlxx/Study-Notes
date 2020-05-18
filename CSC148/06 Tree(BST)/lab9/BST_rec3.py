"""Incomplete Binary Search Tree implementation.
Author: Francois Pitt, March 2013.
        Danny Heap, March 2014
"""

class BST:
    """A Binary Search Tree."""

    def __init__(self, container=[]):
        """(BST, list) -> NoneType
        Initialize this BST by inserting the items from container (default [])
        one by one, in the order given.
        """
        # Initialize empty tree.
        self.root = _BSTNone()
        # Insert every item from container.
        for item in container:
            self.insert(item)

    def __str__(self):
        """(BST) -> str
        Return a "sideways" representation of the values in this BST, with
        right subtrees above nodes above left subtrees and each value preceded
        by a number of TAB characters equal to its depth.
        """
        return self.root._str("")

    def insert(self, item):
        """(BST, object) -> NoneType
        Insert item into this BST.
        """
        self.root = self.root.insert(item)

    def count_less(self, item):
        """(BST, object) -> int
        Return the number of items in this BST that are strictly less than
        item.
        """
        return self.root.count_less(item)

    def size(self: 'BST') -> int:
        """Return number of nodes in BST self"""
        return self.root.size() if self.root else 0


class _BSTNode:
    """A node storing an item in a BST."""

    def __init__(self, item, left, right):
        """(_BSTNode, object, _BSTNode, _BSTNode) -> NoneType
        Initialize this node to store item and have children left and right.
        """
        self.item, self.left, self.right = item, left, right

    def _str(self, indent):
        """(_BSTNode, str) -> str
        Return a "sideways" representation of the values in the BST rooted at
        this node, with right subtrees above nodes above left subtrees and each
        value preceded by a number of TAB characters equal to its depth, plus
        indent.
        """
        return (self.right._str(indent + "\t") +
                indent + str(self.item) + "\n" +
                self.left._str(indent + "\t"))

    def insert(self, item):
        """(_BSTNode, object) -> _BSTNode
        Insert item into the BST rooted at this node and return the root of the
        resulting tree.
        """
        if item < self.item:
            self.left = self.left.insert(item)
        elif item > self.item:
            self.right = self.right.insert(item)
        return self

    def count_less(self: '_BSTNode', item: object) -> int:
        """
        Return the number of items in the BST rooted at this node that are
        strictly less than item.
        """
        # silly stub value --- fix this!
        return -42

    def size(self):
        """(_BSTNode) -> int
        Return the number of nodes in the BST rooted at this node.
        """
        return self.left.size() + 1 + self.right.size()


class _BSTNone(_BSTNode):
    """A node taking the place of None in a BST."""

    def __init__(self):
        """(_BSTNone) -> NoneType
        Initialize this node to store None and have no children.
        """
        super().__init__(None, self, self)

    def _str(self, indent):
        """(_BSTNone, str) -> str
        Return a "sideways" representation of the values in the BST rooted at
        this node, with right subtrees above nodes above left subtrees and each
        value preceded by a number of TAB characters equal to its depth, plus
        indent.
        """
        return ""

    def insert(self, item):
        """(_BSTNone, object) -> _BSTNode
        Insert item into the BST rooted at this node and return the root of the
        resulting tree.
        """
        return _BSTNode(item, self, self)

    def count_less(self, item):
        """(_BSTNone, object) -> int
        Return the number of items in the BST rooted at this node that are
        strictly less than item.
        """
        # ridiculous stub value --- fix this!
        return -42

    def size(self):
        """(_BSTNone) -> int
        Return the number of nodes in the BST rooted at this node.
        """
        return 0
