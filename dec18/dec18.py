import numpy as np

#######
# Part 1
#######
# with open('dec18Test.txt','r') as file:
with open('dec18.txt', 'r') as file:
	lines = file.readlines()

pts = []
for line in lines:
	x, y, z = line.split(',')
	pts.append((int(x), int(y), int(z)))
pts.sort()

pts = np.array(pts)
# grid = np.zeros(np.max(pts,axis=0))
# for pt in pts:
# 	grid[pt[0]-1, pt[1]-1, pt[2]-1]

#######
# Part 1
#######
# Count sides
sides = 6*len(pts)
for row in range(pts.shape[0]-1):
	temp = np.abs(pts[row+1:] - pts[row,:])
	if (num:=np.sum(np.sum(np.sum(temp,axis=1)==1))) >0:
		sides -= 2*num

print(f'Part 1: Sides not adjacent to other cubes {sides}')

#######
# Part 2
#######

directions = np.array( [ [1,0,0], [-1,0,0], [0,1,0], [0,-1,0], [0,0,1], [0,0,-1]])

def flood_fill(grid):
	searchq = []
	ext_pts = np.where(grid==0)
	for x,y,z in zip(*ext_pts):
		if x==0 or x==grid.shape[0]-1 or y==0 or y==grid.shape[1]-1 or z==0 or z==grid.shape[2]-1:
			grid[x,y,z]=2
		else:
			searchq.append((x,y,z))

	done = False
	while not done:
		done=True
		for (x,y,z) in searchq:
			test_pts =  directions + (x,y,z)
			if any(grid[test_pts[:,0],test_pts[:,1],test_pts[:,2]] ==2):
				grid[x,y,z] = 2
				searchq.remove((x,y,z))
				done = False
		# print(x,y,z)
	return


# Find only exterier edges
# Convert to NP array
grid = np.zeros(np.max(pts,axis=0))
for pt in pts:
	grid[pt[0]-1, pt[1]-1, pt[2]-1] = 1

# Use flood fill to fill all exterior points with -1
flood_fill(grid)
int_pts = np.where(grid==0)
for x, y, z in zip(*int_pts):
	pts = np.append(pts, [[x+1, y+1, z+1]], axis=0)

# Count sides
sides = 6*len(pts)
for row in range(pts.shape[0]-1):
	temp = np.abs(pts[row+1:] - pts[row,:])
	if (num:=np.sum(np.sum(np.sum(temp,axis=1)==1))) >0:
		sides -= 2*num

print(f'Part 2: Exterior points: {sides}')