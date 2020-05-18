from stack import *

class ToDoList:

    def __init__(self):
        self.tasks = []

    # ADD IN METHODS HERE ACCORDING TO INSTRUCTIONS #
    def __len__(self):
        return len(self.tasks)
    
    def __str__(self):
        acc =''
        for i in range(len(self.tasks)):
            acc += str(i+1) + ':{}\n'.format(self.tasks[i])
        return acc

    def is_empty(self):
        return self.tasks == []
    
    def delete_task(self,num=0):
        return self.tasks.pop(num)
    
    def add_task(self,c):
        self.tasks.append(c)

class EmptyStackError(Exception):
        """An exception raised when attempting to pop items from an empty stack.
    """
        pass


commands = Stack()#to record every command made
todolist = ToDoList()#an empty list

def print_menu():
    print("-------------------------------------")
    print("At any point, you may type: \n" \
                "'v' to view whole list \n" \
                "'d' to delete an existing item \n" \
                "'u' to undo what you just added \n"
                "'r' to redo what you previously undid")
    print("-------------------------------------")
    #there is no 'a' for adding tasks because the user is already asked what need to get done

print("Welcome to your temporary To Do List\n")

while True:
    print_menu()
    c = input("What is something you need to get done? \n")
    if (c == 'v'):#v stands for view
        print(todolist)
        
    elif (c == 'd'):#d stands for delete
        # MODIFY THIS ACCORDING TO INSTRUCTIONS #
        try:
            num = int(input("Delete which task?"))
            commands.push(('delete', todolist.delete_task(num-1), num-1))
            #a tuple that contains the information was appended into commands
            #(command, the task deleted(while deleting the task), index of the task)
            redos = Stack()#after deleting the task, the redos is refreshed!
            print(todolist)#print the todolist after deleting the task
        except Exception:#if the index is invalid
            print('The index is invalid. Please re-enter.')


        
    elif (c == 'u'):#u stands for undo
        #commands is for undos only, keep track of 'delete' , 'add task' and 'redo' only
        #if (c == 'u'), pop the last action in the commands and do the REVERSE ACTION!
        if commands.isEmpty():########## the program should not crash
            print('Undo operation is not possible at this point.')
        else:
            key = commands.pop()#to get the last action made while deleting the action in the commands
            
            if key[0] == 'delete':
                todolist.tasks.insert(key[2],key[1])
                
            elif key[0] == 'insert':
                todolist.delete_task(key[2])

            redos.push(key) #save original order
            #now we have undid something, we have to record it in the 'redos'
            #'redos' only record the action we undid
            #if we add or delete another task, 'redos' gets refreshed!


                
    elif (c == 'r'):#r stands for redo
        if redos.isEmpty():###########program should not crash
            print('Redo operation is not possible at this point.')
        else:
            
            key = redos.pop()# original order

            if key[0] == 'insert':
                todolist.tasks.insert(key[2],key[1])
                
            elif key[0] == 'delete':
                todolist.delete_task(key[2])#key[2] is the task's index

            commands.push(key)#record the redo command TOO
            #if we delete a task, the 'delete' action is stored in commands
            #we undo it, it gets inserted back, and the action is removed from commands
            #and stored in the 'redos', everything we undid will be stored in the 'redos'
            #if we wanna redo it (here the 'deletion'),we just delete again! (so NO reverse action!)
                
    else:
        todolist.add_task(c)
        commands.push(('insert', c, len(todolist)-1))#record the task added
        redos = Stack()#redos is refreshed after adding a new task, b/c redos are only related to undos
        #the stack 'redos' only stores the commands that have been UNDID
