from node import Node

class LinkedList:

  """Collection of Nodes to form a linked list"""
  
  def __init__(self: 'LinkedList') -> None:
    """Create empty LinkedList"""
    self.front, self.back, self.size = None, None, 0
    
  def __repr__(self: 'LinkedList') -> str:
    """Return str representation of LinkedList"""
    if self.front is None:
      return 'LinkedList()'
    else:
      return repr(self.front)
      
  def repeat_items(self: 'LinkedList') -> None:
    """Repeat each item in LinkedList self."""
    self.size = self.size * 2
    current = self.front
    while current:
      new_node = Node(current.value, current.next)
      current.next = new_node
      current = current.next.next
    self.back = self.back.next
    

a = LinkedList()
a.front = Node(1)
a.front.next = Node(0)
a.front.next.next = Node(9)
nine = Node(9)
a.front.next.next.next = nine
a.back = nine
a.size = 4
a.repeat_items()
print(a)
