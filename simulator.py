#!/usr/bin/python 
import argparse
from elftools.elf.elffile import ELFFile
from elftools.common.exceptions import ELFError
from translator import Translator
from pipeline import Pipeline
from identify_instruction_class import identify_class
import branch_excepgen_syst_instructions
import data_processing_immediate
import data_processing_register
import load_store_instructions
from registers import Context

######			Globals Section

context = Context() 	# Register context
memory = dict() 	# Memory : To be set by shashank  
_start = -1 		# The location in program counter from where we start the execution
stack_start = pow(2,33)
stack_size  = 50
_text_start = -1
translator = Translator()
pipeline = Pipeline()

inst_class_code_mapping = ['Unallocated', 'Data processing - Immediate ' , 'Branch, exception generation and system instructions', 'Loads and stores', ' Data processing - register', ' Data processing - SIMD and floating point' , ' Data processing - SIMD and floating point']

######			Main Function
def main():
	# Argument parser
	parser = argparse.ArgumentParser(description='ARMv8 Simulator')
	parser.add_argument('elf_file', help='The elf file to run by the ARM simulator')
	parser.add_argument('--debug' , help='Run in debug mode', action='store_true')
	arguments = parser.parse_args()
	
	# check if the file specified is an elf file 
	if not check_if_elf_file(arguments.elf_file):
		print "File specified is not an elf file " 
		exit()

	# Run in normal mode or debugging mode 		
	if arguments.debug : 
		run( arguments.elf_file, debug = True)
	else: 
		run( arguments.elf_file)


# verifies if the file is an elf file and returns True, false otherwise
def check_if_elf_file(file_name):
	f = open(file_name, 'rb')
	try : 
		elf = ELFFile(f)
		f.close()
		return True
	except ELFError:
		f.close()
		return False
	
def run(elf_file , debug = False):
	global memory
	global _start
	global _text_len
	global stack_start
	global stack_size
	global _text_start, translation, pipeline

	# read the elf file 
	# load the memory from the elf file, get _start and _text_start addresses
	f = open(elf_file, 'rb')
	elf_handle = ELFFile(f)
	for i in elf_handle.iter_sections():
			image_sections = [".bss", ".data", ".data1", ".rodata", ".rodata1", ".text"]
			if i.__dict__['header']['sh_flags'] == 2 or image_sections.__contains__(i.__dict__['name']):
				sh_addr 	= i.__dict__['header']['sh_addr']
				sh_size 	= i.__dict__['header']['sh_size']
				sh_addralign 	= i.__dict__['header']['sh_addralign']
				
							
				if i.__dict__['name'] == ".text":
					_text_len = sh_size
					_text_start = sh_addr
				
				offset = 0
				# Load the section in the memory  image 
				while offset < sh_size:
					if i.__dict__['name'] == '.bss':
						memory[sh_addr+offset] = '\x00'
					else:
						memory[sh_addr+offset] = i.data()[offset]
					offset += 1
				
				# Section alignment : Insert dummy bytes when the section is not aligned 
				if sh_size % sh_addralign != 0:
					for j in range((sh_addralign) - (sh_size % sh_addralign)):
						# skipping to insert the dummy byte if this section is overlapping with other section
						if not memory.__contains__(sh_addr+offset):
							memory[sh_addr+offset] = '\x00'
							offset += 1
				
			# read the _start symbol from the symbol table
			if i.__dict__['name'] == ".symtab":
				for j in i.iter_symbols():
					if j.__dict__['name'] == "_start":
						_start = j.__dict__['entry']['st_value']
	

	# setting up stack at the end of the memory image
	
	#getting the last allocated mem location
	mem_end = sorted(memory.keys())[-1]
	for i in range(mem_end + 1, mem_end + stack_size + 1):
		memory[i] = '\x00'
	stack_start = mem_end + 1


	# fetch instructions from the .text section till length of the section
		# add each instruction to the pipeline 
		# add translation of that instruction to the translator

	for addr in range(_text_start , _text_start + _text_len, 4):
		if elf_handle.little_endian:
			byte_4 = memory[addr+3] + memory[addr+2] + memory[addr+1] + memory[addr]
		else:
			byte_4 =  memory[addr] + memory[addr+1]  +  memory[addr+2]+ memory[addr+3] 
			
		opcode = bin(int ( byte_4.encode('hex') , base=16) | int ('0x100000000', base=16))[3:]
		#reversing the opcode string 
		opcode = opcode[::-1]
		#print "{0} : {1}, Class : {2}".format(addr, opcode,inst_class_code_mapping[identify_class(opcode)])
		clas = identify_class(opcode)
		if clas == 0:
			# Unallocated class : Skip  and go to next instruction 
			continue
		elif clas ==1:
			# Data processing - Immediate 
			inst = data_processing_immediate.interpret(opcode)
		elif clas ==2:
			# Branch, exception generation and system instructions 
			inst = branch_excepgen_syst_instructions.interpret(opcode)
		elif clas ==3:
			# Loads and stores 
			inst = load_store_instructions.interpret(opcode)
		elif clas ==4:
			# Data processing - register 
			inst = data_processing_register.interpret(opcode)
		elif clas ==5 or clas ==6:
			# Data processing - SIMD and Floating point  
			print "Data processing - SIMD and Floating point Class instructions are not part of the assignment"
			exit()

		index = pipeline.get_len()
		pipeline.enqueue(inst)
		translator.create_mapping(addr, index)




	# set the PC to _start location and begin execution ( make provisions for debug )
	context.set_regval('sp', stack_start)
	context.set_regval('pc', _start)

	
	##  Start the execution of the instructions from _start

	while True:
		pc = context.get_regval('pc')
		index = translator.translate(pc)
		if index == -1:
			break 
		inst = pipeline.fetch(index)
		inst.execute(context)
		if debug : 
			print inst.disassembly

	if debug:
		context.print_hex()

	

main()
