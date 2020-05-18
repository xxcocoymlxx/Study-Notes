class Stack:
    
    def __init__(self):
        '''A new empty stack'''
        self.items = []
    
    def push(self, o):
        '''Make o the new top item in this Stack.'''
        self.items.append(o)
        
    def pop(self):
        '''Remove and return the top item.'''
        return self.items.pop()
    
    def peek(self):
        '''Return the top item.'''
        return self.items[-1]
    
    def isEmpty(self):
        '''Return whether this stack is empty.'''   # This is like a Javadoc comment.
        return self.items == []
    
    def size(self):
        '''Return the number of items in this stack.'''
        return len(self.items)

class UpStack:

    # The top item is at index 0.
    
    def __init__(self):
        '''A new empty stack'''
        self.stack = []
    
    def push(self, o):
        '''Make o the new top item in this Stack.'''
        self.stack.insert(0, o)
        
    def pop(self):
        '''Remove and return the top item.'''
        return self.stack.pop(0)
    
    def peek(self):
        '''Return the top item.'''
        return self.stack[0]
    
    def isEmpty(self):
        '''Return whether this stack is empty.'''   # This is like a Javadoc comment.
        return self.stack == []
    
    def size(self):
        '''Return the number of items in this stack.'''
        return len(self.stack)
