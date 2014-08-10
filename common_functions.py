def ZeroExtend(x,N):
	# x is M bit binary string with MSB at 0 index, with no 0b prefix.
	# Goal: Make width of x = N bits
	M = len(x)
	p = ""
	for i in range(N-M):
		p = p+'0'
		
	return p+x;
				

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
