class BTNode:
  '''A node in a binary tree.'''

  def __init__(self: 'BTNode', item: object, 
               left: 'BTNode'=None, right: 'BTNode'=None) -> None:
    '''Initialize this node.'''
    self.item, self.left, self.right = item, left, right
