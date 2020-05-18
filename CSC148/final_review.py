#5套CSC148 past final exams的答案
#2016 8月Dan出题的卷子没讲

#csc148 2015 4
#2
def nfibonacciNumber(n):
    if n == 0:
        return 0
    if n == 1:
        return 1

    return nfibonacciNumber(n-1) + nfibonacciNumber(n-2)

def nfibonacciNumber(n):
    if n == 0:
        return 0
    if n == 1:
        return 1

    fn_i_2 = 0
    fn_i_1 = 1
    i = 2 #n等于0和1的时候已经有base case，直接从n等于2开始
    while i<=n:
        fn_i = fn_i_1 + fn_i_2
        fn_i_2 = fn_i_1
        fn_i_1 = fn_i#下一项就是前两项的和

        i += 1

    return fn_i

#4
def has_path_sum(t,total):
    if t.item == total and t.is_leaf():
        return True
    if total - t.item < 0:
        return False

    l = r = False
    if t.left:
        l = has_path_sum(t.left,total - t.item)

    if t.right:
        r = has_path_sum(t.right, total - t.item)

    return l or r


#6
def removeDuplicates(head):
    if not head:
        return

    curr = head
    while curr.next != None:
        if curr.element == curr.next.element:
            curr.next = curr.next.next
        else:
            curr = curr.next


def shuffleMerge(head1, head2):
    if not head1:
        return head2
    if not head2:
        return head1

    curr1 = head1
    curr2 = head2

    while curr1 and curr2:
        c1_next = curr1.next
        c2_next = curr2.next
        
        curr1.next = curr2
        if c1_next:
            curr2.next = c1_next

        curr1 = c1_next
        curr2 = c2_next

        


#2017 04

#1
def muntiply(x,y):
    if x == 1:
        return y
    if y == 1:
        return x

    return y + muntiply(x-1, y)
        


#4
def deepest_ancestor(node1, node2):
    if node1.depth == node2.depth:
        if node1.parent == node2.parent:
            return node1.parent
        else:
            return deepest_ancestor(node1.parent, node2.parent)
    elif node1.depth > node2.depth:
        return deepest_ancestor(node1.parent, node2)
    else:
        return deepest_ancestor(node1, node2.parent)

#5
def all_bigger(root, v):
    if not root:
        return True
    if root.item < v:
        return False
    return all_bigger(root.left, v)


#2015 06
#2
#a
def countBinaryString(s):
    x, y = _countBinaryString(s)
    return y >= x

def _countBinaryString(s):
    if s == "":
        return (0,0)
    x, y = _countBinaryString(s[1:])

    if s[0] == '1':
        y += 1
    else:
        x += 1

    return (x, y)
    

def palindromeStr(s):
    if len(s) <= 1:
        return True

    if s[0] != s[-1]:
        return False

    return palindromeStr(s[1:-1])


#3
def to_node_repr(L):
    return _to_node_repr(L)

def _to_node_repr(L, i = 0):

    if i >= len(L):
        return None

    t = BinaryTree(L[i])
    l_index = 2i + 1
    r_index = 2i + 2

    l_subtree = _to_node_repr(L, l_index)
    r_subtree = _to_node_repr(L, r_index)

    t.left = l_subtree
    t.right = r_subtree

    return t

#e
def sameTrees(tree1, tree2):
    if not tree1 and not tree2:
        return True

    if (tree1 or tree2) and not (tree1 and tree2): #有且只有一个tree
        return False

    if tree1.root != tree2.root:
        return False

    return sameTrees(tree1.left, tree2.left) and \
           sameTrees(tree2.right, tree2.right)



#4
def removeDuplicates(head):#recursive
    if not head.next:
        return head

    sub = removeDuplicates(head.next)#此时的sub已经是一个删掉了所有重复元素的list

    if head.element != sub.element:#看sub的第一位和我一不一样，不一样就把我连上sub，一样的话就断开我和sub之前的关系，return sub
        head.next = sub#我已经有点get这类recursion的套路了，以上来就先recursion，才去处理最外一层的东西
        return head

    head.next = None
    return sub

def areLinkedListsEqual(head1, head2):#non-recursive

    curr1 = head1
    curr2 = head2

    while curr1 and curr2:
        if curr1.element != curr2.element:
            return False

        curr1 = curr1.next
        curr2 = curr2.next

    #从上面那个loop出来，就说明其中一个不存在了
    if curr1 or curr2:
        return False

    #若没进上面那个if，就说明while走完两个linked list都为空并且长度一样，那他们就是一样的linked list，non-recursive的code的结构很重要
    return True
        



#2017 08 Sadia出题的卷子
#4
#b
def is_heap(t):
    if not t:
        return True
    
    if not is_heap(t.left) or not is_heap(t.right):
        return False

    if t.left and t.item <= t.left.item:
        return False

    if t.right and t.item <= t.right.item:
        return False

    return True
 

#5
class DLLNode():
    def __init__(self, data,prev,next):
        self.data = data
        self.prev = prev
        self.next = next
        
class DoublyLinkedList():
    def __init__(self):
        self.head = self.tail = None


    def __len__(self):
        n = 0
        curr = self.head
        while curr:
            n += 1
            curr = curr.next

        return n


#bonus question
def create_tree_from_preorder(lst):
    if lst == []:
        return None
    
    root = BTNode(lst[0])
    
    left_sub = []
    right_sub = []
    for e in lst[1:]:
        if e < lst[0]:
            left_sub.append(e)
        else:
            right_sub.append(e)

    left = create_tree_from_preorder(left_sub)
    right = create_tree_from_preorder(right_sub)

    root.left = left
    root.right = right

    return root




#148 2016 4
#1
def merge(s1,s2):
    if not s1 or not s2:
        return s1+s2

    if s1[0] < s2[0]:
        return s1[0] + merge(s1[1:], s2)
    else:
        return s2[0] + merge(s1, s2[1:])

#5
def postorder(root):
    if not root:
        return None

    l_link = postorder(root.left)
    r_link = postorder(root.right)

    if not l_link and not r_link:
        return LLNode(root.item)

    if l_link:
        head = l_link
        end = head
        while end.link:
            end = end.link
            
        end.link = r_link#连接起来了左右的linked list
        while end.link:
            end = end.link

        #上面这个while结束了就找到了右支linked list的最后
        end.link = LLNode(root.item)
            
    else:
        head = r_link
        end = head
        while end.link:
            end = end.link

        end.link = LLNode(root.item)

    return head

            

def level_nums(t):
    if not t:
        return []

    l_level = level_nums(t.left)#左支的元素个数的list
    r_level = level_nums(t.right)#右支的元素个数的list

    level =[]
    if len(l_level) < len(r_level):#看左支右支哪个的depth更长，要相同depth的左右支的node个数才能相加
        length = len(l_level)#至少能保证左支右支length以前的元素都是同一层的，可以直接加
        long = r_level
    else:
        length = len(r_level)
        long = l_level
                 
    for i in range(length):#至少能保证左支右支length以前的元素都是同一层的，可以直接加
        level.append(l_level[i] + r_level[i])

    level.extend(long[length:])#length之后更深的depth上的元素个数就全部append进list里就可以

    #要把root的一个node的数量加到list里
    level.inesert(0, 1)

    return level



def level_nums_2(t):
    if not t:
        return []

    l_level = level_nums_2(t.left)
    r_level = level_nums_2(t.right)

    level =[]
    length = max(len(l_level),len(r_level))
    
    i = 0
    while i < length:
        n = 0 
        if i < len(l_level):
            n += l_level[i]
        if i < len(r_level):
            n += r_level[i]
        level.append(n)
        
        i += 1

    level.inesert(0, 1)

    return level