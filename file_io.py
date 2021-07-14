def divide_file_to_blocks(fileName):
    inputFile = open(fileName,"r")
    fileData = inputFile.read()
    fileData = fileData.encode("utf-8")
    ret_array = ( [fileData[i:i+16] for i in range(0,len(fileData), 16)] )
    while(len(ret_array[len(ret_array)-1]) != 16):
        ret_array[-1] += b'g'
    return ret_array

def get_nth_block(packet_array, n):
    for i in range(len(packet_array)):
        if (i == n-1):
            return packet_array[i].replace("\\n","\n")

def remove_padding(byte_data):
    counter_of_padding = 0
    flag = False
    for i in reversed(byte_data.decode("utf-8")):
        if(i == 'g' and flag == False):
            counter_of_padding+=1
        else:
            flag = True
    return byte_data[:-counter_of_padding]

def write_packets_to_file(data_len, file_dict):
    file_dict[data_len-1] = remove_padding(file_dict[data_len-1])
    final_str = b''
    f = open("incoming.txt", "w")
    file_dict = sorted(file_dict.items())
    final_str = (b''.join(t[1] for t in file_dict)).decode("utf-8")
    f.write(final_str)
    f.close()