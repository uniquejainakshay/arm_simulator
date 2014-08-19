# Branch , Exception Generation and System instructions  
# This disassembles following instructions from this class 

#B _start
#BR X2
#BL _start
#BLR x2
#CBZ w2, _start
#BLE     ng+8
#BL      subC
#NOP
from instruction import instruction
from common_functions import *

instructions = [
#0
'B.cond',
#1
'B',
#2
'BR',
#3
'BL',
#4
'BLR',
#5
'CBNZ',
#6
'CBZ',
#7
'RET',
#8
'NOP'
]


####### 	Instruction mask

inst_mask = [
#0
'00001000000000000000000011111111',
#1
'00000000000000000000000000111111',
#2
'11111000001111111111111111111111',
#3
'00000000000000000000000000111111',
#4
'11111000001111111111111111111111',
#5
'00000000000000000000000011111110',
#6
'00000000000000000000000011111110',
#7
'11111000001111111111111111111111',
#8
'11111000000011111111111111111111'
]


#######		Inst identifier

inst_identifier = [
#0
'00000000000000000000000000101010',
#1
'00000000000000000000000000101000',
#2
'00000000000000001111100001101011',
#3
'00000000000000000000000000101001',
#4
'00000000000000001111110001101011',
#5
'00000000000000000000000010101100',
#6
'00000000000000000000000000101100',
#7
'00000000000000001111101001101011',
#8
'11111000000001001100000010101011'
]


def interpret(opcode):
	for i in range(len(inst_mask)):
		masked_opcode = int(opcode, base=2) & int(inst_mask[i], base =2)
		if masked_opcode == int(inst_identifier[i], base=2):

			if instructions[i] == 'B.cond':
				inst = instruction(opcode)
				inst.opcode_br['cond'] = opcode[0:4][::-1]
				inst.opcode_br['imm19'] = opcode[5:24][::-1]
				
				inst.disassembly = "B.{0} #{1}".format(inst.opcode_br['cond'], hex(int(inst.opcode_br['imm19'], base=2)*4))
				
				inst.operation = B_cond
				return inst
			elif instructions[i] == 'B':
				inst = instruction(opcode)
				inst.opcode_br['op'] = opcode[31]
				inst.opcode_br['imm26'] = opcode[0:26][::-1]
				
				inst.disassembly = "B {0}".format(int(inst.opcode_br['imm26'], base =2)*4)
				
				inst.operation = B
				return inst
			elif instructions[i] == 'BR':
				inst = instruction(opcode)
				inst.opcode_br['op'] = opcode[21:23][::-1]
				inst.opcode_br['Rn'] = opcode[5:10][::-1]
				
				rn = UInt(inst.opcode_br['Rn'])
				
				inst.disassembly = "BR {0}".format('x'+str(rn))
				
				inst.operation = BR
				return inst
			
			elif instructions[i] == 'BL':
				inst = instruction(opcode)
				inst.opcode_br['imm26'] = opcode[0:26][::-1]
				inst.opcode_br['op'] = opcode[31]
				
				inst.disassembly = "BL {0}".format(inst.opcode_br['op']+'00')
				
				inst.operation = BL
				return inst	
			
			elif instructions[i] == 'BLR':
				inst = instruction(opcode)
				inst.opcode_br['Rn'] = opcode[5:10][::-1]
				inst.opcode_br['op'] = opcode[21:23][::-1]
				
				rn = UInt(inst.opcode_br['Rn'])
				inst.disassembly = "BLR {0}".format('x'+str(rn))
				
				inst.operation = BLR
				return inst	
			
			elif instructions[i] == 'CBNZ'\
			  or instructions[i] == 'CBZ':
				inst = instruction(opcode)
				inst.opcode_br['Rt'] = opcode[0:5][::-1]
				inst.opcode_br['imm19'] = opcode[5:24][::-1]
				inst.opcode_br['op'] = opcode[24]
				inst.opcode_br['sf'] = opcode[31]
				
				rt = UInt(inst.opcode_br['Rt'])
				if inst.opcode_br['sf'] == '0':
					inst.disassembly = "CBNZ {0}, {1}".format('w'+str(rt), int(inst.opcode_br['imm19'], base = 2)*4)
				else:
					inst.disassembly = "CBNZ {0}, {1}".format('x'+str(rt), int(inst.opcode_br['imm19'], base = 2)*4)
					
				inst.operation = CBNZ
				return inst
			
			elif instructions[i] == 'RET':
				inst = instruction(opcode)
				inst.opcode_br['Rn'] = opcode[5:10][::-1]
				inst.opcode_br['op'] = opcode[21:23][::-1]
				
				rn = int(inst.opcode_br['Rn'], base = 2)
				inst.disassembly = "RET {0}".format('x'+str(rn))
					
				inst.operation = RET
				return inst									

			elif instructions[i] == 'NOP':
				inst = instruction(opcode)
				inst.opcode_br['CRm'] = opcode[8:12][::-1]
				inst.opcode_br['op2'] = opcode[5:8][::-1]
				
				inst.disassembly = "NOP"
					
				inst.operation = NOP
				return inst
	print "Unindentified instruction"

def B_cond(inst , context):
	offset = SignExtend(inst.opcode_br['imm19']+'00', 64);
	#print offset, "dfvndnslkfvndjnbdjfbndjfnbdjfnb"
	condition = inst.opcode_br['cond']
	
	if ConditionHolds(condition, context):
		target = SInt(offset)  + context.get_regval('pc')
		context.set_regval('pc', target) 
	else:
		pc = context.get_regval('pc')
		pc += 4
		context.set_regval('pc', pc)	

def B(inst , context):
	branch_type = 'BranchType_CALL' if inst.opcode_br['op'] == '1' else 'BranchType_JMP';
	offset = SignExtend(inst.opcode_br['imm26']+'00', 64);

	
	target = SInt(offset)  + context.get_regval('pc')
	context.set_regval('pc', target)

def BR(inst , context):
	n = UInt(inst.opcode_br['Rn']);
	target = context.get_regval('x'+str(n))
	context.set_regval('pc', target)

def BL(inst , context):
	offset = SignExtend(inst.opcode_br['imm26']+'00', 64)
	target = SInt(offset)  + context.get_regval('pc')
	context.set_regval('pc', target)	

def BLR(inst , context):
	n = UInt(inst.opcode_br['Rn']);
	target = context.get_regval('x'+str(n))
	context.set_regval('pc', target)
	
def CBNZ(inst , context):
	t = UInt(inst.opcode_br['Rt']);
	datasize = 64 if inst.opcode_br['sf'] == '1' else 32;
	iszero = (inst.opcode_br['op'] == '0');
	offset = SignExtend(inst.opcode_br['imm19']+'00', 64);
	
	operand1 = context.get_regval('x'+str(t))
	if (operand1 == 0) == iszero:
		target = SInt(offset)  + context.get_regval('pc')
		context.set_regval('pc', target)
	else:
		pc = context.get_regval('pc')
		pc += 4
		context.set_regval('pc', pc)			

def RET(inst , context):
	n = UInt(inst.opcode_br['Rn']);
	target = context.get_regval('x'+str(n))
	context.set_regval('pc', target)

def NOP(inst , context):	
	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)			
	pass
