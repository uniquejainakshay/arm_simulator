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
from common_functions import *

##################   Instructions 
instructions = [
#0
'ADD_EXTENDED_REGISTER' , 
#1
'ADD_SHIFTED_REGISTER', 
#2
'ADDS_EXTENDED_REGISTER',
#3
'ADDS_SHIFTED_REGISTER',
#4
'SUB_EXTENDED_REGISTER' , 
#5
'SUB_SHIFTED_REGISTER', 
#6
'SUBS_EXTENDED_REGISTER',
#7
'SUBS_SHIFTED_REGISTER', 
#8
'AND_SHIFTED_REGISTER',
#9
'ANDS_SHIFTED_REGISTER',
#10
'ASR_REGISTER',
#11
'MOV_register',
]


####### 	Instruction mask

inst_mask = [
#0
'00000000000000000000011111111110', 
#1
'00000000000000000000010011111110', 
#2
'00000000000000000000011111111110', 
#3
'00000000000000000000010011111110', 
#4
'00000000000000000000011111111110', 
#5
'00000000000000000000010011111110', 
#6
'00000000000000000000011111111110', 
#7
'00000000000000000000010011111110', 
#8
'00000000000000000000010011111110', 
#9
'00000000000000000000010011111110', 
#10
'00000000001111110000011111111110', 
#11
'00000000000000000000010011111110',

]


#######		Inst identifier

inst_identifier = [
#0
'00000000000000000000010011010000',
#1
'00000000000000000000000011010000' ,
#2
'00000000000000000000010011010100',
#3 
'00000000000000000000000011010100', 
#4
'00000000000000000000010011010010',
#5
'00000000000000000000000011010010' ,
#6
'00000000000000000000010011010110',
#7 
'00000000000000000000000011010110' ,
#8 
'00000000000000000000000001010000' ,
#9 
'00000000000000000000000001010110' ,
#10
'00000000000101000000001101011000', 
#11
'00000000000000000000000001010100'
]

def interpret(opcode):

	for i in range(len(inst_mask)):
		masked_opcode = int(opcode, base=2) & int(inst_mask[i], base =2)
		if masked_opcode == int(inst_identifier[i], base=2):



			if instructions[i] == 'ADD_EXTENDED_REGISTER' or\
				instructions[i] == 'ADDS_EXTENDED_REGISTER' or\
				instructions[i] == 'SUB_EXTENDED_REGISTER' or\
				instructions[i] == 'SUBS_EXTENDED_REGISTER':
				# ADD_EXTENDED_REGISTER || ADDS_EXTENDED_REGISTER
				# sub_EXTENDED_REGISTER || subS_EXTENDED_REGISTER
				inst = instruction(opcode)
				inst.opcode_br['sf'] = opcode[31]
				opc_sf = opcode[31]
				inst.opcode_br['option'] = opcode[13:16][::-1]
				inst.opcode_br['imm3'] = opcode[10:13][::-1]
				opc_Rn = opcode[5:10][::-1]
				opc_Rd = opcode[0:5][::-1]
				opc_Rm= opcode[16:21][::-1]

				d = int( opc_Rd , base=2)
				n = int( opc_Rn , base=2)
				m = int( opc_Rm , base=2)
				# Destination is always X[] in all the cases 
				if(d == 31):
					Rd = 'sp'
				else:
					Rd = 'x' + str(d)
				if opc_sf == '1':
					# 64 bit execution
					if n == 31:
						Rn = 'sp'
					else:
						Rn = 'x' + str(n)
				else:
					# 32 bit execution

					if(n == 31):
						Rn = 'wsp'
					else:
						Rn = 'w' + str(n)


				option = int(inst.opcode_br['option'], base=2)
				if option %4 == 3:
					Rm = 'x' + str(m)
				else:
					Rm = 'w' + str(m)
				inst.opcode_br['Rm'] = Rm
				inst.opcode_br['Rn'] = Rn
				inst.opcode_br['Rd'] = Rd
				extend_type = DecodeRegExtend(inst.opcode_br['option'])
				extend_type = extend_type.split('_')[1]

				if instructions[i] == 'ADD_EXTENDED_REGISTER':
					inst.operation = ADD_EXTENDED_REGISTER_OP
					inst.disassembly = 'ADD {0}, {1}, {2} {3} {4}'.format(Rd, Rn, Rm, ', ' + extend_type, int(inst.opcode_br['imm3'] , base=2 ))
				elif instructions[i] == 'ADDS_EXTENDED_REGISTER':
					inst.operation = ADDS_EXTENDED_REGISTER_OP
					inst.disassembly = 'ADDS {0}, {1}, {2} {3} {4}'.format(Rd, Rn, Rm, ', ' + extend_type, int(inst.opcode_br['imm3'] , base=2 ))
				elif instructions[i] == 'SUB_EXTENDED_REGISTER':
					inst.operation = SUB_EXTENDED_REGISTER_OP
					inst.disassembly = 'SUB {0}, {1}, {2} {3} {4}'.format(Rd, Rn, Rm, ', ' + extend_type, int(inst.opcode_br['imm3'] , base=2 ))
				elif instructions[i] == 'SUBS_EXTENDED_REGISTER':
					inst.operation = SUBS_EXTENDED_REGISTER_OP
					inst.disassembly = 'SUBS {0}, {1}, {2} {3} {4}'.format(Rd, Rn, Rm, ', ' + extend_type, int(inst.opcode_br['imm3'] , base=2 ))
				return inst


			elif instructions[i] == 'ADD_SHIFTED_REGISTER' or\
				instructions[i] == 'ADDS_SHIFTED_REGISTER' or\
				instructions[i] == 'SUB_SHIFTED_REGISTER' or\
				instructions[i] == 'SUBS_SHIFTED_REGISTER':
				# ADD_SHIFTED_REGISTER || ADDS_SHIFTED_REGISTER
				# sub_SHIFTED_REGISTER || sub_SHIFTED_REGISTER
				inst = instruction(opcode)
				opc_Rd = opcode[0:5][::-1]
				opc_Rn = opcode[5:10][::-1]
				opc_Rm = opcode[16:21][::-1]
				inst.opcode_br['imm6'] = opcode[10:16][::-1]
				inst.opcode_br['shift']= opcode[22:24][::-1]
				opc_shift= opcode[22:24][::-1]
				opc_sf = opcode[31]
				inst.opcode_br['sf'] = opcode[31]

				d = int( opc_Rd , base=2)
				n = int( opc_Rn , base=2)
				m = int( opc_Rm , base=2)
			


				Rd = 'x' + str(d)
				if opc_sf == '1':
					# 64 bit execution
					Rn = 'x' + str(n)
					Rm = 'x' + str(m)
				else:
					# 32 bit execution
					Rn = 'w' + str(n)
					Rm = 'w' + str(m)

				if int(opc_shift, base=2) == 0:
					shift = 'LSL'
				elif int(opc_shift, base=2) == 1:
					shift = 'LSR'
				else :
					shift = 'ASR'

				amount = int(opcode[10:16][::-1], base=2)
				inst.opcode_br['Rd'] = Rd
				inst.opcode_br['Rn'] = Rn
				inst.opcode_br['Rm'] = Rm

				if instructions[i] == 'ADD_SHIFTED_REGISTER':
					inst.operation = ADD_SHIFTED_REGISTER_OP
					inst.disassembly = 'ADD {0}, {1}, {2}, {3} #{4}'.format(Rd, Rn, Rm, shift, amount)
				elif instructions[i] == 'ADDS_SHIFTED_REGISTER':
					inst.operation = ADDS_SHIFTED_REGISTER_OP
					inst.disassembly = 'ADDS {0}, {1}, {2}, {3} #{4}'.format(Rd, Rn, Rm, shift, amount)
				elif instructions[i] == 'SUB_SHIFTED_REGISTER':
					inst.operation = SUB_SHIFTED_REGISTER_OP
					inst.disassembly = 'SUB {0}, {1}, {2}, {3} #{4}'.format(Rd, Rn, Rm, shift, amount)
				elif instructions[i] == 'SUBS_SHIFTED_REGISTER':
					inst.operation = SUBS_SHIFTED_REGISTER_OP
					inst.disassembly = 'SUBS {0}, {1}, {2}, {3} #{4}'.format(Rd, Rn, Rm, shift, amount)
			elif instructions[i] == 'ANDS_SHIFTED_REGISTER' or\
				instructions[i] == 'AND_SHIFTED_REGISTER':
				d = int(opcode[0:5][::-1], base=2)
				n = int(opcode[5:10][::-1], base=2)
				m = int(opcode[16:21][::-1], base=2)
				sf = opcode[31]
				opc = opcode[29:31][::-1]
				shift = opcode[22:24][::-1]
				imm6= opcode[10:16][::-1]
				inst = instruction(opcode)
	
				# for sf = 0/1 the operation is always on X 
				inst.opcode_br['Rd'] = 'x' + str(d)
				inst.opcode_br['Rn'] = 'x' + str(n)
				inst.opcode_br['Rm'] = 'x' + str(m)
				if sf == '1':
					# 64 bit execution
					Rn = 'x' + str(n)
					Rm = 'x' + str(m)
					Rd = 'x' + str(d)
				else:
					# 32 bit execution
					Rn = 'w' + str(n)
					Rm = 'w' + str(m)
					Rd = 'w' + str(d)

				if instructions[i] == 'AND_SHIFTED_REGISTER':
					inst.disassembly = "AND {0}, {1}, {2}, {3} #{4}".format(Rd, Rn, Rm,\
					DecodeShift(shift).split('_')[1], int(imm6, base=2))
				else:
					inst.disassembly = "ANDS {0}, {1}, {2}, {3} #{4}".format(Rd, Rn, Rm,\
					DecodeShift(shift).split('_')[1], int(imm6, base=2))

				inst.operation = AND_SHIFTED_REGISTER_OP
				return inst
			elif instructions[i] == 'ASR_REGISTER':

				d = int(opcode[0:5][::-1], base=2)
				n = int(opcode[5:10][::-1], base=2)
				m = int(opcode[16:21][::-1], base=2)


				inst = instruction(opcode)
				if opcode[31] == '1':
					inst.disassembly = "ASRV {0}, {1}, {2}".format('x' + str(d), 'x' + str(n) , 'x' + str(n))
				else:
					inst.disassembly = 'ASRV {0}, {1}, {2}'.format('w' + str(d), 'w' + str(n) , 'w' + str(n))

				inst.operation = ASR_REGISTER_OP

				return inst
			elif instructions[i] == 'MOV_register':
				inst = instruction(opcode)
				inst.opcode_br['sf'] = opcode[31]
				inst.opcode_br['Rm'] = opcode[16:21][::-1]
				inst.opcode_br['Rd'] = opcode[0:5][::-1]
				
				Rm = int(inst.opcode_br['Rm'], base = 2)
				Rd = int(inst.opcode_br['Rd'], base = 2)
				
				if inst.opcode_br['sf'] == '0':
					rd = int(inst.opcode_br['Rd'], base = 2)
					Rd = 'w'+str(rd)
					rm = int(inst.opcode_br['Rm'], base = 2)
					Rm = 'w'+str(rm)
				else:
					rd = int(inst.opcode_br['Rd'], base = 2)
					Rd = 'x'+str(rd)
					rm = int(inst.opcode_br['Rm'], base = 2)
					Rm = 'x'+str(rm)
				
				inst.opcode_br['Rm'] = Rm
				inst.opcode_br['Rd'] = Rd
				
				inst.disassembly = 'MOV {0}, {1}'.format(Rd, Rm)
				inst.operation = MOV_register
				return inst
			else:
				print "Unidentified"


			return inst






def ADD_EXTENDED_REGISTER_OP(inst, context):
	datasize   = 64 if inst.opcode_br['sf'] == '1' else 32;
	extend_type = DecodeRegExtend(inst.opcode_br['option']);
	shift = UInt(inst.opcode_br['imm3']);
	if shift > 4 :
		print "Shift amount cannot be greater than 4 : {0}".format(inst.disassembly)
		exit()

	#bits(datasize) result;
	# both operands are 64 bit 
	operand1 =bin( context.get_regval(inst.opcode_br['Rn']) )
	operand1 = operand1[2:]
	operand1 = ZeroExtend(operand1, 64)
	#print "shift ", shift

	operand2 = ExtendReg(inst.opcode_br['Rm'], extend_type, shift, context);
	result, n,z,c,v = AddWithCarry(operand1, operand2, '0');
	context.set_regval(inst.opcode_br['Rd'], result)


	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)
			

def ADDS_EXTENDED_REGISTER_OP(inst, context):
	datasize   = 64 if inst.opcode_br['sf'] == '1' else 32;
	extend_type = DecodeRegExtend(inst.opcode_br['option']);
	shift = UInt(inst.opcode_br['imm3']);
	if shift > 4 :
		print "Shift amount cannot be greater than 4 : {0}".format(inst.disassembly)
		exit()

	#bits(datasize) result;
	# both operands are 64 bit 
	operand1 =bin( context.get_regval(inst.opcode_br['Rn']) )
	operand1 = operand1[2:]
	operand1 = ZeroExtend(operand1, 64)
	operand2 = ExtendReg(inst.opcode_br['Rm'], extend_type, shift, context);
	result, n,z,c,v = AddWithCarry(operand1, operand2, '0');
	context.set_regval(inst.opcode_br['Rd'], result)
	
	# setting the flags as it is adds instruction
	context.flags['n'] = n
	context.flags['z'] = z
	context.flags['c'] = c
	context.flags['v'] = v


	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)

def ADD_SHIFTED_REGISTER_OP(inst, context):
	datasize = 64 if inst.opcode_br['sf']== '1' else 32
	sub_op = False
	setflags = False
	shift_type = DecodeShift(inst.opcode_br['shift'])
	shift_amount = UInt(inst.opcode_br['imm6'])
	operand1 = bin (context.get_regval(inst.opcode_br['Rn']))[2:]
	operand1 = ZeroExtend(operand1, 64)
	operand2 = ShiftReg(context.get_regval(inst.opcode_br['Rm']), shift_type, shift_amount)
	result , n, z, c, v = AddWithCarry(operand1, operand2, '0')

	# here we need to set the x register
	reg_no = inst.opcode_br['Rd'][1:]
	#print "result " , result, " reg no " , reg_no
	context.set_regval('x' + reg_no, result)
	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)


def ADDS_SHIFTED_REGISTER_OP(inst, context):
	datasize = 64 if inst.opcode_br['sf']== '1' else 32
	sub_op = False
	setflags = False
	shift_type = DecodeShift(inst.opcode_br['shift'])
	shift_amount = UInt(inst.opcode_br['imm6'])
	operand1 = bin (context.get_regval(inst.opcode_br['Rn']))[2:]
	operand1 = ZeroExtend(operand1, 64)
	operand2 = ShiftReg(context.get_regval(inst.opcode_br['Rm']), shift_type, shift_amount)
	result , n, z, c, v = AddWithCarry(operand1, operand2, '0')

	# here we need to set the x register
	reg_no = inst.opcode_br['Rd'][1:]
	#print "result " , result, " reg no " , reg_no
	context.set_regval('x' + reg_no, result)
# setting the flags as it is adds instruction
	context.flags['n'] = n
	context.flags['z'] = z
	context.flags['c'] = c
	context.flags['v'] = v
	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)


def SUB_EXTENDED_REGISTER_OP(inst, context):
	datasize   = 64 if inst.opcode_br['sf'] == '1' else 32;
	extend_type = DecodeRegExtend(inst.opcode_br['option']);
	shift = UInt(inst.opcode_br['imm3']);
	if shift > 4 :
		print "Shift amount cannot be greater than 4 : {0}".format(inst.disassembly)
		exit()

	#bits(datasize) result;
	# both operands are 64 bit 
	operand1 =bin( context.get_regval(inst.opcode_br['Rn']) )
	operand1 = operand1[2:]
	operand1 = ZeroExtend(operand1, 64)
	#print "shift ", shift

	operand2 = ExtendReg(inst.opcode_br['Rm'], extend_type, shift, context);
	operand2 = NOT(operand2)
	result, n,z,c,v = AddWithCarry(operand1, operand2, '1');
	context.set_regval(inst.opcode_br['Rd'], result)


	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)
			

def SUBS_EXTENDED_REGISTER_OP(inst, context):
	datasize   = 64 if inst.opcode_br['sf'] == '1' else 32;
	extend_type = DecodeRegExtend(inst.opcode_br['option']);
	shift = UInt(inst.opcode_br['imm3']);
	if shift > 4 :
		print "Shift amount cannot be greater than 4 : {0}".format(inst.disassembly)
		exit()

	#bits(datasize) result;
	# both operands are 64 bit 
	operand1 =bin( context.get_regval(inst.opcode_br['Rn']) )
	operand1 = operand1[2:]
	operand1 = ZeroExtend(operand1, 64)
	operand2 = ExtendReg(inst.opcode_br['Rm'], extend_type, shift, context);
	operand2 = NOT(operand2)
	result, n,z,c,v = AddWithCarry(operand1, operand2, '1');
	context.set_regval(inst.opcode_br['Rd'], result)
	
	# setting the flags as it is adds instruction
	context.flags['n'] = n
	context.flags['z'] = z
	context.flags['c'] = c
	context.flags['v'] = v


	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)

def SUB_SHIFTED_REGISTER_OP(inst, context):
	datasize = 64 if inst.opcode_br['sf']== '1' else 32
	sub_op = False
	setflags = False
	shift_type = DecodeShift(inst.opcode_br['shift'])
	shift_amount = UInt(inst.opcode_br['imm6'])
	operand1 = bin (context.get_regval(inst.opcode_br['Rn']))[2:]
	operand1 = ZeroExtend(operand1, 64)
	operand2 = ShiftReg(context.get_regval(inst.opcode_br['Rm']), shift_type, shift_amount)
	operand2 = NOT(operand2)
	result , n, z, c, v = AddWithCarry(operand1, operand2, '1')

	# here we need to set the x register
	reg_no = inst.opcode_br['Rd'][1:]
	#print "result " , result, " reg no " , reg_no
	context.set_regval('x' + reg_no, result)
	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)


def SUBS_SHIFTED_REGISTER_OP(inst, context):
	datasize = 64 if inst.opcode_br['sf']== '1' else 32
	sub_op = False
	setflags = False
	shift_type = DecodeShift(inst.opcode_br['shift'])
	shift_amount = UInt(inst.opcode_br['imm6'])
	operand1 = bin (context.get_regval(inst.opcode_br['Rn']))[2:]
	operand1 = ZeroExtend(operand1, 64)
	operand2 = ShiftReg(context.get_regval(inst.opcode_br['Rm']), shift_type, shift_amount)
	operand2 = NOT(operand2)
	result , n, z, c, v = AddWithCarry(operand1, operand2, '1')

	# here we need to set the x register
	reg_no = inst.opcode_br['Rd'][1:]
	#print "result " , result, " reg no " , reg_no
	context.set_regval('x' + reg_no, result)
	# setting the flags as it is adds instruction
	context.flags['n'] = n
	context.flags['z'] = z
	context.flags['c'] = c
	context.flags['v'] = v
	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)

def AND_SHIFTED_REGISTER_OP(inst, context):
	sf = inst.opcode[31]
	opc =inst.opcode[29:31][::-1]
	shift = inst.opcode[22:24][::-1]
	imm6= inst.opcode[10:16][::-1]
	datasize = 64 if sf == '1' else 32
	setflags = True if opc == '11' else False
	shift_type = DecodeShift(shift);
	shift_amount = UInt(imm6);


	operand1 = context.get_regval(inst.opcode_br['Rn'])
	operand2 = ShiftReg(context.get_regval(inst.opcode_br['Rm']), shift_type, shift_amount)
	result = operand1 & int(operand2, base=2)
	context.set_regval(inst.opcode_br['Rd'], result)
	if setflags:
		context.flags['n'] = bin(result | 0x10000000000000000)[2:][0]
		context.flags['z'] = '1' if result == 0 else '0' 
		context.flags['c'] ='0' 
		context.flags['v'] = '0'

	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)
def ASR_REGISTER_OP(inst, context):
	d = int(inst.opcode[0:5][::-1], base=2)
	n = int(inst.opcode[5:10][::-1], base=2)
	m = int(inst.opcode[16:21][::-1], base=2)
	datasize = 64 if inst.opcode[31] == '1' else 32;
	op2 = inst.opcode[10:12][::-1]
	shift_type = DecodeShift(op2);

	operand2 = context.get_regval('x' + str(m))
	operand2 %= datasize
	result = ShiftReg(context.get_regval('x' + str(n)), shift_type, operand2)
	result = int(result, base=2)
	context.set_regval('x' + str(d), result)
	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)


def MOV_register(inst, context):	
	context.set_regval( inst.opcode_br['Rd'],context.get_regval(inst.opcode_br['Rm']))
	pc = context.get_regval('pc')
	pc += 4
	context.set_regval('pc', pc)		
