class Animal:
    def __init__(self, name, sound):
        '''
        (Animal, str, str) -> None
        Construct an animal with the given name, and of the given species.
        '''
        self.name = name # e.g. a string like "Fido", "Rover", etc.
        self.sound = sound # e.g. a string like "meow", "woof", etc.
        
    def say_hello(self, other):
        print("{} says {} to {}".format(self.name, self.sound, other.name))

class Cat(Animal):

    def __init__(self, name):
        super().__init__(name, "meow")

class Dog(Animal):

    def __init__(self, name):
        super().__init__(name, "woof")
        
class PetOwner:

    def __init__(self, name, id_num, animal):
        self.name = name
        self.id_num = id_num
        self.pet = animal

    def is_cat_owner(self):
        '''
        Return True iff this pet owner's pet is a cat.
        '''
        return isinstance(self.pet, Cat)

        
    def greet_other_pet(self, other):
        '''
        (PetOwner, PetOwner)
        Have this owner's pet say hello to the other owner's pet.
        '''
        self.pet.say_hello(other.pet)
