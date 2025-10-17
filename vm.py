# vm.py — executes bytecode with jumps and conditional logic

class VM:
    def __init__(self, memory):
        self.memory = memory
        self.registers = [0] * 4  # R0–R3
        self.pc = 0               # Program counter
        self.running = True

    def fetch(self):
        byte = self.memory[self.pc]
        self.pc += 1
        return byte

    def run(self):
        while self.running:
            opcode = self.fetch()

            if opcode == 0x01:  # LOAD Rn, value
                reg = self.fetch()
                val = self.fetch()
                self.registers[reg] = val

            elif opcode == 0x02:  # ADD Rn, Rm
                r1 = self.fetch()
                r2 = self.fetch()
                self.registers[r1] += self.registers[r2]

            elif opcode == 0x03:  # PRINT Rn
                reg = self.fetch()
                print(f"R{reg} = {self.registers[reg]}")

            elif opcode == 0x04:  # JMP addr
                addr = self.fetch()
                self.pc = addr

            elif opcode == 0x05:  # JZ Rn, addr
                reg = self.fetch()
                addr = self.fetch()
                if self.registers[reg] == 0:
                    self.pc = addr

            elif opcode == 0x06:  # JNZ Rn, addr
                reg = self.fetch()
                addr = self.fetch()
                if self.registers[reg] != 0:
                    self.pc = addr

            elif opcode == 0xFF:  # HALT
                self.running = False

            else:
                raise Exception(f"Unknown opcode: {opcode:#04x}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python vm.py program.vm")
    else:
        with open(sys.argv[1], "rb") as f:
            program = list(f.read())
        vm = VM(program)
        vm.run()
