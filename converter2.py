import pandas as pd
import sys

# Assign spreadsheet filename to `file`
file = 'truth_table.xlsx'

# Load spreadsheet
xl = pd.ExcelFile(file)

# Load a sheet into a DataFrame by name: df1
df = xl.parse('Sheet1')

PCSel = {4 : "0", "ALU" : "1"}
ImmSel = {"I" : "000", "S" : "001", "B" : "010", "U" : "011", "J" : "100"}
# RegWEn = {"Read" : "0", "Write" : "1"}
ASel = {"Reg" : "0", "PC" : "1"}
BSel = {"Reg" : "0", "Imm" : "1"}
ALUSel = {"add": "0000", "and" : "0001", "or" : "0010", "xor" : "0011", "srl" : "0100", "sra" : "0101", "sll" : "0110", "slt" : "0111", "divu" : "1000", "remu" : "1001", "mul" : "1010", "mulhu" : "1011", "sub" : "1100", "bsel" : "1101", "mulh" : "1110"}
MemRW = {"Read" : "0", "Write" : "1"}
MCSel = {0 : "00", 1: "01", 2 : "10"}
WBSel = {"Mem" : "00", "ALU" : "01", "PC+4" : "10"}

"""
for index, row in df.iterrows():
  	print(row["instruction"])

for name, values in df.iteritems():
    print('{name}: {value}'.format(name=name, value=values[0]))
"""

def convert_opcode(inst):
	bit_code = "0b000"
	address_bit = "0b"
	lst_addr = [address_bit]
	for index, row in df.iterrows():
		if row["instruction"] == inst:
			# Calculateing address
			if row["BrLT"] == "*":
				bit_list = ['0', '1']
				for i in range(len(lst_addr)):
					address_bit_so_far = lst_addr[i]
					for appending_bits in bit_list:
						lst_addr.append(address_bit_so_far + appending_bits)
			else:
				for i in range(len(lst_addr)):
					lst_addr[i] += str(int(row["BrLT"]))

			i = 0
			while i < len(lst_addr):
				if len(lst_addr[i]) != 3:
					lst_addr.pop(i)
				else:
					i += 1

			if row["BrEq"] == "*":
				bit_list = ['0', '1']
				for i in range(len(lst_addr)):
					address_bit_so_far = lst_addr[i]
					for appending_bits in bit_list:
						lst_addr.append(address_bit_so_far + appending_bits)
			else:
				for i in range(len(lst_addr)):
					lst_addr[i] += str(int(row["BrEq"]))

			i = 0
			while i < len(lst_addr):
				if len(lst_addr[i]) != 4:
					lst_addr.pop(i)
				else:
					i += 1


			if row["funct7"] == "*":
				print("You need to fill out the value to several places because func7 can be anything.")
				bit_list = ['00', '01', '10', '11']
				for i in range(len(lst_addr)):
					address_bit_so_far = lst_addr[i]
					for appending_bits in bit_list:
						lst_addr.append(address_bit_so_far + appending_bits)
			else:
				for i in range(len(lst_addr)):
					lst_addr[i] += str(row["funct7"][1:len(row["funct7"])-1])

			i = 0
			while i < len(lst_addr):
				if len(lst_addr[i]) != 6:
					lst_addr.pop(i)
				else:
					i += 1

			if row["funct3"] == "*":
				print("You need to fill out the value to several places because func3 can be anything.")
				bit_list = ['000', '001', '010', '011', '100', '101', '110', '111']

				for i in range(len(lst_addr)):
					address_bit_so_far = lst_addr[i]
					for appending_bits in bit_list:
						lst_addr.append(address_bit_so_far + appending_bits)
			else:
				for i in range(len(lst_addr)):
					lst_addr[i] = lst_addr[i] + str(row["funct3"][1:len(row["funct3"])-1])

			j = 0
			while j < len(lst_addr):
				if len(lst_addr[j]) != 9:
					lst_addr.pop(j)
				else:
					j += 1
			
			for i in range(len(lst_addr)):
				lst_addr[i] = lst_addr[i] + str(row["opcode"][1:len(row["opcode"])-1])


			# Calculating a bit value
			bit_code += PCSel[row["PCSel"]]
			
			if row["ImmSel"] == "*":
				bit_code += "000"
			else:
				bit_code += ImmSel[row["ImmSel"]]

			bit_code += str(int(row["RegWEn"]))

			if row["BrUn"] == "*":
				bit_code += "0"
			else:
				bit_code += str(int(row["BrUn"]))

			bit_code += ASel[row["ASel"]]
			bit_code += BSel[row["BSel"]]
			bit_code += ALUSel[row["ALUSel"]]
			bit_code += MemRW[row["MemRW"]]

			if row["MCSel"] == "*":
				bit_code += "10"
			else:
				bit_code += MCSel[row["MCSel"]]

			if row["WBSel"] == "*":
				bit_code += "00"
			else:
				bit_code += WBSel[row["WBSel"]]

			return bit_code, lst_addr



if __name__ == '__main__':
	command_list = [
				"add", 
				"mul", 
				"sub", 
				"sll", 
				"mulh", 
				"mulhu", 
				"slt", 
				"xor", 
				"divu", 
				"srl", 
				"or", 
				"remu", 
				"and", 
				"lb", 
				"lh", 
				"lw", 
				"addi", 
				"slli", 
				"slti", 
				"xori",
				"srli", 
				"srai", 
				"ori", 
				"andi",
				"sw",
				"beq_true",
				"beq_false", 
				"blt_true", 
				"blt_false",
				"bltu_true",
				"bltu_false", 
				"bne_true",
				"bne_false",
				"lui",
				"jal", 
				"jalr"
				]

	num_of_addresses = 0
	for command in command_list:
		msg, lst_address = convert_opcode(command)
		num_of_addresses += len(lst_address)

	saver = ['0' for _ in range(4096)]
	for command in command_list:
		msg, lst_address = convert_opcode(command)
		hex_msg = str(hex(int(msg, 2)))[2:]
		lst_address = [int(addr, 2) for addr in lst_address]
		for i in lst_address:
			if saver[i] != '0':
				raise Exception
			saver[i] = hex_msg
	
	pivot = saver[0]
	result = []
	pivot = 1
	prev = saver[0]

	for el in saver:
		if el != prev:
			if pivot > 3:
				result.append("{}*{}".format(pivot, prev))
			else:
				if prev == '0':
					for j in range(pivot):
						result.append('0')
				else:
					result.append(prev)
			prev = el
			pivot = 1
		else:
			pivot += 1

	for i in range(len(result)):
		print(result[i], end=' ')
    	

	# if msg != None:
	# 	print('=================================================')
	# 	print("Code for " + sys.argv[1] + " is...")
	# 	for addr in lst_address:
	# 		print("Address in binary: " + addr)
	# 		print("Address in hex: " + hex(int(addr, 2)))
	# 	print('\n')
	# 	print("binary: " + msg)
	# 	print("hex: " + hex(int(msg, 2)))
	# 	print('=================================================\n')
	# else:
	# 	print("There is no instruction called " + sys.argv[1] + " in RISC-V.")
	#C00293 C00313 530463 C00393 400393 730463 1800413 C00493
