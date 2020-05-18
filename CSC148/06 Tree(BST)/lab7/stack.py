'''Stack ADT.

Operations:
    pop: remove and return top item
        push(item): store item on top of stack
        is_empty: return whether stack is empty.
'''


class Stack:

    '''A last-in, first-out (LIFO) stack of items'''

    def __init__(self: 'Stack') -> None:
        '''A new empty Stack.'''
        self._data = []
        
    def pop(self: 'Stack') -> object:
        '''Remove and return the top item.

        >>> s = Stack()
        >>> s.push(2)
        >>> s.push(3)
        >>> s.pop()
        3
        '''
        return self._data.pop()
        
    def is_empty(self: 'Stack') -> bool:
        '''Return whether the stack is empty.

        >>> s = Stack()
        >>> s.push(4)
        >>> s.pop()
        4
        >>>s.is_empty()
        True
        '''
        return self._data == []
        # or return len(self._data) == 0
    
    def push(self: 'Stack', o: object) -> None:
        '''Place o on top of the stack.'''
        self._data.append(o)
        
if __name__ == '__main__':
    import time
    s = Stack()
    items = range(100000)

    # start the clock
    start = time.time()
    
    for i in items:
        s.push(i)
        
    for i in items:
        s.pop()
        
    end = time.time()
    print("It took ", end - start, "to push/pop", len(items), "items")

