import math
def process_monkey(lines):
	# First line is Monkey number
	num = int(lines[0].strip().replace(':','').split()[1])

	# Second line is starting items
	items_txt = lines[1].strip().split(':')[1].split(',')
	items = [int(item) for item in items_txt]

	# Third line is operation
	operation = lines[2].strip().split(':')[1].strip()

	# Fourth line is test
	divby = int(lines[3].strip().split()[-1])

	# Fifth line is true monkey
	trueDestination = int(lines[4].strip().split()[-1])

	# Sixth line is false monkey
	falseDestination = int(lines[5].strip().split()[-1])

	return {'num': num, 'items':items, 'operation':operation, 'divby':divby, 'destTrue': trueDestination, 'destFalse':falseDestination}

def run_process(monkeys,relief=3):
	divisors = [monkeys[i]['divby'] for i in range(len(monkeys))]
	divs_lcm = math.prod(divisors)*relief #lcm(*divisors)
	count = [0]*len(monkeys)
	for monkey in range(len(monkeys)):
		count[monkey] += len(monkeys[monkey]['items'])
		for old in monkeys[monkey]['items']:
			new =  eval(monkeys[monkey]['operation'].split('=')[1])
			new = new // relief
			if new > 2*divs_lcm:
				new = new % divs_lcm + divs_lcm

			# Test for destination
			if new % monkeys[monkey]['divby'] == 0:
				monkeys[monkeys[monkey]['destTrue']]['items'].append(new)
			else:
				monkeys[monkeys[monkey]['destFalse']]['items'].append(new)

		monkeys[monkey]['items'].clear()

	return count

#######
# Part 1
#######
# with open('dec11Test.txt','r') as file:
with open('dec11.txt', 'r') as file:
	lines = file.readlines()

monkeys = []
for cnt in range(0,len(lines),7):
	monkeys.append(process_monkey(lines[cnt:cnt+7]))

# Run the process 20 times
total = []
for cnt in range(20):
	counts = run_process(monkeys)
	if not total:
		total = counts
	else:
		total = [total[i]+counts[i] for i in range(len(total))]

total.sort(reverse=True)
print(f'Part1: {total[0]*total[1]}')

######
# Part 2
######
# Repeat same as above but relief=1 and run 10000 times
# with open('dec11Test.txt','r') as file:
with open('dec11.txt', 'r') as file:
	lines = file.readlines()

monkeys.clear()
for cnt in range(0, len(lines), 7):
	monkeys.append(process_monkey(lines[cnt:cnt + 7]))

# Run the process 10000 times
total.clear()
for cnt in range(10000):
	# if cnt%100 == 0:
	# 	print(cnt)
	counts = run_process(monkeys,relief=1)
	if not total:
		total = counts
	else:
		total = [total[i] + counts[i] for i in range(len(total))]

total.sort(reverse=True)
print(f'Part2: {total[0] * total[1]}')


