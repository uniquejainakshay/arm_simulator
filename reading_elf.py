#!/usr/bin/python 
from elftools.elf.elffile import ELFFile
from fetch_instructions import get_instructions
from identify_instruction_class import identify_class
import disassemble_data_processing_register 
import sys
import codecs

inst_class_code_mapping = ['Unallocated', 'Data processing - Immediate ' , 'Branch, exception generation and system instructions', 'Loads and stores', ' Data processing - register', ' Data processing - SIMD and floating point' , ' Data processing - SIMD and floating point']




def main():
	if len(sys.argv) < 2: 
		print "ELF file expected as argument" 
		exit()
	f = open(sys.argv[1], 'rb')
	elf_handle = ELFFile(f)

	no, inst_list = get_instructions(elf_handle)
	print "The instructions are " 
	for i in range(no):
		class_code = identify_class(inst_list[i])
		if(i == -1):
			cl = "Unidentified " 
		else:
			if class_code == 4:
				disassemble_data_processing_register.interpret(inst_list[i])
			cl = inst_class_code_mapping[class_code]
		print i, " : " , inst_list[i], " Class : ", cl

	#print "Stream" , elf_handle.stream
	#print "elf class " , elf_handle.elfclass
	#print "little endian " , elf_handle.little_endian
	#print "header " , elf_handle.header
	#print "e ident raw " , elf_handle.e_ident_raw

	#print elf_handle.iter_sections()
#	n = elf_handle.num_sections()
#	print "sections in the elf file are : " 
#	for i in range(n):
#		print elf_handle.get_section(i) 



#	n = elf_handle.num_segments()
#	print "segments in the elf file are : " 
#	for i in range(n):
#		print elf_handle.get_segment(i) 


main()




