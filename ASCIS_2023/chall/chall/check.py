def f_b(a, b):
    n = a << b | a >> (32 - b)
    return n
def f_c(a):
    