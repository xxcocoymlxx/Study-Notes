class Tree:
  '''Tree ADT; nodes may have any number of children'''

  def __init__(self: 'Tree', item: object =None, children: list =None):
    '''Create a node with item and any number of children'''

    self.item = item
    if not children:
      self.children = []
    else:
      self.children = children[:] 

  def __repr__(self: 'Tree') -> str:
    '''Return representation of Tree as a string'''

    if self.children:
      return 'Tree({0}, {1})'.format(repr(self.item), repr(self.children))
    else:
      return 'Tree({})'.format(repr(self.item))

  def remove_equal(self: 'Tree') -> None:
    '''Remove every child that has the same item as its parent;
    any children of a removed node n become children of an ancestor of n.

    >>> t = Tree(1, [Tree(2, [Tree(1), Tree(2)]), Tree(1)])
    >>> t.remove_equal()
    >>> repr(t)
    'Tree(1, [Tree(2, [Tree(1)])])'
    >>> t = Tree(4, [Tree(4, [Tree(6)])]) 
    >>> t.remove_equal()
    >>> repr(t)
    'Tree(4, [Tree(6)])'
    >>> t = Tree(4, [Tree(4, [Tree(4, [Tree(4)])])])
    >>> t.remove_equal()
    >>> repr(t)
    'Tree(4)'
    >>> t = Tree(4, [Tree(4, [Tree(4, [Tree(6), Tree(7)]), Tree(8)]), Tree(9)])
    >>> t.remove_equal()
    >>> repr(t)
    'Tree(4, [Tree(6), Tree(7), Tree(8), Tree(9)])'
    '''


if __name__ == '__main__':
  import doctest
  doctest.testmod()
  
