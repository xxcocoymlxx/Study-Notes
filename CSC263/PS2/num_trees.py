#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CSC263 Winter 2019
Problem Set 2, Question 3 Starter Code
University of Toronto Mississauga

References:
	Node and AVLTree are from https://gist.github.com/Twoody/de8d079842e0dd20cf20d870c73168af
	Permutation is from https://docs.python.org/2/library/itertools.html
"""

option = False


def debug(msg):
	if option:
		print(msg)


class Node:
	def __init__(self, key):
		self.key = key
		self.left = None
		self.right = None


class AVLTree:
	def __init__(self, *args):
		self.node = None
		self.height = -1
		self.balance = 0
		
		if len(args) == 1:
			for i in args[0]:
				self.insert(i)
	
	def height(self):
		if self.node:
			return self.node.height
		else:
			return 0
	
	def is_leaf(self):
		return self.height == 0
	
	def insert(self, key):
		tree = self.node
		
		new_node = Node(key)
		
		if tree is None:
			self.node = new_node
			self.node.left = AVLTree()
			self.node.right = AVLTree()
			debug("Inserted key [" + str(key) + "]")
		
		elif key < tree.key:
			self.node.left.insert(key)
		
		elif key > tree.key:
			self.node.right.insert(key)
		
		else:
			debug("Key [" + str(key) + "] already in tree.")
		
		self.re_balance()
	
	def re_balance(self):
		"""
		Re-balance a particular (sub)tree
		"""
		# key inserted. Let's check if we're balanced
		self.update_heights(False)
		self.update_balances(False)
		while self.balance < -1 or self.balance > 1:
			if self.balance > 1:
				if self.node.left.balance < 0:
					self.node.left.l_rotate()  # we're in case II
					self.update_heights()
					self.update_balances()
				self.r_rotate()
				self.update_heights()
				self.update_balances()
			
			if self.balance < -1:
				if self.node.right.balance > 0:
					self.node.right.r_rotate()  # we're in case III
					self.update_heights()
					self.update_balances()
				self.l_rotate()
				self.update_heights()
				self.update_balances()
	
	def r_rotate(self):
		# Rotate left pivoting on self
		debug('Rotating ' + str(self.node.key) + ' right')
		a = self.node
		b = self.node.left.node
		t = b.right.node
		
		self.node = b
		b.right.node = a
		a.left.node = t
	
	def l_rotate(self):
		# Rotate left pivoting on self
		debug('Rotating ' + str(self.node.key) + ' left')
		a = self.node
		b = self.node.right.node
		t = b.left.node
		
		self.node = b
		b.left.node = a
		a.right.node = t
	
	def update_heights(self, recurse=True):
		if self.node is not None:
			if recurse:
				if self.node.left is not None:
					self.node.left.update_heights()
				if self.node.right is not None:
					self.node.right.update_heights()
			
			self.height = max(self.node.left.height, self.node.right.height) + 1
		else:
			self.height = -1
	
	def update_balances(self, recurse=True):
		if self.node is not None:
			if recurse:
				if self.node.left is not None:
					self.node.left.update_balances()
				if self.node.right is not None:
					self.node.right.update_balances()
			
			self.balance = self.node.left.height - self.node.right.height
		else:
			self.balance = 0
	
	def delete(self, key):
		# debug("Trying to delete at node: " + str(self.node.key))
		if self.node is not None:
			if self.node.key == key:
				debug("Deleting ... " + str(key))
				if self.node.left.node is None and self.node.right.node is None:
					self.node = None  # leaves can be killed at will
				# if only one subtree, take that
				elif self.node.left.node is None:
					self.node = self.node.right.node
				elif self.node.right.node is None:
					self.node = self.node.left.node
				
				# worst-case: both children present. Find logical successor
				else:
					replacement = self.logical_successor(self.node)
					if replacement is not None:  # sanity check
						debug("Found replacement for " + str(key) + " -> " + str(replacement.key))
						self.node.key = replacement.key
						
						# replaced. Now delete the key from right child
						self.node.right.delete(replacement.key)
				
				self.re_balance()
				return
			elif key < self.node.key:
				self.node.left.delete(key)
			elif key > self.node.key:
				self.node.right.delete(key)
			
			self.re_balance()
		else:
			return
	
	def logical_predecessor(self, node):
		"""
		Find the biggest valued node in LEFT child
		"""
		node = node.left.node
		if node is not None:
			while node.right is not None:
				if node.right.node is None:
					return node
				else:
					node = node.right.node
		return node
	
	def logical_successor(self, node):
		"""
		Find the smallest valued node in RIGHT child
		"""
		node = node.right.node
		if node is not None:  # just a sanity check
			
			while node.left is not None:
				debug("LS: traversing: " + str(node.key))
				if node.left.node is None:
					return node
				else:
					node = node.left.node
		return node
	
	def check_balanced(self):
		if self is None or self.node is None:
			return True
		
		# We always need to make sure we are balanced
		self.update_heights()
		self.update_balances()
		return (abs(self.balance) < 2) and self.node.left.check_balanced() and self.node.right.check_balanced()
	
	def inorder_traverse(self):
		if self.node is None:
			return []
		
		inlist = []
		l = self.node.left.inorder_traverse()
		for i in l:
			inlist.append(i)
		
		inlist.append(self.node.key)
		
		l = self.node.right.inorder_traverse()
		for i in l:
			inlist.append(i)
		
		return inlist
	
	def display(self, level=0, pref=''):
		"""
		Display the whole tree. Uses recursive def.
		TODO: create a better display using breadth-first search
		"""
		self.update_heights()  # Must update heights before balances
		self.update_balances()
		if self.node is not None:
			print('-' * level * 2, pref, self.node.key, "[" + str(self.height) + ":" + str(self.balance) + "]",
			      'L' if self.is_leaf() else ' ')
			if self.node.left is not None:
				self.node.left.display(level + 1, '<')
			if self.node.left is not None:
				self.node.right.display(level + 1, '>')
	

def permutations(iterable, r=None):
	# permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
	# permutations(range(3)) --> 012 021 102 120 201 210
	pool = tuple(iterable)
	n = len(pool)
	r = n if r is None else r
	if r > n:
		return
	indices = [x for x in range(n)]
	cycles = [x for x in range(n, n-r, -1)]
	yield tuple(pool[i] for i in indices[:r])
	while n:
		for i in reversed(range(r)):
			cycles[i] -= 1
			if cycles[i] == 0:
				indices[i:] = indices[i+1:] + indices[i:i+1]
				cycles[i] = n - i
			else:
				j = cycles[i]
				indices[i], indices[-j] = indices[-j], indices[i]
				yield [pool[i] for i in indices[:r]]
				break
		else:
			return


def compare(t1, t2):
	if t1 is None and t2 is None:
		return True
	if t1.node is None and t2.node is None:
		return True
	elif t1.node is None or t2.node is None:
		return False
	left = compare(t1.node.left, t2.node.left)
	right = compare(t1.node.right, t2.node.right)
	return left and right
	

def get_leaf_num(t):
	if t.node is None:
		return 0
	if t.is_leaf():
		return 1
	else:
		return get_leaf_num(t.node.left) + get_leaf_num(t.node.right)


# calculate the number of tree that has the given number of nodes and leaves
def num_trees(nodes: int, leaves: int):
	
	lsts = [x for x in range(nodes)]
	tree_lst = []
	
	for lst in permutations(lsts):
		flag = True
		tree = AVLTree()
		for i in lst:
			tree.insert(i)
		if len(tree_lst) != 0:
			for pre in tree_lst:
				if compare(pre, tree):
					flag = False
		if flag:
			tree_lst.append(tree)
		
	total = 0
	for tree in tree_lst:
		if get_leaf_num(tree) == leaves:
			total += 1
	
	return total

'''	
if __name__ == '__main__':
	# some small test cases
	# Case 1
	assert 2 == num_trees(5, 3)
'''
