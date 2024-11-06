# Linux Levels writeup - Link
This beginner challenge slowly introduces you to features of the Linux shell.

You connect to server using ssh

```
ssh -o PubkeyAuthentication=no level0@levels.eptc.tf
````

with credentials 

```
Username: level0
Password: EPT_CTF_2024
````

## Level0
We look around with `ls` and see password.txt

A quick `cat password.txt` and we are given the password for level1

`TPgBrAAARZ9CSUeq`

proceed to next level with `su - level1`

## Level1
We look around with `ls` and see level1.txt

Once more we try `cat level1.txt`, but we get `cat: level1.txt: Permission denied`

Ok, then what permissions is there on it? `ls -la` gives us

```
total 28
drwxr-x--- 1 level1 level1 4096 Oct 30 15:31 .
drwxr-xr-x 1 root   root   4096 Oct 29 20:53 ..
-rw-r--r-- 1 level1 level1  220 Jan  6  2022 .bash_logout
-rw-r--r-- 1 level1 level1 3771 Jan  6  2022 .bashrc
-rw-r--r-- 1 level1 level1  807 Jan  6  2022 .profile
---------- 1 level1 level1   45 Oct 29 20:45 level1.txt
-rw-r--r-- 1 root   root    505 Oct 29 20:52 readme.md
```

So we don't have read permissions. Well, we are the owner of it so why not change that?

`chmod +r level1.txt`

We try again with `cat level1.txt` and are finaly given the next password `KZcw0TQuCmTtbZl`

## Level2
A bit wiser this time we immediately check the permissions with `ls -la`

```
total 32
drwxr-x--x 1 level2 level2 4096 Oct 30 15:31 .
drwxr-xr-x 1 root   root   4096 Oct 29 20:53 ..
-rw-r--r-- 1 level2 level2  220 Jan  6  2022 .bash_logout
-rw-r--r-- 1 level2 level2 3771 Jan  6  2022 .bashrc
-rw-r--r-- 1 level2 level2  807 Jan  6  2022 .profile
-r-------- 1 level3 level3   45 Oct 29 20:45 level2.txt
-rw-r--r-- 1 root   root    487 Oct 29 20:45 readme.md
```

Okay, so our user does not even have any permissions to it. Checking the readme.md in the home directory we are given a hint that sudo might be of use.

![](one_eternity_later.jpg)

After trying way too many different things, for way too long, I discover that maybe we can check what sudo commands we can even do as the level2 user with `sudo -l -U level2`

```
User level2 may run the following commands on 6dccd5be5fc7:
    (level3) NOPASSWD: /usr/bin/cat /home/level2/level2.txt
```

Now this looks promising. We try using that exact command with sudo as level3 `sudo -u level3 /usr/bin/cat /home/level2/level2.txt`

```
The password for level 3 is: Udh7X5HQirw9sor
```

We are in business now boys. 

*PS: This step took an absolute embarrassing amount of time to solve. Will get better at reading man pages for next time...*

## Level3
Now, here comes the funny part. In my infinite wisdom on the last level I ended up exploring most of the file system in case there was some alternate binary of cat or something like that. During my search something called `supercat` popped up with level4 permissions in `/bin/`. I could practically hear the Curb Your Enthusiasm Theme in the background...

A quick `/bin/supercat level3.txt` giving us

```
The password for level 4 is: 5oEKE5YnOKFT8kls
```

and we are on our way
## Level4
We are met with `files.txt` which just contain a bunch of file names and a `secret-directory` that contains way to many files.

Reading the readme we are told that one of the filenames from `files.txt` exist within `secret-directory` and it contains the next password.

Now, I'm not interested in doing that manually so we will be bulding on that bash script snippet at the end of the readme

```
FILENAME="files.txt"
#!/bin/bash
for line in $(cat files.txt); do
  echo "$line" # replace with correct command
done
```

but we're gonna have to modify it a bit to this by creating a `script.sh` with `vim script.sh`

```
FILENAME="files.txt"
FOLDER="secret-directory"
#!/bin/bash
for line in $(cat files.txt); do
  if [ -f "$FOLDER/$line" ]; then
    echo "File '$line' exists in folder '$FOLDER'."
    cat $FOLDER/$line
  fi
done
```

a quick `chmod +x script.sh` to make it have execution permission and off to the races we go

```
level4@6dccd5be5fc7:~$ ./script.sh 
File 'zbkobnvbz.txt' exists in folder 'secret-directory'.
The password for level 5 is: N6qOm4atxPIgEKWQ

Did you know that execute on a folder can give unintended capabilities to read files inside the folder?
```

## Level5
Here we have to find the file containing the password in a forest of directories and sub-directories.

We are given a hint that the `find` command might be of use.

Google and Man is your friend if you do not know how to proceed.

Some minutes of digging later and I discover this lovely command `find . -name "*" -not -type d`. This command will search for files (not directories) in the current directory and all sub-directories. This is based on my own assumption that there will only be one file in there.

```
./evfcve/duiewb/txldmo/lfacge/fdkdwd/ffibpx/fdyxja/sqovnz/rhweih/rwautj/ounulanpngkmwzgshjnz
```

and we are correct

```
cat ./evfcve/duiewb/txldmo/lfacge/fdkdwd/ffibpx/fdyxja/sqovnz/rhweih/rwautj/ounulanpngkmwzgshjnz
ggwp, password for level6 is 7AHcUCtSmkVs49gF
```

## Level6
`ls` only reveals the readme. Paranoid as I am by this point I decide to run a quick `ls -la` just in case which reveals

```
total 32
drwxr-x--- 1 level6 level6 4096 Oct 30 19:50 .
drwxr-xr-x 1 root   root   4096 Oct 29 20:53 ..
-rw-r--r-- 1 root   root     89 Oct 29 20:45 ...
-rw-r--r-- 1 level6 level6  220 Jan  6  2022 .bash_logout
-rw-r--r-- 1 level6 level6 3771 Jan  6  2022 .bashrc
-rw-r--r-- 1 level6 level6  807 Jan  6  2022 .profile
-rw-r--r-- 1 root   root    116 Oct 29 20:45 readme.md
```

`...` surely is a unique name, and seems like linux hides it by default 🤔

```
cat ...
Congrats, you've just unlocked the next level
The password for level7 is: Du!kkKC2Jw!FuB
```

## Level7
we are immediately met with
```
┄level 7

This is the last level!

Sometimes people mess up the shell, and nothing works!

Just read the flag.txt in your home folder, and you are done.
total 32
drwxr-x--- 1 level7 level7 4096 Oct 30 19:50 .
drwxr-xr-x 1 root   root   4096 Oct 29 20:53 ..
-rw-r--r-- 1 level7 level7  220 Jan  6  2022 .bash_logout
-rw-r--r-- 1 root   root    218 Oct 29 20:45 .bashrc
-rw-r--r-- 1 level7 level7  807 Jan  6  2022 .profile
-rw-r--r-- 1 root   root     46 Oct 29 20:45 flag.txt
-rw-r--r-- 1 root   root    159 Oct 29 20:45 readme.md
level7@6dccd5be5fc7:~$
```
there is also weirdly no color on the user@hostname, and when we try to read the readme we get

```
-bash: readme.md: command not found
```

Seems like something weird is going on with the shell. Can we even move around?

```
level7@6dccd5be5fc7:~$ cd ..
level7@6dccd5be5fc7:/home$ 
```

ok, so at least that works. But what do we do from here? We have had to manually use cat before, maybe it will work this time too 🤷, and I'm assuming the home directory is /home/level7/ since that has been the convention so far

```
level7@6dccd5be5fc7:~$ /bin/cat /home/level7/flag.txt
EPT{Some_unix_Commands_are_always_fun_to_know}
```

Well, I guess this makes a little bit up for my mushroom trip of a journey finding the level3 password, *but not really...*