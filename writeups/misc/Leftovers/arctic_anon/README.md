# Leftovers CTF Challenge Writeup

Writeup author: [`SondreUM`](https://github.com/SondreUM/)

## Analysis

[Source file](../terminal.log.txt)

The command provided in the challenge description is an encryption command using the `openssl` tool. The command encrypts the contents of the file `master.txt` using the AES-256-CBC encryption algorithm with PBKDF2 key derivation and a specified number of iterations. The encryption key is derived from the password provided by the user. The encrypted output is then base64 encoded.

```bash
❯ openssl enc -aes-256-cbc -pbkdf2 -iter $ITER -in master.txt -k $PWD -a
```

### Command Breakdown

The encryption command explained without any help from chatgpt:

- `openssl enc`: This invokes the openssl encryption tool to encrypt or decrypt data.
- `-aes-256-cbc`: Specifies the encryption algorithm. Here, it is AES (Advanced Encryption Standard) with a 256-bit key length, in CBC (Cipher Block Chaining) mode.
- `-pbkdf2`: Enables the use of PBKDF2 (Password-Based Key Derivation Function 2) to derive the encryption key from the password, adding an additional layer of security by making brute-force attacks harder.
- `-iter $ITER`: Sets the number of iterations for PBKDF2. The variable $ITER is used to specify how many times the key derivation function will run to generate the encryption key. Higher iterations make the process slower but increase security.
- `-in master.txt`: Specifies the input file (master.txt) to be encrypted.
- `-k $PWD`: Sets the password for encryption, using the current working directory ($PWD) as the password. This is generally unconventional and potentially insecure unless $PWD is unique and known only to the user.
- `-a`: Enables Base64 encoding of the output. This makes the encrypted text easier to share or store in text files, as it transforms the binary data into a text format.

## Solving the challenge

Since aes-256-cbc is a symmetric encryption algorithm, we can decrypt the encrypted file using the same password and iterations used for encryption.

First we find the `$PWD` variable, which is set to the current hostname and can be found on the first line on the login prompt.

```bash
.-/+oossssoo+/-.               USER108@ubuntu-s-1vcpu-512mb-10gb-ams3-01
```

Next is the `$ITER` used for deriving the key.
Iter is constructed from current data and time in unix epoch format.

From the command history we can see that the datetime used for the encryption is week 38 of 2024. To get some idea of the values we are dealing with we perform a quick test with current datetime.

```bash
echo $(($(date +%s)/1000000))
1730
```

Which, because of the high divisor is a fairly low number. And if we are lucky means that the possible iter values will be within a small range.

We test the first and last day of week 38 in 2024 to get the possible values for the iter variable.
With some quick terminal math we get the following values.

```bash
$ echo $(($(date -d "2024-09-16" +%s)/1000000))
1726
$ echo $(($(date -d "2024-09-22" +%s)/1000000))
1726
```

We now know the values of both `$PWD` and `$ITER`.
We check the openssl tool to check for any decryption options.

```bash
$ openssl enc --help
General options:
 -help               Display this summary
 -list               List ciphers
 -ciphers            Alias for -list
 -e                  Encrypt
 -d                  Decrypt
```

We now know the values of both `$PWD` and `$ITER`.
And construct the following command to decrypt the file.

```bash
$ openssl enc -aes-256-cbc -pbkdf2 -iter 1726 -in cipher.txt -k ubuntu-s-1vcpu-512mb-10gb-ams3-01 -a -d
Master class secret: EPT{Ach13v3m3nt_Unl0ck3d_293857}
```
