# Here is the binary tree node class that we will use
# Note that the constructor allows us to set the item
# at the node and also its left and right subtrees

class BTNode:
  """A node in a binary tree."""

  def __init__(self: 'BTNode', item: object, 
               left: 'BTNode' =None, right: 'BTNode' =None) -> None:
    """Initialize this node.
    """
    self.item, self.left, self.right = item, left, right

  def __repr__(self):
    return 'BTNode({}, {}, {})'.format(self.item, str(self.left), str(self.right))

#outside the class
def tree_sum(t: BTNode): 
  '''Return the sum of the leaves in t.
  
  >>> t = BTNode(None, BTNode(8), BTNode(9))
  >>> tree_sum(t)
  17
  '''


def tree_height(t: BTNode) -> int:
  '''Return the height of t
  
  >>> tree_height(BTNode(None, BTNode(None, BTNode(4)), BTNode(9)))
  2
  '''


def tree_paths(t: BTNode) -> int:
  '''Return number of paths to get from root of t,
  to all houses, and back to t.
  
  >>> tree_paths(BTNode(None, BTNode(4), BTNode(5)))
  4
  '''


def solve(t: BTNode) -> (int, int):
  '''Return the solution to the tree as a tuple of (paths, candy)
  
  >>> solve(BTNode(None, BTNode(5), BTNode(6)))
  (3, 11)
    '''
  

def read_bt(s: str) -> BTNode:
  '''s is a line that represents a binary tree.
  Return the BTNode corresponding to that string.
  
  >>> read_bt('(3 4)')
  BTNode(None, BTNode(3, None, None), BTNode(4, None, None))
  '''


def process(f) -> None:
  '''
  Solve the problem for all lines in file f.
  '''



if __name__ == '__main__':
  import doctest
  doctest.testmod()
  process(open('candy.txt'))
  
