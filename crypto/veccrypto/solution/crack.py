import numpy as np
import base64
import struct
from decimal import *
from copy import deepcopy

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

bytestoint = lambda x: (-1 if x[0] else 1) * int.from_bytes(x[1:], byteorder='big')
toint = lambda x: int(x.to_integral_exact())
pad = lambda x: x + bytes([16 - len(x) % 16]) * (16 - len(x) % 16)

def unpackint(data):
    bytelen = struct.unpack('I', data[:4])[0]
    x = bytestoint(data[4:4+bytelen+1])
    return data[4+bytelen+1:], x

#key = fourvec(64627752966164072058104173632958734839096778563911235821708246576644979377839, [Decimal('-38255401483294895915733797231974828483822760099209668761780011797100231421885'), Decimal('46950517440181084679975226784525245055805268784245813425136963791848879777231'), Decimal('-69418835033906439294900453597254644899395789368033314281124974137893645359457')])

def getblocks(data):
    data = deepcopy(data)
    blocks = []
    while len(data) != 0:
        data, a = unpackint(data)
        data, b = unpackint(data)
        data, c = unpackint(data)
        data, d = unpackint(data)
        blocks.append(fourvec(a, [b, c, d]))
    return blocks


sent = pad(b'aaaa')
received_sent = b'JAAAAABdqTQDiwtF+KI9C3TAREIPOtz7w+moJlJM8I+oWSXesqDlXsUkAAAAARjLT1xbk++WTgul/r9dkE04jxRWHg1+j62EiIqDtNx6dOARVSQAAAAANJwILQaPTGcBlTvtmaHzBq658m+HkOe49o3XQZ+HTpffv/74JAAAAAFNlgjAxLMpEXar6E/5hv+Rfy0h39pCatBNw6f7pWBdeva2Ges='
received_sent = base64.b64decode(received_sent)
received_vec = getblocks(received_sent)[0]
sent_vec = fourvec(struct.unpack('i', sent[:4])[0], \
                        [struct.unpack('i', sent[4:8])[0], struct.unpack('i', sent[8:12])[0], struct.unpack('i', sent[12:16])[0]])

key = received_vec.conj()/sent_vec

data = b'JAAAAADFyu7b/EwaSJ7ULae3+i6x2sA/hGBoQ+OcBWhajF3+lYTf/m8kAAAAAUeKAN0vC4rKRO8CrDbE1iKOqd9qqpu46T20ol+SPqj5HRJIyyQAAAAAwoLowBbOhUxgByiTq+041fSWFrPTtaS0VSbzgU+KXcX8QBpQJAAAAAAY6NiA0slim2wEeK1KZv4iflduRV0HMz0EyaUU017dWcOlclMkAAAAAHQU3EAkczssjWORXRExgTI5FVnPbX5QC5tzNaV1Vs5wJy2umCQAAAABKcvzXKOHU8RjG1VoIt8KCjVPrhZp1HFtrizrfVKIp4CkayYpJAAAAADlSXD644DDZC/xQRKpsL3iYRCWiEA2oJVhClUdxsT4Kc0Kef0kAAAAAAshuTWBTp1jd1JONSWvrhDS8Rj64ShdoPttzquU6HDZTIRd9CQAAAAAt1wp1JCd13B3X7m0R/gF+7uuQOuef0r7nGvdPt7mcF84swE6JAAAAAFAIhrsnUqo4rkfzrAHf114iXYo0VWcICpqAHki4k5vPtTAPi0kAAAAANvfnKtUp0mMI2ALOIpZ8G84SM8My6TULL/+9y+U8yn3ECj+bSQAAAAAQPj6bkKL6FHQ01O91wrt6h/07oSbc0hrDhprA4T62hXJXdS1JAAAAADkjx6OsHbjAGwFIT/GJc0T2cGZ0JFpzLjf9kePlXEseRSuSnwkAAAAARFUTL2dtfoYOvYjJMydl2dPsIkulGbwQUMP4z3egfDsSDwtkCQAAAAApopNbrsOcy0qfZGVt9Dg369IGqYgWEfjgKDD6oE+DHy4Z1a7JAAAAAAo3MPXX7uY1ccIzu+VmejOrWgiNCijaIrSr8fVtLqcoKAoUc0='
data = base64.b64decode(data)

blocks = getblocks(data)

resblocks = [i / key for i in blocks]
resdata = []
for i in resblocks:
    resdata.append(struct.pack('i', toint(i.a)))
    resdata.append(struct.pack('i', toint(i.vec[0])))
    resdata.append(struct.pack('i', toint(i.vec[1])))
    resdata.append(struct.pack('i', toint(i.vec[2])))

print('flag is {}'.format(b''.join(resdata)))