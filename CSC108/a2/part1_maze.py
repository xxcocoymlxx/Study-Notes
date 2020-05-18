import random
#1
def make_grid(w, h, player_coord, gold_coord):
    '''
    (int, int, tuple of two ints, tuple of two ints) -> None
    
    Given two integers width w and height h, append
    sublists into the variable "grid" to make a maze
    of the specified width and height.

    The coordinates for the player and the gold
    is also given as two two-element tuples. For each tuple,
    the first element has the x-coordinate and the
    second element has the y-coordinate. The player
    and the gold should be included in the grid in
    the positions specified by these tuples.

    The player is represented with the string '(o)'
    The gold is represented with the string '(*)'
    All other spaces are represented with the string '(_)'
    
    This function does not return anything.
    It just modifies the "grid" list, by appending to it.

    >>> make_grid(2, 3, (0, 0), (1, 2))
    >>> print(grid)
    [['(o)', '(_)'], ['(_)','(_)'], ['(_)', '(*)']]
    '''
    for i in range(h):
        grid.append([])
        for i1 in range(w):
            grid[i].append('(_)')
            
    player_x = player_coord[0]
    player_y = player_coord[1]
    gold_x = gold_coord[0]
    gold_y = gold_coord[1]
    grid[player_y][player_x] = '(o)'
    grid[gold_y][gold_x] = '(*)'

def print_grid():
    '''
    () -> None
    
    Print out the grid stored in the variable "grid".
    It should print out as described in the assignment
    instructions.

    e.g. if grid = [['(o)', '(_)'], ['(_)','(_)'], ['(_)', '(*)']]
    this function should print out:
    (o)(_)
    (_)(_)
    (_)(*)

    NOTE:
    THIS FUNCTION IS ALREADY COMPLETE.
    YOU DO NOT NEED TO CHANGE THIS FUNCTION.

    P.S. The code below uses something called list comprehensions,
    to shorten lines of code. This is something we don't officially
    cover in 108, but it can come in handy! So, if you're comfortable
    with it, you're welcome to use it. If not, no worries. You can
    stick to what you're most comfortable with.
    
    More about how this works here:
    http://blog.teamtreehouse.com/python-single-line-loops
    '''

    s = ''
    for row in range(len(grid)):
        s += ''.join(element for element in grid[row]) + "\n"
    print(s)


#2       
def update_grid(w, h, px, py, dx, dy):
    '''
    (int, int, int, int, int, int) -> None or tuple of two ints
    
    Given the player's current position as px and py,
    and the directional changes in dx
    and dy, update the "grid" to change the player's
    x-coordinate by dx, and their y-coordinate by dy.

    More information:
    Use the given w and h (representing the grid's width
    and height) to figure out whether or not the move is valid.
    If the move is not valid (that is, if it is outside
    of the grid's boundaries), then NO change occurs to the grid.
    The grid stays the same, and nothing is returned.

    If the move IS possible, then the grid is updated
    by adding dx to the player's x-coordinate,
    and adding dy to the player's y-coordinate.
    The new position in the grid is changed to the player
    icon '(o)', and the old position the player used to be in
    is changed to an empty space '(_)'. The new x- and y- coordinates
    of the player is returned as a tuple.

    This function does NOT create a new grid.
    It modifies the "grid" variable that was defined at the top of this file.
    
    >>> update_grid(2, 3, 0, 0, 1, 0)
    (1,0)

    >>> update_grid(2, 3, 0, 0, 0, 1)
    (0,1)
    
    >>> update_grid(2, 3, 0, 0, -1, 0)
    (0,0)
    '''
    if  px + dx >= w or px + dx < 0 or py + dy >= h or py + dy < 0:
        return (px,py)
    else:
        grid[py][px] = '(_)'
        grid[py+dy][px+dx] = '(o)'
        return (px+dx,py+dy)

def get_moves(d):
    """
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
    """
    
    if (d == "N"):
        return (0,-1)
    elif (d == "S"):
        return (0,1)
    elif (d == "E"):
        return (1,0)
    else:
        return (-1,0)
    
def get_direction():
    """
    () -> str
    
    Ask the user for a direction that is N, S, E or W.
    Once a valid direction is given, return this direction.

    NOTE:
    THIS FUNCTION IS ALREADY COMPLETE.
    YOU DO NOT NEED TO CHANGE THIS FUNCTION.
    """
    
    d = input("Which way would you like to move? Choose N, S, E, W. ")
    while ((len(d) != 1) or (d.upper() not in 'NSEW')):
        d = input("Invalid input. Choose N, S, E, W. ")
    return d.upper()




# ==== Finish the functions above according to their docstrings ==== #
# ==== The program starts here. ==== #
# ==== Do NOT change anything below this line. ==== #
if __name__ == "__main__":
    # We have a global variable called grid that all functions
    # have access to and can modify directly
    grid = []

    w = int(input("Width: "))
    h = int(input("Height: "))

    p_x = p_y = 0
    gold_x = random.randint(1,w-1)
    gold_y = random.randint(1,h-1)
    game_won = False

    make_grid(w, h, (p_x, p_y), (gold_x, gold_y))

    while (not game_won):
        print_grid()
        d = get_direction()
        # the following line unpacks the tuple returned by get_moves
        # this means the first element in the returned tuple gets assigned
        #    to dx, the second element in the tuple assigned to dy
        dx, dy = get_moves(d) 
        new_xy = update_grid(w, h, p_x, p_y, dx, dy)
        if new_xy: # if something is returned, a change has occurred to player position
            p_x, p_y = new_xy
        game_won = (p_x == gold_x) and (p_y == gold_y)

    print("Congratulations! You won.")
