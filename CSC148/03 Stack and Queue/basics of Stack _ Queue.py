class Stack():
    def __init__(self):
        self.data = []

    def push(self, element): #看你把哪边当top哪边当bottom
        self.data.insert(0,element)
        
##    def push(self, element): 
##        self.data.append(element)

    def pop(self):
        return self.data.pop(0)
    
##    def pop(self): #pop最后一位
##        return self.data.pop()

    def is_empty(self):
        return self.data == []

    def peek(self):  #to see the 'top' item
        return self.data[0]

    def size(self):
        return len(self.data)

    def __repr__(self):
        s = 'top\n'
        for element in self.data:
            s += str(element) + '\n'

        s += 'floor'

        return s


class Queue():
    def __init__(self):
        self.data = []

    def enqueue(self, element):#这些特定的名字一定要记住
        self.data.append(element)

    def dequeue(self):
        return self.data.pop(0)

    def is_empty(self):
        return self.data == []

    def peek(self): #下一个要出去的东西
        return self.data[0]

    def size(self):
        return len(self.data)

    def __repr__(self):
        s = 'head\n'
        for element in self.data:
            s += str(element) + '\n'

        s += 'tail'

        return s
    
###############################################################

#########Order system#########

class Order():
    def __init__(self, title, Type, content, price):
        self.title = title
        self.type = Type
        self.content = content
        self.price = price

    def __repr__(self):
        s = '[Title]:{}     [Type]:{}     [Price]:{}\n[Content]: {}'.format(self.title, \
                            self.type, self.price, self.content)

        return s

    
s = Stack()
q = Queue()


## [load module] ## need info.txt

f = open('info.txt')
line = f.readline().strip()
while line != '':
    info = line.split(',')
    title = info[0]
    Type = info[1]
    content = info[2]
    price = info[3]
    
    order = Order(title, Type, content, price)

    if order.type =='g':
        q.enqueue(order)
    else:
        s.push(order)

    line = f.readline().strip()
        

current_order = None
menu = '#Option:\n#    detail\n#    add\n#    next\n#    quit'
print(menu)
user_input = input('#Input option: ')

while user_input != 'quit':
    
    if user_input == 'add':#add 
        title = input('input the title: ')
        # type i  is important , g is general
        Type = input('input type of order[i/g]: ') # must input i or g
        content = input('content: ')
        price = input('price: ')

        order = Order(title, Type, content, price) # create an order
        #add the order in queue or stack
        if order.type =='g':
            q.enqueue(order)
        else:
            s.push(order)


    elif user_input == 'next':#next
        if not s.is_empty(): # first handle important order
            current_order = s.pop()
            print('current order is : ', order.title)
        elif not q.is_empty():
            current_order = q.dequeue()
            print('current order is : ', order.title)
        else: # not order
            print('finished all orders')

        
    elif user_input == 'detail':#detail
        if current_order == None:
            print('current order is none')
        else:
            print(current_order)

        
    else:
        print('Wrong input, pls input again')


    print()
    print(menu) # print menu and get new input
    user_input = input('#Input option: ')



def size(stk):
    n = 0
    new_stk =Stack()
    
    while not stk.is_empty():
        n +=1
        new_stk.push(stk.pop())



    while not new_stk.is_empty():
       stk.push( new_stk.pop() )

    return n

#############################################################################################

class BuildingCodeViolationError(Exception):
    pass

class InvalidBusinessError(Exception):
    pass

class BuildingCreationException(Exception):
    pass

        

class room():
    def __init__(self, name, square_footage, time):

        if type(name) != str or type(square_footage) != float or type(time) != str:
            raise BuildingCreationException
            
        self.name = name
        self.square_footage = square_footage
        self.t = time

    def __str__(self):
        return self.name + ',' + str(self.square_footage)

    def rename(self, new):
        if type(new) != str:
            raise BuildingCreationException
            
        self.name = new

    def change(self, size):
        if type(size) != float:
            raise BuildingCreationException
            
        self.square_footage = size


class building():
    def __init__(self, addr, time):

        if type(addr) != str or type(time) != str:
            raise BuildingCreationException
        self.rooms =[]
        self.address = addr
        self.num = 0
        self.t = time


    def __str__(self):
        n = 0
        for r in self.rooms:
            n += r.square_footage
            
        return str(n)

    def add_room(self, r):
        if type(r) != room:
            raise BuildingCreationException
            
        self.rooms.append(r)
        self.num += 1

    def rename_room(self, name, new):
        for r in self.rooms:
            if r.name == name:
                r.rename(new)
                return


class house(building):
    def __str__(self):
        s = "Welcome to our house\n"
        for r in self.rooms:
            s += str(r) + '\n'

    def add_room(self, r):

        if self.num == 10:
            raise BuildingCodeViolationError('too many rooms')

        self.rooms.append(r)



class business(building):

    def change_room_size(self, name, new):
        for r in self.rooms:
            if r.name == name:
                r.change(new)

    def add_room(self, r):
        if r.name == 'Bedroom' or r.square_footage < 100:
            raise InvalidBusinessError

        super().add_room(r)
