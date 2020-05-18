'''
这个是没壳的，没壳的才好用recursion。
如果有壳的用recursion就会每次循环都带着壳才不好处理。
In this example, there is no separate Node class.
The LinkedList itself acts like a Node.不要依据class的名字去判断是有壳还是没壳。
So we call the class a LinkedListNode.
这是另外一种结构的linked list，这不是平面式的一个连一个的。
这是一个套一个的嵌套式的linked list。
'''
class LinkedListNode:

    def __init__(self, items=[]):
        """ (LinkedListNode, list) -> None

        Create a new linked list containing the elements in items.
        If items is empty, self.first initialized to EmptyValue.
        把一个普通的list转换成这种嵌套式的linked list。
        """
        if len(items) == 0: # base case: empty list，创建一个空的linked list他的self.first和self.rest就都是None
            self.first = None#整个linked list的最后一位就是一个空的linked list，比如LinkedListNode(3, None)这里None其实就是个空的linked list
            self.rest = None#剩下的一个套一个的linked list node，注意这里的初始self.rest不是一个[],而是None
        else:
            self.first = items[0] #initializes first item，他的first是个data！
            self.rest = LinkedListNode(items[1:]) #creates new list with rest of items，每个item都是一个linked list
            #这就不是水平线平面的,是嵌套式的，相当于之后的每一个item都是以自己为开始的linked list的是self.first
            #>>>LinkedListNode([1,2,3,4,5,6])
            #[1,[2,[3,[4,[5,[6]]]]]]
            

        # We are recursively calling the LinkedListNode constructor in the last line
        # This is because the rest of the list should also be a LinkedListNode itself
        # So now if items = [1, 2, 3], we will end up with something like:
        #     LinkedListNode(1, LinkedListNode(2, LinkedListNode(3, None)))
        # Key idea here:
        # The recursive structure of the LinkedList comes from thinking of the
        # list as a list of the first element, followed by a smaller LinkedList
        # of the rest of the elements
        #   LinkedList = first + smaller LinkedList of the rest


    def __repr__(self: 'LinkedListNode') -> str:
        """Return a detailed str representation of Node.
        """
        if not self.rest: #if self.rest is None
            return 'LinkedListNode({})'.format(repr(self.first))#这里是强行call了一次repr，其实不用的
        else:
            return 'LinkedListNode({}, {})'.format(repr(self.first), repr(self.rest)) 
            # This is recursive; take a few moments to think about how this works
            #So now if items = [1, 2, 3], we will end up with something like:
            #LinkedListNode(1, LinkedListNode(2, LinkedListNode(3, None)))


    def is_empty(self: 'LinkedListNode') -> bool:
        return self.first is None
    
    def __getitem__(self: 'LinkedListNode', index: int) -> object:
        """Return the item at position <index> in this list.
        Raise IndexError if <index> is >= the length of this list.
        """
        # Complete this function recursively
        # Think about this:
        # How is finding an element at a given index in a list,
        # related to finding that index in the REST of the list?
        # e.g.
        # If we want to access the item in position 2 in the list [1,2,3,4,5],（3的index在这里是2）
        # how is this related to accessing an item from the rest
        # of the list, [2,3,4,5]?（3在这里的index就变成了1）

        if self.is_empty():#<index> is >= the length of the list的base case
            raise IndexError
        elif index == 0:
            return self.first
        else:
            return self.rest.__getitem__(index - 1)#每套一次recursion，index就减1，一直减到0，就相当于找到了item（进到了base case）
                    # same as self.rest[index - 1]
                    #__getitem__这个magic method的接口就是这个index的操作，可直接用index notation的方括号
                    
            # recursively call getitem on rest of the list
            # what index would my item be in the rest of the list （index - 1）
            # compared to the original list?

    # Tip on understanding recursion:
    # Think of it using a high-level approach. Don't worry about tracing the code to understand it piece by piece.
    # Instead, trust that the code follows the docstring, and everytime a recursive call occurs, trust that it
    # returns the correct value. IF the correct value is returned, does the final code make sense?

    #参考格式：
    # So now if items = [1, 2, 3], we will end up with something like:
    #     LinkedListNode(1, LinkedListNode(2, LinkedListNode(3, None)))
    def append(self, data):
        '''Add a new data at the end of the linked list using recursion.'''
            #这种嵌套式的linked list的结尾是个空的linked list，self.first为None，self.rest也是None
        if self.rest == None:#当self.rest是None的时候，就找到了最后一个为空的linked list
            self.first = data#给这个空的linked list的self.first赋值
            self.rest = LinkedListNode()#为了不破坏他的嵌套linked list的结构，让他的self.rest再次等于一个空的linked list
            return#就相当于是LinkedListNode(data, LinkedListNode(None，None））

        self.rest.append(data)#他会一次一次的套recursion，直到self.rest是None，就说明已经找到了
        #linked list的最末端，探到了base case


    def find(self, data):
        '''return given data在第几层嵌套。'''
        #如果self.rest是None那self.first也肯定是None，
        #说明已经到了linked list最末端那个空的linked list也没有找到要的data
        if self.rest == None:
            return -1#这里模仿了string，如果没找到要的元素就return-1，其实return什么都行，看你自己

        if self.first == data:
            return 0

        return 1 + self.rest.find(data)#如果不在第一层，就往下再找一层，同时加上这一层的1


    def pop(self, index):
    '''Delete the data with given index from the linked list.
        不带壳的linked list默认不能对第一个元素进行操作，所以默认输入的index>0.'''

        if self.rest == None:#如果是个空linked list
            raise IndexError()

        if index == 1:
            new = self.rest

            self.rest = new.rest
            new.rest = None
            return new.first

        return self.rest.pop(index-1)