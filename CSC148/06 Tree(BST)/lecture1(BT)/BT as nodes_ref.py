class BinaryTree:#tree可以带壳也可以不带壳，这里的是不带壳的
  
  def __init__(self, value): 
    self.key = value
    self.left = None 
    self.right = None 

  def insert_left(self, value):
    if not self.left:#如果左支is None
      self.left = BinaryTree(value)
    else: 
      t = BinaryTree(value)
      t.left = self.left#左边有东西的话，强行插一个进去，让原本的左支等于插进去的value的左支
      self.left = t

  def contains(self, value):
    '''Return True iff value appears as some key in tree.'''

    '''SOLUTION ONE'''
    if self.key == value:
      return True
    if self.left: 
      found = self.left.contains(value)
      if found: # why do we need this?
        return True#还不能直接return found之类的，因为found可以是T/F，如果找了右支是个F，还没找左支就给return了
      # why won't return self.left.contains(value) work?
      # answer: No，because then we only return False or True based on
      #         the left side, and fail to check the right side
    if self.right:
      found = self.right.contains(value)
      if found:
        return True     

    return False#如果左支和右支都不存在，两个if都进不去，就会直接return False
    #就算左支和右支存在了，进去了第一个if，里面的if进不去（没找到value）的话
    #同样回到最下面这个return False
    #otherwise，如果左支/右支存在了，其中任何一个找到了value，都会直接return True

    '''SOLUTION TWO (wrong)'''
    # Why doesn't the code below work?
    # What does the previous one considered that this doesn't?
    return self.key == value or self.left.contains(value) or \
           self.right.contains(value)
    #这里没有check左支/右支有没有值，如果左支/右支是None，就会出error，base case没有写好

    '''SOLUTION THREE'''#这里就判断了为不为None的情况，这个就OK
    return self.key == value or (self.left != None and self.left.contains(value)) \
           or (self.right != None and self.right.contains(value))


def preorder(t):
  '''(BinaryTree) -> list
      RECURSION
      middle -> left -> right'''
  #他这个是在node class外面写的，就不用判断为不为空
  if not t:
    return []

  return [t.key] + preorder(t.left) + preorder(t.right)#如果是其他order就换下顺序就好
  #以一个list形式return，所以base case（root）就自己加一个list的方括号
  #后面的东西也会以list的形式return出来，所以三个东西可以用加号合并
  #整体都按照[中 左 右]的顺序排列，第一层是[root, 左支，右支]
  #左支右支又分别都按照[中 左 右]的顺序排列
