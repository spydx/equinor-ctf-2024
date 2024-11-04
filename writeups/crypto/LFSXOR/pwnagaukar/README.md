# LFSXOR

Writeup author: `dagurb`

## Overview

We get a program that encrypts a black and white image containing the flag. Looking at the rand function, we can see that it is exceptionally simple.

```python
def get_rand(x):
	def _random():
		nonlocal x
		x ^= (x << 14) & 0xFFFFFFFF
		x ^= (x >> 6) & 0xFFFFFFFF
		x ^= (x << 11) & 0xFFFFFFFF
		return x & 0xFF
	return _random
```

The image is encrypted by xoring consecutive outputs from rand with the image data.

## Approach

So, if we assume some set of pixels are the same, we can create a z3 model which finds all solutions which generate those pixels. Initially, I tried solving for first 5 or so pixels, assuming that they were all the same color, but that gave 64 solutions, and I did not want to check them all. So instead I made the assumption that the first 5 pixels in the first column were the same color.

## Implementation

To reverse engineer the rng, we use z3. Technically, we could also have solved a GF(2) matrix, since the rng is clearly linear over GF(2)^32, but that would have taken a longer time to implement.

Firstly, we modify the rng to work with z3

```python
def get_rand(x):
	def _random():
		nonlocal x
		x ^= (x << 14)
		x ^= LShR(x, 6)
		# x ^= (x >> 6)
		x ^= (x << 11)
		return x & 0xFF
	return _random
```

We initialize a symbolic variable `key = BitVec('a', 32)` and use it as the key.

```python
formulae = []

# we assume that the first k pixels are of the same color
pix = BitVec('pix', 32) # 32 bits because I could not be bothered to figure out how Exctract() works
formulae.append(pix & 0xffffff00 == 0)

for y in trange(5):
	for x in range(width):
		if x != 0:
			rand() # step rand
		else:
			formulae.append(simplify(rand()) == int(in_img[y,x]) ^ pix)
```
by default, z3 only finds one solution, but we can force it to find as many as we want with this function

```python
def get_models(F, M):
	result = []
	s = Solver()
	s.add(F)
	while len(result) < M and s.check() == sat:
		m = s.model()
		result.append(m)
		# Create a new constraint the blocks the current model
		block = []
		for d in m:
			# d is a declaration
			if d.arity() > 0:
				raise Z3Exception("uninterpreted functions are not supported")
			# create a constant from declaration
			c = d()
			if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
				raise Z3Exception("arrays and uninterpreted sorts are not supported")
			block.append(c != m[d])
		s.add(Or(block))
	return result
```

Running this we get

```
[[pix = 255, a = 2525603961], [pix = 183, a = 2248927280], [pix = 182, a = 2249828401], [pix = 254, a = 2526799992]]
```

Decrypting using the key `2525603961` we get

![](flag.bmp)

Although this is not the correct key, we can still read the flag `EPT{DOUBLECRYPTOFAIL}`.

Easy first blood.
