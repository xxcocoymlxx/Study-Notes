class Actor:
    def __init__(self, HP, AP, sex):
        self.HP = HP
        self.AP = AP
        self.sex = sex 


class Monster(Actor):


    def attack(self,other, AP, HP_cost):
        if (other.HP >= HP_cost):
            other.HP -= HP_cost
            print("Attack Successfully")
            return True
        else:
            print("The actor is dead")
            return False

    def __str__(self):
        return "The actor info: {0}, {1}, {2}".format(self.HP, self.AP, self.sex)
                 
class Hero(Actor):
    def __init__(self, HP, AP, sex, money): # magic method
        super().__init__(HP,AP, sex)   #constant variables
        self.armour_set = []
        self.money = money

    def attack(self, other1, other2, AP, HP_cost):
        if (other1.HP >= HP_cost and other2.HP >= HP_cost):
            other1.HP -= HP_cost
            other2.HP -= HP_cost
            print("Attack Successfully")
            return True
        else:
            print("The actor is dead")
            return False

    
