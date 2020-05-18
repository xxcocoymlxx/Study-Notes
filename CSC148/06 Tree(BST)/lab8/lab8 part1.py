 """
For this part of the lab, we are dealing with an n-ary tree
(a tree where each node can have any number of children, not just
0-2 like in a binary tree). So, instead of storing self.left, self.right,
we store self.children which equals to a list of all its children
(each of which are Tree objects themselves).

In this particular implementation, we are also keeping track of the parent
node of each node in the Tree.
"""
#不带壳的
class Tree:
  '''A Tree ADT, that keeps track of parent and children of each node.'''

  def __init__(self: 'Tree',
               item: object =None, parent: 'Tree' = None, children: list =None):
    '''Create a node with item and any number of children'''

    self.item = item
    self.parent = parent
    if not children:
      self.children = []
    else:
      self.children = children[:] 

  def __repr__(self: 'Tree') -> str:
    '''Return representation of Tree as a string'''

    if self.children:
      return 'Tree({0}, {1})'.format(repr(self.item),repr(self.children))
    else:
      return 'Tree({})'.format(repr(self.item))

def path_from_root_as_list(t: 'Tree') -> list:
    '''Return a list of all the items that we would look at
    along the path from the root to self, in sequential order.
    把从root到t的path，经过的node的item放进一个list里'''
    if not t:
      return []
    
    acc = []
    if not t.parent:
      acc.append(t.item)
      return acc
    elif t.parent:
      acc += path_from_root_as_list(t.parent)#this function will return a list of path of the parent
      acc.append(t.item)
      return acc
      

def path_from_root_as_nodes(t: 'Tree') -> 'Tree':
    '''Return a Tree that contains all the nodes we would have to look at
    along the path from the root to self.
    把path上的node的值组成一个新的链条式的tree'''     
      #method 1, by calling the helper function above
       p = path_from_root_as_list(t)
       root = Tree(p.pop(0))

       parent = root
       while p != []:
         child = Tree(p.pop(0), parent)#create child and connect child to parent
         parent.children.append(child)#connect parent to child
         parent = child#循环起来

       return root

      #method 2, as a independent function
      if t.parent == None:
        return Tree(t.item)
      
      root = path_from_root_as_nodes(t.parent)#root is an complete tree without self，只要再把self加进去就好
      #recursion, 有几层就进行几次recursion，一直到base case
      #每次得到一个root，一个root和一个root连接，最后return出来一个连接的tree
      #记得每次进行recursion都是call了一次这个整个function
      #探到底抓到值之后就会进行上一层的剩下的function部分
      #也就是创建node和连接父亲和孩子，一层一层这样套出来
      #一层一层链接出来，就是个完整的tree
      curr = root
      while curr.children != []:
        curr = curr.children[0]

      #能到这里就说明curr.children已经是[]了
      new = Tree(t.item, curr)#connect self with parent
      curr.children.append(new)#connect parent with self

      return root
         
  
# Making a Tree
# Q1: What does this tree look like after all the code below is executed?
#    Draw a visual representation of this tree, and then print the tree to see
#    if the text representation matches your drawing.

t1 = Tree(1) # start with no children
child_values = [2, 3, 4]
for v in child_values:
    t1.children.append(Tree(v, t1)) # add in child, with parent t1
t1.children[0].children.append(Tree(20, t1.children[0]))
t1.children[0].children.append(Tree(21, t1.children[0]))

t2 = Tree(30, t1.children[1])
t1.children[1].children.append(t2)
t2.children.append(Tree(300, t2))

# Printing path from root to each node
# Q2: Complete the path_from_root_as_list function above so the following
#     statements print the expected values.
#print(path_from_root_as_list(t1.children[0])) # Expected: [1, 2]
#print(path_from_root_as_list(t1.children[1])) # Expected: [1, 3]
#print(path_from_root_as_list(t1.children[1].children[0])) # Expected: [1, 3, 30]
#print(path_from_root_as_list(t1.children[1].children[0].children[0])) # Expected: [1, 3, 30, 300]

# Q3: Complete the path_from_root_as_nodes function above so we get Tree representations of the above.