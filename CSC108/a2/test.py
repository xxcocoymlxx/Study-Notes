'''def load_map(file_name):
    acc = []
    f = open(file_name)
    line = f.readline()
    while line:
        lst = line.strip().split()
        acc.append(lst)
        line = f.readline()
    return acc
'''
'''
def load_map(filename):
    acc= []
    f = open(filename)
    line = f.readline()
    while line:
        lst = line.strip().split()
        acc.append(lst)
        line = f.readline()
    f.close()
    return acc
'''
'''
def load_map_for(filename):
    f = open(filename)
    lines = f.readlines()
    print(lines)

    for item in lines:
        lst = item.strip()
        print(lst)
'''
'''
def load_map(file_name):
    f = open(file_name)
    lst = f.readlines()
    print(lst)
       
    for item in lst:
        new_lst = item.strip().split()
        print(new_lst)
'''
#for loop好像是不用readline的……直接for line in f就好
def load_map(file_name):
    f = open(file_name)
    lst = []
    for line in f:
        lst.append(line.strip().split())
    return lst
