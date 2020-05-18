"""
Here we are looking at an n-ary tree (a tree where each node can have
any number of children, not just 0-2 like in a binary tree). So, instead
of storing self.left, self.right, we store self.children which equals to
a list of all its children (each of which are Tree objects themselves).
"""

class Tree:
  '''Tree ADT; nodes may have any number of children'''

  def __init__(self: 'Tree',
               item: object =None, children: list =None):
    '''Create a node with item and any number of children'''

    self.item = item
    if not children:
      self.children = []
    else:
      self.children = children[:]
  
  def __repr__(self: 'Tree') -> str:
    '''Return representation of Tree as a string'''

    if self.children:
      return 'Tree({0}, {1})'.format(repr(self.item), repr(self.children))
    else:
      return 'Tree({})'.format(repr(self.item))

  def is_leaf(self: 'Tree') -> bool:
    '''Return True iff this Tree node is a leaf (has no children).'''

    return self.children == []
  
  def remove_equal(self: 'Tree') -> None:
    '''Remove every child that has the same item as its parent;
    【any children of a removed node n become children of an ancestor of n.】
    parent cannot be equal to child, delete all the child that has the same value as parent.
    其实就是广度优先搜索。
    只要孩子和我一样了，就把我删除，把我的孩子提上来，再用while判断我的孩子，
    如果还有和我一样的就继续把他的孩子提上来一层。
    
    >>> t = Tree(1, [Tree(2, [Tree(1), Tree(2)]), Tree(1)])
    >>> t.remove_equal()
    >>> repr(t)
    'Tree(1, [Tree(2, [Tree(1)])])'
    >>> t = Tree(4, [Tree(4, [Tree(6)])]) 
    >>> t.remove_equal()
    >>> repr(t)
    'Tree(4, [Tree(6)])'
    >>> t = Tree(4, [Tree(4, [Tree(4, [Tree(4)])])])
    >>> t.remove_equal()
    >>> repr(t)
    'Tree(4)'
    >>> t = Tree(4, [Tree(4, [Tree(4, [Tree(6), Tree(7)]), Tree(8)]), Tree(9)])
    >>> t.remove_equal()
    >>> repr(t)
    'Tree(4, [Tree(6), Tree(7), Tree(8), Tree(9)])'
    '''
    if self.is_leaf():
      return

    new_children = []

    #只完成了当前我这层的
    while self.children != []:#不能用for loop here, 因为我们在改变list的structure，structure改变后for loop就执行不了了
      child = self.children.pop(0)#it's a list, as a Queue, FIFO
      if child.item == self.item:
        self.children.extend(child.children)#如果我的孩子等于了我，就直接跳过我的孩子把我的孩子的孩子提上来当做我的孩子，这已经是在往下循环
        child.children = None#然后while loop还在继续往后判断我的孩子list（包括我孩子的孩子）里还有没有和我相等的值
      else:
        new_children.append(child)#把和我不相等的item都添加到一个新的list里，循环到最后这个list会有所有和我不相等的孩子

    self.children = new_children#这不是循环的一部分，这是等while已经处理完所有重复孩子后，重新赋值新的children list

    for child in self.children:#再把我的孩子的孩子（下一层级）做同样操作，现在只处理了我当前这层的。
        child.remove_equal()
        

  def same_child_values(self: 'Tree', other: 'Tree') -> None:
    '''
    Return True iff the other tree node given has all the same values for its children.
    The values do not have to occur the same number of times.
    We are only looking at values of the immediate children, not the descendants.
    只管当前一层的孩子想不想等，同时只管值相等，不管孩子个数想不想等，也不管孩子的孩子相不相等
    
    Hint: Use sets to compare a list of all children keys
    More on sets - https://www.programiz.com/python-programming/set
  
    >>> t = Tree(4, [Tree(6), Tree(7), Tree(8), Tree(9)])
    >>> t2 = Tree(5, [Tree(6), Tree(7, [Tree(8, [Tree(9)])])])
    >>> t3 = Tree(6, [Tree(7), Tree(8), Tree(6), Tree(6), Tree(9)])
    >>> t4 = Tree(7, [Tree(7), Tree(7), Tree(6)])
    >>> t.same_child_values(t2)
    False
    >>> t.same_child_values(t3)
    True
    >>> t4.same_child_values(t2)
    True
    '''
    children_1 = self.children[:]
    children_2 = other.children[:]

    while children_1 != []:
        child_1 = children_1.pop()

        i = 0
        while i < len(children_1): ## remove all nodes which has same value with child_1
            if child_1.item == children_1[i].item:
                children_1.pop(i)
            else:
                i += 1
        # children_1里就没有child_1的value了
                

        flag = False
        i = 0
        while i < len(children_2): # remove all nodes which has same value with child_1
            child_2 = children_2[i]

            if child_1.item == child_2.item:
                children_2.pop[i]
                flag = True
            else:
                i += 1
        # children_2里就没有child_1的value了
                
        
        if not flag: # child_1 not in children_2
            return False

    #remove all values from children_1 in children_2 


    if children_2 != []:# children_2 has more value than children_1
        return False

    return True



# Q3: Complete the path_to_leaves function below
#     This function makes use of both the Tree class and the LLNode class

class LLNode:
  '''LLNode for represting a node in a linked list.'''
  
  def __init__(self, item, nxt=None):
    self.item = item
    self.next = nxt

  def __repr__(self):
    return str(self.item) + " -> " + str(self.next)

  
def path_to_leaves(node):
  '''
  与上面共用了一个tree class
  Return a list of Linked Lists (represented using LLNode objects) that give us
  the paths from the root to all leaves of the tree that starts at the given
  node.
  Each LLNode in the returned list contains a path from the root to a leaf.

  >>> bt = Tree(1, [Tree(2, [Tree(4), Tree(5)]), Tree(3, [Tree(6)])])
  >>> path_to_leaves(bt)
  [1 -> 2 -> 4 -> None, 1 -> 2 -> 5 -> None, 1 -> 3 -> 6 -> None]

  >>> bt = Tree(5, [Tree(6), Tree(7, [Tree(8, [Tree(9)])])])
  >>> path_to_leaves(bt)
  [5 -> 6 -> None, 5 -> 7 -> 8 -> 9 -> None]
  '''
  #这会return一个不包含self的【list of linked list】，那么就要把self加进去
  if node.is_leaf():
    return [LLNode(node.item)]#creat a LLNode here

  all_paths = []
  for child in node.children:
    sub_paths = path_to_leaves(child)#list of linked list
    #的所我孩子的所有path，再把我加到我的每个孩子的path前面
    
    for path in sub_paths:
            new_path = LLNode(node.item, path)
            all_paths.append(new_path)

    return all_paths

  
if __name__ == '__main__':
  import doctest
  doctest.testmod()