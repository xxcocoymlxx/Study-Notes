from stack import *
import os


class ToDoList:

    def __init__(self):
        self.tasks = []#list of tasks, keeps track of tasks in order of adding
        self.priority = {}#priorities as keys and tasks as values
        #many tasks may have the same priority, {3:(a,b)}
        self.task_info = {} #tasks as keys and (priority,index) as values
        #{a:(3,0), b:(3,1)} the 1st parameter is the priority
        #the 2nd parameter is the task's index in the priority dictionary
        #only adding and storing info into this dict, never deleting

    def __len__(self):
        return len(self.tasks)

    def __str__(self):
        acc =''
        for i in range(len(self)):
            acc += str(i+1) + ':{}\n'.format(self.tasks[i])
        return acc
    
    
    def delete_task(self,num=0): #deleted the error check here
        '''int->str
            Delete an existing task and its priority by the given index
            in the priority dict and also self.tasks.
            *careful: task can only be deleted by the number of task
            under 'view' mode insdead of the 'view ordered' mode.'''
        #all the errors are gonna be caught by the try block in __main__
        self.del_priority(num)
        return self.tasks.pop(num)


    def add_task(self,task):
        self.tasks.append(task)
        

    def insert_task(self, task, i):
        '''
        str->int
        This is only for undo and redo where all the info of a task is already stored in the task_info dict.
        '''
        self.tasks.insert(i,task) #add task back into the tasks list
        
        p = self.task_info[task][0] #get the priority stored in the task_info dict
        index = self.task_info[task][1] #get the index of task in priority dict that's stored in the task_info
        
        self.set_priority(task, p, index)#insert the task back


    def set_priority(self, task, p, index=None):
        '''str, int, int -> None
        Adding a task and its priority into the priority dict and task_info dict with 3 different situations.
        #store info in priority dict as {priority:[tasks]}
        #store info in task_info dict as {task:(priority, index of task in priority dict)}
        '''
        if p not in self.priority:
            self.priority[p] = [task]#if there's no priority meaning there's no such task
            self.task_info[task] = (p, 0)#adding a new task into a task_info with index 0
            
        elif index == None:#if p is already in self.priority and index == None
            self.priority[p].append(task)
            self.task_info[task] = (p, len(self.priority[p])-1)
            
        else:#if p is already in self.priority and there is a index (meaning it's already in task_info)
            self.priority[p].insert(index, task)

            

    def del_priority(self, num):
        '''
        int->NoneType
        Given a index of task, delete the proirity of the task.
        No need to delete the task in self.tasks, that's another method
        '''
        task = self.tasks[num]  #given the index,find the task

        priority = self.task_info[task][0]   #given the task, find the priority     
        
        self.priority[priority].remove(task)    #a task list, remove the task from priority dict

        if self.priority[priority] == []:   #if there are no more tasks of a particular priority
            #simply remove the priority in the priority dict
            self.priority.pop(priority)#dictionary can also use pop to delete the key:value pair


    def get_priority_list(self):
        '''ToDoList->NoneType
            Return a list of tasks according to their priority from highest to lowest.
            Used when the user chooses option "vo".
            '''

        all_priority = list(self.priority.keys())
        all_priority.sort()#from lowest to highest
        all_priority.reverse()  #get all priority from highest to lowest

        priority_list = []
        for p in all_priority:
            for task in self.priority[p]:
                priority_list.append(task)

        return priority_list


    def save(self,filename): 
        '''
        str->NoneType
        Save the current temporary to do list into a file with format of "task p index".
        '''
        if filename == None:
            filename = input('Please enter your filename as "filename.txt": ')
            
            while not filename.endswith('.txt'):#checking validity of filename
                print("invalid filename! Don't forget to add '.txt' at the end.")
                filename = input('Please enter your filename as "filename.txt": ')
                
        f = open(filename, 'w')

        try:
            for task in self.tasks:
                
                p = self.task_info[task][0]
                index = self.task_info[task][1]
                
                info = '{} {} {}\n'.format(task, p, index)
                f.write(info)
            
            
        except Exception as e:
            print(e)
            print('file did not saved successfully...\n')
        else:
            print('file saved successfully!\n')
        finally:
            f.close()

        

    def load(self, filename):
        '''file->NoneType
            Open, read and load an existing file of to do list that have
            a format of "task p index" into the to do list.'''
        
        f = open(filename, 'r')

        try:
            for line in f:
                info = line.split()
                #assume the file will have a format of "task p index"
                self.add_task(info[0])
                self.set_priority(info[0], int(info[1]), int(info[2]))

        except Exception as e:
            print(e)
            print('file did not load successfully...\n')
        else:
            print('file loaded successfully!\n')
        finally:
            f.close()

######################################################################all the methods for class ToDoList finishes here      

def get_all_txt():
    '''Get all the txt files in the current folder.'''
    l=os.listdir()#all the files in the CURRENT FOLDER
    txt_files = []
    for filename in l:
        if filename.endswith('.txt'):
            txt_files.append(filename)

    return txt_files


def print_menu():
    print("-------------------------------------")
    print("At any point, you may type: \n" \
                "'v' to view whole list \n" \
                "'vo' to view whole list by priority order \n"\
                "'d' to delete an existing item by type in the number of task in 'v' mode \n" \
                "'u' to undo what you just added \n"
                "'r' to redo what you previously undid \n"\
                "'s' to save the current to-do-list to a file \n"\
                "'q' to quit the system")
    print("-------------------------------------")


####################################################################################### Main code starts here


print("Welcome to your temporary To Do List\n")


filename = None
commands = Stack()
todolist = ToDoList()


order = input('Do you want to load your to-do-list from an existing file [Y/N]: ')
while order.upper() not in 'YN':
    print('invalid input! Please re-enter...')
    order = input('Do you want to load your to-do-list from an existing file [Y/N]: ')
    
if order.upper() == 'Y':
    all_txt = get_all_txt()
    if all_txt == []:
        print('Sorry, cound not find any existing files...')
    else:
        print('All the existing files: ')
        for filename in all_txt:
            print('    ' + filename)

        filename = input('\nChoose a file to load (format:filename.txt): ')
        while filename not in all_txt:
            print("invalid filename. Please re-enter.")
            filename = input('\nChoose a file to load (format:filename.txt): ')

        todolist.load(filename)


while True:
    print_menu()
    c = input("What is something you need to get done? (format: task,priority) \n")
    
    if (c == 'v'):#v stands for view
        print(todolist)


    elif (c == 'vo'):#vo stands for view ordered
        priority_list = todolist.get_priority_list()#todolist is an instance of class ToDoList and ths instance is using its method
        s = ''
        for i in range(len(priority_list)):
            s += str(i+1) + ':{}\n'.format(priority_list[i])
        print(s)
        
        
    elif (c == 'd'):#d stands for delete
        try:
            num = int(input("Which task do you want to delete? Enter the number under 'view' mode."))
            commands.push(('delete', todolist.delete_task(num-1), num-1))#commands was appended in a tuple
            redos = Stack()
            print(todolist)
        except Exception:
            print('The index is invalid. Please re-enter.')


    elif (c == 'u'):#u stands for undo
        if commands.isEmpty():
            print('Undo operation is not possible at this point.')
        else:
            key = commands.pop()

            if key[0] == 'delete':
                todolist.insert_task(key[1],key[2]) 
                
            elif key[0] == 'insert':
                todolist.delete_task(key[2])

            redos.push(key) #record the original command (what just undid)
            
                
    elif (c == 'r'):#r stands for redo
        if redos.isEmpty():
            print('Redo operation is not possible at this point.')
        else:
            key = redos.pop()# original order

            if key[0] == 'insert':
                todolist.insert_task(key[1],key[2])
                
            elif key[0] == 'delete':
                todolist.delete_task(key[2])

            commands.push(key)


    elif (c == 's'):#s stands for save
        todolist.save(filename)
        
    elif (c == 'q'):#q stands for quit
        print('\n to do list closed \n')
        break

    elif (len(c.split(',')) != 2) or (not c.split(',')[-1].isdigit()):#check if the input is valid
        print('invalid format! Please re-enter as task,priority')
        
    else:
        task = c.split(',')[0]
        p = int(c.split(',')[1])
        print('task added!')
        #when adding a task, add it into the self.tasks and priority dict (and task_info dict)
        todolist.add_task(task) #store in self.tasks according to order of adding
        todolist.set_priority(task, p) #store in priority dict according to their priority
        #for adding new tasks, set_priority will only has two parameters, the index will be the default value None
        
        commands.push(('insert', task, len(todolist)-1)) #record every command in stack commands 
        redos = Stack()
