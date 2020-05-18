def duplicates(s: str) -> bool:
  '''
  Return True iff string s contains at least two adjacent characters that are the same.
     
  >>> duplicates('abab')
  False
  >>> duplicates('bbaa')
  True
  >>> duplicates('bba')
  True
  '''

  if len(s) < 2:
    return False

  if s[0] == s[1]:
    return True
  else:
    return duplicates(s[1:])
