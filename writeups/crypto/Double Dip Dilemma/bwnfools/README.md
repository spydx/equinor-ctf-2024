# Writeup 

author: .spydx & fibonacciii @ bwnfools

## Double Dip Dilemma :baby:

```plaintext
# Known plaintext 1:
"Always use the one master OTP for all secure communications, it is uncrackable. Now listen carefully"

# Intercepted ciphertext 1 (hex):
c607eea76fc53ada95c9e7321434c264822158f8cc8ae2517deb4cf1ef6687bb4eecff4ac57c5bfcb1f39d5265d89a5e451171f2e3e1d3ffd8916f328e1ea7b3b073466a7e8eb7b56255051de269996654b85254cff2e49b71faec792c908d318ad42c1d

# Plaintext 2: 
🤷‍♂️

# Intercepted ciphertext 2 (hex):
cb02f4af629663c093dee72b1922916a8b210bb5d996b6053ffb60cdde3492f448a3be40c02808edbae3cf5a24c881565a4450cfd0ae87d8d8883c6bdd12f3e7b169153f6388a6a6644a5e5fcb5ce33d6de4491793f6a4b060a4937734bd8325ceda6119
```

We have two intercepted ciphertexts and one known plaintext.

Since the plain text mentions OTP (One-time pad) [1], we could consider this a hint. A OTP cipher uses a pre-shared key, and is uncrackable, given that key is sufficiently random, and is not reused for multiple messages. If the pre-shared key is used in several messages, we can easily derive the pre-shared (`OTP_HEX`) key by XOR the known plaintext 1 (`PT1`) against the intercepted ciphertext 1 (`CT1`). Knowing the key, we can use it to decrypt the intercepted ciphertext 2 (`CT2`), and find its plaintext (`PT2`).

We first convert the known plaintext and intercepted ciphertexts to a common format in bytes.

```psudo
OTP = PT1 XOR CT1
PT2 = CT2 XOR OTP
```

```python
PT1 = "Always use the one master OTP for all secure communications, it is uncrackable. Now listen carefully"
CT1_HEX = "c607eea76fc53ada95c9e7321434c264822158f8cc8ae2517deb4cf1ef6687bb4eecff4ac57c5bfcb1f39d5265d89a5e451171f2e3e1d3ffd8916f328e1ea7b3b073466a7e8eb7b56255051de269996654b85254cff2e49b71faec792c908d318ad42c1d"

# Check PT with CT1 HEX
PT1_BYTES = PT1.encode("utf-8")
CT1_BYTES = bytes.fromhex(CT1_HEX)
XOR1_BYTES = bytes(a ^ b for a, b in zip(PT1_BYTES, CT1_BYTES)) # PT1 XOR OTP = C1, PT1 XOR CT1 = OTP
OTP_HEX  = bytes.hex(XOR1_BYTES)

print("otp:", OTP_HEX)

# Unencrypt CT2
CT2_HEX = "cb02f4af629663c093dee72b1922916a8b210bb5d996b6053ffb60cdde3492f448a3be40c02808edbae3cf5a24c881565a4450cfd0ae87d8d8883c6bdd12f3e7b169153f6388a6a6644a5e5fcb5ce33d6de4491793f6a4b060a4937734bd8325ceda6119"
CT2_BYTES = bytes.fromhex(CT2_HEX)
PT2_BYTES = bytes(a ^ b for a, b in zip(CT2_BYTES, XOR1_BYTES)) # PT2 XOR OTP = CT2, CT2 XOR OTP = PT2
PT2_RAW = bytes.hex(PT2_BYTES)

print("p2, raw:", PT2_RAW)

# Decode and print message
print("p2, plain:", PT2_BYTES.decode("utf-8"))
```

```shell
┌──(.spydx㉿kali)-[~/equinor-ctf-2024/DoubleDIPDilemma]
└─$ python solve.py
otp: 876b99c616b61aafe6acc7467c51e20bec447895adf996340fcb03a5bf46e1d43ccc9e26a95c2899d286ef3745bbf53328641f9b8080a796b7ff1c1eae77d393d900661f10edc5d4013e647f8e0cb7461ad72574a39b97ef1494cc1a4de2e857ffb84064
p2, raw: 4c696d697420796f7572206d6573736167657320746f20313030636861727320746f2066697420746865206d6173746572204f54502e204e6f77207573652074686973207365637265743a204550547b77336c63306d335f74305f6d795f6b723162217d
p2, plain: Limit your messages to 100chars to fit the master OTP. Now use this secret: EPT{w3lc0m3_t0_my_kr1b!}
                                                              
```

`p2, plain` reveal the flag: `EPT{w3lc0m3_t0_my_kr1b!}`

## Source

1. [https://en.wikipedia.org/wiki/One-time_pad](https://en.wikipedia.org/wiki/One-time_pad)