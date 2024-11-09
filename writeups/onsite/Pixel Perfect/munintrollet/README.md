At 12 o'clock the the CTF hosts put us on out first knifes edge of the day. They served lunch at the same time as they released the fire challenges... We did as anny proud CTF player would, and chose the fire challenges. Food could wait another 8 hours. We put our heads down.

Task:
`Something in your surroundings just changed. What?!`

We lifted our heads back up. What had changed? @Tuxeren had the correct angle and instantly spotted moving lights apearing on the wall. 

We started looking into how text could be hidden in colour combinations. Our research indicated that "Gravity falls colour" was a plausible way to get text from colour. This was a rabbithole we do not recommend looking into..

Then we noticed the top row of lights were not moving. 16 different lights not moving with two and two light moving across the wall...The top row could represents 0-16 value. A pair of 0-16 values make up a byte... This is encoded as hex values! Lets look to our trusted friend Cyberchief! 

0(Red) - 8(Light blue)
![image1](./Images/Pasted image 20241108232006.png)
9(Orange) - 16(F in hex) (White):
![[Pasted image 20241108232037.png]]

First we wanted to know what we were looking for. What is `EPT{` in hex values?

![[Pasted image 20241108225338.png]]

45 = cyan + light pink
50 = light pink + red
54 = light pink + cyan
7b = pink + deep pink

Next issiue: The lighting sequence does not start with cyan + light pink..
Soulution: Look for first time this combination apears!

From there it was a straight-forward algorithm: Match the lights in sequence to their respective numbers. Do this until you get pink + lime green (7d equals `}` in hex)(It REALLY helps to not use video sent over discord.. This obfuscates the colour clarity)

Solution:
![[Pasted image 20241108231132.png]]

// munintrollet