import numpy as np

def SNAFU2int(snafu:str)->int:
	snafu = snafu.strip()
	val = 0
	for cnt,c in enumerate(snafu):
		e = len(snafu) - cnt - 1
		if c == '=': d = -2
		elif c == '-': d = -1
		else: d = int(c)
		val += d * 5**e
	return val


def int2SNAFU(val:int)->str:
	snafu = [ int(a) for a in list('00000' + np.base_repr(val,5))[::-1]]
	for cnt in range(len(snafu)):
		if snafu[cnt] > 2:
			snafu[cnt+1] += 1
			snafu[cnt] -= 5
		if snafu[cnt] == -2: snafu[cnt] = '='
		elif snafu[cnt] == -1: snafu[cnt] = '-'
		else: snafu[cnt] = str(snafu[cnt])

	out = (''.join(snafu))[::-1].lstrip('0')
	return out


# Read the beacon and sensor locations
# with open('dec25Test.txt', 'r') as file:
with open('dec25.txt', 'r') as file:
	lines = file.readlines()

sum = 0
for line in lines:
	print(value:=SNAFU2int(line.strip()))
	sum += value

print(sum, int2SNAFU(sum))