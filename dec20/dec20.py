import numpy as np
from math import fmod
# with open('dec20Test.txt','r') as file:
with open('dec20.txt', 'r') as file:
	lines = file.readlines()

array = np.array([*enumerate([int(line) for line in lines])])
# array[array[:,1]==0,1] += 14
N = array.shape[0]

print(array[:, 1].transpose())
for cnt in range(N):
	start =  np.where(array[:,0]==cnt)[0][0]
	temp = array[start, :]
	array = np.delete(array,start,axis=0)
	array =  np.insert(array, int(fmod(temp[1]+start,N-1)), temp,axis=0)
	print(array[:,1].transpose())

pos_zero = np.where(array[:,1]%N==0)[0][0]
out = array[(pos_zero+1000)%N,1] + array[(pos_zero+2000)%N,1] + array[(pos_zero+3000)%N,1]
print(f'Part 1: The sum of the 1000th, 2000th and 3000th grove is: {out}')


#########
# Part 2: Read the data, decrypt 10 times in a loop
#########
array = np.array([*enumerate([int(line) for line in lines])])
array[:,1] *= 811589153
N = array.shape[0]
# print(array[:, 1].transpose())

# Decrypt 10 times
for _ in range(10):
	for cnt in range(N):
		start = np.where(array[:, 0] == cnt)[0][0]
		temp = array[start, :]
		array = np.delete(array, start, axis=0)
		array = np.insert(array, int(fmod(temp[1] + start, N - 1)), temp, axis=0)
		# print(array[:, 1].transpose())

pos_zero = np.where(array[:, 1] % N == 0)[0][0]
out = array[(pos_zero + 1000) % N, 1] + array[(pos_zero + 2000) % N, 1] + array[(pos_zero + 3000) % N, 1]
print(f'Part 2: The sum of the 1000th, 2000th and 3000th grove after 10 iterations is: {out}')