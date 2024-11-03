
# LFSXOR

We are given a `.bmp` image file and a python script used for image encryption. The bitmap image looks at first glance to be pure noise. The python script looks like som sort of [Linear-Feedback Shift Register](https://en.wikipedia.org/wiki/Linear-feedback_shift_register). This challenge also requires having a bit of knowledge about the XOR-operation and its properties when used in cryptography, have a look at my writeup on Double Dip Dilemma on how that works.

# LFSR

If you've never heard of LFSR before or you're not entirely sure what it is, I strongly recommend [Computeriphile's video with Mike Pound](https://www.youtube.com/watch?v=Ks1pw1X22y4) on the subject. It is an excellent coverage of the subject that gives you everything you need to understand this challenge and work towards a solution on your own.

The basic gist is this: you have a register of bits that are set to a random initial value, called a seed. The internal state is then updated by doing XOR on selected indexes of the register to obtain a new value, which is then appended to the start of the register. The end of the register is then removed and used as the first output of the generator.

This PRNG will at most have a preiod equal to the number of possible internal states. In the case of our challenge, the register is 32 bits, making the period at most `2^32 = 4 294 967 296`. Though it may be shorter, as we will see.

# Challenge Solution

The first step is to check the period of the LFSR. We may due this by simulating the generation of bytes with a random seed until we get an internal state that equals the initial seed; this will indicate that the LFSR as circled back to its initial state, and will thus start repeating itself. The number of steps before it reaches this point of repition is known as the *period.*

Credits to feynman137 who found that the LFSR had a short period:

```py
x0 = random.randint(0, 2**32)

x = x0
x ^= (x << 14) & 0xFFFFFFFF
x ^= (x >> 6) & 0xFFFFFFFF
x ^= (x << 11) & 0xFFFFFFFF

i = 0
while x != x0:
    x ^= (x << 14) & 0xFFFFFFFF
    x ^= (x >> 6) & 0xFFFFFFFF
    x ^= (x << 11) & 0xFFFFFFFF
    i += 1
    #print(i, x)

print(i)
### $ python3 lol.py 
### 9361
```

The number at the bottom is the number of steps *after* the initial state before it returned to `x0`. The period is thus `9362 + 1` to account for the initial state.

With this knowledge, I took to re-writing the encryption program to *decrypt* images instead. We simply take the first 9362 pixels of the image, and XOR the whole image, wrapping around at the end of rows.

```py
import sys

import numpy
import matplotlib.pyplot as plt
from PIL import Image

def decrypt(in_img, out_img):
    in_img = plt.imread(in_img)[:, :, 0]
    height = len(in_img)
    width = len(in_img[0])
    
    imarr = numpy.zeros((height, width, 3), dtype='uint8')
    crib = [in_img[(i//2048),i%2048] for i in range(9362)] # grab the first 9362 pixels
    
    for y in range(height):
        for x in range(width):
            imarr[y,x] = int(in_img[y,x] ^ crib[(y*2048 + x)%len(crib)])
    
    im = Image.fromarray(imarr.astype('uint8')).convert('RGB')
    im.save(out_img)

if __name__=='__main__':
    IN_IMG = sys.argv[1]
    OUT_IMG = sys.argv[2]
    decrypt(IN_IMG, OUT_IMG)
```

Running this on `out.bmp` gives us an image with the flag:

`python3 solve.py out.bmp flag.bmp`
![flag](./flag.bmp)


The image is still a bit grainy, but you can make out that the flag is `EPT{DOUBLECRYPTOFAIL}`.