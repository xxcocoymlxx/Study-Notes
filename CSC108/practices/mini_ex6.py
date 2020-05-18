# TO DO:
# 1) Add in AT LEAST ONE test case into the docstring
#    that makes this code FAIL
#
# 2) Explain below WHY you think this function doesn't work
#    i.e. what causes this error?
#    Your answer here:
#    When the big is 'coool pool', the small 'oo' can be found in big[1] 
#    and big[2], which is overlapping. So this case fails.
#    
#

def indices(big, small): 
    '''(str, str) -> list of int 
    Return the indices of big at which non-overlapping 
    copies of small start. small is non-empty.

    Assumption: len(big) > len(small)
    
    >>> indices('cool pool', 'oo')
    [1, 6]
    
    >>> indices('cool pool', 'oo')
    [1, 6]help

    >>> indices('coool pool','oo')
    [1,2,7]
    '''

    index = 0
    indices = []
    while index != -1:
        indices.append(big.find(small, index))
        index = big.find(small, index + len(small))
    return indices    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
