import packet
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def send_packet(block, block_num, cipher, conn):
    conn.sendall(packet.Packet.packet_factory(block_num, block).encrpy_packet_data(cipher))

def receive_packet(s, cipher):
    data = recvall(s, 48)
    return packet.Packet.packet_from_parts(packet.Packet.decode_decrypt_packet(data, cipher))

def recvall(connection_object, buffer_limit): #python doesnt have this for some reason?
    data = connection_object.recv(buffer_limit)
    while(len(data) != buffer_limit):
        data+= connection_object.recv(1)
    return data

def send_sk_iv(cipher, s):
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(open("public.pem").read()))
    s.sendall((cipher_rsa.encrypt(cipher.key)) + (cipher_rsa.encrypt((cipher.iv).to_bytes(16,sys.byteorder))))

def recieve_sk_iv(conn):
    incoming_data = recvall(conn,512)
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(open("private.pem").read()))
    return cipher_rsa.decrypt(incoming_data[:256]), int.from_bytes((cipher_rsa.decrypt(incoming_data[256:])), sys.byteorder)

def get_file_metadata(s):
    data = recvall(s, 16)
    return int.from_bytes(data, sys.byteorder)

def send_file_metadata(conn, file_len):
    conn.sendall(file_len.to_bytes(16,sys.byteorder))

def get_file_name(conn):
    file_name_char_len = int.from_bytes(recvall(conn,16), sys.byteorder)
    return recvall(conn, file_name_char_len).decode("utf-8")

def send_file_name(s, file_name):
    s.sendall(len(file_name).to_bytes(16,sys.byteorder))
    s.sendall(file_name.encode("utf-8"))

def send_missing_block_num(s, block_num):
    s.sendall(block_num.to_bytes(16,sys.byteorder))

def recv_missing_block_info(conn):
    return int.from_bytes(recvall(conn, 16),sys.byteorder)

def send_request(s, selection):
    s.sendall(selection.to_bytes(16,sys.byteorder))

def recieve_request(conn):
    return int.from_bytes(recvall(conn, 16),sys.byteorder)