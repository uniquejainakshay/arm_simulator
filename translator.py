# This translates the address in PC to an index of instruction in a pre-interpreted
# list of instructions in pipeline
class Translator():
	def __init__(self):
		# stores mapping between the inst_address in the memory vs inst_index in pipeline 
		self.mapping = {}
	
	#returns the index of the instruction in the pipeline from the PC value
	def translate(self, pc_value):
		if pc_value == 4 + max(self.mapping.keys()):
			print "Execution Successful " 
			return -1
		if not pc_value in self.mapping:
			print "Error: Translation of address \"{0}\" failed.\
			No mapping for interpreted instruction found.".format(pc_value)
			exit()
		else:
			return self.mapping[pc_value]
		
	def create_mapping(self, mem_addr, index):
		self.mapping[mem_addr] = index
