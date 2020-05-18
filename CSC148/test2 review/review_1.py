#review

#1
class Node():
    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node


    def merge(self, other):
        self_next = self.next
        other_next = other.next

        self.next = other
        other.next = self_next

        if self_next == None:
            other.next = other_next
            return

        if other_next == None:
            return

        self_next.merge(other_next)

    def remove(self, data):
        if self.next == None:
            return

        if self.next.data == data:
            node = self.next
            self.next = node.next
            node.next = None
            return

        self.next.remove(data)



    def remove_repeating(self):
        if self.next == None:
            return

        self.next.remove_repeating()
        sub = self.next

        if sub.data == self.data:
            self.next = sub.next
            sub.next = None
            return

        curr = sub
        while curr.next != None:
            if curr.next.data == self.data:
                node = curr.next
                curr.next = node.next
                node.next = None
                return

            curr = curr.next



    def index(self, i):
        if i == 0:
            return self.data

        if self.next == None:
            raise IndexError('Index out of range')

        return self.next.index(i-1)
            

    
            

    def equal(self, other):
        if self.dada != other.data:
            return False
        
        if self.next == None and other.next == None:
            return True

        if self.next != None and other.next != None:
            return self.next.equal(other.next)
        else:
            return False
            
        




a = Node(1)
b = Node(2,a)
c = Node(3,b)


class Link_list():
    def __init__(self, head = None):\
        self.head = head


a = Node(1)
b = Node(2,a)
c = Node(3,b)

l = Link_list(c)



class BTNode():
    def __init__(self,data,left=None,right=None):
        self.data, self.left, self.right = data, left, right


    def traverse(self):

        print(self.data)
        
        if self.left != None:
            self.left.traverse()
            
        if self.right != None:
            self.right.traverse()
            
    def is_leaf(self):
        return self.left == None and self.right == None
    
    def __repr__(self):
        if self.is_leaf():
            return "( " + str(self.data) + " )"
        
        return "( "+str(self.data)+","+repr(self.left)+","+repr(self.right)+" )"


r = BTNode(1,BTNode(2) ,BTNode(3, BTNode(4), BTNode(5)))


class BT():
    def __init__(self, root=None):
        self.root = root


bt = BT(r)

###################################################################


class BSTNode():
    def __init__(self,data,left=None,right=None):
        self.data, self.left, self.right = data, left, right

    def is_leaf(self):
        return self.left == None and self.right == None
    
    def __repr__(self):
        if self.is_leaf():
            return "( " + str(self.data) + " )"
        
        return "( "+str(self.data)+","+repr(self.left)+","+repr(self.right)+" )"


    def add(self, data):
        if self.data < data:
            if self.right:
                self.right.add(data)
            else:
                self.right = BSTNode(data)

        elif self.data > data:
            if self.left:
                self.left.add(data)
            else:
                self.left = BSTNode(data)
                

    def delete(self, data):
        
        parent_del = None   #initial
        curr_del = self

        while curr_del != None and curr_del.data != data:
            if curr_del.data > data:
                parent_del = curr_del
                curr_del = curr_del.left
            else:
                parent_del = curr_del
                curr_del = curr_del.right

        if curr_del == None:
            # data not in bst
            return

        #found delete_node and its parent!!!


 
        parent_c = curr_del     #initial
        curr_c = curr_del.left
        
        while curr_c != None and curr_c.right != None:
            parent_c = curr_c
            curr_c = curr_c.right

        if curr_c == None:
            # curr_del dont have left child
            # let parent_del connect  curr_del's right child
            if parent_del.left == curr_del: # find position of curr_del in parent_del
                parent_del.left = curr_del.right
            else:
                parent_del.right = curr_del.right

            curr_del.right = None # deleted 
            return

        # found change_node  and its parent in left subtree of curr_del



        #reset the relation of change_node and its parent
        #let parent_c connect  curr_c's left child   # curr_c has only left child
        if parent_c.left == curr_c: # find position of curr_c in parent_c
            parent_c.left = curr_c.left
        else:
            parent_c.right = curr_c.left
        curr_c.left = None # curr_c is free


        #reset the relation of change_node and delete_node's children
        curr_c.left = curr_del.left
        curr_c.right = curr_del.right
        
        #reset the relation of change_node and delete_node's parent
        if parent_del.left == curr_del: # find position of curr_del in parent_del
            parent_del.left = curr_c
        else:
            parent_del.right = curr_c
        #change_node has finished


       curr_del.left = None
       curr_del.right = None    # curr_del is deleted form BST



    def find_max_node(self):
        if self.right == None:
            return self

        return self.right.find_max_node()


    def _delete(self, data):
        if self.data < data:
            if self.right == None:
                return
            
            elif self.right.data == data:
                delete = self.right
                left_max = delete.left.find_max_node()  

            else:
                self.right._delete(data)

        elif self.data > data:
            if self.left == None:
                return
            
            elif self.left.data == data:
                delete = self.right
                left_max = delete.left.find_max_node()

            else:
                self.left._delete(data)
            

            
        
        
        
        
        



class BST():
    
    def __init__(self, root=None):
        self.root = root


    def add(self):
        if self.root == None:
            self.root = BSTNode(data)
            return


        curr = self.root
        while curr :
            if curr.data < data:
                if curr.right:
                    curr = curr.right
                else:
                    curr.right = BSTNode(data)
                    return
            elif curr.data > data:
                if curr.left:
                    curr = curr.left
                else:
                    curr.left = BSTNode(data)
                    return
        

                

            



















            


