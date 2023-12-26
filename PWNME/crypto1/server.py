from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import itertools


FLAG = "PWNME{redacted}"
KEY = os.urandom(16)
# string1 = '0123456789abcdefghijklmnopqrstuvwxyz'


# def encrypt_flag():
#     iv = os.urandom(16)
#     cipher = AES.new(KEY, AES.MODE_CBC, iv)
#     encrypted = cipher.encrypt(pad(FLAG.encode(), 16))
#     signature = [hex(a ^ b)[2:].zfill(2) for a, b in zip(iv, KEY[::-1])]
#     signature = "".join(signature)
#     ciphertext = iv.hex()[4:] + encrypted.hex() + signature
#     return {"ciphertext": ciphertext}


def decrypt_flag():
    ciphertext = "a37b8ab32e581d2615359cc7858e966090d328df2be8b5ad889561d9abce6f961fe03a95a2051e882db2373b33b5a43a1c13ff62af7f835df3cc1ccc64571e74"
    ciphertext = bytes.fromhex(ciphertext)
    iv = "ca92b5919084c02658a2e3d57ee3"
    signature = "f8b84587c727d56c4d37983e7b80ce3c"
    signature = bytes.fromhex(signature)
    for i in range(65536):
        s = hex(i)[2:].zfill(4)
        s += iv
        s = bytes.fromhex(s)
        key = [hex(a ^ b)[2:].zfill(2)
               for a, b in zip(s, signature)]
        key = key[::-1]
        key = "".join(key)

        key = bytes.fromhex(key)
        cipher = AES.new(key, AES.MODE_CBC, s)
        plaintext = cipher.decrypt(ciphertext)
        if b'PWNME{' in plaintext:
            print(plaintext)
            exit


decrypt_flag()
# # ....ca92b5919084c02658a2e3d57ee3

# # KEY=f8b84587c727d56c4d37983e7b80ce3c
