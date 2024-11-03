
# Chatlog

*Writeup by Sithis/solem.dev of team bootplug*

TL;DR: Wiener's attack.

This writeup will give a more deep-dive coverage of how this attack works under the hood. Many years ago I also co-authored a [CryptoBook article](https://cryptohack.gitbook.io/cryptobook/untitled/low-private-component-attacks/wieners-attack) on this attack which I recommend checking out.

During the CTF, I simply found a script for the attack on GitHub and ran it. But I want to share how this attack actually works, so that you can get a more thorough understanding of how one would approach this type of problem.

## Introduction 

We're given a text file containing a brief conversation between Rivest and Adleman. The conversation includes an RSA public key as well as encrypted ciphertext. RSA is one of the first ever invented public key cryptosystems, which allows for sharing knowledge on how to encrypt data without revealing how to decrypt it. As such, the system allows two parties to share secrets over an otherwise unprotected communication channel, without having previously exchanged secrets. RSA is an acronym of the names of its inventors, Rivest, Shamir and Adleman.

The cryptosystem works by combining exponentiation, modular arithmatic and the difficulty of factoring large prime products to create an asymmetric trapdoor function; where an operation is very easy to perform, but theoretically difficult to reverse without some piece of secret information (known as a private key).

If RSA encryption is new to you, I strongly recommend reading the [wikipedia article](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) and doing the introductory [RSA challenge-series](https://cryptohack.org/challenges/rsa/) on cryptohack, then come back to this writeup afterwards.

## Vulnerability: small private exponent

For those familiar with the RSA cryptosystem, one thing may immediately stick out is that the public exponent is much bigger than what is normal. In RSA, the public exponent is a modular multiplicative inverse of the private exponent modulo the totient of the public modulus. In other words, given the public exponent `e` and private exponent `d` for some modulus `n = p * q`, the following congruence defines the relation between `e` and `d`:

```
e * d = 1 (mod ɸ(n))
e * d = 1 (mod (p-1)*(q-1)) # expanding the totient ɸ(n)
```

Considering this, a very large public exponent `e` may imply a rather small private exponent `d`. This can in fact be exploited. One naïve approach could be to try and brute-force `d`, however this quickly becomes computationally expensive, especially for large values of `n`. Luckily, smart people have tackled this problem before us and there are some very mathematically elegant ways of cutting down our search space and find `d` quickly. One of these ways is to use [Continued fractions](https://en.wikipedia.org/wiki/Continued_fraction).

## Continued fractions

Continued fractions is a rather simple yet powerful mathematical tool. Put simply, a continued fraction is a way of expressing any fraction as a nested series of fractions. We accomplish this by separating out how as many multiples of the numerations that goes into the denominator, we den take the reciprocal of the remainder and repeat the process until we have a remainder of 1. The resulting nested sum is our continued fraction. 

For example, take the fraction `37/7`, the following shows how one may expand it to a condinued fraction:

```
37/7
= 35/7 + 2/7
= 5 + 2/7
= 5 + 1/(7/2)
= 5 + 1/(6/2 + 1/2)
= 5 + 1/(3 + 1/2)
= 5 + 1/(3 + 1/(2/1))
= 5 + 1/(3 + 1/(1 + 1/1))
```

Notice how it keeps cascating, forming smaller and smaller fractions until we eventually reach `1/1`. The nice thing about cascading fractions is that is also allows us to find fractions which are close approximates to fractions with larger numerators and denominators, simply by ignoring the remainder after x number of steps. For instance, in the above example, an approximation for the fraction `37/7` would be `5 + 1/3 = 16/3`. It will soon be apparent why this is important.

## Wiener's attack: using continued fractions to recover d

Due to the inverse relation between `e` and `d`, one may make the following observation:

```
e * d = 1 (mod ɸ(n))
e * d = 1 + k*ɸ(n)   # substitute the modulo for the coefficient *k*
e * d = k*ɸ(n) + 1   # rearrange terms
```

Just looking at the equation above, you may spot how this trivializes the recovery of `d`. The first time I was shown this attack, I felt great satisfaction with its elegance. In case it was not obvious: since `e` is roughly of the same size as `ɸ(n)` and `n`, that must mean that `k` is of the same size as `d`, and since we assume `d` to be small, we can also assume `k` to be small. Furthermore, since `ɸ(n) ≈ n` (only their lower bits differ), we can make the following deduction:

```
e * d = k*ɸ(n) + 1
e * d ≈ k*n + 1      # since ɸ(n) ≈ n
e * d ≈ k * n        # we can ignore the tiny constant
e / n ≈ k / d        # rearranging terms, left side are known terms!
```

Great! We now have a pretty good approximation of `k/d`! In fact, by constructing a continued fraction of `e/n`, we may discover factions with smaller denominators and numerators. Because of the close approximation, the chances of these being equal to `k` and `d` are pretty good, and guaranteed for cases where `d` is smaller than `1/3 * n^(1/4)`!

In the cryptobook article mentioned in the start of this writeup, I wrote a pretty handy SageMath implemenation of this attack. It may be handy to take a look at to better understand this attack. This implementation is also expediated by the polynomial relation between `ɸ(n)` and `n`, wherein `p` and `q` are the roots of the quadratic polynomial `x^2 - (n-ɸ(n)+1)x + n`; the proof of this is included in the article, but you may also try to prove it yourself as an exercise.

```py
def wiener(e, n):
    # Convert e/n into a continued fraction
    cf = continued_fraction(e/n)
    convergents = cf.convergents()
    for kd in convergents:
        k = kd.numerator()
        d = kd.denominator()
        # Check if k and d meet the requirements
        if k == 0 or d%2 == 0 or e*d % k != 1:
            continue
        phi = (e*d - 1)/k
        # Create the polynomial
        x = PolynomialRing(RationalField(), 'x').gen()
        f = x^2 - (n-phi+1)*x + n
        roots = f.roots()
        # Check if polynomial as two roots
        if len(roots) != 2:
            continue
        # Check if roots of the polynomial are p and q
        p,q = int(roots[0][0]), int(roots[1][0])
        if p*q == n:
            return d
    return None
```

# Challenge Solution

For the solution, I used the python module [oweiner](https://github.com/orisano/owiener) which implements the attack. This was the most expedient way of solving the challenge, without having to implement the attack by hand.

```py
from Crypto.Util.number import long_to_bytes as b2l
import owiener
import re

chat_log = open('chat.log','r').read()

params = re.findall(r'[0-9a-f]{20,}',chat_log) # capture long numbers
n, e, ct = map(lambda x:int(x), params) # convert hex strings to long types

d = owiener.attack(e, n) # run attack to recover private key
assert not d is None, "Attack failed" # assert that the private key was found

m = pow(ct, d, n) # decrypt ciphertext
message = b2l(m) # decode message
flag = re.findall(b'EPT\{.*\}', message)[0].decode() # regex the flag

print(flag) # print flag 🥳
```

Output: `EPT{Shamir_is_up_2_something}`

Aaaand we got the flag! Another attack that would have worked and deserves an honourable mention is the Boneh-Durfee attack. This attack is more complex but works for larger values of `d`, utilizing lattice reduction rather than continued fractions. It's worth considering this attack if you encounter a similar CTF-challenge where Wiener's attack refuses to work. You can find a Sage implementation of the Boneh-Durfee attack [here](https://github.com/mimoo/RSA-and-LLL-attacks/blob/master/boneh_durfee.sage).