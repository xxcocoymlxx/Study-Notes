#没壳的
class BTNode():
    def __init__(self, data, left=None, right=None):
        self.data, self.left, self.right = data, left, right

    def longest_path(self):
        """ BTNode -> list of BTNode"""
##        这是下面已经包含了的base case
##        if self.left == self.right == None:
##            return [self]

        if self.left:
            l = self.left.longest_path()
        else:
            l = [] #base case

        if self.right:
            r = self.right.longest_path()
        else:
            r = [] #base case

        if len(l) > len(r):
            l.append(self)#记得要添加上自己！
            return l
        else:
            r.append(self)
            return r

    def all_longest_paths(self):
        """ BTNode -> list of list of BTNode
            如果有好几个相同长度的longest path，return a list of list of the paths"""

        if self.left:
            l = self.left.all_longest_paths()
        else:
            l = []

        if self.right:
            r = self.right.all_longest_paths()#此时已经是一个大list里面含有很多个longest path
        else:
            r = []     

        #只想当前一层的情况，现在l和r都是已经包含了所有longest paths的list了
        if l == []:
            longest = r    
        elif r == []:
            longest = l
        elif len(l[0]) > len(r[0]):#既然都是longest path那长度应该都是一样的，比较第一个path的长度就好
            longest = l
        elif len(l[0]) < len(r[0]):
            longest = r
        else:#l和r里的longest path长度相等
            longest = l + r

        if longest == []:
            return [[self]]#左支右支都没有path，tree里只有他一个
        
        for a_path in longest:#大list里的每一个小path
            a_path.append(self)#最后都要加回他自己

        return longest


    def shortest_path(self):#pretty much the same as the longest one
        pass


    def all_data_in_level(self, level):
        """ (BTNode, int) -> list of BTNode
        """
        if level == 0:
            return [self]

        if self.left:
            l = self.left.all_data_in_level(level-1)#除去了root就低了一级level
        else:
            l = []

        if self.right:
            r = self.right.all_data_in_level(level-1)
        else:
            r = []

        return l + r

t = BTNode(1,BTNode(2,BTNode(4,BTNode(8),BTNode(9)),BTNode(5,None,BTNode(10))),BTNode(3,BTNode(6),BTNode(7)))