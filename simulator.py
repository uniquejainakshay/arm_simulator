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
from debug import *

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

# When in debug mode
#	1. Load the the elf file and wait
#	2. Implement following commands
#		break <line_no>
#		list
#		run
#		del
#		help ( show help for all the commands supported ) 
#		print <x/d> reg  ( print individual registers in decimal or hex) 
#		print <no><b/w/d> <x/d> <mem_location>

#	Need to maintain a list for the break points indices in sorted order. Translator must raise an exception when the breakpointed instruction is being translated.

# registers module will maintain the list of watched registers 



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
	while True:

		
		##  Start the execution of the instructions from _start
#		break <line_no>
#		watch <reg_name>
#		list
#		run
#		del
#		help ( show help for all the commands supported ) 
		if debug:
			print "(debug)",
			cmd = read_and_parse_debug_command()
			if cmd[0] == 'help':
				print "break <line_no>"
				print "list"
				print "run"
				print "del <line_no> "
				print "help "
				print "print <x/d> reg "
				print 's'
				print 'c'
				print "quit"
				
				continue
			elif cmd[0] == 'break':
				try: 
					line_no = int(cmd[1])
				#	print translator.mapping.values()
					if line_no not in translator.mapping.values():
						print "Invalid line number. Use list command to get proper line no."
						continue
					if line_no not in translator.break_points:
						translator.break_points += [line_no]
					msg = "Break points at lines: "
					for i in translator.break_points:
						msg += str(i) + ', '
					print msg[:-1]
				except Exception as exp: 
					print "Error parsing the line number " 
				continue
			elif cmd[0] == 'list':
				count  = 0
				for i in pipeline.inst_list:
					print count , ':\t',i.get_opcode_hex(), i.disassembly
					count += 1
				continue

			elif cmd[0] == 'run':
				pc = context.get_regval('pc')
				if pc not in translator.mapping.keys():
					context.set_regval('pc', _start)
					print "Restarting execution from _start  =", _start
				elif pc == _start:
					print "Starting execution from memory location ", _start
				else:
					print "Program already running. Press c to continue execution."
					continue
			elif cmd[0] == 'del':
				try: 
					line_no = int(cmd[1])
					if line_no not in translator.mapping.values():
						print "Invalid line number. Use list command to get proper line no."
						continue
					translator.break_points.remove(line_no)
					msg = "Break points at : "
					for i in translator.break_points:
						msg += str(i) + ', '
					print msg[:-2]
				except Exception as exp: 
					print "Error parsing the line number " 
				continue
			elif cmd[0] == 'print':
				if cmd[1] == 'all':
					context.print_hex()
					continue
				if len(cmd) < 3:
					print "Too few arguments for print command"
					continue
				if not (cmd[1] == 'x' or cmd[1] == 'd'):
					if not (cmd[1][-1] == 'b' or cmd[1][-1] == 'w'or cmd[1][-1] == 'd'):
						print "Invalid 2nd argument for print command "
						continue
					else:
						if len(cmd) < 4:
							print "Too few arugments for printing memory "
							continue
						print_memory(cmd)
						continue
				else:
					if len(cmd) < 3 :
						print "Too few arguments for print command "
						continue
					if cmd[1] == 'x':
						print cmd[2] , " : " , hex(context.get_regval(cmd[2]))
					else:
						print cmd[2] , " : " , context.get_regval(cmd[2])
					continue
			elif cmd[0] == 'quit':
				exit()
		
			elif cmd[0] == 's':
				try:
					pc = context.get_regval('pc')
					index= translator.translate(pc)
					inst = pipeline.fetch(index)
					print "Step : " , index,' ' , inst.disassembly
					inst.execute(context)
				except text_end_exception as e:
					print "Program exited " 
					continue
				except break_point_exception as e:
					index = e.inst_index	
					inst = pipeline.fetch(index)
					print "Step : " , index,' ' , inst.disassembly
					inst.execute(context)
				continue
			elif cmd[0] == 'c':
				print "Continuing execution till next break point "


			else:
				print "Unrecognised command. Try help."
				continue

				
		while True:
			try:
				pc = context.get_regval('pc')
				index= translator.translate(pc)
				if index == -1:
					break 
				inst = pipeline.fetch(index)
				inst.execute(context)
			except break_point_exception as e:
				# debug level code 
				print "Break point at : "
				index = e.inst_index
				inst = pipeline.fetch(index)
				print index , ':\t',inst.get_opcode_hex(), inst.disassembly
				inst.execute(context)
				break
			except text_end_exception as e:
				print "Program exited"
				break


		if not debug :
			break

def read_and_parse_debug_command():
	cmd  = raw_input()
	cmd = cmd.split(' ')
	while '' in cmd:
		cmd.remove('')
	return cmd


#		print <no><b/w/d> <x/d> <mem_location>
def print_memory(cmd):
	no = int(cmd[1][:-1])
	size = str(cmd[1])[-1]
	base = cmd[2]
	location = int(cmd[3])
	print "Memory contents"
	try:
		for i in range(no):
			if base == 'x':
				if size == 'b':
					print location,': ' , memory[location].encode('hex')
					location += 1
				elif size == 'w':
					print location,': ', memory[location].encode('hex'), ' ' , memory[location +1].encode('hex')
					location += 2
				elif size == 'd':
					print location,': ',  memory[location].encode('hex'), ' ' , memory[location +1].encode('hex'), ' ' , memory[location + 2].encode('hex'), ' ' , memory[location + 3].encode('hex')
					location += 4
			elif base == 'd':
				if size == 'b':
					print location,': ' , int(memory[location].encode('hex'), base=16)
					location += 1
				elif size == 'w':
					print location,': ', int(memory[location].encode('hex'), base=16), ' ' , int(memory[location +1].encode('hex'), base=16)
					location += 2
				elif size == 'd':
					print location,': ',  int(memory[location].encode('hex'), base=16), ' ' , int(memory[location +1].encode('hex'), base=16), ' ' , int(memory[location + 2].encode('hex'), base=16), ' ' , int(memory[location + 3].encode('hex'), base=16)
					location += 4
				

	except KeyError:
		print "Invalid memory location accessed : ", location



	

main()
