'''

When can I use inheritance?
When some classes are very similar, but one of the classes is a more SPECIFIC type of the other.

e.g.
class Person:

    attributes:
    - a person has a name
    - a person has an age

    methods:
    - a person can talk
    - a person can walk

class Student(Person):

    # A student can do EVERYTHING a Person can, but ALSO:
    
    attributes:
    - a subject post
    - a cgpa
    - a student number
    - an id
    - courses

    methods:
    - a student can add a course
    - they can drop a course

'''

class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def walk(self):
        print("Hi, I'm a person walking")
        
class Student(Person): # the (Person) here makes it so that it is as though I copy-pasted EVERYTHING from Person class into here

    # This constructor is not always necessary
    # because Student inherits Person's constructor.
    # The only time I need a constructor in the subclass is if
    # I want to have EXTRA parameters.
    def __init__(self, name, age, student_number, courses):
        super().__init__(name, age) # same as doing Person.__init__(self, name, age)
        self.student_number = student_number
        self.courses = courses

    # This is a student only method
    # That means, a Person can NOT call it.
    # Any method that the Person has, the student can use, but this is NOT true the other way around.
    def drop_course(self):
        print("Hi I dropped a course")

    # Note:
    # If I had another method here called "walk",
    # then that method would OVERRIDE the one in Person.
    # This means if a student object walked, then this
    # method would get called, and the Person's walk would no longer get called.

# Careful about when to use inheritance
# Review lecture slide about IS-A vs. HAS-A
class Classroom:

    # e.g. a Classroom HAS a lot of students => does NOT mean it IS A student
    # so, inheritance wouldn't make sense here
    # 'cause if I did Classroom(Student) that would mean I want my CLASSROOM
    # to have a name, age, studentnumber, etc. which makes no sense
    
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)
        
# Another example
class Zoo(Animal): # THIS IS WRONG - A Zoo IS NOT an animal just because it HAS animals..
    pass

class Zoo: # THIS IS RIGHT

    def __init__(self):
        self.animals = []  # list of Animals

     
