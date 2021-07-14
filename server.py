import socket
import packet
import cipher
import sys
import file_io
import transfer_protocol
import control_protocol

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP



HOST = '127.0.0.1'
PORT = 65432

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

key = RSA.generate(2048)
private_key = key.export_key()
file_out = open("private.pem", "wb")
file_out.write(private_key)
file_out.close()

public_key = key.publickey().export_key()
file_out = open("public.pem", "wb")
file_out.write(public_key)
file_out.close()


private_key = RSA.import_key(open("private.pem").read())
cipher_rsa = PKCS1_OAEP.new(private_key)

def create_server_cipher():
    return control_protocol.init_cipher(control_protocol.recieve_sk_iv(conn))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

while(True):

    s.listen()
    conn, addr = s.accept()
    print('Connected by', addr)
    keys_exchanged = False
    file_sent = False

    while (conn):
        request_type = control_protocol.recieve_request(conn)
        if(request_type == 2):
            c = create_server_cipher()
            keys_exchanged = True
        
        if(request_type == 3 and keys_exchanged):
            file_name = control_protocol.get_file_name(conn)
            data_arr = file_io.divide_file_to_blocks(file_name)
            control_protocol.send_file_metadata(conn, len(data_arr))

            for i in range(len(data_arr)):
                transfer_protocol.send_packet(data_arr[i], i, c, conn)
            file_sent = True
                

        if(request_type == 4 and keys_exchanged and file_sent):
            block_num = control_protocol.ack_missing_block_request(conn)
            transfer_protocol.send_packet(data_arr[block_num], block_num, c, conn)

        if(request_type == 5):
            conn.close()
            break
    


