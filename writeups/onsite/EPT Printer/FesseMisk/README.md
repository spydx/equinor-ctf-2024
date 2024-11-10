## EPT PRINTER

### Task

EPT Print was a printing service with a Flask backend. Completed documents could be printed on-site.

To use the printer, users needed to be verified first. In addition to the Flask server, a bot ran a headless browser to open and review these applications without approving them.

The printing lets us insert text into a LaTeX template that gets sent to the printer.

### Solution

First, we need to get approved to use the printer. We can achieve this by injecting XSS. The code actually hints us about it through comments in the source code in `/webapp/app/__init__.py`:

![Comment in code](image.png)

We use XSS to automatically approve our application:

```html
<img src="x" onerror="document.getElementById('submit').click();">
```

We are now approved, and we can now use the printer. To get the flag we can exploit the fact that we can write LaTeX in order to read a potential flag file:

```latex
\begingroup
\catcode`\%=12
\catcode`\_=12
\input{/flag.txt}
\endgroup
```

`\input{/flag.txt}` loads he content of `/flag.txt` as LaTeX. But since the flag file most probably just contains the flag, we dont want it to compile as LaTeX. Therefore we use `\catcode`\%=12` and `\catcode`\_=12`. These lines are added so that any `%` and `_` characters are not interpreted as LaTeX until printed. This proved necessary because the flag contained `_`.

<details>
<summary>Flag</summary>

`EPT{Y0U_4R3_4_PR1NT3R_M4ST3R}`
</details>