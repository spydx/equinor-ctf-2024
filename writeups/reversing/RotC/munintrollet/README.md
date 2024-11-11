**Author: Zukane**

*Just let me rotate.*

##### Challenge overview

In this reversing challenge, we are given an executable file named ``rot_C``. By running this program, we are given an "encrypted" flag and we are prompted for a rotation amount.  

```
└─$ ./rot_C
Original string: LWA{z0_tBjo_y0aha3_pu_ao4a_z7y1un}
Enter rotation amount: 2
👎 That does not look like the start of a flag to me. 👎
Rotated string: NYC{b0_vDl
```

The program does not print the entire flag, but we can try inputting the correct rotation amount:

```
└─$ ./rot_C
Original string: LWA{z0_tBjo_y0aha3_pu_ao4a_z7y1un}
Enter rotation amount: 19
Not allowed!
```

Looks like it is CyberChef time

##### Solution

By simply using the ROT13 recipe with an amount of 19, we get the flag:

`EPT{s0_mUch_r0tat3_in_th4t_s7r1ng}`
