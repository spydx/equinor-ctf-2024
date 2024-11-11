# Random Flag Generator

## Description
This challenge is intened to be an introduction to java.

`java -jar` to run the program, see if you can find a flag in there somewhere.


## Solution
I use [JADX](https://github.com/skylot/jadx) to decompile the java code to see what it does. The new ctf meta is of course to use chatgpt to solve the challenge.

**ME>**  
How can i reverse the flag?
```java
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

**CHATGPT>**  
Here’s a Python script that performs the equivalent operations to reveal the flag:  
```python
import base64

# Step 1: Decode the Base64 string
encoded_string = "ATU6Wy9BFBMqCCsXMVQNRT0lRABlGA=="
decoded_string = base64.b64decode(encoded_string).decode('utf-8')

# Step 2: XOR the decoded string with "Den e brun" to retrieve the flag
xor_key = "Den e brun"
flag = ''.join(chr(ord(decoded_string[i]) ^ ord(xor_key[i % len(xor_key)])) for i in range(len(decoded_string)))

print("Original Flag:", flag)
```
Which when run gives the flag:  
`Original Flag: EPT{Java_for_the_W1n!}`
