# Writeup 
by Bissas

## Solution 
Sending any 32 character long string followed by the string "FLAG" will give you the flag. 
### Example 
```bash
$ ncat --ssl baby-bro-pwn.ept.gg 1337
```
```
What's up dude?
> aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaFLAG
Yoooo lit af fam!
sick tbh...
legit dude, my broski passed me this msg, you can lowkey get it.
no cap.

EPT{g00d_j0b_my_dud3}
```

## Explanation

Looking at main, you see that the program will write the flag, only if `homie.showFlag == 0x47414c46`. Okay! But how do we do that?

When first opening the source file there are two important hints that indicate that the solution might have something to do with a buffer overflow: 
- At the top of the source file, there is a comment containing the command used to compile the source. 
  ```bash
  $ gcc baby_bro_pwn.c -o baby_bro_pwn -fno-stack-protector
  ```
  Here, the `fno-stack-protector` compiler option is used, meaning that the program will give no warnings for buffer overflows.
- The messages gets read from stdin with this line:
  ```c
  fgets(homie.message, 37, stdin);`
  ```
  This reads 37 bytes from stdin and puts it into homie.message. But I thought homie.message was only 32 bytes long! Where do the other bytes end up? 
- The Dude struct is defined with '\_\_attribute\_\_((\_\_packed\_\_))', meaning that the compiler will not insert any padding in between the members of the struct.
  In other words, if you continue writing past the message buffer, you will overflow directly into showFlag.

Now all that is left to do is to overflow the message buffer and write the correct value into homie.showFlag. 
Converting the hexvalue for showFlag into ASCII, we get "GLAF" (FLAG but backwards). 
Now, if you have been paying attention, you may have noticed that in my solution i send FLAG, and not GLAF. 
That is because when we start writing past homie.message we first write to the least significant byte of the homie.showFlag int and then keep writing the bytes from right to left. 
