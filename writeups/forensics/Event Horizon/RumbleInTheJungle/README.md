# Event Horizon writeup

This challenge uses the memory dump from the Phantom Phish challenge. The easiest way to explore the memory dump is by using [MemProcFS](https://github.com/ufrisk/MemProcFS). We can then browse it like a file system.

`MemProcFS.exe -f dump.dmp -forensic 1`

Given the name of the challenge, the attacker's workstation name can most likely be found in the Event Logs. With the dump opened in MemProcFS, the Event Logs can be found in `M:\forensic\files\ROOT\Windows\System32\winevt\Logs`.

Security.evtx is usually the place to go when looking for information related to logins, but the file extracted with MemProcFS is corrupted. We can use [EVTXtract](https://github.com/williballenthin/EVTXtract) to recover fragments.

`evtxtract ffffc50ce048c510-Security.evtx > security.xml`

From a previous challenge using the same memory dump, we know the attacker uses IP 192.168.88.130. Near the first occurrence of this IP in the extracted fragments, there is a strange WorkstationName.

```xml
<Data Name="TargetUserName">Benjamin</Data>
<Data Name="TargetDomainName">DESKTOP-995TBHT</Data>
<Data Name="TargetLogonId">0x0000000000ba8724</Data>
<Data Name="LogonType">3</Data>
<Data Name="LogonProcessName">NtLmSsp </Data>
<Data Name="AuthenticationPackageName">NTLM</Data>
<Data Name="WorkstationName">5GD5rtMUx94PcATWoU3dngvmsVQsn</Data>
<Data Name="LogonGuid">{00000000-0000-0000-0000-000000000000}</Data>
<Data Name="TransmittedServices">-</Data>
<Data Name="LmPackageName">NTLM V2</Data>
<Data Name="KeyLength">128</Data>
<Data Name="ProcessId">0x0000000000000000</Data>
<Data Name="ProcessName">-</Data>
<Data Name="IpAddress">192.168.88.130</Data>
```

`5GD5rtMUx94PcATWoU3dngvmsVQsn` is identified as Base58 by CyberChef.

Decoding it gives us the flag `EPT{opsec_hax0r_h0st}`
