from Crypto.Cipher import AES
import os
import binascii
import sys

class AES_cipher:

    def __init__(self, key, iv):
        self.key = key
        self.iv = iv
        self.cipher = AES.new(key,1)

    def xor_bytes(self, a, b):
        return (int.from_bytes(a, sys.byteorder) ^ int.from_bytes(b, sys.byteorder)).to_bytes(len(a),sys.byteorder)

    def encrypt(self, data, n):
        return self.xor_bytes(data, self.cipher.encrypt((self.iv+n).to_bytes(16,sys.byteorder)))

    def decrypt(self, cipher_text,n):
        return self.xor_bytes(cipher_text, self.cipher.encrypt((self.iv+n).to_bytes(16,sys.byteorder)))