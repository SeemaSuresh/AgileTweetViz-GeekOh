'''
This file has all the functions and classes which are being used at multiple places and is general in functionality
Author: Harsha Kadekar
Date: 10/02/2015
Reference: http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python -> For singleton classes
           http://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256 -> Encryption/Decryption algorithm
'''

import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random


class TweetVizSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(TweetVizSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TweetVizAESCipher:

    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()
        self.BS = 32

    def pad(self, s):
        return s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)

    def unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

    def encrypt( self, raw ):
        raw = self.pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return self.unpad(cipher.decrypt( enc[16:] ))