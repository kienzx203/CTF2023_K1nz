# **DeconstruCT.F**

## **Web1-where-are-the-cookies**

- Ở đây trang web đã gợi ý cho chúng ta biết bài ra có liên quan cookie. Vậy việc đầu tiên chúng ta sẽ kiểm tra robots.txt

![](./img_decon/Screenshot%202023-08-05%20205012.png)

- Sau khi truy nhập đường link chúng ta nhận được cookie `caniseethecookie = bm8==;` . Đó một đoạn mã base63 và decode đoạn mã ấy chúng ta được 'no'. Và tôi đã thay đổi thành 'yes' và encode. Chúng ta sẽ nhận được flag như sau:

![](./img_decon/Screenshot%202023-08-05%20205233.png)


## **Web2-why-are-types-weird**

- Khi truy cập vào chúng ta có một trang web đăng nhập

![](./img_decon/Screenshot%202023-08-12%20100217.png)


- Điều chúng ta cần làm ở đây là đăng nhập admin.

- Với tiêu đề của challenge tôi đã nghĩ đến [`PHP Type Juggling`](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Type%20Juggling/README.md)

- Sau khi thử một số giá trị băm, tôi đã tìm thấy một giá trị hợp lệ: `10932435112`. Số ma thuật này có giá trị băm là `0e07766915004133176347055865026311692244` với thuật toán SHA1 và cho phép tôi kết nối với tư cách quản trị viên.

- Sau đó tôi đã truy cập được trang admin như sau:

![](./img_decon/Screenshot%202023-08-12%20100934.png)

- Ở đây dường như lỗi sql injection errorbase. Tôi đã thử nhập input lỗi và nhận thầy rằng trang web đã dùng `SQLite3`.

```
Warning: SQLite3::query(): Unable to prepare statement: 1, incomplete input in /var/www/html/read_details.php on line 8
```

- Sau đó tôi đã thử với tân công union như sau: `1 union SELECT sql, 1, 1 FROM sqlite_schema`

![](./img_decon/Screenshot%202023-08-12%20102121.png)

- Tôi truy cập vào table `power_users` với câu truy vấn: `1 union SELECT id, username, password FROM power_users`. Vậy flag: `dsc{tYp3_juGgl1nG_i5_cr4zY}`

![](./img_decon/Screenshot%202023-08-12%20102315.png)

## **Web3-gitcha**

- Đề bài đã gợi ý cho chúng ta có thể đọc được file git.

![](./img_decon/Screenshot%202023-08-12%20144024.png)

- Tôi sử dụng công cụ `git-dumper` để dump ra;

```
$ python3 /home/michel/Desktop/CTF/Tools/WEB/git-dumper/git_dumper.py https://ch28744128075.ch.eng.run/.git/ git
[-] Testing https://ch28744128075.ch.eng.run/.git/HEAD [200]
[-] Testing https://ch28744128075.ch.eng.run/.git/ [200]
[-] Fetching common files
[-] Fetching https://ch28744128075.ch.eng.run/.gitignore [404]
...
[-] Fetching https://ch28744128075.ch.eng.run/.git/objects/b5/e3f89e84b3ff0a2d3941ff52aceb7233e156d0 [200]
[-] Running git checkout .
```

- Bây giờ chúng ta vào bên trong thư mục .git và tìm thấy flag.txt ở thư mục gốc của dự án và thông tin hữu ích bên trong index.js:

```javascript
const checkAdmin = (req, res) => {
  if (req.cookies["SECRET_COOKIE_VALUE"] === "thisisahugesecret") {
 return true;
  }
  return false;
};
```

- khi chúng tôi là quản trị viên, chúng tôi có thể truy cập vào /supersecret nơi chúng tôi có thể thêm ghi chú.

![](./img_decon/Screenshot%202023-08-12%20154221.png)

- Ở đây có một lỗ hổng `NodeJS Server Side Template Injection`. Tôi thực hiện tấn công như sau:

![](./img_decon/Screenshot%202023-08-12%20154324.png)

- `dsc{g1t_enum3r4ti0n_4nD_sSt1}`


## **Web4-debugzero**

- Sau khi truy nhập trang web chúng ta biết trang web được code bằng framework python.

- Đọc source code html chúng ta nhận được comment như sau:

```
  <!-- John, please don't run the app in debug mode, how many times do I have to tell you this! -->
```

- Tôi đã truy cập vào giao diện gỡ lỗi Flask bằng cách truy cập /console, nhưng bảng điều khiển được bảo vệ bằng mã PIN:

- Chúng tôi đã thực hiện một số nghiên cứu để tìm cách bypass PIN và tìm thấy một số bài viết về nó:

    - [`Werkzeug / Flask Debug - HackTricks`](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/werkzeug)
    - [`Werkzeug Console Pin Exploit - grav3m1nd-byte`](https://github.com/grav3m1nd-byte/werkzeug-pin)

- Đọc file css ta nhận được mã PIN như sau:

```
/* Nothing interesting here except this number - 934123 */

```

- Sau đó tôi thực hiện tấn công kết hợp với dự liệu đề cho FLAG nằm trong file flag.txt như sau:

![](./img_decon/Screenshot%202023-08-12%20155318.png)

- `dsc{n3veR_u53_d3BuG_m0d3}`