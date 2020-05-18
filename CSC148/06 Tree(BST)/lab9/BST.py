"""A simple visual test module for the BST implementation.
Author: Francois Pitt, March 2013
        Danny Heap, March 2014
"""

# Uncomment exactly one of these, to test the corresponding implementation.
#from BST_rec1 import BST
#from BST_rec2 import BST
#from BST_rec3 import BST
#from BST_iter import BST


if __name__ == '__main__':
    # Create a few simple trees, print them, and count the number of values less
    # than various values.

    tree = BST([])
    print("\nempty:", tree, sep="\n")
    print("< 5:", tree.count_less(5))
    print("size: {}".format(tree.size()))

    tree = BST([2])
    print("\nroot only:", tree, sep="\n")
    print("< 1:", tree.count_less(1))
    print("< 2:", tree.count_less(2))
    print("< 3:", tree.count_less(3))
    print("size: {}".format(tree.size()))

    tree = BST([2, 4])
    print("\nroot and right child:", tree, sep="\n")
    print("< 1:", tree.count_less(1))
    print("< 2:", tree.count_less(2))
    print("< 3:", tree.count_less(3))
    print("< 4:", tree.count_less(4))
    print("< 5:", tree.count_less(5))
    print("size: {}".format(tree.size()))

    tree = BST([4, 2])
    print("\nroot and left child:", tree, sep="\n")
    print("< 1:", tree.count_less(1))
    print("< 2:", tree.count_less(2))
    print("< 3:", tree.count_less(3))
    print("< 4:", tree.count_less(4))
    print("< 5:", tree.count_less(5))
    print("size: {}".format(tree.size()))

    tree = BST([4, 2, 6])
    print("\nroot with two children:", tree, sep="\n")
    print("< 1:", tree.count_less(1))
    print("< 2:", tree.count_less(2))
    print("< 3:", tree.count_less(3))
    print("< 4:", tree.count_less(4))
    print("< 5:", tree.count_less(5))
    print("< 6:", tree.count_less(6))
    print("< 7:", tree.count_less(7))
    print("size: {}".format(tree.size()))

    tree = BST([8, 6, 4, 2])
    print("\nchain left:", tree, sep="\n")
    print("< 1:", tree.count_less(1))
    print("< 2:", tree.count_less(2))
    print("< 3:", tree.count_less(3))
    print("< 4:", tree.count_less(4))
    print("< 5:", tree.count_less(5))
    print("< 6:", tree.count_less(6))
    print("< 7:", tree.count_less(7))
    print("< 8:", tree.count_less(8))
    print("< 9:", tree.count_less(9))
    print("size: {}".format(tree.size()))

    tree = BST([2, 4, 6, 8])
    print("\nchain right:", tree, sep="\n")
    print("< 1:", tree.count_less(1))
    print("< 2:", tree.count_less(2))
    print("< 3:", tree.count_less(3))
    print("< 4:", tree.count_less(4))
    print("< 5:", tree.count_less(5))
    print("< 6:", tree.count_less(6))
    print("< 7:", tree.count_less(7))
    print("< 8:", tree.count_less(8))
    print("< 9:", tree.count_less(9))
    print("size: {}".format(tree.size()))

    tree = BST([8, 4, 10, 2, 6, 14, 12])
    print("\ntypical:", tree, sep="\n")
    print("<  1:", tree.count_less(1))
    print("<  2:", tree.count_less(2))
    print("<  3:", tree.count_less(3))
    print("<  4:", tree.count_less(4))
    print("<  5:", tree.count_less(5))
    print("<  6:", tree.count_less(6))
    print("<  7:", tree.count_less(7))
    print("<  8:", tree.count_less(8))
    print("<  9:", tree.count_less(9))
    print("< 10:", tree.count_less(10))
    print("< 11:", tree.count_less(11))
    print("< 12:", tree.count_less(12))
    print("< 13:", tree.count_less(13))
    print("< 14:", tree.count_less(14))
    print("< 15:", tree.count_less(15))
    print("size: {}".format(tree.size()))
