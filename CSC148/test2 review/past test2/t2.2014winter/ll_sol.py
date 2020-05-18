class LinkedList:
  '''Linked list class'''

  def __init__(self: 'LinkedList', head: object=None, 
               rest: 'LinkedList'=None) -> None:
    '''Create a new LinkedList.
    head - first element of linked list
    rest - linked list of remaining elements
    The empty linked list has head None
    '''
    # a linked list is empty if and only if it has no head
    self.empty = head is None
    if not self.empty:
      self.head = head
      if rest is None:
        self.rest = LinkedList()
      else:
        self.rest = rest

  def prepend(self: 'LinkedList', newhead: object) -> None:
    '''Add new head to front of LinkedList'''
    if not self.empty:
      temp = LinkedList(self.head, self.rest)
    else:
      temp = LinkedList()  
    self.head = newhead
    self.rest = temp
    self.empty = False

  def append(self: 'LinkedList', newlast: object) -> None:
    '''Add newlast to end of LinkedList'''
    ll = self
    while not ll.empty:
      ll = ll.rest
    ll.prepend(newlast)
