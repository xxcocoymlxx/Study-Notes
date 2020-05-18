#Linklist

class Node():
    def __init__(self,data, next_node=None):
        self.data = data
        self.next = next_node



    def append_node(self, data):
        if self.next == None:
            self.next = Node(data)
            return

        self.next.append_node(data)
        

    def insert_node(self,index, data):
        if index == 1:
            new = Node(data)
            new.next = self.next
            self.next = new
            return
        
        if self.next == None:
            self.next = Node(data)
            return

        self.next.insert_node(index-1, data)


    def pop(self, index):
        if self.next == None:
            raise IndexError('LinkList index out range')
        
        if index == 1:
            node = self.next
            self.next = node.next
            node.next = None
            return node.data
 

        self.next.pop(index-1)
            
            
    
    def __len__(self):
        if self.next == None:
            return 1

        return 1 + len(self.next)

    def __contains__(self,key):
        if self.data == key:
            return True
        if self.next == None:
            return False

        return key in self.next

    def find_max(self):
        if self.next == None:
            return self.data

        curr_max = self.next.find_max()

        if curr_max < self.data:
            return self.data
        return curr_max

    def reverse(self):
        if self.next == None:
            return self

        head_node = self.next.reverse()
        self.next.next = self
        self.next = None

        #head_node.append_node(self.data)  #build new node

        return head_node

    
    
    def __repr__(self):
        if self.next == None:
            return str(self.data) + ' -> None'

        s = str(self.data) + ' -> '

        return s + str(self.next)


#############################################################################



class LinkNode():
    def __init__(self,data,next_node=None):
        self.data = data
        self.next = next_node


class LinkList():
    def __init__(self):
        self.head = None


    def append(self, data):
        if self.head == None:
            self.head = LinkNode(data)
            return

        curr = self.head
        while curr.next != None:
            curr = curr.next

        curr.next = LinkNode(data)



    def insert(self, index, data):
        if self.head == None:
            self.head = LinkNode(data)
            return

        if index == 0:
            old = self.head
            new = LinkNode(data)
            new.next = old
            self.head = new
            return
        

        parent = self.head
        curr = self.head.next
        while curr != None and index != 1:
            parent = curr
            curr = curr.next
            index -= 1


        new = LinkNode(data)
        parent.next = new
        new.next = curr



    def remove(self, data):
        if self.head == None:
            return

        if self.head.data == data:
            old = self.head
            self.head = self.head.next
            old.next = None
            return


        parent = self.head
        curr = self.head.next
        while curr != None:
            if curr.data == data:
                parent.next = curr.next
                curr.next = None
                return

            parent = curr
            curr = curr.next


    def pop(self, index):
        if self.head == None:
            raise IndexError("Linklist index out range")

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
            

        raise IndexError("Linklist index out range")


    def __len__(self):
        t = 0
        if self.head == None:
            return t

        curr = self.head
        while curr != None:
            curr = curr.next
            t += 1

        return t

    def __contains__(self,key):
        if self.head == None:
            return False

        curr = self.head
        while curr != None:
            if curr.data == key:
                return True

            curr = curr.next

        return False

    def find_min(self):
        if self.head == None:
            return None

        curr = self.head
        min_v = curr.data

        while curr != None:
            if curr.data < min_v:
                min_v = curr.data

            curr = curr.next

        return min_v


    def reverse(self):
        if self.head == None:
            return


        head = None
        curr = self.head
        while curr != None:
            curr_next = curr.next
            
            curr.next = head
            head = curr

            curr = curr_next
            

        self.head = head
            
            
            
    def __repr__(self):

        if self.head == None:
            return 'None'

        s = ''
        curr = self.head
        while curr != None:
            s += str(curr.data) + ' -> '
            curr = curr.next


        s += 'None'
        return s
        

ll = LinkList()

ll.append('a')
ll.append('b')
ll.append('c')
ll.append('b')
ll.append('d')


#####################################\



def merge(n1,n2): # l1 and l2 are node
    if n1 == None:
        return n2
    elif n2 == None:
        return n1


    new_n1 = n1.next
    new_n2 = n2.next

    head = n1
    n1.next = n2

    n2.next = merge(new_n1,new_n2)

    return head

    






