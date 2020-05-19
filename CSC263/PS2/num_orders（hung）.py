'''
CSC263 Winter 2019
Problem Set 2, Question 2  Starter Code
University of Toronto Mississauga
'''

# Do NOT add any "import" statements

def combination(n,k):
  permutation = 1#nCk = nPk/k!
  factorial = 1
  for i in range(k):
    permutation *= n-i
    factorial *= i+1

  return permutation//factorial


class BTNode():
  def __init__(self, data):
    self.data = data
    self.r = None
    self.l = None

  def insert(self, data):
    if self.data < data:
      if self.r == None:
        self.r = BTNode(data)
      else:
        self.r.insert(data)
    else:
      if self.l == None:
        self.l = BTNode(data)
      else:
        self.l.insert(data)



        
def size(root):
  if root == None:
    return 0
  return 1 + size(root.l) + size(root.r)



def num_order_trees(root):
    if root == None:
      return 0
    if root.r == root.l == None:
      return 1
    
    l_order = max(1, num_order_trees(root.l))#找到左子树的同形数量
    r_order = max(1, num_order_trees(root.r))#找到左子树的同形数量

    l_size = size(root.l) #左子树节点个数
    r_size = size(root.r) #右子树节点个数
    
    combination_lr = combination(l_size + r_size, r_size) #节点交叉排列的数量
    #print(l_order, r_order, combination_lr)
    return l_order*r_order*combination_lr
    
    


def num_orders(lst):
  # TODO: implement this function
  if lst == []:
    return 0

  r = BTNode(lst[0])
  for i in range(1, len(lst)):
    r.insert(lst[i])

  return num_order_trees(r)
  
  
'''
if __name__ == '__main__':

  # some small test cases
  # Case 1
  assert 2 == num_orders([2, 1, 3])
  # Case 2
  assert 8 == num_orders([4, 2, 1, 5, 3])
  assert num_orders([5,2,1,3,4,6,7])  == 45

  assert num_orders([4,2,1,3,6,5,7])  == 80
  assert num_orders([5,5,5,4,3,2,1,5,5,5]) == 20
  assert num_orders([1,3,2,5,4,7,6,9,8]) == 105
  assert num_orders([50,25,30,1,2,3,4,5,6,7,8,10,40,24,53,4]) == 8190
  assert num_orders([6,5,4,6,5,4,3,2,6,7,6,5,4,3,2,1]) == 2316600
  '''
