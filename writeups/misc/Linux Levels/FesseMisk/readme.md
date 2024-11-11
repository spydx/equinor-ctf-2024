## Solution

This was a nice beginner `OverTheWire`-like challenge, where you have to use various linux commands in order to progess the different levels and achieve the flag.

### Level 0

I started by connecting to the server using SSH.

```bash
$ ssh -o PubkeyAuthentication=no level0@levels.eptc.tf
Password: EPT_CTF_2024

$ ls
password.txt  readme.md

$ cat password.txt
TPgBrAAARZ9CSUeq
```
The readme.md file explained that there are 8 levels and each level has a password to access the next level. I used the password from password.txt to switch to level 1.

**Level 1**
```bash
$ su - level1
Password: TPgBrAAARZ9CSUeq

$ ls
level1.txt  readme.md

$ cat level1.txt
cat: level1.txt: Permission denied
```
Our user does not have read permission on `level1.txt`. By running `ls -al` we can see the permission codes for the files in the current folder, where we see that the file has no read, write og execute permission at all (w/r/x). We are allowed to change the permissions of the file using `chmod`. The `+r` argument gives read permission to the file - which is all we need.


```bash
$ ls -al
---------- 1 level1 level1   45 Oct 29 20:45 level1.txt q

$ chmod +r level1.txt

$ ls -al
-r--r--r-- 1 level1 level1   45 Oct 29 20:45 level1.txt

$ cat level1.txt
The password for level 2 is: KZcw0TQuCmTtbZl
```

**Level 2**
```bash
$ su - level2
Password: KZcw0TQuCmTtbZl

$ ls
level2.txt  readme.md

$ cat level2.txt
cat: level2.txt: Permission denied
```
We do not have permission now either to read the file, and we are not allowed to use `chmod` to fix it. The `readme.md` hinted that I could use sudo to read the level2.txt file. I used sudo to read the file as user "level3" and found the password for level 3.

```bash
$ sudo -u level3 cat /home/level2/level2.txt
sudo: unable to resolve host b170d4014777: Temporary failure in name resolution
The password for level 3 is: Udh7X5HQirw9sor
```

**Level 3**
```bash
$ su - level3
Password: Udh7X5HQirw9 sor

$ ls
level3.txt  readme.md
```

The `readme.md` file hinted that I could use a `setuid` program to read the level3.txt file. I used `find` to locate setuid programs and found supercat, which I used to read the file.

```bash
$ find / -perm -4000 2>/dev/null
/usr/bin/chfn
/usr/bin/su
/usr/bin/chsh
/usr/bin/gpasswd
/usr/bin/umount
/usr/bin/newgrp
/usr/bin/passwd
/usr/bin/mount
/usr/bin/supercat
/usr/bin/sudo
```

`supercat` sounds like the on we are looking for.

```bash
$ /usr/bin/supercat level3.txt
The password for level 4 is: 5oEKE5YnOKFT8kls
```

**Level 4**
```bash
$ su - level4
Password: 5oEKE5YnOKFT8kls

$ ls
files.txt  secret-directory
```

The `readme.md` file hinted that I needed to find a readable file in the `secret-directory`. I wrote a script to find the readable file and found the password for level 5

```bash
#!/bin/bash
# shell.sh
FILENAME="files.txt"
DIRECTORY="secret-directory"

for line in $(cat "$FILENAME"); do
  if cat "$DIRECTORY/$line" &>/dev/null; then
    echo "Found readable file: $line"
    cat "$DIRECTORY/$line"
    break
  fi
done
```
```bash
$ ./shell.sh
Found readable file: zbkobnvbz.txt
The password for level 5 is: N6qOm4atxPIgEKWQ

Did you know that execute on a folder can give unintended capabilities to read files inside the folder?
```

**Level 5**

```bash
$ su - level5
Password: N6qOm4atxPIgEKWQ

$ ls
folders
```
The `readme.md`file hinted that I needed to find a file containing the password in the `folders` directory. I used `find` to locate the file and found the password for level 6.

```bash
$ find folders -type f
folders/evfcve/duiewb/txldmo/lfacge/fdkdwd/ffibpx/fdyxja/sqovnz/rhweih/rwautj/ounulanpngkmwzgshjnz

$ cat folders/evfcve/duiewb/txldmo/lfacge/fdkdwd/ffibpx/fdyxja/sqovnz/rhweih/rwautj/ounulanpngkmwzgshjnz
ggwp, password for level6 is 7AHcUCtSmkVs49gF
```
**Level 6**
```
$ su - level6
Password: 7AHcUCtSmkVs49gF

$ ls
```
The `readme.md` file hinted that the password for level 7 was hidden in a file in my home folder, which is our current working directory. The command `ls -a` shows all files in the current directory, including hidden files with a filename beginning with `.`. At first I thougt the password was hidden in the `.profile` or `.bashrc`, until I spotted the `...` file, hiding among the `.`=current directory and `..`=One folder up.

```bash
$ ls -a
.  ..  ...  .bash_logout  .bashrc  .profile  readme.md

$ cat ...
Congrats, you've just unlocked the next level
The password for level7 is: Du!kkKC2Jw!FuB
```
**Level 7**

```bash
$ su - level7
Password: Du!kkKC2Jw!FuB

$ ls
flag.txt

$ cat ./flag.txt
EPT{Some_unix_Commands_are_always_fun_to_know}
```

**EPT{Some_unix_Commands_are_always_fun_to_know}**