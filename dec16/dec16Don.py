import numpy as np, collections as c, re, functools, itertools
from functools import cache

D, W, V = c.defaultdict(lambda:1000),dict(), set()

nodes = re.findall(r'Valve *(\w+) .*=(\d+); .* valves? *(.*)',open('dec16.txt','r').read())
for v,w,dests in nodes:
	V.add(v)
	if w !='0': W[v] = int(w)
	for d in dests.replace(' ','').split(','):
		D[v,d] = D[d,v]= 1

for k,i,j in itertools.product(sorted(V),repeat=3):
	# print(i,k,j,min(D[i,j], D[i,k]+D[k,j]))
	D[i,j] = D[j,i] = min(D[i,j], D[i,k]+D[k,j])


def search(t,node, rnodes = frozenset(W)):
	new_weight = [0]
	for next_node in rnodes:
		if (new_t := t-D[node,next_node]-1) >0:
			w = new_t*W[next_node] + search(new_t,next_node,rnodes-{next_node})
		else:
			w = 0
		new_weight.append(w)
	return max(new_weight)


def search2(t,nodes, rnodes = frozenset(W)):
	if (t[0]<=2 and t[1]<=2) or len(rnodes)==0: return 0

	new_weight = []
	for next_node in rnodes:
		if t[0] >= t[1] and (new_t := t[0]-D[nodes[0],next_node]-1) >0:
			w = new_t*W[next_node] + search2((new_t,t[1]),(next_node,nodes[1]),rnodes-{next_node})
		elif (new_t := t[1]-D[nodes[1],next_node]-1) >0:
			w = new_t*W[next_node] + search2((t[0],new_t),(nodes[0],next_node),rnodes-{next_node})
		else:
			w = 0
		new_weight.append(w)
		if t==(26,26):
			print(new_weight)

	return max(new_weight)


print(search(30,'AA'))

print(search2((26,26),('AA','AA')))

# if len(rnodes) == 1:
# 	rnodes = frozenset(set(rnodes).union({None}))
# for nn0, nn1 in itertools.permutations(rnodes, 2):
# 	if nn0 and (new_t0 := t[0] - D[nodes[0], nn0] - 1) > 0:
# 		w0 = new_t0 * W[nn0]
# 	else:
# 		w0 = 0
# 	if nn1 and (new_t1 := t[1] - D[nodes[1], nn1] - 1) > 0:
# 		w1 = new_t1 * W[nn1]
# 	else:
# 		w1 = 0
# 	w = w0 + w1 + search2((new_t0, new_t1), (nn0, nn1), rnodes - {nn0, nn1})
# 	new_weight.append(w)