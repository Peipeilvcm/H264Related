import socket,sys,time,os,math

BUFFER_SIZE = 10240

try:
    port = 8888
except IndexError:
    print("Please enter a correct port number0.")
    sys.exit()

try:
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
except socket.error:
    print("failed to create socket.")
    sys.exit()

s.bind(("",port))

def command_get(client_addr,file_name):
    try:
        print("Sending File..")
        file_hander = open(file_name,"rb")
        x = os.path.getsize(file_name)
        x = math.ceil(x/BUFFER_SIZE)
        chunk_size = x
        s.sendto(str(x).encode("utf-8"),client_addr)    #传块的数量给客户端

        data, client_addr = s.recvfrom(BUFFER_SIZE)
        #print(data.decode("utf-8"))
        while(x != 0):
            file_hander.seek(0,1)   #文件指针当前位置
            content = file_hander.read(BUFFER_SIZE)
            s.sendto(content,client_addr)

            data, client_addr = s.recvfrom(BUFFER_SIZE)
            #print(data.decode("utf-8"))
            x = x-1
            print("send chunk ", chunk_size - x)
            if(x == 0):
                print("File sent totally")
                s.sendto("file received".encode("utf-8"),client_addr)

    except FileNotFoundError:
        print(file_name,"not found")
        s.sendto("file not found".encode(),client_addr)


def command_send(client_addr,file_name,counter):
    print("Receiving File..")
    s.sendto("Sending data".encode("utf-8"),client_addr)
    file_name = "get_from_client_"+file_name
    file_handler = open(file_name,"wb")
    while True:
        data, client_addr = s.recvfrom(BUFFER_SIZE)
        file_handler.write(data)
        file_handler.seek(0,1)
        counter = counter -1
        s.sendto("next chunk".encode("utf-8"),client_addr)
        if counter == 0:
            print("File Received.")
            break

def command_list(client_addr):
    path = os.getcwd()
    file_list = os.listdir(path)
    print("Sending File List\n",file_list)
    files = (" ".join(file_list)).encode("utf-8")
    s.sendto(files,client_addr)

def command_exit():
    print("Exit!!!")
    time.sleep(2)
    s.close()
    sys.exit()

if __name__=='__main__':
    while(1):
        print("waiting on port:",port)

        data, client_addr = s.recvfrom(BUFFER_SIZE)
        msg = data.split(b"|||")
        command = msg[0].decode("utf-8")

        if command == "get":
            command_get(client_addr,msg[1].decode("utf-8"))
        elif command == "send":
            command_send(client_addr,msg[1].decode("utf-8"),int(msg[2].decode("utf-8")))
        elif command == "list":
            command_list(client_addr)
        elif command == "exit":
            command_exit()
