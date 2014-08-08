#	Instruction class

# Each 4 Byte instruction is read and stored in an object of the class below
#It has the following fields 
# Opcode : stores the opcode read from the elf file 
# Opcode_br : stores the opcode break up of the instruction as specified in the manual 
# operation : The function to be called when the instructions execute method is called. 
# disassembly : Instruction disassembled back to its Assembly Language code 



class instruction():
	#Default constructor 
	def __init__(self, opcode):
		
		# stores the opcode fetched from the elf file 
		self.opcode =opcode

		# stores the breakage of the opcode in the dictionary for future use while execution
		self.opcode_br = {} 

		# The function to be called when the instruction needs to be executed 
		self.operation = None

		# Assembly language equivalent of the opcode
		self.disassembly = ''
		# may be some additional fields like location, may be added later 

	# Set the function to be called when the instruction is executed
	def add_operation(self, func):
		self.operation = func

	# Execute the instruction 
	def execute(self, execute, context):
		self.operation(context)
