def UInt(x):
	# x is N bit binary string with MSB at 0 index, with no 0b prefix.
	result = 0
	x = x[::-1]
	for i in range(len(x)):
		if x[i] == '1':
			result = result + pow(2,i)
	return result

def SInt(x):
	# x is N bit binary string with MSB at 0 index, with no 0b prefix.
	result = 0
	x = x[::-1]
	for i in range(len(x)):
		if x[i] == '1':
			result = result + pow(2,i)
	if x[len(x)-1] == '1':
		result = result - pow(2,len(x)-1);
	return result;

def AddWithCarry(x, y, carry_in):
	# x is N bit binary string with MSB at 0 index, with no 0b prefix.
	# y is N bit binary string with MSB at 0 index, with no 0b prefix.
	# carry_in is 1 bit binary string with MSB at 0 index, with no 0b prefix.
	
	N = len(x)
	unsigned_sum = UInt(x) + UInt(y) + UInt(carry_in);
	signed_sum = SInt(x) + SInt(y) + UInt(carry_in);
	result = int(bin(unsigned_sum)[2:][::-1][0:N][::-1], base = 2)
	n = ZeroExtend(bin(result)[2:], N)[::-1][N-1]
	z = '1' if result == 0 else '0'
	c = '0' if UInt(bin(result)[2:]) == unsigned_sum else '1';
	v = '0' if SInt(bin(result)[2:]) == signed_sum else '1';
	return result, n, z, c, v;


ShiftType = ['ShiftType_LSL' ,'ShiftType_LSR' ,'ShiftType_ASR' ,'ShiftType_ROR' ]

def DecodeShift(op):
	if op == '00':
		return 'ShiftType_LSL'
	elif op == '01':
		return 'ShiftType_LSR'
	elif op == '10':
		return 'ShiftType_ASR'
	else:
		return 'ShiftType_ROR'
	
def Zeros(n):
	p = ''
	for i in range(n):
		p += '0' 
	return p

#  return 64 bit only 

def ShiftReg(oprand, shift_type, shift_amount):
	if shift_type == 'ShiftType_LSL':
		op = bin(oprand)[2:]
		op += Zeros(shift_amount)
		return ZeroExtend(op, 64)
	elif shift_type == 'ShiftType_LSR':
		op = bin(oprand)[2:]
		op = op[0:-shift_amount]
		op = ZeroExtend(op, 64)
		return op
	elif shift_type == 'ShiftType_ASR':
		oprand = bin(oprand)[2:]
		extended_x = SignExtend(oprand, shift_amount  +64);
		#print extended_x
		result = extended_x[0:-shift_amount]
		if shift_amount == 0 :
			return extended_x
		return result
	else:
		op = bin(oprand)[2:]
		op = ZeroExtend(op, 64)
		for i in range(shift_amount):
			op = op[-1] + op[0:-2]
		return op

ExtendType = ['ExtendType_UXTB', 'ExtendType_UXTH', 'ExtendType_UXTW', 'ExtendType_UXTX', 'ExtendType_SXTB', 'ExtendType_SXTH', 'ExtendType_SXTW', 'ExtendType_SXTX']

def DecodeRegExtend(op):
	# op in 3 bit binary string with MSB at 0 index, with no 0b prefix. 
	global ExtendType
	return 	ExtendType[int(op, base = 2)]

def ExtendReg(m, extend_type, shift, context):
	# m is extended register name, e.g. x1, x2
	# extend_type is one of the member in ExtendType
	# shift is python interger
	# context is set of registers
	global ExtendType
	assert shift >= 0 , "shift is less than 0"
	assert shift <= 4 , "shift is greater than 4"
	val = ZeroExtend(bin(context.get_regval(m))[2:], 64)
	N = len(val)
	
	v = [[True, 8], [True, 16], [True, 32], [True, 64], [False, 8], [False, 16], [False, 32], [False, 64]]
	i = ExtendType.index(extend_type)
	unsigned, len_= v[i][0], v[i][1]
	len_ = min(len_, N - shift)
	
	return Extend(val[::-1][0:len_ ][::-1] + Zeros(shift), N, unsigned);
	
	
def NOT(x):
	# x is N bit binary string with MSB at 0 index, with no 0b prefix.
	a = ""
	for i in x:
		if i == '0':
			a = a + '1'
		else:
			a = a + '0'	
	return a		

def Extend(x, N, unsigned):
	# x is M bit binary string with MSB at 0 index, with no 0b prefix.
	# N is python integer
	# unsigned is boolean
	
	return ZeroExtend(x, N) if unsigned else SignExtend(x, N);

def HighestSetBit(x):
	# x is N bit binary string with MSB at 0 index, with no 0b prefix.
	x = x[::-1]
	N = len(x)
	for i in range(N-1, -1,  -1):
		if x[i] == '1':
			return i;
	return -1;
	
	
	
	
#print int(ShiftReg(45, 'ShiftType_LSR', 3), base=2)
#print int(ShiftReg(45, 'ShiftType_LSL', 3), base=2)
#print int(ShiftReg(4, 'ShiftType_LSL', 3), base=2)

LogicalOp = ['LogicalOp_AND', 'LogicalOp_EOR', 'LogicalOp_ORR']
MoveWideOp = ['MoveWideOp_N', 'MoveWideOp_Z', 'MoveWideOp_K']


def Ones(N):
	s = ""
	for i in range(N):
		s += '1'
	return s

def Replicate(b, N):
	# b is N bit binary string with MSB at 0 index, with no 0b prefix.
	# returns b bits replicated across N bit register.
	b = int(b, base = 2)
	b = bin(b)[2:]
	l = len(b)
	b = int(b, base = 2)
	
	j = 0
	for i in range(N/l):
		j = j | b
		b = b << l
			
	return ZeroExtend(bin(j)[2:], N)

def SignExtend( x,  N):
	# x is M bit binary string with MSB at 0 index, with no 0b prefix.
	# N is python integer
	M = len(x)
	b = x[::-1][M-1]
	for i in range(N-M):
		x = b + x
	return x;

def ZeroExtend(x, N):
	# x is M bit binary string with MSB at 0 index, with no 0b prefix.
	# N is python integer
	M = len(x)
	return Zeros(N-M)+x	


def DecodeBitMasks(immN, imms, immr, immediate, datasize):
	# immN is 1 bit binary string with MSB at 0 index, with no 0b prefix.
	# imms is 6 bit binary string with MSB at 0 index, with no 0b prefix.	
	# immr is 6 bit binary string with MSB at 0 index, with no 0b prefix.		
	# immediate is boolean variable
	len_ = HighestSetBit(immN+NOT(imms))
	if len_ < 1:
		print "HighestSetBit returned -1."
		exit()
	levels = ZeroExtend(Ones(len_), 6)
	
	S = UInt(ZeroExtend( bin( int(imms, base = 2)&int(levels, base = 2) )[2:], 6))
	R = UInt(ZeroExtend( bin( int(immr, base = 2)&int(levels, base = 2) )[2:], 6))
	diff = ZeroExtend(bin(S-R)[2:], 6)
	
	esize = 1 << len_
	d = UInt(diff)
	welem = ZeroExtend(Ones(S + 1), esize)
	telem = ZeroExtend(Ones(d + 1), esize)
	wmask = Replicate(ROR(welem, R), datasize)
	tmask = Replicate(telem, datasize)
	return wmask, tmask


def ROR(op, amount):
	for i in range(amount):
		op =op[-1] +  op[0:-1] 
	return op
