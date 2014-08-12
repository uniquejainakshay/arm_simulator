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
'ADDS_IMMEDIATE',
#2
'SUB_IMMEDIATE', 
#3
'SUBS_IMMEDIATE',
#4
'AND_IMMEDIATE' ,
#5
'ANDS_IMMEDIATE' ,
#6
'ADR',
#7
'ASR_IMMEDIATE',
#8
'MOV_SP',
#9
'MOV_inverted_wide_immediate',
#10
'MOV_wide_immediate', 
#11
'MOV_BITMASK_IMMEDIATE',
]


####### 	Instruction mask

inst_mask = [
#0
'00000000000000000000000011111110', 
#1
'00000000000000000000000011111110',
#2
'00000000000000000000000011111110', 
#3
'00000000000000000000000011111110',
#4
'00000000000000000000000111111110' ,
#5
'00000000000000000000000111111110' ,
#6
'00000000000000000000000011111001',
#7
'00000000000000000000000111111110' ,
#8
'00000000000000000000000011111110',
#9
'00000000000000000000000111111110',
#10
'00000000000000000000000111111110',
#11
'00000000000000000000000111111110',
]


#######		Inst identifier

inst_identifier = [
#0
'00000000000000000000000010001000',
#1
'00000000000000000000000010001100',
#2
'00000000000000000000000010001010',
#3
'00000000000000000000000010001110',
#4
'00000000000000000000000001001000',
#5
'00000000000000000000000001001110',
#6
'00000000000000000000000000001000',
#7
'00000000000000000000000011001000',
#8
'00000000000000000000000010001000',
#9
'00000000000000000000000101001000',
#10
'00000000000000000000000101001010',
#11
'00000000000000000000000001001100',
]

def interpret(opcode):
	for i in range(len(inst_mask)):
		masked_opcode = int(opcode, base=2) & int(inst_mask[i], base =2)
		if masked_opcode == int(inst_identifier[i], base=2):

			if instructions[i] == 'ADD_IMMEDIATE' or\
				instructions[i] == 'ADDS_IMMEDIATE' or\
				instructions[i] == 'SUB_IMMEDIATE' or\
				instructions[i] == 'SUBS_IMMEDIATE':
				print instructions[i]
				inst = instruction(opcode)
				inst.opcode_br['sf'] = opcode[31]
				inst.opcode_br['op'] = opcode[30]
				inst.opcode_br['S'] = opcode[29]
				inst.opcode_br['shift'] = int(opcode[22:24][::-1], base = 2)
				inst.opcode_br['imm12'] = opcode[10:22][::-1]
				Rn = int(opcode[5:10][::-1], base = 2)
				Rd = int(opcode[0:5][::-1], base = 2)
				datasize = -1
				
				if Rd == 31:
					inst.opcode_br['Rd'] = 'sp'
				else:
					inst.opcode_br['Rd'] = 'x'+str(Rd)


				if inst.opcode_br['sf'] == '0':
					# 32-bit variant
					# ADD <Wd|WSP>, <Wn|WSP>, #<imm>{, <shift>}
					if Rn == 31:
						inst.opcode_br['Rn'] = 'wsp'
					else:
						inst.opcode_br['Rn'] = 'w'+str(Rn)
					
					datasize = 32	
					
				else:
					# 64-bit variant
					# ADD <Xd|SP>, <Xn|SP>, #<imm>{, <shift>}
					if Rn == 31:
						inst.opcode_br['Rn'] = 'sp'
					else:
						inst.opcode_br['Rn'] = 'x'+str(Rn)	
				
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
					inst.operation = ADD_IMMEDIATE_OP;
				elif instructions[i] == 'ADDS_IMMEDIATE' :
					inst.disassembly = "ADDS ", inst.opcode_br['Rd']+", ", 
					inst.opcode_br['Rn']+", ", "#<"+imm+">{, <",shift,">}"
					inst.operation = ADDS_IMMEDIATE_OP;
				elif instructions[i] == 'SUB_IMMEDIATE':
					inst.disassembly = "SUB ", inst.opcode_br['Rd']+", ", 
					inst.opcode_br['Rn']+", ", "#<"+imm+">{, <",shift,">}"
					inst.operation = SUB_IMMEDIATE_OP;
				elif instructions[i] == 'SUBS_IMMEDIATE' :
					inst.disassembly = "SUBS ", inst.opcode_br['Rd']+", ", 
					inst.opcode_br['Rn']+", ", "#<"+imm+">{, <",shift,">}"
					inst.operation = SUBS_IMMEDIATE_OP;


				return inst
			if instructions[i] == 'AND_IMMEDIATE' or\
				instructions[i] == 'ANDS_IMMEDIATE':
				# AND_IMMEDIATE
				inst = instruction(opcode)
				inst.opcode_br['sf'] = opcode[31]
				inst.opcode_br['opc'] = opcode[29:31][::-1]
				inst.opcode_br['N'] = opcode[22]
				inst.opcode_br['immr'] = opcode[16:22][::-1]
				inst.opcode_br['imms'] = opcode[10:16][::-1]
				
				inst.opcode_br['Rn'] = opcode[5:10][::-1]
				inst.opcode_br['Rd'] = opcode[0:5][::-1]
				
				Rn = int(opcode[5:10][::-1], base = 2)
				Rd = int(opcode[0:5][::-1], base = 2)
				datasize = -1
				
				if inst.opcode_br['sf'] == '0' and inst.opcode_br['N'] == '0':
					# AND <Wd|WSP>, <Wn>, #<imm>
					if Rd == 31:
						Rd = 'wsp'
					else:
						Rd = 'w'+str(Rd)			
					datasize = 32	
					imm = inst.opcode_br['N']+inst.opcode_br['immr']+inst.opcode_br['imms']
					if inst.opcode_br['opc'] == '00':
						inst.disassembly = 'AND {0}, {1}, #{2}'.format(Rd, 'w'+str(Rn), int(imm, base=2))
					else:
						inst.disassembly = 'ANDS {0}, {1}, #{2}'.format(Rd, 'w'+str(Rn), int(imm, base=2))
					
				else:
					# 64-bit variant
					# AND <Xd|SP>, <Xn>, #<imm>
					if Rd == 31:
						Rd = 'sp'
					else:
						Rd = 'x'+str(Rd)
					datasize = 64	
					imm = inst.opcode_br['N']+inst.opcode_br['immr']+inst.opcode_br['imms']
					if inst.opcode_br['opc'] == '00':
						inst.disassembly = 'AND {0}, {1}, #{2}'.format(Rd, 'x'+str(Rn), int(imm, base=2))
					else:
						inst.disassembly = 'ANDS {0}, {1}, #{2}'.format(Rd, 'x'+str(Rn), int(imm, base=2))
				
				inst.operation = AND_IMMEDIATE;
				return inst
			elif instructions[i] == 'ADR':
				# ADR
				inst = instruction(opcode)
				inst.opcode_br['op'] = opcode[31]
				inst.opcode_br['immlo'] = opcode[29:31][::-1]
				inst.opcode_br['immhi'] = opcode[5:24][::-1]
				inst.opcode_br['Rd'] = 'x'+str(int(opcode[0:5][::-1], base = 2))
				
				hi = inst.opcode_br['immhi']
				lo = inst.opcode_br['immlo']

				inst.disassembly = 'ADR {0}, {1}'.format(inst.opcode_br['Rd'], int( hi+lo, base = 2))
				
				inst.operation = ADR;
				return inst	
			
			elif instructions[i] == 'ASR_IMMEDIATE':
				# ASR_IMMEDIATE
				inst = instruction(opcode)
				inst.opcode_br['sf'] = opcode[31]
				inst.opcode_br['opc'] = opcode[29:31][::-1]
				inst.opcode_br['N'] = opcode[22]
				inst.opcode_br['immr'] = opcode[16:22][::-1]
				inst.opcode_br['imms'] = opcode[10:16][::-1]
				inst.opcode_br['Rn'] = opcode[5:10][::-1]
				inst.opcode_br['Rd'] = opcode[0:5][::-1]
								
				if inst.opcode_br['sf'] == '0' and inst.opcode_br['N'] == '0':
					Rd = 'w'+str(int(inst.opcode_br['Rd'], base = 2))
					Rn = 'w'+str(int(inst.opcode_br['Rn'], base = 2))
					
					if inst.opcode_br['imms'] == '011111':
						inst.disassembly = 'SBFM {0}, {1}, #{2}, #63'.format(Rd, Rn, int(inst.opcode_br['immr'], base =2))
					else:
						inst.disassembly = 'ASR {0}, {1}, #{2}'.format(Rd, Rn, int(inst.opcode_br['immr'], base =2))	
				
				if inst.opcode_br['sf'] == '1' and inst.opcode_br['N'] == '1':
					Rd = 'x'+str(int(inst.opcode_br['Rd'], base = 2))
					Rn = 'x'+str(int(inst.opcode_br['Rn'], base = 2))
					
					if inst.opcode_br['imms'] == '111111': 
						inst.disassembly = 'SBFM {0}, {1}, #{2}, #63'.format(Rd, Rn, int(inst.opcode_br['immr'], base =2))
					else:
						inst.disassembly = 'ASR {0}, {1}, #{2}'.format(Rd, Rn, int(inst.opcode_br['immr'], base =2))	
				
				inst.operation = ASR_IMMEDIATE
				return inst		
			
			elif instructions[i] == 'MOV_SP':
				inst = instruction(opcode)
				inst.opcode_br['sf'] = opcode[31]
				inst.opcode_br['op'] = opcode[30]
				inst.opcode_br['S'] = opcode[29]
				inst.opcode_br['shift'] = opcode[22:24][::-1]
				inst.opcode_br['imm12'] = opcode[10:22][::-1]
				inst.opcode_br['Rn'] = opcode[5:10][::-1]
				inst.opcode_br['Rd'] = opcode[0:5][::-1]
				
				if inst.opcode_br['sf'] == '0':
					rd = int(inst.opcode_br['Rd'], base = 2)
					Rd = 'w'+str(rd) if rd < 31 else 'wsp'
					rn = int(inst.opcode_br['Rn'], base = 2)
					Rn = 'w'+str(rn) if rn < 31 else 'wsp'
				else:
					rd = int(inst.opcode_br['Rd'], base = 2)
					Rd = 'x'+str(rd) if rd < 31 else 'sp'
					rn = int(inst.opcode_br['Rn'], base = 2)
					Rn = 'x'+str(rn) if rn < 31 else 'sp'
				
				inst.opcode_br['Rn'] = Rn
				inst.opcode_br['Rd'] = Rd
				inst.disassembly = 'MOV {0}, {1}'.format(Rd, Rn)
				inst.operation = MOV_SP
				return inst		
			
			elif instructions[i] == 'MOV_inverted_wide_immediate' or\
				instructions[i] == 'MOV_wide_immediate':
				
				inst = instruction(opcode)
				inst.opcode_br['sf'] = opcode[31]
				inst.opcode_br['opc'] = opcode[29:31][::-1]
				inst.opcode_br['hw'] = opcode[21:23][::-1]
				inst.opcode_br['imm16'] = opcode[5:21][::-1]
				inst.opcode_br['Rd'] = opcode[0:5][::-1]
				
				if inst.opcode_br['sf'] == '0':
					rd = int(inst.opcode_br['Rd'], base = 2)
					Rd = 'w'+str(rd)
				else:
					rd = int(inst.opcode_br['Rd'], base = 2)
					Rd = 'x'+str(rd)
				imm = hex(int(inst.opcode_br['hw']+ inst.opcode_br['imm16'], base=2))
				inst.disassembly = 'MOV {0}, {1}'.format(Rd, imm)
				inst.operation = MOV_inverted_wide_immediate
				return inst
			elif instructions[i] == 'MOV_BITMASK_IMMEDIATE':
				if opcode[31] == '1':
					Rd = 'x' + str(int(opcode[0:5][::-1], base=2))
				else:
					Rd = 'w' + str(int(opcode[0:5][::-1], base=2))
				immr = opcode[16:22][::-1]
				imms = opcode[10:16][::-1]
				N = opcode[22]
				
				imm =N + imms + immr 
				inst = instruction(opcode)
				print "immediate value " , imm
				inst.disassembly = "MOV {0} # {1}".format(Rd, int(imm, base=2))
				inst.operation = MOV_BITMASK_IMMEDIATE_OP
				return inst
			
			
	print "Unindentified instruction"

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


def SUB_IMMEDIATE_OP(inst, context):
	operand2 = inst.opcode_br['imm']
	operand1 = ZeroExtend(bin(context.get_regval(inst.opcode_br['Rn']))[2:], len(operand2))
	
	operand2 = NOT(operand2)
	result, n, z, c, v = AddWithCarry(operand1, operand2, '1')
	context.set_regval(inst.opcode_br['Rd'], result)
	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)

def SUBS_IMMEDIATE_OP(inst, context):
	operand2 = inst.opcode_br['imm']
	operand1 = ZeroExtend(bin(context.get_regval(inst.opcode_br['Rn']))[2:], len(operand2))

	operand2 = NOT(operand2)
	result, n, z, c, v = AddWithCarry(operand1, operand2, '1')
	context.set_regval(inst.opcode_br['Rd'], result)
# setting flags as adds instruction
	context.flags['n'] = n
	context.flags['z'] = z
	context.flags['c'] = c
	context.flags['v'] = v


	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)
def AND_IMMEDIATE(inst, context):
	d = UInt(inst.opcode_br['Rd'])
	n = UInt(inst.opcode_br['Rn']);
	datasize = 64 if inst.opcode_br['sf'] == '1' else 32
	setflags = bool()
	
	op = -1
	opc = inst.opcode_br['opc']
	if opc == '00':
		op = 'LogicalOp_AND'
		setflags = False
	elif opc == '01':
		op = 'LogicalOp_ORR'
		setflags = False
	elif opc == '10':
		op = 'LogicalOp_EOR'
		setflags = False
	else:
		op = 'LogicalOp_AND'
		setflags = True
	
	imm = Zeros(datasize)
	imm, t = DecodeBitMasks(inst.opcode_br['N'], inst.opcode_br['imms'], inst.opcode_br['immr'], True, datasize)
	
	result = Zeros(datasize)
	operand1 = context.get_regval('x'+str(n))
	operand2 = imm
	if op == 'LogicalOp_AND':
		result = operand1 & int(operand2, base=2)
	elif op == 'LogicalOp_ORR':
		result = operand1 | int(operand2, base=2)
	else:
		result = operand1 ^ int(operand2, base=2)
	if setflags:
		context.flags['n'] = bin(result | 0x10000000000000000)[3:][0]
		context.flags['z'] = '1' if result == 0 else '0'
		context.flags['c'] = '0'
		context.flags['v'] = '0'
	
	if d == 31 and not setflags:
		context.set_regval('sp', result)
	else:
		context.set_regval('x'+str(d), result)

	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)
def ADR(inst, context):
	d = UInt(inst.opcode_br['Rd']);
	page = (inst.opcode_br['op'] == '1');
	imm = Zeros(64)
	immhi = inst.opcode_br['immhi']
	immlo = inst.opcode_br['immlo']
	
	if page:
		imm = SignExtend(immhi+immlo+Zeros(12), 64)
	else:
		imm = SignExtend(immhi+immlo, 64)
	
	base = ZeroExtend(bin(context.get_regval('pc'))[2:], 64)
	if page:
		base = base[::-1][12:][::-1]
		base = base+Zeros(12)
	
	r = int(base, base = 2) + int(imm, base = 2)
	context.set_regval('x'+str(d), r)
	
	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)
def ASR_IMMEDIATE(inst, context):
	print inst.opcode_br['imms']
	print inst.disassembly 
	d = UInt(inst.opcode_br['Rd'])
	n = UInt(inst.opcode_br['Rn'])
	datasize = 64 if inst.opcode_br['sf'] == '1' else 32
	inzero = bool()
	extend = bool();
	
	if inst.opcode_br['opc'] == '00':
		iszero = True
		extend = True
	elif  inst.opcode_br['opc'] == '00':
		iszero = False
		extend = False
	elif inst.opcode_br['opc'] == '00':
		iszero = True
		extend = False	
		
	R = UInt(inst.opcode_br['immr'])
	S = UInt(inst.opcode_br['imms'])
	wmask, tmask = DecodeBitMasks(inst.opcode_br['N'], inst.opcode_br['imms'], inst.opcode_br['immr'], False, datasize)
	
	dst = Zeros(datasize) if inzero else ZeroExtend(bin(context.get_regval('x'+str(d)))[2:], 64)
	src = ZeroExtend(bin(context.get_regval('x'+str(n)))[2:], 64)
	
	bot = ZeroExtend(bin((int(dst, base =2) & int(NOT(wmask), base =2)) | (int(ROR(src, R), base = 2) & int(wmask, base = 2)))[2:], 64)
	top = Replicate(src[::-1][S], 64) if extend else dst;
	
	context.set_regval( 'x'+str(d), (int(top, base = 2) & int(NOT(tmask), base =2)) | (int(bot, base = 2) & int(tmask, base = 2)))
	
	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)		

def MOV_SP(inst, context):
	AND_IMMEDIATE(inst, context)

def MOV_inverted_wide_immediate(inst, context):
	d = UInt(inst.opcode_br['Rd'])
	datasize = 64 if inst.opcode_br['sf'] == '1' else 32
	imm = inst.opcode_br['imm16']
	pos = -1
	opcode = -1
	
	if inst.opcode_br['opc'] == '00':
		opcode = 'MoveWideOp_N'
	elif inst.opcode_br['opc'] == '10':
		opcode = 'MoveWideOp_Z'
	elif inst.opcode_br['opc'] == '11':	
		opcode = 'MoveWideOp_K'
		
	pos = UInt(inst.opcode_br['hw']+'0000')
	
	result = Zeros(datasize)
	
	if opcode == 'MoveWideOp_K':
		result = ZeroExtend(bin(context.get_regval('x'+str(d)))[2:], 64)
	
	result = result[::-1]
	result = result[0:pos] + imm[::-1] + result[pos+16:]
	result = result[::-1]
	
	if opcode == 'MoveWideOp_N':
		result = NOT(result)
	
	context.set_regval('x'+str(d), int(result, base = 2))
	
	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)		

def MOV_BITMASK_IMMEDIATE_OP(inst , context):
	opcode = inst.opcode
	d = int(opcode[0:5][::-1] , base=2)
	n = int(opcode[5:10][::-1] , base=2)
	datasize = 64 if opcode[31] == '1' else 32 
	N = opcode[22]
	imms = opcode[10:16][::-1]
	immr = opcode[16:22][::-1]
	imm = DecodeBitMasks(N , imms, immr, True, datasize)
	print "val of n " , n
	operand1 = context.get_regval('x' + str(n))
	operand2 = int(imm, base=2)

	result = operand1 | operand2
	if d == 31:
		context.set_regval('sp', result)
	else:
		context.set_regval('x' + str(d) , result)
	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)		
	
