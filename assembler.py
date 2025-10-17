# assembler.py — now supports labels and jump instructions

import sys

OPCODES = {
    "LOAD": 0x01,
    "ADD": 0x02,
    "PRINT": 0x03,
    "JMP": 0x04,
    "JZ": 0x05,
    "JNZ": 0x06,
    "HALT": 0xFF
}

REGISTERS = {
    "R0": 0x00,
    "R1": 0x01,
    "R2": 0x02,
    "R3": 0x03
}

def first_pass(lines):
    labels = {}
    pc = 0
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.endswith(":"):
            label = line[:-1]
            labels[label] = pc
        else:
            tokens = line.split()
            instr = tokens[0].upper()
            if instr == "LOAD":
                pc += 3
            elif instr == "ADD":
                pc += 3
            elif instr == "PRINT":
                pc += 2
            elif instr in ("JMP", "JZ", "JNZ"):
                pc += 2
            elif instr == "HALT":
                pc += 1
    return labels

def second_pass(lines, labels):
    bytecode = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or line.endswith(":"):
            continue
        tokens = line.split()
        instr = tokens[0].upper()

        if instr == "LOAD":
            bytecode += [OPCODES[instr], REGISTERS[tokens[1].rstrip(",")], int(tokens[2])]
        elif instr == "ADD":
            bytecode += [OPCODES[instr], REGISTERS[tokens[1].rstrip(",")], REGISTERS[tokens[2]]]
        elif instr == "PRINT":
            bytecode += [OPCODES[instr], REGISTERS[tokens[1]]]
        elif instr == "JMP":
            bytecode += [OPCODES[instr], labels[tokens[1]]]
        elif instr == "JZ":
            bytecode += [OPCODES[instr], REGISTERS[tokens[1].rstrip(",")], labels[tokens[2]]]
        elif instr == "JNZ":
            bytecode += [OPCODES[instr], REGISTERS[tokens[1].rstrip(",")], labels[tokens[2]]]
        elif instr == "HALT":
            bytecode += [OPCODES[instr]]
        else:
            raise ValueError(f"Unknown instruction: {instr}")
    return bytecode

def assemble_file(input_path, output_path):
    with open(input_path, "r") as f:
        lines = f.readlines()
    labels = first_pass(lines)
    bytecode = second_pass(lines, labels)
    with open(output_path, "wb") as out:
        out.write(bytes(bytecode))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python assembler.py input.asm output.vm")
    else:
        assemble_file(sys.argv[1], sys.argv[2])
