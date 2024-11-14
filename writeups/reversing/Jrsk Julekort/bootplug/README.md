# Jærsk Julekort
By poiko

We get a binary that apparently implements a version of the stego used in NPST's infamous :snegle:-challenge from 2019, together with a BMP image where something has been hidden. 
```console
$ ./julekort
Usage: ./julekort <message> <input_bmp> <output_bmp>
```
The binary takes a message and an input image and generates an output image. Turns out the first argument is not the message itself, but a file containing the message. The binary is statically linked and with symbols, but opening it in ida we also see that most of the relevant symbols are just a garbled mess:
```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
    [...]

    init_buffering();
    if ( argc == 4 )
    {
        SAScJWtbKaO3scxb = read_RYAOrlhDFATpppdjSvnI_uAcCjZslXRWbcRlNDvUc_into_array(argv[1], &ZvZkKJWwCwOkNs);
        qzRBoUrJHnaWhEQyzAbw = BXMaZvZkKJWwCwhdPcgm(argv[2], &uAcCjZslXRWbcRlNDvUcHeader, &GcnwUmRVencQYyYPtXmL);
        if ( qzRBoUrJHnaWhEQyzAbw && ZvZkKJWwCwOkNs )
        {
            CfwmYPIaAbEKHCyNzJhp(qzRBoUrJHnaWhEQyzAbw, GcnwUmRVencQYyYPtXmL.SrTQnYWFmoofiDcjyLXs, GcnwUmRVencQYyYPtXmL.IcnwkMhDBwqClbkzXNxz);
            generate_random_vSBrFLJcJWtbKaObJyeu_in_lsb(qzRBoUrJHnaWhEQyzAbw, GcnwUmRVencQYyYPtXmL.SrTQnYWFmoofiDcjyLXs, GcnwUmRVencQYyYPtXmL.IcnwkMhDBwqClbkzXNxz);
            OJKLHASFk23_vSBrFLJcJWtbKaObJyeu(qzRBoUrJHnaWhEQyzAbw, GcnwUmRVencQYyYPtXmL.SrTQnYWFmoofiDcjyLXs, GcnwUmRVencQYyYPtXmL.IcnwkMhDBwqClbkzXNxz);
```
Maybe the obfuscated symbols are generated in a systematic way and it's possible to recover the original symbols, but I just started reversing instead of trying to figure it out. Curiously some of the error messages are also garbled.

First we see that it reads in the message and input BMP image. Here it helps to rename at least some of the fields in the BMP header struct, which is easily done with the help of some BMP file format docs. Then comes all the stego stuff. Some of the functions loop through the image pixels and does something to the lower bits of each pixel, some functions process the message in some way. Below is all the relevant code from the `main()` function, after reversing and renaming:
```c
    message = read_message(argv[1], &msg_size);
    pixels = read_image(argv[2], &header, &dib_header);
    if ( pixels && msg_size )
    {
        clear_lsb(pixels, dib_header.width, dib_header.height);
        generate_random_in_lsb(pixels, dib_header.width, dib_header.height);
        set_bit2(pixels, dib_header.width, dib_header.height);
        swap_data(message, msg_size);
        shuffle_bits(message);
        seed_rand();
        msg_size_div_3 = (int)msg_size / 3;
        msg_size_mod_3 = msg_size % 3;
        initial = generate_initial(msg_size, dib_header.width);
        hide(initial, dib_header.width, dib_header.height, message, msg_size_div_3, pixels, 0);
        width = dib_header.width;
        rand_val_0 = rand();
        initial = generate_initial(rand_val_0, width);
        hide(initial, dib_header.width, dib_header.height, &message[msg_size_div_3], msg_size_div_3, pixels, 1);
        v10 = dib_header.width;
        rand_val = rand();
        initial = generate_initial(rand_val, v10);
        hide(initial, dib_header.width, dib_header.height, &message[2 * msg_size_div_3], msg_size_div_3 + msg_size_mod_3, pixels, 2);
        write_image(argv[3], &header, &dib_header, pixels);
        free(pixels);
        return 0;
    }
```
The function `clear_lsb()` does the obvious thing, setting all LSBs to zero. `generate_random_in_lsb()` generates random bits for the LSBs and ORs them in. `set_bit2()` sets all the second to least significant bits (bit 2 if LSB is bit 1) to some hardcoded values. This will come into play later when the actual message bits are hidden.

`swap_data()` shuffles the message bytes around according to an LCG function:
```c
    for ( i = size - 1; i; --i )
    {
        lcg_val = lcg(&size_);
        j = lcg_val % (i + 1);
        indices[i] = j;
        temp = data[i];
        data[i] = data[j];
        data[j] = temp;
    }
```
(The indices array is not used anywhere.) Note that the size of the message is used as seed for the LCG. The `lcg()` function looks like this:
```c
uint32_t __cdecl lcg(uint32_t *state)
{
    *state = (0x41C64E6D * *state + 0x3039) % 0x7FFFFFFF;
    return *state;
}
```

The `shuffle_bits()` function moves the bits in each byte around, with the following loop:
```c
    for ( i = 0; data[i]; ++i )
        data[i] = (4 * data[i]) & 0x30 | ((int)data[i] >> 2) & 0xC | (data[i] << 6) | (data[i] >> 6);
```
It reverses the position of pairs of bits in a byte, so we can just apply it again to undo it. `seed_rand()` reads a seed from `/dev/urandom` and calls `srandom()` on it.

Then we see the message is divided into 3 parts of equal size (the last part might be a bit bigger if the size is not divisible by 3), and `generate_initial()` and `hide()` called for each part. Finally the resulting image is written out.

The `generate_initial()` function generates a sequences of bits:
```c
int *__cdecl generate_initial(uint32_t init_val, int width)
{
    [...]

        for ( i = 0; i < width; ++i )
        {
            bits[i] = init_val & 1;
            init_val = (init_val >> 1) ^ -(init_val & 1) & 0xB400;
        }
        return bits;

    [...]
}
```
This is a Galois LFSR, but it's not necessary to know that to solve the challenge. The generated bits (called `initial` in the code) are passed to the `hide()` function, along with the message and the image pixels so far. The last argument chooses an RGB component to hide the bits in. We see that different components are used for the three message parts.

Now for the last and most complex function:
```c
void __cdecl hide(int *initial, int width, int height, unsigned __int8 *data, __int64 data_len, unsigned __int8 *pixels, int rgb_pos)
{
    [...]

    write_init_lsb(initial, width, height, pixels, rgb_pos);
    for ( i = 0; i < width; ++i )
        current[i] = initial[i];
    for ( y = 1; y < height; ++y )
    {
        for ( i_0 = 1; i_0 < width - 1; ++i_0 )
            next[i_0] = current[i_0 - 1] ^ current[i_0 + 1];
        for ( i_1 = 0; i_1 < width; ++i_1 )
            current[i_1] = next[i_1];
        hide_line(current, y, width, height, data, data_num_bits, pixels, rgb_pos, &cur_bit_pos);
        if ( data_num_bits <= cur_bit_pos )
        {
            done = 1;
            break;
        }
    }

    [...]
}
```
The `write_init_lsb()` call just writes the bits from `inital` to the LSBs of the first line in the image. Thus we can easily recover the bits in `initial` by reading out the LSBs of the first line in the given output image.

Then a `current` array is initialized to the valus in `initial`. Now it loops through all lines in the image, but skips the first line since that is already used to store the initial bits. It then generates a new sequence of bits for this line, by XORing the two bits to the left and right in the previous line. Then these bits and all the other stuff are then passed to `hide_line()` function.

```c
void __cdecl hide_line(int *bits, int y, int width, int height, unsigned __int8 *data, __int64 num_bits, unsigned __int8 *pixels, int rgb_pos, int *cur_bit_pos)
{
    [...]

    for ( x = 0; x < width; ++x )
    {
        pixel_pos = 3 * (x + width * (height - 1 - y));
        if ( (pixels[pixel_pos + 2 - rgb_pos] & 2) != 0 && bits[x] == 1 )
        {
            bit = get_bit(data, *cur_bit_pos);
            ++*cur_bit_pos;
            if ( bit )
                pixels[pixel_pos + rgb_pos] |= 1u;
            else
                pixels[pixel_pos + rgb_pos] &= ~1u;
            if ( num_bits <= *cur_bit_pos )
                break;
        }
    }
}
```
Finally in `hide_line()` the message bits are written to the image. It loops through each pixel in the specified line, then it checks both the existing bit 2 values in the image (remember those were set to hardcoded values earlier), and the bits that trickled down from the LFSR. If both are set, then we write a message bit to the LSB. An important detail here is that it reverses the order of the RGB component used when it checks the bit 2 values. This is confusing, since the component order is already reversed because of BMP being BMP. Also the image is upside down for the same reason.

So to recover the message bits, we need to recover the LFSR bits in `initial`, which we get from the LSBs of the first line in the image. Then we can generate the same bit sequence by XORing as in the code above. We also need bit 2 from each pixel. Then we need to deal with the shuffling and swapping of message bits/bytes from the `swap_data()` and `shuffle_bits` functions.

Let's first find the length of the hidden message. Since it's used as the LFSR state for the first part of the message, we can brute force it and compare the output from the LFSR with what we read in from the first line of the image.
```python
from itertools import *
from PIL import Image

def lfsr(state):
    while True:
        yield state & 1
        state = (state >> 1) ^ ((-(state & 1)) & 0xB400)

im = Image.open("julekort.bmp")
pix = im.load()
lsbs = [pix[x,0][2] & 1 for x in range(im.width)]

for msg_len in range(10000):
    bits = islice(lfsr(msg_len), im.width)
    if list(bits) == lsbs:
        print(msg_len)
        exit()
```
We find that the message length (in bytes) is 1135. So the three message parts are of length 378, 378, and 379.

Now we have all we need to write a solve script. One thing that had me stuck for a while during the compeition was the `lcg()` function, where I didn't mask out the lower 32 bits before doing the modulo 0x7FFFFFFF...

```python
from PIL import Image

im = Image.open("julekort.bmp")
pix = im.load()

msg_len = 1135
msg_part1_len = 378
msg_part2_len = 378
msg_part3_len = 379

def recover_msg_bits(msg_part_len, rgb_comp):
    msg_bits = []
    noise_bits = [pix[x,0][rgb_comp] & 1 for x in range(im.width)]

    y = 1
    while True:
        noise_bits = [0] + [noise_bits[x-1] ^ noise_bits[x+1] for x in range(1, im.width-1)] + [0]
        for x in range(im.width):
            lsb = pix[x,y][rgb_comp] & 1
            bit2 = pix[x,y][2-rgb_comp] & 2
            if bit2 == 2 and noise_bits[x] == 1:
                msg_bits.append(lsb)
                if len(msg_bits) == msg_part_len * 8:
                    return msg_bits
        y += 1

msg_bits = recover_msg_bits(msg_part1_len, 2)
msg_bits += recover_msg_bits(msg_part2_len, 1)
msg_bits += recover_msg_bits(msg_part3_len, 0)

def unshuffle_bits(val):
    return (val << 2) & 0x30 | (val >> 2) & 0xC | (val << 6) & 0xff | (val >> 6)

msg = [int("".join(map(str,msg_bits[i:i+8][::-1])), 2) for i in range(0, len(msg_bits), 8)]
for i in range(len(msg)):
    msg[i] = unshuffle_bits(msg[i])

def lcg(state):
    return (((0x41C64E6D * state)&0xffff_ffff) + 0x3039) % 0x7FFFFFFF

state = msg_len
swaps = []
for i in range(msg_len-1, -1, -1):
    state = lcg(state)
    j = state % (i+1)
    swaps.append((i,j))

for i,j in swaps[::-1]:
    msg[i], msg[j] = msg[j], msg[i]

print(bytes(msg))
```
The resulting message is Lorem ipsum with the flag placed somewhere in the middle:
```
...
Suspendisse sit amet sapien varius tortor sollicitudin mollis nec sit amet sapien. EPT{god_hjul1!}  Aenean non eleifend nulla. Nullam quis posuere nisi, ut sollicitudin urna. Quisque et mollis ipsum.
...
```
