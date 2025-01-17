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
    
    splitedInstruction = inst.split(' ', 1)
    if(len(splitedInstruction) > 1):  
        instruction = splitedInstruction[0].strip()
        arguments = [arg.strip() for arg in splitedInstruction[1].split(',')]
        return [instruction] + arguments
    return splitedInstruction

def isA(data, type):
    data = data.strip()
    if(data[0] == type): return True
    return False

def shiftBit(binary, size):
    save = binary
    for i in range(size - len(save)): save = "0" + save
    return save

def getBinaryFromRegister(register):
    register = register.strip()
    registerBinary = str(format(int(register[1]),"b"))

    if(len(registerBinary) == 3): return registerBinary

#    for i in range(3 - len(registerBinary)): registerBinary = "0" + registerBinary
#    return registerBinary

    return shiftBit(registerBinary, 3)



def getBinaryFromImmX(imm, size):
    imm = imm.strip("")
    immBinary = str(format(int(imm[1:]),"b"))

    if(len(immBinary) == size): return immBinary

#    for i in range(size - len(immBinary)): immBinary = "0" + immBinary
#    return immBinary

    return shiftBit(immBinary,size)

def divideImmX(imm, diviser):
    imm = imm.strip()
    return "#" + str(int(imm[1:])//diviser)

def getDataProcessingBinary(inst):
    inst[0] += "_DP"
    return dictionnaire[inst[0]] + getBinaryFromRegister(inst[2]) + getBinaryFromRegister(inst[1])

def getRegisterOpBinary(inst):
    inst[0] += "_RO"
    return dictionnaire[inst[0]] + getBinaryFromImmX(inst[3],5) + getBinaryFromRegister(inst[2]) + getBinaryFromRegister(inst[1])

def getArithmeticOperationBinary(inst):
    if(len(inst) == 4):
        if(isA(inst[3],"R")): 
            inst[0] += "_AOR"
            return dictionnaire[inst[0]] + getBinaryFromRegister(inst[3]) + getBinaryFromRegister(inst[2]) + getBinaryFromRegister(inst[1])
        else: 
            inst[0] += "_AOI"
            return dictionnaire[inst[0]] + getBinaryFromImmX(inst[3],3) + getBinaryFromRegister(inst[2]) + getBinaryFromRegister(inst[1])
    else:
        return dictionnaire[inst[0]] + getBinaryFromRegister(inst[1]) + getBinaryFromImmX(inst[2],8)

def getSPStorageBinary(inst):
    inst[0] += "_ST"
    stripedInst = inst[3].strip()
    inst[3] = stripedInst[0:len(stripedInst) - 1]
    inst[3] = divideImmX(inst[3],4)
    return dictionnaire[inst[0]] + getBinaryFromRegister(inst[1]) + getBinaryFromImmX(inst[3],8)

def getSPShiftBinary(inst):
    inst[0] += "_SH"
    inst[2] = divideImmX(inst[2],4)
    return dictionnaire[inst[0]] + getBinaryFromImmX(inst[2], 7)

def getLabelReference(labelName, sizeImm = 8):
    label = str(format(int(labels[labelName]), "b"))
    print(label," -> ",sizeImm)
    return shiftBit(label,sizeImm)

def getBranchBinary(inst):
    if(len(inst[0]) == 1): return dictionnaire[inst[0]] + getLabelReference(inst[1],11)
    return dictionnaire[inst[0]] + getLabelReference(inst[1])

def translateInstructionInBinary(inst):
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
            binary = getBranchBinary(inst) 

        case "BNE":
            binary = getBranchBinary(inst) 

        case "BCS":
            binary = getBranchBinary(inst) 

        case "BCC":
            binary = getBranchBinary(inst) 

        case "BMI":
            binary = getBranchBinary(inst) 

        case "BPL":
            binary = getBranchBinary(inst) 

        case "BVS":
            binary = getBranchBinary(inst) 

        case "BHI":
            binary = getBranchBinary(inst) 

        case "BLS":
            binary = getBranchBinary(inst) 

        case "BGE":
            binary = getBranchBinary(inst) 

        case "BLT":
            binary = getBranchBinary(inst) 

        case "BLE":
            binary = getBranchBinary(inst) 

        case "BAL":
            binary = getBranchBinary(inst)
        
        case "B":
            binary = getBranchBinary(inst)

        case _: 
            return ""
    return binary
        

def sanitizeInput(input):
    return [inst for inst in input if inst.strip()]

def convertBinaryToHexa(binary):
    hexa = hex(int(binary,2))[2:]
    if(len(hexa) == 4): return hexa

    for i in range(0,4-len(hexa)):
        hexa = "0" + hexa
    return hexa

#   return shiftBit(hexa,4)


def lire_fichier_assembleur(nom_fichier):
    """
    Lit un fichier assembleur et affiche les lignes non vides
    et non commentées.

    :param nom_fichier: Le chemin vers le fichier assembleur.
    """

    hexadecimals = []
    filteredInstructions = []
    PC = 0

    try:
        with open(nom_fichier, 'r') as fichier:
            instructions = fichier.read().splitlines()
            # Filter empty elements
            instructions = [line for line in instructions if line.strip()]

        for inst in instructions:
            inst = sanitizeInput(splitInstruction(inst.upper()))
            if not inst or inst[0].startswith(';') or inst[0].startswith('#') or inst[0].startswith('@'):
                continue
            elif (inst[0].startswith('.')): 
                labels[inst[0][0:len(inst[0])-1]] = PC
                continue
            PC += 1
            filteredInstructions.append(inst)
        
        print(labels)

        for filteredInst in filteredInstructions:
            print(filteredInst)
            filteredInst = translateInstructionInBinary(filteredInst)
            print(filteredInst)
            hexadecimals.append(convertBinaryToHexa(filteredInst))

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' n'existe pas.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    
    return hexadecimals

nom_fichier = "/home/superdri/Documents/Polytech/si3/s5/architecture/parm_project/code_asm/test_integration/conditional/branch.s"
print(lire_fichier_assembleur(nom_fichier))


