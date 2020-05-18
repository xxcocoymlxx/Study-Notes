import turtle
window = turtle.Screen() #creating a window
alex = turtle.Turtle()#creating an object
turtle.color("purple")

hobby = input("Do you want to make a free drawing on turtle?")
shape = input("Do you want to draw a square or triangle?")

if hobby == "yes":
   if shape == "square":
      for i in [0,1,2,3]:
        alex.forward(50)
        alex.left(90)
   elif hobby == triangle:
       print("maybe next time")
else:
    print("okay thats fine")
    
window.mainloop() #keeps the window open
