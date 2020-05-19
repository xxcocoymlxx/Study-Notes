#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CSC263 Winter 2019
Problem Set 3 Starter Code
University of Toronto Mississauga
"""
#这他妈就跟midterm最后一题很像了啊！就是如果不用hash table的话至少需要n^2的
#因为使用了hash table，真的省略了很多不必要的比较

class Node:
	
	def __init__(self, value):
		self.value = value
		self.next = None


class LinkedList:
	
	def __init__(self):
		self.head = None
	
	def insert(self, value):
		new = Node(value)
		new.next = self.head
		self.head = new


def hash_pizza(flag, n):
	'''
	Make sure that two pizzas are hashed to the same slot if it
	is possible for them to be equivalent.
	这里用的就是sum of pizza’s ratings
	如果两块pizza rating的总和一样，那很有可能两块pizza就是同一块
	就把两块pizza放到同一个slot里去，如果那个slot里已经有东西了，就和他比
	如果是一样的可以preppend到前面，也可以不存。如果是不一样的，就说明
	这是另一种新的pizza的种类，就用linear probing找到下一个空位存下来就行。
	'''
	
	return int(n * ((flag * 0.618) % 1))


def check_equivalent(first, second):
	for i in range(5):#一个pizza只有5块for sure
		if first == second[i:] + second[:i]:#check了所有pizza的rotation，只要其中一个相当就return true
			return True
	return False


def num_pizza_kinds(pizzas):
	"""
	the parameter: pizzas 是一个list of tuples
	Pre: pizzas is a list of pizza 5-tuples
	Post: return number of kinds of pizzas
	"""
	pizza_table = []#空的hash table
	n = len(pizzas)
	for i in range(n):
		pizza_table.append(None)#initializa hash table

	for pizza in pizzas:
		flag = sum(pizza)
		index = hash_pizza(flag, n)#得到这个pizza potentially可能存到哪个位置里

		while True:
			current = pizza_table[index]
			if current is None:#如果这个rating总和是从来没出现过的，那肯定就是一个新的pizza的种类
				head = LinkedList()
				head.insert(pizza)
				pizza_table[index] = head
				break
			elif check_equivalent(current.head.value, pizza):#如果已经有pizza了，check他们是不是同一种
				current.insert(pizza)
				break
			else:#如果不是同一种的话用linar probing放到下一个合适的位置
				index += 1
				if index >= n:
					index = 0
	
	total = 0
	for l in pizza_table:#最后来计算hush table里被占了几个位子，就是有几种不同的pizza
		if l is not None:
			total += 1
	return total


if __name__ == '__main__':
	# some small test cases
	# Case 1
	p = [(1, 2, 3, 4, 5), (2, 3, 4, 5, 1), (5, 4, 3, 2, 1), (4, 3, 2, 1, 5), (20, 10, 2, 9, 1)]
	assert 3 == num_pizza_kinds(p)
