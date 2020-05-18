def size(stk):

    n = 0
    new = Stack()
    while not stk.is_empty():
        new.push(stk.pop())
        n += 1

    while not new.is_empty():
        stk.push(new.pop())


    return n


#stk
# 1    5    4     1
# 2    4    5     2
# 3    3    3     3
# 4    2    2     5
# 5    1    1     4


class TestError(Exception):
    pass

def swap_top_2(stk):
    if stk.is_empty():
        raise TestError
    f = stk.pop() # 1

    if stk.is_empty():
        stk.push(f)
        raise TestError
    s = stk.pop() # 2
    

    stk.push(f)
    stk.push(s)





try:
    #code
    
    a = [1,2,3,4]
    print(a)

    assert a[3] > 3, 'hahaha' 

    p = 1.5
    if type(p) != int:
        raise TestError('T__T')
    
    print('done')

except NameError as w:
    print(w)

except IndexError as qqq:
    print('index')

except TestError as t:
    print('.........', t)

except AssertionError as o:
    print(o)
    
##except Exception:
##    print('all error')

else:
    print('no error')


finally:
    print('fianlly')



def is_palindrome(s):

    if len(s) <= 1:
        return True
    

    if s[0] != s[-1]:
        return False

    return is_palindrome(s[1:-1])


#(3, 10)            -> 94
#(2, 22)        -> 94
#(1, 46)    -> 94
#(0, 94) -> 94
def find_count(day, num):
    if n == 0 :
        return num

    return find_count(day-1, 2*(num + 1))



def find_count_2(n, count):
    if n <= 1:
        return count

    return find_count_2(n-2, 2*count)


def find_count_3(n, count):
    if n == 0:
        return count

    new = 2*(count-1)

    return find_count_3(n-1, new)





# (4, 10)   [130, 66, 34, 18, 10]
# (3, 18)   [130, 66, 34, 18]
# (2, 34)   [130, 66, 34]
# (1, 66)   [130, 66]
# (0, 130)  [130]
def find_count_3_c(n, count):
    if n == 0:
        return [count]

    new = 2*(count-1)
    l = find_count_3_c(n-1, new)
    l.append(count)

    return l



def replace_ab(s):
    if len(s) < 2:
        return s

    if s[0:2] == 'ab':
        return 'xy' + replace_ab(s[2:])

    else:
        return s[0] + replace_ab(s[1:])


def queue_size(q):
    n = 0
    new = Queue()
    
    while not q.is_empty():
        new.enqueue(q.dequeue())
        n += 1

    while not new.is_empty():
        q.enqueue(new.dequeue())


def remove_dups(s):

    new = Stack()

    while not s.is_empty():
        new.push(s.pop())

    item = new.pop()
    s.push(item)
    while not new.is_empty():
        curr = new.pop()
        if item != curr:
            s.push(curr)
            item = curr


# [[2,3,4],[1,[2],2],[],1]  depth =[1, 2, 0, 0] -> 3

# [2,3,4] -> 1

# [1,[2],2]  depth= [0,1,0] -> 2
# [2] -> 1

# [] -> 0

def max_depth(lst):
    if lst == []:
        return 0
    
    depth = []
    for e in lst:
        if type(e) == int:
            depth.append(0)
        else:
            depth.append(max_depth(e))

    return max(depth) + 1


# [[0,1,2,[3,4]],[5,[6,[7]]],10,[11]]


def mystery(lst):
    '''按广度搜索的顺序形成一个新list'''
    #[[0,1,2,[3,4]],[5,[6,[7]]],10,[11]]
    q = Queue() # ()
    ret = []
    for item in lst:
        q.enqueue(item) #[0,1,2,[3,4]] #[5,[6,[7]]] #10 #[11]

    while not q.is_empty(): 

        element = q.dequeue() #7
        if isinstance(element, list):
            for element2 in element:
                q.enqueue(element2)
        else:
            ret.append(element) #ret = [10, 0, 1, 2, 5, 11, 3, 4, 6, 7]
    return ret




def divide_loop(s, char):

    s = char
    for c in s:
        if c < char:
            s = c + s
        elif c > char:
            s = s + c
            
    return s


#'acdeb'  'c'

# 'a' + divide('cdeb','c') -> 'abced'
# divide('debc','c') -> 'bced'

#  divide('ebc','c') + 'd' -> 'bced'
#  divide('bc','c') + 'e' -> 'bce'
#  'b' + divide('c','c') -> 'bc'

# divide('c','c') -> 'c'

def divide(s, char):
    if s == char:
        return s
    
    if s[0] < char:
        return s[0] + divide(s[1:], char)

    elif s[0] > char:
        return divide(s[1:], char) + s[0]

    else:
        return divide(s[1:]+ s[0], char)












