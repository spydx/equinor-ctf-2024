import base64 

message =  "ATU6Wy9BFBMqCCsXMVQNRT0lRABlGA=="
message = base64.b64decode(message)

xor = "Den e brun"


flag = ""

for i in range(len(message)):
    flag += chr((message[i])^ord(xor[i % len(xor)]))

print(flag)

"""
public static String xorString(String var0, String var1) {
      StringBuilder var2 = new StringBuilder();

      for(int var3 = 0; var3 < var0.length(); ++var3) {
         var2.append((char)(var0.charAt(var3) ^ var1.charAt(var3 % var1.length())));
      } 

      return var2.toString();
   }
"""