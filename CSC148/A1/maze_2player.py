import random

class MazeGame:
    '''
    A game where two players move through a grid in a race to
    be the first to reach some treasure.
    '''

    def __init__(self, width, height, player1, player2):
        '''
        (MazeGame, Player, Player) -> None
        Construct a new MazeGame with the given width and height,
        and two players. MazeGame should also place a "gold" at
        a randomly chosen coordinate on the far edge of the grid.
        '''
        
        self.width = width
        self.height = height
        self.players = (player1, player2)
        # place the gold at a random spot on the far edge of the grid
        self.gold_coord = (width-1, random.randint(1, height-1)) 

        self.grid = []
        self.make_grid()

        self.turn = 0 # keep track of whose turn it is out of the two players
        
    def make_grid(self):
        '''
        (MazeGame) -> None
        Given width, height and positions of player and gold,
        append things to this maze's grid.
        '''
        
        for i in range(self.height):
            self.grid.append([])
            for j in range(self.width):
                self.grid[i].append('(_)') 
        
        self.grid[self.players[0].y][self.players[0].x] = '(x)'
        self.grid[self.players[1].y][self.players[1].x] = '(o)'
        self.grid[self.gold_coord[1]][self.gold_coord[0]] = '(*)'

    def whose_turn(self, count):
        '''
        (MazeGame, int) -> Player
        Return the Player whose turn it is.
        '''
        if count % 2 == 0:
            next_player = self.players[0]
        else:
            next_player = self.players[1]
        return next_player
    
    def play_game(self):
        '''
        (MazeGame) -> None
        Play the game, with each player taking turns making a move, until
        one player reaches the gold. Players each keep track of their wins and losses.
        '''
        
        # print out the starting state of the maze
        print(self)
        print('------------')
        
        winner = None
        while (not winner):
            if (self.players[0].x, self.players[0].y) == \
               (self.gold_coord[0], self.gold_coord[1]):
                winner = self.players[0]
            elif (self.players[1].x, self.players[1].y) == \
                 (self.gold_coord[0], self.gold_coord[1]):
                winner = self.players[1]
            else:
                 # if no one has reached the gold yet, play one turn of the game (one player makes one move)
                self.play_one_turn()
        
        print('And {} is the winner!!!'.format(winner.name))


    def get_new_position(self, current_player, other_player, d):
        '''
        (MazeGame, Player, Player, str) -> tuple of two ints or None
        
        Given the current player, the other player, and a direction represented
        as a string "N", "S", "E", or "W" (for moving North, South, East or West
        respectively), return the new position. If the new position is not valid (falls outside
        of the grid, or is already occupied by the other player), return None.
        '''
        
        direction_dict = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
        dx, dy = direction_dict[d]
        new_x = current_player.x + dx
        new_y = current_player.y + dy#only current_player moves

        if (0 <= new_x < self.width) and (0 <= new_y < self.height) and \
           not (new_x, new_y) == (other_player.x, other_player.y):#current_player cannot move to the other player's coordinates
                return new_x, new_y
        else:
            return None

    def update_grid(self, player, new_position):
        '''
        (MazeGame, Player, tuple of two ints) -> None
        Given a player and new position, move that player to new position in grid.
        '''
        # update grid to reflect updated coordinates for current_player
        # keep track of the Player's current position before they move
        old_x, old_y = player.x, player.y #for changing the player's icon to a empty space
        player.move(new_position)
        self.grid[player.y][player.x] = self.grid[old_y][old_x]
        self.grid[old_y][old_x] = '(_)'
        
    def play_one_turn(self):
        '''
        (MazeGame) -> None
        Play one turn of the game. Turn could involve moving one place,
        attempting to move one place, or undoing the most recent move.
        '''
        
        current_player = self.whose_turn(self.turn) # get the Player whose turn it currently is
        other_player = self.whose_turn(self.turn-1) # get the other Player in the game
        direction = current_player.get_direction() # get the direction the Player wants to move

        # this returns None if move is not valid
        new_position = self.get_new_position(current_player, other_player, direction) 
            
        if new_position: # this is the same as saying "if new_position != None"                
            self.update_grid(current_player, new_position)
            print("Player {} moved {}.".format(current_player.name, direction))
        else:
            print("Player {} attempted to move {}. Way is blocked.".format(current_player.name, direction))

        # print current state of game
        print(self)
        print('------------')
        
        self.turn += 1
    
    def __str__(self):
        '''
        (MazeGame) -> str
        Return string representation of the game's grid.
        '''
        s = ''
        for row in self.grid:
            s += ''.join(row) + "\n"
        return s.strip()


# TODO: IMPLEMENT PLAYER CLASSES AS DESCRIBED IN INSTRUCTIONS
class Player:
    def __init__(self,name,x,y):
        self.name = name
        self.x = x
        self.y = y
        
    def move(self,new_position):
        self.x = new_position[0]
        self.y = new_position[1]
    

class UserPlayer(Player):
    def get_direction(self):
        d = 'X'
        while d.upper() not in 'SWEN':
            d = input('Which way would you like to move, {}? Choose N,S,E,or W. '.format(self.name))
        return d.upper()
    
class ComputerPlayer(Player):
    def get_direction(self):
        d = {1:'N',2:'S',3:'W',4:'E'}
        i = random.randint(1,4)
        return d[i]


def make_player(player_name, player_type, x, y):
    """
    (str, int, int) -> Player

    Given a player name, player type (either c for computer or u for user),
    and an x and y coordinate, create a new Player of the right type and return it.
    """

    if player_type == "c":
        return ComputerPlayer(player_name, x, y)
    elif player_type == "u":
        return UserPlayer(player_name, x, y)

def main():
    """Prompt the user to configure and play the game."""

    width = int(input("Width: "))
    height = int(input("Height: "))

    name = input("What is p1's name? ")
    p1 = make_player(name, 'u', 0, 0) # make the first player a User at position (0,0)
    
    player_type = input("Is p2 a user or a computer? Enter 'u' for user, 'c' for computer. ")
    name = input("What is p2's name? ")
    # make the second player either a User or Computer based on response to prompt, at position (0,1)
    p2 = make_player(name, player_type.lower(), 0, 1) 

    play_again = True
    while play_again:
        g = MazeGame(width, height, p1, p2)
        g.play_game()
        # reset player locations at end of round
        p1.move((0,0))
        p2.move((0,1))
        play_again = input('Again? (y/n) ') == 'y'         


if __name__ == '__main__':
    main()

