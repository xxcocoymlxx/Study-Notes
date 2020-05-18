# open file & read file & write file
# ==================================
# VERSION1 Open File and Read format
f = open(filename, 'r') # r can be ignored
lst = readlines() # [ first line, second line, third line...]
for item in lst:
    ....
    ....
    # do operation
    # strip().split()

# VERSION2 Open File and Read format
f = open(filename, 'r')
line = f.readline()
while line != '':
    ....
    ....
    # do operation
    # line.strip().split()
    line = f.readline()


# VERSION3 Open File and Write format (w mode overwrite)
f = open(filename, 'w') # this will delete all content in a file, and write it
f.write(...) # put what you want to write in ...
f.close () # must close, this means save the changes

# VERSION4 Open File and Append format (a mode append)
f = open(filename, 'a') # This will append your stuff to the end of a file
f.write(...)
f.close()
