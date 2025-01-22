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
    "BCC":     "11010011",
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


def splitInstruction(inst):
    
    '''_summary_
    
    Split the instruction to get the separate components
    
    Args:
        inst (String): String of the instruction 

    Returns:
        List: List of every components of the instruction
    '''
    
    splitedInstruction = inst.split(' ', 1)
    if(len(splitedInstruction) > 1):  
        instruction = splitedInstruction[0].strip()
        arguments = [arg.strip() for arg in splitedInstruction[1].split(',')]
        return [instruction] + arguments
    return splitedInstruction

def isA(data, type):
    
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

def shiftBit(binary, size):
    '''_summary_
    
    format the binary to fit with the given size by shifting the bit representation

    Args:
        binary (String): Binary representation that we want to shift
        size (int): size that the binary should reach

    Returns:
        String: return a representation of the binary encoded with "size" bits
    '''

    save = binary
    for i in range(size - len(save)): save = "0" + save
    return save


def getBinaryFromRegister(register):
    '''_summary_
    
    Get the binary representation of the register number
    
    Args:
        register (String): The register that will be converted 

    Returns:
        String: return a binary representation of the register, encoded with 3 bits

    '''
    
    register = register.strip()
    registerBinary = str(format(int(register[1]),"b"))

    if(len(registerBinary) == 3): return registerBinary

    return shiftBit(registerBinary, 3)


def getBinaryFromImmX(imm, size):
    '''_summary_

    Convert an immediate value to a binary representation with the specified size

    Args:
        imm (String): The immediate value that needs to be converted
        size (int): The size in bits that the binary representation should have

    Returns:
        String: Return a binary representation of the immediate value with the specified size
    '''
    
    imm = imm.strip("")
    immBinary = str(format(int(imm[1:]),"b"))

    if(len(immBinary) == size): return immBinary

    return shiftBit(immBinary,size)


def divideImmX(imm, divisor):
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


def getDataProcessingBinary(inst):
    '''_summary_

    Generate the binary encoding for a data processing instruction

    Args:
        inst (List): List of components of the data processing instruction (e.g., opcode, registers, immediate values)

    Returns:
        String: Return the binary encoding for the given data processing instruction
    '''
    inst[0] += "_DP"
    return dictionnaire[inst[0]] + getBinaryFromRegister(inst[2]) + getBinaryFromRegister(inst[1])

def getRegisterOpBinary(inst):
    '''_summary_

    Generate the binary encoding for a register operation instruction

    Args:
        inst (List): List of components of the register operation instruction

    Returns:
        String: Return the binary encoding for the given register operation instruction
    '''
    inst[0] += "_RO"
    return dictionnaire[inst[0]] + getBinaryFromImmX(inst[3],5) + getBinaryFromRegister(inst[2]) + getBinaryFromRegister(inst[1])


def getArithmeticOperationBinary(inst):
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
        if(isA(inst[3],"R")): 
            inst[0] += "_AOR"
            return dictionnaire[inst[0]] + getBinaryFromRegister(inst[3]) + getBinaryFromRegister(inst[2]) + getBinaryFromRegister(inst[1])
        else:
            #if its not a register then its a immediate 
            inst[0] += "_AOI"
            return dictionnaire[inst[0]] + getBinaryFromImmX(inst[3],3) + getBinaryFromRegister(inst[2]) + getBinaryFromRegister(inst[1])
    else:
        return dictionnaire[inst[0]] + getBinaryFromRegister(inst[1]) + getBinaryFromImmX(inst[2],8)

def getSPStorageBinary(inst):
    '''_summary_

    Generate the binary encoding for a stack pointer storage instruction (e.g., STR, LDR)

    Args:
        inst (List): List of components of the stack pointer storage instruction

    Returns:
        String: Return the binary encoding for the given stack pointer storage instruction
    '''
    
    inst[0] += "_ST"
    stripedInst = inst[3].strip()
    inst[3] = stripedInst[0:len(stripedInst) - 1]
    inst[3] = divideImmX(inst[3],4)
    #We need to divide the immediate by 4 because the stack is composed with blocs of 4 bytes (32 bits)
    #By dividing the immediate we can evaluate how long is the jump of the stack pointer
    return dictionnaire[inst[0]] + getBinaryFromRegister(inst[1]) + getBinaryFromImmX(inst[3],8)

def getSPShiftBinary(inst):
    '''_summary_

    Generate the binary encoding for a stack pointer shift instruction (e.g., ADD, SUB with SP)

    Args:
        inst (List): List of components of the stack pointer shift instruction

    Returns:
        String: Return the binary encoding for the given stack pointer shift instruction
    '''
    
    inst[0] += "_SH"
    inst[2] = divideImmX(inst[2],4)
    return dictionnaire[inst[0]] + getBinaryFromImmX(inst[2], 7)

def getLabelReference(labelName, pc, sizeImm = 8):
    '''_summary_

    Get the binary representation of a label reference (used for branching)

    Args:
        labelName (String): The name of the label
        sizeImm (int, optional): The size of the immediate value in bits. Defaults to 8.

    Returns:
        String: Return the binary representation of the label reference
    '''
    
    labelIndex = int(labels[labelName]) - pc - 3
    return twoComplement(labelIndex, sizeImm)

def getBranchBinary(inst, pc):
    '''_summary_

    Generate the binary encoding for a branch instruction (e.g., BEQ, BNE)

    Args:
        inst (List): List of components of the branch instruction

    Returns:
        String: Return the binary encoding for the given branch instruction
    '''
    
    if(len(inst[0]) == 1): return dictionnaire[inst[0]] + getLabelReference(inst[1], pc, 11)
    return dictionnaire[inst[0]] + getLabelReference(inst[1], pc)

def twoComplement(integer, size):
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
        binary = shiftBit(binary, size)

        # transform all the 0 in 1 and the 1 in 0
        reversed = ""
        for i in range(len(binary)):
            if(binary[i] == "1"): reversed += "0"
            else: reversed += "1"

        binary = int(reversed, 2) + 1
        if(binary >= 2**size): return str(format(binary, "b"))[-size:]
        return str(format(binary, "b"))
    else:
        return shiftBit(str(format(integer, "b")),size)

def convertAssemblyToBin(inst, pc):
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
                binary = getRegisterOpBinary(inst)
            else:
                binary = getDataProcessingBinary(inst)
        
        case "LSRS":
            if(len(inst) == 4):
                binary = getRegisterOpBinary(inst)
            else:
                binary = getDataProcessingBinary(inst) 
            
        case "ASRS":
            if(len(inst) == 4):
                binary = getRegisterOpBinary(inst)
            else:
                binary = getDataProcessingBinary(inst)
        
        case "ADDS":
            binary = getArithmeticOperationBinary(inst)
        
        case "SUBS":
            binary = getArithmeticOperationBinary(inst)
        
        case "MOVS":
            binary = getArithmeticOperationBinary(inst)
        
        case "CMP":
            if(isA(inst[1],"#")):
                binary = getArithmeticOperationBinary(inst)
            else:
                binary = getDataProcessingBinary(inst)
        
        case "ANDS":
            binary = getDataProcessingBinary(inst)
        
        case "EORS":
            binary = getDataProcessingBinary(inst)
        
        case "ADCS":
            binary = getDataProcessingBinary(inst)
            
        case "SBCS":
            binary = getDataProcessingBinary(inst)
            
        case "RORS":
            binary = getDataProcessingBinary(inst)
            
        case "TST":
            binary = getDataProcessingBinary(inst)
        
        case "RSBS":
            binary = getDataProcessingBinary(inst)
        
        case "CMN":
            binary = getDataProcessingBinary(inst)
        
        case "ORRS":
            binary = getDataProcessingBinary(inst)
            
        case "MULS":
            binary = getDataProcessingBinary(inst)
            
        case "BICS":
            binary = getDataProcessingBinary(inst)
        
        case "MVNS":
            binary = getDataProcessingBinary(inst)

#       LOAD/STORE

        case "STR":
            binary = getSPStorageBinary(inst)

        case "LDR":
            binary = getSPStorageBinary(inst)

#       MISCELLANEOUS

        case "ADD":
            binary = getSPShiftBinary(inst)

        case "SUB":
            binary = getSPShiftBinary(inst)
        
#       BRANCH

        case "BEQ":
            binary = getBranchBinary(inst, pc) 

        case "BNE":
            binary = getBranchBinary(inst, pc) 

        case "BCS":
            binary = getBranchBinary(inst, pc) 

        case "BCC":
            binary = getBranchBinary(inst, pc) 

        case "BMI":
            binary = getBranchBinary(inst, pc) 

        case "BPL":
            binary = getBranchBinary(inst, pc) 

        case "BVS":
            binary = getBranchBinary(inst, pc) 

        case "BHI":
            binary = getBranchBinary(inst, pc) 

        case "BLS":
            binary = getBranchBinary(inst, pc) 

        case "BGE":
            binary = getBranchBinary(inst, pc) 

        case "BLT":
            binary = getBranchBinary(inst, pc) 

        case "BLE":
            binary = getBranchBinary(inst, pc) 

        case "BAL":
            binary = getBranchBinary(inst, pc)
        
        case "B":
            binary = getBranchBinary(inst, pc)

        case _: 
            return ""
    return binary
        
def sanitizeInput(input):
    '''_summary_

    Clean up input by stripping leading and trailing spaces and filtering empty entries

    Args:
        input (List): List of strings to be sanitized

    Returns:
        List: Return a list of non-empty and sanitized instruction strings
    '''
    
    return [inst for inst in input if inst.strip()]



def convertBinaryToHexa(binary):
    '''_summary_

    Convert a binary string to its hexadecimal representation

    Args:
        binary (String): The binary string to be converted

    Returns:
        String: Return the hexadecimal representation of the given binary string
    '''
    
    hexa = hex(int(binary,2))[2:]
    if(len(hexa) == 4): return hexa
    return shiftBit(hexa,4)

def convertAssemblyToHex(fileName):
    '''_summary_
    
    Read an assembly file and write, in hexadecimal, the non empty or non comments lines into a file

    Args:
        fileName (Path/String): Path of the assembly file
        
    Returns:
        void
    '''
    
    hexadecimals = []           # Hexadecimals values that will be written in the file
    filteredInstructions = []   # Formated instructions
    PC = 0                      # Program Counter

    try:
        with open(fileName, 'r') as fichier:
            instructions = fichier.read().splitlines()
            # Filter empty elements
            instructions = [line for line in instructions if line.strip()]

        # init the label and sanitize all the instructions
        for inst in instructions:
            inst = sanitizeInput(splitInstruction(inst.upper()))
            if not inst or inst[0].startswith(';') or inst[0].startswith('#') or inst[0].startswith('@'):       # Remove non usefull line
                continue
            elif (inst[0].startswith('.')): 
                labels[inst[0][0:len(inst[0])-1]] = PC         # Adding the new label with the program counter value in the label dictionnary
                continue
            PC += 1
            filteredInstructions.append(inst)

        PC = 0
        for filteredInst in filteredInstructions:
            filteredInst = convertAssemblyToBin(filteredInst, PC) # Get the binary representation of the instruction
            PC += 1
            hexadecimals.append(convertBinaryToHexa(filteredInst)) # Convert the binary representation in hexadecimal and add it to the list
 
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{fileName}' n'existe pas.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    
    return hexadecimals

def writeFile(hexadecimals, fileName = './output.bin'):
    '''_summary_
        Write the content of hexadecimals in a .bin file
        
        Args:
            hexadecimals (List): List of hexadecimals
            fileName (Path/String): Path to the output file
            
        Returns:
            void
    '''
    
    with open(fileName, 'w') as file:
        file.write('v2.0 raw\n')
        for hexa in hexadecimals:
            file.write(hexa + ' ')


fileName = "./../test_integration/conditional/branch.s"

writeFile(convertAssemblyToHex(fileName))