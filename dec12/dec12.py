import numpy as np
import heapq
from enum import IntEnum
from itertools import count


class Direction(IntEnum):
	# NONE = -1
	UP = 1
	RIGHT = 2
	DOWN = 4
	LEFT = 8
	ALL = 0b1111

class SEARCHED(IntEnum):
	NONE = 0
	INQUEUE =  1
	SEARCHED = 2

def reverse(indir:Direction)->Direction:
	return Direction((indir.value+(indir.value<<4)>>2)&0x0F)


def man_dist(start, end):
	return abs(end[0]-start[0]) + abs(end[1]-start[1])

def valid_position(new_pos, mshape):
	return np.all(new_pos>=0) and np.all(new_pos<mshape)

def valid_move(matrix,old_pos, new_pos):
	if matrix[old_pos[0],old_pos[1]] == ('y'):
		pass
	return (  ord(matrix[new_pos[0],new_pos[1]]) - ord(matrix[old_pos[0],old_pos[1]])  ) <= 1

def shortest_path(matrix,start,end):
	node_number = count(step=-1)
	deltas = np.array([ (-1,0), (0,1), (1,0), (0,-1)], dtype=int)
	searched = np.zeros(matrix.shape,dtype=int)

	tosearch = [(man_dist(start, end)+0, 0, next(node_number), start)]


	while node:=heapq.heappop(tosearch):
		path_len = node[1]
		cur_pos = node[3]
		searched[cur_pos[0], cur_pos[1]] |= SEARCHED.SEARCHED

		if np.all(cur_pos==end):
			break

		for cnt in range(4):
			dir_ = Direction(2**cnt)
			new_pos = cur_pos + deltas[cnt,:]

			if valid_position(new_pos, matrix.shape) and valid_move(matrix,cur_pos, new_pos):
				if not searched[new_pos[0],new_pos[1]]:
					searched[new_pos[0], new_pos[1]] |= SEARCHED.INQUEUE
					heapq.heappush(tosearch,(man_dist(new_pos, end)+path_len+1, path_len+1, next(node_number), new_pos))
				else:
					pass # already in queue
		if len(tosearch)==1:
			pass

	return path_len

#######
# Part 1
#######
# with open('dec12Test.txt','r') as file:
with open('dec12.txt', 'r') as file:
	lines = file.readlines()

matrix = []
for line in lines:
	matrix.append(list(line.strip()))

matrix = np.array(matrix)
start = np.where(matrix=='S')
start = np.array([start[0][0], start[1][0]],dtype=int)
finish = np.where(matrix=='E')
finish = np.array([finish[0][0], finish[1][0]], dtype=int)
matrix[start[0],start[1]] = 'a'
matrix[finish[0],finish[1]]='z'

steps = shortest_path(matrix,start,finish)
print(f'Part1: {steps}')

#####
# Part 2.
# Find shortest path from any 'a'
# The only 'ab' or 'ba' are in the first column (any row)
shortest = steps
for row in range(matrix.shape[0]):
	start = np.array([row,0])
	steps = shortest_path(matrix, start, finish)
	if steps < shortest: shortest = steps

print(f'Part2: Shortest path {shortest}')