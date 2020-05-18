# This question ended up being a bit too tricky in light of the test 1 grades
# I accepted the 'helper' code as a correct solution
# even though it does not always place chr correctly.
# But as a student has asked for the full deal, here it is
# The full solution removes chr, permutes the string,
# then puts chr in the proper place

def divide(s: str, chr: str) -> str:
  '''
  Precondition: chr is a character that appears in string s. 
  Precondition: Every character in s is unique and lowercase.
     
  Return a new string where all characters that are alphabetically less
  than chr come first, then chr, then all characters alphabetically
  greater than chr.
  
  >>> divide('jkldcf', 'f')
  'dcflkj'
  >>> divide('xyzdabc', 'd')
  'abcdzyx'
  >>> divide('abde', 'b')
  'abed'
    '''
  index = s.find(chr)
  s = s[:index] + s[index+1:]
  s = helper(s, chr)
  i = 0
  while i < len(s) and s[i] < chr:
    i = i + 1
  return s[:i] + chr + s[i:]
  
def helper(s, chr):
  if s == '':
    return s
  if s[0] < chr:
    return s[0] + helper(s[1:], chr)
  else:
    return helper (s[1:], chr) + s[0]
  
import doctest
doctest.testmod()
