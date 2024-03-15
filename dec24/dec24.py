import numpy as np
from enum import IntEnum
import heapq

class DIRECTION(IntEnum):
	R = 1
	L = 2
	U = 4
	D = 8
	N = 0


def move_storm(map1:np.ndarray):
	map2 = map1.copy()
	map1[map1 != 17] = 0
	for row in range(map2.shape[0]):
		for col in range(1,map2.shape[1]-1):
			if map2[row,col] in [0,17]:
				continue
			if map2[row,col] & DIRECTION.R:
				if col == map2.shape[1]-2:
					map1[row,1] |= DIRECTION.R
				else:
					map1[row, col + 1] |= DIRECTION.R

			if map2[row, col] & DIRECTION.L:
				if col == 1:
					map1[row, -2] |= DIRECTION.L
				else:
					map1[row, col - 1] |= DIRECTION.L

			if map2[row,col] & DIRECTION.U:
				if row == 0 or (row == 1 and map1[0,col]==17):
					map1[-2, col] |= DIRECTION.U
				else:
					map1[row-1, col] |= DIRECTION.U

			if map2[row, col] & DIRECTION.D:
				if row == map1.shape[0]-1 or (row == map1.shape[0]-2 and map1[-1, col] == 17):
					map1[1, col] |= DIRECTION.D
				else:
					map1[row+1, col] |= DIRECTION.D

	return


def find_path(path, map1):
	# Check up, down, right and left for all the possible paths
	old_path = path.copy()
	path.clear()
	for (row,col) , pathlen in old_path:
		# Case UP
		if row != 0 and map1[row-1, col] == 0:
			if not ((row -1, col), pathlen+1) in path:
				path.append( ((row -1, col), pathlen+1))
		# CASE Down
		if row != map1.shape[0]-1 and map1[row+1, col] == 0:
			if not ((row + 1, col), pathlen+1) in path:
				path.append( ((row + 1, col), pathlen+1))
		# Case RIGHT
		if map1[row, col+1] == 0:
			if not ((row, col+1), pathlen + 1) in path:
				path.append(((row, col+1), pathlen + 1))
		# CASE LEFT
		if map1[row, col-1] == 0:
			if not ((row, col-1), pathlen + 1) in path:
				path.append(((row, col-1), pathlen + 1))
		# CASE NO MOVE
		if map1[row, col] == 0:
			if not ((row, col), pathlen + 1) in path:
				path.append(((row, col), pathlen + 1))

# Read the beacon and sensor locations
# with open('dec24Test.txt', 'r') as file:
with open('dec24.txt', 'r') as file:
	lines = file.readlines()

transtable = str.maketrans('#.><^v','901248')
map1 = []
for line in lines:
	map1.append(list(line.strip('\n').translate(transtable)))

map1= np.array(map1,dtype=int)
map1[map1==9] = 17
start = (0, np.where(map1[0,:]==0)[0][0])
fini = (map1.shape[0]-1, np.where(map1[-1,:]==0)[0][0])

path = []
path.append( (start , 0) )
while path:
	move_storm(map1)
	find_path(path, map1)
	path.sort()

	if (path[-1][0]) == fini:
		break
t1 =path[-1][1]
print(f'Min path: {t1}')

#####
# Part 2: Return to start and then return back to finish
path = [path[-1]]
while path:
	move_storm(map1)
	find_path(path, map1)
	path.sort()

	if path[0][0] == start:
		break
t2 = path[-1][1]
print(f'Time to return {t2}')

# now go from start to finish again
path = [path[0]]
while path:
	move_storm(map1)
	find_path(path, map1)
	path.sort()

	if (path[-1][0]) == fini:
		break

t3 = path[-1][1]
print(f'Path 2: Cross 3 times: {t3}')
