import sys
import hashlib
import cipher

class Packet:
    
    def __init__(self, block_num, hash, data):
        self.block_num = block_num
        self.hash = hash
        self.data = data
    
    def encrpy_packet_data(self, cipher):
        return self.block_num.to_bytes(16,sys.byteorder) + cipher.encrypt(self.hash, self.block_num) + cipher.encrypt(self.data, self.block_num)

    def check_md5(self):
        return hashlib.md5(self.data).digest() == self.hash

    @staticmethod
    def decode_decrypt_packet(incoming_packet, cipher):
        b = [incoming_packet[index : index + 16] for index in range(0, len(incoming_packet), 16)]
        block_num = int.from_bytes(b[0],sys.byteorder)
        hash = cipher.decrypt(b[1],block_num)
        data = cipher.decrypt(b[2],block_num)
        return block_num, hash, data

    @staticmethod
    def packet_from_parts(parts):
        return Packet(parts[0], parts[1], parts[2])

    @staticmethod
    def packet_factory(block_num, data):
        return Packet(block_num, hashlib.md5(data).digest(), data)
