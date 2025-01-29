# ========== Assembleur PARM ==========

import re

label = {}

conditions = {
    'EQ': "0000",
    'NE': "0001",
    'CS': "0010",
    'HS': "0010",
    'CC': "0011",
    'LO': "0011",
    'MI': "0100",
    'PL': "0101",
    'VS': "0110",
    'VC': "0111",
    'HI': "1000",
    'LS': "1001",
    'GE': "1010",
    'LT': "1011",
    'GT': "1100",
    'LE': "1101",
    'AL': "1110"
}
# Parseur

def dec_to_bin(n, bits):
    if not (0 <= n < 2**bits):
        raise ValueError(f"L'entier doit être compris entre 0 et {2**bits - 1} inclus pour {bits} bits.")
    return f"{n:0{bits}b}"
def get_reg(line):
    final = []
    for elem in line:
        if elem[0].lower() == "r":
            final.append(int(elem[1]))
    return final
def get_imm(line):
    final = []
    for elem in line:
        if elem[0] == "#":
            final.append(int(elem[1]))
    return final
def get_offset(line):
    final = []
    for elem in line:
        match = re.search(r'#(\d+)\]', elem)
        if match:
            final.append(int(match.group(1)))
    return final

def get_label(line):
    final = []
    for elem in line:
        if elem[0] == ".":
            final.append(elem)
    return final

def LSRS(imm, reg):
    if len(imm) == 0:
        return "0100000011" + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)
    return "00001" + dec_to_bin(imm[0], 5) + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)

def ASRS(imm, reg):
    if len(imm) == 0:
        return "0100000101" + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)
    return "00010" + dec_to_bin(imm[0], 5) + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)

def ADDS(imm, reg):
    if len(reg) == 3:
        return "0001100" + dec_to_bin(reg[2], 3) + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)
    elif len(reg) == 2:
        return "0001110" + dec_to_bin(imm[0], 3) + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)
    return "00110" + dec_to_bin(reg[0], 3) + dec_to_bin(imm[0], 8)

def SUBS(imm, reg):
    if len(reg) == 3:
        return "0001101" + dec_to_bin(reg[2], 3) + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)
    elif len(reg) == 2:
        return "0001111" + dec_to_bin(imm[0], 3) + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)
    return "00111" + dec_to_bin(reg[0], 3) + dec_to_bin(imm[0], 8)

def MOVS(imm, reg):
    return "00100" + dec_to_bin(reg[0], 3) + dec_to_bin(imm[0], 8)

def CMP(imm, reg):
    if len(reg) == 2:
        return "0100001011" + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)
    return "00101" + dec_to_bin(reg[0], 3) + dec_to_bin(imm[0], 8)

def ANDS(imm, reg):
    return "0100000000" + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)

def EORS(imm, reg):
    return "0100000010" + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)

def ASRS(imm, reg):
    if len(imm) == 0:
        return "0100000100" + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)
    return "00010" + dec_to_bin(imm[0], 5) + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)

def ADCS(imm, reg):
    return "0100000101" + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)

def SBCS(imm, reg):
    return "0100000110" + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)

def RORS(imm, reg):
    return "0100000111" + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)

def TST(imm, reg):
    return "0100001000" + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)

def RSBS(imm, reg):
    return "0100001001" + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)

def CMN(imm, reg):
    return "0100001011" + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)

def ORRS(imm, reg):
    return "0100001100" + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)

def MULS(imm, reg):
    return "0100001101" + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)

def BICS(imm, reg):
    return "0100001110" + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)

def MVNS(imm, reg):
    return "0100001111" + dec_to_bin(reg[1], 3) + dec_to_bin(reg[0], 3)

def STR(imm, reg, offset):
    return "10010" + dec_to_bin(reg[0], 3) + dec_to_bin(offset[0] >> 2, 8) # >> 2 is to divide by 4

def LDR(imm, reg, offset):
    return "10011" + dec_to_bin(reg[0], 3) + dec_to_bin(offset[0] >> 2, 8)

def ADD_SP(imm, reg, offset):
    return "101100000" + dec_to_bin(imm[0], 7)

def SUB_SP(imm, reg, offset):
    return "101100001" + dec_to_bin(imm[0], 7)

def B_UNCOND(labName):
    return "11100" + label[labName]

def B_COND(cond, labName):
    return "1101" + conditions[cond] + label[labName]




def association_line_cond(line):

    instruction = line[0].upper()
    imm = get_imm(line)
    reg = get_reg(line)
    offset = get_offset(line)

    if instruction == "LSRS":
        return LSRS(imm, reg)
    elif instruction == "ASRS":
        return ASRS(imm, reg)
    elif instruction == "ADDS":
        return ADDS(imm, reg)
    elif instruction == "SUBS":
        return SUBS(imm, reg)
    elif instruction == "MOVS":
        return MOVS(imm, reg)
    elif instruction == "CMP":
        return CMP(imm, reg)
    elif instruction == "ANDS":
        return ANDS(imm, reg)
    elif instruction == "EORS":
        return EORS(imm, reg)
    elif instruction == "ASRS":
        return ASRS(imm, reg)
    elif instruction == "ADCS":
        return ADCS(imm, reg)
    elif instruction == "SBCS":
        return SBCS(imm, reg)
    elif instruction == "RORS":
        return RORS(imm, reg)
    elif instruction == "TST":
        return TST(imm, reg)
    elif instruction == "RSBS":
        return RSBS(imm, reg)
    elif instruction == "CMN":
        return CMN(imm, reg)
    elif instruction == "ORRS":
        return ORRS(imm, reg)
    elif instruction == "MULS":
        return MULS(imm, reg)
    elif instruction == "BICS":
        return BICS(imm, reg)
    elif instruction == "MVNS":
        return MVNS(imm, reg)
    elif instruction == "STR":
        return STR(imm, reg, offset)
    elif instruction == "LDR":
        return LDR(imm, reg, offset)
    elif instruction == "ADD SP":
        return ADD_SP(imm, reg, offset)
    elif instruction == "SUB SP":
        return SUB_SP(imm, reg, offset)
    elif instruction == "B":
        return B_UNCOND(get_label(line))
    elif instruction == "B.COND":
        return B_COND(line[0][1:3],get_label(line))

    


def open_assembly_file(path):
    try:
        file = open(path, 'r')
        return file
    except:
        raise Exception("Error: Can't open file")
    
def parse_assembly_file(file):
    allLines = file.readlines()
    finalBinary = ""
    PC = 0

    #Pre-parsing for label :
    for line in allLines:
        line.replace(" ", "")
        if line[0] == "@" or line == "":
            continue # go to the next line
        elif line[0].startswith('.'):
            label[line[0]] == PC
            continue
        PC += 1


    # Parsing 
    for line in allLines:         
        line = line.split(" ")
        if len(line) > 0:
            instruction = line[0].upper()
    print(finalBinary)
    return finalBinary




parse = parse_assembly_file(open_assembly_file("./load_store/load_store.s"))

print(parse)
