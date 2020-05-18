def codes(r):
    '''
    Given length r, return list of all binary codes of that length.
    给出长度r，return所有由0和1组成的r长度的数字.
    >>>codes(2)
    ['00', '01', '10', '11']
    >>>codes(3)
    ['000', '001', '010', '011', '100', '101', '110', '111']
'''

    if r == 0:
        return ['']
    #之前的疑问：这里return了接下来还会append吗?
    #答：会，因为他是base case，如果只有一层，则会return，function结束
    #但若有很多层，他也会return，但return出来的只是一层的结果，
    #这一层的结果会返回到再上一层，最后答案累计，才为最终return的结果

    else:   # if r > 0
        
        lst = []#每次call function都刷新一遍lst

        smaller = codes(r-1)#要相信这个function就是得到并返回所有binary code的list
        for code in smaller:#把smaller里的每一个elm再加个0和1
            lst.append(code + '0')# ''+ '1' = '1'
            lst.append(code + '1')#此时lst里是没有东西的，每次都append(小规模的数+1)
                                  #和append(小规模的数+0)进lst

        return lst

def count_people(L):
    if L == []:   # base case YOU MUST HAVE THIS FOR THE RECURSION TO NOT BE INFINITE
        return 0
    else:
        return 1 + count_people(L[1:])


def strlen(s):
    '''Recursively figure out length of s and return it.'''

    if s == '':
        return 0
    else:
        return 1 + strlen(s[1:])

    

def num_a(s):
    '''Use recursion. Return the number of 'a's in s.

    >>> num_a('bob')
    0

    >>> num_a('aaaaaah')
    6
    '''
    #USE RECURSION. you can use things like s == , s[0], s[1:]
    if s == '':
        return 0
    elif s[0] == 'a':
        return 1 + num_a(s[1:])
    else:
        return num_a(s[1:])
    
def remove_three(L):
    '''Use recursion. Return a new list with all elements of L except the 3s.
    DO NOT USE ANY LIST METHODS!
    
    >>> remove_three([1, 2, 3])
    [1, 2]

    >>> remove_three([1, 3, 3, 1, 3])
    [1, 1]
    '''

    if L == []:
        return []
    elif L[0] == 3:
        return remove_three(L[1:])
    else:
        return [L[0]] + remove_three(L[1:])#lists can be added by '+'


def contains(lst, v):
    '''Return True iff lst contains value v.'''
    # DO NOT USE "in", use recursion
    
    if lst == []:
        return False
    elif lst[0] == v:
        return True
    else:
        return contains(lst[1:], v)

def contains2(lst, v):
    '''
    Return True iff lst contains value v.
    lst may have nesting to arbitrary depth.

    >>> contains2([1, [[2], 3]], 3)
    True

    >>>contains2([1, [[2], 3]], 4)
    False
    '''
    if lst == []:
        return False

    elif isinstance(lst[0], int): # if it's an integer
        if lst[0] == v:
            return True
        else:
            return contains2(lst[1:], v)
        
    else: # if lst[0] is another nested list
        return contains2(lst[0], v) or contains2(lst[1:], v)
    #这个东西要么在sub-list里，要么在之后的list里，
    #这个expression自动返回bool值（这里or是把if和elif合一起写了）
    

def contains3(lst, v):#better one

    for e in lst:
        if isinstance(e, int):
            if e == v:
                return True
        else:
            if contains3(e, v):
                return True

    return False
