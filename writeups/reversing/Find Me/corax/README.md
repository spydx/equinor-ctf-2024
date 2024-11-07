# Find me
By: langemyh @ Corax

Categories: Reversing

```
This time, the author is in way too deep; he has no clue what he is doing other than thinking it is so fancy. Run the program and find out.
```

## Intruduction
A binary which outputs the first five bytes of the flag. It is an `ELF`, so Linux all the way here!

## Writeup
Trying to find out what kind of file this is:
```zsh
❯ file findme
findme: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=4f00317451453d0535ef5e5d07b9184d1c58af6b, for GNU/Linux 3.2.0, stripped
```

Then running it:
```zsh
❯ chmod +x findme

❯ ./findme
This is the 5 first bytes of the flag: EPT{Y
Can you find the rest?
```

Running the binary using `pwndgb`[1]:
```zsh
gdb ./findme
```

Running the binary and automatically setting a breakpoint at `entry` using the `entry` command:
```zsh
pwndbg> entry
Temporary breakpoint 1 at 0x55555555bd70
```

The hypothesis is that the flag is to be found somewhere in the memory. Just checking if we can find it using the `pwndbg` `search` command[2]:
```zsh
pwndbg> search "EPT{"
Searching for byte: b'EPT{'
```

No luck. We do know that the first five bytes of the flag being displayed as output. So, trying to see if it is possible to just set a breakpoint when something is being output to the screen[3]:
```zsh
pwndbg> catch syscall write
Catchpoint 2 (syscall 'write' [1])
pwndbg> c
Continuing.
[New Thread 0x7fbf62e006c0 (LWP 9946)]
[New Thread 0x7fbf612006c0 (LWP 9948)]
```

This puts us at the start of the `write` function:
```zsh
 ► 0   0x7ffff7dc924f write+79
```

From the registry, we can see that the correct text is in memory at least:
```zsh
*R13  0x7fffffffd990 ◂— 'This is the 5 first bytes of the flag: EPT{Y\nU'
```

Trying the `search` command for `EPT{` again:
```zsh
pwndbg> search "EPT{"
Searching for byte: b'EPT{'
[anon_7fbffa400] 0x7fbffa405710 'EPT{YOU_FOUND_4_WAY_TO_R3AD_M3_W3LL_DON3}gacCbTnx1QaFBxwIxVfAqW4izCGtBMORMdEtF5O6'
```

And there the flag is:
> EPT{YOU_FOUND_4_WAY_TO_R3AD_M3_W3LL_DON3}

## Links
[1] https://github.com/pwndbg/pwndbg
[2] https://browserpwndbg.readthedocs.io/en/docs/commands/procinfo/search/
[3] https://stackoverflow.com/questions/1538463/how-can-i-put-a-breakpoint-on-something-is-printed-to-the-terminal-in-gdb