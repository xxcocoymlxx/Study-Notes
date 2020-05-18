class LinkedNode():
    def __init__(self,data, next_node=None):
        self.data = data
        self.next = next_node


class LinkedList():
    '''把一些基本的queue会用到的method添加进来。'''
    def __init__(self):
        self.head = None

    def append(self, data):
        if self.head == None:
            self.head = LinkedNode(data)
            return

        curr = self.head
        while curr.next != None:
            curr = curr.next#找到linked list的最末端

        curr.next = LinkedNode(data)


    def pop(self, index):
        if self.head == None:
            raise IndexError("Linked list index out of range")

        if index == 0:
            old = self.head
            self.head = old.next
            old.next = None
            return old.data
        
        parent = self.head
        curr = self.head.next
        curr_index = 1
        while curr != None:
            if curr_index == index:
                parent.next = curr.next
                curr.next = None
                return curr.data

            parent = curr
            curr = curr.next
            curr_index += 1
            

        raise IndexError("Linked list index out of range")


    def __len__(self):
        t = 0
        if self.head == None:
            return t

        curr = self.head
        while curr != None:
            curr = curr.next
            t += 1

        return t


class EmptyQueueError(Exception):

    """An exception raised when attempting to dequeue from an empty queue.
    """

    pass


class Queue():
    '''这个装data的容器是个linked list而已，只是尊崇了Queue先进先出的性质而已。'''
    def __init__(self):
        self.items = LinkedList()#建立个queue就是建立个空的linked list，不需要加什么parameters，之后可以慢慢加元素进去

    def enqueue(self, data):
        self.items.append(data)#append东西进linked list时会在linked list里创建node的，只用给data就好

    def dequeue(self):
        if self.is_empty():
            raise EmptyQueueError()
        
        return self.items.pop(0)#先进先出

    def is_empty(self):
        return self.items.head == None#这里self.items就是个linked list

    def front(self):
        if self.is_empty():
            raise EmptyQueueError()

        return self.items.head.data#若一开始linked list没有东西，第一个加进去的东西会自动被设为head的