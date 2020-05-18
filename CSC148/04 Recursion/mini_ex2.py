# EXAMPLE THAT WE DID IN CLASS
def remove_three(lst):
  '''(list of int) -> list of int
  
  Return a new list with all elements of lst except the 3s.
  lst has no nesting.
  
  >>> remove_three([1, 2, 3, 3, 4])
  [1, 2, 4]
  '''
  if L == []:
    return []
  elif L[0] == 3:
    return remove_three(L[1:])
  else:
    return [L[0]] + remove_three(L[1:])


# MINI-EXERCISE Q1: COMPLETE THE FOLLOWING USING RECURSION
def remove_three_nested(lst):
  '''(list of int) -> list of int
  
  Return a new list with all elements of lst except the 3s.
  lst may have nesting to arbitrary depth.
  
  >>> remove_three_nested([1, [2, 3], 3, 4])
  [1, [2], 4]
  '''
  
##  if lst == []:
##      return []
##  elif isinstance(lst[0], int):
##      if lst[0] == 3:
##            return remove_three_nested(lst[1:])
##      else: 
##            return [lst[0]] + remove_three_nested(lst[1:])
##  else: #if lst[0] is a nested list
##      return [remove_three_nested(lst[0])] + remove_three_nested(lst[1:])
##

  l = []
  for e in lst:
    if type(e) == int:
      if e != 3:
          l.append(e)
    else:
      l.append(remove_three_nested(e))
      
    return l
        

# MINI-EXERCISE Q2: COMPLETE THE DOCSTRING DESCRIPTION OF THE FOLLOWING
def mystery(lst, n):
  '''
  (list, int) -> bool

  # Describe here in PLAIN ENGLISH (not a line-by-line description)
  # what this function does
  Return ture iff lst[i] is less than n-i.
  >>>mystery([2, 2, 3, 4], 6)
  False
  >>>mystery([1, 1, 1], 3)
  True
  '''
  if lst == []:
    return True
  elif lst[0] > n:
    return False
  else:
    return mystery(lst[1:], n-1)
