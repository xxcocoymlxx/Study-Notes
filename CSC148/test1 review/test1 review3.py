#test1 review 2
#2017.t1.utm

#Q1
class StackFullException(Exception):
    pass


class SpecialStack:
    """A last-in, first-out (LIFO)
    stack of integer items and limited capacity"""
    
    def __init__(self, max_capacity):
        """(SpecialStack, int) -> None
        A new empty SpecialStack."""
        self._data = []
        self._max_capacity = max_capacity

        
    def push(self, item):
        """(SpecialStack, int) -> None
        Place item on top of the stack.
        >>> s = SpecialStack(2)
        >>> s.push(1)
        >>> s.push(’a’)
        ... TypeError raised: Sorry. Only integers are permitted
        >>> s.push(2)
        >>> s.push(3)
        ... StackFullException raised: Sorry. Maximum capacity reached
        """
        if type(item) != int:
            raise TypeError('Sorry. Only integers are permitted')

        if self._max_capacity == len(self._data):
            raise StackFullException('Sorry. Maximum capacity reached')

        self._data.append(item)



try:
    s = SpecialStack(3)

    s.push(1)

except StackFullException:
    print('aaaa')


except TypeError as t:
    print(t)



#############
#Q2

# o1 top[1,2,3,4,5] -> x[5,4,3,2,1]

# o2 head[a,b,c,d,e] -> y[a,b,c,d,e]


#b = e
#a = 5

# x[1,2,3,4,5]

#o1 top[5,4,3,2,e]

#o2 head[a,b,c,d,5]

#################
#Q3

def A():
    return 'aaaa'


#########
#Q4
def number_of_digits(n):
    if n == 0:
        return 0
    
    return 1 + number_of_digits(n//10)


##############
def octonary(n):
    if n == 0:
        return ''
    return octonary(n//8) + str(n%8)

# (22) -> (2) + '6' -> '26'
# (2) ->  (0) + '2' -> '2'
# (0) -> ''


def hexadecimal(n):
    s='0123456789ABCDEF'

    if n == 0:
        return ''

    curr = n%16
    next_n = n//16

    return hexadecimal(next_n) + s[curr]
    






def is_show(count, n)
    coin = [1,5,10,25]

    if n == 0:
        return False

    if count in coin:
        return True


    for c in coin:
        rest =  count - c
        if is_show(rest, n-1):
            return True

    return False



def first_int(L):
    if L == []:
        return None

    if type(L[0]) == int:
        return L[0]

    return first_int(L[1:])



def find_num(SL, n):

    if n in SL:
        return True
    
    for sub in SL:
        if type(sub) == list:
            if find_num(sub, n):
                return True
            
    return False



def freeze(L):
# l [1,2,[3,4,[5]]]

#new [1,2,f([3,4,[5]])] -> [1,2,[3,4,[5]]]

#[3,4,[5]]
#new =[3,4, f([5])] -> [3,4, [5]]

#[5]
#new [5]
    
    new = []
    for i in range(len(L)):
        if type(L[i]) == list:
            sub = freeze(L[i])
            new.append(sub)

        else:
            new.append(i)


    return new
            

