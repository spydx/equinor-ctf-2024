
# Double Dip Dilemma

*Writeup by Sithis/solem.dev of team bootplug*

We're given a file `intercept.txt` containing one plaintext and two ciphertexts. The messages are encrypted with a so-called [One-Time Pad](https://en.wikipedia.org/wiki/One-time_pad) (OTP). This is a very simple form of encryption which relies of bitwise XORing a message with a random binary sequence. As the name implies, the pad may only be used once. Using the pad twice allows an attacker to recover it using the inherent properties of XOR.

# Exclusive OR

Exclusive OR, called *XOR* for short, is a bit operation between two or more bits. For two bits, this operation will be `1` if and only if the two bits are different, and `0` otherwise. This operation has a nice property in that it functions as both a commutative operation and as its own inverse operation, which makes it very handy for cryptograpy IF used cautiously. This operation is usually denoted as an encircled plus-sign `⊕`, usually programming languages denote it with the caret sign `^` (not to be confused with exponentiation, which is often denoted as a double asterisk `**`). In general, any number of input bits, the XOR-operation whether there is an odd number of `1`; this property is known as "parity" and is handy in e.g. error correction algorithms.

Here is a truth table of the XOR operation

| A | B | A⊕B |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

Do note that the operation works as its own inverse, so `A = (A⊕B)⊕B` and `B = (A⊕B)⊕A`.

# One-Time Pad

As the name One-Time Pad implies, this sequence may only be used once; this is because XOR is its own inverse operation, and it's commutative. The way OTP works normally is that you encrypt your message with a random bit sequence (known as a "key", "bitstream" or  "one-time pad") that only you and the receiver knows, you then send this encrypted message to its recipient, which may decrypt the message by XORing it again with the same random sequence; the self-inverse property of XOR ensures that the original message is recovered by the recipient.

The commutative property of XOR also has the side-effect that anyone with the knowledge of both the message and the ciphertext (encrypted version of the message) may recover the OTP sequence simply by XORing these together:

```
normal OTP operations:
ciphertext = key ⊕ message
message = key ⊕ ciphertext

key recovery:
key = message ⊕ ciphertext
```

We have both the plaintext message and ciphertext of the first message, so we may then recover the key and decrypt the 2nd message, which should grant us the flag.

# Challenge Solution

There are several methods one could use to solve this challenge. For beginners, I would recommend checking out [CyberChef](https://gchq.github.io/CyberChef/), it's a very user-friendly tool for solving codes developed by the British intelligence and security service GCHQ.

The following link is a recipe in cyberchef which decrypts the message:

https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')XOR(%7B'option':'UTF8','string':'Always%20use%20the%20one%20master%20OTP%20for%20all%20secure%20communications,%20it%20is%20uncrackable.%20Now%20listen%20carefully'%7D,'Standard',false)XOR(%7B'option':'Hex','string':'c607eea76fc53ada95c9e7321434c264822158f8cc8ae2517deb4cf1ef6687bb4eecff4ac57c5bfcb1f39d5265d89a5e451171f2e3e1d3ffd8916f328e1ea7b3b073466a7e8eb7b56255051de269996654b85254cff2e49b71faec792c908d318ad42c1d'%7D,'Standard',false)&input=Y2IwMmY0YWY2Mjk2NjNjMDkzZGVlNzJiMTkyMjkxNmE4YjIxMGJiNWQ5OTZiNjA1M2ZmYjYwY2RkZTM0OTJmNDQ4YTNiZTQwYzAyODA4ZWRiYWUzY2Y1YTI0Yzg4MTU2NWE0NDUwY2ZkMGFlODdkOGQ4ODgzYzZiZGQxMmYzZTdiMTY5MTUzZjYzODhhNmE2NjQ0YTVlNWZjYjVjZTMzZDZkZTQ0OTE3OTNmNmE0YjA2MGE0OTM3NzM0YmQ4MzI1Y2VkYTYxMTk&oeol=CR

Alternatively, you could solve it with python:

```py
>>> xor = lambda a,b:bytes(i^j for i,j in zip(a,b)) # black magic that allows for bitwise xor of byte strings
>>> message = b'Always use the one master OTP for all secure communications, it is uncrackable. Now listen carefully'
>>> ct1 = bytes.fromhex('c607eea76fc53ada95c9e7321434c264822158f8cc8ae2517deb4cf1ef6687bb4eecff4ac57c5bfcb1f39d5265d89a5e451171f2e3e1d3ffd8916f328e1ea7b3b073466a7e8eb7b56255051de269996654b85254cff2e49b71faec792c908d318ad42c1d')
>>> key = xor(message, ct1)
>>> ct2 = bytes.fromhex('cb02f4af629663c093dee72b1922916a8b210bb5d996b6053ffb60cdde3492f448a3be40c02808edbae3cf5a24c881565a4450cfd0ae87d8d8883c6bdd12f3e7b169153f6388a6a6644a5e5fcb5ce33d6de4491793f6a4b060a4937734bd8325ceda6119')
>>> flag = xor(key, ct2)
>>> flag
b'Limit your messages to 100chars to fit the master OTP. Now use this secret: EPT{w3lc0m3_t0_my_kr1b!}'
```

The flag is `EPT{w3lc0m3_t0_my_kr1b!}`. Note that this is a common problem that may occur in more advanced cryptosystems. For instance, [stream ciphers](https://en.wikipedia.org/wiki/Stream_cipher) such as CTR-mode or RC4 are an extention of OTP which allows for shorter keys and a nonce to generate the bitstream, rather than using it as a key directly. If the nonce is reused, the streams will be identical, and thus an attacker could use the same technique demonstrated here to recover the ciphertream and decrypt future messages.

Another pitfall with XOR-based encryption, as we will see in the challenge `LFSXOR`, is the use of a bitstream shorther than the plaintext message. If the bitstream wraps around and is used on repeat to encrypt the whole message, one may once again employ the same technique to use a known part of the message to decrypt the unknown parts.
