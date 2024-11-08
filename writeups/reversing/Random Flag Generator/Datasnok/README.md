# Writeup for Random Flag Generator
By seal (seal524)

## Description
Category: Reversing
```
This challenge is intened to be an introduction to java.

`java -jar` to run the program, see if you can find a flag in there somewhere.
```
## Solution
To start with try to decompile the .jar file provided with the challenge. To do that simply google java decompiler online and pick one. I used [javadecompilers.com](http://www.javadecompilers.com/) and got the [RandomFlagGenerator.java](RandomFlagGenerator.java) file.

In the file there are two especially interesting functions `main()` and `xorString()`: 
```
import java.util.Base64;
import java.util.Random;
import java.util.Base64.Decoder;
import java.util.Base64.Encoder;

public class RandomFlagGenerator {
   public static void main(String[] var0) {
      String var1 = "ATU6Wy9BFBMqCCsXMVQNRT0lRABlGA==";
      String var2 = "Den e brun";
      String var3 = xorString(base64Decode(var1), var2);
      String var4 = generateRandomString(20, var3);
      System.out.println("Random Flag: " + var4);
   }

   public static String generateRandomString(int var0, String var1) {
      String var2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz" + var1;
      Random var3 = new Random();
      StringBuilder var4 = new StringBuilder(var0);

      for(int var5 = 0; var5 < var0; ++var5) {
         var4.append(var2.charAt(var3.nextInt(var2.length())));
      }

      return var4.toString();
   }

   public static String xorString(String var0, String var1) {
      StringBuilder var2 = new StringBuilder();

      for(int var3 = 0; var3 < var0.length(); ++var3) {
         var2.append((char)(var0.charAt(var3) ^ var1.charAt(var3 % var1.length())));
      }

      return var2.toString();
   }

   public static String base64Encode(String var0) {
      Encoder var1 = Base64.getEncoder();
      return var1.encodeToString(var0.getBytes());
   }

   public static String base64Decode(String var0) {
      Decoder var1 = Base64.getDecoder();
      return new String(var1.decode(var0));
   }
}

```

In `main()` we see that `var1` is base64 decoded, and then is xored with `var2`. After that there is created a random string that is outputted.

I assume that the flag is `var1` xored with `var2`. In order to do this I created a [solve script](solve.py) in python:

```
import base64 

message =  "ATU6Wy9BFBMqCCsXMVQNRT0lRABlGA=="
message = base64.b64decode(message)

xor = "Den e brun"


flag = ""

for i in range(len(message)):
    flag += chr((message[i])^ord(xor[i % len(xor)]))

print(flag)
```

Flag: `EPT{Java_for_the_W1n!}`