import numpy as np
import base64
import struct
from Cryptodome.Random import random
from decimal import *
from secret import flag

BITS = 256
getcontext().prec = 4000

class fourvec():
    def __init__(self, a, b:list):
        self.a = Decimal(a)
        self.vec = np.array([Decimal(b[0]), Decimal(b[1]), Decimal(b[2])], dtype=Decimal)
    def __add__(self, other):
        return fourvec(self.a+other.a, self.vec+other.vec)
    def __sub__(self, other):
        return self.__add__(-other)
    def __neg__(self):
        return fourvec(-self.a, -self.vec)
    def inverse(self):
        sm = self.a*self.a + pow(self.vec, 2).sum()
        return fourvec(self.a / sm, self.vec / sm)
    def conj(self):
        return fourvec(self.a, -self.vec)
    def __mul__(self, other):
        return fourvec(self.a*other.a+np.dot(self.vec, other.vec), self.a*other.vec-other.a*self.vec+np.cross(self.vec, other.vec))
    def __truediv__(self, other):
        # if A*B = C then C/A = B but C/B =/= A
        resa = other.inverse().conj()
        return resa.__mul__(self)

toint = lambda x: int(x.to_integral_exact())
inttobytes = lambda x, y: bytes([x < 0]) + abs(x).to_bytes(y, byteorder='big')

pad = lambda x: x + bytes([(16 - len(x) % 16) % 16]) * ((16 - len(x) % 16) % 16)

def packint(x):
    bytelen = (int(x).bit_length() + 7) // 8
    return struct.pack('I', bytelen) + inttobytes(int(x), bytelen)

def encrypt(key, data):
    assert type(key) == fourvec
    if type(data) != bytes:
        data = data.encode('utf-8')
    data = pad(data)
    result = bytes()
    for i in range(0, len(data), 16):
        block = data[i:i+16]
        blockvec = fourvec(struct.unpack('i', block[:4])[0], \
                        [struct.unpack('i', block[4:8])[0], struct.unpack('i', block[8:12])[0], struct.unpack('i', block[12:16])[0]])
        encrypted = key*blockvec
        result += packint(toint(encrypted.a))
        for i in range(3):
            result += packint(toint(encrypted.vec[i]))
    result = base64.b64encode(bytes(result))
    return result

if __name__ == '__main__':
    signs = [random.getrandbits(1), \
        random.getrandbits(1), random.getrandbits(1), random.getrandbits(1)]
    key = [random.getrandbits(BITS), \
        random.getrandbits(BITS), random.getrandbits(BITS), random.getrandbits(BITS)]
    for i in range(4):
        if signs[i]:
            key[i] = -key[i]
    key = fourvec(key[0], [key[1], key[2], key[3]])
    # for debugging
    #print('key a: %d' % toint(key.a))
    #print('key vec: \n%s' % str(list(key.vec)))
    print('+---------------------------------------+')
    print('|Welcome to my supersecure block cipher |')
    print('|I love showing off so I wanted you to  |')
    print('|check out how secure this baby is! You |')
    print('|can try cracking it, but it\'s impossi- |')
    print('|ble! Here\'s your options mate:         |')
    print('|1 - get encrypted secret               |')
    print('|2 - encrypt your own data              |')
    print('+---------------------------------------+')
    try:
        while True:
            inp = int(input('Your choice: '))
            if inp not in set([1, 2]):
                print('Invalid choice bruv!')
            if inp == 1:
                print('Here\'s my secret: ')
                print(encrypt(key, flag))
            else:
                data = input('Input your data:\n')
                print('Here\'s your securely encrypted data:')
                print(encrypt(key, data))
            print()
    except:
        print('Damn.. you really had to do that? :(')