# assembler.py — converts .asm to .vm bytecode

import sys

OPCODES = {
    "LOAD": 0x01,
    "ADD": 0x02,
    "PRINT": 0x03,
    "HALT": 0xFF
}

REGISTERS = {
    "R0": 0x00,
    "R1": 0x01,
    "R2": 0x02,
    "R3": 0x03
}

def assemble_line(line):
    tokens = line.strip().split()
    if not tokens or tokens[0].startswith("#"):
        return []

    instr = tokens[0].upper()
    if instr == "LOAD":
        return [OPCODES[instr], REGISTERS[tokens[1].rstrip(",")], int(tokens[2])]
    elif instr == "ADD":
        return [OPCODES[instr], REGISTERS[tokens[1].rstrip(",")], REGISTERS[tokens[2]]]
    elif instr == "PRINT":
        return [OPCODES[instr], REGISTERS[tokens[1]]]
    elif instr == "HALT":
        return [OPCODES[instr]]
    else:
        raise ValueError(f"Unknown instruction: {instr}")

def assemble_file(input_path, output_path):
    bytecode = []
    with open(input_path, "r") as f:
        for line in f:
            bytecode.extend(assemble_line(line))

    with open(output_path, "wb") as out:
        out.write(bytes(bytecode))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python assembler.py input.asm output.vm")
    else:
        assemble_file(sys.argv[1], sys.argv[2])
