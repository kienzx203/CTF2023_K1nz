from pwn import *

conn = remote('challs.n00bzunit3d.xyz', 13541)

for e in range(0, 1000):
    c = conn.recvline()
    if b'n00bz{' in c:
        print(c)
        break
    c = conn.recvline()
    if b'n00bz{' in c:
        print(c)
        break
    if (e != 0):
        c = conn.recvline()
        if b'n00bz{' in c:
            print(c)
            break
    data = c.split()
    a = int(data[2].decode("utf-8").split("'")[0])
    b = int(data[5].decode("utf-8").split("?")[0])
    print(a, b)
    t = 500
    while t > 0:
        n, x = b, a
        d = 0
        for j in range(1, n):
            i = j
            while i != 0:
                if i % 10 == x:
                    d += 1
                i //= 10
        t -= 1
    str1 = bytes(str(d), 'UTF-8')
    print(str1)
    # exit()
    conn.send(str1)
    conn.send(b'\n')
