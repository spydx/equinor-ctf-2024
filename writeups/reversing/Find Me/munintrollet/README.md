## Find Me

### Challenge

We were given a binary which prints the first 5 bytes of the flag.

```
$ ./findme
This is the 5 first bytes of the flag: EPT{Y
Can you find the rest?
```

By running `strace` we can find out that the `write` syscall is used to print the text to `stdout`.

```
$ strace ./findme
...
write(4, "This is the 5 first bytes of the"..., 45This is the 5 first bytes of the flag: EPT{Y
) = 45
write(4, "Can you find the rest?\n", 23Can you find the rest?
) = 23
...
```

By setting a breakpoint in gdb for write and running the program we break on write where the register `r13` contains the text `This is the 5 first bytes of the flag: EPT{Y\nU`
```
pwndbg> b *write
Breakpoint 1 at 0x7190
pwndbg> r
```

```
R13  0x7fffffffd080 <- 'This is the 5 first bytes of the flag: EPT{Y\nU'
```

The entire flag is not there, but if we search for it in gdb, we get it.
```
pwndbg> search -t bytes "EPT"
Searching for value: 'EPT'
libstdc++.so.6.0.33 0x7fbf5bf6d49f 0x1511554554545045
libicudata.so.72.1 0x7fbf6182fd6b 0x6556550065545045 /* 'EPTe' */
libicudata.so.72.1 0x7fbf618387aa 0x4c50454e55545045 ('EPTUNEPL')
libicudata.so.72.1 0x7fbf6183b64d 0x120454e55545045
libicudata.so.72.1 0x7fbf6183e00e 0x5245424d45545045 ('EPTEMBER')
libicudata.so.72.1 0x7fbf6183e7f8 0x420455649545045
libicudata.so.72.1 0x7fbf6184d004 0x20454c5055545045 ('EPTUPLE ')
libicudata.so.72.1 0x7fbf6185b449 0x1c28624e4f545045
libicudata.so.72.1 0x7fbf6185fafe 0x3c5031948545045
libicudata.so.72.1 0x7fbf61862875 0x70c08666545045
libicudata.so.72.1 0x7fbf61864f0c 0xab01205245545045
libcrypto.so.3  0x7fbf62625b2c 0x7245000a48545045 /* 'EPTH\n' */
[anon_7fbffa800] 0x7fbffa8057b8 'EPT{YOU_FOUND_4_WAY_TO_R3AD_M3_W3LL_DON3}g0mRZDjBmC5IHTS9Qvlav8CSt5OkjBETaf6ZUa3d'
[stack]         0x7fffffffd0a7 0x550a597b545045 /* 'EPT{Y\nU' */
```