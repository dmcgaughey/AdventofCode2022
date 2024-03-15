import numpy as np

###########
# Part 1
# List comparison
###########

def print_map(rock_map):
	for row in rock_map:
		txt = str(row).replace('-1','~').replace('\n','').replace(' ','').replace('1','#').replace('2','o').replace('0','.')[1:-1]
		print(txt)

# Read the string with the wind gusts
# with open('dec14Test.txt','r') as file:
with open('dec14.txt', 'r') as file:
	lines = file.readlines()

# Read all the lines into lists and find the min_x, max_y
min_x = 500
max_x = 500
max_y = 0
rocks = []
cur_pts = []
for line in lines:
	cur_pts.clear()
	for point in line.strip().split('->'):
		pt = tuple([int(p) for p in point.split(',')])
		cur_pts.append(pt)
		if pt[0] < min_x: min_x = pt[0]
		if pt[0] > max_x: max_x = pt[0]
		if pt[1] > max_y: max_y = pt[1]

	rocks.append(tuple(cur_pts))

# Create a numpy array of the rocks
rock_map = np.zeros([max_y+1, max_x-min_x+1],dtype=int)

for rock in rocks:
	for rcnt in range(len(rock)-1):
		x_st = rock[rcnt+1][0] - min_x
		x_end = rock[rcnt][0] - min_x
		# dx = -np.sign(rock[rcnt+1][0]-rock[rcnt][0])
		y_st = rock[rcnt + 1][1]
		y_end = rock[rcnt][1]
		# dy = -np.sign(rock[rcnt + 1][1] - rock[rcnt][1])
		if x_st==x_end:
			rock_map[min(y_st,y_end):max(y_st,y_end)+1, x_st] = 1
		elif y_st == y_end:
			rock_map[y_st, min(x_st,x_end):max(x_st,x_end)+1] = 1
		else:
			pass

print_map(rock_map)

# Now simulate the sand falling
done = False
num_rocks = 0
while (not done):
	cur_pos = (500-min_x, 0)
	while (1):
		rock_map[cur_pos[1], cur_pos[0]] = -1
		# Check down
		if cur_pos[1]+1 == rock_map.shape[0]:
			done = True
			break
		elif rock_map[cur_pos[1]+1,cur_pos[0]] <= 0:
			cur_pos = (cur_pos[0], cur_pos[1]+1)
			continue

		# Check down left
		if cur_pos[0] <= 0:
			done = True
			break
		elif rock_map[cur_pos[1]+1,cur_pos[0]-1] <= 0:
			cur_pos = (cur_pos[0]-1, cur_pos[1]+1)
			continue

		# Check down-right
		if cur_pos[0] + 1 >= rock_map.shape[1]:
			done = True
			break
		elif rock_map[cur_pos[1]+1,cur_pos[0]+1] <= 0:
			cur_pos = (cur_pos[0]+1, cur_pos[1]+1)
			continue

		 # No moves found if you get here
		rock_map[cur_pos[1], cur_pos[0]] = 2
		num_rocks += 1
		break

print(f'Part 1: {num_rocks}')
print_map(rock_map)