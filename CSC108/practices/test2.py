def fold2(d1, d2):
    '''(dict, dict) -> dict
    Return a new dictionary that contains all (a, c)
    such that (a, b) is in d1 and (b, c) is in d2.

    >>> fold2({1:4}, {9:10})
    {}
    
    >>> fold2({1:4, 9:10}, {4:5})
    {1: 5}
    
    >>> d = fold2({1:4, 9:10, 8:4}, {4:5})
    >>> d == {1: 5, 8: 5}
    True

    # OTHER POSSIBLE TEST CASES:
    
    # empty dict

    # no match

    # if d2 is longer than d1

    # if d1 is longer than d2

    # one match
    
    # more than one match
    
    '''
    
    outd = {}
    for key, value in d1.items():
        if value in d2:
            outd[key] = d2[value]
    return outd

# alternative:
#for key in d1:
#    if d[key] in d2:
        
import doctest
doctest.testmod()
