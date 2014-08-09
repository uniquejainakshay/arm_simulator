# This translates the address in PC to an index of instruction in a pre-interpreted
# list of instructions in pipeline
class translator():
	def __init__(self):
		# stores mapping between the inst_address in the memory vs inst_index in pipeline 
		self.mapping = {}
	
	#returns the index of the instruction in the pipeline from the PC value
	def translate(pc_value):
		if not pc_value in self.mapping:
			print "Error: Translation of address \"{0}\" failed.\
			No mapping for interpreted instruction found.".format(pc_value)
		else:
			return self.mapping[pc_value]
		
	def create_mapping(self, mem_addr, index):
		self.mapping[mem_addr] = index
