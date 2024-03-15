from sympy import symbols, solve, sympify

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

	if name == 'humn':
		return 'x'

	if operation.isnumeric():
		return operation

	operation = operation.split()
	val1 = find_value(operation[0])
	val2 = find_value(operation[2])

	if name == 'root':
		x = symbols('x')
		out = solve(sympify(val2 + '-' + val1), x)
		return out
	else:
		return '(' + val1 + operation[1] + val2 + ')'


val = find_value('root')
print(f'Part 2: Human yells  {val}')