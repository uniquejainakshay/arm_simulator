# This class is as good as a list data structure with some restrictions. 
# A pipeline must be instanciated at the start of each simulation.
# Pipeline holds the instruction found in the text section sequentially
# The program control can fetch required instruction by translating the 
#	memory address in PC reg using translator class and fetch the required index. 

from instruction import instruction
class pipeline():
	def __init__(self):
		# list that contains the instructions
		self.inst_list = []	

	# enqueue the instruction in the list
	def enqueue(inst):
		if not isinstance(inst, instruction):
			print "Error : Object \"{0}\" cannot be enqueued in the pipeline".format(type(inst))
			exit()
		self.inst_list += [inst]


	#fetch the instruction at the said index from the list
	def fetch(inst_no):
		if inst_no not in range(len(self.inst_list)):
			print "Fetching instruction number : {0} failed.\
			Instruction out of bounds (0, {1})".format(inst_no, len(self.inst_list))
			exit()

		else:
			return self.inst_list[inst_no]
