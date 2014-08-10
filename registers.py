
# 		context class : This class simulates the registers of ARM processor
#The class simulates following registers : 
# General purpose registers 32bit registers w0 to w31 
# General purpose registers 64bit registers x0 to x31 
# Registers PC SP


class Context():
	def __init__(self):
		self.regs = ['w0',  'w1',  'w2',  'w3',  'w4',  'w5',  'w6',  'w7',  'w8',  'w9',  'w10',
		'w11',  'w12',  'w13',  'w14',  'w15',  'w16',  'w17',  'w18',  'w19',  'w20',
		'w21',  'w22',  'w23',  'w24',  'w25',  'w26',  'w27',  'w28',  'w29',  'w30',
		'x0',  'x1',  'x2',  'x3',  'x4',  'x5',  'x6',  'x7',  'x8',  'x9',  'x10',
		'x11',  'x12',  'x13',  'x14',  'x15',  'x16',  'x17',  'x18',  'x19',  'x20',
		'x21',  'x22',  'x23',  'x24',  'x25',  'x26',  'x27',  'x28',  'x29',  'x30',
		'pc', 'sp', 'wsp']

		self.val = [
		0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
		0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
		0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ,
		0 , 0 , 0 , 0 , 0 , 0, 0, 0]

		self.flags = {'n':0 , 'z':0 , 'c':0, 'v':0}
	
	#returns the content of the register, specified in the argument 	
	def get_regval(self, reg_name):
		reg_name  = reg_name.lower()

		# Check if register being accessed is valid 
		if not reg_name in self.regs:
			print "Undefined register access tried : " , reg_name
			exit()

		# We need to be careful when gen purpos(GP) register is accessed, 
		# Also ensure that any new register added passes this if-else ladder check 
		if reg_name[0] == 'w':
			return self.val[self.regs.index(reg_name)]
		elif reg_name[0] == 'x':
			#user intends to use GP register in 64 bit width size
			reg_no = reg_name[1:]
			lower_32_val = self.val[self.regs.index('w' + reg_no)]
			higher_32_val  = self.val[self.regs.index(reg_name)]
			final_val = higher_32_val * pow(2, 32) + lower_32_val
			return final_val
		elif reg_name == 'sp':
			lower_32_val = self.val[self.regs.index('wsp')]
			higher_32_val = self.val[self.regs.index('sp')]
			return higher_32_val * pow(2, 32) + lower_32_val
		else:
			return self.val[self.regs.index(reg_name)]



	def set_regval(self, reg_name, value):
		reg_name  = reg_name.lower()

		# Check if register being set is valid 
		if not reg_name in self.regs:
			print "Undefined register modification tried : " , reg_name
			exit()

		# We need to be careful when gen purpos(GP) register is accessed, 
		# Also ensure that any new register added passes this if-else ladder check 
		if reg_name[0] == 'w':
			if value > pow(2, 32) -1:
				print "register capacity exceeded. reg : {0} , capacity : {1}, value : {3}".format(reg_name, 
					'32 bits' , value)
				exit()
			self.val[self.regs.index(reg_name)] = value
			return
		elif reg_name[0] == 'x':
			#user intends to use GP register in 64 bit width size
			if value > pow(2, 64) -1:
				print "register capacity exceeded. reg : {0} , capacity : {1}, value : {3}".format(reg_name, 
				'64 bits' , value)
				exit()

			reg_no = reg_name[1:]
			lower_32_val = value % pow(2,  32)
			higher_32_val  = value / pow(2, 32)
			# setting the values 
			self.val[self.regs.index(reg_name)] = higher_32_val
			self.val[self.regs.index('w'+reg_no)] = lower_32_val
			return

		# 64 bit SP access, 32 bit gets covered in the else part 
		elif reg_name == 'sp':
			lower_32_val = value % pow(2, 32)
			higher_32_val = value / pow(2, 32)
			self.val[self.regs.index(reg_name)] = higher_32_val
			self.val[self.regs.index('wsp')] = lower_32_val
		else:
			self.val[self.regs.index(reg_name)] = value
		return 
	def print_dec(self):
		no_regs = len(self.regs)
		for j in range((no_regs / 5) + 1):
			print "-----------------------------------------------------------------------------------"
			lb = j*5
			if (j + 1 )*5 >  no_regs:
				ub = no_regs
			else:
				ub = (j + 1) * 5
			#print "lb = {0}, ub = {1}".format(lb, ub)
			for i in range(lb, ub):
				print self.regs[i], "\t\t", 
			print '\n'
			for i in range(lb, ub):
				reg = self.regs[i]
				value = self.get_regval(reg)
				print value, "\t\t", 
			print '\n'
			#print "-----------------------------------------------------------------------------------"


	def print_hex(self):
		no_regs = len(self.regs)
		for j in range((no_regs / 5) + 1):
			print "-----------------------------------------------------------------------------------"
			lb = j*5
			if (j + 1 )*5 >  no_regs:
				ub = no_regs
			else:
				ub = (j + 1) * 5
			#print "lb = {0}, ub = {1}".format(lb, ub)
			for i in range(lb, ub):
				print self.regs[i], "\t\t", 
			print '\n'
			for i in range(lb, ub):
				reg = self.regs[i]
				value = self.get_regval(reg)
				print hex(value)[2:], "\t\t", 
					#print hex(self.get_reg(self.regs[i]))[2:], "\t\t", 
					#print "this is str : " , i
			print '\n'
			#print "-----------------------------------------------------------------------------------"


##  Code for testing registes class 
#cont = Context()
#cont.set_regval('w0',2) 
#cont.set_regval('pc', int('abcdabcdabcdabcd', base=16))
#cont.print_hex()
