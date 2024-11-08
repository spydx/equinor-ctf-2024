## QR MADNESS

Vi blir gitt et stort bilde med mange qr koder. 10 i bredden, og veldig mange i høyden.

Fra bildestørrelsen **3300x32670** ser jeg at det må være 10x100 qrkoder.

Scanner vi den første blir vi sendt til får vi opp: `https://127.0.0.1/A`

### Løsning

Løsningen blir å bruke pyzbar for å lese qrkodene. Den leser alle qrkoder i bildet, så det er ikke nødvendig å splitte bildet opp i biter.

Looper vi gjennom alle kodene og setter sammen svaret får vi en lang streng med tekst. Jeg forstår at pyzbar har lest alle kodene i baklengs rekkefølge, derfor legger jeg til en reversed i for-loopen:

```bash
sudo apt-get install libzbar0
pip install pyzbar
```
```py
import cv2
from pyzbar.pyzbar import decode

# Example usage
image = cv2.imread("handout/qr.png")

result = ""

for qrcode in reversed(decode(image)):
    result += qrcode.data.decode("utf-8").replace("https://127.0.0.1/", "")

print(result)
```

Scriptet gir en lang streng, der vi også finner flagget:

```
AQRcodeisatypeoftwo-dimensionalmatrixbarcode,inventedin1994,byJapan ... EPT{***} ... identification,time
```

<details>
<summary>Flagg</summary>

`EPT{QR_qu3st_0wn3d_2024}`
</details>