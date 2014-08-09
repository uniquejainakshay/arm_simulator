import argparse
from elftools.elf.elffile import ELFFile
from elftools.common.exceptions import ELFError

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
		print "Running in debug mode :  " , arguments.elf_file
	else: 
		print "Running : " , arguments.elf_file


# verifies if the file is an elf file and returns True, false otherwise
def check_if_elf_file(file_name):
	f = open(file_name, 'rb')
	try : 
		elf = ELFFile(f)
		return True
	except ELFError:
		return False
	


main()
