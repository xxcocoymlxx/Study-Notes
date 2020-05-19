#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CSC263 Winter 2019
Problem Set 4
University of Toronto Mississauga
@Author: Junwen Shen
"""
moves = [(-1, 2), (-1, -2), (1, 2), (1, -2), (-2, 1), (-2, -1), (2, 1), (2, -1)]


def get_path_len(rows, cols, start, end):
	"""
	Parameters
	----------
	rows: number of rows in the board
	cols: number of columns in the board
	start: start position of Sushant
	end: target position of Sushant

	Returns
	-------
	the minimum number of steps that Sushant needs from start to end
	"""
	board = [[0] * cols for i in range(rows)]
	paths = {}
	tries = []
	p1 = end
	while p1 != start:
		for d in moves:
			p2 = (p1[0]+d[0], p1[1]+d[1])
			if p2[0] in range(rows) and p2[1] in range(cols) and board[p2[0]][p2[1]] == 0 and p2 not in paths:
				board[p2[0]][p2[1]] = 1
				tries.append(p2)
				paths[p2] = p1
		try:
			p1 = tries.pop(0)
		except IndexError:
			return -1
	count = 0
	p = start
	while p != end:
		p = paths[p]
		count += 1
	return count


def game_outcome(rows, cols, dan_row, dan_col, sushant_row, sushant_col):
	"""
	Parameters
	----------
	rows: number of rows in the board
	cols: number of columns in the board
	dan_row: Dan's starting location (row)
	dan_col: Dan's starting location (col)
	sushant_row: Sushant's starting location (row)
	sushant_col: Sushant's starting location (col)

	Returns
	-------
	the appropriate string, as described in the handout.
	"""
	target_positions = [(i, dan_col) for i in range(dan_row+1, rows)]
	start = (sushant_row, sushant_col)
	x = 1
	while x < len(target_positions):
		steps = get_path_len(rows, cols, start, target_positions[x-1])
		if steps < 0:
			continue
		elif ((steps + x) ^ 2) & 1:
			break
		elif steps - x > 2:
			x += (steps - x) // 2
			continue
		elif steps <= x:
			return "Sushant wins in {0} moves".format(x)
		x += 1
		
	return "Dan wins in {0} moves".format(rows - dan_row - 2)


if __name__ == '__main__':
	import time
	# Case 1
	init = time.time()
	s = game_outcome(50, 50, 10, 10, 10, 12)
	print("Case 1:\n{0}\nRuntime: {1:.4f}s\n".format(s, time.time()-init))
	assert s == "Sushant wins in 1 moves"

	# Case 2
	init = time.time()
	s = game_outcome(6, 8, 2, 3, 0, 0)
	print("Case 2:\n{0}\nRuntime: {1:.4f}s\n".format(s, time.time() - init))
	assert s == "Dan wins in 2 moves"

	# Case 3
	init = time.time()
	s = game_outcome(40, 40, 2, 5, 3, 6)
	print("Case 3:\n{0}\nRuntime: {1:.4f}s\n".format(s, time.time() - init))
	assert s == "Sushant wins in 2 moves"

	# Case 4
	init = time.time()
	s = game_outcome(40, 40, 4, 4, 8, 6)
	print("Case 4:\n{0}\nRuntime: {1:.4f}s\n".format(s, time.time() - init))
	assert s == "Sushant wins in 3 moves"
	
	# Case 5
	init = time.time()
	s = game_outcome(40, 40, 2, 5, 3, 7)
	print("Case 5:\n{0}\nRuntime: {1:.4f}s\n".format(s, time.time() - init))
	assert s == "Dan wins in 36 moves"
	
	# Case 6
	init = time.time()
	s = game_outcome(100, 100, 3, 5, 50, 50)
	print("Case 6:\n{0}\nRuntime: {1:.4f}s\n".format(s, time.time() - init))
	assert s == 'Sushant wins in 23 moves'
	
	# Case 7
	s = game_outcome(100, 100, 2, 5, 3, 7)
	print("Case 7:\n{0}\nRuntime: {1:.4f}s\n".format(s, time.time() - init))
	assert s == 'Dan wins in 96 moves'
	
	# Case 8
	init = time.time()
	s = game_outcome(300, 300, 2, 5, 3, 7)
	print("Case 8:\n{0}\nRuntime: {1:.4f}s\n".format(s, time.time() - init))
	assert s == 'Dan wins in 296 moves'
	
	# Case 9
	init = time.time()
	s = game_outcome(279, 290, 115, 163, 247, 211)
	print("Case 9:\n{0}\nRuntime: {1:.4f}s\n".format(s, time.time() - init))
	assert s == 'Sushant wins in 45 moves'
	
	# Case 10
	init = time.time()
	s = game_outcome(194, 275, 164, 96, 142, 223)
	print("Case 11:\n{0}\nRuntime: {1:.4f}s\n".format(s, time.time() - init))
	assert s == 'Dan wins in 28 moves'
	
	# Case 11
	init = time.time()
	s = game_outcome(48, 247, 22, 131, 25, 77)
	print("Case 10:\n{0}\nRuntime: {1:.4f}s\n".format(s, time.time() - init))
	assert s == 'Dan wins in 24 moves'
	
	# Case 12
	init = time.time()
	s = game_outcome(202, 249, 70, 225, 201, 226)
	print("Case 12:\n{0}\nRuntime: {1:.4f}s\n".format(s, time.time() - init))
	assert s == 'Sushant wins in 44 moves'
	
	# Case 13
	init = time.time()
	s = game_outcome(137, 219, 96, 193, 76, 28)
	print("Case 13:\n{0}\nRuntime: {1:.4f}s\n".format(s, time.time() - init))
	assert s == 'Dan wins in 39 moves'
	
	# Case 14
	init = time.time()
	s = game_outcome(300, 300, 0, 0, 0, 250)
	print("Case 14:\n{0}\nRuntime: {1:.4f}s\n".format(s, time.time() - init))
	assert s == 'Sushant wins in 125 moves'
