OPCODES = {
    'NOP':  0xCC,
    'MOV':  0x01,
    'MOVI': 0x02,
    'LOAD': 0x03,
    'STORE':0x04,
    'LOADI':0x05,
    'XCHG': 0x06,
    'LOADW':0x07,
    'STOREW':0x08,
    'ADD':  0x10,
    'ADDI': 0x11,
    'SHL':  0x12,
    'SHR':  0x13,
    'AND':  0x14,
    'OR':   0x15,
    'XOR':  0x16,
    'NOT':  0x17,
    'JMP':  0x20,
    'JE':   0x21,
    'JO':   0x22,
    'MOVS': 0x23,
    'OUT':  0x40,
    'CMP':  0x50,
    'HLT':  0xFF,
}

REGISTERS = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
}

class Assembler:
    def __init__(self):
        self.labels = {}          
        self.instructions = []    
        self.machine_code = []   
        self.errors = []         

    def assemble(self, code):
        self.lines = code.strip().splitlines()
        self.first_pass()
        if not self.errors:
            self.second_pass()
        else:
            for error in self.errors:
                print(error)

    def first_pass(self):
        
        address = 0
        for lineno, line in enumerate(self.lines):
            line = line.strip()
            if not line or line.startswith(';'):
                continue
            if ':' in line:
                label, rest = line.split(':', 1)
                label = label.strip()
                rest = rest.strip()
                if label in self.labels:
                    self.errors.append(f"Error on line {lineno+1}: Duplicate label '{label}'")
                else:
                    self.labels[label] = address
                line = rest
                if not line:
                    continue
            tokens = line.split()
            mnemonic = tokens[0].upper()
            if mnemonic not in OPCODES:
                self.errors.append(f"Error on line {lineno+1}: Unknown instruction '{mnemonic}'")
                continue
            self.instructions.append({'line': line, 'address': address, 'lineno': lineno+1})
            address += 4

    def second_pass(self):
        for instr in self.instructions:
            line = instr['line']
            address = instr['address']
            lineno = instr['lineno']
            tokens = line.strip().split()
            if not tokens:
                continue
            mnemonic = tokens[0].upper()
            opcode = OPCODES.get(mnemonic)
            operands = ' '.join(tokens[1:]).split(',')
            operands = [operand.strip() for operand in operands]
            bytecode = [0x00] * 4
            bytecode[0] = opcode

            try:
                if mnemonic in ('NOP', 'HLT'):
                    pass 
                
                elif mnemonic == 'MOV':
                    dest = self.parse_register(operands[0], lineno)
                    src = self.parse_register(operands[1], lineno)
                    bytecode[1] = dest
                    bytecode[2] = src

                elif mnemonic == 'MOVI':
                    reg = self.parse_register(operands[0], lineno)
                    imm = self.parse_immediate(operands[1], lineno)
                    bytecode[1] = reg
                    bytecode[2] = (imm >> 8) & 0xFF
                    bytecode[3] = imm & 0xFF
                
                elif mnemonic == "LOAD":
                    reg = self.parse_register(operands[0], lineno)
                    imm = self.parse_immediate(operands[1], lineno)
                    bytecode[1] = reg
                    bytecode[2] = (imm >> 8) & 0xFF
                    bytecode[3] = imm & 0xFF
                
                elif mnemonic == "STORE":
                    reg = self.parse_register(operands[0], lineno)
                    imm = self.parse_immediate(operands[1], lineno)
                    bytecode[1] = reg
                    bytecode[2] = (imm >> 8) & 0xFF
                    bytecode[3] = imm & 0xFF
                
                elif mnemonic == "LOADI":
                    dest = self.parse_register(operands[0], lineno) 
                    src = self.parse_register(operands[1], lineno)
                    bytecode[1] = dest
                    bytecode[2] = src
                
                elif mnemonic == "XCHG":
                    reg1 = self.parse_register(operands[0], lineno) 
                    reg2 = self.parse_register(operands[1], lineno)
                    bytecode[1] = reg1
                    bytecode[2] = reg2

                elif mnemonic == 'ADD':
                    dest = self.parse_register(operands[0], lineno)
                    src = self.parse_register(operands[1], lineno)
                    bytecode[1] = dest
                    bytecode[2] = src

                elif mnemonic == 'ADDI':
                    reg = self.parse_register(operands[0], lineno)
                    imm = self.parse_immediate(operands[1], lineno)
                    bytecode[1] = reg
                    bytecode[2] = (imm >> 8) & 0xFF
                    bytecode[3] = imm & 0xFF

                elif mnemonic == 'OUT':
                    reg = self.parse_register(operands[0], lineno)
                    bytecode[1] = reg

                elif mnemonic == 'CMP':
                    reg = self.parse_register(operands[0], lineno)
                    imm = self.parse_immediate(operands[1], lineno)
                    bytecode[1] = reg
                    bytecode[2] = (imm >> 8) & 0xFF
                    bytecode[3] = imm & 0xFF

                elif mnemonic == "LOADW":
                    reg = self.parse_register(operands[0], lineno)
                    add = self.parse_immediate(operands[1], lineno)
                    bytecode[1] = reg
                    bytecode[2] = (add >> 8) & 0xFF
                    bytecode[3] = add & 0xFF

                elif mnemonic == "STOREW":
                    reg = self.parse_register(operands[0], lineno)
                    add = self.parse_immediate(operands[1], lineno)
                    bytecode[1] = reg
                    bytecode[2] = (add >> 8) & 0xFF
                    bytecode[3] = add & 0xFF

                elif mnemonic == "SHR":
                    reg = self.parse_register(operands[0], lineno)
                    imm = self.parse_immediate(operands[1], lineno)
                    bytecode[1] = reg
                    bytecode[3] = imm
                
                elif mnemonic == "SHL":
                    reg = self.parse_register(operands[0], lineno)
                    imm = self.parse_immediate(operands[1], lineno)
                    bytecode[1] = reg
                    bytecode[3] = imm
                
                elif mnemonic in ('JMP', 'JE', 'JO'):
                    addr = self.parse_address(operands[0], lineno)
                    bytecode[2] = (addr >> 8) & 0xFF
                    bytecode[3] = addr & 0xFF
                
                elif mnemonic == "CMP":
                    reg = self.parse_register(operands[0], lineno)
                    imm = self.parse_immediate(operands[1], lineno)
                    bytecode[1] = reg
                    bytecode[2] = (imm >> 8) & 0xFF
                    bytecode[3] = imm & 0xFF

                elif mnemonic == "MOVS":
                    imm = self.parse_immediate(operands[0], lineno)
                    bytecode[2] = (imm >> 8) & 0xFF
                    bytecode[3] = imm & 0xFF

                else:
                    self.errors.append(f"Error on line {lineno}: Instruction '{mnemonic}' not implemented")
                    continue

                self.machine_code.extend(bytecode)

            except IndexError:
                self.errors.append(f"Error on line {lineno}: Incorrect operands for '{mnemonic}'")

        if self.errors:
            for error in self.errors:
                print(error)

    def parse_register(self, reg, lineno):
        reg = reg.upper()
        if reg in REGISTERS:
            return REGISTERS[reg]
        else:
           return int(reg)
            

    def parse_immediate(self, imm_str, lineno):
        try:
            if imm_str.startswith("0x"):
                imm = int(imm_str,16)
            elif not imm_str.isnumeric():
                if len(imm_str) == 2:
                    imm = (ord(imm_str[0]) << 8) | ord(imm_str[1])
                else:
                    imm = ord(imm_str)
            else:
                imm = int(imm_str)

            if 0 <= imm <= 0xFFFF:
                return imm
            else:
                self.errors.append(f"Error on line {lineno}: Immediate value out of range: {imm_str}")
                raise ValueError
        except ValueError:
            self.errors.append(f"Error on line {lineno}: Invalid immediate value '{imm_str}'")
            raise

    def parse_address(self, addr_str, lineno):
        if addr_str in self.labels:
            return self.labels[addr_str]
        else:
            return self.parse_immediate(addr_str, lineno)

    def get_machine_code(self):
        return self.machine_code
