# Saint Rings - writeup

## Description

In the code where the shadows lie,

St. Rings with the binary eye,

Illuminates what can't be found,

In pitch dark, her skills renowned,

Bringing truth forth from the digital nigh.

## Writeup

### Analysis

When running the file ```darkness```, the the following text is printed
```bash
Speak friend and enter
```
and prompts the user for an input. After providing an input (e.g., "hello"), the program prints
```bash
'Only after devoting myself to Str. Rings could I finally see the truth'
```
Based on this, it is likely futile to find the correct input, so reversing it is.

### Reversing

Since this is a baby challenge, I started with the ```strings``` command. Since the flag format is also known, I also used the ```grep``` command:

```bash
strings darkness | grep -i "ept"
```

This listed the flag ```EPT{0n3_str1ng_t0_rul3_th3m_4ll}```