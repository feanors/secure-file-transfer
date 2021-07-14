import socket
import cipher
import os
import random
import sys
import transfer_protocol
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def init_session(HOST, PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s

def init_sk_iv():
    session_key = os.urandom(32)
    iv = random.randint(0,123)
    return session_key, iv

def init_cipher(sk_iv_tuple):
    return cipher.AES_cipher(sk_iv_tuple[0], sk_iv_tuple[1])

def send_sk_iv(cipher, s):
    transfer_protocol.send_sk_iv(cipher, s)

def recieve_sk_iv(conn):
    return transfer_protocol.recieve_sk_iv(conn)

def get_file_metadata(s):
    return transfer_protocol.get_file_metadata(s)

def send_file_metadata(conn, file_len):
    transfer_protocol.send_file_metadata(conn, file_len)

def get_file_name(conn):
    return transfer_protocol.get_file_name(conn)

def send_file_name(s, file_name):
    transfer_protocol.send_file_name(s, file_name)

def request_missing_block(s, block_num):
    transfer_protocol.send_missing_block_num(s, block_num)

def ack_missing_block_request(conn):
    return transfer_protocol.recv_missing_block_info(conn)

def send_request(s, selection):
    transfer_protocol.send_request(s, selection)

def recieve_request(conn):
    return transfer_protocol.recieve_request(conn)

