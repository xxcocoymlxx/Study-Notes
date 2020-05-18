import time

TILE_DESCS = {'(_)': 'dirt', '(r)': 'ruby', '(s)': 'sapphire',
                     '(e)': 'emerald', '(d)': 'diamond',
                     '(x)': 'wall'}

GEMS = ['ruby', 'sapphire', 'emerald', 'diamond']

class Tile:
    '''A class to represent one spot/location on the map.'''
    
    def __init__(self, x: int, y: int, icon: str, desc: str) -> None:
        '''
        Construct Tile using x, y coordinates, a string icon to represent
        this tile on the map, and a longer string description of
        what this tile represents.

        --======================================================-        
        The Tile also keeps track of a list of Tiles that are adjacent
        to it (horizontally or vertically; Drillbots can NOT move diagonally).
        '''
        
        self.x = x
        self.y = y
        self.icon = icon
        self.desc = desc
        self.adj_tiles = []

    def get_visited(self, id_num: int) -> None:
        '''
        Update this tile's icon/desc to represent drillbot visiting the location.
        '''

        self.icon = '(' + str(id_num) + ')'
        self.desc = 'drillbot'
        
    def get_dug(self) -> None:
        '''
        Update this tile's icon/desc to be dirt, after being dug.
        '''

        self.icon = '(_)'
        self.desc = 'dirt'
        
    def __str__(self) -> str:
        '''
        Return string representation of this tile.
        '''

        return self.icon

    def __repr__(self) -> str:
        '''
        Return detailed string representation of this tile.
        '''

        return 'desc: ' + self.desc + '\nx: ' + str(self.x) + '\ny: ' + str(self.y)
    
class Map:
    '''A class to represent a map made of several connected tiles.'''

    def __init__(self, map_data: list):
        '''
        Given a list of lists representing map data, construct Tiles to represent
        each location, connect adjacent tiles, and assign a starting point.
        
        In a valid map, the starting point will NOT be a wall, and every gem
        in the map will be accessible through up/down/left/right movements,
        beginning from this starting point.
        
        You may assume all maps that are passed in are valid.
        (That is, we will only test your code with valid maps).
        '''

        self.tiles = self._create_tiles(map_data)
        self._connect_tiles()
        self.start = self.tiles[0][0]

    def _create_tiles(self, map_data: list) -> list:
        '''
        Return a list of lists of Tile objects representing each location
        on the given map_data as a Tile (each with x, y coordinates, the visual
        icon representation of it, and a string description).
        '''
        
        tiles = []
        for i in range(len(map_data)):
            new_row = []
            for k in range(len(map_data[i])):
                icon = map_data[i][k]
                new_row.append(Tile(k, i, icon, TILE_DESCS[icon]))
            tiles.append(new_row)
        return tiles

    def _connect_tiles(self) -> None:
        '''
        For each tile in self.tiles, keep track of a list of all of
        that tile's adjacent non-wall tiles.
        '''
        
        for i in range(len(self.tiles)):
            for k in range(len(self.tiles[i])):
                self.tiles[i][k].adj_tiles = self.find_adj(k, i)

    # TO DO -- COMPLETE THE METHOD BELOW
    def find_adj(self, x: int, y: int) -> list:
        '''
        Return a list of non-wall Tile objects which are adjacent (to the north,
        south, east and west; NO diagonals) of the given x and y position.
        
        e.g.
        If my map is as follows:
        (x) (s) (d)
        (_) (_) (r)
        (e) (x) (_)
        And we called find_adj on coordinates (2, 2) which is the bottom-right
        corner of the map, then this method should return a list of just one
        adjacent tile -- the tile at position (2, 1) containing the ruby (r) to the
        north of this spot. This is because every other spot beside this location
        is out of bounds, and to the left is a wall, so the wall is not
        included in the adjacent tiles.
        '''
        acc = []
        num = [1,-1]
        #把哪个位置上的相邻tile先放入acc决定了'0'行走方向的优先级
        for i in num:
            if y + i >= 0 and y + i < len(self.tiles):
                if self.tiles[y+i][x].desc != 'wall':
                    acc.append(self.tiles[y+i][x])
        for k in num:
            if x+k >= 0 and x+k < len(self.tiles[y]):
                if self.tiles[y][x+k].desc != 'wall':
                    acc.append(self.tiles[y][x+k])
        
        return acc
        
        
    def __repr__(self) -> str:
        '''
        Return a string representation of this map.
        '''
        
        s = ''
        for row in self.tiles:
            for t in row:
                s += str(t)
            s += "\n"
        return s

# TO DO -- COMPLETE THE CLASS BELOW
# Step 1: Read and understand this class. Add in docstrings for the class, and
#         its methods to demonstrate your understanding. Use proper docstring format.
# Step 2: Complete the "explore" method as described on the assignment handout.
#         Your code MUST be recursive.
class DrillBot:

    def __init__(self, m:Map):
        self.id_num = 0
        self.storage = {}
        self.visited = []
        self.map = m

    def visit(self, location:Tile)->None:
        dug = location.desc
        location.get_visited(self.id_num)
        print(self.map)
        if dug in GEMS:
            self.storage[dug] = self.storage.get(dug, 0) + 1
        location.get_dug()
        self.visited.append(location)
        time.sleep(0.5)
        
    #partner写的，不是我写的
    def explore(self, location:Tile)->None:
        if not location:
                return None
        else:
            self.visit(location)
            if location.adj_tiles == []: #没有可以前进的相邻tile
                return None
            elif location == self.map.start and len(self.visited) > 1: #因为map至少有两个tile，则转完一圈回到start时len(self.visited)肯定大于2
                return None#但这个写法只适用于这个map，若是其他的map，回到起始点时，self.visited可以大于2
            else:  # map至少有2个非wall tiles, 即start location 至少有一个可以进入的相邻tile
                for tile in location.adj_tiles:
                    if tile not in self.visited:
                        return self.explore(tile) #如果有可进入的相邻tile不在self.visited内，则直接将这个相邻tile代入self.explore（）运行
                visit_index = self.visited.index(location) #如果运行到了这条，就说明location tile的所有相邻tile都已走过
                pre_tile = self.visited[visit_index-1] #所以只要找到最初是从哪里进入这个location tile就行了
                return self.explore(pre_tile)
            
        
if __name__ == "__main__":
    # Some set worlds; feel free to add more maps to test things out
    map1 = [['(_)','(_)','(s)'],
             ['(_)','(x)','(r)'],
             ['(_)','(_)','(_)']]

    map2 = [['(_)','(_)','(s)','(r)','(_)'],
             ['(_)','(x)','(r)','(x)','(s)'],
             ['(_)','(_)','(_)','(x)','(r)'],
             ['(_)','(x)','(_)','(x)','(_)'],
             ['(d)','(x)','(x)','(x)','(_)'],
             ['(_)','(d)','(_)','(s)','(r)']]

    # Set the map_data to use, construct a Map object, start drilling, print out results
    map_data = map2
    #map_data = map1
    m = Map(map_data)
    print('this is the starting point')
    print(m.start)
    print('it also has children that are adjacent tiles')
    print(m.start.adj_tiles)
    print('now to build a drill bot and have it explore map.start')
    print("'0' is the drill bot, \n'_' is just dirt, \n'x' is an impassable wall, \n'r' is a ruby, \n's' is a saphhire, \n'e' is an emerald, \n'd' is a diamond")
    d = DrillBot(m)
    d.explore(m.start)
    print('and this is what the drillbot managed to mine')
    print(d.storage)
