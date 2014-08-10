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
				opc_sf = opcode[31]
				opc_Rm= opcode[16:21][::-1]
				opc_option = opcode[13:16][::-1]
				opc_imm3 = opcode[10:13][::-1]
				opc_Rn = opcode[5:10][::-1]
				opc_Rd = opcode[0:5][::-1]

				d = int( opc_Rd , base=2)
				n = int( opc_Rn , base=2)
				m = int( opc_Rn , base=2)
				if opc_sf == '1':
					# 64 bit execution
					if(d == 31):
						Rd = 'sp'
					else:
						Rd = 'x' + str(d)
					if n == 31:
						Rn = 'sp'
					else:
						Rn = 'x' + str(n)
				else:
					# 32 bit execution
					if(d == 31):
						Rd = 'wsp'
					else:
						Rd = 'w' + str(d)

					if(n == 31):
						Rn = 'wsp'
					else:
						Rn = 'w' + str(n)


				option = int(opc_option, base=2)
				if option %4 == 3:
					Rm = 'x' + str(m)
				else:
					Rm = 'w' + str(m)
				inst.opcode_br['Rm'] = Rm
				inst.opcode_br['Rn'] = Rn
				inst.opcode_br['Rd'] = Rd
				inst.disassembly = 'ADD {0}, {1}, {2}'.format(Rd, Rm, Rn)
				inst.operation = ADD_EXTENDED_REGISTER_OP
				return inst

			elif i ==1:
				# ADD_SHIFTED_REGISTER
				inst = instruction(opcode)
				opc_Rd = opcode[0:5]
				opc_Rn = opcode[5:10]
				opc_Rm = opcode[16:21]




def ADD_EXTENDED_REGISTER_OP(instruction, context):
	pc = context.get_regval('pc')
	print "ADD_EXTENDED_REGISTER : Not implemented yet"
	pc += 4
	context.set_regval('pc', pc)
				
