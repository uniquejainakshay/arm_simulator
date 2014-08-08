inst_class_mask = ['00000000000000000000000000011000', '00000000000000000000000000111000', '00000000000000000000000000111000', '00000000000000000000000001010000', '00000000000000000000000001110000', '00000000000000000000000001111000', '00000000000000000000000001111000']


inst_class_identifier= ['00000000000000000000000000000000', '00000000000000000000000000001000', '00000000000000000000000000101000', '00000000000000000000000000010000', '00000000000000000000000001010000', '00000000000000000000000001110000', '00000000000000000000000001111000']

# function identify_class(instruction)
#identifies the class of the instruction from its opcode as follows

# code 		class
#  0 		Unallocated
#  1 		Data processing - Immediate 
#  2 		Branch, exception generation and system instructions'
#  3 		Loads and stores
#  4 		Data processing - register', ' Data processing - SIMD and floating point
#  5 		Data processing - SIMD and floating point'
#  6 		Data processing - SIMD and floating point'

# return value : returns  the associated code for each class


def identify_class(inst):
	global inst_class_mask, inst_class_identifier
	inst_int = int(inst, base=2)
	for i in range(6):
		masked = inst_int & int(inst_class_mask[i], base=2)
		if masked == int(inst_class_identifier[i], base=2):
			return i

	return -1
