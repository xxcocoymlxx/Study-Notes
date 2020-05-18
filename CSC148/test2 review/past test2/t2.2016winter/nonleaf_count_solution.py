class Tree:
  """Tree ADT; nodes may have any number of children"""

  def __init__(self: 'Tree',
               value: object =None, children: list =None):
    """Create node with value and any number of children"""

    self.value = value
    if not children:
        self.children = []
    else:
        self.children = children[:]

def nonleaf_count(t):
  """Return number of internal nodes in t

  >>> tn2 = Tree(2, [Tree(4), Tree(4.5)])
  >>> tn3 = Tree(3, [Tree(6)])
  >>> tn1 = Tree(1, [tn2, tn3])
  >>> nonleaf_count(tn1)
  3
  """

  if t.children == []:
    return 0

  total = 1
  for child in t.children:
    total = total + nonleaf_count(child)
  return total

# Dan: or this?

def nonleaf_count(t):
  """Return number of internal nodes in t

  >>> tn2 = Tree(2, [Tree(4), Tree(4.5)])
  >>> tn3 = Tree(3, [Tree(6)])
  >>> tn1 = Tree(1, [tn2, tn3])
  >>> nonleaf_count(tn1)
  3
  """

  if t.children == []:
    return 0

  return 1 + nonleaf_count(t.children[0]) + nonleaf_count(Tree(t.value, t.children[1:])) - len(t.children) + 1


import doctest
doctest.testmod()
