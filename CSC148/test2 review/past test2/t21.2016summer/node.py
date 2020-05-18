class Node:

  """Node in a linked list"""
  
  def __init__(self: 'Node', value: object, next: 'Node'=None) -> None:
    """Create Node self with data value and successor next."""
    self.value, self.next = value, next
    
  def __repr__(self: 'Node') -> str:
    """Return str representation of Node"""
    if not self.next:
      return 'Node({})'.format(repr(self.value))
    else:
      return 'Node({}, {})'.format(
        repr(self.value), repr(self.next))


