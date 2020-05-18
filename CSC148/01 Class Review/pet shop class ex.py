'''

PetShop
attributes:
    animals: list of Animals
methods:
    pass

Animal
attributes:
    name: str
    age: int
methods:
    eat
    sleep
   
Cat -> inherits from Animal
attributes:
methods:
    meow
    purr
    
Dog -> inherits from Animal
attributes:
methods:
    bark
    rollover

Bird -> inherits from Animal
attributes:
methods:
    fly
'''

class PetShop:

    def __init__(self, animals=[]):
        self.animals = animals

    # try running these methods to see how they work
    def feed_all(self):
        for animal in self.animals:
            animal.eat()

    def sleep_all(self):
        for animal in self.animals:
            animal.sleep()

    def fly_all(self):
        for animal in self.animals:
            animal.fly()
        # this method will give an error because not
        #    all animals can fly
        # this will only work if all animals in self.animals
        #    is a Bird
        
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def eat(self):
        print(self.name + " is eating.")

    def sleep(self):
        print(self.name + " is sleeping.")

class Cat(Animal):

    def __init__(self, name, age, color):
        # A subclass can also have its own attributes
        # Here, we let Cat class have a 'color' attribute
        # But now, we need to call the superclass constructor
        # explicitly, to handle the superclass attributes
        super().__init__(name, age) # this is how we call a method from the superclass
        self.color = color

        # NOTE: above, super().__init__(name, age) is the same as calling Animal.__init__(self, name, age)

    # If I define an "eat" method for Cat class, this
    # will OVERRIDE the one defined by the Animal class
    def eat(self):
        print(self.name + " eats like a cat.")
        
    def meow(self):
        print(self.name + " says meow.")

    def purr(self):
        print(self.name + " purrs.")

class Dog(Animal):

    # The constructor is already being inherited
    # So, no need to put any __init__ here
    # I only need a constructor if I have specific, extra attributes for the subclass
    # which the superclass does not have
    # The following is ALREADY done for you if you do Dog(Animal), so
    # although it would work, it's redundant:
    #def __init__(self, name, age):
    #   super().__init__(name, age)
        
    def bark(self):
        print(self.name + " barks.")

    def roll_over(self):
        print(self.name + " rolls over.")

class Bird(Animal):

    def fly(self):
        print(self.name + " flies.")

# Using the above classes:
c1 = Cat("Kyoko", 5, "calico")
c1.eat()
# Whenever I call a method, it's going to check this subclass first
# e.g. If Cat has an 'eat' method, it's going to use Cat's method
#      If it can't find an 'eat' method in Cat, it's going to search the superclass Animal and use that

p = PetShop([Cat("Simba",5,"orange"), Dog("Sporty",7)])
p.feed_all()
        
