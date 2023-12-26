import pandas as pd

a = []
b = []
f = open("D:/web/web/thuchanh/web_exploit/SVATTT/CRY2/cipher.txt", "r")
for line in f:
    line = line.strip()  # remove leading/trailing whitespace
    if line not in a:
        a.append(line)
        b.append(1)
    else:
        b[a.index(line)] += 1

sum = 0
for i in b:
    sum += i
print(sum)

d = ["E", "A", "R", "I", "O", "T", "N", "S", "L", "C", "U", "D", "P", "M", "H", "G", "B", "F", "Y", "W",
     "K", "V", "X", "Z", "J", "Q", ".", ",", "-", "_", "{", "}"]

c = []
for i in b:
    c.append(i / sum * 100)

df = pd.DataFrame({'Ciphertext': a, 'Appear': b, 'Frequency': c})
df = df.sort_values('Appear', ascending=[False])
df['Alphabet'] = d
print(df)
