import requests
from base64 import b64decode
from base64 import b64encode


ADDRESS = "http://mercury.picoctf.net:10868/"

s = requests.Session()
s.get(ADDRESS)
cookie = s.cookies["auth_name"]
decoded_cookie = b64decode(cookie)
raw_cookie = decoded_cookie


def exploit():
    for position_idx in range(0, len(raw_cookie)):
        for bit_idx in range(0, 8):
            bitflip_guess = (
                raw_cookie[0:position_idx]
                + ((raw_cookie[position_idx] ^
                   (1 << bit_idx)).to_bytes(1, "big"))
                + raw_cookie[position_idx + 1:]
            )
            guess = b64encode(bitflip_guess).decode()
            r = requests.get(ADDRESS, cookies={"auth_name": guess})
            if "picoCTF{" in r.text:
                print("Flag: " + r.text.split("<code>")[1].split("</code>")[0])
                return


exploit()
