# Basketball CTF Challenge Writeup

**Solved by:** Covey

## Analysis of the Game Logic

Upon examining the `game.py` file, this is what we noted as areas of interest:

1. The game uses a state variable to keep track of the total score.
2. The player's input is validated using a regex pattern `^[1-3]{1,3}$`.
3. Dad's turn is implemented to always make optimal moves towards the next multiple of 10.

## Vulnerability

After an initial exploration phase, trying to identify possible attack vectors, we concluded that the regex guard was our best (and only?) shot at defeating Dad's seemingly unbeatable strategy.

The vulnerability in this challenge is a combination of two things:

1. A minor flaw in the regex pattern
2. The inclusion of a default value in case of "invalid input".

Let's take a look at the regex pattern first. The symbols `^` and `$` marks the beginning and end of a string. 
The start of a string is pretty straight forward, we think, but the end of a string however is a little bit more ambiguous - when exactly does a string end? Heres a few ways we could think of:

```python
"Hello, World!"  # No more characters - string ends with a "!"
"Hello, World!\x00"  # In C there's the null byte
"Hello, World!\n"  # How about a new line?
"Hello, Windows!\r\n"  # More new lines?
```

Of the above examples, adding a simple `\n` at the end of the string will still pass the regex check for "end-of-string". 

For the second vulnerability, lets take a look at the code snippet that handles the player's input:

```python
if re.match("^[1-3]{1,3}$", inp):
    for c in inp:
        value = {
            "1": 1,
            "2": 2,
            "3": 3
        }.get(c, 1)
        state += value
```

If we manage to escape the regex check, every character in the input string will score us points; `1`, `2` and `3` will each score their repective value, and any other character will default to a score of 1.

## Exploitation

The exploit takes advantage of the two vulnerabilities mentioned above.

1. We send the string `"333\n"` as our first move. This string passes the regex check but also contains a newline character.
2. When scoring, 9 points are added from the `"333"` and 1 point is added from the newline character - totalling 10 points.
3. Dad will try to get as close as he can to the _next_ multiple of 10, which in this case is 20. However - he does not know about the neat "newline trick" we used, so he will only be able to score 9 points by sending `"333"`.
4. The total score is now 19, and we only need to score 1 more point to win! So we send: `"1"`, bringing the total to 20.

## Flag

Upon successfully exploiting the vulnerability and winning the game, the server responds with the flag:
> `You win! Here are my dads final words to you: EPT{l3t_m3_ad0pt_y0u_pl34s3}`
