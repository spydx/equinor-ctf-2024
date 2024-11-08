## BASKETBALL WITH DAD

### Task

In the analysis of the task, we find that this is where all the input is processed, so this is the only part of the code where we can make changes:

```py
if re.match("^[1-3]{1,3}$", inp):
    for c in inp:
        value = {
            "1": 1,
            "2": 2,
            "3": 3
        }.get(c, 1)
        state += value
```

### Solution

The solution is to send a double `\n` at the end of the numbers. This works because the Python code only removes the last `\n` from the string.

```python
if inp and inp[-1] == '\n':
		inp = inp[:-1]
```

Since `$` matches `\n`, the regex check will pass:

```py
if re.match("^[1-3]{1,3}$", inp):
```

But why would we want an extra `\n`? The reason is that `.get(c, 1)` has set a default value of `1`. Therefore, `\n` will cause the code to score an additional point:

```py
for c in inp:
    value = {
        "1": 1,
        "2": 2,
        "3": 3
    }.get(c, 1)
    state += value
```

This results in your shots giving a total of 10 points. Therefore, you can beat **dad**, whose score is 19.

```bash
(echo -n "333\n\n"; cat) | ncat --ssl game.ept.gg 1337
```

```
Each round you get up to 3 shots, each shot is worth up to 3 points.
First one to bring the score to 20 point wins.
You start, and please beat my dad, he has gotten so cocky these last years.

Enter your shots as a series of numbers (max 3)
> The total score is now 10

Dads turn...
Dads shoots...
And he scores! 333

The total score is now 19

Enter your shots as a series of numbers (max 3)
> 1
The total score is now 20

You win! Here are my dads final words to you:
EPT{ ... }
```

<details>
<summary>Flag</summary>

`EPT{l3t_m3_ad0pt_y0u_pl34s3}`
</details>