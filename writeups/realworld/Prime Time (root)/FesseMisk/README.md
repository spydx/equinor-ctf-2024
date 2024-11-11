# Prime Time (Root)

## Description
Can you escalate your privileges to root?

Use the same instance as for Prime Time (user).

## Solution

Starting from the reverse shell gained in the user challenge, we aim to escalate privileges to root. Running [linpeas](https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS) reveals that our user can execute all scripts in `/opt/CSCOlumos/rcmds/` as root without a password:



From the reverse shell we gained in the user challenge, we have to now try and escalate our privileges to root. I quickly run [linpeas](https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS) on the box and scroll through the output.

From linpeas, we see that that our user can run all script in the `/opt/CSCOlumos/rcmds/` directory as root without a password. 

```bash
User prime may run the following commands:
    (ALL) SETENV: NOPASSWD: /opt/CSCOlumos/rcmds/
```
This directory contains many scripts, offering multiple potential paths to root. Writing secure Bash code can be challenging, and common pitfalls make it easy to overlook vulnerabilities. For more on these issues, check out [Bash Pitfalls](https://mywiki.wooledge.org/BashPitfalls).

Among the many scripts in this directory, some have a race condition vulnerability. These scripts copy a temporary file to `/tmp` and then execute it. By continually overwriting this file with a simple bash command, we can get a root shell:
```bash
while true; do echo -e '#!/bin/sh\n/bin/bash' > /tmp/rmanExec.sh; done
```

The flag is in `/root/root.txt`.
