Question 1

def mystery(t):
  if not t:
    return True
  if not t.left and not t.right: # if there is no left and right subtree...
    return True
  return t.left != None and t.right!= None \
         and mystery(t.left) and mystery(t.right)

Use example trees for intuition of what this code is doing!

1->2
1->None
Function returns False

1->None
1->2
False again

1->2
1->3
This time, True

English: return True iff symmetric, balanced... these terms are not precise.

Return True iff every node in the binary tree has 0 or 2 children.
Return True iff every internal node in the binary tree has two children.


-----

Question 2

Find two distinct binary trees t1 and t2 such that
*t1 and t2 have the same preorder, and
*t1 and t2 have the same postorder

t1 (root and left child):
1->2
1->None

t2 (root and right child):
1->None
1->2 

Preorder for both of these trees: 1 2
Postorders for both of these trees: 2 1

Question 1: if I give you the preorder and postorder for a tree, can you tell me the tree?
No

Question 2: if I give you preorder and inorder, can you tell me the tree?
Yes

If you have all three pre/in/postorder,
then based on the above you can reconstruct the tree.

-----

Question 4

Given a binary tree of height h, what is the maximum number of nodes in the tree.

If you want to maximize the number of nodes, every internal node must have two children.

1->2
1->5
Heiht is 1. Number of nodes is 3.

Height 0: 1 node
height 1: 3 nodes
Height 2: 7 nodes
Height 3: 15
Height 4: 31
...

Maximum number of nodes for a binary tree of height h is 2^(h+1) -1


OK. What if we have trees where the maximum branching factor is 3.
3^{h+1}-1... no! Work on this!

------

Question 5

Trace through a simple tree
e.g.
BTree(1, BTree(2), BTree(3))
and see what the stack and output are at each iteration of the while loop.

Based on this, you should be able to tell whether the traversal is
PREORDER, POSTORDER, INORDER or LEVEL-ORDER.
