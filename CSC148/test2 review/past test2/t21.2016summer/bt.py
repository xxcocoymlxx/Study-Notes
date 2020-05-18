class BTNode:
  """A node in a binary tree."""

  def __init__(self: 'BTNode', item: object, 
               left: 'BTNode' =None, right: 'BTNode' =None) -> None:
    """Initialize this node.
    """
    self.item, self.left, self.right = item, left, right

def longest_path(t: BTNode) -> list:
  """Return a Python list containing the values in a longest path of t.
  If there are multiple longest paths, return a list of one of them.
  
  >>> b1 = BTNode(7)
  >>> b2 = BTNode(3, BTNode(2), None)
  >>> b3 = BTNode(5, b2, b1)
  >>> longest_path(b3)
  [5, 3, 2]
  """
  if not t:
    return []
  left_longest = longest_path(t.left)
  right_longest = longest_path(t.right)
  if len(left_longest) > len(right_longest):
    return [t.item] + left_longest
  else:
    return [t.item] + right_longest
    
import doctest
doctest.testmod()

    