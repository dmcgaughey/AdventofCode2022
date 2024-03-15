import numpy as np
import re
from enum import IntEnum

delta = ( (0,1), (1,0), (0,-1), (-1,0))

POSITION = tuple[int, int]      #(x,y)

class ROTATE_DIR(IntEnum):
    R =  1
    L = -1

class DIRECTION(IntEnum):
	R = 0
	D = 1
	L = 2
	U = 3

	@staticmethod
	def rotate(dir: "DIRECTION", rot: ROTATE_DIR) -> "DIRECTION":
		return DIRECTION((dir + rot + 4) % 4)

	@staticmethod
	def delta1square(dir: "DIRECTION") -> POSITION:
		match dir:
			case DIRECTION.U:
				out = (-1, 0)
			case DIRECTION.R:
				out = (0, 1)
			case DIRECTION.D:
				out = (1, 0)
			case DIRECTION.L:
				out = (0, -1)
		return out


def add_positons(x:POSITION, delta:POSITION)->POSITION:
    new_pos = (x[0]+delta[0], x[1]+delta[1])
    return new_pos

def valid_position(x:POSITION,*,shape) -> bool:
    return x[0]>=0 and x[0]<=shape[0]-1 and x[1]>=0 and x[1]<=shape[1]-1

def move(x:POSITION, facing: DIRECTION, steps: int, map1: np.ndarray) -> POSITION:
	for cnt in range(steps):
		next_pos = add_positons(x, DIRECTION.delta1square(facing))
		# DOWN
		if facing == DIRECTION.D and (next_pos[0] > map1.shape[0] or map1[next_pos[0],next_pos[1]] == ''):
			next_pos = [np.min(np.where(map1[:,next_pos[1]] != '')), next_pos[1]]
		# UP
		elif facing == DIRECTION.U and (next_pos[0] < 0 or map1[next_pos[0],next_pos[1]] == ''):
			next_pos = [np.max(np.where(map1[:,next_pos[1]] != '')), next_pos[1]]
		# RIGHT
		elif facing == DIRECTION.R and (next_pos[1] > map1.shape[1] or map1[next_pos[0],next_pos[1]] == ''):
			next_pos = [next_pos[0], np.min(np.where(map1[next_pos[0],:] != ''))]
		# LEFT
		elif facing == DIRECTION.L and (next_pos[1] < 0 or map1[next_pos[0],next_pos[1]] == ''):
			next_pos = [next_pos[0], np.max(np.where(map1[next_pos[0], :] != ''))]
		elif map1[next_pos[0],next_pos[1]] == '':
			pass

		if map1[next_pos[0],next_pos[1]] == '#':
			break

		if map1[next_pos[0], next_pos[1]] == '.':
			x = next_pos
		else:
			pass

	return x


# Read the beacon and sensor locations
# with open('dec22Test.txt', 'r') as file:
with open('dec22.txt', 'r') as file:
	lines = file.readlines()

map1 = []
# Read map
for line in lines:
	if not (line := line.strip('\n')): break
	map1.append(list(line))

# Read directions
directions = lines[-1].strip()

cols = [len(a) for a in map1]

map2 = np.zeros([len(map1)+2, max(cols)+2], dtype=str)
for row in range(len(map1)):
	map2[row+1,1:cols[row]+1] = np.array(map1[row])
map2[map2 == ' '] = ''
print(map2)
print(directions)

steps = [('R',re.search(r'(^\d+)',directions)[0])] + re.findall(r'\d*([RL])(\d+)',directions)
print(steps)

start = np.argwhere(map2 == '.')[0]
pos = start
facing = DIRECTION.U
for step in steps:
	facing = DIRECTION.rotate(facing, ROTATE_DIR[step[0]])
	pos = move(pos, facing, int(step[1]), map2)

val = 1000*pos[0] + 4 * pos[1] + facing
print(f'Part 1: {val}')