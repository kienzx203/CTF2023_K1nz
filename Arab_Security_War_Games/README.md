# **Arab Security War Games Qualifications**

## **N1 - Easy 200 points**

- Sau khi kiểm tra trang web không thấy một chút thông tin gì để tôi có thể tấn công. Tôi sử dụng công cụ `dirbuster` tôi phát hiện ra có file `robots.txt`.

- Nội dung `robots.txt` như sau:

![](./img/Screenshot%202023-08-10%20224628.png)

- Tôi truy cập với đường dẫn trên kết quả `404`. Dường như nó không dễ dàng. 

- Sau khi đọc lại đề, đề bài đã gợi ý cho tôi tìm kiếm xâu bên trong trang web. Tôi sử dụng công cụ [`param-miner`](https://github.com/PortSwigger/param-miner) và may mắn tôi tìm ra một param là url.

![](./img/Screenshot%202023-08-10%20225119.png)

- Kết hợp với đường dẫn robots.txt tôi đã tìm được FLAG:

![](./img/Screenshot%202023-08-10%20225215.png)

## **Iniectio - Easy 300 points**

![](./img/Screenshot%202023-08-10%20225916.png)

- Tôi nhận ra đây là một trang tĩnh, nhưng đây là file PHP. Tôi cố găng nối thêm `~` xem mã nguồn có suốt hiện hay không và nó đã xuất hiện.

```php
<?php
  
  $dangerousFunctions = array('GET','POST','print','exec', 'shell_exec', 'popen', 'system', 'touch', 'echo', 'mv', 'cp', 'sed','``', 'passthru', 'proc_open', 'while', 'read ', '>', '<', 'nano', 'vi', 'vim', 'fopen', 'fgets', 'fgetc', 'file_get_contents', 'fwrite', 'file_put_contents', 'curl_exec', 'curl_multi_exec', 'parse_ini_file', 'sleep', 'rm', 'mkdir', '}', 'show_source', 'symlink', 'apache_child_terminate', 'apache_setenv', 'define_syslog_variables', 'escapeshellarg', 'escapeshellcmd', 'eval', 'pcntl_exec', 'posix_kill', 'posix_mkfifo', 'posix_setpgid', 'posix_setsid', 'posix_setuid', 'posix_uname', 'proc_close', 'proc_get_status', 'proc_nice', 'proc_terminate', 'putenv', 'register_shutdown_function', 'register_tick_function', 'ini_set', 'set_time_limit', 'set_include_path', 'header', 'mail', 'readfile', 'file_get_contents', 'file_put_contents', 'unlink', 'cat', 'tail', 'head', 'more', 'less', 'dd', 'od', 'xxd', 'tac', 'hexdump', 'file', 'awk', 'nano', 'vim', 'iconv', 'strings', 'rev', '|');

  $name = $_GET['name'];
  if (strlen($name) > 36) {
    die ("The name is too long.");
  }

  
  foreach ($dangerousFunctions as $func) {
    if (stripos($name, $func) !== false) {
      die("oooooooooooh hacker !");
    }
  }
?>

<!DOCTYPE html>
<html>
<head>
 <style>
    body {
      background-image: url("x.webp");
      background-repeat: no-repeat;
      background-size: cover;
      background-position: center center;
      height: 100vh;
      margin: 0;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    @media (max-width: 768px) {
      body {
        background-size: contain;
      }
    }
  </style> 
</head>
<body>
  <?php
    
   $str = "echo \"<div style='position: fixed; top: 0; left: 0;'><p style='font-size: x-large; color: white;'>Hello " . $name . "!!!</p></div>\";";




    eval($str);
  ?>
</body>
</html>

```

- Sau khi đọc source code ta nhận biết biến name đã đc filter. Chúng ta hãy chú ý đến hàm eval. Từ đấy, tôi có thể injection code như sau: `";$x='sys'.'tem';$x('ls');"`

![](./img/Screenshot%202023-08-10%20230627.png)

## **Father's Light - Medium 600 points**

- Ở đây trang web có chức năng đăng nhập.

![](./img/Screenshot%202023-08-10%20231818.png)

- Tôi đã thử gây ra một số lỗi và truyền vào thông tin đăng nhập. Tôi đã đọc được một số source code.

![](./img/Screenshot%202023-08-10%20232350.png)
![](./img/Screenshot%202023-08-10%20232506.png)

- chúng tôi có một dòng khác chứa thông tin đăng nhập để đăng nhập. Khi chúng tôi đăng nhập, chúng tôi đã được chuyển hướng đến `/user`. Sau khi chuyện hướng đến tôi đã nhận được một mã JWT. Ý tưởng trong đâu của tôi là thử crack secret của JWT và nó đã thành công như sau:

![](./img/Screenshot%202023-08-10%20232729.png)

- Và sau khi crack jwt trang hiện ra như sau:

![](./img/Screenshot%202023-08-10%20232912.png)


- Không có gì khác thay đổi nhưng chúng tôi không phải là quản trị viên, vì vậy hãy tìm kiếm các điểm cuối chỉ dành cho quản trị viên có thể truy cập được. Brute buộc các thư mục chúng tôi nhận được 3 điểm cuối.

    - `/dashboard`
    - `/console`
    - `/admin`

- Tôi chuyển hướng tới `/dashboard` 

![](./img/Screenshot%202023-08-10%20233613.png)

- Tôi thực hiện nhập lỗi và chúng ta đọc được một đoạn source code như sau:

```python
def template():
    if request.method == 'GET':
        return redirect(url_for('dashboard'))
    if 'username' in session_for_template and session_for_template['is_admin']:
        if request.method == 'POST':
            name = request.form['name']
            pattern = r'\b(bash|sh|nc|netcat|python|perl|ruby|ncat|python|curl|wget|__subclasses__|read()|__class__|/etc/passwd|/|write|__import__|popen|__init__|_TemplateReference__context|__globals__|__init__|for|from_pyfile|bin|shell|RUNCMD|request.__class__|request|attr|{{request.__class__}}|join|application|config.items)\b'
            if re.search(pattern, name) or name.lower() == "{{config}}":
                alert_message = "Againnn ?? Do You think you can Hack My Applicationnnnnnnn!!!"
                return render_template('index.html', alert_message=alert_message)
            else:
```

- Từ đấy, chúng ta có thể khai thác như sau:

![](./img/Screenshot%202023-08-10%20233812.png)

## **SadQL - Medium 600 points**

- Ở trang web này tiêu đề cũng đã gợi ý cho chúng ta owe đây tồn tại lỗ hổng SQL injection

![](./img/Screenshot%202023-08-10%20235950.png)

- Sau một thời gian injection không thành công. Tôi thử với đăng nhập lỗi và thấy một số error:

![](./img/Screenshot%202023-08-11%20000155.png)

- Lỗi chỉ ra rằng hàm addlashes() trong PHP được sử dụng để thoát đầu vào của chúng tôi, vì vậy chúng tôi không thể ngắt truy vấn. Tôi đã tìm thấy [`blog`](https://www.openbugbounty.org/blog/_r00t1ng_/bypass-addslashes-using-multibyte-character/) tuyệt vời này giải thích cách bỏ qua chức năng này. Đó là một cách bỏ qua khá phổ biến bằng cách sử dụng các ký tự GBK, là một ký tự nhiều byte để đánh lừa hàm addlashes().

![](./img/Screenshot%202023-08-11%20000503.png)

- Hoặc thực hiện input như sau: `admin%bf%5C%27OorR/**/1!=2;#`

## **Blind - Medium 600 points**

- Đề bài mô tả nó yêu cầu chúng tôi nâng cấp đặc quyền của mình và trở thành giám đốc (quản trị viên).

![](./img/Screenshot%202023-08-11%20225252.png)

- Sau khi đăng nhập thành công chúng ta thấy có chức năng cập nhật profile

![](./img/Screenshot%202023-08-11%20225738.png)

- Lỗ hổng là chức năng cập nhật có SQL injection giống hệt như thử thách SadQL. Vì vậy, tôi đã dành hàng giờ cố gắng lấy mật khẩu quản trị viên hoặc đại loại như vậy nhưng không gặp may. Tôi gần như đã bỏ cuộc nhưng đã thử một điều cuối cùng trước khi đi ngủ :"D, tôi đã thử cung cấp thêm một tham số trong chức năng cập nhật, như thế này..

![](./img/Screenshot%202023-08-11%20230606.png)
![](./img/Screenshot%202023-08-11%20230635.png)
## **Gr00t - Medium 900 points**

![](./img/Screenshot%202023-08-11%20231420.png)

- Sau khi truy cập trang web chúng ra có 2 trang có thể truy cập `index.php và groot.php`

- Chúng ta đi phân tích từng source trang web

> `index.php`

![](./img/Screenshot%202023-08-11%20232938.png)

- Như ta đã thấy trang web sử dụng CSP và sử dụng thanh gi iframe.

- Tôi sẽ giải thích sơ qua CSP trên:
```html
`<meta http-equiv="Content-Security-Policy" content="...">` là một thẻ HTML được sử dụng để thiết lập chính sách an ninh nội dung (Content Security Policy - CSP) cho một trang web. Chính sách an ninh nội dung được sử dụng để xác định các nguồn và loại tài nguyên nội dung nào được phép được tải trong trang web, như script, style, font, image, iframe, v.v.

Trong thẻ `<meta http-equiv="Content-Security-Policy">` mà bạn cung cấp, có hai phần chính:

1. `script-src 'unsafe-eval' 'self';`: Đây là phần quy định các nguồn được phép cung cấp script cho trang web. `'unsafe-eval'` cho phép sử dụng `eval()` và tương tự, `'self'` cho phép sử dụng script từ cùng một nguồn (trang web đang hiển thị).

2. `object-src 'none'`: Đây là phần quy định các nguồn được phép cung cấp object (như `<object>`, `<embed>`, ...). `'none'` nghĩa là không cho phép tải các object từ bất kỳ nguồn nào.

Những quy định này giúp hạn chế các lỗ hổng bảo mật liên quan đến việc tải và thực thi mã động (như JavaScript) và đối tượng động (như Flash) từ các nguồn không an toàn.

Tuy nhiên, `'unsafe-eval'` có thể mở cửa sẽ tạo ra một lỗ hổng bảo mật, vì nó cho phép thực thi mã bằng cách sử dụng `eval()` và tương tự. Nên hạn chế việc sử dụng `'unsafe-eval'` trong CSP.

Trong tổng quan, thẻ `<meta http-equiv="Content-Security-Policy">` giúp bạn xác định cách trình duyệt xử lý các nguồn nội dung của trang web, tạo ra một lớp bảo vệ bổ sung để ngăn chặn các cuộc tấn công liên quan đến mã động và các nguồn không an toàn.
```

- Chúng ta đi kiểm tra `frame.js`

![](./img/Screenshot%202023-08-11%20234716.png)

- Chúng ta đi kiểm tra `main.js`

![](./img/Screenshot%202023-08-11%20235138.png)

- Khi chúng ta nhấp vào nút Let's go, dữ liệu đầu vào được gửi qua hàm postMessage tới frame.html sẽ được chuyển đến HTML bên trong.

- Tôi đã thực hiện build ở local để thử khai thác:

```html
<!DOCTYPE html>
<html>
<head>
    <title>XSS PoC</title>
 <meta charset="utf-8" />
</head>
<body>
 <iframe name="frame" src="<http://127.0.0.1:9090/groot/frame.html>" onload="sendMessage()"></iframe>
<script>
  
function sendMessage(){
    
    let msg = 'ASCWG_2023'
    frame.postMessage(msg, '*');
    
}
</script>
</body>
</html>
```
![](./img/Screenshot%202023-08-12%20000401.png)

- Nhưng khi tôi thử với `msg` là script thì nó không hoạt động. Vì nó đã được bảo vệ bởi `CSP`.

- Sau khi tìm kiếm, tôi phát hiện ra rằng `InnerHTML` không thực thi các thẻ tập lệnh.

- Do đó, để tránh bất kỳ sự cố nào với `InnerHTML`, chúng ta cần sử dụng một kỹ thuật gọi là `đóng gói (encapsulation).`

- Điều này liên quan đến việc đặt thẻ tập lệnh của chúng tôi bên trong một thẻ khác không ảnh hưởng đến `InnerHTML`. Thẻ phù hợp nhất cho mục đích này là thẻ iframe.
 
- Tuy nhiên, nếu chúng tôi cố gắng đặt thuộc tính src của iframe thành một miền khác, điều đó sẽ dẫn đến việc thực thi tập lệnh chéo trang (XSS) trên miền đích.

- May mắn thay, thẻ iframe có một thuộc tính hữu ích được gọi là srcdoc, thuộc tính này có thể được sử dụng thay cho thuộc tính src.

- Thuộc tính này cho phép chúng tôi nhúng HTML, bao gồm các thẻ tập lệnh, trực tiếp bên trong nội dung của khung nội tuyến bằng cách sử dụng `InnerHTML`.

![](./img/Screenshot%202023-08-12%20001156.png)

- Tôi thử tấn công như sau: `<iframe srcdoc="<html><script src=main.js></script></html>"></iframe>`

![](./img/Screenshot%202023-08-12%20001345.png)

- Và nó đã thành công.

> `Tôi thực hiện tấn công bằng Angular sandbox escape`

![](./img/Screenshot%202023-08-12%20001727.png)
![](./img/Screenshot%202023-08-12%20001645.png)
![](./img/Screenshot%202023-08-12%20001811.png)
- Flag nhận được : `ASCWG{Y0u_aRe_3_Gr33T_P!3Y3R}`



## **Bugs need Hug - Medium 900 points**

![](./img/Screenshot%202023-08-11%20231312.png)