import socket
import os
import sys
import packet
import cipher
import transfer_protocol
import control_protocol
import random
import file_io

faulty_packets = []
file_dict = {}

def create_client_cipher():
    return control_protocol.init_cipher(control_protocol.init_sk_iv())

def create_client_socket():
    return control_protocol.init_session("127.0.0.1", 65432)

def client_send_cipher_info(c, s):
    control_protocol.send_sk_iv(c, s)

def check_packet_integrity(packet):
    if(packet.check_md5() == False):
        faulty_packets.append(packet.block_num)

def modify_packet_for_testing(packet):
    packet.data = (packet.data.decode("utf-8")[0:6] + 'l' + packet.data.decode("utf-8")[7:]).encode("utf-8")
    return packet

def delete_packet_for_testing(delete_array):
    global file_dict
    for i in delete_array:
        del file_dict[i]


def get_user_action():
    print("\n\nPress 1) Initiate a session with the local host")
    print("Press 2) Exchange session key")
    print("Press 3) Get file data")
    print("Press 4) Request a missing block")
    print("Press 5) End the current session")
    print("Press 10) Modify or delete packets\n\n")

    user_input = int(input("Enter your selection: "))
    if(user_input not in (1,2,3,4,5,10)):
        print("Invalid input, please enter again")
        return -1
    else:
        return user_input

def find_missing_packets(data_len):
    global faulty_packets
    for i in range(data_len):
        if(i not in file_dict.keys()):
            faulty_packets.append(i)
    faulty_packets = list(dict.fromkeys(faulty_packets))


def fix_missing(s, c, selected_block):
    control_protocol.request_missing_block(s, selected_block)
    packet = transfer_protocol.receive_packet(s, c)
    file_dict[packet.block_num] = packet.data
    print("Packet received")
    faulty_packets.remove(selected_block)

def check_if_complete(data_len):
    if(len(faulty_packets) == 0):
        print("All packets arrived succesfully, writing to file")
        file_io.write_packets_to_file(data_len, file_dict)
    else:
        print("The following blocks are either damaged or missing, you can re-request those blocks")
        print(faulty_packets)

def write_blocks_to_dict(data_len,s,c, modify_array):
    global file_dict
    for i in range(data_len):
        packet = transfer_protocol.receive_packet(s, c)
        file_dict[packet.block_num] = packet.data
        if(i in modify_array):
            packet = modify_packet_for_testing(packet)
        check_packet_integrity(packet)


def main():

    print("\n\nIf you want to delete or modify a packet, do it before recieving the packet from the server...")
    print("... as they are checked instantly after recieving packets, and packets are written to file if all are okay")
    print("You also can't exchange a sesion key without first connecting, and can't get file data without exchanging keys")
    print("After every action there will be a text saying press anything to continue\n\n")
    input("Press anything to continue")

    global faulty_packets
    global file_dict
    data_len = 0
    initiated_flag = False
    exchanged_flag = False
    file_received = False
    user_selection = 1
    s = ""
    c = ""
    modify_array = []
    delete_array = []

    while(user_selection != 5):
        
        user_selection = get_user_action()
        if(user_selection == -1):
            continue
            

        if(user_selection == 1 and initiated_flag == False):
            initiated_flag = True
            print("Connection initiated")
            s = create_client_socket()
        
        if(user_selection == 2 and exchanged_flag == False and initiated_flag):
            exchanged_flag = True
            control_protocol.send_request(s, user_selection)
            c = create_client_cipher()
            print("Session key exchanged")
            client_send_cipher_info(c, s)

        if(user_selection == 3 and exchanged_flag and initiated_flag):
            file_received = True
            file_name = input("Enter file name: ")
            control_protocol.send_request(s, user_selection)
            control_protocol.send_file_name(s,file_name)
            data_len = control_protocol.get_file_metadata(s)
           
            write_blocks_to_dict(data_len, s, c, modify_array)
            delete_packet_for_testing(delete_array)

            find_missing_packets(data_len)
            check_if_complete(data_len)

        if(user_selection == 4 and exchanged_flag and initiated_flag and file_received and len(faulty_packets) > 0):
            selected_block = int(input("Enter the block number you want to recover: "))
            if(selected_block in faulty_packets):
                control_protocol.send_request(s, user_selection)
                fix_missing(s, c, selected_block)
            else:
                print("That packet already exists")

            check_if_complete(data_len)


        if(user_selection == 5):
            control_protocol.send_request(s, user_selection)
            s.close()

        if(user_selection == 10 and file_received == False):
            mod_count = int(input("\n\nEnter how many packets you want to modify :"))
            print()

            for i in range(mod_count):
                modify_array.append(int(input("Enter the blocknumber you want to modify: ")))

            del_count = int(input("\n\nEnter how many packets you want to delete :"))
            print()
            
            for i in range(del_count):
                delete_array.append(int(input("Enter the blocknumber you want to delete: ")))


if __name__ == "__main__":
    main()