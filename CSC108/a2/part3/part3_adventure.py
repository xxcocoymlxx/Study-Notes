import random
#1
def load_map(filename):
    '''
    (str) -> list of lists
    
    Read data from the file with the given filename
    and return it as a nested list of strings.

    e.g. if the file had a map like this:
            1 2 5
            3 -1 4
         this function would return [['1','2','5'], ['3','-1','4']]
        
    The given 'filename' is a string that gives name of text file
    in which map data is located. Remember, you have to open the
    file with this filename first before you can read it.
    '''
    acc= []
    f = open(filename)
    line = f.readline()
    while line:
        lst = line.strip().split()
        acc.append(lst)
        line = f.readline()
    f.close()
    return acc


def mapfile_hight(filename):
    f = open(filename)
    acc = 0
    line = f.readline()
    while line != '':
        acc += 1
        line = f.readline()
    return acc

def mapfile_width(filename):
    f = open(filename)
    acc = 0
    lst = f.readline().strip().split()
    for item in lst:
        if item != '':
            acc += 1
    return acc

#2   done
def generate_map(map_data, p_x, p_y, player_id):
    '''
    (list of lists, int, int, str) -> list of lists, dict
    
    Given a list of lists representing map data, generate
    and return the following:
    (1) a list of lists that provides a visual representation
    of the map, and
    (2) a dictionary where the keys are tuples of two ints that are
    (x, y) coordinates, and the associated values are the int location
    ids that are at that position.

    In the visual representation, each blank space should be
    (_), every blocked area (represented as -2 in the map data)
    should be (x), and the player's location at (p_x, p_y) should be
    (*) where * is actually the player's id.
    
    e.g.
    if the player_id was the letter 's' and
    if the original map file had a map like this:
            1 2 -2
            3 -1 4
    the map data would be [['1','2','-2'], ['3','-1','4']]
    and its visual representation would be:
    [['(s)','(_)','(x)'],['(_)','(_)','(_)']]
    and the coordinates dictionary would be:
    {(0, 0): 1, (0, 1): 3, (1, 0): 2, (1, 1): -1, (2, 0): -2, (2, 1): 4}
    '''
    map_visual = []
    map_coors = {}
    for i in range(len(map_data)):
        map_visual.append([])
        for i2 in range(len(map_data[i])):
            if map_data[i][i2] == '-2':
                map_visual[i].append('(x)')              
            else:
                map_visual[i].append('(_)')

    map_visual[p_y][p_x] = '(' +player_id +')'
            
            
    for index in range(len(map_data)):
        for ind in range(len(map_data[0])):
            key = (ind,index)
            map_coors[key] = float(map_data[index][ind])
 
    return map_visual, map_coors


#3  done!!!!!!
def load_items(filename):
    '''
    (str) -> dict

    Read data from the file with the given filename and
    create and return a dictionary with item data, structured
    as described in the assignment handout, Part 2 Section III.
    '''
    acc= {}
    f = open(filename)
    line = f.readline()
    while line:
        lst = line.strip().split(',')
        acc[lst[0]] = lst[1:]
        line = f.readline()
    f.close()
    return acc
    

#4  done!!!!!!!!
def load_locations(filename):
    '''
    (str) -> dict

    Read data from the file with the given filename and create
    and return a dictionary with location data, structured as
    described in the assignment handout, Part 2 Section III.
    '''
    Dict = {}
    f = open(filename)
    line = f.readline().strip()# output is 0
    new_key = float(line) #new_key = 0
    line = f.readline() #begin description
    while line:
        line = line.strip('\n')
        if line == '[BEGIN DESCRIPTION]':
            line = f.readline().strip()#description
            acc = []
            acc.append(line)
            acc.append([])  #acc = [description,[]]
            line = f.readline().strip()#end description
            line = f.readline().strip()#either new ID or begin action #the func.
            if line == '[BEGIN ACTIONS]':#begin action
                line = f.readline() #first action
                while line != '[END ACTIONS]':#use loop to get every line of actions
                    lst = line.strip().split(',')
                    lst[1] = float(lst[1])
                    acc[1].append(tuple(lst))#acc = [description,[(action,ID)]]
                    Dict[float(new_key)] = acc #{0:[action,[(description,ID)]]}
                    line = f.readline().strip()#end actions # how to get to 2.1 and loop
                line = f.readline().strip() #2.1
                new_key = line
                line = f.readline()#begin description
            elif line != '[BEGIN ACTIONS]': #new id, 1
                Dict[float(new_key)] = acc
                new_key = line.strip()# 1,2
                line = f.readline()
    f.close()
    return Dict


    
#5  done!!!!!
def get_indices(lst, elm):
    '''
    (list of lists, object) -> tuple of two ints
    
    Given a list of lists and an element, find the first
    pair of indices at which that element is found and return
    this as a tuple of two ints. The first int would be the
    index of the sublist where the element occurs, and the
    second int would be the index within this sublist where
    it occurs.

    >>> get_indices([[1, 3, 4], [5, 6, 7]], 1)
    (0, 0)
    
    >>> get_indices([[1, 3, 4], [5, 6, 7]], 7)
    (1, 2)
    '''
    for i1 in range(len(lst)):
        for i2 in range(len(lst[i1])):
            if elm == lst[i1][i2]:
                return(i1,i2)

#6 done!!
def update_map(map_visual, map_coors, player_id, px, py, dx, dy):
    '''
    (list of lists, dict, str, int, int, int, int) -> None or tuple of two ints

    This function is very similar to update_grid from
    Part 1, but there are few IMPORTANT differences.
    Read the description below carefully!
    
    Given the player's current position as px and py,
    and the directional changes in dx
    and dy, update "map_visual" to change the player's
    x-coordinate by dx, and their y-coordinate by dy.
    The player's position should be represented as (*)
    where * is their given player id.

    Notes:
    This time, we don't have a w and h representing the grid,
    as the map's width and height may vary depending on the
    file that we read. So, you should figure out the width
    and height using the len function and the given map_visual.

    If the move is NOT valid (not within the map's area) OR
    it would involve moving to a coordinate in which the
    location ID is -2 (which is the ID representing all
    inaccessible locations), then NO change occurs to the map_visual.
    The map_visual stays the same, and nothing is returned.

    If the move IS possible, the grid is updated just like it was
    for Part 1, and the new x- and y- coordinates of the player
    are returned as a tuple.
    '''
    if px + dx >= len(map_visual[0]) or px +dx < 0 or \
       py + dy >= len(map_visual) or py + dy < 0:
        return (px,py)
    elif map_visual[py+dy][px+dx] == '(x)':
        return (px,py)
    else:
        map_visual[py][px] = '(_)'
        map_visual[py+dy][px+dx] = '(' +player_id +')'
        return(px+dx,py+dy)


#7  done!
def check_items(current_location, game_items, inventory):
    '''
    (int, dict) -> None
    
    Given an int location id and a dict of game items where the keys are the
    item names, and the values are lists with the following
    information in this order: [description of item, starting
    location where item is found, location where item should be
    dropped of], check if any of the game items are found in the current
    location provided. If they are, add them to the inventory.
    
    You should be modifying the variable 'inventory',
    within this function, and NOT returning anything.
    '''
    keys = list(game_items.keys())
    values = list(game_items.values())
    index = None
    for i in range(len(values)):
        if float(current_location) == float(values[i][1]) or \
           float(current_location) == float(values[i][2]):
           index = i #to record the index
    if index != None:
        if keys[index] not in inventory:
            inventory = inventory.append(keys[index])


#8
def check_game_won(game_data, inventory, p_x, p_y):
    '''
    (dict, list, int, int) -> bool
    
    Return True iff the player is at the goal location, and all
    goal items are in the player's inventory.   
    '''
    for item in list(game_data["game_items"].keys()):
        if item not in inventory:
            return False
    if game_data["goal_location"][0] == p_y and \
        game_data["goal_location"][1] == p_x:
        return True
        

 #9               
def do_action(decision, game_data, current_location, inventory):
    '''
    (int, dict, float, list) -> str

    Given the game data dict, and the current location ID, get
    all the possible actions at that location.

    If the decision number given as 'decision' falls outside the number
    of allowed actions at this location, then return the string
    "Invalid decision. Please select choice from the decisions listed."
    Make sure this string is EXACTLY as above.

    Else, if the decision is valid, then figure out the location information
    of the new location ID that the player should end up at after
    doing this decision (use game_data, current_location, and the decision
    chosen to figure this out).

    Check for any items at this new location and add to inventory (remember you
    can call already existing functions to make your code shorter
    and less repetitive).

    Return the text description of the new location ID where you end up
    after doing this action (e.g. the same way that visit_location function
    returns text description of visited location).
    '''
    for key in game_data["location_data"]:
        if current_location == key:
            new_key = key
            values = game_data["location_data"][new_key]
            if decision > len(values[1]):
                return "Invalid decision. Please select choice from the decisions listed."
            elif decision <= len(values[1]):
                new_location_id = values[1][decision-1][1]
                check_items(new_location_id, game_data["game_items"], inventory)
                return game_data["location_data"][new_location_id][0]
                

# --------------------------------------------------------------------------------------#
# --- EVERYTHING BELOW IS COMPLETED FOR YOU. DO NOT MAKE CHANGES BEYOND THIS LINE. ---- #
# --------------------------------------------------------------------------------------#

def check_inventory(inventory):
    '''
    (list) -> None

    Print out the contents of the inventory.
    
    NOTE:
    THIS FUNCTION IS ALREADY COMPLETE.
    YOU DO NOT NEED TO CHANGE THIS FUNCTION.
    '''
    
    if len(inventory) == 0:
        print("You have nothing in" \
              "your inventory.")
    print("Items in your inventory: " + str(inventory))
    
def visit_location(game_data, current_location):
    '''
    (dict, int) -> str
    
    Visit the current location data by printing out the map,
    checking if any items are found at that location,
    and then returning the text associated with this current location.

    NOTE:
    THIS FUNCTION IS ALREADY COMPLETE.
    YOU DO NOT NEED TO CHANGE THIS FUNCTION.
    '''
    
    print_map(game_data["map_visual"])
    check_items(current_location, game_data["game_items"], inventory)
    return game_data["location_data"][current_location][0]

def show_actions(actions):
    '''
    (list) -> None

    Given a list of special actions, print out all these actions (if any),
    and other basic actions that are possible.

    NOTE:
    THIS FUNCTION IS ALREADY COMPLETE.
    YOU DO NOT NEED TO CHANGE THIS FUNCTION.
    '''
    
    print("-------------------------")
    for i in range(len(actions)):
        print(i+1, actions[i][0])
    print("Type N, S, E, or W to move, or inventory to check inventory. Type quit to exit the game.")
    print("-------------------------")
    
def print_map(map_data):
    '''
    (list of lists) -> None
    
    Print out the map represented by the given list of lists map_data.

    NOTE:
    THIS FUNCTION IS ALREADY COMPLETE.
    YOU DO NOT NEED TO CHANGE THIS FUNCTION.
    '''
    
    s = ''
    for row in range(len(map_data)):
        s += ''.join(location for location in map_data[row]) + "\n"
    print(s)
    
def get_moves(d):
    '''
    (str) -> tuple of two ints

    Given a direction that is either 'N', 'S', 'E' or 'W'
    (standing for North, South, East or West), return
    a tuple representing the changes that would occur
    to the x- and y- coordinates if a move is made in that
    direction.

    e.g. If d is 'W', that means the player should move
    to the left. In order to do so, their x-coordinate should
    decrease by 1. Their y-coordinate should stay the same.
    These changes can be represented as the tuple (-1, 0),
    because the x-coordinate would have -1 added to it,
    and the y-coordinate would have 0 added to it.

    >>> get_moves('W')
    (-1, 0)
    >>> get_moves('E')
    (1, 0)

    NOTE:
    THIS FUNCTION IS ALREADY COMPLETE.
    YOU DO NOT NEED TO CHANGE THIS FUNCTION.
    '''
    
    if (d == "N"):
        return (0,-1)
    elif (d == "S"):
        return (0,1)
    elif (d == "E"):
        return (1,0)
    else:
        return (-1,0)

def print_help():
    '''
    () -> None

    Print out possible decisions that can be made.
    This function is called if the user provides an invalid decision.

    NOTE:
    THIS FUNCTION IS ALREADY COMPLETE.
    YOU DO NOT NEED TO CHANGE THIS FUNCTION.
    '''
    
    print("Type N, S, E or W to move North, South, East or West. \n" \
          "Type inventory to check inventory. \n" \
          "Type quit to quit the game.")
    print("If special actions are listed, you may type the number beside that action to choose that action.")

def set_game_data(map_file, item_file, location_file):
    '''
    (str, str, str) -> dict
    
    Read data from the given files and return a dictionary
    of all game data.

    NOTE:
    THIS FUNCTION IS ALREADY COMPLETE.
    YOU DO NOT NEED TO CHANGE THIS FUNCTION.
    '''
    
    map_data = load_map(map_file)
    map_visual, map_coors = generate_map(map_data, p_x, p_y, player_id)
    game_items = load_items(item_file)
    location_data = load_locations(location_file)

    # The lines below use list comprehensions again!
    # As stated in Part 1 starer code, this is not covered in 108
    #   but I'm showing this to you anyway because it can come in handy for shortening code.
    # You can achieve the same thing without using this technique though, so no worries
    #   if you're not fully comfortable with it.
    # More info here about what this means: http://blog.teamtreehouse.com/python-single-line-loops
    game_overs = [k for k, v in location_data.items() if v[0].lower().startswith("game over")]
    goal_items = [k for k, v in game_items.items() if v[2] == -1]

    goal_location = get_indices(map_data, "-1")

    return {"map_data": map_data, "map_visual": map_visual, "map_coors": map_coors,
            "game_items": game_items, "location_data": location_data,
            "goal_items": goal_items, "goal_location": goal_location,
            "game_overs": game_overs, "won": False, "lost": False}

# ==== Finish the functions above according to their docstrings ==== #
# ==== The program starts here. ==== #
# ==== Do NOT change anything below this line. ==== #
if __name__ == "__main__":

    player_id = input("Choose any letter other than 'x' to represent you: ")
    while len(player_id) != 1 or not player_id.isalpha() or player_id.lower() == 'x':
        print("Invalid input.")
        player_id = input("Choose any letter other than 'x' to represent you: ")

    # initialize current player info
    w = mapfile_hight('map.txt')
    h = mapfile_width('map.txt')
    p_x = random.randint(0,w-1)
    p_y = random.randint(0,h-1)
   # player's starting point will be randomized on the map.
    inventory = []
    
    game_data = set_game_data("map.txt", "items.txt", "locations.txt")

    # show map and location data
    current_location = game_data["map_coors"][(p_x, p_y)]    
    result = visit_location(game_data, current_location)

    while not game_data["won"] and not game_data["lost"]:

        show_actions(game_data["location_data"][current_location][1])
        decision = input("What do you want to do? > ")

        if decision.upper() in 'NSEW':
            dx, dy = get_moves(decision.upper())
            new_xy = update_map(game_data["map_visual"], game_data["map_coors"], player_id, p_x, p_y, dx, dy)
            if not new_xy:
                print("You can't go there.")
            else:
                p_x, p_y = new_xy
                current_location = game_data["map_coors"][(p_x, p_y)]    
                result = visit_location(game_data, current_location)
                print(result)
    
        elif decision.isdigit():
            result = do_action(int(decision), game_data, current_location, inventory)
            print(result)
            
        elif "inventory" in decision:
            check_inventory(inventory)

        elif decision == 'quit':
            print('Game Over!')
            exit(1)

        game_data["lost"] = result.lower().startswith("game over")
        game_data["won"] = check_game_won(game_data, inventory, p_x, p_y)

    if game_data["won"]:
        print("Congratulations! You found your way back home!")

