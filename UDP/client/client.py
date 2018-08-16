import socket,time,math,os
import sys

BUFFER_SIZE = 10240

try:
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
except socket.error:
    print("failed to create udp socket")
    sys.exit()

try:
    host_name = socket.gethostname()
    ip = socket.gethostbyname(host_name)
    #print(host_name,ip)
    port = 8888
except IndexError:
    print("Error ip or port")
    sys.exit()

def get_file_from_server(file_name):     #向服务器请求file
    server_addr = (ip,port)
    complete_msc = "get".encode("utf-8")+b"|||"+file_name.encode("utf-8")
    s.sendto(complete_msc,server_addr)

    data, server_addr = s.recvfrom(BUFFER_SIZE)
    if data == b"file not found":
        print(file_name, "not found.exit")
        sys.exit()
    else:
        conuter1 = int(data.decode("utf-8"))        #第一次传块的数量来
        s.sendto("Sending file..".encode("utf-8"),server_addr)
        data, server_addr = s.recvfrom(BUFFER_SIZE)
        file_name = "received_"+file_name
        file_handler = open(file_name,"wb")
        while(conuter1 != 0):
            file_handler.write(data)
            file_handler.seek(0,1)
            conuter1 = conuter1-1
            s.sendto("next chunk".encode("utf-8"),server_addr)

            data, server_addr = s.recvfrom(BUFFER_SIZE)

            if(conuter1 == 0):
                print("file received totally!")

def send_file_to_server(file_name):
    server_addr = (ip, port)
    try:
        file_handler = open(file_name,"rb")
    except FileNotFoundError:
        print("\n",file_name,"doesn't exist\n")
        sys.exit()

    y = os.path.getsize(file_name)
    y = math.ceil(y/BUFFER_SIZE)
    chunk_size = y;
    complete_msg = "send".encode("utf-8")+b"|||"+file_name.encode("utf-8")+b"|||"+str(y).encode("utf-8")
    s.sendto(complete_msg,server_addr)

    data, server_addr = s.recvfrom(BUFFER_SIZE)
    while True:
        file_handler.seek(0,1)
        content = file_handler.read(BUFFER_SIZE)
        s.sendto(content,server_addr)

        data, server_addr = s.recvfrom(BUFFER_SIZE)

        y = y-1
        print("send chunk",chunk_size-y)
        if y == 0:
            print("put file totally")
            break

def list_files_from_server():
    server_addr = (ip, port)
    s.sendto("list".encode("utf-8"),server_addr)
    data, server_addr = s.recvfrom(BUFFER_SIZE)
    files = data.decode()
    file_list = files.split(" ")
    print(file_list)

def exit_server():
    server_addr = (ip, port)
    print("The server will be closed and you will exit.")
    s.sendto("exit".encode("utf-8"),server_addr)
    s.close()
    sys.exit()

if __name__=='__main__':
    while(1):
        try:
            print("\nEnter one of the following commands:\nget [file_name]\nsend [file_name]\nlist\nexit")
            command = input("Enter command here:")
            msg_ic = command.split()
            msg_ic[0] = msg_ic[0].lower()

            if msg_ic[0]=="get":
                get_file_from_server(msg_ic[1])
            elif msg_ic[0]=="send":
                send_file_to_server(msg_ic[1])
            elif msg_ic[0] == "list":
                list_files_from_server()
            elif msg_ic[0] == "exit":
                exit_server()
            else:
                print("\nPlease enter the correct command\n")
        except ConnectionRefusedError:
            print("Connextion Failed")
            sys.exit()
