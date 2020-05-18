def is_ok(group_list, class_list):
    '''
    Return true iff every student in class_list is in
    exactly one group according to group_list.

    # See Lecture 15 slides for examples and test cases

    >>> is_ok([[1, 3, 4], [2]], [1, 2, 3, 4])
    '''
    acc = []
    acc2 = []
    for item in group_list:
        acc.extend(item)

    for item in acc:
        if item not in acc2:
            acc2.append(item)
        else:
            return False

    for item in class_list:
        if item not in acc2:
            return False

    return True


# OPTIONAL; try completing the following function as well
def col_sums(lst):
    '''(list of list of int) -> list of int
    Return a new list that contains the sum of each column in lst. 
    All columns in lst are of the same length.

    >>> col_sums([[5, 10, 15], [1, 2, 3]])
    [6, 12, 18]
    '''
    acc = lst[0]
    for i in range(len(lst)):
        i2 = 0
        for item in lst[i]:
            acc += item[i2]
            i2 += 1
    return acc
        
