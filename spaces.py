#messy module for displaying arrays
def longest(array_names):
	'''
	finds the largest title in the array then finds its length 
	'''
	maxim = ""
	maxim = len(array_names[0])
	for i in range(len(array_names)):	
		if len(array_names[i])>maxim:
			maxim = len(array_names[i])
	return maxim
def no_spaces(array_input):
	'''
	finds the number of no_spaces that each title should have
	'''
	#loop through the array, and for each title, find the number of spaces needed to balanc out such that the longest title has a space of 1 before the next
	num = [0]*len(array_input)
	max = longest(array_input)
	for counter in range((len(array_input))):
		num[counter] = (max+2) - (len(array_input[counter]))
	return num
	
def spaces(array_input,symbol = None):
	if symbol:
		sign = symbol
	else:
		sign = "-"
	space = [""]*len(array_input)
	for k in range(len(array_input)):
		for i in range(no_spaces(array_input)[k]):
			space[k]+= sign
	return space

def no_items(all_arrays):
	'''
	finds the number of no_items that each array should have
	'''
	num = [0]*len(all_arrays)
	max = longest(all_arrays)
	for counter in range((len(all_arrays))):
		num[counter] = (max) - (len(all_arrays[counter]))
	return num
def blanks(all_arrays):
	for k in range(len(all_arrays)):
		for i in range(no_items(all_arrays)[k]):
			all_arrays[k].append("")
	return all_arrays

def display(array1,array2):
	string = ""
	all_arrays = [array1,array2]
	for k in range(longest(all_arrays)):
		string += (str(array1[k])+" "+spaces(array1)[k]+" "+str(array2[k])+"\n")
	return string
def single(Array1,symbol = None, end = None):
	string = ""
	if symbol:
		sign = symbol
	else: 
		sign = "•"
	if end:
		end_sign = end
	else:
		end_sign = ""
	 
	for k in Array1:
		string += sign+str(k)+f"{end_sign}\n"
	return string