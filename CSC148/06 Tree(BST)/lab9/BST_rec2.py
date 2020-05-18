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
        self.root = None
        # Insert every item from container.
        for item in container:
            self.insert(item)

    def __str__(self):
        """(BST) -> str
        Return a "sideways" representation of the values in this BST, with
        right subtrees above nodes above left subtrees and each value preceded
        by a number of TAB characters equal to its depth.
        """
        if self.root:
            return self.root._str("")#calling the node's method
        else:
            return ""

    def insert(self, item):
        """(BST, object) -> NoneType
        Insert item into this BST.
        """
        if self.root:
            self.root.insert(item)
        else:
            self.root = _BSTNode(item)

    def count_less(self, item):
        """(BST, object) -> int
        Return the number of items in this BST that are strictly less than
        item.
        """
        if self.root:
            return self.root.count_less(item)

        return 0

    def size(self: 'BST') -> int:
        """Return number of nodes in BST self"""
        return self.root.size() if self.root else 0


class _BSTNode:
    """A node in a BST."""

    def __init__(self, item, left=None, right=None):
        """(_BSTNode, object, _BSTNode, _BSTNode) -> NoneType
        Initialize this node to store item and have children left and right.
        """
        self.item = item
        self.left = left
        self.right = right

    def _str(self, indent):
        """(_BSTNode, str) -> str
        Return a "sideways" representation of the values in the BST rooted at
        this node, with right subtrees above nodes above left subtrees and each
        value preceded by a number of TAB characters equal to its depth, plus
        indent.
        """
        if self.right:
            right_str = self.right._str(indent + "\t")
        else:
            right_str = ""
        if self.left:
            left_str = self.left._str(indent + "\t")
        else:
            left_str = ""
        return right_str + indent + str(self.item) + "\n" + left_str

    def insert(self, item):
        """(_BSTNode, object) -> NoneType
        Insert item into the BST rooted at this node.
        """
        if item < self.item:
            if self.left:
                self.left.insert(item)
            else:
                self.left = _BSTNode(item)
        elif item > self.item:
            if self.right:
                self.right.insert(item)
            else:
                self.right = _BSTNode(item)

    def count_less(self: '_BSTNode', item: object) -> int:
        """
        Return the number of items in the BST rooted at this node that are
        strictly less than item.
        我们是在node里面写的，必须要判断为不为空
        """
        if self.item < item:
            if self.right:
                right = self.right.count_less(item)
            else:
                right = 0
            return self.left.size() + 1 + right
        else:
            if self.left:
                left = self.left.count_less(item)
            else:
                left = 0
            return left


    def size(self):
        """(_BSTNode) -> int
        Return the number of nodes in the BST rooted at this node.
        """
        return (1 + 
                (self.left.size() if self.left else 0) +
                (self.right.size() if self.right else 0))

