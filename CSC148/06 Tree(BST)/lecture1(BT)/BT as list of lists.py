# A binary tree (BT) is None or a list of three elements

def binary_tree(value):
  '''(value) -> BT
  Create BT with value as root and no children.
  '''
  return [value, None, None]
  
def insert_left(bt, value):#bt就只是个list of 3 elements
  '''(BT, value) -> NoneType
  Insert value as the left node of the root of bt.如果root已经有左支，强行把现有的
  左支变成加进去的value的更下一级左支。
  '''
  if not bt:#如果bt不存在
    raise ValueError('cannot insert into empty tree')

  #bt的1号为就只有两种可能，要么就是None，要么就是个list of 3 elements
  left_branch = bt.pop(1)  # [3, [5, None, None], None]

  if not left_branch:#if left_branch is None
    bt.insert(1,[value,None, None])#在bt的1号位置insert进这个list of 3 elm（insert是List本身的method）
  else:#如果bt的1号位已经有个list of 3 elm了
    bt.insert(1,[value, left_branch,None])#强行把given value变成了root的左支
    #原本的left_branch变成了given value的左支（往下移了一层）
  


def insert_right(bt, value):
  '''(list representing bt, object) -> None
  Insert value as the right node of the root of bt.
  '''
  if not bt:
    raise ValueError('cannot insert into empty tree')

  right_branch = bt.pop(2)  # [8, None, None]
  
  if not left_branch：
    bt.insert(2,[value,None, None])
  else：
    bt.insert(2, [value, None, right_branch])
    

def contains(bt, value):
    '''(list representing bt, object) -> bool
    Return True iff the given tree with root of bt
    contains the given value.
    '''
    if not bt:
        return False
    
    return bt[0] == value or \
           contains(bt[1], value) or \
           contains(bt[2], value)

def preorder():
  '''return a list of node values in preorder'''
  pass

def inorder():
  '''return a list of node values in inorder'''
  pass

def postorder():
  '''return a list of node values in postorder'''
  pass