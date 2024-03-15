# Read the beacon and sensor locations
# with open('dec21Test.txt', 'r') as file:
with open('dec21.txt', 'r') as file:
	lines = file.readlines()

table = {}
for line in lines:
	split = line.split(':')
	name = split[0].strip()
	operation = split[1].strip()
	table[name] = operation

print(table)

def find_value(name):
	operation = table[name]

	if operation.isnumeric():
		return int(operation)

	operation = operation.split()
	val1 = find_value(operation[0])
	val2 = find_value(operation[2])

	match operation[1]:
		case '+':
			return val1+ val2
		case '-':
			return val1 - val2
		case '*':
			return val1 * val2
		case '/':
			return val1 / val2
	return


val = find_value('root')
print(f'Part 1: Root monkey yells {val}')