"""Incomplete Binary Search Tree implementation.
Author: Francois Pitt, March 2013,
        Danny Heap, October 2013.
"""

class BST:
    """A Binary Search Tree."""

    def __init__(self: 'BST', container: list =[]) -> None:
        """
        Initialize this BST by inserting the values from container (default [])
        one by one, in the order given.
        """
        # Initialize empty tree.
        self.root = None
        # Insert every value from container.
        for value in container:
            self.insert(value)

    def __str__(self: 'BST'):
        """
        Return a "sideways" representation of the values in this BST, with
        right subtrees above nodes above left subtrees and each value preceded
        by a number of TAB characters equal to its depth.
        """
        # Tricky to do iteratively so we cheat,
        # You could take up the challenge...
        return BST._str("", self.root)

    # Recursive helper for __str__.
    def _str(indent: str, root: '_BSTNode') -> str:
        """
        Return a "sideways" representation of the values in the BST rooted at
        root, with right subtrees above nodes above left subtrees and each
        value preceded by a number of TAB characters equal to its depth, plus
        indent.
        """
        if root:
            return (BST._str(indent + "\t", root.right) +
                    indent + str(root.value) + "\n" +
                    BST._str(indent + "\t", root.left))
        else:
            return ""

    def insert(self: 'BST', value: object) -> None:
        """
        Insert value into this BST.
        """
        # Find the point of insertion.
        parent, current = None, self.root
        while current:
            if value < current.value:
                parent, current = current, current.left
            else:  # value > current.value
                parent, current = current, current.right
        # Create a new node and link it in appropriately.
        new_node = _BSTNode(value)
        if parent:
            if value < parent.value:
                parent.left = new_node
            else:  # value > parent.value
                parent.right = new_node
        else:
            self.root = new_node

    def count_less(self: 'BST', value: object) -> int:
        """
        Return the number of values in this BST that are strictly less than
        value.
        """
        # ridiculous stub value --- fix this!
        return -42


    def size(self: 'BST') -> int:
        """Return number of nodes in BST self"""
        stack = Stack()
        count = 0
        stack.push(self.root)
        while not stack.is_empty():
            node = stack.pop()
            if node: # only count non-empty nodes
                count += 1
                stack.push(node.left)
                stack.push(node.right)
        return count


class _BSTNode:
    """A node in a BST."""

    def __init__(self: '_BSTNode', value: object, 
                 left: '_BSTNode' =None, right: '_BSTNode' =None) -> None:
        """
        Initialize this node to store value and have children left and right.
        """
        self.value, self.left, self.right = value, left, right



'''Stack ADT.

Operations:
	pop: remove and return top item
        push(item): store item on top of stack
        is_empty: return whether stack is empty.
'''

class Stack:

    '''A last-in, first-out (LIFO) stack of items'''

    def __init__(self):
        '''A new empty Stack.'''

        self._data = []
        
    def pop(self):
        '''Remove and return the top item.'''

        return self._data.pop()
        
    def is_empty(self):
        '''Return whether the stack is empty.'''

        return self._data == []
    
    def push(self, o):
        '''Place o on top of the stack.'''

        self._data.append(o)
