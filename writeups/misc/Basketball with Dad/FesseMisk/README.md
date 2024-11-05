## BASKETBALL WITH DAD

### Oppgave

I analysen av oppgaven finner vi at det er her alt av inndata blir behandlet, så det er bare denne delen av koden vi kan gjøre noe med:

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
        
### Løsning

Løsningen er å sende dobbel `\n` på slutten av tallene. Dette fungerer fordi pythoncoden kun fjerner den siste \n fra stringen.

```python
if inp and inp[-1] == '\n':
		inp = inp[:-1]
```

Siden `$` matcher `\n` vil du passere regexsjekken:

```py
if re.match("^[1-3]{1,3}$", inp):
```

Men hvorfor vil vi ha med en ekstra `\n`? Jo det er fordi `.get(c, 1)` har angitt en default verdi, `1`. Derfor vil `\n` føre til at vi scorer ett ekstra poeng:

```py
for c in inp:
    value = {
        "1": 1,
        "2": 2,
        "3": 3
    }.get(c, 1)
    state += value
```

Dette gjør at dine skudd gir totalt 10 poeng. Derfor klarer du å slå **dad** når han skyter scoren opp til 19.

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
```


<details>
<summary>Flagg</summary>

`EPT{l3t_m3_ad0pt_y0u_pl34s3}`
</details>