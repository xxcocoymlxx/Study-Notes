def cookies_needed(adults, teens, children):    
    ''' (int, int, int) -> int
    Return the number of cookies needed to
    feed this number of adults, teens and children.
    Each adult eats three, each teen five, and each child two.
    >>> cookies_needed(2, 3, 1)
    23
    '''
    return ((adults * 3) + (teens * 5) + (children * 2))


def is_multiple_of_3(x):
    ''' (int) -> bool
    Return True iff x is an even multiple of 3.
    >>> is_multiple_of_3(15)
    True
    >>> is_multiple_of_3(7)
    False
    '''
    return (x % 3 == 0) 


def is_multiple(x, y):
    ''' (int, int) -> bool
    Return True iff x is an even multiple of y.
    >>> is_multiple(15, 3)
    True
    >>> is_multiple(7, 2)
    False
    '''
    return (x % y == 0)
