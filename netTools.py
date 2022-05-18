# -*- coding: utf-8 -*-
# ***   author:LC   ***
# created date：2022/3/28
# description：网络工具的控制端=w= 
import sys
import getopt

# Extensions
import server_connect
# 长格式如果加参数要加= 如 output= 
opt_list = ["help","listen","execute","target","port","command","upload","debug"]
# 后面1个冒号表示必需跟一个参数 参数紧跟在选项后或者以空格隔开 
short_opts = "hle:t:p:cu:"



def usage():
    """工具使用说明
    """
    print("NET工具盒子=w=:")
    #print(f"version:{uclient._version} updated data:{uclient._updateDate}")
    print("使用说明:")
    print("-h --help - 帮助信息喵")
    print("-l --listen - listen on[host]:[port]")
    print("-e --execute")
    print("-c --commandshell")
    print("-u --upload")
def listen_func(ip):
    """指定连接 

    Args:
        ip (_type_): _description_
    """
    pass

def upload_func(local_path,server_path):
    """上传功能

    Args:
        local_path (str): 本地路径
        server_path (str): 服务器的路径
    """

    pass

def panel():
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
            sys.exit()
        elif o in ("-l","--listen"):
            listen_func()
        elif o in ("-e","--execute"):
            uclient.execute = a
        elif o in ("-c","--commandshell"):
            uclient.command = True
        elif o in ("-u","--upload"):
            uclient.upload_destination = a
        elif o in ("-t","--target"):
            uclient.target = a
        elif o in ("-p","--port"):
            uclient.port = int(a)
        elif o in ("--debug"):
            uclient._debugModel = True
        else:
            assert False,"unhandled option"
    uclient._debug_status("main")
    #openShell()

def __debug__():
    print("listen = "+str(Listen))
    print("command = "+str(command))
    print("upload = "+str(upload))
    print("execute = "+str(execute))
    print("target = "+str(target))
    print("upload_dest = "+str(upload_destination))
    print("port = "+str(port))
    print("debugModel = "+str(_debugModel))
    print(" \n")

if __name__ == "main":
    panel()



 
