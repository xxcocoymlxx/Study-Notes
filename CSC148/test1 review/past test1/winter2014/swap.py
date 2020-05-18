from stack import Stack

class StackException(Exception):
  pass

def swap_top(s: Stack) -> None:
  '''Swap the top two elements of s.
  If there are fewer than two items on the stack, 
  the stack is unchanged and a StackException is raised.
  
  >>> s = Stack()
  >>> s.push(1)
  >>> s.push(2)
  >>> swap_top(s)
  >>> s.pop()
  1
  '''
  if s.is_empty():
    raise StackException
  first = s.pop()
  if s.is_empty():
    s.push(first)
    raise StackException
  second = s.pop()
  s.push(first)
  s.push(second)
  