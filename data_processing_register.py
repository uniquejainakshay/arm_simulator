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

from instruction import instruction

##################   Instructions 
instructions = [
#0
'ADD_EXTENDED_REGISTER' , 
#1
'ADD_SHIFTED_REGISTER'
]


####### 	Instruction mask

inst_mask = [
#0
'00000000000000000000011111111110', 
#1
'00000000000000000000010011111110', 
]


#######		Inst identifier

inst_identifier = [
#0
'00000000000000000000010011010000',
#1
'00000000000000000000000011010000' 
]

def interpret(opcode):

	for i in range(len(inst_mask)):
		masked_opcode = int(opcode, base=2) & int(inst_mask[i], base =2)
		if masked_opcode == int(inst_identifier[i], base=2):



			if i == 0:
				# ADD_EXTENDED_REGISTER
				inst = instruction(opcode)
				inst.opcode_br['sf'] = opcode[31]
				inst.opcode_br['Rm'] = opcode[16:21][::-1]
				inst.opcode_br['option'] = opcode[13:16][::-1]
				inst.opcode_br['imm3'] = opcode[10:13][::-1]
				inst.opcode_br['Rn'] = opcode[5:10][::-1]
				inst.opcode_br['Rd'] = opcode[0:5][::-1]
				







