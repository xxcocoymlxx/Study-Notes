#Handout, question 1

from stack import Stack

def change(s1: Stack):
  s2 = Stack()
  while not s1.is_empty():
    first = s1.pop()
    if s1.is_empty():
      s2.push(first)
    else:
      second = s1.pop()
      s2.push(second)
      s2.push(first)
  while not s2.is_empty():
    s1.push(s2.pop())
    
##For the 1 2 3 4 stack, we will get this from the first loop:
##
##s1:
##s2: 3 4 1 2
##
##First loop is done. Now second loop...
##
##s1: 2 1 4 3
##s2: 
##
##Now we know how to trace this code.
##But now I want an English explanation of what the code does. NOT a line-by-line description of the code.
##
##Great answer: Each pair of neighboring elements in s1 swap places; if s1 is of odd length, the bottom element remains in-place.
##
##Tip: don't "invent" special cases. Even if your code has special cases, it doesn't mean that your explanation has to.
##In this case, the "odd-length" stack is a special case because otherwise it isn't clear what happens to the element that's left out of a pair.
##
##----

#Handout, question 2

from stack import *

def roll (s, n):
    '''Perform the roll operation on s.'''
    t = Stack()
    
    for i in range(n - 1):#to move all the elm before n
        t.push(s.pop())
        
    rollVal = s.pop()#save the elm we wanna move to the top

    while t.isEmpty() == False:
        s.push(t.pop())
    s.push(rollVal)#lastly push in the elm we wanna move

# == sample marking scheme; mark this out of 5 marks ==
# 0.5 for creating an empty stack
# 0.5 for using a loop; 0.5 for having the correct range
# 0.5 for doing the t.push(s.pop()) part
# 0.5 for keeping track of the rollVal
# 0.5 for having another loop to empty out new stack; 0.5 for using it correctly (doing the s.push(t.pop() part)
# 0.5 for pushing in the roll value



#Handout, question 3

'''Queue ADT.

Operations:
    dequeue: remove and return head of queue
        enqueue(item): add to tail of queue
        is_empty: return whether queue is empty.
'''


class Queue:

    '''A first-in, first-out (FIFO) queue of items'''

    def __init__(self: 'Queue') -> None:
        '''A new empty Queue.'''
        self._data = {}
        
    def dequeue(self: 'Queue') -> object:
        '''Remove and return the head of the queue.

        >>> q = Queue()
        >>> q.enqueue(2)
        >>> q.enqueue(3)
        >>> q.dequeue()
        2
        '''
        return self._data.pop(min(self._data.keys()))
        
    def is_empty(self: 'Queue') -> bool:
        '''Return whether the queue is empty.

        >>> q = Queue()
        >>> q.enqueue(4)
        >>> q.dequeue()
        4
        >>> q.is_empty()
        True
        '''
        return self._data == {}
        # or return len(self._data) == 0
    
    def enqueue(self: 'Queue', o: object) -> None:
        '''Place o at tail of queue.'''
        self._data[max([0] + list(self._data.keys())) + 1] = o
        
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()


#BONUS PRACTICE QUESTION: Try implementing another version of Queue,
#but instead of a list or a dictionary, use two Stacks to implement it.
#(Assume Stack class is available for you to use. You can import Stack into your program.
