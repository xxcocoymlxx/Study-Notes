from stack import Stack


def swap_bottom(s: Stack) -> None:
  '''Precondition: s has at least two elements.
  
  Swap the bottom two elements of Stack s.
  
  >>> s = Stack()
  >>> s.push(1)
  >>> s.push(2)
  >>> s.push(3)
  >>> swap_bottom(s)
  >>> s.pop()
  3
  >>> s.pop()
  1
  '''
  t = Stack()
  while not s.is_empty():
    t.push(s.pop())
  bottom = t.pop()
  second_bottom = t.pop()
  s.push(second_bottom)
  s.push(bottom)
  while not t.is_empty():
    s.push(t.pop())
