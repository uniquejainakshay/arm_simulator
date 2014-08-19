# Loads and stores instructions
# This disassembles following instructions from this class 

#LDP w1, w2, [sp], #12
#LDR w1, [X1], #10
#LDRSW x1, [x2], #10
#STP w1, w2, [x1], #12
#STR w1, [x1], #24

from instruction import instruction
from common_functions import *

instructions = [
#0
'LDP_post_index',
#1
'LDP_pre_index',
#2
'LDP_signed_offset'
]


####### 	Instruction mask

inst_mask = [
#0
'00000000000000000000001111111110',
#1
'00000000000000000000001111111110',
#2
'00000000000000000000001111111110',
]


#######		Inst identifier

inst_identifier = [
#0
'00000000000000000000001100010100',
#1
'00000000000000000000001110010100',
#2
'00000000000000000000001010010100',
]


def interpret(opcode):
	for i in range(len(inst_mask)):
		masked_opcode = int(opcode, base=2) & int(inst_mask[i], base =2)
		if masked_opcode == int(inst_identifier[i], base=2):

			if instructions[i] == 'LDP_post_index' or instructions[i] == 'LDP_pre_index' or\
			instructions[i] == 'LDP_signed_offset':
				inst = instruction(opcode)
				inst.opcode_br['opc'] = opcode[30:32][::-1]
				inst.opcode_br['L'] = opcode[22]
				inst.opcode_br['imm7'] = opcode[15:22][::-1]
				inst.opcode_br['Rt2'] = opcode[10:15][::-1]
				inst.opcode_br['Rn'] = opcode[5:10][::-1]
				inst.opcode_br['Rt'] = opcode[0:5][::-1]
				
				Rt2 = UInt(inst.opcode_br['Rt2'])
				Rn = UInt(inst.opcode_br['Rn'])
				Rt = UInt(inst.opcode_br['Rt'])
				
				if opcode[23:26][::-1] = '001':
					if inst.opcode_br['opc'] = '00':
						Rt = 'w'+str(Rt)
						Rt2 = 'w'+str(Rt2)
						
						if Rn == 31:
							Rn = 'sp'
						else:
							Rn = 'w'+str(Rn)	
						
						imm = inst.opcode_br['imm7']+'00'
						imm = SInt(imm)
						
					else:
						Rt = 'x'+str(Rt)
						Rt2 = 'x'+str(Rt2)
						
						if Rn == 31:
							Rn = 'sp'
						else:
							Rn = 'x'+str(Rn)
						
						imm = inst.opcode_br['imm7']+'000'
						imm = SInt(imm)	
					inst.disassembly = "LDP {0}, {1}, [{2}], #{3}".format(Rt, Rt2, Rn, imm)
							
				elif opcode[23:26][::-1] = '011':
					if inst.opcode_br['opc'] = '00':
						Rt = 'w'+str(Rt)
						Rt2 = 'w'+str(Rt2)
						
						if Rn == 31:
							Rn = 'sp'
						else:
							Rn = 'w'+str(Rn)	
						
						imm = inst.opcode_br['imm7']+'00'
						imm = SInt(imm)
						
					else:
						Rt = 'x'+str(Rt)
						Rt2 = 'x'+str(Rt2)
						
						if Rn == 31:
							Rn = 'sp'
						else:
							Rn = 'x'+str(Rn)
						
						imm = inst.opcode_br['imm7']+'000'
						imm = SInt(imm)	
					inst.disassembly = "LDP {0}, {1}, [{2}, #{3}]!".format(Rt, Rt2, Rn, imm)
					
				elif opcode[23:26][::-1] = '010':
					if inst.opcode_br['opc'] = '00':
						Rt = 'w'+str(Rt)
						Rt2 = 'w'+str(Rt2)
						
						if Rn == 31:
							Rn = 'sp'
						else:
							Rn = 'w'+str(Rn)	
						
						imm = inst.opcode_br['imm7']+'00'
						imm = SInt(imm)
						
					else:
						Rt = 'x'+str(Rt)
						Rt2 = 'x'+str(Rt2)
						
						if Rn == 31:
							Rn = 'sp'
						else:
							Rn = 'x'+str(Rn)
						
						imm = inst.opcode_br['imm7']+'000'
						imm = SInt(imm)	
					inst.disassembly = "LDP {0}, {1}, [{2}, #{3}]".format(Rt, Rt2, Rn, imm)
				
				inst.operation = LDP
				return inst
	print "Unindentified instruction"

def LDP(inst , context):
	n = UInt(inst.opcode_br['Rn'])
	t = UInt(inst.opcode_br['Rt'])
	t2 = UInt(inst.opcode_br['Rt2'])
	acctype = 'AccType_NORMAL'
	memop = 'MemOp_LOAD' if inst.opcode_br['L'] == '1' else 'MemOp_STORE'
	signed = (inst.opcode_br['opc'][::-1][0] != '0')
	scale = 2 + UInt(inst.opcode_br['opc'][::-1][1])
	datasize = 8 << scale
	offset = LSL(SignExtend(inst.opcode_br['imm7'], 64), scale)
	
	
