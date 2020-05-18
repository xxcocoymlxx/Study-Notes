#BST by Hung
#不带壳的，recursion
class BSTNode():
    def __init__(self,data,left=None,right=None):
        self.data, self.left, self.right = data, left, right

    def is_leaf(self):
        return self.left == self.right == None

    def height(self):
        '''maximum depth'''
        if self.is_leaf():
            return 1

        if self.left:
            l = self.left.height()
        else:
            l = 0 #base case

        if self.right:
            r = self.right.height()
        else:
            r = 0 #base case

        return 1 + max(r,l)

    def find_data(self, data):
        '''Return True iff the BST contains the given data.'''
        if self.data == data:
            return True

        if self.data > data and self.left != None:
            return self.left.find_data(data)

        if self.data < data and self.right != None:
            return self.right.find_data(data)

        return False

    def add_node(self, data):
        '''在BST合适的地方添加进新data。'''
        if self.data < data:
            if self.right:
                self.right.add_node(data)
            else:#如果右支不存在了就说明已经是在最底层了，recursion会自己在合适的位置添加的
                self.right = BSTNode(data)

        elif self.data > data:
            if self.left:
                self.left.add_node(data)
            else:
                self.left = BSTNode(data)


    def delete(self,data):
        '''此时是不带壳的，我们默认不能删除root。'''
        parent_del = None #初始化要删除元素的parent
        curr_del = self #初始化要删除的元素
        ############################################################################
        #以下就是找删除元素和删除元素的父亲
        while curr_del != None and curr_del.data != data:#只要当前node不等于要删除的元素
            parent_del = curr_del #往后移动
            if curr.data > data:
                curr = curr.left
            else:
                curr_del = curr_del.right #此时while要是结束了那就只有一种可能性，就是找到了我们要删除的元素

        #从上面那个while出来要么curr_del是None要不然就是找到了删除元素
        #找不到要删除的元素
        if curr_del == None:#那就说明我要删除的元素根本就不再tree里
            return#就直接结束

        ############################################################################
        #初始化替换点和他的父亲
        parent_c = curr_del#从删除点的左支开始查找
        curr_c = curr_del.left #替换节点：删除点的左支最大值
        #查找替换点和他的父亲
        while curr_c != None and curr_c.right != None:#最大值肯定在右支
            parent_c = curr_c
            curr_c = curr_c.right

        #这也是删除元素是leaf时，进入这里，直接删
        #找不到替换点，也就是左支最大值，不存在左支，那就只有一个孩子，就直接链接
        if curr_c == None:#如果这里是none，说明一开始赋值的时候就是none，就说明我要删除的点没有左孩子，只有右孩子，就是只有一个孩子的情况，直接链接就好了
            #此时要判断我是我的父亲的左支还是右支，找到curr_del在我父亲当中的为止
            if parent_del.left == curr_del:#如果我是我父亲的左支
                parent_del.left = curr_del.right#链接我的右支
            else:#如果我是我父亲的右支
                parent_del.right = curr_del.right#让我的右支来替代我父亲中我的位置

            #断开我和我右支的链接（我就是删除的元素，删除元素已经被删除）
            curr_del.right = None
            return

        #######################################################################
        #既然我能够下来到这里，现在已经在左支找到了替换点，也就是左支最大值，和他的父亲，和删除点和删除点的父亲，说明是有两个孩子的情况
        #接下来就要处理他们之间的关系了

        #先处理替换点和替换点的父亲的关系
        #我是左支最大值，我没有右支了
        #让我的父亲和我的左支链接起来就可以，替换点就拿出来了
        #但是此时还是不知道替换点究竟是替换点父亲的左支还是右支

        #让我的孩子来继承我和我孩子的关系
        #替换点和他父亲的关系
        if parent_c.left == curr_c:
            parent_c.left = curr_c.left
        else:
            parent_c.right = curr_c.left

        #断开替换点和替换点孩子的关系
        curr_c.left = None
        #此时替换点已经自由了，替换点的父亲已经和替换点的孩子链接起来了

        #下一步，替换点和删除点孩子之间的关系
        curr_c.left = curr_del.left#替换点已经链接了删除点的孩子
        curr_c.right = curr_del.right

        #这里就是处理删除点的父亲和替换点之间的关系
        #再次判断删除点在删除点父亲的左支还是右支
        if parent_del.left == curr_del:#如果我是我父亲的左支
            parent_del.left = curr_c#链接我的右支
        else:#如果我是我父亲的右支
            parent_del.right = curr_c#让我的右支来替代我父亲中我的位置

        #断开我和我右支的链接（我就是删除的元素）
        curr_del.left = None#此时删除点已经自由了
        curr_del.right = None
        return


    def find_max_node(self):
        '''找到左支最大值'''
        if self.left == None:
            return self

        return self.left.find_max_node()

    def __str__(self):
        '''print a sideway tree.
            这个不用看了'''
        if self.is_leaf():
            return str(self.data)

        s = ''
        if self.left:
            l = str(self.left)
        else:
            l = ''

        if self.right:
            r = str(self.right)
        else:
            r = ''
            
        s = l + '\n' + self.height()*4*" "+ str(self.data) + '\n' + r

        return s


###########################################################################
#带壳的
class BTNode():
    def __init__(self,data,left=None,right=None):
        self.data, self.left, self.right = data, left, right

    def is_leaf(self):
        return self.left == self.right == None


class BST():
    def __init__(self, root=None):
        self.root = root

    def add_node(self, data):
        '''
        在BST里合适的为止添加进新的元素。
        没壳的就用recursion做，有壳的就用loop写。
        loop写的话，设curr = self.root，当curr不为None时，就一个一个往后移。'''
        if not self.root:#empty tree
            self.root = BTNode(data)

        curr = self.root
        while curr != None:
            if curr.data > data:
                if curr.left:#如果有左支，就一直往下看，一直找到没有左支为止
                    curr = curr.left #循环起来
                else:
                    curr.left = BTNode(data)#如果没有左支了，就是添加新的node的位置
                    return
            elif curr.data < data:
                if curr.right:
                    curr = curr.right #循环起来
                else:
                    curr.right = BTNode(data)
                    return


    def delete(data):
        '''找到左支最大值（这时我一定没有右孩子，因为如果还有右孩子那我就不是最大的了）
            删除时，就可以把我的左支连接到我的父亲（我没右支了），然后把要删除元素的父亲连到我，
            我连向删除元素的左右孩子。最后再断开删除元素原本的链接。
            我们要保留一下4个node才能完成删除：
            1.要保留的要删除元素的父亲
            2.要保留要删除元素
            3.要保留左支最大值
            4。要保留左支最大值的父亲'''
        parent = None
        curr = self.root # find delete-node
        while curr != None and curr.data != data:
            parent = curr
            if curr.data > data:
                curr = curr.left
            else curr.data < data:
                curr = curr.right

        if curr == None:
            return

        r_parent = curr
        r_curr = curr.right #replace-node   min in right subtree of curr
        while r_curr != None and r_curr.left != None:
            r_parent = r_curr
            r_curr = r_curr.left

        if r_curr == None:
            if parent:#delete-node is not root
                connect(parent,curr,curr.left)
                
            else:#delete-node is root
                self.root = curr.left

            curr.left = None
            return

        #take out replace-node from its network
        connect(r_parent,r_curr, r_curr.right)
        r_curr.right = None


        # let replace-node to replace delete-node

        #for children
        r_curr.left = curr.left
        r_curr.right = curr.right
        curr.left = None
        curr.right = None

        #for parent
        if parent: #delete-node is not root
            connect(parent,curr, r_curr)
            
        else: #delete-node is root
            self.root = r_curr

##############################################################################
#outside the class! 所以helper function是写在class外面的。
def connect(p,c,new): 
    '''delete function的helper function。
        帮助我们链接parent和新的child node
        p是parent node， c是child node， new是新添加的node'''
    if p.left == c:
        p.left = new
    else:
        p.right = new

###############################################################################
#下面两个function都是把list变成一个BST
def make_BST_from_list():
    '''
    在有壳的BST里有已经写好了add_node function的情况下，直接用loop添加就可以。
    按照given list里的元素顺序添加进BST（同时也满足BST的property）
    比如 l = [3,21,56,89,56,1,4,56,8,5]
    '''
    t = BST()
    for e in l:
        t.add_node(e)#这个function会按照BST的property添加进新的node

    return t


def make_BST_from_list():
    '''
    有壳的BST
    在没有已经写好的add_node function的情况下直接把一个list转化为BST。
    for loop只会每次往后读取一个元素，while才是判断把当前元素放到BST里哪个位置的，
    如果位置不对就一直while，直到找到正确的位置后添加。'''
    t = BST()

    for e in l: 
        if not t.root:
            t.root = BTNode(e)
        else:
            flag = 0#打开开关
            curr = t.root
            while flag == 0:#如果没加过东西就是0，加了东西就是1，就停止循环了，因为要不然下面不管左支为None还是右支为None都会添加进东西去
                if curr.data > e:
                    if curr.left:
                        curr = curr.left#
                    else:
                        curr.left = BTNode(e)
                        flag = 1 #关掉开关，不能再往里加东西了 
                        #这个flag是为了让while停止，如果不让while进不去，就会无限的添加东西！

                elif curr.data < e:
                    if curr.right:
                        curr = curr.right
                    else:
                        curr.right = BTNode(e)
                        flag = 1#关掉开关

    return t
