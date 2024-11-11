# Writeup
by fluffyhake

## Solution
Finding the hidden file and looking at it's contents reveals the flag.

### Example
```
┌──(kali㉿kali)-[~]
└─$ sudo grep -r "EPT{" /
/dev/shm/.secret:EPT{y0ur_v3ry_0wn_EPTb0x_tm}
```

## Explanation
Looking at the challenge we learn there is a hidden file which most likely contains our flag.
Using grep we can look through all files and output the content that contains our specified string.

---

```
sudo grep -r "EPT{" /
```

- **`sudo`**: Runs the command with elevated permissions, allowing us to search through all files in the filesystem.
- **`grep`**: The tool used to search the contents of files.
- **`-r`**: Recursive flag for `grep`, enabling it to search through all subdirectories and their files.
- **`"EPT{"`**: The target string to match in the file contents.
- **`/`**: Specifies the starting point for the search. Here, `/` refers to the root directory, so `grep` searches through all files on the system.
