def max_depth(lst):
  '''(list, possibly with nesting) -> int
  
  Return the maximum depth of any element in lst.
  lst may be nested arbitrarily.
  
  >>> max_depth([10, 20, [30, [[40]]]])
  4
  >>> max_depth([])
  0
  >>> max_depth([[], 10])
  1

  '''
  maximum = 0
  for element in lst:
    if isinstance(element, int):
      maximum = max(maximum, 1)
    else:
      inside = max_depth(element)
      if inside > 0:
        maximum = max(maximum, inside + 1)
  return maximum
  
import doctest
doctest.testmod()
