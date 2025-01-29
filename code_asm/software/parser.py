import re

dictionnaire = {

#   REGISTER OPERATIONS
    "LSLS_RO":"00000",
    "LSRS_RO":"00001",
    "ASRS_RO":"00010",

#   ARITHMETIC OPERATIONS
    "ADDS_AOR":"0001100",
    "SUBS_AOR":"0001101",
    "ADDS_AOI":"0001110",
    "SUBS_AOI":"0001111",
    "MOVS":    "00100",
    "CMP_AO":  "00101",
    "ADDS":    "00110",
    "SUBS":    "00111",

#   DATA PROCESSING

    "ANDS_DP": "0100000000",
    "EORS_DP": "0100000001",
    "LSLS_DP": "0100000010",
    "LSRS_DP": "0100000011",
    "ASRS_DP": "0100000100",
    "ADCS_DP": "0100000101",
    "SBCS_DP": "0100000110",
    "RORS_DP": "0100000111",
    "TST_DP":  "0100001000",
    "RSBS_DP": "0100001001",
    "CMP_DP":  "0100001010",
    "CMN_DP":  "0100001011",
    "ORRS_DP": "0100001100",
    "MULS_DP": "0100001101",
    "BICS_DP": "0100001110",
    "MVNS_DP": "0100001111",

#   SP STORAGE
    "STR_ST":  "10010",
    "LDR_ST":  "10011",

#   SP SHIFT
    "ADD_SH":  "101100000",
    "SUB_SH":  "101100001",

#   CONDITIONAL BRANCH
    "BEQ":     "11010000",
    "BNE":     "11010001",
    "BCS":     "11010010",
    "BHS":     "11010010",
    "BCC":     "11010011",
    "BLO":     "11010011",
    "BMI":     "11010100",
    "BPL":     "11010101",
    "BVS":     "11010110",
    "BVC":     "11010111",
    "BHI":     "11011000",
    "BLS":     "11011001",
    "BGE":     "11011010",
    "BLT":     "11011011",
    "BLE":     "11011101",
    "BAL":     "11011110",

#   BRANCH
    "B":       "11100"

}

labels = {}

def split_instruction(inst):
    
    '''_summary_
    
    Split the instruction to get the separate components
    
    Args:
        inst (String): String of the instruction 

    Returns:
        List: List of every components of the instruction
    '''

    components = re.split(r'[\t, ]+', inst.strip())
    return [comp for comp in components if comp]

def is_a(data, type):
    
    '''_summary_

    Check if the first arg of data is equal to type
    
    Args:
        data (List): data to be tested
        type (String/Char): first char that define the type (# for an Immediate or R for a register)

    Returns:
        Boolean: return true if data is in the type asked, false otherwise
    '''
    
    data = data.strip()
    if(data[0] == type): return True
    return False

def shift_bit(binary, size):
    '''_summary_
    
    format the binary to fit with the given size by shifting the bit representation

    Args:
        binary (String): Binary representation that we want to shift
        size (int): size that the binary should reach

    Returns:
        String: return a representation of the binary encoded with "size" bits
    '''

    save = binary
    for _ in range(size - len(save)): save = "0" + save
    return save


def get_binary_from_register(register):
    '''_summary_
    
    Get the binary representation of the register number
    
    Args:
        register (String): The register that will be converted 

    Returns:
        String: return a binary representation of the register, encoded with 3 bits

    '''
    
    register = register.strip()
    register_binary = str(format(int(register[1]),"b"))

    if(len(register_binary) == 3): return register_binary

    return shift_bit(register_binary, 3)


def get_binary_from_immx(imm, size):
    '''_summary_

    Convert an immediate value to a binary representation with the specified size

    Args:
        imm (String): The immediate value that needs to be converted
        size (int): The size in bits that the binary representation should have

    Returns:
        String: Return a binary representation of the immediate value with the specified size
    '''
    
    imm = imm.strip("")
    imm_binary = str(format(int(imm[1:]),"b"))

    if(len(imm_binary) == size): return imm_binary

    return shift_bit(imm_binary,size)


def divide_immx(imm, divisor):
    '''_summary_

    Divide the immediate value by the given divisor and return the result as a string

    Args:
        imm (String): The immediate value to be divided
        diviser (int): The value by which the immediate value will be divided

    Returns:
        String: Return the result of the division as a string prefixed with "#"
    '''
    
    imm = imm.strip()
    return "#" + str(int(imm[1:])//divisor)


def get_data_processing_binary(inst):
    '''_summary_

    Generate the binary encoding for a data processing instruction

    Args:
        inst (List): List of components of the data processing instruction (e.g., opcode, registers, immediate values)

    Returns:
        String: Return the binary encoding for the given data processing instruction
    '''
    inst[0] += "_DP"
    return dictionnaire[inst[0]] + get_binary_from_register(inst[2]) + get_binary_from_register(inst[1])

def get_register_op_binary(inst):
    '''_summary_

    Generate the binary encoding for a register operation instruction

    Args:
        inst (List): List of components of the register operation instruction

    Returns:
        String: Return the binary encoding for the given register operation instruction
    '''
    inst[0] += "_RO"
    return dictionnaire[inst[0]] + get_binary_from_immx(inst[3],5) + get_binary_from_register(inst[2]) + get_binary_from_register(inst[1])


def get_arithmetic_operation_binary(inst):
    '''_summary_

    Generate the binary encoding for an arithmetic operation instruction (add, subtract, etc.)

    Args:
        inst (List): List of components of the arithmetic operation instruction

    Returns:
        String: Return the binary encoding for the given arithmetic operation instruction
    '''
    #check if there is 4 args
    if(len(inst) == 4):
        #check if the last arg is a register
        if(is_a(inst[3],"R")): 
            inst[0] += "_AOR"
            return dictionnaire[inst[0]] + get_binary_from_register(inst[3]) + get_binary_from_register(inst[2]) + get_binary_from_register(inst[1])
        else:
            #if its not a register then its a immediate 
            inst[0] += "_AOI"
            return dictionnaire[inst[0]] + get_binary_from_immx(inst[3],3) + get_binary_from_register(inst[2]) + get_binary_from_register(inst[1])
    else:
        return dictionnaire[inst[0]] + get_binary_from_register(inst[1]) + get_binary_from_immx(inst[2],8)

def get_sp_storage_binary(inst):
    '''_summary_

    Generate the binary encoding for a stack pointer storage instruction (e.g., STR, LDR)

    Args:
        inst (List): List of components of the stack pointer storage instruction

    Returns:
        String: Return the binary encoding for the given stack pointer storage instruction
    '''

    #We need to divide the immediate by 4 because the stack is composed with blocs of 4 bytes (32 bits)
    #By dividing the immediate we can evaluate how long is the jump of the stack pointer
    inst[0] += "_ST"

    if(len(inst) == 4):
        striped_inst = inst[3].strip()
        inst[3] = striped_inst[0:len(striped_inst) - 1]
        inst[3] = divide_immx(inst[3],4)
        return dictionnaire[inst[0]] + get_binary_from_register(inst[1]) + get_binary_from_immx(inst[3],8)
    else:
        return dictionnaire[inst[0]] + get_binary_from_register(inst[1]) + get_binary_from_immx("#0",8)

    

def get_sp_shift_binary(inst):
    '''_summary_

    Generate the binary encoding for a stack pointer shift instruction (e.g., ADD, SUB with SP)

    Args:
        inst (List): List of components of the stack pointer shift instruction

    Returns:
        String: Return the binary encoding for the given stack pointer shift instruction
    '''
    
    inst[0] += "_SH"
    inst[-1] = divide_immx(inst[-1],4)
    return dictionnaire[inst[0]] + get_binary_from_immx(inst[-1], 7)

def get_label_reference(label_name, pc, size_imm = 8):
    '''_summary_

    Get the binary representation of a label reference (used for branching)

    Args:
        label_name (String): The name of the label
        size_imm (int, optional): The size of the immediate value in bits. Defaults to 8.

    Returns:
        String: Return the binary representation of the label reference
    '''
    
    label_index = int(labels[label_name]) - pc - 3
    return two_complement(label_index, size_imm)

def get_branch_binary(inst, pc):
    '''_summary_

    Generate the binary encoding for a branch instruction (e.g., BEQ, BNE)

    Args:
        inst (List): List of components of the branch instruction

    Returns:
        String: Return the binary encoding for the given branch instruction
    '''
    
    if(len(inst[0]) == 1): return dictionnaire[inst[0]] + get_label_reference(inst[1], pc, 11)
    return dictionnaire[inst[0]] + get_label_reference(inst[1], pc)

def two_complement(integer, size):
    '''_summary_
    
    Convert a base 10 integer into a binary encoded with Two's complement
    
    Args:
        integer (int): number that we want to represent with Two's Complement
        size (int): number of bits that we use to code the Two's complement

    Return:
        String: Return the Two's Complement representation of the integer
    '''
    
    # get the absolute value of the integer    
    
    if(integer < 0): 
        integer *= -1
        binary = str(format(integer, "b"))
        binary = shift_bit(binary, size)

        # transform all the 0 in 1 and the 1 in 0
        reversed_binary = ""
        for index in range(len(binary)):
            if(binary[index] == "1"): reversed_binary += "0"
            else: reversed_binary += "1"

        binary = int(reversed_binary, 2) + 1
        if(binary >= 2**size): return str(format(binary, "b"))[-size:]
        return str(format(binary, "b"))
    else:
        return shift_bit(str(format(integer, "b")),size)

def convert_assembly_to_bin(inst, pc):
    '''_summary_

    Translate an assembly instruction into its binary representation

    Args:
        inst (List): List of components of the assembly instruction

    Returns:
        String: Return the binary encoding for the given instruction
    '''
    
    match inst[0]:

        case "LSLS":
            if(len(inst) == 4):
                binary = get_register_op_binary(inst)
            else:
                binary = get_data_processing_binary(inst)
        
        case "LSRS":
            if(len(inst) == 4):
                binary = get_register_op_binary(inst)
            else:
                binary = get_data_processing_binary(inst) 
            
        case "ASRS":
            if(len(inst) == 4):
                binary = get_register_op_binary(inst)
            else:
                binary = get_data_processing_binary(inst)
        
        case "ADDS":
            binary = get_arithmetic_operation_binary(inst)
        
        case "SUBS":
            binary = get_arithmetic_operation_binary(inst)
        
        case "MOVS":
            binary = get_arithmetic_operation_binary(inst)
        
        case "CMP":
            if(is_a(inst[1],"#")):
                binary = get_arithmetic_operation_binary(inst)
            else:
                binary = get_data_processing_binary(inst)
        
        case "ANDS":
            binary = get_data_processing_binary(inst)
        
        case "EORS":
            binary = get_data_processing_binary(inst)
        
        case "ADCS":
            binary = get_data_processing_binary(inst)
            
        case "SBCS":
            binary = get_data_processing_binary(inst)
            
        case "RORS":
            binary = get_data_processing_binary(inst)
            
        case "TST":
            binary = get_data_processing_binary(inst)
        
        case "RSBS":
            binary = get_data_processing_binary(inst)
        
        case "CMN":
            binary = get_data_processing_binary(inst)
        
        case "ORRS":
            binary = get_data_processing_binary(inst)
            
        case "MULS":
            binary = get_data_processing_binary(inst)
            
        case "BICS":
            binary = get_data_processing_binary(inst)
        
        case "MVNS":
            binary = get_data_processing_binary(inst)

#       LOAD/STORE

        case "STR":
            binary = get_sp_storage_binary(inst)

        case "LDR":
            binary = get_sp_storage_binary(inst)

#       MISCELLANEOUS

        case "ADD":
            binary = get_sp_shift_binary(inst)

        case "SUB":
            binary = get_sp_shift_binary(inst)
        
#       BRANCH

        case "BEQ":
            binary = get_branch_binary(inst, pc) 

        case "BNE":
            binary = get_branch_binary(inst, pc) 

        case "BCS":
            binary = get_branch_binary(inst, pc) 

        case "BCC":
            binary = get_branch_binary(inst, pc) 

        case "BMI":
            binary = get_branch_binary(inst, pc) 

        case "BPL":
            binary = get_branch_binary(inst, pc) 

        case "BVS":
            binary = get_branch_binary(inst, pc) 

        case "BHI":
            binary = get_branch_binary(inst, pc) 

        case "BLS":
            binary = get_branch_binary(inst, pc) 

        case "BGE":
            binary = get_branch_binary(inst, pc) 

        case "BLT":
            binary = get_branch_binary(inst, pc) 

        case "BLE":
            binary = get_branch_binary(inst, pc) 

        case "BAL":
            binary = get_branch_binary(inst, pc)
        
        case "B":
            binary = get_branch_binary(inst, pc)

        case _: 
            return "NONE"
    return binary
        
def sanitize_input(input):
    '''_summary_

    Clean up input by stripping leading and trailing spaces and filtering empty entries

    Args:
        input (List): List of strings to be sanitized

    Returns:
        List: Return a list of non-empty and sanitized instruction strings
    '''
    
    return [inst for inst in input if inst.strip()]



def convert_binary_to_hex(binary):
    '''_summary_

    Convert a binary string to its hexadecimal representation

    Args:
        binary (String): The binary string to be converted

    Returns:
        String: Return the hexadecimal representation of the given binary string
    '''
    
    hexa = hex(int(binary,2))[2:]
    if(len(hexa) == 4): return hexa
    return shift_bit(hexa,4)

def convert_assembly_to_hex(file_name):
    '''_summary_
    
    Read an assembly file and write, in hexadecimal, the non empty or non comments lines into a file

    Args:
        file_name (Path/String): Path of the assembly file
        
    Returns:
        void
    '''
    
    hexadecimals = []           # Hexadecimals values that will be written in the file
    filtered_instructions = []   # Formated instructions
    PC = 0                      # Program Counter

    try:
        with open(file_name, 'r') as fichier:
            instructions = fichier.read().splitlines()
            # Filter empty elements
            instructions = [line for line in instructions if line.strip()]

        # init the label and sanitize all the instructions
        for inst in instructions:
            inst = sanitize_input(split_instruction(inst.upper()))
            if not inst or inst[0].startswith(';') or inst[0].startswith('#') or inst[0].startswith('@'):       # Remove non usefull line
                continue
            elif (inst[0].startswith('.') or inst[0].endswith(':')): 
                labels[inst[0][0:len(inst[0])-1]] = PC         # Adding the new label with the program counter value in the label dictionnary
                continue
            PC += 1
            filtered_instructions.append(inst)

        PC = 0
        for filtered_inst in filtered_instructions:
            filtered_inst = convert_assembly_to_bin(filtered_inst, PC) # Get the binary representation of the instruction
            if(filtered_inst == "NONE"): 
                hexadecimals.append("XXXX")
                PC += 1
                continue
            PC += 1
            hexadecimals.append(convert_binary_to_hex(filtered_inst)) # Convert the binary representation in hexadecimal and add it to the list
 
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{file_name}' n'existe pas.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    
    return hexadecimals

def write_file(hexadecimals, file_name = './output.bin'):
    '''_summary_
        Write the content of hexadecimals in a .bin file
        
        Args:
            hexadecimals (List): List of hexadecimals
            file_name (Path/String): Path to the output file
            
        Returns:
            void
    '''
    
    with open(file_name, 'w') as file:
        file.write('v2.0 raw\n')
        for hexa in hexadecimals:
            file.write(hexa + ' ')


file_name = str(input("Enter file path: "))

write_file(convert_assembly_to_hex(file_name))
