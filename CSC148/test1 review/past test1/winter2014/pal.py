def is_palindrome(s: str) -> bool:
  '''Return True iff s is a palindrome.
  '''
  if not s:
    return True
  if s[0] == s[-1]:
    return is_palindrome(s[1:-1])
  else:
    return False
        