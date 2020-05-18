#Recursion[递归]
        #一种在方程中调用自己的结构模式

        #Bace case [底层出口]
        #Recursion [子结构]
        #Return [结构出口]
        #探底--抓值(构建)--返回


def is_palindrome(s): #回文 'level'
    #s='abcdcba'   s' = 'bcdcb'    s'' = 'cdc'    s''' = 'd' [True]
    
    if len(s) <= 1:
        return True

    if s[0] != s[-1]:   #s[0] = a = s[-1]
        return False

    
    return is_palindrome(s[1:-1])



def fib(n):
    #s(n) = s(n-1) + s(n-2)       s(1) = s(2) = 1

    if n <= 2:
        return 1

    return  fib(n-1)  + fib(n-2)


def count_sum(obj):
    # ojb = [[2,[5,6,[1]]], [1,4], 3, 5]
    #26
    

    s = 0

    for ele in obj:
        if type(ele) == int:
            s += ele
        else:
            s += count_sum(ele)

    return s


def max_value(obj):
    if obj == []:
        return 0

    l = []
    for elm in obj:
        if type(elm) == int:
            l.append(elm)
        else:
            m = max_value(elm)
            l.append(m)

    return max(l)


def binary(n): # 13 ->  1111         | 8765 ->   8765

    # binary(13) = binary(6)['111'] + '1'

    #binary(6) = binary(3)['11'] + '1'
    #binary(3) = binary(1)['1'] + '1'
    #binary(1) = binary(0)[''] + '1'
    #binary(0) = ''
    
    if n == 0:
        return ''

    return  binary(n//2)  + str(n%2)
    

def binary_2(n):#??????????
    s = ''
    while n != 0:
        s = str(n%2) + s

        n = n//2

    return s


def octonary(n): # 177 - 22 - 2 - 0  -> 261
    if n == 0:
        return ''
    return octonary(n//8) + str(n%8)



def is_show_in_num(money, num):
    '''给你money分钱，看能否用num个硬币表示出来'''
    coin = [1,5,10,25]

    # (31,3) -> (30,2) (26,2) (21,2) (26,2)

    # (30,2) -> (29,1) (25,1) (20,1) (5,1)

    if num == 0 or money < 0:
        return False

    if money in coin:
        return True

    for c in coin:
        new = money - c
        if is_show_in_num(new, num-1):
            return True

    return False



##import time

##t1 = time.time()
##b=binary(3**600)
##t2 = time.time()
##print('r:', t2-t1)
##
##
##t1 = time.time()
##b=binary_2(3**600)
##t2 = time.time()
##print('w:', t2-t1)



def subset_sum(w,t):
    """
    看t能不能被w里的数表示出来,每个数只能用一次

    >>> subset_sum([1,4,4,6,9], 16)
    True
    >>> subset_sum([1,4,4,6,9], 24)
    True
    >>> subset_sum([1,4,4,6,9], 12)
    False
    
    """
    if t in w:
        return True
    if sum(w) < t:
        return False

    for e in w:

        new_t = t - e
        new_w = w[:]#cannot change the original w
        new_w.remove(e)

        if subset_sum(new_w, new_t):
            return True

    return False


def subset_sum_2(w,t):#???????????
    """
    如果t能被w里的数表示出来(每个数只能用一次), return the list
    >>> subset_sum([1,4,4,6,9], 16)
    True
    >>> subset_sum([1,4,4,6,9], 24)
    True
    >>> subset_sum([1,4,4,6,9], 12)
    False
    
    """
    if t in w:
        return [t]
    if sum(w) < t:
        return []

    for e in w:

        new_t = t - e
        new_w = w[:]
        new_w.remove(e)

        sub = subset_sum_2(new_w, new_t)
        if sub != []:
            return [e] + sub

    return []



def factorial(n):
    if n <= 1:
        return 1

    return  n*factorial(n-1)



class UnequalLists(Exception):
    pass

def dotProduct(a,b):
    if len(a) != len(b):
        raise UnequalLists()

    if a == b == []:
        return 0

    return a[0]*b[0] + dotProduct(a[1:],b[1:])


def factor(x):
    ''' Return a factor dict that key is a factor
    and the value is frequency of the factor
    '''
    if x in [2,3,5,7,11,13,17,19,23,29]:#some prime numbers
        return {x:1}
    #当这个循环结束了依然没有进去if，就说没没找到任何因数，所以这个数是个prime number
    
    d={}
    for i in range(2,x//2):#尽量拆小 拆一层 最小的因数是2
        #最大的因数不会超过n//2, 因数上下限
        
        # 既然能进去if 就说明找到了一个因数了 那我们就找除去那个因数的factor就好了
        if x/i == x//i:#找因数,看能不能除尽,若不能,loop进不去,换下一个
            d[i]=1
            l=factor(x//i)#找到了一个因数i了,找除去那个因数的factor就好
            for key in l:#这里return出来的值assign进了l,all the factors found
                if key not in d:
                    d[key]=l[key]#??????
                else:
                    d[key]+=l[key]

            return d
            

    return {x:1}





##    # 100  2  -> {5:2, 2:2}
##    # 50   2  -> {5:2, 2:1}
##    # 25   5 -> {5:2}
##    # 5    {5:1} 
##    for i in range(2,n//2):
##        if n//i == n/i: #判断i是否是n的因数
##            f = factor(n//i)
##            if i in f:
##                f[i] += 1
##            else:
##                f[i] = 1
##            return f
##
##    return {n:1}
##

def nested_concat(s):
    """(str or list) -> str

    'str' -> 'str'
    ['a',['w','e',['1'],'2'],'r'] ->'awe12r'

    """

    if type(s) == str:
        return s
    r=''
    for e in s :
        r+= nested_concat(e)

    return r


def count_element(s):
    """(list or non-list) -> int

    ['a',['w','e',['1'],'2'],'r']
    """
    
    if type(s) != list:
        return 1

    r=0
    for  e in s:
        r += conut_element(e)

    return r


def length(s):
    """(list or non-list) -> int
    Return  max lenght of all list

    e - > 0

    [1,2,[2,3,4,0,9,5],5,6]
    """
    if type(s) != list:
        return 0

    l=[]
    l.append(len(s))

    for e in s:
        l.append(length(e))
        
    return max(l)


def nest_level(l):#????????
    n=0
    for e in l:
        if type(e) == list:
            n=max(n,nest_level(e))
           
    return 1+n

