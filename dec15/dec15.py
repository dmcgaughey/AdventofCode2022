import re

def man_dist(p1,p2):
	return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

def merge_regions(r1,r2):
	if (r2[0] <= r1[0] <= r2[1]) or (r2[0] <= r1[1] <= r2[1]) or (r1[0] <= r2[0] <= r1[1]) \
			or (r1[1]+1==r2[0]) or (r2[1]+1==r1[0]):
		return ( min(r1[0],r2[0]), max(r1[1],r2[1]) )
	return None      #(r1, r2)

def blank_region_on_row(sensors, beacons, row):
	regions = []
	for cnt, sensor in enumerate(sensors):
		if temp := blank_region_on_row_one_sensor(sensor,beacons[cnt],row):
			regions.append(temp)
	done = False

	while len(regions)>1 and not done:
		done = True
		cnt1 = 0
		while cnt1 < len(regions)-1:
			cnt2 = cnt1 + 1
			while cnt2 < len(regions):
				if temp := merge_regions(regions[cnt1],regions[cnt2]):
					done = False
					regions.pop(cnt2)
					regions.pop(cnt1)
					regions.insert(cnt1,temp)
				else:
					cnt2 += 1
			cnt1 += 1

	return regions

def len_regions(regions):
	rlen = 0
	for region in regions:
		rlen += region[1]-region[0]+1
	return rlen

def number_on_row(list,row):
	num = 0
	for el in list:
		if el[1]==row:
			num += 1
	return num

def blank_region_on_row_one_sensor(sensor,beacon,row):
	distance = man_dist(sensor,beacon)
	dy = abs(sensor[1]-row)
	if dy > distance:
		return None
	else:
		dx = distance-dy
		return (sensor[0]-dx, sensor[0]+dx)


def count_blank_regions(sensors,beacons,row):
	regions = blank_region_on_row(sensors,beacons,row)
	return len_regions(regions) - number_on_row(set(sensors),row) -  number_on_row(set(beacons),row)

# Read the beacon and sensor locations
# with open('dec15Test.txt','r') as file:
with open('dec15.txt', 'r') as file:
	lines = file.readlines()

sensors = []
beacons = []
for line in lines:
	coords = re.findall(r'-*[\d]+',line)
	sensors.append(tuple([int(c) for c in coords[:2]]))
	beacons.append(tuple([int(c) for c in coords[2:]]))

print(sensors)
print(beacons)

blanks = count_blank_regions(sensors,beacons,2000000)

print(f'Part 1: Number of blanks on row 10 is: {blanks}')

#####
# Part 2
#####
for row in range(4000000+1):
	regions = blank_region_on_row(sensors, beacons,row)
	if len(regions)>=2:
		if regions[0][0] < regions[1][0]:
			missing = regions[0][1] + 1
		else:
			missing = regions[1][1] + 1
		print(f'Part2: {row+1}, {missing} {regions}')
		print(f'Part 2: {4000000*missing + row}')

		break
