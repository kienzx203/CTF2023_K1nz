from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

KEY_LEN = 2
BS = 16
# Output:
# iv = 1df49bc50bc2432bd336b4609f2104f7
# ct = a40c6502436e3a21dd63c1553e4816967a75dfc0c7b90328f00af93f0094ed62

for i in range(65536):
    key = hex(i)[2:].zfill(4)
    key = bytes.fromhex(key)
    key = pad(key, BS)
    iv = " 1df49bc50bc2432bd336b4609f2104f7"
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = "a40c6502436e3a21dd63c1553e4816967a75dfc0c7b90328f00af93f0094ed62"
    ct = bytes.fromhex(ct)
    plaintext = cipher.decrypt(ct)
    if b'cvctf{' in plaintext:
        print(plaintext)
        exit()
