from node import *

def preorder(t):
  if t:
    return [t.item] + preorder(t.left) + preorder(t.right)
  else:
    return []
    

def remove_leaves(t: 'BTNode') -> 'BTNode':
  '''Remove the leaves of t.
  Do not remove any node that was not originally a leaf in t.
  Return the root of the tree 
  (which could be None if the tree is now empty).
  >>> left = BTNode('B', None, BTNode('D', BTNode('G')))
  >>> right = BTNode('C', BTNode('E'), BTNode('F'))
  >>> root = BTNode('A', left, right)
  >>> root2 = remove_leaves(root)
  >>> root2 == root
  True
  >>> preorder(root2)
  ['A', 'B', 'D', 'C']
  >>> remove_leaves(None)
  '''
  if not t or (not t.left and not t.right):
    return None # no nodes, or root is leaf
  if t.left:
    if not t.left.left and not t.left.right: # t.left is a leaf
      t.left = None
  if t.right:
    if not t.right.left and not t.right.right: # t.right is a leaf
      t.right = None
  remove_leaves(t.left)
  remove_leaves(t.right)
  return t
  
import doctest
doctest.testmod()
