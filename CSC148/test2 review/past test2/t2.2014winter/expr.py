def is_plex(s: str) -> bool:
  '''Return True iff s is a plex according to the above rules.
  
  >>> is_plex('++(1+1)')
  True
  >>> is_plex('++1')
  True
  >>> is_plex('+(1+1+2)')
  False
  >>> is_plex('(((1+1)+0)+0)')
  True
  >>> is_plex('(+1+1)')
  True
  '''
  if len(s) == 0:
    return False
  if len(s) == 1 and s in '01':
    return True
  if s[0] == '+':
    return is_plex(s[1:])
  if s[0] == '(' and s[-1] == ')':
    smaller = s[1:-1]
    for i in range(len(smaller)):
      if smaller[i] == '+' and is_plex(smaller[:i]) and is_plex(smaller[i+1:]):
        return True
  return False
  
import doctest
doctest.testmod()
