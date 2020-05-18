import turtle

d = input("Do you want to move right or left? ")
n = int(input("How far do you want to move? "))

'''
Homework Exercise
Due: Tuesday 5pm

Write the code so that this happens:

- if the user said d should be right,
  move the turtle to the right by n

- if the user said d should be left,
  move the turtle to the left by n
  
'''

my_turtle = turtle.Turtle()

# YOUR CODE GOES BELOW
# If you don't manage to figure out the correct answer, but
# reach some sort of partial solution, or just any sort of attempt,
# please include that, and explain your thinking process, as comments like this.



import turtle
window = turtle.Screen()
my_turtle = turtle.Turtle() #creating a new turtle

d = input("Do you want to move right or left?")#if user only input left or right
n = int(input("How far do you want to move?"))

if d == "right":
  my_turtle.forward(n)
else:
  my_turtle.backward(n)


