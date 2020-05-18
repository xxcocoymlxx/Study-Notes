class BinaryTree:#这是没壳的
    """Binary Tree node."""

    def __init__(self: 'BinaryTree', key: object,
                 left: 'BinaryTree'=None, right: 'BinaryTree'=None) -> None:
        """Create BT node with data and children left and right."""
        self.key, self.left, self.right = key, left, right

    def __repr__(self: 'BinaryTree') -> str:
        """Represent this node as a string."""
        return ('BTNode(' + str(self.key) + ', ' + repr(self.left) +
                ', ' + repr(self.right) + ')')

#The following functions are outside the class   
def expr(tree):
    '''按照（左边的运算 + 运算符号 + 右边的运算）把tree表示出来'''
  if not tree:
    return ''
  s = '(' + expr(tree.left)
  s = s + str(tree.key)
  s = s + expr(tree.right)+')'
  return s

def solve_expr(tree):
  '''
  Given an expression tree, return the solution of the expression
  it represents.
  算完左支的结果，再算完右支的结果，最后以root的运算符号合到一起（post-order）

  NOTE: You may assume the only possible operations are
  +, -, *, and / (i.e. add, subtract, multiply and divide).
  
  >>> t = BinaryTree('1')
  >>> solve_expr(t)
  1

  >>> t = BinaryTree('+', BinaryTree('1'), BinaryTree('2'))
  >>> solve_expr(t)
  3

  >>> t = BinaryTree('+', BinaryTree('*', BinaryTree('1'), BinaryTree('2')), BinaryTree('3'))
  >>> solve_expr(t)
  5
  '''
  if tree.key.isdigit():#第一个元素不是digit就是运算符号"+ - * /"
      return int(tree.key) #base case

  left_result = solve_expr(tree.left)#note:tree.left也是一个tree
  right_result = solve_expr(tree.right)#这两行可以分别得到左支和右支的expression

  if tree.key == '+':
      return left_result + right_result
  elif tree.key == '-':
      return left_result - right_result
  elif tree.key == '*':
      return left_result * right_result
  else:
      return left_result / right_result
      
import doctest
doctest.testmod()
