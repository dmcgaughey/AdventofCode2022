import re
import numpy as np
from collections import namedtuple
# import heapq
from sortedcontainers import SortedList

from itertools import zip_longest

r = r'Blueprint (\d+):.*Each ore robot costs (\d+) ore\. Each clay robot costs (\d+) ore\. Each obsidian robot costs (\d+) ore and (\d+) clay\. Each geode robot costs (\d+) ore and (\d+) obsidian\.'

# Read the beacon and sensor locations
# with open('dec19Test.txt', 'r') as file:
with open('dec19.txt', 'r') as file:
	lines = file.readlines()

blueprints = []
for line in lines:
	bp = re.findall(r'-*\d+', line)
	blueprints.append(tuple(bp))

print(blueprints)

State = namedtuple('State', 't, robots, resources, numr')
weights = []
max_t=24


# Resourses and robots are
def add_robot(rtoa, state:State, maxt, w):
	t, robots, resources, numr = state
	# Flip the robot array so when pruning keep branch with most of robot 3, then 3 etc
	robots, resources = -np.array(robots)[::-1], -np.array(resources)[::-1]

	tempw = w[rtoa, :]
	if np.any(robots[tempw != 0] == 0):
		return (100,-1, np.sum(w), 100/(resources[-1]+1), tuple(-robots[::-1]), tuple(-resources[::-1]) )

	dt = max(int(np.max(np.ceil((tempw-resources)[robots != 0] / robots[robots !=0]))),0)
	if dt<0:
		dt = 0
	if t+dt > maxt: dt = maxt-t

	# resources[-1] = resources[-1] + robots[-1] * (dt + 1)
	resources += robots*int(dt+1) - tempw
	robots[rtoa] += 1
	t += dt+1

	return State( t,tuple(-robots[::-1]), tuple(-resources[::-1]), maxt-np.sum(robots) )



# totest = [[[0]],[[0]],[[0],[1],[0,1],[1,0]],[[0],[2],[0,2],[2,0]]]
totest = [[[0], [1]], [[0], [1]], [[0], [1], [2]], [[0], [1], [2], [3]]]


pruned = []
def to_prune(state,inQ,maxt,weights):
	prune = False
	dt = inQ.t - state.t
	temp_resources = np.add(state.resources,np.multiply(dt,state.robots))
	rless = np.greater(temp_resources, inQ.resources)
	if state == inQ:
		prune = True
	elif np.all(np.less_equal(state.robots, inQ.robots)):
		if np.all(np.less_equal(temp_resources, inQ.resources)):
			prune = True
		elif np.all(np.equal(rless, np.array([False, False, False, True]))) and \
				state.robots[-1] <= -np.max(weights[1:, 0]) and temp_resources[-1] <= -np.max(weights[1:,0]):
			prune = True
		elif np.all(np.equal(rless, np.array([False, False, True, False]))) and \
				state.robots[-2] <= -np.max(weights[1:, 1]) and temp_resources[-2] <= -np.max(weights[1:,1]):
			prune = True
		elif np.all(np.equal(rless, np.array([False, True, False, False]))) and \
				state.robots[-3] <= -np.max(weights[1:, 2]) and temp_resources[-3] <= -np.max(weights[1:, 2]):
			prune = True
	if (state.t == inQ.t) and (inQ.resources[0] - state.resources[0] >= 2) and \
			np.all(np.less(state.robots[:2],inQ.robots[:2])):
		prune = True
	if (inQ.resources[0]-state.resources[0]) > (maxt - state.t) and state.robots[0] <= inQ.robots[0]:
		prune = True

	return prune


def find_geodes_dfs(maxt, w = weights):
	max_robots = np.max(w[1:,:],axis=0)
	max_robots[-1] =  maxt
	searchQ = SortedList()
	state = State(t=1, robots=(0, 0, 0, -1), resources=(0, 0, 0, 0), numr=maxt-1)
	best = state
	searchQ.add(add_robot(0, state, maxt, w))
	searchQ.add(add_robot(1, state, maxt, w))

	while searchQ:
		if searchQ[0].t > maxt:
			break
		else:
			state = searchQ.pop(0)

		# Prune nodes that all robots are equal or less and all resources are equal or less than current state
		if best.t != state.t:
			best = state

		cnt = 0
		while cnt < len(searchQ):
			if to_prune(state, searchQ[cnt], maxt, w):
				searchQ.pop(cnt)
			# elif (best.t == searchQ[cnt].t) and ((searchQ[cnt].numr - best.numr) > 4):
			# 	 searchQ.pop(cnt)
			else:
				cnt +=1


		# Test to add each of the 4 robots and add to heap if have ability to make inputs
		robots = -np.array(state.robots)[::-1]
		for rtoadd in range(4):
			if rtoadd<2 or (rtoadd == 2 and robots[1] != 0) or (rtoadd == 3 and robots[2] != 0):
				if robots[rtoadd] < max_robots[rtoadd]:
					temp_robot = add_robot(rtoadd, state, maxt, w)
					if temp_robot.t <= maxt or (temp_robot.t> maxt and temp_robot.resources[0]<0):
						searchQ.add(temp_robot)
					else:
						pass

	obs = 0 if not searchQ else -min([searchQ[cnt].resources[0] for cnt in range(len(searchQ))])
	return obs


def extract_blueprint(bp):
	weights = np.zeros([4, 4], dtype=int)
	weights[0, 0] = bp[1]  	# ore
	weights[1, 0] = bp[2]   # clay
	weights[2, 0] = bp[3]   # obsidian
	weights[2, 1] = bp[4]
	weights[3, 0] = bp[5]   # geode
	weights[3, 2] = bp[6]
	indx = int(bp[0])
	return indx, weights

# Part 1: Quality of blueprint metrics
value=0
for bp in blueprints:
	# bp = blueprints[4]
	indx, weights = extract_blueprint(bp)
	# pruned.clear()
	geodes = find_geodes_dfs(24, weights)
	print(indx, geodes)
	value += geodes * indx

print(f'Part 1: Quality Metric: {value}')

# Part 2
value2=1
for bp in blueprints[:3]:
	# bp = blueprints[2] #################################
	indx, weights = extract_blueprint(bp)
	geodes = find_geodes_dfs(32, weights)
	print(indx, geodes)
	value2 *= geodes
print(f'Part 2: Product of metrics {value2}')
