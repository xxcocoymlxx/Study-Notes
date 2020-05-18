#Linked_list by Hung

#############################################################################################
#不带壳的, lots of recursion!!
class Node():
    def __init__(self, data, next_node = None):
        '''注意！self代表的就是head，当前元素'''
        self.data = data
        self.next = next_node

    def append_node(self, data):
        '''Add a new node containing the given data at the end of the linked list.'''
        if self.next == None:#base case
            self.next = Node(data)#注意！这里直接是self.next
            return

        self.next.append_node(data)#recursion会一直套，直到找到self.next为None的node后再添加

    def insert_node(self,index, data):
        '''Add a new node at the given index. 这是个没壳的linked list，我们不能对第一个元素进行操作。
        所以最靠前只能再idnex为1位添加new data。
        不能对第一个元素进行操作的原因是我们创建这个linked list的时候，
        variable是指向第一个元素的，如果改变了第一个元素，
        variable就不再指向同一个东西了，也就是variable指向了新的元素，
        而且丢失了所有之前的linked list。而当我们有个壳，
        壳里有个attribute指向第一个元素，那我们就可以对第一个元素进行更改，
        因为那时的variable就是指向我们的壳的，改变了第一个元素也不会改变variable的指向。'''
        if index == 1:
            new = Node(data)
            new.next = self.next
            self.next = new
            return
        
        if self.next == None:#当index大于linked list的长度时
        #index还不等于1，但self.next已经是None了，就默认直接在linked list最后添加了
            self.next = Node(data)
            return

        #当判断完index不等于1和self.next不等于None后，就会进入这一行code
        self.next.insert_node(index-1, data) # recursion，每次会往后移一位变成个更小规模的linked list
        #一直缩短self.next，同时index减一，当index减到1时就会跳转到base case添加


    def pop(self, index):
        '''Delete the element at given index. 这是个没壳的linked list，我们不能删除第一个（0号位）元素。'''
        if self.next == None:
            raise IndexError('Linked List index out of range')
        
        if index == 1:
            node = self.next #先记录下这个elm，因为不仅要连接新的node，还是断开这个node之前的链接
            self.next = node.next #让第一个元素跳过要删除的元素直接连接下一个元素
            node.next = None #断开要删除的元素与他下一个元素之间的连接
            return node.data #显示被删除元素

        #如果index不为1和self.next不为None了，才会进入下面的code
        self.next.pop(index-1)#进行recursion，每叠代一次就往后移一位形成个更小规模的linked list继续看


    def remove(self, data):
        '''delete data thet first appear in the linked list. we cannot delete the head node'''
        if self.next == None:#cannot remove
            return
        
        if self.next.data == data:
            node = self.next
            self.next = node.next
            node.next = None

        self.next.remove(data)


    def remove_repeating(self):
        '''删除linked list里所有重复元素。从后面开始看，先探底，
        默认底部的东西是不存在任何重复元素的，用它返回到上一层和前面的元素比较，
        前面的元素不能含有后面已经有的东西。
        【从我到我的后面都没有重复的，】
        先叠代，后处理
        叠代完了找到base case才开始往下走code，才开始处理删除重复元素
        每次出来完数据返回到上层recursion的东西就已经是处理完的东西，这是先写叠代
        如果叠代写在后面，就是处理完本层的东西后才叠代'''
        if self.next == None:#肯定没有重复元素
            return 

        self.next.remove_repeating()#一直判断是不是最后一个node，一直到找到最后一个node
        #然后才删重复元素，删了一个返回上层recursion，一直删删删返回返回返回，
        #一直返回到最后一层时就是没有重复元素的linked list了

        sub = self.next #这个已经不含有任何重复元素了，但我并不知道self.data是否跟sub里的元素重复
      
        if sub.data == self.data:
            self.next = sub.next #跳开sub里的重复元素，链接sub里的下一位
            sub.next = None #断开链接
            return

        curr = sub #curr一定跟我不重复，所以直接判断下一位
        while curr.next != None:
            if curr.next.data == self.data:
                node = curr.next
                curr.next = node.next #跳开要删除元素，重新链接
                node.next = None
                return
            curr = curr.next

    def find_index(self,i):
        '''查找特定位置。'''
        if i == 0:
            return self.data

        if self.next == None:#base case index大于linked list长度了
            raise IndexError('Index out of range')

        return self.next.find_index(i-1) 

            
    def __len__(self):#注意！这些都是magic method，都是可以使用接口的
        '''Return the length of the linked list.'''
        if self.next == None:#base case
            return 1

        return 1 + len(self.next)#当前这一层的length加上后面所有的length

    def __contains__(self,key):
        '''Return True if the linked list contains the given value.'''
        if self.data == key:#base case
            return True
        #(注意code的先后顺序排列对structure的影响)
        if self.next == None:#如果self.data不等于key并且self.next是None
            return False#如果linked list里只有一个元素并且这个元素不是我们要找的元素，return False

        return key in self.next #calling this function by interface
        #recursion会一层一层减小linked list（往后移一位）
        #每往后移一位的头位就是self.data，会一直判断到self.data == key了，return 

    def equal(self,other):
        '''判断两个linked list是否相等。'''
        if self.data != other.data:#base case
            return False
            
        if self.next == None and other.next == None:
            return True

        if self.next != None and other.next != None:
            return self.next.equal(other.next)
        else:
            return False


    def find_max(self):
        '''Return the maximum value in the linked list.'''
        if self.next == None:#如果只有一个值，那最大就是他
            return self.data

        curr_max = self.next.find_max()#找到后面所有数的max来和我（self.data）比较
        #注：self.next是一整个linked list

        if curr_max < self.data:#如果后面找到的max比我大，return后面找到的max
            return self.data

        return curr_max#后面找到的max还没我大，那就直接return我

    def reverse(self):
        '''Reverse the linked list.
            1 -> 2 -> 3 -> 4 -> 3 -> 2 -> 1
            原本的linked list [ 1 2 3 4 ] 直接被更改3和4之间的连接，3被连接到4后面去(4是不动的)
            所有链接全部倒转过去，一层一层叠代，从而变成 [4 3 2 1]
            看不懂的时候就画个图。
            head_node的值每次叠代分别是4，43，432，最后return 4321
            要相信self.next.reverse()是已经得到了next剩下所有已经reverse过得linked list'''
        if self.next == None:
            return self
            #注意！这里我们只return self而不是self.data
            #因为reverse后还是个linked list，要以node的形式return

        head_node = self.next.reverse()#在第三层recursion，探到了底，head_node里抓到了4，返回到上层recursion，上层recursion的self就是3
        self.next.next = self#此时的self就是3，self.next.next就是4的后面，等于了self，也就是3
        #【注意！我们只是断开了左边3和4之间的连接，但左边的2此时还连接着右边的3！】
        #所以左边的2的next还是右边的3，左边2的next的next就变成了右边的3的后面
        #所以assign 当前self左边的的2去self.next.next就是把2重新放去了右边3的后面！
        self.next = None#同时断开了原本3与4之间的连接，此时head_node就是4 3，然后返回到再上层recursion

        #这是创建了个new node的方法，以上的方法只是改变了linked list，没有创建新的node
        #head_node.append_node(self.data) 

        #每次recursion完成后都return了一个head_node作为上一层recursion的抓到的值
        #当所有recursion完成后，才最终return reversed过的linked list，也就是head_node
        return head_node

    
    def __repr__(self):
        if self.next == None:
            return str(self.data) + ' -> None'#这里只是string化self.data

        s = str(self.data) + ' -> '

        return s + str(self.next)


#########################################################################################
#带壳的#

class LinkedNode():
    def __init__(self,data,next_node=None):
        self.data = data
        self.next = next_node


class LinkedList():
    '''带壳的linked list就只有一个attribute，就是self.head。有了壳，我们就可以对linked list
        的第一位元素进行操作，因为variable指向的只是self.head这个container，self.head里面
        存储的data可以随意变换。注意！带壳的linked list就不方便用recursion写，因为每次进行
        叠代，都会套着一个壳，处理起来很麻烦。'''
    def __init__(self):
        self.head = None


    def append(self, data):
        '''Add a new node at the end of the linked list.'''
        if self.head == None:
            self.head = LinkedNode(data)
            return

        curr = self.head
        #如果没有self.last这个attribute我们append data就只能每次都循环一次到linked list的最后面
        #每次loop的话就是O(n),input越大，runtime越长
        #但若有self.last，加东西就可以直接加去self.last的后面，O(1),无论input多大操作都是一样的
        while curr.next != None:
            curr = curr.next

        #curr.next是None了进不去loop了
        curr.next = LinkedNode(data)


    def insert(self, index, data):
        '''Insert a new node at given index. 默认如果given index
            大于linked list的长度就把new node添加到linked list的最后面。'''
        if self.head == None:
            self.head = LinkedNode(data)
            return

        if index == 0:
            old = self.head
            new = LinkedNode(data)
            new.next = old
            self.head = new
            return
        
        #if index != 0
        parent = self.head#要记录两个node因为添加node进linked list需要involve改变周边两个node的链接！
        curr = self.head.next
        while curr != None and index != 1:#当index为1了也就是在我们想要添加的位置了（parent后面）
            parent = curr
            curr = curr.next#两个node同时向后移动
            index -= 1#每次loop往后移动一位，index相对来说也就减小一位
            #因为要在given index位添加，所以index是几就只能loop(index-1)，
            #index也只减去（index-1），因为要移动到given index前面的位置
            #所以当index被减到1时，我们才知道已经移动到了我们要添加new node的位置

        #当index == 1，已经到了要添加node的地方
        #或者curr == None，已经到了linked list的最后一位，就把new node直接添加到linked list最后面
        #进不去上面的loop到了这里
        new = LinkedNode(data)
        parent.next = new
        new.next = curr


    def remove(self, data):
        '''Remove the given data from the linked list. 如果given data不在linked list里，就什么都不做。'''
        if self.head == None:
            return

        if self.head.data == data:
            old = self.head#把self.head这个node放进了old里
            self.head = self.head.next#让self.head.next这个node重新放进self.head这个container里
            old.next = None #一定要断开要删除的node与后面的链接，不然我们就会有两个access to后面的node
            return

        parent = self.head #这里我们也是要记录两个会involve到改变reference的node
        curr = self.head.next
        while curr != None:#如果curr == None了他也什么都不会做
            if curr.data == data:
                parent.next = curr.next
                curr.next = None
                return
            parent = curr
            curr = curr.next#循环起来


    def pop(self, index):
        '''Delete and return the data with given index from the linked list.
            raise IndexError if the given index if bigger than the
            length of the linked list.'''
        if self.head == None:
            raise IndexError("Linked list index out of range")
            #error后面的括号里的东西可写可不写，是exception出现时的红字提示语

        if index == 0:
            old = self.head
            self.head = old.next
            old.next = None
            return old.data#pop有return值
        
        parent = self.head#parent是为了要记录要删除元素前面那个元素，才好链接前后
        curr = self.head.next
        curr_index = 1#设定一个虚拟的index，每次往后移动一位check元素的时候index跟着加1
        while curr != None:#我们要删除和操作的是curr位的元素，所以初始index就从1开始加而不是0，0是parent的初始index
            if curr_index == index:#这里是每次往后移一位index就加1，一直加到我们设定的index和input的index相等
                parent.next = curr.next#或者也可以就用input的index每次减1，直到减到index为1时，就删除curr位的元素
                curr.next = None
                return curr.data
            parent = curr#依次往后移，循环起来
            curr = curr.next
            curr_index += 1
            
        #如果curr == None了，说明given index大于linked list的长度了
        raise IndexError("Linked list index out of range")


    def __len__(self):
        '''Return the length of the linked list.'''
        t = 0
        if self.head == None:
            return t

        curr = self.head
        while curr != None:
            curr = curr.next
            t += 1

        return t

    def __contains__(self,key):
        '''Return True iff the linked list contains the given data.'''
        if self.head == None:
            return False

        curr = self.head
        while curr != None:
            if curr.data == key:
                return True
            curr = curr.next

        #如果上面那个loop全部出来了也没有return，就说明linked list里没有要找的data
        return False

    def find_min(self):
        '''Ruturn the smallest value in the linked list.'''
        if self.head == None:
            return None

        curr = self.head
        min_v = curr.data

        while curr != None:
            if curr.data < min_v:
                min_v = curr.data #不断比较，不断刷新min_v的值
            curr = curr.next#如果if没进去，就不刷新min_v的值，继续往下比较

        return min_v


    def reverse(self):
        '''Reverse the linked list. 不用recursion写，用loop写。
            [1 2 3]这个例子的话，
            第一次loop，让1后面接上了head的值（此时为None），并且断开了1和2之间的链接，同时assign新的head值，也就是当前curr和后面跟着的值，[1 None]
            第二次loop，让2后面跟上了head的值（此时为1，而1通过第一次loop后面又跟着None），并且断开了2和3之间的链接，同时assign新的head值,[2 1 None]
            第三次loop，让3后面跟上了head的值（此时为2，2后面跟着1，1后面跟着None），[3 2 1 None]
            head是每loop一次都是在不断累积新的值的，从让None跟着第一个元素，让第二个元素跟上第一个元素和None，依次累积。
            一定要画图理解！！'''
        if self.head == None:
            return

        head = None#初始head为None，是为了让linked list里第一个值后面接上None，后面head的值也在不断刷新
        curr = self.head
        while curr != None:
            curr_next = curr.next#一定要在这里先存一个curr.next因为之后curr就会重新赋值，curr.next就变了！现在存的1.next就是2，一会儿1.next就是None了！！！！
            curr.next = head#把新的head的值跟到curr后面，并断开之间的链接（已经断开了链接，curr.next就不再是原来的值了）
            head = curr#之前的head已经用完，此处刷新head的值，此时的head是跟了一串东西的一个node
            curr = curr_next#curr等于之前存的还没变过得下一个我们要reverse的元素，而不是我们后来添加到curr后面的元素
            
        #此时一定要重新assign self.head的值，不然self.head的值还是之前的！！
        self.head = head#当loop进不去说明curr已经是None，已经loop完了整个linked list
        #此时的head就是连着一大串元素的最后一个元素了，所以我们重新assign self.head为当前head，就完成了reverse linked list
            
            
    def __repr__(self):
        if self.head == None:
            return 'None'

        s = ''
        curr = self.head
        while curr != None:
            s += str(curr.data) + ' -> ' #string化curr.data
            curr = curr.next

        s += 'None'
        return s
        

ll = LinkedList()

ll.append('a')
ll.append('b')
ll.append('c')
ll.append('b')
ll.append('d')


#####################################################################################

def merge(n1,n2):
'''
(LinkedNode,LinkedNode)->LinkedNode
合并两个不带壳的linked list node by node， one node from n1， followed by
the other node from n2. 可能会在考试中出现。'''
    if n1 == None:#base case
        return n2
    elif n2 == None:#base case非常重要，因为可能存在给的两个linked list长度不一样
        return n1

    new_n1 = n1.next#这里是n1里除第一个node外剩下所有连着的linked list
    new_n2 = n2.next#这里是n2里除第一个node外剩下所有连着的linked list

    head = n1
    n1.next = n2#n1后面跟着n2

    n2.next = merge(new_n1,new_n2)#n2后面跟着后面一大串已经merge好的以n1的node为起始的linked list

    return head
