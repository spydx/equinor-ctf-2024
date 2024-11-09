## Basketball with Dad

### Challenge

The game allows us to take 3 shots, where each shot can be either worth 1, 2 or 3 points. The input format is a series of numbers (max 3). Ex: "111" or "3" or "323" or ...


Our input is passed to this function, which calculates the state/score of the game after the player has entered the numbers
```py
def player_turn(state, inp):
	if inp and inp[-1] == '\n':
		inp = inp[:-1]
	
	if re.match("^[1-3]{1,3}$", inp):
		for c in inp:
			value = {
				"1": 1,
				"2": 2,
				"3": 3
			}.get(c, 1)
			state += value
	else:
		return -1
	
	return state
```

The input is ran through a regex match to see if it is in the format `^[1-3]{1,3}$`. 
Before the input is checked with the regex, the input is truncted by 1 character if the last character is a newline. If the input is for example "232\n". The input becomes "232". 
The problem is if we input 2 newlines after the numbers. Then an input like this: "232\n\n" will become "232\n". This doesn't seem like a big deal, but the `re.match()` method will still match if the input ends with a newline. 

Our goal is to score 10 on our first turn. This will force a win because Dad can only play a maximum of 9 points. Therefore we can simply play 1 on our last turn and win the game.
To accomplish this, we can input "333\n\n". 

After the check below, the input will look like this: "333\n".
```py
if inp and inp[-1] == '\n':
		inp = inp[:-1]
```

The input "333\n" will match this pattern and enter the if test.
```py
if re.match("^[1-3]{1,3}$", inp):
```

The input is then looped through and added to the state/score variable. When this for loop loops over "333\n", it will find the string "3" in the dictionary "value" and extract the value 3 from that key. But when the for loop reaches the newline character, it won't find it in the dictionary, and it will therefore use its default value: 1. The sum will therefore be `3+3+3+1 = 10`
```py
for c in inp:
    value = {
        "1": 1,
        "2": 2,
        "3": 3
    }.get(c, 1)
    state += value
```


```
$ python3 solve.py
[+] Opening connection to game.ept.gg on port 1337: Done
[*] Switching to interactive mode
The total score is now 20

You win! Here are my dads final words to you: EPT{l3t_m3_ad0pt_y0u_pl34s3}
```


### Solve script
```py
from pwn import *

io = remote("game.ept.gg", 1337, ssl=True)

io.recvuntil(b"> ")

io.send(b"333\x0a\x0a")

io.recvuntil(b"> ")
io.send(b"1")

io.interactive()
```