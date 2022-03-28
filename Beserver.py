import threading
import socket
def server_loop():
    global target
    # 没有定义target的情况下
    if not len(target):
        target = "0.0.0.0"
    
    #监听对应端口
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(max_listenClient)
    print("listening on %s: %d"%(target,port))

    #新线程
    while True:
        client_socket,addr = server.accept()
        print("[*] Accepted connection from: %s:%d "%(addr[0],addr[1]))

        client_thread = threading.Thread(target=client_handler,args=(client_socket,))
        client_thread.start()
    
def client_handler(client_socket):
    global upload
    global execute
    global command

    #如果给定了本地保存的地址
    if(len(upload_destination)):
        file_buffer = ""
        #接收远程文件数据
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data
        #对接收的数据进行保存
        try:
            file_descriptor = open(upload_destination,"wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            information = "Successfully saved file to %s\r\n"%upload_destination

            client_socket.send(information.encode())
        except:
            information = "Failed to saved file to %s\r\n"%upload_destination

            client_socket.send(information.encode())
    if(len(execute)):
        output = run_command(execute)
        client_socket.send(output)
    if command:
        while True:
            information = "<NETTOOLS:#> "
            client_socket.send(information.encode())
            cmd_buffer = ""
            while ("\n" not in cmd_buffer):
                cmd_buffer += client_socket.recv(1024).decode()
                response = run_command(cmd_buffer)
                client_socket.send(response)