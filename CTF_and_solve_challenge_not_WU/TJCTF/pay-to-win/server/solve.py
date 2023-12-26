from flask import Flask, request, render_template, redirect, make_response
from base64 import b64encode, b64decode
import hashlib
import random
import json
import itertools


def hash(data):
    return hashlib.sha256(bytes(data, 'utf-8')).hexdigest()


data = {
    "username": "admin",
    "user_type": "premium"
}
b64data = b64encode(json.dumps(data).encode())
data_hash = hash(b64data.decode() + "cc1f79")
print(data_hash)

# print(b64data)
# # print(type(hex(random.getrandbits(24))[2:]))

# str_1 = b"eyJ1c2VybmFtZSI6ICJhZG1pbiIsICJ1c2VyX3R5cGUiOiAiYmFzaWMifQ=="

# # print(str_1.decode())

# characters = "0123456789ABCDEFabcdef"
# hex_strings = [''.join(chars)
#                for chars in itertools.product(characters, repeat=6)]
# for hex_str in hex_strings:
#     key = str_1.decode()+hex_str
#     res = hash(key)
#     if res == "1af835e5354b1eabb67dfe7df8818f7377f4c83066de39ad3187fd8035f84cb7":
#         print(hex_str)
#         break
