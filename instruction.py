class instruction():
	def __init__(self):
		self.opcode ='' 
		self.opcode_br = {} 
		self.operation = None


	def add_operation(self, func):
		self.operation = func

	def execute(self, execute
