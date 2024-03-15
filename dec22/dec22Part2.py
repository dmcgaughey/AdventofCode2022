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
				out = np.array((-1, 0))
			case DIRECTION.R:
				out = np.array((0, 1))
			case DIRECTION.D:
				out = np.array((1, 0))
			case DIRECTION.L:
				out = np.array((0, -1))
		return out


def add_positons(x:POSITION, delta:POSITION)->POSITION:
    new_pos = x + delta
    return new_pos

def valid_position(x:POSITION,*,shape) -> bool:
    return x[0]>=0 and x[0]<=shape[0]-1 and x[1]>=0 and x[1]<=shape[1]-1

TEST = False
if TEST:
	GRID_SIZE = 4
	offsets = ((8, 8), (4, 4), (0, 8), (8, 12), (4, 8), (4, 0))

	next_edge = ((0, 'R', 3, 'R', 'row', '0'),
				 (0, 'D', 5, 'U', '3', '3-col'),
				 (0, 'L', 1, 'U', '3', '3-row'), 
				 (0, 'U', 4, 'D', '3', 'col'),  
				 (1, 'R', 4, 'R', 'row', '0'),
				 (1, 'D', 0, 'R', '3-col', '0'), 
				 (1, 'L', 5, 'L', 'row', '3'), 
				 (1, 'U', 2, 'R', 'col', '0'), 
				 (2, 'R', 3, 'L', '3-row', '3'),
				 (2, 'D', 4, 'D', '0', 'col'), 
				 (2, 'L', 1, 'D', '0', 'row'), 
				 (2, 'U', 5, 'D', '0', '3-col'),
				 (3, 'R', 2, 'L', '3-row', '3'), 
				 (3, 'D', 5, 'R', '3-col', '0'), 
				 (3, 'L', 0, 'L', 'row', '3'), 
				 (3, 'U', 4, 'L', '3-col', '3'), 
				 (4, 'R', 3, 'D', '0', '3-row'),
				 (4, 'D', 0, 'D', '0', 'col'), 
				 (4, 'L', 1, 'L', 'row', '3'), 
				 (4, 'U', 2, 'U', '3', 'col'),
				 (5, 'R', 1, 'R', 'row', '0'),
				 (5, 'D', 0, 'U', '3', '3-col'),
				 (5, 'U', 2, 'D', '0', '3-col'),
				 (5, 'L', 3, 'U', '3', '3-row') )
else:
	GRID_SIZE = 50
	offsets = ((100, 0), (0, 50), (0, 100), (100, 50), (50, 50), (150, 0))

	next_edge = ((0, 'R', 3, 'R', 'row', '0'),
				 (0, 'D', 5, 'D', '0', 'col'),
				 (0, 'L', 1, 'R', '49-row', '0'),
				 (0, 'U', 4, 'R', 'col', '0'),
				 (1, 'R', 2, 'R', 'row', '0'),
				 (1, 'D', 4, 'D', '0', 'col'),
				 (1, 'L', 0, 'R', '49-row', '0'),
				 (1, 'U', 5, 'R', 'col', '0'),
				 (2, 'R', 3, 'L', '49-row', '49'),
				 (2, 'D', 4, 'L', 'col', '49'),
				 (2, 'L', 1, 'L', 'row', '49'),
				 (2, 'U', 5, 'U', '49', 'col'),
				 (3, 'R', 2, 'L', '49-row', '49'),
				 (3, 'D', 5, 'L', 'col', '49'),
				 (3, 'L', 0, 'L', 'row', '49'),
				 (3, 'U', 4, 'U', '49', 'col'),
				 (4, 'R', 2, 'U', '49', 'row'),
				 (4, 'D', 3, 'D', '0', 'col'),
				 (4, 'L', 0, 'D', '0','row'),
				 (4, 'U', 1, 'U', '49', 'col'),
				 (5, 'R', 3, 'U', '49', 'row'),
				 (5, 'D', 2, 'D', '0', 'col'),
				 (5, 'L', 1, 'D', '0', 'row'),
				 (5, 'U', 0, 'U', '49', 'col') )


def move(x:POSITION, facing: DIRECTION, cur_side:int, steps: int, map1: np.ndarray) -> POSITION:
	for cnt in range(steps):
		next_pos = add_positons(x, DIRECTION.delta1square(facing))
		# DOWN
		if np.any(next_pos<0) or np.any(next_pos>=GRID_SIZE) or \
				map1[next_pos[0] + offsets[cur_side][0],next_pos[1] + offsets[cur_side][1]] == '':
			row, col = x
			indx = 4*cur_side + facing
			next_side =  next_edge[indx][2]
			next_facing = DIRECTION[next_edge[indx][3]]
			next_pos = [eval(next_edge[indx][4]), eval(next_edge[indx][5])]
		else:
			next_side = cur_side
			next_facing = facing


		if map1[next_pos[0] + offsets[next_side][0],next_pos[1] + offsets[next_side][1]] == '#':
			break

		if map1[next_pos[0] + offsets[next_side][0],next_pos[1] + offsets[next_side][1]] == '.':
			x = next_pos
			facing = next_facing
			cur_side = next_side
		else:
			pass

	return cur_side, facing, x

# Read the beacon and sensor locations
# with open('dec22Test.txt', 'r') as file:
with open(fname := 'dec22.txt', 'r') as file:
	lines = file.readlines()


map1 = []
# Read map
for line in lines:
	if not (line := line.strip('\n')): break
	map1.append(list(line))

# Read directions
directions = lines[-1].strip()

cols = [len(a) for a in map1]

map2 = np.zeros([len(map1), max(cols)], dtype=str)
for row in range(len(map1)):
	map2[row,:cols[row]] = np.array(map1[row])
# map2 = np.array(map1)
map2[map2 == ' '] = ''
print(map2)
print(directions)

steps = [('R',re.search(r'(^\d+)',directions)[0])] + re.findall(r'\d*([RL])(\d+)',directions)
print(steps)

start = np.argwhere(map2 == '.')[0]
cur_side = start[1]//GRID_SIZE
pos = start % GRID_SIZE
facing = DIRECTION.U
for step in steps:
	facing = DIRECTION.rotate(facing, ROTATE_DIR[step[0]])
	cur_side, facing, pos = move(pos, facing, cur_side, int(step[1]), map2)

val = 1000*(pos[0]+offsets[cur_side][0]+1) + 4 * (pos[1] + offsets[cur_side][1]+1) + facing
print(f'Part 2: {val}')