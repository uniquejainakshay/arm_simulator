# Data processing - Immediate
# This disassembles following instructions from this class 

#DR x2,_start 
# ADD_IMMEDIATE 4 eg ADD w1, w2, #4 eg ADD w1, w2, #4 eg ADD w1, w2, #4
#ADRP x2, _start


	
from instruction import instruction
from common_functions import *

##################   Instructions 
instructions = [
#0
'ADD_IMMEDIATE', 
#1
'ADDS_IMMEDIATE'
]


####### 	Instruction mask

inst_mask = [
#0
'00000000000000000000000011111110', 
#1
'00000000000000000000000011111110' 
]


#######		Inst identifier

inst_identifier = [
#0
'00000000000000000000000010001000',
#1
'00000000000000000000000010001000'
]

def interpret(opcode):

	for i in range(len(inst_mask)):
		masked_opcode = int(opcode, base=2) & int(inst_mask[i], base =2)
		if masked_opcode == int(inst_identifier[i], base=2):

			if instructions[i] == 'ADD_IMMEDIATE' or\
				instructions[i] == 'ADDS_IMMEDIATE':

				# ADD_IMMEDIATE
				inst = instruction(opcode)
				inst.opcode_br['sf'] = opcode[31]
				inst.opcode_br['op'] = opcode[30]
				inst.opcode_br['S'] = opcode[29]
				inst.opcode_br['shift'] = int(opcode[22:24][::-1], base = 2)
				inst.opcode_br['imm12'] = opcode[10:22][::-1]
				Rn = int(opcode[5:10][::-1], base = 2)
				Rd = int(opcode[0:5][::-1], base = 2)
				datasize = -1
				
				if inst.opcode_br['sf'] == '0':
					# 32-bit variant
					# ADD <Wd|WSP>, <Wn|WSP>, #<imm>{, <shift>}
					if Rn == 31:
						inst.opcode_br['Rn'] = 'wsp'
					else:
						inst.opcode_br['Rn'] = 'w'+str(Rn)
					
					if Rd == 31:
						inst.opcode_br['Rd'] = 'wsp'
					else:
						inst.opcode_br['Rd'] = 'w'+str(Rd)			
					datasize = 32	
					
				else:
					# 64-bit variant
					# ADD <Xd|SP>, <Xn|SP>, #<imm>{, <shift>}
					if Rn == 31:
						inst.opcode_br['Rn'] = 'sp'
					else:
						inst.opcode_br['Rn'] = 'x'+str(Rn)	
				
					if Rd == 31:
						inst.opcode_br['Rd'] = 'sp'
					else:
						inst.opcode_br['Rd'] = 'x'+str(Rd)
					datasize = 64	
				
				inst.opcode_br['imm'] = '\x00'
				
				if inst.opcode_br['shift'] == 0:
					inst.opcode_br['imm'] = ZeroExtend(inst.opcode_br['imm12'], datasize)
					
				elif inst.opcode_br['shift'] == 1:
					inst.opcode_br['imm'] = ZeroExtend(inst.opcode_br['imm12']+'000000000000', datasize)
					
				
				imm = hex(int(inst.opcode_br['imm12'], base = 2))
				shift = hex(inst.opcode_br['shift'])
				if instructions[i] == 'ADD_IMMEDIATE':
					inst.disassembly = "ADD ", inst.opcode_br['Rd']+", ", 
					inst.opcode_br['Rn']+", ", "#<"+imm+">{, <",shift,">}"
					inst.operation = ADDS_IMMEDIATE_OP;
				elif instructions[i] == 'ADDS_IMMEDIATE' :
					inst.disassembly = "ADDS ", inst.opcode_br['Rd']+", ", 
					inst.opcode_br['Rn']+", ", "#<"+imm+">{, <",shift,">}"
					inst.operation = ADDS_IMMEDIATE_OP;
				
				return inst

def ADD_IMMEDIATE_OP(inst, context):
	operand2 = inst.opcode_br['imm']
	operand1 = ZeroExtend(bin(context.get_regval(inst.opcode_br['Rn']))[2:], len(operand2))

	result, n, z, c, v = AddWithCarry(operand1, operand2, '0')
	context.set_regval(inst.opcode_br['Rd'], result)
	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)

def ADDS_IMMEDIATE_OP(inst, context):
	operand2 = inst.opcode_br['imm']
	operand1 = ZeroExtend(bin(context.get_regval(inst.opcode_br['Rn']))[2:], len(operand2))

	result, n, z, c, v = AddWithCarry(operand1, operand2, '0')
	context.set_regval(inst.opcode_br['Rd'], result)
# setting flags as adds instruction
	context.flags['n'] = n
	context.flags['z'] = z
	context.flags['c'] = c
	context.flags['v'] = v


	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)
