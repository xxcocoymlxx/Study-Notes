def find_num(SL:list, n: int) -> bool:
    """
    Return True if n is in SL, False otherwise.
    Notice that if a given integer is less than element 0,
    it is either in element 1 somewhere, or not in the SearchList at all.
    Similarly, if a given integer is greater than element 0,
    it is either in element 2 somewhere, or not in the SearchList at all.
    >>> find_num([5, [2, [1, None, None], [3, None, None]], [6, None, None]],3)
    >>>True
    """
##    if SL is not None:
##        if SL[0] == n:
##            return True
##        elif SL[0] > n and find_num(SL[1],n):
##            return True
##        elif SL[0] < n and find_num(SL[2],n):
##            return True
##        else:
##            return False
##    else:
##        return False
    if n in SL:
        return True
    
    for sub in SL:
        if tyoe(sub) == list:
            if find_num(sub,n):
                return True
    return False

def freeze(X: object) -> object:
    """
    If X is a list, return a new list with equivalent contents,
    and recursively treat the contents of X as you treated X itself...
    If X is not a list, return X itself
    >>> ... don’t forget examples!
    ...
    ...
    """
    if type(X) is not list:
        return [X]
    if X==[]:
        return []
    else:
        if X != []:
            return freeze(X[0])+freeze(X[1:])
