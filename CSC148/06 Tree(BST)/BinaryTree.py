#不带壳的Tree
#这里介绍一个很重要的思想：遍历
#tree的很多method都会用到遍历，包括深度优先搜索和广度优先搜索
#我已经get了tree的遍历（用到recursion）的题的诀窍了
#直接就对tree的左支和右支call当前function，把他当做已经得到了你要的结果了，再想之后要怎么办，再凑我们最终要的答案
#只做当前一层要做的事！
#还有！在class里面的function必须判断左支右支为不为空！

class BTNode():
    def __init__(self, data, left = None, right = None):
        self.data = data
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.left == self.right == None

    def traversal(self):#遍历
        '''
        遍历就是把tree里所有元素都visit一遍，visit的同时do something with the data.
        这个function就是把tree里的所有元素都print出来。
        遍历的格式基本就是这样，你想要这个遍历干什么基本就取决于你的base case是什么。

        这三种order都属于深度优先搜索（DFS)

        pre-order:  middle -> left -> right

        post-order: left -> right -> middle

        in-order: left -> middle -> right
        '''
        #这个其实是in-order
        #如果要其他order就把下面这3行code换一下顺序就好

        #如果是在class内部写的就要判断为不为空，如果再class外面写的就不用
        if self.left:#左
            self.left.traversal()#要相信call了这个function他就会自己完成给你所有排列好的元素的

        #也是base case
        print(self.data)#中
        
        if self.right:
            self.right.traversal()#右
            

    def find(self, data):
        '''Return True iff the tree contains the given data.
            这个function的思想和遍历也是一样的，只是在visit每个元素的
            同时判断一下当前元素是不是我们要找的元素。
            接下来几个function的格式都和这个很像，就是要注意判断两个东西：
            1.左支右支存不存在 2.如果不存在怎么办（base case）'''
        if self.data == data:
            return True
        
        if self.left:
            left_result = self.left.find(data)#注意，在class里面是self.call这个function，class外面就只function(parameter)
        else:
            left_result =  False #base case

        #这里不能直接return，因为要左边右边最后要合起来一起看，不能based on一边的结果就return
        #所以这里要把左支和右支的结果都存起来
        if self.right:
            right_result = self.right.find(data)
        else:
            right_result = False#base case
        
        return left_result or right_result



    def node_num(self):  
        '''Return the number of nodes/data in the tree.
            这个function也是沿用了遍历的思想。
            左支的总元素数加上右支的总元素数加上1（self.head）'''

        if self.left:
            left_result = self.left.node_num()
        else:#如果左支不存在
            left_result = 0 #遍历时要这个function干嘛就取决于base case
        
        if self.right:
            right_result = self.right.node_num()
        else:#如果右支不存在
            right_result = 0 #base case

        return 1 + left_result + right_result


    def find_max(self):
        '''Return the maximum value in the tree.
            用recursion得到左支最大，右支最大，来和self.head比较'''

        if self.left:
            left_max = self.left.find_max()
        else:
            left_max = self.data#这里的base case就是self.data

        if self.right:
            right_max = self.right.find_max()
        else:
            right_max = self.data

        return max(self.data,left_max,right_max)
        

    def height(self):
        '''Return the height of the tree (maximum depth).
            这种code就别想着track了，一层上的逻辑对了就行。'''

        if self.left:
            left_height = self.left.height()
        else:
            left_height = 0

        if self.right:
            right_height = self.right.height()
        else:
            right_height = 0

        return 1 + max(left_height, right_height)#左支右支的最高depth加上本身的1
        


#壳
class BinaryTree():
    def __init__(self, root=None):
        self.root = root #Tree的壳也只有一个root的attribute

    def traversal_pre(self):
        '''
        (BinaryTree)->list
       pre-order: middle -> left -> right
        '''
        #这个function画遍图就懂了
        todo = [self.root]

        while todo != []:
            curr = todo.pop() #这个pop是list的method
            if curr != None:
                print(curr.data)
        
                todo.append(curr.right) #先append进curr.right，就后pop出  
                todo.append(curr.left)  #后append进curr.left，就先pop出左支的
                #todo里又有东西了，就又循环起来，按照中左右的顺序print完所有东西

            
    def traversal_post(self):
        '''Postorder: left -> right -> middle'''
        todo = [self.root]
        nodes = []

        while todo != []:
            curr = todo.pop()
            if curr != None:
                nodes.append(curr)#先按照反的顺序把元素都加进nodes里，最后再倒转回来
                
                todo.append(curr.left)
                todo.append(curr.right)   
                  
        while nodes !=[]:#最后再把nodes里存的元素从后面print出来
            node = nodes.pop()
            print(node.data)

    def DFS(self):
        '''难：深度优先搜索，三种order其实都是DFS
            读一个数放进list，pop并print，同时读他的右支左支并放进list，pop左支出来并print，
            然后再把他的右支左支加到list里，再pop掉右支并print，再把他的在下级的右支左支加进去。
            【读上层元素就把当前元素的右支左支加进list，pop并print左支，再把他的再下级加进list，
             再pop并print list的最后一位，也就是左支，直到没有更下一级的元素，这样list里的左支元素就
             都被pop和print掉的，剩下的就是按照顺序添加进去的右边的元素】'''
        todo = [self.root]  #as Stack

        while todo != []:
            curr = todo.pop()

            if curr != None:
                print(curr.data, end = ' ')

                todo.append(curr.right)
                todo.append(curr.left)


    def BFS(self):
        '''简单：广度优先搜索
            读一个数，放进list，pop的同时print，同时读取他的左支，右支
            放到list最后，然后从list的前面开始pop并print，并读取他的左支右支放到list最后面
            【读上一层的元素时就同时把他的下一层按照顺序放到了list最后，然后按照从前往后的顺序读list的元素就好】'''
        todo = [self.root]  #as Queue

        while todo != []:
            curr = todo.pop(0)

            if curr != None:
                print(curr.data, end = ' ')

                todo.append(curr.left)#从前往后pop，所以按照正序append
                todo.append(curr.right)
    
                

a = BTNode(1,BTNode(2,BTNode(4), BTNode(5)),BTNode(3, BTNode(6)))
t = BinaryTree(a)