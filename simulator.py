#!/usr/bin/python 
import argparse
from elftools.elf.elffile import ELFFile
from elftools.common.exceptions import ELFError

######			Globals Section

context = None # Register context
memory  = None # Memory : To be set by shashank  
_start = None  # The location in program counter from where we start the execution


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
		run(debug = True, arguments.elf_file)
	else: 
		run(arguments.elf_file)


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
	
def run(debug, elf_file):
	# read the elf file 
	# load the memory from the elf file, get _start and .text addresses
	# fetch instructions from the .text section till length of the section
		# add each instruction to the pipeline 
		# add translation of that instruction to the translator
	# set the PC to _start location and begin execution ( make provisions for debug )
	

main()
