# Data processing - Register
# This disassembles following instructions from this class 

#ADD w1, w2, w3
#ADDS w1, w2, w3
#SUB w1, w2, w3
#SUBS w1, w2, w3
#ASR w1, w2, w3
#AND w1, w2, w3
#CMP w1, w2
#LSL w1, w2, w3 
#LSR w1, w2, w3 
#MOV w1, w2
instructions = ['ADD' ,'ADDS' ,'SUB' ,'SUBS' ,'ASR' ,'AND' ,'CMP' ,'LSL' ,'LSR' ,'MOV']
inst_mask = ['00000000000000000000011111111110']
inst_identifier = ['00000000000000000000010011010000']

def interpret(opcode):

	for i in range(len(inst_mask)):
		masked_opcode = int(opcode, base=2) & int(inst_mask[i], base =2)
		print opcode , "\n", inst_mask[i], "\n", inst_identifier[i]
		if masked_opcode == int(inst_identifier[i], base=2):
			print "Instruction is : " , instructions[i]




