import hashlib
from string import printable
from time import time
import itertools
from array import array

ENCODING = "ascii"  # utf-8 for unicode support


class CharSet():
    def __init__(self, chars):
        chars = to_bytes(chars)
        self.chars = set(chars)
        self.first = chars[0]
        self.last = chars[-1]
        self.next = array("B", [0] * 256)
        for char, next_char in zip(chars, chars[1:]):
            self.next[char] = next_char

    def update_chars(self, new_chars):
        new_chars = to_bytes(new_chars)
        new_chars = set(new_chars) - self.chars
        if new_chars:  # if theres anything new
            self.chars |= new_chars
            new_chars = list(new_chars)
            self.next[self.last] = new_chars[0]
            self.last = new_chars[-1]
            for char, next_char in zip(new_chars, new_chars[1:]):
                self.next[char] = next_char

    def get_advance(self, arr, hash_):
        first = self.first
        last = self.last
        next_ = self.next

        def advance():
            for ind, byte in enumerate(arr):
                if byte == last:
                    arr[ind] = first
                else:
                    arr[ind] = next_[byte]
                    return hash_(arr)

            arr.append(first)
            return hash_(arr)

        return advance


class PasswordCracker():
    def __init__(self, hash_, chars=None):
        self.hash = hash_
        if chars is None:
            chars = printable
        self.char_set = CharSet(chars)

    def update_chars(self, string):
        self.char_set.update_chars(string)

    def crack(self, hashed):
        arr = bytearray()
        advance = self.char_set.get_advance(arr, self.hash)
        for _ in iter(advance, hashed):
            pass
        return arr


def to_bytes(string):
    if isinstance(string, str):
        return bytearray(string, ENCODING)
    elif isinstance(string, (bytes, bytearray)):
        return string
    else:
        raise TypeError(f"Cannot convert {string} to bytes")


def get_hasher(hash_):
    def hasher(bytes):
        return hash_(bytes).digest()

    return hasher


md5 = get_hasher(hashlib.md5)

cracker = PasswordCracker(md5)

password = input("Enter password: ")

cracker.update_chars(password)
password = md5(to_bytes(password))

start = time()
cracked = cracker.crack(password)
end = time()
print(f"Password cracked: {cracked.decode(ENCODING)}")
print(f"Time: {end - start} seconds.")
# 98371fd6630a26b9f04d623a6ea3d0af
# 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
