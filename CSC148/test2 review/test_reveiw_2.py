#2016 sumer

#3
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


def merge(l1, l2):
    if l2 == None:
        return

    new = Node(l2.value)
    new.next = l1.next
    l1.next = new

    merge(new.next, l2.next)

#4
class Tree:
    def __init__(self: 'Tree',value: object =None, children: list =None):
        self.value = value
        if not children:
            self.children = []
        else:
            self.children = children[:]

def nonleaf_count(t):
    if t.children != []:
        return 0

    t = 1
    for c in t.children:
        t += nonleaf_count(c)
    return t
    

#2016 Fall

#2
class BTNode:
    def __init__(self: 'BTNode', item: object,
        left: 'BTNode' =None, right: 'BTNode' =None) -> None:
        """Initialize this node."""
        self.item, self.left, self.right = item, left, right

def longest_path(t):
    if not t:
        return []

    left = longest_path(t.left)
    right = longest_path(t.right)

    if len(left) > len(right):
        left.insert(0, t.item)
        return left

    right.insert(0, t.item)
    return right

t = BTNode(1, BTNode(2,BTNode(3)),BTNode(4,BTNode(5),BTNode(6,BTNode(7))))



#3
class Node:
    """Node in a linked list"""
    def __init__(self: 'Node', value: object, next: 'Node'=None) -> None:
    """Create Node self with data value and successor next."""
        self.value, self.next = value, next


class LinkedList:
    """Collection of Nodes to form a linked list"""
    def __init__(self: 'LinkedList') -> None:
        """Create empty LinkedList"""
        self.front, self.back, self.size = None, None, 0


    def repeat_items(self: 'LinkedList') -> None:
        """Repeat each item in LinkedList self."""

        if self.size == 0:
            return

        curr = self.front
        while curr != None:
            new = Node(curr.value, curr.next)
            curr.next = new

            self.size  += 1
            curr = new.next

        #self.back = self.back.next
        self.back = new


    def repeat_items_2(self: 'LinkedList') -> None:
        """Repeat each item in LinkedList self."""
        
        repeat(self.front)
        self.size *= 2
        self.back = self.back.next
        

        

def repeat(node):
    if not node:
        return

    new = Node(node.value, node.next)
    node.next = new

    repeat(new.next)
    





#2
def is_plex(s: str) -> bool:
    '''Return True iff s is a plex according to the above rules.
    '''
    if s == "0" or s == "1":
        return True

    if s[0] == "+": 
        return is_plex(s[1:])
    if s[0] == "(" and s[-1] == ")" and s.find("+") != -1:

        if "(" not in s[1:-1]:
            # +0+1
            return is_plex(s[1:s.find('+')]) and  is_plex(s[s.find('+')+1:-1])
        
        s1 = 0
        s2 = 0
        for i in range(1,len(s)-1):
            if s[i]=="(":
                s1 +=1
            if s[i]==")":
                s2 +=1

            if s1 == s2 and s1 != 0:
                index = i + 1
                return is_plex(s[1:index]) and  is_plex(s[index+1:-1])

    return False 

    #"((1+1)+(0+(1+0)))+(1+1)"

#3
class BTNode:
    '''A node in a binary tree.'''
    def __init__(self: 'BTNode', item: object,
        left: 'BTNode'=None, right: 'BTNode'=None) -> None:
        '''Initialize this node.'''
        self.item, self.left, self.right = item, left, right

def remove_leaves(t):
    if not t:
        return None
    
    if t.left == t.right == None:
        return None

    t.left = remove_leaves(t.left)
    t.right = remove_leaves(t.right)


#4
class LinkedList:
    '''Linked list class'''
        def __init__(self: 'LinkedList', head: object=None,
            rest: 'LinkedList'=None) -> None:
            '''Create a new LinkedList.
            head - first element of linked list
            rest - linked list of remaining elements
            The empty linked list has head None
            '''
            # a linked list is empty if and only if it has no head
            self.empty = head is None
            if not self.empty:
                self.head = head
                if rest is None:
                    self.rest = LinkedList()
                else:
                    self.rest = rest

                    
    def prepend(self: 'LinkedList', newhead: object) -> None:
        '''Add new head to front of LinkedList'''
        if not self.empty:
            temp = LinkedList(self.head, self.rest)
        else:
            temp = LinkedList()
            
        self.head = newhead
        self.rest = temp
        self.empty = False

        
    def append(self: 'LinkedList', newlast: object) -> None:
        '''Add newlast to end of LinkedList'''
        #1
        curr = self
        while not curr.empty:
            curr = curr.rest

        curr.head = newlast
        curr.rest = LinkedList()

##        #2
##        if self.empty:
##            self.head = newlast
##            self.rest = LinkedList()
##
##        curr = self
##        while not curr.rest.empty:
##            curr = curr.rest
##
##        temp = LinkedList(newlast, curr.rest)
##        curr.rest = temp

        
#########################################
#reverse
class Node():
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

    def __repr__(self):
        if self.next == None:
            return str(self.data)

        return str(self.data) + " -> " + repr(self.next)

    def reverse(self):
        if self.next == None:
            return self

        new_link = self.next.reverse()

        curr = new_link
        while curr.next != None:
            curr = curr.next

        curr.next = self

        return new_link


n1 = Node(1)
n2 = Node(2,n1)
n3 = Node(3,n2)
l = Node(4,n3)
            















    
