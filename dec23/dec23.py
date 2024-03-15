import numpy as np
import re
from enum import IntEnum
from scipy.sparse import lil_matrix

delta = ( (0,1), (1,0), (0,-1), (-1,0))

POSITION = tuple[int, int]      #(x,y)

class ROTATE_DIR(IntEnum):
    CW =  1
    CCW = -1

class DIRECTION(IntEnum):
	N = 0
	S = 1
	W = 2
	E = 3

	def next_dir(self):
		return DIRECTION((self.value+1)%4)


# Read the beacon and sensor locations
# with open('dec23Test1.txt', 'r') as file:
# with open('dec23Test2.txt', 'r') as file:
with open('dec23.txt', 'r') as file:
	lines = file.readlines()

map1 = []
# Read map
for line in lines:
	line = line.replace('\n','').replace('.','0').replace('#','1')
	map1.append(list(line))

# Read directions
row, col = len(map1), len(line)
spmap = lil_matrix((3*row, 3*col),dtype=int)

inpos = np.where(np.array(map1, dtype=int))
spmap[1*row + inpos[0],1*col + inpos[1]] = 1
start_dir = DIRECTION.N

for round in range(10):
	inpos = [*zip(*spmap.nonzero())]
	outpos = inpos.copy()
	# Check the potential move of each elf
	for cnt, p in enumerate(inpos):
		#Check each 4 directions and determine potential move
		matrix = spmap[p[0]-1:p[0]+2, p[1]-1:p[1]+2].todense()
		matrix[1,1] = 0
		# Update potential move array
		if np.all(matrix==0):
			outpos[cnt] = inpos[cnt]
		else:
			for dir in range(4):
				match (dir+start_dir)%4:
					case DIRECTION.N:
						if np.all(matrix[0,:]==0):
							outpos[cnt] = (p[0]-1,p[1])
							break
					case DIRECTION.S:
						if np.all(matrix[2, :] == 0):
							outpos[cnt] = (p[0] + 1, p[1])
							break
					case DIRECTION.W:
						if np.all(matrix[:, 0] == 0):
							outpos[cnt] = (p[0], p[1]-1)
							break
					case DIRECTION.E:
						if np.all(matrix[:, 2] == 0):
							outpos[cnt] = (p[0], p[1] + 1)
							break
	for cnt, p in enumerate(outpos):
		if outpos.count(p) > 1:
			outpos[cnt] = inpos[cnt]
			indx = outpos.index(p,cnt+1)
			outpos[indx] = inpos[indx]
	# Update spmatrix
	start_dir = start_dir.next_dir()
	x, y = zip(*outpos)
	spmap[:,:] = 0
	spmap[x, y] = 1

# Calculate box size
x, y = zip(*outpos)
empty = (max(x) - min(x)+1) * (max(y) - min(y) + 1) - len(x)
print(f'Part 1: Empty ground after 10 iterations {empty}')

