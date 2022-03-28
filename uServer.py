# -*- coding: utf-8 -*-
_version = "0.1"
_updateDate = "2022/3/28"

import threading
import socket
import subprocess


upload_destination = ""
port = 9999
max_listenClient = 5

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

def run_command(command):
    command = command.rstrip() #删除尾部空格
    #运行命令
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)

    except Exception as e:
        output = "failed to execute command.\r\n"
        output += e
        output = output.encode()

    #返回命令结果
    return output

def client_handler(client_socket):
    global execute
    global command
    

    #如果给定了保存的地址
    if(len(upload_destination)):
        file_buffer = ""
        #接收客户端的文件数据
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
        except:
            information = "Failed to saved file to %s\r\n"%upload_destination
        finally:
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