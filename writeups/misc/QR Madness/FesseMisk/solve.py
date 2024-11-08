import cv2
from pyzbar.pyzbar import decode

# Example usage
image = cv2.imread("qr.png")

result = ""

for qrcode in reversed(decode(image)):
    result += qrcode.data.decode("utf-8").replace("https://127.0.0.1/", "")

print(result)