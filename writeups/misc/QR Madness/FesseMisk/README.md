## QR MADNESS

We are given a large image with many QR codes. 10 in width, and very many in height.

From the image size **3300x32670**, I can deduce that there are 10x100 QR codes.

Scanning the first one, we are sent to: `https://127.0.0.1/A`

### Solution

The solution is to use `pyzbar` to read the QR codes. It reads all the QR codes in the image, so there is no need to split the image into parts.

By looping through all the codes and concatenating the result, we get a long string of text. I understand that `pyzbar` has read all the codes in reverse order, so I add a `reversed` in the `for` loop:

```bash
sudo apt-get install libzbar0
pip install pyzbar
```

```python
import cv2
from pyzbar.pyzbar import decode

# Example usage
image = cv2.imread("handout/qr.png")

result = ""

for qrcode in reversed(decode(image)):
    result += qrcode.data.decode("utf-8").replace("https://127.0.0.1/", "")

print(result)
```

The script gives a long string, and we also find the flag:

```
AQRcodeisatypeoftwo-dimensionalmatrixbarcode,inventedin1994,byJapan ... EPT{***} ... identification,time
```

<details>
<summary>Flag</summary>

`EPT{QR_qu3st_0wn3d_2024}`
</details>