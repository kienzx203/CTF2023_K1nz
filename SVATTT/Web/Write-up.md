# **WU BÀI TẬP VỀ NHÀ**

| IP     | Flag |
| ----------- | ----------- |
| [http://167.172.80.186:2345/index.php?action=home](#bài-về-lỗ-hổng-lfi-và-file-upload)      | `PTITCTF{2b3a6657d4e39d896106c8f8b8be8d34}`       |
| [http://167.172.80.186:9009/](#bài-về-lỗ-hổng-lfi-và-rce-bằng-log-apache)   | `FLAG{L0g_l0g_l0g_d3s3r141i53d}`        |
| [http://167.172.80.186:9011/](#bài-về-lỗ-hổng-ssrf)   | `FLAG{wh4tt-y0u-r-h42k3rr????}`       |
---

## **Bài về lỗ hổng LFI và file upload**

- Như ta đã thấy trang web sử dụng tham số `action` có thể nó điều hướng các trang qua include.

- Em đã thử một số payload ../etc/passwd .... Nhưng dường như không thành công vậy câu hỏi đặt ra là vì sao `home`, `login` đều có thể thực thi được còn payload trên thì không. Em nghĩ có thể do include(path.php) tức là sẽ có đuôi php sau những path.

- Em đã thử payload `php://filter/convert.base64-encode/resource=login` và `home` sau đó decode sang base64 để đọc source code.

![](./img_DT/Screenshot%202023-06-01%20003126.png)

![](./img_DT/Screenshot%202023-06-01%20003405.png)

- Như ta đã thấy để đăng nhập được admin chúng ta phải tìm được `$_SESSION['password']` nhưng `$_SESSION['password']=mt_rand();` Vậy nếu như không có phiên thì `$_SESSION['password']` sẽ rỗng từ đó mình đăng nhập được admin và có chức năng file upload.

![](./img_DT/Screenshot%202023-06-01%20003949.png)

- Em đã tử bypass bằng file upload như sau:

![](./img_DT/Screenshot%202023-06-01%20004037.png)

- Nhưng sau khi upload xong server sẽ chủ động đổi tên file theo đúng định dạng và không thể thực thi được bằng php.

- Trên PHP 7.2.0, zip: // wrapper đã được giới thiệu để thao tác với các tệp nén zip.Có cấu trúc tham số sau: zip: /// filename_path # internal_filename trong đó filename_path là đường dẫn đến tệp độc hại và internal_filename là đường dẫn chứa tệp độc hại bên trong tệp ZIP đã xử lý. Trong quá trình khai thác, thông thường # sẽ được mã hóa bằng URL của nó Giá trị được mã hóa % 23.

- Việc  này có thể cho phép kẻ tấn công thiết kế một tệp ZIP độc hại có thể được tải lên máy chủ, chẳng hạn như hình ảnh đại diện hoặc sử dụng bất kỳ hệ thống tải lên tệp nào có sẵn trên trang web mục tiêu (php: zip: // wrapper thì không yêu cầu tệp zip có bất kỳ phần mở rộng cụ thể nào) được thực thi bởi lỗ hổng LFI.

- Từ đó, em thực hiện các bước sau và thực hiện đọc flag, mình có thể sử dụng reverse shell, nhưng em chưa thử:

![](./img_DT/Screenshot%202023-06-01%20004559.png)

![](./img_DT/Screenshot%202023-06-01%20004736.png)

## **Bài về lỗ hổng LFI và RCE bằng log apache**

![](./img_DT/Screenshot%202023-06-01%20012514.png)

- Khi mình vào trang web chung ta sẽ thấy phiên cookie như trên khi decode sang base64 ta sẽ được nội dung sau : `O:4:"Page":1:{s:4:"file";s:10:"index.html";}`

- Em đã thử đọc etc/passwd bằng cách encode cookie như sau thành base64 :`O:4:"Page":1:{s:4:"file";s:19:"../../../etc/passwd";}`

- Và chúng ta có thể đọc được nội dung trang web:

![](./img_DT/Screenshot%202023-06-01%20012955.png)

- Em sẽ thực hiện RCE bằng cách đọc log của nginx `/var/log/nginx/access.log`

![](./img_DT/Screenshot%202023-06-01%20013733.png)

- Từ đấy, em thực hiện RCE như sau:

![](./img_DT/Screenshot%202023-06-01%20014138.png)

![](./img_DT/Screenshot%202023-06-01%20014210.png)

- Từ đấy, em đã đọc được flag:

![](./img_DT/Screenshot%202023-06-01%20014308.png)

## **Bài về lỗ hổng SSRF**

```python
from flask import Flask, request, render_template
import advocate
import requests

app = Flask(__name__)
flag = open('flag.txt', 'r').read()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        r = requests.get(url)
        return render_template('index.html', result=r.text)
    return render_template('index.html')


@app.route('/flag')
def flag_page():
    if request.remote_addr == '127.0.0.1':
        return render_template('flag.html', FLAG=flag)

    else:
        return render_template('403.html'), 403


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1337)
```

- Sau khi đọc source chúng ta thấy trang web có chức năng khi ta nhập url nó sẽ gửi request đến và lấy nội dụng ở đây có một lỗ hổng ssrf là khi nếu chúng ta nhập url bằng địa chỉ localhost:1337 ta sẽ nhận được flag.

![](./img_DT/Screenshot%202023-06-01%20015231.png)

