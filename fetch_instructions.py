#!/usr/bin/python 
from elftools.elf.elffile import ELFFile

#This reads the text section of elf file. 
#Divides the section into 4Bytes chunks where each chunk is a 64 bit instruction
#returns the no of instructions read and the list of binary encoded string instruction bytes 

inst_class_identifier = []
def get_instructions(elfFileObj):
	data = elfFileObj.get_section_by_name(".text").data()
	#hex_data = data.encode('b')
	hex_data = data
	no_bytes = len(hex_data)
	inst_list = []
	for i in range(no_bytes / 4):
		hex_val = hex_data[i*4 : i*4 + 4].encode('hex')
		# Be wise, check for 'endian'ness and return accordingly 
		if elfFileObj.little_endian:
			instruction = bits(hex_val[6:]) + bits(hex_val[4:6]) + bits(hex_val[2:4]) + bits(hex_val[:2])
		else:
			instruction = bits(hex_val[:2]) + bits(hex_val[2:4]) + bits(hex_val[4:6]) + bits(hex_val[6:])

# with space between each byte 
	#	print bits(hex_val[6:]) + " " + bits(hex_val[4:6]) + " " + bits(hex_val[2:4]) + " " + bits(hex_val[:2])
		inst_list  = inst_list + [instruction[::-1]]

	return no_bytes / 4 , inst_list

def bits(byte):
	no = bin(0x100 | int('0x' + byte, base=16))
	return no[3:]





#code for testing this module 


#f = open('objdump', 'rb')
#no, inst_list = get_instructions(ELFFile(f))
#print "The instructions are " 
#for i in range(no):
	#print i, " : " , inst_list[i]
