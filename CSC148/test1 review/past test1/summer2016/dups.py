from stack import Stack

def remove_dups(s: Stack) -> None:
  '''Modify s so that consecutive duplicates are removed.
    
  >>> s = Stack()
  >>> s.push(1)
  >>> s.push(2)
  >>> s.push(2)
  >>> remove_dups(s)
  >>> s.pop()
  2
  >>> s.pop()
  1
  >>> s = Stack()
  >>> s.push(1)
  >>> s.push(2)
  >>> remove_dups(s)
  >>> s.pop()
  2
  >>> s.pop()
  1
    '''
  t = Stack()
  while not s.is_empty():
    element = s.pop()
    t.push(element)
    done = False
    while not s.is_empty() and not done:
      element2 = s.pop()
      if element2 != element:
        done = True
        s.push(element2)
  while not t.is_empty():
    s.push(t.pop())
    
        
import doctest
doctest.testmod()
