# **Amateurs_CTF**

| Challenge     | FLAG|
| ----------- | ----------- |
| [**web/waiting-an-eternity**](#webwaiting-an-eternity)      | `amateursCTF{im_g0iNg_2_s13Ep_foR_a_looo0ooO0oOooooOng_t1M3}`      |
| [**web/funny factorials**](#webfunny-factorials)  | `amateursCTF{h1tt1ng_th3_r3curs10n_l1mt_1s_1mp0ssibl3}`        |
| [**web/latek**](#weblatek)  | `amateursCTF{th3_l0w_budg3t_and_n0_1nstanc3ing_caus3d_us_t0_n0t_all0w_rc3_sadly}`|

#### **`Các challenge sau tôi ghi lại dưới sự tham khảo của tác giả khác`**

| Challenge     |
| ----------- |
| [**web/go-gopher**](#webwaiting-an-eternity)      |
| [**web/uwuctf**](#webfunny-factorials)        |
| [**web/sanity**](#weblatek)  |

[**`Link-tac-gia`**](https://gist.github.com/voxxal/fb69443f0a31bc6f2ddbce763d609935)

## **web/waiting-an-eternity**

![](./img_/Screenshot%202023-07-20%20113205.png)

- Ở đây sau khi chúng ta truy cập trang web chúng ta chú ý đến header sau:
`Refresh: 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000; url=/secret-site?secretcode=5770011ff65738feaf0c1d009caffb035651bb8a7e16799a433a301c0756003a`

- Vậy sau từng ấy giây nó sẽ chuyển hướng đến trang web sau:

![](./img_/Screenshot%202023-07-20%20113412.png)

- Tôi thực hiện setcookie: `Cookie: time=1689827636.9888983`

![](./img_/Screenshot%202023-07-20%20113517.png)

- Tôi liền nghĩ có thể challenge này nhằm múc đích tấn công làm tràn số trong float python. Tôi đã thử việc `cookie = -inf` và tôi đã thành công và có được flag.

![](./img_/Screenshot%202023-07-20%20113716.png)

## **web/funny factorials**

```python
def filter_path(path):
    # print(path)
    path = path.replace("../", "")
    try:
        return filter_path(path)
    except RecursionError:
        # remove root / from path if it exists
        if path[0] == "/":
            path = path[1:]
        print(path)
        return path


@app.route('/', methods=['POST'])
def calculate_factorial():
    safe_theme = filter_path(request.args.get("theme", "themes/theme1.css"))

    f = open(safe_theme, "r")
    theme = f.read()
    f.close()
    try:
        num = int(request.form['number'])
        if num < 0:
            error = "Invalid input: Please enter a non-negative integer."
            return render_template('index.html', error=error, css=theme)
        result = factorial(num)
        return render_template('index.html', result=result, css=theme)
    except ValueError:
        error = "Invalid input: Please enter a non-negative integer."
        return render_template('index.html', error=error, css=theme)
```

- Sau khi đọc code chúng ta đã thấy trang web có chức thay đổi dao diện trang web bằng cạch đọc trang css. Nhân cơ hội đó tôi có thể bypass để đọc file flag như sau:

![](./img_/Screenshot%202023-07-20%20115554.png)

## **web/latek**

- Ở đây trang web đã sử dụng latek để triển khai pdf.

![](./img_/Screenshot%202023-07-20%20115742.png)

- Sau khi tôi đọc [**tại liệu về latek**](https://devdocs.io/latex/_005cinput#index-_005cinput) tôi đã thấy có phương thức `/input` để đọc file.

- Tôi thực hiện đọc file `/etc/passwd`.

![](./img_/Screenshot%202023-07-20%20120131.png)

- Nó thông báo cho tôi thiếu kí tự `$`. Tôi đã thử thực hiện chèn thêm `$$` xem nó có hoạt động hay không.

![](./img_/Screenshot%202023-07-20%20120303.png)

- Cuối cùng nó đã thành công, và tôi đọc file flag như sau:

![](./img_/Screenshot%202023-07-20%20120422.png)

## **web/go-gopher**

![](./img_/Screenshot%202023-07-20%20125146.png)

## **web/uwuctf**

![](./img_/Screenshot%202023-07-20%20125751.png)

## **web/sanity**

![](./img_/Screenshot%202023-07-20%20125847.png)
