from stack import *


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
def read_bt(s): # nasty iterative version
  '''s is a line that represents a binary tree.
  Return the BTNode corresponding to that string.
  
  >>> read_bt('4')
  BTNode(4, None, None)
  >>> read_bt('(3 4)')
  BTNode(None, BTNode(3, None, None), BTNode(4, None, None))
  >>> read_bt('((1 2) (3 4))')
  BTNode(None, BTNode(None, BTNode(1, None, None), BTNode(2, None, None)), BTNode(None, BTNode(3, None, None), BTNode(4, None, None)))
  '''
  return read_bt_helper(s)[0]

def read_bt_helper(s):
  st = Stack()
  current = (s, None, None, 0) # string, left, right, stage
  while True:
    s, left, right, stage = current
    if stage == 0:
      s = s.strip()
      if s[0] == '(':
        st.push((s, left, right, 1))
        current = s[1:], left, right, 0
      else: # a digit
        assert s[0].isdigit(), 'digit expected'
        i = 0
        while i < len(s) and s[i].isdigit():
          i = i + 1
        temp1, temp2 = BTNode(int(s[:i])), s[i:]
        if not st.is_empty():
          current = st.pop()
        else:
          return temp1, temp2
    elif stage == 1:
      left, s = temp1, temp2
      s = s.strip()
      st.push((s, left, right, 2))
      current = s, left, right, 0
    elif stage == 2:
      right, s = temp1, temp2
      s = s.strip()
      assert s[0] == ')', 'expected )'
      temp1, temp2 = BTNode(None, left, right), s[1:]
      if not st.is_empty():
        current = st.pop()
      else:
        return temp1, temp2
      
  

if __name__ == '__main__':
  import doctest
  doctest.testmod()
