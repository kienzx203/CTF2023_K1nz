cipher = [0x01, 0x21, 0x31, 0x7d, 0x1d, 0x5d, 0x07,
          0x01, 0x63, 0x6e, 0x35, 0x5f, 0x4b, 0x23, 0x7e]

flag = ""
for j in range(0, 256):
    v2 = j
    v5 = 2606
    while (v5):
        for i in range(0, 15):
            v7 = v2 ^ cipher[i]
            v2 = cipher[i]
            flag += chr(v2)
        v5 -= 1
    if "ATTT" in flag:
        print(flag)
