
def factor(n):
    ''' 100 -> 2,2,5,5 {2:2,5:2}    99->3,3,11 {3:2, 11:1}
    '''

    # 100  2  -> {5:2, 2:2}
    # 50   2  -> {5:2, 2:1}
    # 25   5 -> {5:2}
    # 5    {5:1} 
    for i in range(2,n//2):
        if n//i == n/i: #判断i是否是n的因数
            f = factor(n//i)#f is a dict
            if i in f:
                f[i] += 1
            else:
                f[i] = 1
            return f

    return {n:1}


def is_prime(n):#??????
    for i in range(2, n//2):
        if n//2 == n/2:
            return False

    return True


def factor_2(n):
    if is_prime(n):
        return {n:1}

    for i in range(2, n//2):
        if n//i == n/i:
            f = factor_2(n//i)

            if i in f:
                f[i] += 1
            else:
                f[i] = 1

            return f



def factor_3(n):
    primes = [2,3,5,7,11,13,17,19,23,29,31]
    for p in primes:
        if n//p == n/p:
            f = factor_3(n//p)
            if p in f:
                f[p] += 1
            else:
                f[p] = 1
            return f

    
    for i in range(32, n//31):
        if n//i == n/i:
            f = factor_3(n//i)
            if i in f:
                f[i] += 1
            else:
                f[i] = 1
            return f

    return {n:1}


def factor_4(n):
    ''' 100 -> 2,2,5,5 {2:2,5:2}    99->3,3,11 {3:2, 11:1}
    '''

    # 100  2  -> {5:2, 2:2}
    # 50   2  -> {5:2, 2:1}
    # 25   5 -> {5:2}
    # 5    {5:1} 
    for i in range(2,n):
        if n//i == n/i: #判断i是否是n的因数
            f = factor_4(n//i)
            if i in f:
                f[i] += 1
            else:
                f[i] = 1
            return f

    return {n:1}



##import time
##
##n = 123**10
##
##t1 = time.time()
##factor(n)
##t2 = time.time()
##print(t2-t1)
##
##t1 = time.time()
##factor_3(n)
##t2 = time.time()
##print(t2-t1)
##
##t1 = time.time()
##factor_4(n)
##t2 = time.time()
##print(t2-t1)



# n细菌  x -> 2x - 0.3x , 初始规模:50     2x-0.3x = n
def find_time(n):
    if n <=50:
        return 0

    new =  n//1.7
    return 1 + find_time(new)


def gcd(a, b):#??????????????
    if a < b:
        a,b = b,a

    if b == 0:
        return a

    r = a%b
    return (b,r)



class Stack():
    def __init__(self):
        self.data = []

    def is_empty(self):
        return self.data == []
    
    def pop(self):
        return self.data.pop()
    
    def push(self,e):
        self.data.append(e)


#2013.winter,utsc

#1
def size(stk):
    n = 0
    new = Stack()

    while not stk.is_empty():   # stk[1,2,3] -> new[3,2,1]
        n += 1
        new.push(stk.pop())


    while not new.is_empty():   # new[3,2,1] -> stk[1,2,3]
        stk.push(new.pop())
    
    return n


def reverse_below_2(stk):
    new = Stack()

    while not stk.is_empty():  # stk[1,2,3,4,5] -> new[5,4,3,2,1]
        new.push(stk.pop())


    f = new.pop()   # f = 5, new[4,3,2,1]
    s = new.pop()   # s = 4, new[3,2,1]

    stk.push(s)     # stk[4]
    stk.push(f)     # stk[5]

    while not new.is_empty(): #new[3,2,1] -> stk[1,2,3,5,4]
        stk.push(new.pop())



#Q2
def fib(n):
    if n <= 2:
        return 1

    return fib(n-1) + fib(n-2)
    

#Q3
class BuildingCodeViolationError(Exception):
    pass

class InvalidBusinessError(Exception):
    pass

class BuildingCreationException
(Exception):
    pass


class room():
    def __init__(self, name, sq, time):
        self.name = name
        self.square_footage = sq
        self.t = time


class building():
    def __init__(self, addr, num, time):
        self.address = addr
        self.num = num
        self.t = time
        self.rooms = []

    def __str__(self):
        s = 0
        for r in self.rooms:
            s += r.square_footage

        return str(s)

###########################################

class StackException(Exception):
    pass

#2014.utm
#Q1
def swap_top(s):
    if s.is_empty():
        raise StackException
    f = s.pop()

    if s.is_empty():
        s.push(f) # the stack has to be unchanged!!!
        #so if the stack only has one elm in it we have to put the elm back after popping it out
        raise StackException
    s = s.pop()


    s.push(f)
    s.push(s)

#Q2
#rec(2,2) -> rec(1,2)#[5] + rec(1,1)[3]##  = 8

#rec(1,2) -> rec(0,2)[3] + rec(0,1)[2]      
#rec(0,2) -> rec(-1,2)[2] + rec(-1,1)[1]
#rec(-1,2) -> rec(-2,2)[1] + rec(-2,1)[1]

#rec(0,1) -> rec(-1,1)[1] + rec(-1,0)[1]

##rec(1,1) -> rec(0,1)[2] + rec(0,0)[1]

#Q3

def is_palindrome(s):
    if len(s) <= 1:
        return True
    
    if s[0] != s[-1]:
        return False

    return is_palindrome(s[1:-1])



################

#2016.utm



#2

def duplicates(s):
    
if len(s) < 2:
        
return False

    
if s[0] == s[1]:
        
return True
    

    
return duplicates(s[1:])

#3

class TaskOverloadError(Exception):
    pass

class InvalidDateError(Exception):
    
pass


class TODOList():
    

def __init__(self, name, tasks = []):
        self.name = name
        self.tasks = tasks

    def add_task(self, task):
        if len(self.tasks) == 50:
            raise TaskOverloadError

        self.tasks.append(task)
    


class Task():
    def __init__(self,d,m,y,detail):
        if not(1=<d<=31) or not(1=<m<=12) or y<2016:
            raise InvalidDateError




School = TODOList('School')

d = input('Pls input a day: ')

while not d.isdigit():
    
print('invalid input')
    
d = input('Pls input a day: ')

m = input('Pls input a month: ')

while not d.isdigit():
    
print('invalid input')
    m = input('Pls input a month: ')
    


try:
    task = Task(int(d),int(m),2016,'Ace CSC148 test')
    School.add_task(task)
    

except TaskOverloadError:
    
print('too many tasks')
    

except InvalidDateError:
    
print('invalid data')


############################################################
#2011.utm
#1
class FullStackError(Exception):
    
pass


class BoundedStack(Stack):
    
def __init__(self,capacity):
        self.capacity = capacity
        
        #self._content = [] 
    	super.__init__()
    	


    
def push(self, item):
        if len(self._content) == self.capacity:
            raise FullStackError

        
#self._content.append(item)

        super.push(item)












