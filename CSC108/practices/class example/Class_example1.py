class Monster:
    def __init__(self, HP, AP, sex: # magic method
        self.HP = HP
        self.AP = AP
        self.sex = sex   #constant variables
        self.armour_set = []

    def attack(self, AP, other, HP_cost):
        if (other.HP >= HP_cost):
                
    

    def demage(self, HP, HP_cost):
        if self.HP > 0:
            self.HP -= HP_cost
        else:
            print("You are dead")

    def __str__(self):
        return "This is hero1 named Gary"

    def __repr__(self):
        return "This is demonstration for repr for hero1 named gary"
