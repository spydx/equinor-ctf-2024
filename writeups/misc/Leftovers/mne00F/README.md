# Leftovers - writeup

## Description

Our "employee of the week" eloped. He was the only one that knew the master class secret. We managed to extract logs from his last activities   

Can you find anything from this?

## Writeup

### Analysis

First, the ```master.txt``` file is likely the master secret, and further down the log, the openssl tool has been used to encrypt this file:
```bash
~/code/openssl
❯ openssl enc -aes-256-cbc -pbkdf2 -iter $ITER -in master.txt -k $PWD -a
U2FsdGVkX1+/39qrCQ9rlxMW2E30ylTUXYS+GTAVDMUK0oXJvkUDBCRbhClK2GKYc50OQZ7zgLPBhkMW8CM5VVnZBrxfyH5CAG8nj5BPDCg=
```
This command:
- encrypts (```enc```) the input file (```-in master.txt```)
- uses the AES256 (Advanced Encryption Standard 256-bit key) encryption algorithm with the CBC (Cipher Block Chaining) mode (```-aes-256-cbc```)
- enables the use of the Password-Based Key Derivation Function 2 (```-pbkdf2```) with a given number of iterations (```-iter $ITER```)
- sets the password for the encryption (```-k $PWD```)
- and enables base64 processing of the data (```-a```)

### Decryption

Having the command makes it possible to decrypt it:
- First, find the decryption command - I just googled "openssl decryption" and found this [Stack Overflow](https://stackoverflow.com/questions/16056135/how-to-use-openssl-to-encrypt-decrypt-files) forum with this command:
```bash
openssl aes-256-cbc -d -a -pbkdf2 -in secrets.txt.enc -out secrets.txt.new
```
- Then create a file (secret.txt.enc) with the output from the encryption command:
```bash
❯ echo U2FsdGVkX1+/39qrCQ9rlxMW2E30ylTUXYS+GTAVDMUK0oXJvkUDBCRbhClK2GKYc50OQZ7zgLPBhkMW8CM5VVnZBrxfyH5CAG8nj5BPDCg= > secret.txt.enc
```
- Then, the number of iterations are needed, and the log file snippet below shows how the ```ITER``` environment variable was made. The employee used the today's date (when he encrypted the secret) in epoch format and divided it on 1000000.
```bash
> export ITER=$(($(date +%s) / 1000000))
```
- Before the creation of the ```ITER``` environment variable, the user printed the current week, the calendar, and the files in the directory:
```bash
❯ ls -la
total 8
drwxr-xr-x   3 USER108  staff   96 Sep 20 14:22 .
drwxr-xr-x  13 USER108  staff  416 Sep 20 14:04 ..
-rw-r--r--   1 USER108  staff   54 Sep 20 14:22 master.txt

~/code/openssl
> week
38

~/code/openssl
> cal
   September 2024
Su Mo Tu We Th Fr Sa
 1  2  3  4  5  6  7
 8  9 10 11 12 13 14
15 16 17 18 19 20 21
22 23 24 25 26 27 28
29 30
```
- Week 38 was from September 15 to 21, and the timestamp of the files indicate that it must be the 20th or 21st (can't have a timestamp in the future usually) - so I started with the 20th September to get:
```bash
❯ (date -d "2024-09-20" +"%s")
1726804800 // divided on 1000000 gives 1726 (remove decimals)
```
- Now, only the password variable remains, which was added with:
```bash
~/code/openssl
> export PWD=$(hostname)
```
- This means the hostname is the password, which is given at the top of the file: ```ubuntu-s-1vcpu-512mb-10gb-ams3-01```

- Now, with all the parts, the command (excluding the ```-out``` option) ends up as:
```bash
❯ openssl aes-256-cbc -d -a -pbkdf2 -iter 1726 -in secret.txt.enc -k ubuntu-s-1vcpu-512mb-10gb-ams3-01
```
This yields the output 

```Master class secret: EPT{Ach13v3m3nt_Unl0ck3d_293857}```
