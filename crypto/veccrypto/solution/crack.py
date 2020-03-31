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

# вместо sent подставляем те байты которые мы послали серверу
sent = pad(b'aaaa')
# вместо received_sent подставляем те байты которые сервер выплюнул нам на запрос зашифровать свои данные
received_sent = b'JAAAAAAUbDEkCcWc8bzGMTBTA/MjKYOeXfj9IZNffm76HrVYFK/OBRUkAAAAAS5l2pkYl7ub0+70gtoIJrJ5vkU+SstDhCDmbhNbitWa1hyOMSQAAAAAJMO9l2QkZ8tcGfbSeZrD19PweyBNeQ4UbmYs7ktzNBqpAxiYJAAAAAArvWid6QOfwrrZA5JwZZizqimtfSb51oTBTuMd5ZMD4duOg+s='
received_sent = base64.b64decode(received_sent)
received_vec = getblocks(received_sent)[0]
sent_vec = fourvec(struct.unpack('i', sent[:4])[0], \
                        [struct.unpack('i', sent[4:8])[0], struct.unpack('i', sent[8:12])[0], struct.unpack('i', sent[12:16])[0]])

key = received_vec.conj()/sent_vec
# вместо data подставляем то что сервер выплюнул на запрос зашифровать флаг
data = b'JAAAAAABJSRiC903b+4q4Zc88QhR0UYKGU2GgcemmNvMxUEut61VXlckAAAAATiS+wVScJeRGlMOBTUg1BOxaB00Lw/mDS+U+9rJoT5lbO+GvyQAAAABBAQ8LlrLuYjgHGVQgbk7QVYQVLdLc2gilag+Lg7VGl5NTyT4JAAAAACYvdHIkLFqn3rYzbBxhWRhkMB5fZ49diM0OO6/TukgUipOPtUkAAAAABA6pSD0TgrU5WCl8o0JSaBx1HO126RQ0kizpHIx7fDgnB44CiQAAAABB1RROvBQNZKhzydS3zqGF+6EoQo9O5VQ2TUldytTiuZTBzgNJAAAAAAJfBULf7tbR1qBCPPEhG1FbYPaahrJrjX1FE0gysZQZJQC440kAAAAAJJHD26RGA4ArmE8mFeAOIDwwvpYU/mrk6jJYAP2NfX6DJ5FhiQAAAABAmKUkiIieZAKZBf5RZDOrDnZxbfF4vB9iTWXex9Kx5G0biKiJAAAAAEl4bMvsJ9Ixud4THL9fPluzxxMaeElwAw4ywkdDfocyF9HXEskAAAAARV0g/9+Un4UAwIOjF3FXLWTLvJY9pYliQtgHZKn9IACeqCtSyQAAAAApJXp53BwFWyvmLFYtuItj0XKGHiRCJbIRP6av+JjgkAnXWbRJAAAAAAXecc+sa/DL74wwQJk+wj5qrTODwaAfNKeXdkQRwpkAxR8g/QkAAAAAUdfFEiSmOC2JrV5r20YDWhqXNjgj3Cr0iRsDUAgbQpSQLevtCQAAAABHq59VLhww7UrmMD2GGoI2F7Pet4BprDEuq/RtLG/eIu8wkI3JAAAAACMbmA6CnO635XgCZE1NLRHsyJnHO1N4NTBHPmQcAIx8pgIahc='
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