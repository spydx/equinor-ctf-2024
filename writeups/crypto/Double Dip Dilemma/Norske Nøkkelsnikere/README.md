# Double Dip Dilemma

Writeup author: `Hoover`

## Overview

We are given a `intercept.txt` file that contains two plaintexts and two ciphertexts. The ciphertexts are encrypted with a One-Time Pad (OTP), which is a very simple form of encryption that relies on bitwise XORing a message with a random binary sequence. Since the OTP is deterministic, we can use the inherent properties of XOR to recover the key.

## Vulnerability

The vulnerability: OTP key reuse

The one-time pad is theoretically unbreakable when used correctly. However, its security relies on two critical factors:

1. The key must be truly random
2. The key must never be reused

In this challenge, the second rule is violated, since we are given two plaintexts and two ciphertexts that are encrypted with the same OTP key. By reusing the OTP key, the system becomes vulnerable to a [known-plaintext attack](https://en.wikipedia.org/wiki/Known-plaintext_attack).

## The Attack

The attack exploits the properties of the XOR operation used in OTP encryption:

If $P_1 \oplus K = C_1$, then $K = P_1 \oplus C_1$

Once we have $K$, we can decrypt any message encrypted with this key: $P_2 = C_2 \oplus K$

We first extract the key from the first ciphertext and plaintext:

$K = P_1 \oplus C_1$

Then we use this key to decrypt the second ciphertext:

$P_2 = C_2 \oplus K$

## Solution

For first solving the challenge, I used CyberChef since it was the fastest way to get the solution, when I recognized the OTP vulnerability. This lead me to a first blood on this introductory crypto challenge.

For a more technical and indepth writeup, please check out Sithis from bootplug's [writeup](../bootplug/README.md). At the end I wrote a simple [solve.py](solve.py) script that will print out the whole message. 

```
Limit your messages to 100chars to fit the master OTP. Now use this secret: EPT{w3lc0m3_t0_my_kr1b!}
```	

The flag is: `EPT{w3lc0m3_t0_my_kr1b!}`