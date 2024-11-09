import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import sys
from pathlib import Path
import json
import re

aes_key=base64.b64decode("nKOUoSsKsktfVHw92oRnK79V5/JA9TP3VKrJD+uWU9Y=")


def new_aes_key(session_key):
    global aes_key
    priv_key = RSA.import_key(open("rsa_key.pem").read())
    cipher_rsa = PKCS1_OAEP.new(priv_key)
    new_session_key = cipher_rsa.decrypt(base64.b64decode(session_key))
    aes_key = new_session_key

    

def aes_decrypt(payload: str):
    payload_decoded = base64.b64decode(payload)

    uuid=payload_decoded[0:36]
    rest = payload_decoded[36:]


    cipher = AES.new(aes_key, AES.MODE_CBC, iv=rest[:16])
    plain = cipher.decrypt(rest[16:-32])
    plain = plain.replace(b"\r", b"")
    plain = plain.replace(b"\x0c", b"")
    plain = plain.replace(b"\x0f", b"")
    plain = plain.replace(b"\x10'", b"")
    plain = plain.decode("utf-8")
    try:
        plain_json = json.loads(plain)
    except:
        return plain
    session_key = plain_json.get("session_key", None)
    if session_key:
        new_aes_key(session_key)
    #return plain_json
    return plain

def main() -> None:
    with Path.open("c2.txt", "r") as f:
        for line in f.readlines():
            if line.startswith("HTTP") \
                or line.startswith("POST")  \
                or line.startswith("User-Agent") \
                or line.startswith("Host") \
                or line.startswith("Content-Length") \
                or line.startswith("Connection") \
                or line.startswith("Expect") \
                or line.startswith("Content-Type") \
                or line.startswith("Transfer-Encoding") \
                or line.startswith("Date"):
                continue
            if len(line) < 2:
                continue
            line = line.replace("HTTP/1.1 200 OK", "")
            line = line.replace("HTTP/1.1 100 Continue", "")
            print(aes_decrypt(line))
    

if __name__ == "__main__":
    main()
