
class ID():
    def __init__(self, name, gender, age, num = None):
        self.name = name
        self.g = gender
        self.age = age
        self.addr = ''
        self.no = num

    def change_address(self, new_addr):
        self.addr = new_addr

    def set_number(self, number):
        self.no = number


    def __len__(self):
        return 0

    def __lt__(self, other):
        pass

    def __gt__(self, other):
        return self.age > other.age

    def __eq__(self, other):
        return True

    def __ge__(self, other):
        pass

    def __str__(self):
        
        s = "Name: {}     Gender: {}\nAge: {}      N.O: {}\nAddr: {}"
        return s.format(self.name, self.g, self.age, self.no, self.addr)

    def __repr__(self):
        return 'hahahahah'

    def __add__(self,other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass



#########################################################################



class A():
    def __init__(self):
        self.a = 'Class A'

    def test(self):
        print('A test')

    def info(self):
        print('Parent Class A')


class B(A):

    def test(self):
        super().test()
        print('B test')

    def t2(self):
        super().test()

    def b(self):
        print('T_T')


class C(B):
    pass



##########################################################################



import random   
class Player():
    def __init__(self, name, gender, occupation):
        #初始化角色信息
        self.name = name
        self.g = gender
        self.occupation = occupation
        self.level = 0
        self.exp = 0
        if occupation == 'warrior': #判断职业
            self.hp = 90
            self.atk = 20
            self.lucky = 15
        elif occupation == 'mage':
            self.hp = 60
            self.atk = 35
            self.lucky = 10

    def combat(self, other): #进行战斗
        hp1 = self.hp
        hp2 = other.hp
        
        while hp1 > 0 and hp2 > 0: #回合攻击
            if hp1 > 0:
                # random.random() 会产生一个0~1的随机数
                d = self.atk + self.lucky*random.random() #攻击数值浮动
                d = round(d)
                print(self.name, 'atk',d)
                hp2 -= d

            if hp2 > 0:
                d = other.atk + other.lucky*random.random()
                d = round(d, 2)
                print(other.name, 'atk',d)
                hp1 -= d

        if hp1 > 0: #判断胜负
            self.update(other) #升级
            print('\n{} won the combat'.format(self.name))
        else:
            other.update(self)
            print('\n{} won the combat'.format(other.name))
        
                         
    def update(self, other): #升级公式
        self.exp += (other.level +3)*15

        self.level  += self.exp //100
        self.exp = self.exp%100
            
    def __str__(self):
        s = "name: {}   occupation: {}   level: {}".format(self.name, \
                                self.occupation, self.level)
        return s        
    


#############################################################################



class UTStudent():
    def __init__(self, name, campus, no):
        self.name = name
        self.campus = campus
        self.n = no
        self.timetable = {}
        self.friend =[]

    def __str__(self):
        s = 'name: {}   campus: {}   NO: {}\n'.format(self.name, \
                                                      self.campus, self.n)
        s  += 'Timetable: \n'

        for day in self.timetable:
            s += '{}:  {}\n'.format(day, self.timetable[day])
        return  s

    def add_course(self, day, course):

        if day in self.timetable:
            self.timetable[day].append(course)

        else:
            self.timetable[day] = [course]
        
    def del_course(self, course):
        for day in self.timetable:
            if course in self.timetable[day]:
                self.timetable[day].remove(course)
                










