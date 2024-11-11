**Author: Zukane**

*We intercepted some encrypted communication we think is very important. But it appears they are using uncrackable OTP?*
*We have two ciphertexts from the communication, and also the plaintext for the first. Can you help decrypt the second?*

##### Challenge Overview

In this crypto challenge, we are given a **intercept.txt** textfile containing the following:

```
# Known plaintext 1:
"Always use the one master OTP for all secure communications, it is uncrackable. Now listen carefully"

# Intercepted ciphertext 1 (hex):
c607eea76fc53ada95c9e7321434c264822158f8cc8ae2517deb4cf1ef6687bb4eecff4ac57c5bfcb1f39d5265d89a5e451171f2e3e1d3ffd8916f328e1ea7b3b073466a7e8eb7b56255051de269996654b85254cff2e49b71faec792c908d318ad42c1d

# Plaintext 2: 
🤷♂

# Intercepted ciphertext 2 (hex):
cb02f4af629663c093dee72b1922916a8b210bb5d996b6053ffb60cdde3492f448a3be40c02808edbae3cf5a24c881565a4450cfd0ae87d8d8883c6bdd12f3e7b169153f6388a6a6644a5e5fcb5ce33d6de4491793f6a4b060a4937734bd8325ceda6119    
```

Essentially, we are given **C1**, **C2** and **P1** where **P2** is presumably the flag. A One-Time-Pad can easily be broken if the same key is used multiple times. The messages are encrypted by performing: 

$$C1 = P1 \oplus K$$ 

$$C2 = P2 \oplus K$$ 

Since the XOR has the inverse property, we can retrieve K by performing

$$K = C1 \oplus P1$$

and with the key, we can simply XOR with C2 to decrypt:

$$C1 \oplus K = P2$$

##### Solution

```python
def xor_bytes(bytes1, bytes2):
    return bytes([b1 ^ b2 for b1, b2 in zip(bytes1, bytes2)])

plaintext1 = b"Always use the one master OTP for all secure communications, it is uncrackable. Now listen carefully"
ciphertext1 = bytes.fromhex("c607eea76fc53ada95c9e7321434c264822158f8cc8ae2517deb4cf1ef6687bb4eecff4ac57c5bfcb1f39d5265d89a5e451171f2e3e1d3ffd8916f328e1ea7b3b073466a7e8eb7b56255051de269996654b85254cff2e49b71faec792c908d318ad42c1d")
ciphertext2 = bytes.fromhex("cb02f4af629663c093dee72b1922916a8b210bb5d996b6053ffb60cdde3492f448a3be40c02808edbae3cf5a24c881565a4450cfd0ae87d8d8883c6bdd12f3e7b169153f6388a6a6644a5e5fcb5ce33d6de4491793f6a4b060a4937734bd8325ceda6119")
key = key[:len(ciphertext2)]

plaintext2 = xor_bytes(ciphertext2, key).decode()
print(plaintext2)
```

This gives us the output:

```
Limit your messages to 100chars to fit the master OTP. Now use this secret: EPT{w3lc0m3_t0_my_kr1b!}
```

flag: `EPT{w3lc0m3_t0_my_kr1b!}`
