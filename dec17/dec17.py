import numpy as np

###########
# Part 1
# Falling rocks - tetris like
###########

# Reade the string with the wind gusts
# with open('dec17Test.txt','r') as file:
with open('dec17.txt', 'r') as file:
	lines = file.readlines()
gust_str = lines[0].strip()

MAX_ROCKS = 1731+1735+144		# Constant for MAX_ROCKS

# Initialize the shapes and the matrix for the column of rocks
hline = np.array([[0,0],[0,1],[0,2],[0,3]])
plus = np.array([[0,1],[1,0],[1,1],[1,2],[2,1]])
ell = np.array([[0,0],[0,1],[0,2],[1,2],[2,2]])
vline = np.array([[0,0],[1,0],[2,0],[3,0]])
square = np.array([[0,0],[0,1],[1,0],[1,1]])
shapes = [hline, plus, ell, vline, square]
shape_size = ( (1,4), (3,3), (3,3), (4,1), (2,2))
column = np.zeros([4*MAX_ROCKS,7],dtype=int)


# Run the process of dropping the rocks
top = 0
gust_counter = 0
height = 0
full_row_list = []
num_rocks_dropped_list = []
height_per_set = []
rocks_per_set = []

for cnt in range(MAX_ROCKS):
	shape = shapes[cnt%5]
	offset = [top+3,2]

	# if cnt % 40 == 0:
	# 	height_per_set.append(height + top)

	while(1):
		gust = gust_str[gust_counter]
		gust_counter = (gust_counter + 1) % len(gust_str)

		if gust_counter==0:
			# pass
			height_per_set.append(height + top)
			rocks_per_set.append(cnt)

		# Perform gust
		match(gust):
			case '<':
				if offset[1] >0:
					if np.all(column[shape[:,0]+offset[0],shape[:,1]+offset[1]-1] == 0):
						offset[1] -=1
			case '>':
				if offset[1]+shape_size[cnt%5][1]-1 < 6:
					if np.all(column[shape[:, 0] + offset[0], shape[:, 1] + offset[1] + 1] == 0):
						offset[1] += 1

		# Perform drop 1 square
		if offset[0]==0 or np.any(column[shape[:,0]+offset[0]-1,shape[:,1]+offset[1]]):
			column[shape[:, 0] + offset[0], shape[:, 1] + offset[1]] = 1
			top = max(offset[0] + shape_size[cnt%5][0], top)

			# Check for row all ones.  If found delete all rows before all 1's row and agjust height and top
			rows = np.unique(shape[:, 0] + offset[0])
			all_ones = rows[np.where(np.all(column[rows,:] == np.ones([1,7],dtype=int), axis = 1))]

			# Keep the matrix size small by collapsing matrix when row of all 1's is found
			if all_ones.size>0:
				# pass
				full_row_list.append(all_ones[0])
				num_rocks_dropped_list.append(cnt)
				column[0:top-all_ones[0]-1,:] = column[all_ones[0]+1:top,:]
				column[(top-all_ones[0]-1):,:]=0
				height += all_ones[0]+1
				top -= all_ones[0]+1

			break
		else:
			offset[0] -= 1


print(f'Part 1: height = {height+top}')

###################
# Part 2:
# ###################
# # For dec17test
# ###################
# hps = np.diff(height_per_set,1)
# rps  = np.diff(rocks_per_set,1)
#
# height_period = np.sum(hps[2:7])
# rocks_period = np.sum(rps[2:7])
# periods = (1000000000000-np.sum(rps[:2]))//rocks_period
# remainder = (1000000000000-np.sum(rps[:2]))%rocks_period
#
# height = periods * height_period + np.sum(hps[:2])
# print(f'Part 2: {height+1}')   # Has remainder of 1 and we know the rock is square : Adds height of 1

# print(remainder)
# 1514285714288

###################
# For dec17
###################
hps = np.diff(height_per_set,1)
rps  = np.diff(rocks_per_set,1)

height_period = hps[0]
rocks_period = rps[0]
periods = (1000000000000-rocks_per_set[0])//rocks_period
remainder = (1000000000000-rocks_per_set[0])%rocks_period

height_of_remainder = height+top - height_per_set[1]

height2 = height_per_set[0] + periods * height_period + height_of_remainder
print(f'Part 2: {height2}')