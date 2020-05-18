class BTNode:
    """Binary Tree node."""

    def __init__(self: 'BTNode', data: object,
                 left: 'BTNode'=None, right: 'BTNode'=None) -> None:
        """Create BT node with data and children left and right."""
        self.data, self.left, self.right = data, left, right

    def __repr__(self: 'BTNode') -> str:
        """Represent this node as a string."""
        return ('BTNode(' + str(self.data) + ', ' + repr(self.left) +
                ', ' + repr(self.right) + ')')

#################################outsize the class############################################
def find_min(t):#t is a node
    '''这相当于是在binary tree里找最小值，
       我们写helper function是为了判断bst！
       所以现在还不能直接使用bst的性质来找最小值！'''
    ans = t.data
    if t.left:
        ans = min(ans, find_min(t.left))
    if t.right:
        ans = min(ans, find_min(t.right))
    return ans #这里不用再对ans作比较是因为他自己已经刷新成最小的值了

def find_max(t):
    ans = t.data
    if t.left:
        ans = max(ans, find_max(t.left))
    if t.right:
        ans = max(ans, find_max(t.right))
    return ans

def is_bst(t):
    if not t:
        return True

    return (not t.left or find_max(t.left) < t.data) and \
           (not t.right or find_min(t.right) > t.data) and \
           is_bst(t.left) and is_bst(t.right)

t = BTNode(5, BTNode(4, BTNode(3, BTNode(1))), BTNode(90))
print(is_bst(t))
