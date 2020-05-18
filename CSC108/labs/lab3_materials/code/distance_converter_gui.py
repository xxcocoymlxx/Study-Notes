# Michelle Craig
# July 6, 2012

try:
    import distance_converter
    calculator = True
except ImportError:
    calculator = False
    
from tkinter import *

def functions_implemented():
    '''Do a simple check to see if the required functions are there in the 
       required module. It would have already failed if the module wasn't 
       found and will fail later if the functions have incompatible signatures.
    '''
    return ('km_to_miles' in distance_converter.__dict__) and \
        ('miles_to_km' in distance_converter.__dict__)
    

class Application(Frame):

    def recalculate_miles(self, event):
        miles = distance_converter.km_to_miles(self.km.get())
        self.miles.set(miles)

    def recalculate_kms(self, event):
        kms = distance_converter.miles_to_km(self.miles.get())
        self.km.set(kms)

    def post_message(self):

        QUIT = Button(self)
        QUIT["text"] = "QUIT"
        QUIT["command"] = self.quit
        QUIT.pack()

        message = '''You correctly have a module called distance_converter.py but it
needs to contain both a km_to_miles and miles_to_km function. 

Go back and look at the lab instructions.'''
        message_label = Label(text=message)
        message_label.pack({"padx":10})

    def post_no_calculator(self):

        QUIT = Button(self)
        QUIT["text"] = "QUIT"
        QUIT["command"] = self.quit
        QUIT.pack()

        message = '''You do not have a module called distance_converter.py
required by this graphical calculator.

Go back and look at the lab instructions.'''
        message_label = Label(text=message)
        message_label.pack({"padx":10})

    def create_widgets(self):

        QUIT = Button(self)
        QUIT["text"] = "QUIT"
        QUIT["command"] = self.quit
        QUIT.pack({"side": "top"})

        message = '''Try changing either distance and then press enter.'''
        message_label = Label(text=message)
        message_label.pack({"padx":10})

        km_frame = Frame(self)
        km_label = Label(km_frame, text="kilometers")
        km_label.pack({"side":"left"})
        km_enterbox = Entry(km_frame)
        km_enterbox.pack({"side":"right"})
        self.km = DoubleVar()
        self.km.set(16.0)
        km_enterbox["textvariable"] = self.km
        km_frame.pack()
        km_enterbox.bind('<Key-Return>',
                              self.recalculate_miles)

        mile_frame = Frame(self)
        mile_label = Label(mile_frame, text="miles")
        mile_label.pack({"side":"left"})
        mile_enterbox = Entry(mile_frame)
        mile_enterbox.pack({"side":"right"})
        self.miles = DoubleVar()
        self.miles.set(10.0)
        mile_enterbox["textvariable"] = self.miles
        mile_frame.pack()
        mile_enterbox.bind('<Key-Return>',
                              self.recalculate_kms)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        if calculator and functions_implemented():
            self.create_widgets()
        elif calculator:
            self.post_message()
        else:
            self.post_no_calculator()

root = Tk()
app = Application(master=root)
app.master.title("Simple Graphical Distance Converter")
app.mainloop()
root.destroy()
