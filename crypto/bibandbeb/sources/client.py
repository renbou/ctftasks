#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import socket
import hashlib
from Cryptodome.Random import random
from Cryptodome.Util import number
from Cryptodome.Cipher import Salsa20
import base64
from secret import flag
import crypt

LISTEN_PORT = 61976
HOSTNAME = 'localhost'
BITS = 2048
BYTES = (BITS + 7) // 8
START_WORD = b'priempriem'
END_WORD = b'koneckonec'

def intToBytes(number):
    return number.to_bytes(BYTES,byteorder = 'big')

def bytesToInt(b):
    return int.from_bytes(b,byteorder = 'big')

def readUntil(sock, until):
    res = b''
    while res[-len(until):] != until:
        c = sock.recv(1)
        res += c
    return res

def sendMessage(sock, number):
    sock.send(START_WORD+intToBytes(number)+END_WORD)

def sendData(sock, data):
    sock.send(START_WORD+data+END_WORD)

def recvMessage(sock):
    readUntil(sock, START_WORD)
    data = readUntil(sock, END_WORD)[:-len(END_WORD)]
    return bytesToInt(data)

def recvData(sock):
    readUntil(sock, START_WORD)
    data = readUntil(sock, END_WORD)[:-len(END_WORD)]
    return data

def encrypt(data, number):
    data = base64.b64encode(data.encode('utf-8'))
    seckey = hashlib.sha256(str(number).encode('utf-8')).digest()
    cipher = Salsa20.new(key=seckey)
    msg = cipher.nonce + cipher.encrypt(data)
    return base64.b64encode(msg)

def decrypt(data, number):
    enc = base64.b64decode(data)
    seckey = hashlib.sha256(str(number).encode('utf-8')).digest()
    nonce = enc[:8]
    cipher = Salsa20.new(key=seckey, nonce=nonce)
    ciphertext = enc[8:]
    plaintext = cipher.decrypt(ciphertext)
    return base64.b64decode(plaintext)

class bib():
    def __init__(self):
        self.p = number.getPrime(BITS)
        self.a = random.getrandbits(BITS) % self.p
        self.g = 2
        self.bibsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bibsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        self.bibsock.bind((socket.gethostbyname(HOSTNAME), LISTEN_PORT))
        self.bibsock.listen(1)
        bebsock, bebaddr = self.bibsock.accept()
        sendMessage(bebsock, self.p)
        sendMessage(bebsock, self.g)
        ag = pow(self.a, self.g, self.p)
        aga = pow(ag, self.a, self.p)
        sendMessage(bebsock, ag)
        sendMessage(bebsock, aga)
        agb = recvMessage(bebsock)
        key = pow(agb, self.a, self.p)
        sendData(bebsock, encrypt(flag, key))
        bebsock.close()

class beb():
    def __init__(self):
        self.b = random.getrandbits(BITS)
        self.bebsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.getprotobyname('TCP'))
    
    def run(self):
        self.bebsock.connect((socket.gethostbyname(HOSTNAME), LISTEN_PORT))
        p = recvMessage(self.bebsock)
        g = recvMessage(self.bebsock)
        ag = recvMessage(self.bebsock)
        aga = recvMessage(self.bebsock)
        agb = pow(ag, self.b, p)
        sendMessage(self.bebsock, agb)
        key = pow(aga, self.b, p)
        data = recvData(self.bebsock)
        flag = decrypt(data, key)
        print(flag)
    
who = 'bib'

if who == 'beb':
    beb = beb()
    beb.run()
elif who == 'bib':
    bib = bib()
    bib.run()
