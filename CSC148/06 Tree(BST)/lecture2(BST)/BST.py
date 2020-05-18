"""binary search tree ADT"""

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

    def is_leaf(self: 'BTNode') -> bool:
        """Return True iff BTNode is a leaf"""
        return not self.left and not self.right
    
#有壳的
class BST:
    """Binary search tree."""

    def __init__(self: 'BST', root: BTNode=None) -> None:
        """Create BST with BTNode root.
            BST所有的左支都小于中间，所有的右支都大于中间。"""
        self._root = root

    def __repr__(self: 'BST') -> str:
        """Represent this binary search tree."""
        return 'BST(' + repr(self._root) + ')' #这里的repr是node class的repr

    def find(self: 'BST', data: object) -> BTNode:
        """Return node containing data, otherwise return None."""
        return _find(self._root, data) # return Node where data occurs

#问：这种helper function是相当于把壳拆了的写法吗？是的，带壳的tree是不好用recursion写的，input是BST
#他在外面写个helper function，input直接就是个node，所以就可以使用recursion

#问：这种helper function都是写在class外面？ 答：doesn't matter，也可写在class的function里面
def _find(node: BTNode, data: object):
    """Return the node containing data, or else None."""
    if not node or node.data == data:#base case
        return node
    else:
        if (data < node.data):
            return _find(node.left, data)#一直套recursion，直到进入base case为止
        else:
            return _find(node.right, data)

    
    def insert(self: 'BST', data: object) -> None:
        """Insert data, if necessary, into this tree.

        >>> b = BST()
        >>> b.insert(8)
        >>> b.insert(4)
        >>> b.insert(2)
        >>> b.insert(6)
        >>> b.insert(12)
        >>> b.insert(14)
        >>> b.insert(10)
        >>> b
        BST(BTNode(8, BTNode(4, BTNode(2, None, None), BTNode(6, None, None)),\
 BTNode(12, BTNode(10, None, None), BTNode(14, None, None))))
    """
        self._root = _insert(self._root, data) #在class里面的function一般只是重新赋值，不return


def _insert(node: BTNode, data: object) -> BTNode:
    """Insert data in BST rooted at node, if necessary,
    and return 添加完了data的 root."""
    return_node = node #把input的node为root的一个tree添加data，最后要return node，所以现在把他存下来
    if not node: #如果没有node，就创建了个新的node，直接return这个node
        return_node = BTNode(data)
    elif data < node.data:
        node.left = _insert(node.left, data)#在node的左支insert进data
    elif data > node.data:
        node.right = _insert(node.right, data)#在node的右支insert进data
    else:  # 如果data已经存在在tree里面？
        pass# nothing to do
    return return_node#此时已经是self.left或者self.right被modified过得node了


    def delete(self: 'BST', data: object) -> None:
        """Remove, if there, node containing data.

        >>> b = BST()
        >>> b.insert(8)
        >>> b.insert(4)
        >>> b.insert(2)
        >>> b.insert(6)
        >>> b.insert(12)
        >>> b.insert(14)
        >>> b.insert(10)
        >>> b.delete(12)
        >>> b
        BST(BTNode(8, BTNode(4, BTNode(2, None, None), BTNode(6, None, None)),\
 BTNode(10, None, BTNode(14, None, None))))
        >>> b.delete(14)
        >>> b
        BST(BTNode(8, BTNode(4, BTNode(2, None, None), BTNode(6, None, None)),\
 BTNode(10, None, None)))
        """
        self._root = _delete(self._root, data)


def _delete(node: BTNode, data: object) -> BTNode:
    """Delete, if exists, node with data and return resulting tree."""
    # Algorithm for _delete:
    # 1. If this node is None, return that
    # 2. If data is less than node.data, delete it from left child and
    #     return this node
    # 3. If data is more than node.data, delete it from right child
    #     and return this node
    # 4. If node with data has fewer than two children,
    #     and you know one is None, return the other one
    # 5. If node with data has two non-None children,
    #     replace data with that of its largest child in the left subtree,
    #     and delete that child, and return this node.
    #    左支最大值吗或者右支最小值（左支最大值一定没有右孩子，所以直接删除和替换）
    return_node = node
    if not node:
        pass
    elif data < node.data:
        node.left = _delete(node.left, data)
    elif data > node.data:
        node.right = _delete(node.right, data)
    #this is where deletion happens?
    elif not node.left:#data == node.data
        return_node = node.right#replaces node with its right child
    elif not node.right:#data == node.data
        return_node = node.left
    else:#如果有两个children，就找到左支最大值去替换要删掉那个元素
        node.data = _find_max(node.left).data
        node.left = _delete(node.left, node.data)
    return return_node


    def height(self: 'BST') -> int:
        """Return height of this tree."""
        return _height(self._root)

def _height(node):
    """Return height of tree rooted at node."""
    return 1 + max(_height(node.left), _height(node.right)) if node else -1 #如果有base case，是叶子的话就return 0就好
    #这里return-1是因为如果没有下一个level了，他还是加了1（前面那里），所以要剪掉


def _find_max(node: BTNode) -> BTNode:
    """Find and return maximal node, assume node is not None
        这里只是找到右支最大值"""
    return _find_max(node.right) if node.right else node#这里没有做任何比较是因为这只是一直在剥离
    #一直在往下找右支，直到没有再右边的值，就是最大值（利用了BST的structure）

    #SAME AS:
#    if node.right:
#        return _find_max(node.right)
#    else:
#        return node


# EXERCISE: Fix the code below which is currently incorrect. 
# There's something that needs to be changed in order to fix it.
# You may make use of helper functions to do so.
def is_bst(t):
    '''Return True iff the tree rooted at t is a BST.'''
    if not t:
        return True

    return (not t.left or t.left.data < t.data) and \
           (not t.right or t.right.data > t.data) and \
           is_bst(t.left) and is_bst(t.right)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    b = BST()
    b.insert(8)
    b.insert(4)
    b.insert(2)
    b.insert(6)
    b.insert(12)
    b.insert(14)
    print(b.height())
    print(b.find(4))
    print(b.find(7))
    print(str(b))
    b.delete(12)
    print(b)
    b.delete(14)
    print(b)
    print(b.height())
