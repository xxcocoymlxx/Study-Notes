----------

BST Handout Solutions

Q1.

(a) Consider each of the following orders of insertion into an empty BST. 

Which one results in the tree where searches are fastest?

A. 1, 2, 3, 4, 5, 6, 7
What does this tree look like?
It looks like a linked list.
Root 1
Right child of 1 is 2
Right child of 2 is 3
Right child of 3 is 4.
...
chain
Height: 6

B. 7, 6, 5, 4, 3, 2, 1
This is just as bad.
Root is 7
Left child of 7 is 6
Left child of 6 is 5
Left child of 5 is 4
...
Height: 6

C. 3, 2, 1, 7, 6, 5, 4
This has to be better because it is not sorted.

In general, what is the best way to insert into a BST?
You want to insert in random order.
8, 2, 15, 9, 1, -3, 40, 20, 22, 18, -50...
No pattern


(b) What is the maximum height of a BST that contains 32 elements?
31

What is the minimum height of a BST that contains 32 elements?
5

To think about this...
Height 0: maximum 1 node
Height 1: root, left child of the root, right child of the root... 3 nodes maximum
Height 2: 7 nodes maximum
Height 3: 15 nodes maximum
Height 4: 31 nodes maximum
Height 5: maximum nodes is 63


Q2.
Deleting 7: follow algorithm for deleting node with one child
Deleting 20: follow algorithm for deleting node with
two children (replace 20 with max from left subtree, so new root becomes 7)

Q3.

The algorithm for deleting a node with two children that we discussed during lecture involved replacing the unwanted value with the maximum value from the left subtree.

(a) What is the algorithm to find the maximum value of a BST?

if not right
	return node
else
	keep recursively calling find_max on the right child


def maximum(t):
  while t.right:
    t = t.right
  return t.value # or t.data, t.item... whatever it is

(b) Your friend proposes an alternative delete algorithm as follows: replace the unwanted value with the maximum
value from the right subtree.Does this still work? If yes, explain why. If not, explain why not and fix the algorithm.

Does this work? No. e.g. in the tree of question 2, replacing 20 by 35 breaks the BST property.

What can I do instead?
Is there any value in the right subtree that I can use? Yes. It is the smallest value in the right subtree.

Summarize...
When you want to delete a node that has two children, you can replace that node by one of two things:
1. The maximum value in the left subtree, or
2. The minimum value in the right subtree
They'll both maintain the BST property.

Suppose you wanted to find the minimum in the right subtree... what would the algorithm be for that?
Just keep taking the left path


