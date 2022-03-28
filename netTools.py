# -*- coding: utf-8 -*-
# ***   author:LC   ***
# created date：2022/3/28
# description：网络工具的控制端=w= 
_version = "0.1"
_updateDate = "2022/3/28"

import subprocess
import sys
import getopt
import socket
import threading

# global variable
Listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0
opt_list = ["help","listen","execute","target","port","command","upload"]
short_opts = "hle:t:p:cu"
max_listenClient = 5

def _debug_status(show = ""):
    print(show)
    print("listen = "+str(Listen))
    print("command = "+str(command))
    print("upload = "+str(upload))
    print("execute = "+str(execute))
    print("target = "+str(target))
    print("upload_dest = "+str(upload_destination))
    print("port = "+str(port))
    print(" \n")

def usage():
    print("NET工具盒子=w=:")
    print("version:{0} updated data:{1}".format(_version,_updateDate))
    print("使用说明:")
    print("-h --help - 帮助信息喵")
    print("-l --listen - listen on[host]:[port]")
    print("-e --execute")
    print("-c --commandshell")
    print("-u --upload")

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
            buffer += "\n"
            client.send(buffer.encode())
    except Exception as e:
        print("[*] Exception ! Exiting.")
        print(e)
    client.close()

def openShell():
    #客户端控制
    #不是监听状态并且输入了目标ip和地址
    if (not Listen and len(target) and port >0):
        #print("buffer read!")
        #buffer = sys.stdin.read()
        buffer = "ls"
        client_sender(buffer)

def panel():
    global Listen
    global command
    global upload_destination
    global execute
    global target
    global port
    if not len(sys.argv[1:]):
        usage()
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],short_opts,opt_list)
        print(opts,args)
    except getopt.GetoptError as err:
        print (str(err))
        usage()
    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-l","--listen"):
            Listen = True
        elif o in ("-e","--execute"):
            execute = a
        elif o in ("-c","--commandshell"):
            command = True
        elif o in ("-u","--upload"):
            upload_destination = a
        elif o in ("-t","--target"):
            target = a
        elif o in ("-p","--port"):
            port = int(a)
        else:
            assert False,"unhandled option"
    openShell()


 
