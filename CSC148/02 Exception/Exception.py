##################################
class Stack():
    def __init__(self, size = 5):
        self.data = []
        self.size = size

    def is_empty(self):
        return self.data == []
    

    def push(self,e):
        if len(self.data) <self.size:
            self.data.append(e)
        else:
            print('The Stack is full')

    def pop(self):
        if not self.is_empty():
            return self.data.pop()
        else:
            print("The Stack is empty")

    def __repr__(self):
        s=""
        for e in self.data:
            s+= str(e) +" -> "

        return s[:-4]
####################################

#Exception

class testError(Exception):
    pass


class StackException(Exception):
    pass



#assert
x = 10
assert type(x) == int , 'person must be intager'
# assert [expression] , [prompt message]


assert 1 >= 0
assert True, 'False'
##########



#raise
#raise IndexError()
#raise Exception('info')
#raise testError('test')

s = Stack()
s.push(1)
if s.is_empty():
    raise SackException()
#print(s.pop())

########



#try
##try:
##    #data  = 1
##
##    if type(data) != int:
##        raise IndexError
##    
##
##    print('done code module')
##
##
##except NameError as a:
##    print(a)
##
##except AssertionError:
##    print('assert error')
##else:
##    print('No error')
##finally:
##    print('finally, alway execute')
##
##print('finish try module')
##print('go on ......')
##
##print('################')



#########################


##prompt = 'input price or quit: '
##total = 0
##
##order = input(prompt)
##while order != 'quit':
##    try:
##        x = int(order)
##
##    except Exception:
##        print('invalid input')
##        x = 0
##
##    total += x
##    print('total is ',total)
##
##    order = input(prompt)




#recursion example
# 1,1,2,3,5,8,13,21,34
# a(n) = a(n-1)+ a(n-2)

def fal(n):
    if n <= 2:
        return 1

    return fal(n-1) + fal(n-2)



    
f(6)-> f(5)                    +            f(4)
        f(4)        +   f(3)                f(3)   +  f(2)
        f(3)    + f(2)   f(2)+f(1)          f(2)+f(1)
        f(2)+f(1)





























    
