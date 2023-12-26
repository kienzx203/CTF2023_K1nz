import asyncio
import websockets

# Hàm xử lý kết nối WebSocket


async def handle_websocket(websocket, path):
    async for message in websocket:
        # Xử lý tin nhắn từ kết nối WebSocket ở đây
        print(f"Received message: {message}")

# Tạo máy chủ WebSocket và lắng nghe trên tất cả cổng (0.0.0.0) và cổng 0
start_server = websockets.serve(handle_websocket, host="0.0.0.0", port=0)

# Lấy thông tin cổng máy chủ đã chọn tự động
server_address = start_server.sockets[0].getsockname()
print(f"Server is listening on {server_address}")

# Bắt đầu máy chủ WebSocket
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
