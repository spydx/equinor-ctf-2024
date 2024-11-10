# Writeup
by Kinje

## Solution
Converting the colors on the wall to hex, and then converting that to plain text, which gave us the flag.

## Explanation
At the top there were 16 different colors, that stayed still for the whole duration.
The colors below came together 2 and 2, and were going for about a minute.

![Skjermbilde 2024-11-10 210320](https://github.com/user-attachments/assets/61813aff-474f-4dd7-9ce1-5e96ed39123a)

Seeing that there were 16 colors at the top, and how the colors came in pairs, we began to think that they had to be hexadecimal numbers. 
We figured that the ones standing still at the top would have to indicate what number or letter they would have to be. Starting from the left, noting them down as 0-9 and A-F.

https://github.com/user-attachments/assets/a5e6d9a7-9a58-474c-96af-7c79f5f5f556

By noting down the rotating colors, and connecting them to the colors at the top, we got alot of hexadecimal numbers.
Putting them into a hexadecimal to plain text converter, we got something along the lines of;
"This is the flag: EPT{c0l0r_m3_h4ppy}"
