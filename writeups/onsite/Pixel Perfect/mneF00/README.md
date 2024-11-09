# Pixel Perfect
Solved by n0tus and petfly

<video width="320" height="240" controls>
  <source src="pixel_perfect_long.mov" type="video/quicktime">
  Your browser does not support the video tag.
</video>

In a room already filled with fun colors and lights, we saw an interesting sequence of colors move along one of the walls. After admiring the colors on the wall, we soon realized it had to be a hidden message for us to decipher.

Looking at the colors, we noticed a few hints. First, there were 16 colors with a fixed position on top. Second, the moving colors came in pairs of two. This led us to believe that there was a correlation between color and position.

With a numerical system that uses a base of 16, we believed the colors had to point to hexadecimal numbers: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F.

On that assumption, the moving color pairs could make up hex numbers that we could map to the ASCII table to find the flag. We believed the last character in the hidden message would be a “}”. To test this, we looked up the hex number for “}” (7D) and looked at the last color pair in the sequence, and this corresponded to the colors in the position “7” and “D”.
We then had to map all the colors in the sequence to find the flag.

---

This script takes a sequence of color abbreviations, maps each color pair to a set of possible values based on predefined mappings, and uses these to generate characters, which are then printed out to decode the hidden flag.

**Defining Color Codes and Ambiguities:**
- The `colours` list defines possible color abbreviations (e.g., `"re"` for red, `"gr"` for green, etc.).
- The `ambigs` list contains tuples of ambiguous colors, meaning some colors may represent multiple values or be interchangeable.

```python
colours = [
    "re",
    "gr",
    "bl",
    "ye",
    "cy",
    "pi",
    "or",
    "ma",
    "grey",
    "ye2",
    "pu",
    "peach",
    "wh",
    "skog",
    "lg",
    "sand"
]

ambigs = [("ye", "ye2", "sand"), ("lg", "skog", "gr"), ("ma", "pu")]
```


**Input and Pairing:**

- The `elts` list contains a sequence of color codes. This list is paired into tuples in `tups`, where each adjacent pair of elements in `elts` forms a tuple.
- `tups` is created by iterating through `elts` in steps of two, pairing each element with the next one in sequence (e.g., `("ma", "ma")`, `("ye", "re")`, etc.).


```python
elts = ["ma", "ma", "ye", "re", "ye", "re", "ma", "re", "bl", "re", "ma", "ma", "ye", "re", "ye", "re", "ma", "re", "bl", "gr", "bl", "re", "pi", "cy", "or", "wh", "or", "pi", "bl", "re", "or", "or", "or", "wh", "or", "gr", "or", "ma", "bl", "re", "or", "ye", "ma", "ye", "ye", "pu", "re", "bl", "cy", "pi", "pi", "re", "pi", "cy", "pu", "peach", "or", "ye", "pu", "ye", "or", "wh", "ye2", "re", "pu", "bl", "pi", "wh", "or", "lg", "ye", "ye", "pi", "sand", "or", "grey", "ye2", "cy", "ma", "re", "ma", "re", "ma", "ye2", "ma", "skog"]

tups = [(elts[i],elts[i+1]) for i in range(0, len(elts), 2)]
```

**Mapping Colors to Numbers:**

At first, we created a dictionary that mapped each color abbreviation in `colours` to an integer index for easy referencing. However, we soon discovered that we struggled with differentiating between some of the colors, which in turn made it harder to read the flag.  

We therefore created the `colourmap2` dictionary which provides a more detailed mapping where colors can correspond to single integers or multiple possible values (ambiguous colors e.g., `'or'`, `'ye'`), which are mapped to a tuple of values instead of a single integer.

```python
colourmap2 = {
 're': 0,
 'gr': 1,
 'bl': 2,
 'ye': (3, 6, 9, 15),
 'cy': 4,
 'pi': 5,
 'or': (3, 6, 9, 15),
 'ma': (7, 10),
 'grey': 8,
 'ye2': (3, 6, 9, 15),
 'pu': (7, 10),
 'peach': 11,
 'wh': 12,
 'skog': (13, 14),
 'lg': (13, 14),
 'sand': (3, 6, 9, 15)}
```

**Character Decoding:**

The script iterates over each color pair `(a, b)` in `tups`. It retrieves the mapped values for each color from `colourmap2`. If a color maps to multiple values, it converts them into a list for easy handling.

For each combination of values from `a_set` and `b_set` it calculates a character by interpreting the combination as a byte value. The `chr` function converts this byte value into a character, which is then printed out as part of the decoded message.

```python
print(elts)

for a, b in tups:
    a_set = colourmap2[a]
    b_set = colourmap2[b]
    if type(a_set) == int:
        a_set = [a_set]
    if type(b_set) == int:
        b_set = [b_set]


    for i in a_set:
        for k in b_set:
            print(chr(i*16 + k), end=" ")
    print("")
```

**Result:**

The decoded message is printed as characters formed by the color pairs. Each pair of colors maps to one or more possible characters, depending on the ambiguities in `colourmap2`.

-----------------------------------------
w z § ª\
0  ð\
0  ð\
p

w z § ª\
0  ð\
0  ð\
p\
!

T\
< l  ü\
5 e  õ

3 6 9 ? c f i o     ó ö ù ÿ\
< l  ü\
1 a  ñ\
7 : g j   ÷ ú

3 6 9 ? c f i o     ó ö ù ÿ\
s v y  £ ¦ © ¯\
7 : g j   ÷ ú

<b style="color:red;">E</b>\
<b style="color:red;">P</b>\
<b style="color:red;">T</b>\
<b style="color:red;">{</b> «\
3 6 9 ? <b style="color:red;">c</b> f i o     ó ö ù ÿ\
s v y  £ ¦ © ¯\
< <b style="color:red;">l</b>  ü\
<b style="color:red;">0</b> `  ð\
<b style="color:red;">r</b> ¢\
\\\\ \
= > <b style="color:red;">m</b> n   ý þ\
<b style="color:red;">3</b> 6 9 ? c f i o     ó ö ù ÿ\
S V Y <b style="color:red;">_</b>\
8 <b style="color:red;">h</b>  ø\
<b style="color:red;">4</b> d  ô\
<b style="color:red;">p</b>\
<b style="color:red;">p</b>\
s v <b style="color:red;">y</b>  £ ¦ © ¯\
<b style="color:red;">}</b>\ ~ ­ ®

-----------------------------------------
flag: EPT{col0r_m3_h4ppy}