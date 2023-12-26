from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse
from sympy import divisors
from gmpy2 import is_prime
e = 65537
d = 47409517223849197923891137253648342022495427280216172836753733737836598856533
c = 28922782974963041022900967144272236971606170990861287861751602032656406857187
K = divisors(d*e - 1)
list_prime = []
for k in K:
    pp = ((d*e - 1)//k) + 1

    if is_prime(pp) and int(pp).bit_length() == 128:
        list_prime.append(pp)

list_text = []
for p in list_prime:
    for q in list_prime:
        if inverse(e, (p - 1) * (q - 1)) == d:
            n = p*q
            list_text.append(long_to_bytes(int(pow(c, d, n))))

print(list_text)
