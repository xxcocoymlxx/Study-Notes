import time

class Stack():
    def __init__(self, size=5):
        self.data = []
        self.size = size


    def push(self, element):
        if len(self) < self.size:
            self.data.insert(0, element)
        else:
            print('Stack is full!!')


    def pop(self):
        if self.is_empty():
            print('Stack is empty!!!')
            return
        
        return self.data.pop(0)

    
    def is_empty(self):
        return self.data == []

    def __len__(self):
        return len(self.data)

    def peek(self):
        return self.data[0]




class Stack1():
    def __init__(self, size=5):
        self.data = []
        self.size = size


    def push(self, element):
        if len(self) < self.size:
            self.data.append(element)
        else:
            print('Stack is full!!')

        #head
        #self.data.insert(0, element)


    def pop(self):
        if self.is_empty():
            print('Stack is empty!!!')
            return
        
        return self.data.pop()

        #
        #return self.data.pop(0)

    
    def is_empty(self):
        return self.data == []

    def __len__(self):
        return len(self.data)

    def peek(self):
        return self.data[-1]

    

##s1 = Stack(1000)
##t1 = time.time()
##for i in range(1000):
##    s1.push(i)
##t2 = time.time()
##print('s1 push', t2-t1)
##
##
##s2 = Stack1(1000)
##t1 = time.time()
##for i in range(1000):
##    s2.push(i)
##t2 = time.time()
##print('s2 push', t2-t1)
##
##
##
##
##t1 = time.time()
##for i in range(1000):
##    s1.pop()
##t2 = time.time()
##print('s1 pop', t2-t1)
##
##
##t1 = time.time()
##for i in range(1000):
##    s2.pop()
##t2 = time.time()
##print('s2 pop', t2-t1)



class Queue():
    def __init__(self, size=5):
        self.data = []
        self.size = size

    def enqueue(self, element):
        if len(self) < self.size:
            self.data.append(element)
        else:
            print('Queue is full!')

    def dequeue(self):
        if self.is_empty():
            print('Queue is empty!')
            return

        return self.data.pop(0)

    def is_empty(self):
        return self.data == []

    def __len__(self):
        return len(self.data)

    def peek(self):
        if self.is_empty():
            print('nothing')
            return
        return self.data[0]
    




class TODOList():
    def __init__(self):
        self.data = []

    def add_msg_n(self, msg):
        self.data.append(msg)

    def add_msg_s(self, msg):
        self.data.insert(0, msg)

    def next_todo(self):
        if self.data == []:
            return '----No msg----'
        return self.data.pop(0)

    def peek(self):
        if self.data == []:
            return '----No msg----'
        return self.data[0]

    def __str__(self):
        s = 'TO DO LIST:\n'
        for msg in self.data:
            s += msg + '\n'

        return s

    def run_todo_list(self):
        curr = '----No msg----'
        order = '   add msg\n   see\n   finish current\n   quit\n'

        print('Current Event: ', curr)
        print()
        print(order)
        info = input('please input an order:')
        
        while info != 'quit':
            if info not in ['add msg','see','finish current']:
                print('wrong order! input again!')
                
            elif info == 'add msg':
                msg = input('please input msg: ')

                t = input('msg type[n/s]: ')
                while t not in 'ns':
                    print('wrong type, input again!!!')
                    t = input('msg type[n/s]: ')

                if t == 'n':
                    self.add_msg_n(msg)
                else:
                    self.add_msg_s(msg)

            elif info == 'see':
                print(self)

            elif info == 'finish current':
                print('Finish current:', self.next_todo())


            if self.data != []:
                curr = self.data[0]
            
            print('\n=============================\n')
            print('Current Event: ', curr)
            print()
            print(order)
            info = input('please input an order:')
