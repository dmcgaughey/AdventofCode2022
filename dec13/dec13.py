import numpy as np
from itertools import zip_longest

def list_string_less_than(l_str,r_str):
	left = eval(l_str.strip())
	right = eval(r_str.strip())
	return -list_less_than(left, right)

def list_less_than(left,right):
	# Case: Both are integers
	if isinstance(left, int) and isinstance(right, int):
		if left == right:
			return 0
		elif left < right:
			return 1
		else:
			return -1

	# Cose: 1 int and 1 list
	if isinstance(left, int) and isinstance(right,list):
		return list_less_than([left],right)
	if isinstance(left, list) and isinstance(right,int):
		return list_less_than(left,[right])

	# Case 2 lists
	for litem, ritem in zip_longest(left,right):
		if litem==None and ritem==None: return 0
		elif litem==None:  return 1
		elif ritem==None:  return -1

		if (temp:= list_less_than(litem,ritem)) !=0:
			return temp

	# Went through all the lists and have not found any differences
	return 0

###########
# Part 1
# List comparison
###########


# Read the string with the wind gusts
# with open('dec13Test.txt','r') as file:
with open('dec13.txt', 'r') as file:
	lines = file.readlines()

correct_order=[]
indx = 0
for cnt in range(0,len(lines),3):
	left = eval(lines[cnt].strip())
	right = eval(lines[cnt+1].strip())

	if list_less_than(left,right)>0:
		correct_order.append(cnt//3+1)
print(correct_order)
print(sum(correct_order))

#########
# Part 2
#########
from functools import cmp_to_key
lines = [line.strip() for line in lines if line!='\n']
lines.append('[2]')
lines.append('[6]')

lines.sort(key=cmp_to_key(list_string_less_than))
indx1 = lines.index('[2]')+1
indx2 = lines.index('[6]')+1

print(f'Part2: {indx1*indx2}')