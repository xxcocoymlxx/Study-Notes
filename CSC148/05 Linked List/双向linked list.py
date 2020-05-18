#带壳的双向linked list

class Node():
    def __init__(self, data, next_node=None, prev=None):
        '''双向linked list，有next也有previous指向。'''
        self.data = data
        self.next = next_node
        self.prev = prev

    def __str__(self):
        return str(self.data)

class EmptyError(Exception):
    pass

class LinkedList_2():
    def __init__(self):
        self.head = None
        self.tail = None #with pointer to the last 添加东西到linked list最末尾的时候也会快很多，不用再loop一遍找末尾
        self.size = 0
        #在这里添加个attribute记录size，当问这个linked list
        #的长度时就不用每次loop一遍
        #现在每加进一个data，self.size就加1
        #问linked list的长度时直接return self.size就会快很多，runtime就是constant

    def __len__(self):
        return self.size

    def append(self, data):
        '''Add a new data to the end of the linked list.'''
        new = Node(data)
        self.size += 1

        if self.head == None:
            self.head = new
            self.tail = new
            return
        
        self.tail.next = new #注意：现在要更改的就是3层链接
        new.prev = self.tail
        self.tail = new
        return


    def pop(self, index):
        '''Delete the data with given index from the linked list.
            这个pop其实建议写helper function来写，太长了。'''

        #如果是个空的linked list 或者 index大于liked list的长度
        if self.head == None or index >= self.size:
            raise EmptyError()

        #如果要删除的是第一位元素
        if index == 0:
            old = self.head#记录下这个node方便之后断开链接

            self.head = old.next

            old.next = None#断开要删除的node与linked list的链接
            self.head.prve = None

            self.size -= 1

            return old.data

        #如果要删除的是最后一位元素
        if index == self.size-1:
            old = self.tail

            self.tail = old.prev

            old.prev = None#断开链接
            self.tail.next = None

            self.size -= 1

            return old.data

        #如果given index在linked list的前半段（more efficient）
        if index < self.size//2:
            curr = self.head
            curr_index = 0
            while curr != None:
                if curr_index == index:
                    prev_node = curr.prev#这里就可以call个帮助删除和创建链接的function
                    next_node = curr.next
                    
                    prev_node.next = next_node#跳过要删除元素把两个node连接起来
                    next_node.prev = prev_node

                    curr.next = None#断开删除元素与linked list的链接
                    curr.prev = None

                    #这里不用多加一行写self.size -= 1，
                    #因为我们loop的方式会进到base case里
                    #也就是index==0和index=size-1时，在上面那两个if里会减的
                    return curr.data
                
                curr = curr.next#循环起来
                curr_index += 1

        else:#如果given index在linked list的后半段（more efficient）
            curr = self.tail
            curr_index = self.size - 1

            while curr != None:
                if curr_index == index:
                    prev_node = curr.prev
                    next_node = curr.next
                    
                    prev_node.next = next_node#跳过删除元素链接相邻两个node
                    next_node.prev = prev_node

                    curr.next = None#断开删除元素与linked list的链接
                    curr.prev = None

                    return curr.data

                curr = curr.prev
                curr_index -= 1