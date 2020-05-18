from stack import Stack, EmptyStackError

# solution 1
def is_balanced2(s):
  '''(str) -> bool
  Return True iff s consists of balanced brackets. Accept round,
  square, and curly brackets.

  >>> is_balanced2('[a * (3 + b)]')
  True

  >>> is_balanced2('[a * (3 + b]]')
  False

  >>> is_balanced2('3 â€“ [x')
  False
  '''

  open_brackets = "{[("
  close_brackets = "}])"
  st = Stack()

  for char in s:
    if char in open_brackets:
      st.push(char)
    elif char in close_brackets:
      try:
        last_opened = st.pop()
        if (open_brackets.find(last_opened) != close_brackets.find(char)):
          return False
      except EmptyStackError:
        return False

  return st.is_empty()


# solution 2, using a helper function
def is_matching(b1, b2):
    '''
    Given a pair of brackets, return True iff they are a matching pair.
    '''
    return (b1 == '(' and b2 == ')') or (b1 == '{' and b2 == '}') or \
           (b1 == '[' and b2 == ']')

def is_balanced3(s):
  '''(str) -> bool
  Return True iff s consists of balanced brackets. Accept round,
  square, and curly brackets.
  '''

  st = Stack()

  for char in s:
    if char in '([{':
      st.push(char)
    elif char in ')]}':
      try:
        last_opened = st.pop()
        if not is_matching(last_opened, char):
          return False
      except EmptyStackError:
        return False

  return st.is_empty()

# if you have some other solution that works,
#feel free to share on discussion board :)
