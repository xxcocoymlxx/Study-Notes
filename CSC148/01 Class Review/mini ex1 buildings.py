'''
==================
Mini-Exercise #1
==================
#2013 witer test1 UTSC
Write a series of classes, complete with documentation that satisfy the following specification. 

* A building has an address (a string), and a number of rooms, provided at the time of construction. (创建这个class instance的时候)

* A room has a name (a string) and a square_footage (float), provided at the time of construction. 

* When printed, a building prints the sum of the square footages of all of its rooms.

* A house is a type of building with at most 10 rooms, and prints "Welcome to our house",
plus the details of all of its rooms (name and square footage, separated by ',') 

* A business building may have any number of rooms, but no room may be named Bedroom, or have a square footage of less than 100

* It is possible to rename any room in any building (by specifying an old and a new name),
#所以rename一定是个room的method，而room也一定是个单独的class
but only a business can change the square footage of their rooms (by specifying the room name and the new square footage)

--

Write a main code body (that should only execute when this file is run directly, not when it 
is imported), to perform the following: 

1. Prompt the user for a building type (that is either "building", "house", or "business"), an address, and a number of rooms.
2. Using this number of rooms, ask for room name and square footage repeatedly until that many rooms have been created.
3. Create a building of the chosen type, with the given address, and this list of rooms that you created in Step 2.

Main code body should look like this

if __name__ == "__main__":
	# code
'''

'''
草稿
class Building:
Attributes: address, num_rooms

Methods:
__str__: prints the sum of the square footages of all of its rooms

class Room:
Attribute: name, square_footage,
Methods:
Rename（self, old_name, new_name）:
__str__:details of all of its rooms (name, square footage, separated by ',')

class House(Building):
Attribute: at most 10 rooms
Methods:
__str__: prints "Welcome to our house", and the details of all of its rooms (name, square footage, separated by ',')
this print method should also be written in class room for every room's details
and give this part to the class room and just call the method from class room 

class Business:
attributes: have any number of rooms， but no room may be named Bedroom, or have a square footage of less than 100
method:
change size(self, room_name, new_sq_ft): can change the square footage of their rooms

'''
class building():

    def __init__(self, addr, num):
        self.address = addr
        self.num = num
        self.rooms = [] #里面的每一个东西都是一个已经创建好的room instance，他们都有各自的属性和method


    def __str__(self):
        n = 0

        for r in self.rooms:
            n += r.sq#the attribute 'sq' for every room instance

        return 'The sum of all the room is ' + str(n)

    #这些都是题目没告诉你的隐藏的method
    def add_room(self, name, sq):
        if len(self.rooms) == self.num:
            return
        
        r = room(name, sq)#先要建立room才能把room添加到room list里
        self.rooms.append(r)

    #注意class building里的rename和class room里的rename
    def rename(self, old_name, new_name):        
            if r.get_name() == old_name: #find the room you want to change name
                r.rename(new_name) #这是class room里的rename,
                #每个room instance可以call他自己的method去rename， 剩下的事就交给room里的rename去做了
                return

    ##        for r in self.rooms:
    ##            if r.name == old_name:
    ##                r.name = new_name 
    ##                return
    ##最好不要这样直接在另一个class里改其他class的属性，
    ##最好是写个那个class的function交给那个class去handle他自己的part
    ##（call他自己的function让他自己去改他自己的属性）

            

class house(building):

    def __init__(self, addr, num):
        if num > 10:
            num = 10

        super().__init__(addr, num)#只需要判断room nums是不是小于10， 其他东西都跟继承的building一样

#注意class house里的__str__和class room里的__str__
    def __str__(self):
        s = "Welcome to our house\n"
        for r in self.rooms:
            s += str(r) + '\n' #这里的str(r)就相当于是call了class room里的__str__method，直接print出每个room的信息

        return s
    

class business(building):

    #"no room may be named Bedroom" or "have a square footage of less than 100"
    #这两个属性都是关于room的属性，又因为只有business的room有这些属性，
    #所以只在class business里的add room这个method里做改变和判断
    #只有满足条件的room才会被加到business的room list里

    def add_room(self, name, sq):
        if name == 'Bedroom' or sq < 100:
            return
        
        super().add_room(name, sq)#沿用，call父亲的method


#注意class business里的change size和class room里的change size
    def change_size(self, name, new_sq):
        for r in self.rooms:
            if r.get_name() == name:#注意get name这个method的用法，虽然是个很简单的function,但就比直接r.name好
                r.change_size(new_sq)
                return

##        for r in self.rooms: #这是直接在这个class里改了另一个class的属性
##            if r.name == name:
##                r.sq = new_sq
##                return

class room():
    def __init__(self, name, sq):
        self.name = name
        self.sq = sq

    #注意class house里的__str__和class room里的__str__
    def __str__(self):
        return self.name + ',' + str(self.sq) #return的东西是个string，所有东西都要string化


    def get_name(self):
        return self.name

    #注意class building里的rename和class room里的rename
    def rename(self, new_name):
        self.name = new_name

    #注意class business里的change size和class room里的change size
    def change_size(self, new_sq):
        self.sq = new_sq


if __name__ == "__main__": #注意main的写法，也要会独立写出完整的__main__function
    print('=======choice building type=======')
    #to get a valid building type
    prompt = 'input a building type: '
    menu = 'type: "building", "house", "business"'
    print(menu)
    b_type = input(prompt)
    while b_type not in ["building", "house", "business"]:
        print('wrong type! input again!!!\n')
        print(menu)
        b_type = input(prompt)

    print('\n')

    
    print('=======input building info=======')
    #to get a valid building address and number of rooms of the buuilding 
    prompt = 'input address and room number[separated by comma]: '#address may contain space
    info = input(prompt)
    info = info.split(',')
    while True:
        if len(info) != 2 or not info[1].isdigit():
            print('wrong parameter!!! input again!\n')
            info = input(prompt)
            info = info.split(',')

        elif b_type == 'house' and int(info[1]) > 10:#only house has special requirement, so we only check house
            print('A house is a type of building with at most 10 rooms!\n')
            info = input(prompt)
            info = info.split(',')

        else:#如果没进到else（input都满足要求），就一直loop，进到了else了，loop才break
            addr = info[0]
            num = int(info[1])
            break

    print('\n')


    print('=======input room info=======')
    #using the number of rooms of the building to get all the info of all the rooms as a list
    n = 0
    rooms_info = [] #把所有room的信息都一次性收集齐，之后再用loop全部加到building的room list里去
    while n < num:
        prompt = 'input ' + str(n) + ' room name and square footage[separated by space]: '
        info = input(prompt)
        info = info.split()
        while True:
            if len(info) != 2 or not info[1].isdigit():
                print('wrong parameter!!! input again!\n')
                info = input(prompt)
                info = info.split()

            elif b_type == 'business' and (info[0] == 'Bedroom' or int(info[1]) < 100):
                print('No room may be named Bedroom or have a square footage of less than 100.')
                info = input(prompt)
                info = info.split()

            else:
                rooms_info.append((info[0], int(info[1])))#every rooms's info is appended in a list as a (tuple)
                print('room '+ str(n) + ' created.\n')
                break #for the inner loop
        n += 1 #for the outter loop


    #using all the info we collected so far (num_rooms, address, room list) to create a building!!!!
    if b_type == 'building':
        b = building(addr, num)

    elif b_type == 'house':
        b = house(addr, num)

    else:
        b = business(addr, num)

    for r_info in rooms_info:#把所有room的信息都一次性收集齐，之后再用loop全部加到building的room list里去
        b.add_room(r_info[0], r_info[1])


    print('\nbuilding info: ')
    print(b)
