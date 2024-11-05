import binascii

def xor_hex_strings(hex1, hex2):
    # Convert hex strings to bytes
    bytes1 = binascii.unhexlify(hex1)
    bytes2 = binascii.unhexlify(hex2)
    
    # XOR the bytes
    xored_bytes = bytes([b1 ^ b2 for b1, b2 in zip(bytes1, bytes2)])
    
    # Convert the result back to a hex string
    return binascii.hexlify(xored_bytes).decode()

# Known plaintext 1
plaintext1 = "Always use the one master OTP for all secure communications, it is uncrackable. Now listen carefully"
plaintext1_hex = binascii.hexlify(plaintext1.encode()).decode()

# Intercepted ciphertext 1 (hex)
ciphertext1 = "c607eea76fc53ada95c9e7321434c264822158f8cc8ae2517deb4cf1ef6687bb4eecff4ac57c5bfcb1f39d5265d89a5e451171f2e3e1d3ffd8916f328e1ea7b3b073466a7e8eb7b56255051de269996654b85254cff2e49b71faec792c908d318ad42c1d"

# Derive the key by XORing plaintext1 and ciphertext1
key = xor_hex_strings(plaintext1_hex, ciphertext1)

# Intercepted ciphertext 2 (hex)
ciphertext2 = "cb02f4af629663c093dee72b1922916a8b210bb5d996b6053ffb60cdde3492f448a3be40c02808edbae3cf5a24c881565a4450cfd0ae87d8d8883c6bdd12f3e7b169153f6388a6a6644a5e5fcb5ce33d6de4491793f6a4b060a4937734bd8325ceda6119"

plaintext2 = binascii.unhexlify(xor_hex_strings(ciphertext2, key)).decode()

print(plaintext2)