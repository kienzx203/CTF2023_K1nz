import requests

url = 'http://localhost:11111/api/load'

file_path = 'filesave.pkl'
proxies = {
    'https': 'https://127.0.0.1:8080'
}
with open(file_path, 'rb') as file:
    files = {'file': (file_path, file)}
    response = requests.post(url, files=files, proxies=proxies)

if response.status_code == 200:
    print("Upload thành công!")
    print("Nội dung:", response.text)
else:
    print("Upload thất bại. Mã lỗi:", response.status_code)
    print("Nội dung lỗi:", response.text)
