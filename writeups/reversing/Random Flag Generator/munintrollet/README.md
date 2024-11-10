**Author: Zukane**

*This challenge is intened to be an introduction to java.*
*`java -jar` to run the program, see if you can find a flag in there somewhere.*

##### Challenge overview

In this reversing challenge we are given a jar file named `RandomFlagGenerator.jar`. I tried running the jar file, but had some version issues:

```
└─$ java -jar RandomFlagGenerator.jar                                                                                                                                                                                     
Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
Error: LinkageError occurred while loading main class RandomFlagGenerator
        java.lang.UnsupportedClassVersionError: RandomFlagGenerator has been compiled by a more recent version of the Java Runtime (class file version 65.0), this version of the Java Runtime only recognizes class file versions up to 61.0
```

Because I am lazy, I just jump straight to the reversing instead.

Using the tool `procyon` we can extract the ``.java`` source-code files from the compiled ``.jar`` file. 

```
└─$ procyon RandomFlagGenerator.jar -o program.java/
Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
Decompiling RandomFlagGenerator...
```

The `jar` file contained only a single ``RandomFlagGenerator.java`` file:

```java
import java.util.Base64;
import java.util.Random;

// 
// Decompiled by Procyon v0.6.0
// 

public class RandomFlagGenerator
{
    public static void main(final String[] array) {
        System.out.println("Random Flag: " + generateRandomString(20, xorString(base64Decode("ATU6Wy9BFBMqCCsXMVQNRT0lRABlGA=="), "Den e brun")));
    }
    
    public static String generateRandomString(final int capacity, final String s) {
        final String s2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz" + s;
        final Random random = new Random();
        final StringBuilder sb = new StringBuilder(capacity);
        for (int i = 0; i < capacity; ++i) {
            sb.append(s2.charAt(random.nextInt(s2.length())));
        }
        return sb.toString();
    }
    
    public static String xorString(final String s, final String s2) {
        final StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); ++i) {
            sb.append((char)(s.charAt(i) ^ s2.charAt(i % s2.length())));
        }
        return sb.toString();
    }
    
    public static String base64Encode(final String s) {
        return Base64.getEncoder().encodeToString(s.getBytes());
    }
    
    public static String base64Decode(final String src) {
        return new String(Base64.getDecoder().decode(src));
    }
}
```

##### Solution

RandomFlagGenerator.java contains a function  for generating a random string, a helper function for XORing strings and helper functions for base64 encoding and decoding. 
The main function makes a call to the `generateRandomString` function with a capacity of 20, and presumable the flag. The interesting part is

```java
xorString(base64Decode("ATU6Wy9BFBMqCCsXMVQNRT0lRABlGA=="), "Den e brun")
```

We can use a simple python script to recover the string:

```python
from pwn import xor
import base64

print(xor(base64.b64decode("ATU6Wy9BFBMqCCsXMVQNRT0lRABlGA=="), "Den e brun").decode())
```

Running this gives us the flag:

```
└─$ python solve.py
EPT{Java_for_the_W1n!}
```

