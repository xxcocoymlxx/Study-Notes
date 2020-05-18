class NNode():
    def __init__(self, data, children = []):
        self.data = data
        self.children = children


    def __repr__(self):
        return str(self.data)



class BT():
    def __init__(self, root = None):
        self.root = root

class Node():
    def __init__(self, data, left = None, right = None):
        self.data =  data
        self.left = left
        self.right = right



    def has_element(self, data):
        if self.data == data:
            return True

        if self.is_leaf():
            return False
        return self.left.has_element(data) or self.right.has_element(data)
    
    def find(self, data):
        if self.data == data:
            return self

        if self.is_leaf():
            return None

        result_left = self.left.find(data)
        result_right = self.right.find(data)
        
        if result_left != None:
            return result_left
        elif result_right != None:
            return result_right
        return None
    
    def get_max(self):
        if self.is_leaf():
            return self.data

        return max(self.data, self.left.get_max(), self.right.get_max())


    def get_all_over(self, data):
        l = []
        if self.data > data:
            l.append(self.data)

        if self.is_leaf():
            return l

        if self.left:
            result_left = self.left.get_all_over(data)
        else:
            result_left = []

        if self.right:
            result_right = self.right.get_all_over(data)
        else:
            result_right = []

        l.extend(result_left)
        l.extend(result_right)

        return l


    def get_sum(self):
        if self.is_leaf():
            return self.data

        return self.data + self.left.get_sum() + self.right.get_sum()

    def pre_order(self) :#traversal
        if self.is_leaf():
            return [self.data]

        if self.left != None:
            result_left = self.left.pre_order()
        else:
            result_left = []
            
        if self.right != None:
            result_right = self.right.pre_order()
        else:
            result_right = []

        return  [self.data] + result_left + result_right # order

    def height(self):
        if self.is_leaf():
            return 0
        
        if self.left != None:
            result_left = self.left.height()
        else:
            result_left = -1

        if self.right != None:
            result_right = self.right.height()
        else:
            result_right = -1


        return 1 + max(result_left, result_right)


    def is_leaf(self):
        return self.left == None and self.right == None
    


    def __str__(self):
        pass



###################################

class BSTNode():
    def __init__(self,data, l =None. r = None):
        self.data = data
        self.left = l
        self.right = r

    def __repr__(self):
        return str(self.data)

    def is_leaf(self):
        return self.left == None and self.right == None

    def longest(self):

        if self.is_leaf():
            return [self.data]


        if self.left != None:
            left = self.left.longest()
        else:
            left = []

        if self.right != None:
            right = self.right.longest()
        else:
            right = []
            
        if len(left) < len(right):
            long =  right
        else:
            long = left

        long.insert(0, self.data)
        return long

    def get_max(self):
        if self.right == None:
            return self
        
        return self.right.get_max()

    def find(self, data):
        if self.data == data :
            return self

        if self.is_leaf():
            return None

        if data < self.data:
            return self.left.find(data)
        else:
            return self.right.find(data)

    def insert(self, data):
        
        if self.data < data:
            if self.right == None:
                self.right = Node(data)
            else:
                self.right.insert(data)
        else:
            if self.left == None:
                self.left = Node(data)
            else:
                self.left.insert(data)

    def delete(self, data):
        
        if self.data == data:
            if self.right == None:
                return self.left
            elif self.left == None:
                return self.right
            else:
                parent = self
                curr = self.left
                while curr.right != None:
                    parent = curr
                    curr = curr.right

                if parent.left = curr:
                    parent.left = curr.left
                else:
                    paren.right = curr.left

                curr.left = self.lelf
                curr.right = self.right
                self.left = None
                self.right = None
                return curr
                

        elif self.data < data:
            self.right = self.right.delete(data)
        else:
            self.left = self.left.delete(data)
                        
        return self
    
    

        
class BST():
    def __init__(self, root = None):
        self.root = root

    def height(self):
        if self.root == None:
            return 0
        
        if self.root.is_leaf():
            return 1

        left_tree = BST(self.root.left)
        right_tree = BST(self.root.right)
        
        return 1 + max(left_tree.height() , right_tree.height())


    def longest_path(self):
        if self.root == None:
            return []

        if self.root.is_leaf():
            return [self.root.data]


        left_tree = BST(self.root.left)
        right_tree = BST(self.root.right)

        left = left_tree.longest_path()
        right = right_tree.longest_path()
        
        if len(left) < len(right):
            longest = right
        else:
            longest = left
        
        longest.insert(0, self.root.data)
        return longest


    def get_max(self):
        curr = self.root

        while curr.right != None:
            curr = curr.right

        return curr.data

    def get_max_r(self):
        if self.root == None:
            return None
        if self.root.right == None:
            return self.root.data
        t = BST(self.root.right)
        return t.get_max_r()


    def find(self, data):
        curr = self.root

        while curr != None:
            if curr.data == data:
                return curr
            
            if curr.data < data:
                curr = curr.right
            else:
                curr = curr.left

    def find_r(self, data):
        if self.root == None:
            return None

        if self.root.data == data:
            return self.root

        if self.root.is_leaf():
            return None

        if self.root.data > data:
            left_tree = BST(self.root.left)
            return left_tree.find_r(data)

        else:
            right_tree = BST(self.root.right)
            return right_tree.find_r(data)
        

    def insert(self, data):
        if self.root == None:
            self.root = Node(data)

        curr = self.root
        while curr != None:
            if curr.data < data:
                parent = curr
                curr = curr.right

            else:
                parent = curr
                curr = curr.left

        if parent.data < data:
            parent.right = Node(data)

        else:
            parent.left = Node(datahun)

    def insert_r(self, data):
        if self.root == None:
            self.root = Node(data)
            return

        if self.root.data > data:
            if self.root.left == None:
                self.root.left = Node(data)
            else:
                left_tree = BST(self.root.left)
                left_tree.insert_r(data)

        else:
            if self.root.right == None:
                self.root.right = Node(data)
            else:
                right_tree = BST(self.root.right)
                right_tree.insert_r(data)

                


    def delete(self, data):
        #set position
        parent = None
        target = self.root

        while target.data != data and target != None:
            parent = target
            if target.data < data:
                target = target.right
            else:
                target = target.left

        if target == None: # target not exist
            return

    
        if target.left == None:
            if parent == None:
                self.root = target.right
            elif parent.data < data:
                parent.right = target.right
            else:
                parent.left = target.right

            target.right = None
            
        elif target.right == None:
            if parent == None:
                self.root = target.left
            elif parent.data < data:
                parent.right = target.left
            else:
                parent.left = target.left

            target.right = None

        else:
            curr_parent = target
            curr = target.left

            #find ledf max
            while curr.right != None:
                curr_parent = curr
                curr = curr.right

            # set curr node link
            if parent.right == curr:
                parent.right = curr.left
            else:
                parent.left = curr.left
            curr.left = None

            # copy target link
            curr.left = target.left
            curr.right = target.right

            if parent == None:
                self.root = curr
            elif parent.data < target.data:
                parenet.right = curr
            else:
                parent.left = curr
        
            target.left = None
            target.right = None
        
        
                










        

        
