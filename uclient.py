# -*- coding: utf-8 -*-
# ***   author:LC   ***
# created date：2022/3/28
# description：客户端代码 
_version = "0.1"
_updateDate = "2022/3/28"
import socket

_debugModel = False

# global variable
Listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def _debug_status(show = ""):
    print(show)
    print("listen = "+str(Listen))
    print("command = "+str(command))
    print("upload = "+str(upload))
    print("execute = "+str(execute))
    print("target = "+str(target))
    print("upload_dest = "+str(upload_destination))
    print("port = "+str(port))
    print("debugModel = "+str(_debugModel))
    print(" \n")

def openShell(opts = ""):
    #客户端控制
    #不是监听状态并且输入了目标ip和地址
    if (not Listen and len(target) and port >0):
        #print("buffer read!")
        #buffer = sys.stdin.read()
        #buffer = "ls"
        client_sender(opts)

#ip:port
def client_sender(buffer):
    #如果已经存在buffer
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((target,port))
        if(len(buffer)):
            client.send(buffer.encode())
        
        while True:
            recv_len = 1
            response = ""

            #一次读取4896字节
            while recv_len:
                data = client.recv(4896).decode()
                recv_len = len(data)
                response += data
                if recv_len < 4896:
                    break
            print (response)

            buffer = input("")
            #buffer += "\n"
            client.send(buffer.encode())
    except Exception as e:
        print("[*] Exception ! Exiting.")
        print(e)
    client.close()

