# **Africa battle CTF 2023**

## **Web-Civilization**

- Ở trang web có đề cập cho chúng ta cách để đọc source trang web đó là `?source`

![](./img_Africa/Screenshot%202023-07-05%20173609.png)

- Sau khi truy vấn source ta nhận được source code như sau:

```php
<?php
require("./flag.php");
if(isset($_GET['source'])){
    highlight_file(__FILE__);  
}
if(isset($_GET['ami'])){
    $input = $_GET['ami'];
    $cigar = 'africacradlecivilization';
    if (preg_replace("/$cigar/",'',$input) === $cigar) {// có chức năng loại bỏ hết tất cả các chuỗi $cigar
        africa();
    }
}
include("home.html");
?>
```

- Vậy để thực hiện cách bypass với câu if trên tôi đã code ra một đoạn python tạo ra một chuỗi để bypass:

```python
s = "africacradlecivilization"
ami = ""
for i in range(0, len(s)):
    ami += s[i]+s
print(ami)
#Output: aafricacradlecivilizationfafricacradlecivilizationrafricacradlecivilizationiafricacradlecivilizationcafricacradlecivilizationaafricacradlecivilizationcafricacradlecivilizationrafricacradlecivilizationaafricacradlecivilizationdafricacradlecivilizationlafricacradlecivilizationeafricacradlecivilizationcafricacradlecivilizationiafricacradlecivilizationvafricacradlecivilizationiafricacradlecivilizationlafricacradlecivilizationiafricacradlecivilizationzafricacradlecivilizationaafricacradlecivilizationtafricacradlecivilizationiafricacradlecivilizationoafricacradlecivilizationnafricacradlecivilization
```

- Và chúng ta nhận được flag:

![](./img_Africa/Screenshot%202023-07-05%20173917.png)

## **Web-Own reality**

- Vì trang web gợi ý là khám phám nên tôi đã sử dụng công cụ `dirsearch` để scan các thư mục và tôi tìm đc thư mục `.git`:

![](./img_Africa/Screenshot%202023-07-05%20192534.png)

- Và tôi dùng công cụ [**git-dumper**](https://github.com/arthaud/git-dumper) để dump về máy của mình

![](./img_Africa/Screenshot%202023-07-05%20195427.png)

- Tôi kiểm tra git log thì có 2 lần đã commit và kiểm tra branch thì có 2 branch.

![](./img_Africa/Screenshot%202023-07-05%20195659.png)

- Tôi thực hiện kiểm tra sự khác nhau lần lượt các bước sau:
  - git checkout ff092a2d7c85f81a47131b7ef303ba8ece1a8492 -b flag
  - git switch -c flag
  - git diff a1346a3abab8f97748e5480b61eb6824d4692f44

- Và tôi nhận được mã morse như sau:

![](./img_Africa/Screenshot%202023-07-05%20195911.png)

- Sau khi đi code mã morse kia không thành công tôi lại nghĩ có một ý tưởng rằng dấu `. = 0 và _ = 1`. Từ đấy, tôi viết một đoạn python và decrypt nó sang chuỗi nhị phân:

```python
s = ".__..._..__...._.___._...___._...__.__...__.._._._....__._._._..._...__..____.__._._._._.__.___..__._.__.__.___..__.____.___.___.__.___.._._____.__..._..__._.._.___._...___..__._._____..__..__..___.....__._...__.._._.__.._._.__...._..__._....___.._.__..._...__._....__..._..__.___.__.._._.__.._._..__.._..__..__..__..__...__._._.__...._..__..._..__..__.__..__..__..._..__.._...__...__.__...__.__...._..__.__..__..__...__..__..__.._...__.___._____._"
ami = ""
for i in range(0, len(s)):
    if s[i] == '_':
        ami += '1'
    else:
        ami += '0'
print(ami)
//battleCTF{Unknown_bits_384eea49b417ee2ff5a13fbdcca6f327}
```
