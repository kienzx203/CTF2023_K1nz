import requests
import websocket
import threading
import time

# Thông tin cần thiết
server_url = "http://localhost:1337/api/register"
websocket_url = "http://localhost:1337/socket.io/?EIO=4&transport=polling&t=OjiuONR&sid=oQ3bK5BIH7hqiWx3AAAg"


def http_request():
    json_data = {
        "email": "K1nz@example.com",
    }
    response = requests.post(server_url, json=json_data)

    if response.status_code == 200:
        print("Yêu cầu HTTP thành công!")
    else:
        print(
            f"Yêu cầu HTTP thất bại với mã trạng thái: {response.status_code}")


def on_message(ws, message):
    print(f"Received message from WebSocket: {message}")
    # Thực hiện xử lý dữ liệu từ server ở đây


def websocket_listener():
    ws = websocket.WebSocketApp(websocket_url, on_message=on_message)
    ws.run_forever()


# Bắt đầu một luồng cho kết nối WebSocket
websocket_thread = threading.Thread(target=websocket_listener)
# Sẽ tắt thread tự động khi chương trình chính kết thúc
websocket_thread.daemon = True
websocket_thread.start()

# Thực hiện yêu cầu HTTP
http_request()

# Giữ chương trình chạy để duy trì kết nối WebSocket
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
