from stack import Stack
'''
Stack:
- __init__       s = Stack() -> this makes an empty Stack
- pop -> returns and removes top element in Stack
- push -> takes in an object and adds it to top of Stack
- is_empty -> True or False
'''


def get_top(s):
    '''
    (Stack) -> object
    Given a stack, return the top item on the stack
    but leave the stack unchanged when the function ends.
    '''

    item = s.pop()
    s.push(item)
    return item

def remove_items(s):
    '''
    (Stack) -> None
    Given a stack, remove all but the bottom item from it.
    The removed items are simply discarded.
    '''

    while not s.is_empty():
        item = s.pop()
    s.push(item)

    # This won't work because this would return whatever
    # s.push returns which is None, because the push
    # method doesn't return anything:
    #  return s.push(s.pop())

    # This won't work because the function will exit
    # after you return, so the second line won't get run.
    #  return s.pop()
    #  s.push(s.pop())
 
def size(s):
    """(Stack) -> int 
    Return the number of items on Stack s, *without* modifying s. 
    (It's OK if the contents of s are modified during the execution of this 
    function, as long as everything is restored before the function returns.) 
    """ 
    # Hint: You can use more than one stack. 

    s2 = Stack() # this creates a new empty stack

def size1(s):
    return len(s) # can not assume this works; it's not part of Stack's public interface
    return len(s._data) # DO NOT TOUCH INTERNALS OF THE ADT

def size2(s):
    total = 0
    while not s.is_empty():
        total += 1
        s.pop()
    return total # this will give the right total, but the stack is destroyed!!!

def size3(s):
    s2 = Stack()
    total = 0
    while not s.is_empty():
        total += 1
        s2.push(s.pop())   # this is same as: item = s.pop(); s2.push(item)

    while not s2.is_empty():
        s.push(s2.pop())

    return total

def size4(s):
    lst = []
    total = 0
    while not s.is_empty():
        total += 1
        lst.append(s.pop())

    for item in lst:
        s.push(item)

    return total # DOES THIS WORK? this will reverse the order
# simple fix: use lst.reverse()










