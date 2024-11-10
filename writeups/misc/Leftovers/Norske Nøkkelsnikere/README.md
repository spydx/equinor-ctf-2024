# Leftovers

Writeup author: `Hoover`

## Overview

We are given a terminal log from a user, where the user is encrypting a file called `master.txt` with openssl. It uses the hostname as the password and the current time as the number of iterations, and the encryption algorithm is AES-256-CBC with PBKDF2 key derivation. At last it is encoded with base64.

Full command:
```bash
openssl enc -aes-256-cbc -pbkdf2 -iter $ITER -in master.txt -k $PWD -a
```

Output:
```
U2FsdGVkX1+/39qrCQ9rlxMW2E30ylTUXYS+GTAVDMUK0oXJvkUDBCRbhClK2GKYc50OQZ7zgLPBhkMW8CM5VVnZBrxfyH5CAG8nj5BPDCg=
```

## Solution

AES-256-CBC is a symmetric encryption algorithm, which means that the same key and iterations are used for encryption and decryption.

Since we know the hostname and the iteration count from the terminal log, we can decrypt the file using the same command but with the decryption flag `-d`.

Save the output to a file called `encrypted.txt` and run the following command to decrypt it:

```bash
openssl enc -aes-256-cbc -pbkdf2 -iter 1726 -d -a -in encrypted.txt -k ubuntu-s-1vcpu-512mb-10gb-ams3-01
```

The output contains the flag.

```
Master class secret: EPT{Ach13v3m3nt_Unl0ck3d_293857}
```

Flag: `EPT{Ach13v3m3nt_Unl0ck3d_293857}`