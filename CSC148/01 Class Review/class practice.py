'''
#############################################################################################################
##Be able to write all three class questions incliding the __main__ function. Practice! Practice! Practice!##
#############################################################################################################
Question 1
Write one or more classes for the following specification. Begin by carrying out an object-oriented
analysis to determine the classes, methods, attributes, and interactions.
Context: An airline reservation system
3 main classes:
供给端:seats(economy & business)
需求端:passenger
控制台:ReserveSys
Each seat on a plane is classified as business class or economy, and has a unique name (like
“17C”). Passengers have booking IDs (a mix of letters and numbers). When they book a seat, they
request their preferred class (business or economy) and are given any seat in that class. If the chosen
class is full, then their booking is unsuccessful. This airline gives passengers no choice about their
specific seat. We want to be able to report on how full a flight is: the percentage of seats that are
booked in economy, in business class, and overall.
'''
#should have writen these two classes as a whole class named Seat
class Business():
    def __init__(self,num, seats):
        self.num = num #total number of seats 
        self.seats = seats#list of seats

    def percentage(self):#seats booked %
        return (1 - len(self.seats)/self.num)*100 ##不在这里写string representation，在main里才写

    def book_seat(self):
        if self.seats != []:
            return self.seats.pop(0)
        
        else:
            print('Booking is unsuccessful. All the seats are full. Choose another class.')
            return None

class Economy(Business):
    pass

        
class Passenger:
    def __init__(self,ID, seat_type, seat):
        self.ID = ID
        self.t = seat_type
        self.seat = seat
        
    def __str__(self):
        s = 'Passenger: {}\nClass: {}\nSeat: {}\n'.format(self.ID, self.t, self.seat)
        return s
        
class ReserveSys(): #big class that stores all the information
    def __init__(self, seatsList_e, seatsList_b, eco_seat_num, business_seat_num):
        self.passengerList = []
        self.economy = Economy(eco_seat_num, seatsList_e)
        self.business = Business(business_seat_num, seatsList_b)
        #在这里就创建好了两个舱型的座位信息

    def book_seat(self, c, ID):
        if c == 'business':
            seat = self.business.book_seat() #self.business这个instance去book seat
            if seat != None:
                passenger = Passenger(ID, c, seat)#在这里才创建passenger,相当于这个passenger才上了飞机
                self.passengerList.append(passenger)
                print('successful\n')
                print(passenger)
                
        else:
            seat = self.economy.book_seat()
            if seat != None:#seat class里的book seat method，若seat满了，return None
                passenger = Passenger(ID, c, seat)
                self.passengerList.append(passenger)
                print('Booking successful!\n')
                print(passenger)#__str__应该是在passenger里写成个method的，不应该在ReserveSys里hard code文字进去
            

    def how_full(self, c):
        if c == 'business':
            return self.business.percentage()
        
        return self.economy.percentage()
        

    def how_full_overall(self):
        return len(self.passengerList)/(self.business.num + self.economy.num)
        

if __name__ == '__main__':
    plane1 = ReserveSys(['1E','2E','3E'],['1B','2B','3B'], 3, 3)

    menu = '"b" to book a seat\n' + \
           '"ce" to check economy capacity\n' + \
           '"cb" to check business capacity\n' + \
           '"c" to check the plane capacity\n' + \
           '"q" to quit the system'

    print(menu)
    order = input('Input an order: ')
##    while order not in ['b','ce','cb','c','q']:
##        print('invalid input, please re-enter again.')
##        order = input('Input an order: ')
#在main里的最后一个else有包裹invalid input,这里不用check

    
    while order != 'q':
        if order == 'b':
            c = input('Do you want to book seat from business class or economy class? ')
            while c not in ['business','economy']:
                print('Invalid Class, please re-enter again.')
                c = input('Do you want to book seat from business class or economy class? ')

            ID = input('Input your Booking ID [a mix of letters and numbers]: ')
            while not ID.isalnum():#alnum()的用法！
                print('Invalid ID')
                ID = input('Input your Booking ID [a mix of letters and numbers]: ')

            plane1.book_seat(c,ID)

        elif order == 'ce':
            p = plane1.how_full('economy')
            print('The economy capacity is: {}'.format(p))
        elif order == 'cb':
            p = plane1.how_full('business')
            print('The business capacity is: {}'.format(p))
        elif order == 'c':
            p = plane1.how_full_overall()
            print('The plane capacity is: {}'.format(p))
        else:
            print('Invalid order! input again.....')

        print(menu)
        order = input('Input an order: ')
    


'''
Question 2
Write one or more classes for the following specification. Begin by carrying out an object-oriented
analysis to determine the classes, methods, attributes, and interactions.
Context: an inventory system
3 main classes:
供给端:items
需求端: None
控制台:InventorySys
Items are for sale, each at its own price. Items are identified by their item number, and they also
have a text description, such as “bath towel”. There are categories that items belong to, such as
“housewares” and “books”. We need to be able to print a suitable price tag for an item (you can decide
exactly the format). Sometimes an item is discounted by a certain percentage. We need to be able to
compare two items to see which is cheaper.
'''
class InventorySys:
    def __init__(self,goods=[]):

        self.inventory = {}

        for good in goods:
            self.inventory[good.number] = good

    def sold(self,num):
        g = self.inventory.pop(num)
        print(g)
        print('item sold')

    def show(self):
            s = ''
            for num in self.inventory:
                s += '{}: {}\n'.format(num, str(self.inventory[num]))
            print(s)

    def discount(self, num, p):
        good = self.inventory[num]

        new = good.price*p
        good.change_price(new)


    def compare(self, n1,n2):
        g1 = self.inventory[n1]
        g2 = self.inventory[n2]

        if g1 > g2:
            return g2
        elif g2 > g1:
            return g1
        else:
            return None

    
class items:
    def __init__(self, number, description, category, price):
        self.number = number
        self.description = description
        self.category = category
        self.price = price

    def __str__(self):
        return 'Item {} is worth {} dollars.'.format(self.number, self.price)


    def discount(self, discount):
        self.price = self.price*discount


    def cheaper(self, item1,item2):
        if item1.price < item2.price:
            return item1.number
        elif item1.price > item2.price:
            return item2.number
        else:
            return 'Both items are same price.'


    def change_price(self, new):
        self.price = new

    def __gt__(self, other):
        return self.price > other.price


                  
if __name__ == '__main__':
    
    g1 = items(2001,'notebook','book',10)
    g2 = items(2002,'mark pen','pen',15)
    g3 = items(2003,'newbook','book',12)

    goods = [g1,g2,g3]

    s = InventorySys(goods)

    menu = 'show\nsold\ndiscount\ncompare\nquit'

    print(menu)
    order = input('input an order: ')

    while order != 'quit':
        if order == 'show':
            s.show()

        elif order == 'sold':
            num = int(input('good num: '))
            s.sold(num)

        elif order == 'discount':
            num = int(input('good num: '))
            p = float(input('discount: '))
            s.discount(num,p)

        elif order == 'compare':
            n1 = int(input('good1 num: '))
            n2 = int(input('good2 num: '))

            g = s.compare(n1, n2)

            if g == None:
                print('same price')

            else:
                print(g)
            
        print('------------------\n')
        print(menu)
        order = input('input an order: ')




'''
Q3
A To Do List has a name (an arbitrary string), and a list of tasks, provided when the list is created.
New tasks can be added to the To Do List, but the total number of tasks in the list must be 50 or less.
Attempting to add more than 50 tasks to a list should raise the TaskOverloadError.
Each task has a date, month and year, provided when the task is created.
The date must be an integer between 1 and 31, the month must be an integer between 1 and 12,
and the year must be 2016 or greater. An invalid date, month or year should raise the InvalidDateError
A task also has details about the task in the format of a string (e.g. "date with Jane"),
provided when the task is created.

Write code to perform the following:
Create a To Do List named "School" with an empty list of tasks
Prompt the user for a date
Prompt the user for a month
Create a task for "Ace CSC108 test" using the given date, month and 2018 as the year, and add the task to the to do list that was created
If this raises an InvalidDateError, print "invalid date"
If this raises a TaskOverloadError, print "too many tasks"

'''
class ToDoList:
    def __init__(self,name, tasklist=[]):
        self.name = name
        self.tasklist = tasklist

    def add_task(self,task):
        if len(self.tasklist) == 50:
            raise TaskOverloadError
        #('To do list is full. Cannot add new task.') 不在这里加,main里得接住这个error然后才print这句话
        else:
            self.tasklist.append(task)
    
                  
class Task:
    def __init__(self, date, month, year, task):
        if not (1 <= date <= 31) or not (1 <= month <= 12) or year < 2016:
            raise InvalidDateError
        #else:
        self.date = date
        self.month = month
        self.year = year
        self.task = task

              
class TaskOverloadError(Exception):
    print('too many tasks')
    

class InvalidDateError(Exception):
    print('invalid data')

    
if __name__ == '__main__':
    school = ToDoList('School') #with empty task list
    
    date = input('Please enter a date.')
    while not date.isdigit():
        print('Invalid date! Please enter again.')
        date = input('Please enter a date.')
##WRONG!!    while date is not <=1 and date is not <= 31:
##        raise InvalidDateError("invalid date")
    
     month = input('Please enter a month.')
    while not month.isdigit():
        print('Invalid month! Please enter again.')
        date = input('Please enter a month.')

    try:
        task = Task(int(d),int(m),2016,'Ace CSC148 test')
        school.add_task(task)
