data = [101, 84, 0x54, 84, 173, 77, 0x65, 111, 167, 95, 0x6d, 101, 157, 119, 0x5f, 109, 145, 111, 0x77, 95, 155, 101, 0x6f, 119,
        137, 116, 0x72, 97, 137, 108, 0x61, 105, 137, 116, 0x61, 109, 137, 116, 0x72, 105, 137, 116, 0x6f, 105, 137, 100, 0x61, 121, 175]
s = ""


def OctalToDecimal(num):
    decimal_value = 0
    base = 1

    while num:
        last_digit = num % 10
        num = int(num / 10)
        decimal_value += last_digit * base
        base = base * 8
    return decimal_value


for i in range(len(data)):
    if i % 4 == 0:
        s += chr(OctalToDecimal(data[i]))
    else:
        s += chr(data[i])
print(s)
